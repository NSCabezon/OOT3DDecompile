#!/usr/bin/env python3
"""Merge a finished workspace ws/<A> into oot3d/.
- copies src/game/actors/<A>/* wholesale
- for src/functions/functions_*.cpp: removes GLOBAL_ASM lines the agent deleted (doesn't overwrite file)
- reports any other differing files (manual review)
usage: merge_ws.py <A> [ws-name]"""
import sys, os, re, filecmp, shutil, glob
D = '/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike'
a = sys.argv[1]; W = f'{D}/ws/' + (sys.argv[2] if len(sys.argv) > 2 else a); M = f'{D}/oot3d'
import time, atexit
LOCK = f'{D}/.tree.lock'
while True:
    try: os.mkdir(LOCK); break
    except FileExistsError: time.sleep(2)
atexit.register(lambda: os.rmdir(LOCK))
src = f'{W}/src/game/actors/{a}'
for f in os.listdir(src):
    if f != '.DS_Store':
        shutil.copy(f'{src}/{f}', f'{M}/src/game/actors/{a}/{f}')
# split head -> tail (cfg_split.py log); a ws that has the tail line knows the split
SPLITS = {}
if os.path.exists(f'{M}/split/splits.tsv'):
    for row in open(f'{M}/split/splits.tsv'):
        p = row.rstrip('\n').split('\t')
        if len(p) >= 3 and not row.startswith('#'): SPLITS[p[0]] = p[2]
for wf in glob.glob(f'{W}/src/functions/functions_*.cpp'):
    mf = f'{M}/src/functions/' + os.path.basename(wf)
    # compare by function name: main may have `../split/asm/X.s` where an older ws has `asm/X.s` (cfg_split.py)
    nm = lambda l: (re.findall(r'asm/([\w$@.]+)\.s', l) or [l.strip()])[0]
    wl = set(nm(l) for l in open(wf) if 'GLOBAL_ASM' in l)
    ml = open(mf).read().split('\n')
    # `../split/` lines are kept (older ws may predate the split) unless the ws has the split's tail line
    # and dropped the head: then the head moved to C.
    TAILS = {t: h for h, t in SPLITS.items()}
    # names the ws references through ../split/ lines: proof the ws was created after that split
    wsplit = set(nm(l) for l in open(wf) if 'GLOBAL_ASM' in l and '../split/' in l)
    wall = set(nm(l) for g in glob.glob(f'{W}/src/functions/functions_*.cpp') + glob.glob(f'{src}/*.cpp')
               for l in open(g) if 'GLOBAL_ASM' in l)
    def removed(l):
        if 'GLOBAL_ASM' not in l or nm(l) in wl: return False
        if '../split/' not in l: return True
        n = nm(l)
        # head moved to C (ws keeps its split tail line) / tail moved to C (ws keeps its split head line)
        if SPLITS.get(n) in wsplit or TAILS.get(n) in wsplit: return True
        # ws has the split's .s (knows the split) but references it nowhere: moved to C
        # (covers head and tail both in C, where neither line survives in the ws)
        return os.path.exists(f'{W}/split/asm/{n}.s') and n not in wall
    gone = [l for l in ml if removed(l)]
    # only drop lines that the agent actually removed (present in ws base? assume all GLOBAL_ASM in main absent from ws were removed by this agent)
    if gone:
        open(mf, 'w').write('\n'.join(l for l in ml if l not in gone))
        print(f'{os.path.basename(mf)}: removed {len(gone)}: ' + ', '.join(re.findall(r'asm/(\w+)', ' '.join(gone))))
    extra = [l for l in open(wf).read().split('\n') if l.strip() and l not in ml and 'GLOBAL_ASM' not in l]
    if extra:
        print(f'WARN {os.path.basename(wf)} has {len(extra)} non-GLOBAL_ASM new lines -> review manually')
for root in ('include',):
    c = filecmp.dircmp(f'{W}/{root}', f'{M}/{root}', ignore=['.DS_Store'])
    def walk(c, p=''):
        for f in c.diff_files + c.left_only: print(f'WARN {root}/{p}{f} differs -> review manually')
        for k, sub in c.subdirs.items(): walk(sub, p + k + '/')
    walk(c)
with open(f'{D}/merged.txt', 'a') as o: o.write(a + '\n')
print('merged', a)
