
<!-- merge 2026-10-14 23:21:11 -->
# En_Brob (G18, haiku stage) status

MATCHED (C, fastchk 0 words; ws_check baseline not re-verified, see note):
- EnBrob_Destroy (C in z_en_brob.cpp). FUN_003508b8 is called as a 2-arg fn (ROM sets only r0/r1): cast to `(void(*)(Actor*,void*))`.
- FUN_0036461c = EnBrob_SetupIdle (moved from functions_360000s.cpp; GLOBAL_ASM removed).
- FUN_001208cc = EnBrob_Stunned (moved from functions_120000s.cpp). Uses out-of-line `EnBrob_CurFramePtr` (z_en_brob_anim.cpp, armlink inline).
- FUN_003e440c = EnBrob_Idle (moved from functions_3E0000s.cpp).
- FUN_003e2b80 = EnBrob_Wobble (moved from functions_3E0000s.cpp).
- FUN_003d6d70 = EnBrob_MoveDown (moved from functions_3C0000s.cpp).
- FUN_003b96d8 = EnBrob_MoveUp (moved from functions_3A0000s.cpp).

NOT MATCHED:
- EnBrob_Draw: 23-24/36 words off. ROM computes 1.0 into s0 before the PauseContext compare and copies it to pos.x (vmov s2,s0); best C shapes still differ. Draft under #if 0, GLOBAL_ASM kept.
- FUN_003da5f8 = EnBrob_Shock: 9 words off (colour pointer: ROM derives prim as env-4 (`sub r2,r3,#4`), pool order). Draft under #if 0, GLOBAL_ASM kept in functions_3C0000s.cpp. Colours: data_syms.s EQU 0x521408 / 0x52140C.

SPLIT: FUN_00272930 at 0x00272e34 -> FUN_00272e34 (88 B tail = EnBrob_PostLimbDraw, stays asm).
Layout (3DS): actionFunc 0x4B4, timer 0x4B8, modelOffsetY 0x4BA, colliders 0x4C0/0x518, skelAnime 0x1BC.

Debt: Actor has no colorFilterTimer (raw store at +0x11A); FUN_00272e34 used via raw cast in Draw draft.
Verification: fastchk only. ws_check is currently failing for every workspace incl. an untouched control (Door_Toki) since main-tree data_chunks.txt / data/oot3d.ld changed at 23:03.
