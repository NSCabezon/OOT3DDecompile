
<!-- merge 2026-10-14 18:00:21 -->
# Obj_Hamishi (G3, haiku stage) STATUS

Matched (C in src/game/actors/Obj_Hamishi/z_obj_hamishi.cpp): ObjHamishi_Init, ObjHamishi_Destroy, ObjHamishi_Draw (3/3).
- Init/Destroy/Draw use EQU data symbols in src/game/actors/Obj_Hamishi/data_syms.s (sInitChain 0x535064, sCylinderInit 0x535018, sColChkInfoInit 0x535010).
- Draw float args: arg5 = 2/3, arg6 = 26/51 (ROM literal pool order).
ws_check Obj_Hamishi: baseline only (FUN_00249af8).

Sonnet stage: ObjHamishi_Update (282 insns) NOT matched, far (best draft ~50 insns / 249 words off after ~70 variants; draft under #if 0 in z_obj_hamishi.cpp, GLOBAL_ASM kept).
Diff note: ROM keeps `thisx` in fp separate from `self` (r5) and self+0x200 in r4 (our armcc coalesces thisx/self); Break loop 0x421/-450/0x241/0x221/-380 come from literal pool in ROM (-320 hoisted in sb) but derived in ours; float regs s17..s23 numbering shifted.
Header now has named fields (shakePosSize 0x1FC, shakeRotSize 0x200, shakeFrames 0x204, shakePosPhase 0x206, shakeRotPhase 0x208, hitCount 0x20A); data_syms.s has ObjHamishi_sEffectScales (0x535050).
