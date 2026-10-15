# usage: fast.py file.cpp [-v]  : compile only, compare FUN_0012795c / FUN_003df814 words vs ROM (ignoring BL + pool relocs)
import sys, subprocess, struct, os
from elftools.elf.elffile import ELFFile
W='/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike/ws/Bg_Haka_Huta'
src=sys.argv[1]
obj=src+'.o' if '/tmp/fast/' in src else W+'/tmp/fast/'+os.path.basename(src)+'.o'
env=dict(os.environ, ARMCC_PATH='/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike/tools/rvct839', RVCT40INC='/Users/nscabezon/Apps/OOT3DDecompile/821/include', RVCT40LIB='/Users/nscabezon/Apps/OOT3DDecompile/821/lib')
cmd=[W+'/build/armwrap/armcc','-I'+W+'/include','-I'+W+'/library/3ds_sdk/include','-I'+W+'/src/game','-I'+W+'/src/game/actors/Bg_Haka_Huta','--apcs=//interwork','--cpu=MPCore','--fpmode=fast','--vfe','--no_rtti','--no_rtti_data','--cpp','--arm','--force_new_nothrow','--signed_chars','--data-reorder','--split_sections','--forceinline','-O3','-Otime','-o',obj,'-c',src]
r=subprocess.run(cmd,capture_output=True,text=True,env=env)
if r.returncode: print(r.stdout[-2000:],r.stderr[-2000:]); sys.exit(1)
rom=open(W+'/disassembly/baserom/exefs/code.bin','rb').read()
funcs={'FUN_0012795c':(0x12795c,680),'FUN_003df814':(0x3df814,524)}
e=ELFFile(open(obj,'rb'))
import capstone
md=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_ARM)
for name,(addr,size) in funcs.items():
    sec=e.get_section_by_name('i.'+name)
    d=sec.data()
    o=rom[addr-0x100000:addr-0x100000+size]
    if len(d)!=size: print(name,'SIZE',len(d),'vs',size); continue
    # reloc offsets
    rel=set()
    for rs in e.iter_sections():
        if rs.name in ('.reli.'+name,'.rel.i.'+name):
            for x in rs.iter_relocations(): rel.add(x['r_offset'])
    bad=[]
    for i in range(0,size,4):
        if i in rel: continue
        if d[i:i+4]!=o[i:i+4]: bad.append(i)
    print(name, len(bad),'words differ')
    if '-v' in sys.argv:
        for i in bad:
            a=list(md.disasm(o[i:i+4],addr+i)); b=list(md.disasm(d[i:i+4],addr+i))
            fa=(a[0].mnemonic+' '+a[0].op_str) if a else o[i:i+4].hex(); fb=(b[0].mnemonic+' '+b[0].op_str) if b else d[i:i+4].hex()
            print('  %x  %-35s | %s'%(addr+i,fa,fb))
