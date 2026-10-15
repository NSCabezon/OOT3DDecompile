#!/usr/bin/env python3
"""Progress metric for the oot3d tree: functions/bytes still GLOBAL_ASM vs. in C, named vs FUN_.
usage: progress.py <oot3d dir> <functions.tsv from aot_stats> [--git-head]"""
import re, sys, glob, os, json, subprocess
root = sys.argv[1]
spans = {}
for l in open(sys.argv[2]).readlines()[1:]:
    a, n, s = l.split('\t')[:3]; spans[n] = int(s)
asm = set()
for f in glob.glob(os.path.join(root, 'src/**/*.cpp'), recursive=True):
    asm |= set(re.findall(r'GLOBAL_ASM\("(?:\.\./split/)?asm/([\w$@.]+)\.s"\)', open(f, errors='replace').read()))
total = sum(spans.values())
# a function counts as C only if it has no GLOBAL_ASM line AND a C/C++ definition exists in src/ (or an EQU alias
# to a symbol name mangled by C++ is not enough: we want a real body)
src = ''.join(open(f, errors='replace').read() for f in glob.glob(os.path.join(root, 'src/**/*.c*'), recursive=True))
defs = set(re.findall(r'\b([A-Za-z_]\w*)\s*\([^;{)]*\)\s*(?:__attribute__\(\([^)]*\)\)\s*)?\{', src))
dec = {n: s for n, s in spans.items() if n not in asm and n in defs}
undefined = sorted((s, n) for n, s in spans.items() if n not in asm and n not in defs)
named = [n for n in spans if not n.startswith('FUN_')]
actorish = re.compile(r'^(En|Bg|Obj|Boss|Demo|Door|Item|Magic|Oceff|Arrow|Elf|Eff|Efc|Mir|Shot|Arms|Fishing|End|Object|Player|Actor_1)')
out = dict(functions=len(spans), functions_in_c=len(dec), bytes_total=total, bytes_in_c=sum(dec.values()),
           pct_bytes_in_c=round(100.0 * sum(dec.values()) / total, 3),
           pct_functions_in_c=round(100.0 * len(dec) / len(spans), 3),
           named_functions=len(named), pct_named=round(100.0 * len(named) / len(spans), 2),
           actor_named_functions=sum(1 for n in named if actorish.match(n)),
           no_asm_no_def=len(undefined), no_asm_no_def_bytes=sum(s for s, n in undefined))
print(json.dumps(out, indent=1))
with open(os.path.join(os.path.dirname(sys.argv[2]), 'no_asm_no_def.txt'), 'w') as o:
    for s, n in sorted(undefined, reverse=True): o.write('%s\t%d\n' % (n, s))
with open(os.path.join(os.path.dirname(sys.argv[2]), 'decompiled_functions.txt'), 'w') as o:
    for n in sorted(dec, key=lambda n: -dec[n]):
        o.write('%s\t%d\n' % (n, dec[n]))
