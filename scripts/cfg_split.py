#!/usr/bin/env python3
"""Split a cfg-merged asm function into head + tail, tree-locally (idempotent).

usage: cfg_split.py <tree> <head_func> <split_addr> <new_name> [--tsv FUNCTIONS_TSV] [--cfg OOT3D_CFG] [--dry-run]

  <tree>   oot3d-like tree (oot3d/ or ws/<A>/). Everything written by default lives INSIDE it:
             <tree>/split/asm/<head>.s      shrunk head (copy of disassembly/asm/<head>.s up to split_addr)
             <tree>/split/asm/<new>.s       tail as its own AREA |i.<new>| + EXPORT <new>
             <tree>/src/**.cpp              GLOBAL_ASM("asm/<head>.s") -> GLOBAL_ASM("../split/asm/<head>.s")
                                            + GLOBAL_ASM("../split/asm/<new>.s") on the next line
             <tree>/data/oot3d.ld           scatter region "<new> <addr> { * (i.<new>) }" right after <head>'s
             <tree>/data/keep_symbols.txt   --keep=<new> after --keep=<head> (else armlink --remove drops it)
  The shared disassembly/asm/<head>.s is NOT modified (other workspaces keep building against it).
  --tsv PATH  also split the row in that functions.tsv (shared analysis/aot/functions.tsv when applying to main;
              harmless for unsplit trees: the bytes compared are the same, just in two rows).
  --cfg PATH  also add "arm_func <addr> <new> force" to that oot3d.cfg (bookkeeping for a future regen).
Head may be named by a previous split (chain splits: split A at x -> B, then split B at y -> C).
"""
import os, sys
# scripts/dis.py shadows stdlib `dis` (pulled in by argparse): drop the script dir from sys.path (= python -P)
sys.path = [p for p in sys.path if os.path.abspath(p or '.') != os.path.dirname(os.path.abspath(__file__))]
import argparse, re, glob

ap = argparse.ArgumentParser()
ap.add_argument('tree'); ap.add_argument('head', nargs='?'); ap.add_argument('addr', nargs='?'); ap.add_argument('new', nargs='?')
ap.add_argument('--tsv'); ap.add_argument('--cfg'); ap.add_argument('--dry-run', action='store_true')
ap.add_argument('--reapply', action='store_true', help='replay every split recorded in <tree>/split/splits.tsv (in order)')
a = ap.parse_args()
T = os.path.abspath(a.tree)
LOG = os.path.join(T, 'split', 'splits.tsv')
if a.reapply:
    import subprocess
    rc = 0
    for row in (open(LOG).read().split('\n') if os.path.exists(LOG) else []):
        if not row.strip() or row.startswith('#'): continue
        h, ad, nw = row.split('\t')[:3]
        cmd = [sys.executable, '-P', os.path.abspath(__file__), T, h, ad, nw] + (['--dry-run'] if a.dry_run else [])
        cmd += (['--tsv', a.tsv] if a.tsv else []) + (['--cfg', a.cfg] if a.cfg else [])
        print('==', h, ad, nw); rc |= subprocess.call(cmd)
    sys.exit(rc)
if not (a.head and a.addr and a.new): ap.error('need <head_func> <split_addr> <new_name> (or --reapply)')
head, new = a.head, a.new
split = int(a.addr, 16)
SPLITDIR = os.path.join(T, 'split', 'asm')
LD = os.path.join(T, 'data', 'oot3d.ld')
KEEP = os.path.join(T, 'data', 'keep_symbols.txt')
changed = []

def die(m): sys.exit('cfg_split: ERROR: ' + m)
def wr(path, text):
    changed.append(path)
    if a.dry_run: return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(text)

if split & 3: die('split address not 4-aligned')
if not re.fullmatch(r'[A-Za-z_]\w*', new): die('bad new name')

# ---- scatter: head start address (authoritative), new name must be free -------------------------------------
ld = open(LD).read()
m = re.search(r'^\t%s (0x[0-9a-fA-F]+)\n\t\{\n\t\t\* \(i\.%s\)\n\t\}\n' % (re.escape(head), re.escape(head)), ld, re.M)
if not m: die('no scatter region for %s in %s' % (head, LD))
hstart = int(m.group(1), 16)
if not hstart < split: die('split addr 0x%x not after head start 0x%x' % (split, hstart))
already_ld = re.search(r'^\t%s 0x' % re.escape(new), ld, re.M)
if not already_ld and re.search(r'\(i\.%s\)' % re.escape(new), ld): die('%s already in scatter elsewhere' % new)

# ---- asm split -------------------------------------------------------------------------------------------------
hsplit = os.path.join(SPLITDIR, head + '.s')
tfile = os.path.join(SPLITDIR, new + '.s')
_cpps = glob.glob(os.path.join(T, 'src', '**', '*.cpp'), recursive=True)
_hre = re.compile(r'GLOBAL_ASM\("(?:asm|\.\./split/asm)/%s\.s"\)' % re.escape(head))
head_referenced = any(_hre.search(open(f, errors='replace').read()) for f in _cpps)
if os.path.exists(tfile) and (os.path.exists(hsplit) or not head_referenced):
    print('asm: %s already exists, skipping asm split' % os.path.relpath(tfile, T))
