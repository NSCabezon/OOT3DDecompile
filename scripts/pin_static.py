#!/usr/bin/env python3
"""Pin a C++ function-local static (guard word in .data, object in .bss) at its ROM addresses.

Image-neutral: the guard word is cut out of the raw data dump (proper data_chunks.txt split +
regenerated data .s, same generator as disassembly/tools/split_arm_data_chunks.py, no n3dsdisasm),
and data/oot3d.ld gets the regions that put the compiled guard/object back at the same addresses.

usage (tree = oot3d or ws/<name>, relative to decomp-spike or absolute):
  pin_static.py TREE split ADDR [--size N]
      Remove N bytes (default 4) at ADDR from the data chunk containing it (2-way split at a chunk edge,
      3-way in the middle: the new tail chunk is <base>_<ADDR+N> + GLOBAL_ASM line + ld region).
  pin_static.py TREE guard ADDR SELECTOR --label L
      Add region `L.guard +0 { SELECTOR }` at the hole left by `split ADDR`.
      SELECTOR: a COMDAT section name (`.data__ZZ...`) -> `*(.data__ZZ...)`, or `file.o(+DATA)`.
      Not needed when the guard is the anonymous .data of a plain function's TU and the hole directly follows
      that TU's existing `*z_x.o(+DATA)` region (the guard lands there by itself).
  pin_static.py TREE place ADDR SELECTOR --label REGION [--size N]
      Same as guard, but the region is named exactly REGION (e.g. a TU's .constdata cut out of a rodata chunk:
      SELECTOR `z_x.o(+RO-DATA)`). data_chunks.txt and rodata_chunks.txt are both handled by split.
  pin_static.py TREE bss ADDR SIZE SELECTOR --label L
      Add ZI region `L.bss 0xADDR { SELECTOR }` (SELECTOR `.bss__ZZ...` or `z_x.o(+BSS)`) in address order,
      re-basing the next relative (+off) ZI region so nothing after it moves.
  pin_static.py TREE pin --guard ADDR [--guard-sel SEL] --obj ADDR --obj-size N --obj-sel SEL --label L
      split + guard (if --guard-sel) + bss in one go.
  pin_static.py TREE regen CHUNK...   regenerate data/<CHUNK>.s from data_chunks.txt.
Options: --dry-run (print what would change).
In a workspace, disassembly/data_chunks.txt and disassembly/data are symlinks into oot3d/: they are
materialised first (file copy; directory of per-file symlinks) so nothing under oot3d/ is ever written.
Idempotent: a step that is already applied is reported and skipped.
"""
import argparse, os, re, shutil, sys

D = '/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike'
DRY = False


def log(*a):
    print(*a)


def tree_path(t):
    p = t if os.path.isabs(t) else os.path.join(D, t)
    if not os.path.isfile(os.path.join(p, 'data', 'oot3d.ld')):
        sys.exit(f'not a tree: {p}')
    return p


def write(path, text):
    if DRY:
        log(f'  (dry) write {path}')
        return
    if os.path.islink(path):
        os.unlink(path)
    with open(path, 'w') as f:
        f.write(text)


def materialise(tree):
    """Make disassembly/{data,rodata}_chunks.txt and disassembly/data writable without touching their targets."""
    dis = os.path.join(tree, 'disassembly')
    main = os.path.realpath(os.path.join(D, 'oot3d'))
    if os.path.realpath(tree) == main:
        return
    chs = [os.path.join(dis, fn) for fn in ('data_chunks.txt', 'rodata_chunks.txt')]
    for ch in chs:
        if os.path.islink(ch):
            src = os.path.realpath(ch)
            log(f'  materialise {ch}')
            if not DRY:
                os.unlink(ch)
                shutil.copyfile(src, ch)
    dd = os.path.join(dis, 'data')
    if os.path.islink(dd):
        src = os.path.realpath(dd)
        log(f'  materialise {dd} (per-file symlinks)')
        if not DRY:
            os.unlink(dd)
            os.mkdir(dd)
            for n in sorted(os.listdir(src)):
                os.symlink(os.path.join(src, n), os.path.join(dd, n))
    for p in chs + [dd]:
        if not DRY and os.path.realpath(p).startswith(main + '/'):
            sys.exit(f'refusing: {p} still resolves into oot3d/')


CHUNK_LINES = {}
CHUNK_FILES = ('data_chunks.txt', 'rodata_chunks.txt')


def read_chunks(tree, fname=None):
    """Rows [name, start, end] of data_chunks.txt + rodata_chunks.txt (or just `fname`); unchanged rows are
    written back byte-for-byte."""
    rows = []
    for fn in ([fname] if fname else CHUNK_FILES):
        for line in open(os.path.join(tree, 'disassembly', fn)):
            p = [x.strip() for x in line.split(',')]
            if len(p) >= 3 and p[0]:
                rows.append([p[0], int(p[1], 16), int(p[2], 16)])
                CHUNK_LINES[(p[0], rows[-1][1], rows[-1][2])] = line
    return rows


