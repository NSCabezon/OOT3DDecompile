import sys,os,re
act=os.environ['ACT']; rel=os.environ['REL']; p='ws/%s/%s'%(act,rel)
fn,note=sys.argv[1:3]
s=open(p).read()
i=re.search(r'^(static )?(inline )?\S+ %s\([^;{]*\) \{'%fn,s,re.M).start();j=s.index('\n}\n',i)+3
s=s[:i]+'// draft: %s\n#if 0\n'%note+s[i:j]+'#endif\nGLOBAL_ASM("asm/%s.s")\n'%fn+s[j:]
open(p,'w').write(s)
