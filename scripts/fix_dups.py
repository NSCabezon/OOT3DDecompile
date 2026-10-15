#!/usr/bin/env python3
"""Remove GLOBAL_ASM lines in oot3d/src/functions/*.cpp for symbols the linker reports as multiply defined."""
import re, glob, sys
log = open('/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike/build.log').read()
syms = sorted(set(re.findall(r'Symbol (\w+) multiply defined', log)))
for f in glob.glob('/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike/oot3d/src/functions/*.cpp'):
    lines = open(f).read().split('\n')
    keep = [l for l in lines if not any(l.strip() == 'GLOBAL_ASM("asm/%s.s")' % s for s in syms)]
    if len(keep) != len(lines):
        open(f, 'w').write('\n'.join(keep)); print(f.split('/')[-1], len(lines) - len(keep))
print('syms', syms)
