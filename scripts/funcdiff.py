#!/usr/bin/env python3
"""Per-function diff of a built code.bin vs the original.
usage: funcdiff.py <orig code.bin> <built code.bin> <functions.tsv> [decompiled_functions.txt]"""
import sys
orig, built = open(sys.argv[1], 'rb').read(), open(sys.argv[2], 'rb').read()
BASE = 0x100000
funcs = []
for l in open(sys.argv[3]).readlines()[1:]:
    a, n, s = l.split('\t')[:3]
    funcs.append((int(a, 16), n, int(s)))
inc = set()
if len(sys.argv) > 4:
    inc = {l.split('\t')[0] for l in open(sys.argv[4])}
covered = bytearray(len(orig))
bad = []
for a, n, s in funcs:
    o = a - BASE
    covered[o:o + s] = b'\x01' * s
    if orig[o:o + s] != built[o:o + s]:
        nw = sum(1 for i in range(0, s, 4) if orig[o + i:o + i + 4] != built[o + i:o + i + 4])
        bad.append((a, n, s, nw))
for a, n, s, nw in bad:
    print('%08X %-50s %6d B %4d words differ%s' % (a, n, s, nw, '  [C]' if n in inc else ''))
other = [i for i in range(len(orig)) if orig[i] != built[i] and not covered[i]]
print('functions differing: %d / %d; C funcs among them: %d / %d' % (len(bad), len(funcs), sum(1 for b in bad if b[1] in inc), len(inc)))
print('non-function bytes differing: %d' % len(other))
if other:
    print('  first at file offset 0x%X (addr 0x%X)' % (other[0], other[0] + BASE))