else:
    # regenerate from the shared asm when the tail exists but the split head was deleted (head reverted to asm)
    src = hsplit if os.path.exists(hsplit) and not os.path.exists(tfile) else os.path.join(T, 'disassembly', 'asm', head + '.s')
    if os.path.exists(tfile) and not os.path.exists(src): die('tail exists, split head missing and no shared asm')
    if not os.path.exists(src): die('no asm for %s (%s)' % (head, src))
    lines = open(src).read().split('\n')
    # header = AREA/EXPORT lines + head label; body after it
    try:
        hl = lines.index(head)
    except ValueError:
        die('head label line %r not found in %s' % (head, src))
    header, body = lines[:hl + 1], lines[hl + 1:]
    while body and body[-1].strip() in ('', 'END'): body.pop()
    exports = [l.split()[1] for l in header if l.strip().startswith('EXPORT')]
    area = [l for l in header if l.strip().startswith('AREA')]
    if len(area) != 1 or ('|i.%s|' % head) not in area[0]: die('unexpected AREA header in %s' % src)

    def nbytes(stmt):
        s = stmt.strip()
        if not s: return 0
        op = s.split()[0]
        if op == 'DCB': return len(s[3:].split(';')[0].split(','))
        if op == 'DCD': return 4 * len(s[3:].split(';')[0].split(','))
        if op == 'DCW': return 2 * len(s[3:].split(';')[0].split(','))
        if op in ('EXPORT', 'IMPORT', 'EXTERN', 'END', 'AREA'): return 0
        return 4  # ARM instruction
    pc = hstart
    cut = None   # (line index, byte offset within DCB line or 0)
    for i, l in enumerate(body):
        if not l.strip(): continue
        if not l.startswith('\t'):  # label [directive]
            lab, _, rest = l.strip().partition(' ')
            mm = re.fullmatch(r'_([0-9a-f]{8})', lab)
            if mm and int(mm.group(1), 16) != pc:
                die('address tracking mismatch at %s (computed 0x%08x)' % (lab, pc))
            if pc == split and cut is None: cut = (i, 0)
            pc += nbytes(rest)
            continue
        if pc == split and cut is None: cut = (i, 0)
        n = nbytes(l)
        if cut is None and pc < split < pc + n:
            if l.strip().split()[0] != 'DCB': die('split 0x%x falls inside a non-DCB statement: %r' % (split, l))
            cut = (i, split - pc)
        pc += n
    hend = pc
    if cut is None: die('split addr 0x%x not inside %s (0x%x..0x%x)' % (split, head, hstart, hend))
    ci, off = cut
    hbody, tbody = body[:ci], body[ci:]
    if off:
        vals = [v.strip() for v in tbody[0].strip()[3:].split(',')]
        hbody.append('\tDCB ' + ', '.join(vals[:off]))
        tbody = ['\tDCB ' + ', '.join(vals[off:])] + tbody[1:]
    # cross references between halves (labels are file-local; once the head becomes C they vanish)
    def labels(ls): return {l.split()[0] for l in ls if l.strip() and not l.startswith('\t')}
    def refs(ls, labs):
        txt = '\n'.join(l.split(';')[0] for l in ls if l.startswith('\t') or ' ' in l.strip())
        return {x for x in labs if re.search(r'\b%s\b' % re.escape(x), txt)}
    hl_, tl_ = labels(hbody), labels(tbody)
    bad = refs(hbody, tl_ - set(exports)) | refs(tbody, hl_)
    if bad: die('cross-half label references: %s (fix by hand)' % sorted(bad))
    # tail starting with raw DCB (disassembler saw no code) -> first word as DCI so the symbol is typed ARM Code ($a)
    k = next((k for k, l in enumerate(tbody) if l.startswith('\t')), None)
    if k is not None and tbody[k].strip().startswith('DCB ') and all(not l.startswith('\t') for l in tbody[:k]):
        vals = [v.strip() for v in tbody[k].strip()[3:].split(';')[0].split(',')]
        if len(vals) >= 4:
            w = sum(int(v, 0) << (8 * j) for j, v in enumerate(vals[:4]))
            rest = ['\tDCB ' + ', '.join(vals[4:])] if len(vals) > 4 else []
            tbody = tbody[:k] + ['\tDCI 0x%08x' % w] + rest + tbody[k + 1:]
    texports = [e for e in exports if e in tl_]
    hexports = [e for e in exports if e not in tl_]
    hdr_h = [area[0], *['\tEXPORT ' + e for e in hexports], head]
    hdr_t = [area[0].replace('|i.%s|' % head, '|i.%s|' % new), '\tEXPORT ' + new,
             *['\tEXPORT ' + e for e in texports], new]
    wr(hsplit, '\n'.join(hdr_h + hbody) + '\n\n\tEND\n')
    if not os.path.exists(tfile):  # never overwrite an existing tail (it may itself have been split further)
        wr(tfile, '\n'.join(hdr_t + tbody) + '\n\n\tEND\n')
    print('asm: head 0x%08x..0x%08x (%d B) | %s 0x%08x..0x%08x (%d B)%s' % (
        hstart, split, split - hstart, new, split, hend, hend - split,
        ' moved EXPORTs %s' % texports if texports else ''))