def chunk_file_of(tree, name):
    for fn in CHUNK_FILES:
        if any(r[0] == name for r in read_chunks(tree, fn)):
            return fn
    sys.exit(f'chunk {name} not found')


def write_chunks(tree, rows, fname='data_chunks.txt'):
    text = ''.join(CHUNK_LINES.get((n, s, e), f'{n},{s:08X},{e:08X}\n') for n, s, e in rows)
    write(os.path.join(tree, 'disassembly', fname), text)


def regen(tree, name, start, end):
    """Same output as disassembly/tools/split_arm_data_chunks.py for one chunk."""
    code = open(os.path.join(tree, 'disassembly', 'baserom', 'exefs', 'code.bin'), 'rb').read()
    b = code[start - 0x100000:end - 0x100000]
    out = [f'\tAREA |i.{name}|, DATA, READWRITE\n\n', f'; {name} : @ 0x{start:08X}\n']
    for i in range(0, len(b), 4):
        out.append('\tDCD 0x%s\n' % b[i:i + 4][::-1].hex().upper())
    out.append('\tEND\n')
    write(os.path.join(tree, 'disassembly', 'data', name + '.s'), ''.join(out))
    log(f'  regen data/{name}.s  0x{start:08X}..0x{end:08X}')


def tail_name(name, addr):
    m = re.match(r'^(data|rodata)_[0-9A-Fa-f]+$', name)
    if m:
        return f'{m.group(1)}_{addr:X}'
    m = re.match(r'^(.*\.data)(_[0-9A-F]{8})?$', name)
    if m:
        return f'{m.group(1)}_{addr:08X}'
    return f'{name}_{addr:08X}'


# ---------------------------------------------------------------- ld helpers
REG_RE = re.compile(r'^    (\S+) (\+0x[0-9A-Fa-f]+|\+0|0x[0-9A-Fa-f]+)(.*)$')


def ld_read(tree):
    return open(os.path.join(tree, 'data', 'oot3d.ld')).read().split('\n')


def ld_write(tree, lines):
    write(os.path.join(tree, 'data', 'oot3d.ld'), '\n'.join(lines))


def ld_regions(lines):
    """[(name, base, comment, start_line, end_line_inclusive, selectors)] for 4-space-indented exec regions."""
    regs = []
    i = 0
    while i < len(lines):
        m = REG_RE.match(lines[i])
        if m and i + 1 < len(lines) and lines[i + 1].strip() == '{':
            j = i + 2
            sels = []
            while lines[j].strip() != '}':
                sels.append(lines[j].strip())
                j += 1
            regs.append((m.group(1), m.group(2), m.group(3), i, j, sels))
            i = j + 1
        else:
            i += 1
    return regs


def region_text(name, base, sel, comment=''):
    return [f'    {name} {base}{comment}', '    {', f'        {sel}', '    }']


def find_region_with(lines, sel):
    for r in ld_regions(lines):
        if sel in r[5]:
            return r
    return None


def selector(s, kind):
    if s.endswith(')'):
        return '*' + s if not s.startswith('*') else s
    return f'*({s})'


# ---------------------------------------------------------------- steps
def find_cpp_with(tree, asm_ref):
    hits = []
    for root, _, files in os.walk(os.path.join(tree, 'src')):
        for f in files:
            if f.endswith('.cpp'):
                p = os.path.join(root, f)
                if asm_ref in open(p, errors='replace').read():
                    hits.append(p)
    return hits


def do_split(tree, addr, size):
    materialise(tree)
    rows = read_chunks(tree)
    # already split?
    for n, s, e in rows:
        if s <= addr < e:
            break
    else:
        log(f'split 0x{addr:08X}: not inside any chunk (already split?) -> skip')
        return
    fname = chunk_file_of(tree, n)
    rows = read_chunks(tree, fname)
    idx = rows.index([n, s, e])
    if addr + size > e:
        sys.exit(f'0x{addr:08X}+{size} crosses end of {n}')
    log(f'split 0x{addr:08X} (+{size}) out of {n} 0x{s:08X}..0x{e:08X}')
    if addr == s:
        rows[idx] = [n, addr + size, e]
        changed = [rows[idx]] if addr + size < e else []
        if addr + size == e:
            sys.exit('chunk would become empty: drop its GLOBAL_ASM/ld region by hand')
    elif addr + size == e:
        rows[idx] = [n, s, addr]
        changed = [rows[idx]]
    else:
        t = tail_name(n, addr + size)
        rows[idx] = [n, s, addr]
        rows.insert(idx + 1, [t, addr + size, e])
        changed = [rows[idx], rows[idx + 1]]
        # GLOBAL_ASM line for the tail chunk, right after the head's
        ref = f'GLOBAL_ASM("data/{n}.s")'
        cpps = find_cpp_with(tree, ref)
        if len(cpps) != 1:
            sys.exit(f'expected one .cpp with {ref}, got {cpps}')
        src = open(cpps[0]).read()
        src = src.replace(ref, ref + f'\nGLOBAL_ASM("data/{t}.s")', 1)
        write(cpps[0], src)
        log(f'  {os.path.relpath(cpps[0], tree)}: + GLOBAL_ASM("data/{t}.s")')
        # ld region for the tail, right after the head's
        lines = ld_read(tree)
        r = find_region_with(lines, f'*(i.{n})')
        if r is None:
            sys.exit(f'no ld region selects *(i.{n})')
        lines[r[4] + 1:r[4] + 1] = region_text(t, '+0', f'*(i.{t})', f' /* 0x{addr + size:08X} */')
        ld_write(tree, lines)
        log(f'  oot3d.ld: + region {t} after {r[0]}')
    write_chunks(tree, rows, fname)
    for cn, cs, ce in changed:
        regen(tree, cn, cs, ce)


