#!/usr/bin/env python3
# Fast compile-only checker (~1 s): compiles ONE .cpp in a workspace and compares each named function's
# section bytes vs ROM (relocated words masked). Does NOT link, so it can't catch layout shifts; confirm
# with ws_check.sh at the end.
# usage: .venv/bin/python -P scripts/fastchk.py <ws-name> <path/to/file.cpp relative to ws> FUNC [FUNC...]
#        SIDE=FUNC ... -> side-by-side disasm of FUNC
import sys, subprocess, os, struct
from elftools.elf.elffile import ELFFile
D='/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike'
W=D+'/ws/'+sys.argv[1]
src=W+'/'+sys.argv[2]
os.makedirs(W+'/tmp/fast',exist_ok=True)
obj=W+'/tmp/fast/'+os.path.basename(src)+'.o'
env=dict(os.environ, ARMCC_PATH=D+'/tools/rvct839', RVCT40INC=D+'/../821/include', RVCT40LIB=D+'/../821/lib', WIBO=D+'/tools/wibo/wibo-macos')
cmd=[W+'/build/armwrap/armcc','-I'+W+'/include','-I'+W+'/library/3ds_sdk/include','-I'+W+'/src/game','-I'+os.path.dirname(src),'--apcs=//interwork','--cpu=MPCore','--fpmode=fast','--vfe','--no_rtti','--no_rtti_data','--cpp','--arm','--force_new_nothrow','--signed_chars','--data-reorder','--split_sections','--forceinline','-O3','-Otime','-o',obj,'-c',src]
r=subprocess.run(cmd,capture_output=True,text=True,env=env,cwd=W+'/build')
if r.returncode or 'Error' in r.stdout+r.stderr:
    print((r.stdout+r.stderr)[-3000:]); sys.exit(1)
rom=open(W+'/disassembly/baserom/exefs/code.bin','rb').read()
funcs={}
for line in open(D+'/analysis/aot/functions.tsv'):
    p=line.rstrip('\n').split('\t')
    if len(p)>=3 and p[0].startswith('0x'): funcs[p[1]]=(int(p[0],16),int(p[2]))
names=sys.argv[3:]
e=ELFFile(open(obj,'rb'))
import capstone
md=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_ARM)
for name in names:
    addr,size=funcs[name]
    sec=e.get_section_by_name('i.'+name)
    if sec is None: print(name,'MISSING'); continue
    d=sec.data()
    o=rom[addr-0x100000:addr-0x100000+size]
    rel=set()
    for rs in e.iter_sections():
        if rs.name in ('.rel.i.'+name,'.reli.'+name):
            for x in rs.iter_relocations(): rel.add(x['r_offset'])
    if len(d)!=size: print(name,'SIZE built',len(d),'rom',size)
    bad=[i for i in range(0,min(len(d),size),4) if i not in rel and d[i:i+4]!=o[i:i+4]]
    print(name,'words differ:',len(bad),'of',size//4, 'bad offs', [hex(b) for b in bad][:12])
    if '-v' in os.environ.get('FC',''):
        pass

def side(name):
    addr,size=funcs[name]
    d=e.get_section_by_name('i.'+name).data()
    o=rom[addr-0x100000:addr-0x100000+size]
    a=list(md.disasm(o,addr)); b=list(md.disasm(d,0))
    for k in range(max(len(a),len(b))):
        l=('%08x %-6s %-22s'%(a[k].address,a[k].mnemonic,a[k].op_str)) if k<len(a) else ' '*40
        r=('%04x %-6s %s'%(b[k].address,b[k].mnemonic,b[k].op_str)) if k<len(b) else ''
        mark='  ' if k<len(a) and k<len(b) and (a[k].mnemonic,a[k].op_str)==(b[k].mnemonic,b[k].op_str) else '!!'
        print(mark,l,'|',r)
if os.environ.get('SIDE'):
    side(os.environ['SIDE'])
