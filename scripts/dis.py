#!/usr/bin/env python3
"""Disassemble functions of code.bin by name/address using the oot3d.cfg symbol list.
usage: dis.py <code.bin> <oot3d.cfg> NAME_OR_0xADDR...
"""
import sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

BASE = 0x100000
code = open(sys.argv[1], 'rb').read()
syms = {}
starts = []
for ln in open(sys.argv[2]):
    p = ln.split()
    if len(p) >= 3:
        a = int(p[1], 16)
        syms[a] = p[2]
        if p[0].endswith('func'):
            starts.append(a)
starts.sort()
byname = {v: k for k, v in syms.items()}
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
import bisect
for arg in sys.argv[3:]:
    a = int(arg, 16) if arg.startswith('0x') else byname[arg]
    i = bisect.bisect_right(starts, a)
    end = starts[i] if i < len(starts) else BASE + 0x3C99A8
    print('%s @ 0x%08x (%d bytes)' % (syms.get(a, '?'), a, end - a))
    for ins in md.disasm(code[a - BASE:end - BASE], a):
        s = ins.op_str
        if ins.mnemonic.startswith('b') and s.startswith('#0x'):
            t = int(s[1:], 16)
            s += '  ; ' + syms.get(t, '')
        if '[pc' in s and ins.mnemonic.startswith('ldr') and '#' in s:
            try:
                off = int(s.split('#')[1].rstrip(']!'), 16 if '0x' in s.split('#')[1] else 10)
                la = ins.address + 8 + (-off if '#-' in s else off)
                w = int.from_bytes(code[la - BASE:la - BASE + 4], 'little')
                s += '  ; =0x%08x %s' % (w, syms.get(w, ''))
            except Exception:
                pass
        print('  %08x: %08x  %-8s %s' % (ins.address, int.from_bytes(ins.bytes, 'little'), ins.mnemonic, s))
    print()
