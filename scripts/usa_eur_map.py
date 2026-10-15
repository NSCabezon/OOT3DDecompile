#!/usr/bin/env python3
"""Check how well USA function boundaries (oot3d.cfg) transfer to EUR Rev1 code.bin.
Mapping from OoT3D_Randomizer address_conversion_info.txt: <0x419E18: +0; 0x41A144..0x43668B: +0x24;
0x436690..0x4A5ADF: +0x20; >=0x4A5B00: +0.  A function 'matches' if all words are equal after masking
the 24-bit immediate of B/BL/BLX and words that look like pointers into code/data (relocated literals)."""
import sys, struct
usa = open(sys.argv[1], 'rb').read(); eur = open(sys.argv[2], 'rb').read()
B = 0x100000
def m(a):
    if a < 0x419E18: return a
    if 0x41A144 <= a < 0x43668C: return a + 0x24
    if 0x436690 <= a < 0x4A5AE0: return a + 0x20
    if a >= 0x4A5B00: return a
    return None
fs = sorted(int(l.split()[1], 16) for l in open(sys.argv[3]) if l.startswith('arm_func'))
end = B + 0x3C99A8
ok = nomap = bad = 0; badlist = []
for i, a in enumerate(fs):
    e = fs[i + 1] if i + 1 < len(fs) else end
    ea = m(a)
    if ea is None: nomap += 1; continue
    good = True
    for x in range(a, e, 4):
        wu = struct.unpack_from('<I', usa, x - B)[0]; we = struct.unpack_from('<I', eur, ea + (x - a) - B)[0]
        if wu == we: continue
        if (wu >> 25) & 7 == 5 and (we >> 25) & 7 == 5 and (wu >> 24) == (we >> 24): continue  # b/bl imm
        if (wu >> 25) == 0x7D and (we >> 25) == 0x7D: continue  # blx imm
        if 0x100000 <= wu < 0x600000 and 0x100000 <= we < 0x600000 and abs(we - wu) <= 0x24: continue  # pointer
        good = False; break
    if good: ok += 1
    else: bad += 1; badlist.append(a)
print('functions', len(fs), 'identical-modulo-relocation', ok, 'differ', bad, 'unmapped', nomap)
print('differing:', ' '.join('0x%x' % a for a in badlist[:40]))
