#!/usr/bin/env python3
"""Side-by-side ARM disassembly of one function: original code.bin vs built code.bin.
usage: asmdiff.py <orig code.bin> <built code.bin> <functions.tsv> <name|0xaddr>"""
import sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
BASE = 0x100000
o, b = open(sys.argv[1], 'rb').read(), open(sys.argv[2], 'rb').read()
key = sys.argv[4]
for l in open(sys.argv[3]).readlines()[1:]:
    a, n, s = l.split('\t')[:3]
    if n == key or int(a, 16) == (int(key, 16) if key.startswith('0x') else -1):
        a, s = int(a, 16), int(s); break
else:
    sys.exit('function not found')
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
def dis(buf):
    out = []
    for i in range(0, s, 4):
        w = buf[a - BASE + i:a - BASE + i + 4]
        ins = list(md.disasm(w, a + i))
        out.append((w, '%s %s' % (ins[0].mnemonic, ins[0].op_str) if ins else '.word 0x%08x' % int.from_bytes(w, 'little')))
    return out
for i, ((wo, so), (wb, sb)) in enumerate(zip(dis(o), dis(b))):
    print('%08x %s %-42s | %s' % (a + 4 * i, '  ' if wo == wb else '!!', so, sb))
