#!/usr/bin/env python3
"""Extract code.bin / exheader / exefs files / RomFS listing (optionally files) from a
decrypted (NoCrypto) NCSD .3ds image.  Pure python, no deps.

usage: extract.py <rom.3ds> <outdir> [--romfs-dump]
"""
import struct, sys, os, json, hashlib

MU = 0x200


def blz_decompress(d):
    """3DS backward-LZ (code.bin) decompressor."""
    bufboth, add = struct.unpack('<II', d[-8:])
    top = bufboth >> 24
    bottom = bufboth & 0xFFFFFF
    out = bytearray(len(d) + add)
    out[:len(d)] = d
    src = len(d) - top
    dst = len(out)
    end = len(d) - bottom
    while src > end:
        src -= 1
        flags = out[src]
        for _ in range(8):
            if src <= end:
                break
            if flags & 0x80:
                src -= 2
                v = out[src] | (out[src + 1] << 8)
                ln = (v >> 12) + 3
                disp = (v & 0xFFF) + 3
                for _ in range(ln):
                    dst -= 1
                    out[dst] = out[dst + disp]
            else:
                src -= 1
                dst -= 1
                out[dst] = out[src]
            flags = (flags << 1) & 0xFF
    return bytes(out)


def parse_exheader(exh):
    sci = exh[:0x200]
    def ci(o):
        a, pages, sz = struct.unpack('<III', sci[o:o + 12])
        return dict(addr=a, pages=pages, size=sz)
    deps = []
    for i in range(48):
        tid = struct.unpack('<Q', sci[0x40 + i * 8:0x48 + i * 8])[0]
        if tid:
            deps.append('%016X' % tid)
    aci = exh[0x200:0x400]
    prog_id = struct.unpack('<Q', aci[0:8])[0]
    core_ver = struct.unpack('<I', aci[8:12])[0]
    flag1, flag2, flag0, prio = aci[0xC], aci[0xD], aci[0xE], aci[0xF]
    # service access list at 0x50 (34 x 8 bytes)
    svcs = []
    for i in range(34):
        s = aci[0x50 + i * 8:0x58 + i * 8].rstrip(b'\0')
        if s:
            svcs.append(s.decode('ascii', 'replace'))
    # kernel caps at 0x170 (28 x u32)
    kcaps = list(struct.unpack('<28I', aci[0x170:0x170 + 0x70]))
    allowed_svcs = set()
    for c in kcaps:
        if (c >> 27) == 0b11110:  # syscall mask descriptor
            idx = (c >> 24) & 7
            for b in range(24):
                if c & (1 << b):
                    allowed_svcs.add(idx * 24 + b)
    return dict(
        title=sci[:8].rstrip(b'\0').decode('ascii', 'replace'),
        flags=sci[0xD], code_compressed=bool(sci[0xD] & 1), sd_app=bool(sci[0xD] & 2),
        remaster_version=struct.unpack('<H', sci[0xE:0x10])[0],
        text=ci(0x10), stack_size=struct.unpack('<I', sci[0x1C:0x20])[0],
        rodata=ci(0x20), data=ci(0x30), bss_size=struct.unpack('<I', sci[0x3C:0x40])[0],
        dependencies=deps,
        savedata_size=struct.unpack('<Q', sci[0x1C0:0x1C8])[0],
        jump_id='%016X' % struct.unpack('<Q', sci[0x1C8:0x1D0])[0],
        program_id='%016X' % prog_id, core_version=core_ver,
        aci_flags=[flag0, flag1, flag2], priority=prio,
        services=svcs, allowed_svcs=sorted(allowed_svcs),
        kernel_caps=['%08X' % c for c in kcaps if c != 0xFFFFFFFF],
    )


def romfs_walk(f, romfs_abs, dump_dir=None):
    f.seek(romfs_abs)
    ivfc = f.read(0x60)
    assert ivfc[:4] == b'IVFC', ivfc[:4]
    master_hash_size = struct.unpack('<I', ivfc[0x08:0x0C])[0]
    lvl3_bs_log2 = struct.unpack('<I', ivfc[0x4C:0x50])[0]
    bs = 1 << lvl3_bs_log2
    l3off = (0x60 + master_hash_size + bs - 1) & ~(bs - 1)
    l3 = romfs_abs + l3off
    f.seek(l3)
    h = struct.unpack('<10I', f.read(0x28))
    (hlen, dh_off, dh_len, dm_off, dm_len, fh_off, fh_len, fm_off, fm_len, fdata_off) = h
    f.seek(l3 + dm_off); dmeta = f.read(dm_len)
    f.seek(l3 + fm_off); fmeta = f.read(fm_len)
    files = []

    def read_dir(off, path):
        parent, sib, child, ffile, nxt, nlen = struct.unpack('<6I', dmeta[off:off + 0x18])
        name = dmeta[off + 0x18:off + 0x18 + nlen].decode('utf-16le')
        p = path + name + '/' if off else '/'
        fo = ffile
        while fo != 0xFFFFFFFF:
            fpar, fsib, doff, dsz, fnxt, fnlen = struct.unpack('<IIQQII', fmeta[fo:fo + 0x20])
            fname = fmeta[fo + 0x20:fo + 0x20 + fnlen].decode('utf-16le')
            files.append((p + fname, dsz, l3 + fdata_off + doff))
            fo = fsib
        c = child
        while c != 0xFFFFFFFF:
            read_dir(c, p)
            c = struct.unpack('<I', dmeta[c + 4:c + 8])[0]
    read_dir(0, '')
    if dump_dir:
        for p, sz, off in files:
            out = os.path.join(dump_dir, p.lstrip('/'))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            f.seek(off)
            with open(out, 'wb') as o:
                rem = sz
                while rem:
                    chunk = f.read(min(rem, 1 << 20)); o.write(chunk); rem -= len(chunk)
    return files


