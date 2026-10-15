# env ACT (actor), REL (cpp relative to ws); usage: var.py FUNC variants.txt [apply NAME]
import subprocess,sys,os,re
act=os.environ['ACT']; rel=os.environ['REL']; p='ws/%s/%s'%(act,rel)
fn,vfile=sys.argv[1:3]; apply=sys.argv[4] if len(sys.argv)>4 else None
orig=open(p).read()
i=re.search(r'^(static )?(inline )?\S+ %s\([^;{]*\) \{'%fn,orig,re.M).start();j=orig.index('\n}\n',i)+3
for v in open(vfile).read().split('\n//===='):
    name,code=v.split('\n',1); name=name.replace('//====','').strip()
    extra=''
    if '//PRE\n' in code: extra,code=code.split('//PRE\n')
    new=orig[:i]+extra+code.strip()+'\n'+orig[j:]
    if apply:
        if name.split()[0]==apply: open(p,'w').write(new); print('applied',name)
        continue
    open(p,'w').write(new)
    r=subprocess.run(['.venv/bin/python','-P','scripts/fastchk.py',act,rel,fn],capture_output=True,text=True)
    out=(r.stdout+r.stderr).strip().splitlines()
    print(name, [l for l in out if 'differ' in l or 'rror' in l][-1:])
    open(p,'w').write(orig)