# ---- .cpp GLOBAL_ASM lines --------------------------------------------------------------------------------------
pat_any = re.compile(r'^([ \t]*)GLOBAL_ASM\("(?:asm|\.\./split/asm)/%s\.s"\)[ \t]*$' % re.escape(head), re.M)
tail_line = 'GLOBAL_ASM("../split/asm/%s.s")' % new
cpps = glob.glob(os.path.join(T, 'src', '**', '*.cpp'), recursive=True)
hits = [f for f in cpps if pat_any.search(open(f, errors='replace').read())]
tail_hits = [f for f in cpps if tail_line in open(f, errors='replace').read()]
# tail already decompiled (C definition `NEW(...) {`): never re-add its GLOBAL_ASM line (--reapply after merges)
tail_c = re.compile(r'\b%s\s*\([^;{]*\)\s*\{' % re.escape(new))
tail_in_c = any(tail_c.search(open(f, errors='replace').read()) for f in cpps)
if len(hits) > 1: die('head GLOBAL_ASM in several files: %s' % hits)
if hits:
    f = hits[0]; s = open(f).read()
    mm = pat_any.search(s); ind = mm.group(1)
    rep = '%sGLOBAL_ASM("../split/asm/%s.s")' % (ind, head)
    if not tail_hits and not tail_in_c:
        rep += '\n%s%s' % (ind, tail_line)
    elif tail_hits != [f]:
        die('tail line already in another file: %s' % tail_hits)
    s2 = s[:mm.start()] + rep + s[mm.end():]
    if s2 != s: wr(f, s2)
    else: print('cpp: %s already up to date' % os.path.relpath(f, T))
    if not a.dry_run: os.utime(f)   # force preproc re-run (CMake asm deps are configure-time)
elif tail_hits:
    print('cpp: head no longer GLOBAL_ASM (in C?); tail line present in %s' % os.path.relpath(tail_hits[0], T))
    if not a.dry_run: os.utime(tail_hits[0])
elif tail_in_c:
    print('cpp: head and tail %s both in C; nothing to do' % new)
else:
    die('no GLOBAL_ASM for %s and no tail line: add `%s` after %s by hand' % (head, tail_line, head))

# ---- scatter + keep ---------------------------------------------------------------------------------------------
if not already_ld:
    blk = '\t%s 0x%08x\n\t{\n\t\t* (i.%s)\n\t}\n' % (new, split, new)
    wr(LD, ld[:m.end()] + blk + ld[m.end():])
keep = open(KEEP).read().split('\n')
if '--keep=' + new not in keep:
    try: keep.insert(keep.index('--keep=' + head) + 1, '--keep=' + new)
    except ValueError:
        keep.insert(len(keep) - (1 if keep[-1] == '' else 0), '--keep=' + new)
    wr(KEEP, '\n'.join(keep))

# ---- optional shared bookkeeping --------------------------------------------------------------------------------
if a.tsv:
    rows = open(a.tsv).read().split('\n')
    names = [r.split('\t')[1] if '\t' in r else None for r in rows]
    if new not in names:
        i = names.index(head)
        p = rows[i].split('\t')
        if int(p[0], 16) != hstart: die('tsv addr mismatch for %s' % head)
        span = int(p[2]); hs = split - hstart; ts = span - hs
        if ts <= 0: die('tsv span of %s (%d) does not cover split' % (head, span))
        p[2] = str(hs); p[3] = str(min(int(p[3]), hs // 4))
        rows[i] = '\t'.join(p)
        rows.insert(i + 1, '\t'.join(['0x%08x' % split, new, str(ts), str(ts // 4)] + ['0'] * (len(p) - 4)))
        wr(a.tsv, '\n'.join(rows))
if a.cfg:
    cl = open(a.cfg).read().split('\n')
    if not any(l.split()[2:3] == [new] for l in cl if l.startswith('arm_func')):
        line = 'arm_func 0x%08x %s force' % (split, new)
        idx = next((k for k, l in enumerate(cl) if l.startswith('arm_func') and int(l.split()[1], 16) > split), None)
        if idx is None: die('cannot place cfg line')
        cl.insert(idx, line)
        wr(a.cfg, '\n'.join(cl))

rec = '%s\t0x%08x\t%s' % (head, split, new)
if not a.dry_run:
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    have = open(LOG).read().split('\n') if os.path.exists(LOG) else ['# head\tsplit_addr\tnew  (replay: cfg_split.py <tree> --reapply)']
    if rec not in have:
        have = [l for l in have if l] + [rec]
        open(LOG, 'w').write('\n'.join(have) + '\n')
print('changed%s: %s' % (' (dry-run)' if a.dry_run else '', ', '.join(os.path.relpath(c, T) if c.startswith(T) else c for c in changed) or 'nothing'))