def main():
    rom, outdir = sys.argv[1], sys.argv[2]
    dump = '--romfs-dump' in sys.argv
    os.makedirs(outdir, exist_ok=True)
    f = open(rom, 'rb')
    hdr = f.read(0x200)
    assert hdr[0x100:0x104] == b'NCSD'
    p0off, p0len = struct.unpack('<II', hdr[0x120:0x128])
    base = p0off * MU
    f.seek(base)
    n = f.read(0x200)
    assert n[0x100:0x104] == b'NCCH'
    info = dict(
        ncsd_media_id='%016X' % struct.unpack('<Q', hdr[0x108:0x110])[0],
        product_code=n[0x150:0x160].rstrip(b'\0').decode(),
        ncch_version=struct.unpack('<H', n[0x112:0x114])[0],
        ncch_flags=n[0x188:0x190].hex(), nocrypto=bool(n[0x18F] & 4),
        partitions=[struct.unpack('<II', hdr[0x120 + i * 8:0x128 + i * 8]) for i in range(8)],
    )
    assert info['nocrypto'], 'encrypted ROM - not supported'
    exh_size = struct.unpack('<I', n[0x180:0x184])[0]
    exefs_off, exefs_len = struct.unpack('<II', n[0x1A0:0x1A8])
    romfs_off, romfs_len = struct.unpack('<II', n[0x1B0:0x1B8])
    f.seek(base + 0x200)
    exh = f.read(0x800)
    open(os.path.join(outdir, 'exheader.bin'), 'wb').write(exh)
    info['exheader'] = parse_exheader(exh)
    f.seek(base + exefs_off * MU)
    eh = f.read(0x200)
    efiles = {}
    for i in range(10):
        nm = eh[i * 16:i * 16 + 8].rstrip(b'\0').decode()
        off, sz = struct.unpack('<II', eh[i * 16 + 8:i * 16 + 16])
        if nm:
            efiles[nm] = (off, sz)
    info['exefs_files'] = {k: v[1] for k, v in efiles.items()}
    os.makedirs(os.path.join(outdir, 'exefs'), exist_ok=True)
    for nm, (off, sz) in efiles.items():
        f.seek(base + exefs_off * MU + 0x200 + off)
        d = f.read(sz)
        open(os.path.join(outdir, 'exefs', nm.lstrip('.') + '.bin'), 'wb').write(d)
        if nm == '.code':
            code = blz_decompress(d) if info['exheader']['code_compressed'] else d
            open(os.path.join(outdir, 'code.bin'), 'wb').write(code)
            info['code_bin_size'] = len(code)
            info['code_bin_sha1'] = hashlib.sha1(code).hexdigest()
            e = info['exheader']
            exp = e['text']['pages'] * 0x1000 + e['rodata']['pages'] * 0x1000 + e['data']['size']
            info['code_bin_expected_min'] = exp
    files = romfs_walk(f, base + romfs_off * MU, os.path.join(outdir, 'romfs') if dump else None)
    with open(os.path.join(outdir, 'romfs_listing.tsv'), 'w') as o:
        for p, sz, off in files:
            o.write('%s\t%d\n' % (p, sz))
    exts = {}
    for p, sz, off in files:
        e = os.path.splitext(p)[1].lower() or '(none)'
        c = exts.setdefault(e, [0, 0]); c[0] += 1; c[1] += sz
    info['romfs'] = dict(file_count=len(files), total_bytes=sum(s for _, s, _ in files),
                         by_ext=dict(sorted(exts.items(), key=lambda kv: -kv[1][1])),
                         dynamic_modules=[p for p, _, _ in files if p.lower().endswith(('.cro', '.crs', '.crr'))])
    json.dump(info, open(os.path.join(outdir, 'info.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in info.items() if k != 'romfs'}, indent=1))
    print('romfs files', len(files), 'dyn modules', info['romfs']['dynamic_modules'])


if __name__ == '__main__':
    main()
