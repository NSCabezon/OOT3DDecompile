#!/usr/bin/env python3
# usage: _try_block.py WS CPPREL START_MARKER END_FUNC VARIANTS_FILE FUNC_TO_CHECK...
# replaces text from START_MARKER (line start) through the end of function END_FUNC with each variant; fastchk the funcs.
import sys,re,subprocess
D='/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike'
ws,cpp,start,endfn,vf=sys.argv[1:6]; chk=sys.argv[6:]
p=f'{D}/ws/{ws}/{cpp}'
orig=open(p).read()
a=orig.index(start)
m=re.search(r'^[A-Za-z_][^\n;{]*\b%s\([^;{]*\)\s*\{\n.*?\n\}\n'%re.escape(endfn),orig[a:],re.S|re.M)
b=a+m.end()
vs=[v.strip('\n')+'\n' for v in open(vf).read().split('//----\n')]
best=None
try:
    for i,v in enumerate(vs):
        open(p,'w').write(orig[:a]+v+orig[b:])
        r=subprocess.run([f'{D}/.venv/bin/python','-P',f'{D}/scripts/fastchk.py',ws,cpp]+chk,capture_output=True,text=True,cwd=D)
        out=(r.stdout+r.stderr).strip().splitlines()
        ns=[int(x) for x in re.findall(r'words differ: (\d+)',r.stdout)]
        n=sum(ns) if ns else 9999
        print(i,n,'' if ns else ' | '.join(out[-4:])[:500])
        if best is None or n<best[0]: best=(n,i)
finally:
    open(p,'w').write(orig)
print('best',best)
