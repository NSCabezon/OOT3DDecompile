#!/usr/bin/env python3
"""Render logs/group_prompt.txt for a group of actors.
usage: group_prompt.py G STAGE kind A1 A2 ...   kind = haiku (small fns) | all (every asm fn)
Writes logs/prompt_<G>_<STAGE>.txt and prints its path."""
import subprocess, sys
D = '/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike'
g, stage, kind, actors = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
lines = []
for a in actors:
    r = subprocess.run([f'{D}/.venv/bin/python', '-P', f'{D}/scripts/plan_batches.py', a, '--tsv'],
                       capture_output=True, text=True, cwd=D).stdout
    fs = []
    for l in r.splitlines():
        p = l.split('\t')
        if len(p) < 4 or (kind == 'haiku' and not p[0].startswith('haiku')): continue
        fs.append(p[1] + (f'[{p[3]}]' if p[3] != 'actor' else '') + f'({p[2]} insns)')
    if fs: lines.append(f'- {a}: ' + ', '.join(fs))
t = open(f'{D}/logs/group_prompt.txt').read()
t = t.replace('__G__', g).replace('__ACTORS__', ' '.join(actors)).replace('__STAGE__', stage).replace('__FUNCS__', '\n'.join(lines))
out = f'{D}/logs/prompt_{g}_{stage.split()[0]}.txt'
open(out, 'w').write(t); print(out)
