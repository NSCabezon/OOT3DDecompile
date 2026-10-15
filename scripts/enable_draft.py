#!/usr/bin/env python3
"""Enable a #if 0 C draft for FUNC in an actor .cpp and drop the head's split GLOBAL_ASM line.
usage: enable_draft.py <ws> <actor_cpp_rel> <FUNC>   (run with python3 -P)"""
import sys, re, os, glob
ws, cpp, fn = sys.argv[1:4]
p = os.path.join(ws, cpp)
L = open(p).read().split('\n')
defn = re.compile(r'^[A-Za-z_][\w\s\*]*\b%s\s*\([^;]*$' % re.escape(fn))
done = False
i = 0
while i < len(L):
    if L[i].startswith('#if 0'):
        j = i + 1; depth = 1
        while j < len(L):
            if L[j].startswith('#if'): depth += 1
            elif L[j].startswith('#endif'):
                depth -= 1
                if depth == 0: break
            j += 1
        if any(defn.match(x) for x in L[i+1:j]):
            del L[j]; del L[i]; done = True; break
        i = j
    i += 1
if not done: sys.exit('draft for %s not found' % fn)
open(p, 'w').write('\n'.join(L))
n = 0
for f in glob.glob(os.path.join(ws, 'src', '**', '*.cpp'), recursive=True):
    s = open(f).read()
    for pat in ('GLOBAL_ASM("../split/asm/%s.s")\n' % fn, 'GLOBAL_ASM("asm/%s.s")\n' % fn):
        if pat in s:
            s = s.replace(pat, '', 1); n += 1; open(f, 'w').write(s)
print('enabled', fn, 'removed GLOBAL_ASM lines:', n)
