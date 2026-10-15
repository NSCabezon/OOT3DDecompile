
<!-- merge 2026-10-14 22:30:00 -->
# En_Part (stage haiku, small functions only)

- EnPart_Init (5 insns): MATCHED. Action byte 0x1D1 = 0xFF, s32 0x1A8 = -1.
- EnPart_Destroy (21 insns): MATCHED. Virtual call slot 2 on 0x1C4 (EnPartModel, _ZTI11EnPartModel EQU in syms.s), FUN_00350f34 on 0x1A4, SystemArena_Free tail on 0x1C8.
- FUN_00282820 (3 insns, action = 3): MATCHED, moved into z_en_part.cpp (GLOBAL_ASM removed from functions_280000s.cpp).
- FUN_0028282c (106 insns), FUN_002b2940 (111), FUN_0026c56c (112), EnPart_Draw (94): NOT ATTEMPTED in stage haiku (small functions only; Sonnet takes the rest). Still GLOBAL_ASM.
- Struct: z_en_part.hpp now names 0x1A4 skelAnimModel, 0x1A8 unk, 0x1C4 EnPartModel*, 0x1C8 heap ptr, 0x1D1 action (u8), 0x1D2 timer (s16). Size 0x21C kept.

## Stage sonnet (G15)
MATCHED (moved into z_en_part.cpp, GLOBAL_ASM removed from functions_*.cpp): FUN_0028282c (action 3, was func_80ACE5C8), FUN_002b2940 (action 4),
FUN_0026c56c (particle action 4), FUN_0037ea38 (action 0 setup), FUN_0037eea0 (action 1), FUN_002823f4 (particle action 1), EnPart_Draw.
- 3DS EnPart has a particle-array mode (action 0xFF): EnPart+0x1C8 = array of 0x80-byte EnPartParticle, +0x1CC = count. Particle actions at 0x52DC34, actor actions at 0x52DC4C.
- EnPart_sColor EQU 0x004D9B04 in syms.s (4 floats, Draw color).
- Idioms: `f32 dist = __sqrtf(..); if (dist <= 40.0f)` (const reg order), (Self*, PlayState* play2) + `PlayState* play = play2;` (FUN_0037ea38), dead `EnPart* s2 = self;` used on ONE access (declared right after the function's first line) fixed r7/r8 + VFP numbering in 0026c56c/002823f4/0037eea0, zero Vector3f init with `f32 a,b,c; a=0;c=0;b=0; Vector3f(c,b,a)` (002b2940), `EnPartParticle* p0 = self->particles; EnPartColor color = EnPart_sColor;` (Draw).
NOT MATCHED:
- FUN_00281edc (particle action 0 setup): 0 semantic diffs but literal-pool layout: ROM flushes the pool one block earlier (`bne L6; b B4; pool; B4`), shifting every pc-relative load (135 words). Adding any 1 dead insn before the type==4/6 check reproduces the `b`, so threshold is 4 bytes; natural source for the extra estimate not found. Draft under #if 0 in z_en_part.cpp. GLOBAL_ASM stays in functions_280000s.cpp.
- EnPart_Update: `matrix` — per-particle scale MTX34 built with integer-register stores (only as u32 word copy of actor.scale + integer zeros); rest also differs (spilled play in arg-home slot, VFP numbering). Draft under #if 0 (needs EQU for 0x52DC4C/0x52DC34).
- 2026-10-15 R9 MakeScale (Opus): EnPart_Update draft uses MTX34_MakeScale, 191w (zero-CSE: ROM re-does mov r0,#0 per scale block, armcc keeps zero in sl; + play entry load + VFP numbering). syms.s EQUs EnPart_sParticleFuncs/EnPart_sActionFuncs added for the draft.
