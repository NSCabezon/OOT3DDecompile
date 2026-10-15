
<!-- merge 2026-10-15 09:44:02 -->
# En_Dnt_Demo — G26 haiku stage

Matched (C in z_en_dnt_demo.cpp, ws_check baseline):
- EnDntDemo_Destroy, EnDntDemo_Update (blx tail via actionFunc), EnDntDemo_Prize, EnDntDemo_Results

Not matched:
- EnDntDemo_Init (113 insns list says 69): draft under #if 0 + GLOBAL_ASM. 60/77 words off. ROM frame 0x20 with a 12-byte
  temp at sp+0x14 for `scrubPos[i] = sScrubPos[i]` (ldm/stm); element-copy shapes (temp local, member-wise, pointer, ref) did not reproduce it.
  Also the r6/r8 self/play register order at entry differs.

Notes:
- Header: full 3DS layout (N64 +0x58 for fields after Actor); leader (En_Dnt_Jiji) fields used here are a partial struct EnDntDemoLeader.
- sScrubPos via actor-dir data_syms.s EQU (EnDntDemo_sScrubPos = 0x0052252C).
- EnDntDemo_Judge not in this group list: still GLOBAL_ASM.

## G26 sonnet stage
Matched (0 words, ws_check baseline): EnDntDemo_Init, EnDntDemo_Judge.
- Init: the sScrubPos copy goes through a class with a user copy-ctor (`struct V3 { V3(const V3&) : x(o.x).. }`, `*(V3*)&dst = V3(*(V3*)&src)`) -> member-wise vldr/vstr to the stack temp then ldm/stm; `EnDntDemo* self` declared before `PlayState* play = play2`; `if (leader != NULL) subCamId = 0` (predicated strh).
- Judge: jump-table switch on Player_GetMask (cases 1..8); sResultTable/sResultValues/sScrubPos are now REAL statics in z_en_dnt_demo.cpp (ROM derives sResultValues from sResultTable). Data chunk z_En_Dnt_Demo.data (0x5224B0..0x522598) dropped: data/oot3d.ld region `z_En_Dnt_Demo_ASM.data` and disassembly/data_chunks.txt row removed (apply to main like the other 23 chunk drops); data_syms.s deleted. 3DS: the three BGM ids use Audio_QueueSeqCmd(0, id, 0) (no fade arg).
- Leader struct: u8 isSolid at +0x1B4.
