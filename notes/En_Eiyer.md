
<!-- merge 2026-10-15 10:57:39 -->
# En_Eiyer (group G29, haiku stage) — status

ws_check: baseline only (FUN_00249af8).

Matched (C, byte-exact in fastchk and ws_check):
- EnEiyer_Destroy
- FUN_00239050 (SetupInactive), FUN_003465e0 (SetupAppearFromGround), FUN_00125e80 (AppearFromGround)
- FUN_00125700 (dive-end wait -> Land), FUN_001ca520 (Land), FUN_0013f714 (Die), FUN_003d5578 (Dead)
- FUN_003e1500 (Stunned), FUN_0010a380 (StartAttack), FUN_0011cbf0 (DiveAttack), FUN_00120d7c (Hurt)
- FUN_00127260 (Ambush), FUN_001cd1d4 (WanderUnderground), FUN_003e2080 (Glide), FUN_001e4908 (limb rotate callback)

Not matched (draft under `#if 0`, GLOBAL_ASM kept):
- EnEiyer_Init: 9 words. Clone-spawn / child-chain register use (ROM reuses r0/r2/r1 differently); Kill-tail `mov r0,r4` is predicated in ours.
- EnEiyer_Draw: ~58 words. Graphics stub call (`GraphicsContext_UnknownStub`) ordering and gfx/action register use; size 308 vs 312.
- FUN_003de594 (CircleUnderground): 1 word. Compare `parent->actionFunc != FUN_003de594` emitted as `sub r0,pc,#..` (ROM: literal pool). Draft in actor cpp under `#if 0`, asm stays in functions_3C0000s.cpp.

Splits applied:
- FUN_00199688 @ 0x00199700 -> FUN_00199700 (Inactive, cfg tail; FUN_00199688 also used by Bg_Spot18_Shutter).

Layout:
- z_en_eiyer_anim.cpp (new TU): FUN_00239050 and EnEiyer_CurFramePtr (accessor, inlined by armlink). Keeps the Circle/Wander tail call and the ROM `add/add/vldr` accessor shape.
- Removed GLOBAL_ASM for the 15 matched FUN_ from src/functions/functions_*.cpp.
- data_syms.s: EQU for sColChkInfoInit/sCylinderInit/sDamageTable/sInitChain (0x522E08/10/48/68).
