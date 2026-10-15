#!/usr/bin/env python3
import sys,capstone
from elftools.elf.elffile import ELFFile
obj,name=sys.argv[1:3]
e=ELFFile(open(obj,'rb'))
sec=e.get_section_by_name('i.'+name)
d=sec.data()
md=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_ARM); md.skipdata=True
for i in md.disasm(d,0):
    print('%04x %s %s'%(i.address,i.mnemonic,i.op_str))