def do_guard(tree, addr, sel, label, size=4, region=None):
    sel = selector(sel, 'data')
    lines = ld_read(tree)
    if find_region_with(lines, sel):
        log(f'guard {label}: {sel} already placed -> skip')
        return
    rows = read_chunks(tree)
    before = [r for r in rows if r[2] == addr]
    after = [r for r in rows if r[1] == addr + size]
    if before:
        r = find_region_with(lines, f'*(i.{before[0][0]})')
        at = r[4] + 1
        where = f'after {r[0]}'
    elif after:
        r = find_region_with(lines, f'*(i.{after[0][0]})')
        at = r[3]
        where = f'before {r[0]}'
    else:
        sys.exit(f'no chunk edge at 0x{addr:08X}: run split first')
    region = region or f'{label}.guard'
    lines[at:at] = region_text(region, '+0', sel, f' /* 0x{addr:08X} */')
    ld_write(tree, lines)
    log(f'guard {label}: + region {region} {where} ({sel})')


def zi_regions(lines):
    """ZI regions of the data load region: those after the last RW region, with absolute addresses."""
    regs = ld_regions(lines)
    out = []
    for r in regs:
        if r[0].endswith('.bss'):
            m = re.search(r'0x([0-9A-Fa-f]+)', r[2]) if r[1].startswith('+') else None
            a = int(r[1], 16) if not r[1].startswith('+') else (int(m.group(1), 16) if m else None)
            out.append((r, a))
    return out


def do_bss(tree, addr, size, sel, label):
    sel = selector(sel, 'bss')
    lines = ld_read(tree)
    if find_region_with(lines, sel):
        log(f'bss {label}: {sel} already placed -> skip')
        return
    zis = zi_regions(lines)
    if not zis:
        sys.exit('no .bss regions found in ld')
    nxt = [(r, a) for r, a in zis if a is not None and a > addr]
    prev = [(r, a) for r, a in zis if a is not None and a < addr]
    if nxt:
        r, a = nxt[0]
        if addr + size > a:
            sys.exit(f'0x{addr:08X}+0x{size:X} overlaps {r[0]} @0x{a:08X}')
        if r[1].startswith('+'):
            off = a - (addr + size)
            lines[r[3]] = f'    {r[0]} +0x{off:06X} /* 0x{a:08X} */'
            log(f'  {r[0]}: {r[1]} -> +0x{off:06X} (still 0x{a:08X})')
        at = r[3]
    else:
        at = prev[-1][0][4] + 1
    lines[at:at] = region_text(f'{label}.bss', f'0x{addr:08X}', sel)
    ld_write(tree, lines)
    log(f'bss {label}: + region {label}.bss 0x{addr:08X} size 0x{size:X} ({sel})')


def main():
    global DRY
    ap = argparse.ArgumentParser()
    ap.add_argument('tree')
    ap.add_argument('cmd', choices=['split', 'guard', 'place', 'bss', 'pin', 'regen'])
    ap.add_argument('args', nargs='*')
    ap.add_argument('--size', default='4')
    ap.add_argument('--label')
    ap.add_argument('--guard')
    ap.add_argument('--guard-sel')
    ap.add_argument('--obj')
    ap.add_argument('--obj-size')
    ap.add_argument('--obj-sel')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    DRY = a.dry_run
    t = tree_path(a.tree)
    h = lambda x: int(x, 16) if isinstance(x, str) else x
    if a.cmd == 'split':
        do_split(t, h(a.args[0]), int(a.size, 0))
    elif a.cmd == 'guard':
        do_guard(t, h(a.args[0]), a.args[1], a.label, int(a.size, 0))
    elif a.cmd == 'place':
        do_guard(t, h(a.args[0]), a.args[1], a.label, int(a.size, 0), region=a.label)
    elif a.cmd == 'bss':
        do_bss(t, h(a.args[0]), int(a.args[1], 0), a.args[2], a.label)
    elif a.cmd == 'pin':
        do_split(t, h(a.guard), 4)
        if a.guard_sel:
            do_guard(t, h(a.guard), a.guard_sel, a.label)
        do_bss(t, h(a.obj), int(a.obj_size, 0), a.obj_sel, a.label)
    elif a.cmd == 'regen':
        materialise(t)
        rows = {n: (s, e) for n, s, e in read_chunks(t)}
        for n in a.args:
            regen(t, n, *rows[n])


if __name__ == '__main__':
    main()
