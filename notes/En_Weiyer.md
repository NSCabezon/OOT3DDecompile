
<!-- merge 2026-10-14 19:12:23 -->
# En_Weiyer (G12, haiku stage) STATUS

ws_check: baseline only (FUN_00249af8). Scratch dir ws/En_Weiyer/tmp removed at end.

## Matched (C, byte-identical in fastchk)
- EnWeiyer_Init, EnWeiyer_Destroy (actor .cpp; Destroy calls FUN_003508b8 via a 2-arg cast; Init calls FUN_00372f38 via a 3-arg cast; damage table = colChk+0x40)
- FUN_001cca7c  SetupTurnAround  (moved from functions_1C0000s.cpp; z_en_weiyer_setup.cpp)
- FUN_001c8264  SetupInactive    (moved from functions_1C0000s.cpp; z_en_weiyer_setup.cpp)
- FUN_003d59b8  Dead action      (moved from functions_3C0000s.cpp; actor .cpp)
- FUN_00364394  SetupFreeSwim    (moved from functions_360000s.cpp; z_en_weiyer_setup.cpp)
- FUN_00126840  TurnAround act.  (moved from functions_120000s.cpp)
- FUN_0019fce0  InitInsideWaterBox (moved from functions_180000s.cpp)
- FUN_00125798  StuckOnFloor act. (moved from functions_120000s.cpp)
- FUN_0034613c  SetupHurt        (moved from functions_340000s.cpp)
- FUN_0019b798  Hurt/Inactive-timer action (moved from functions_180000s.cpp)
- FUN_003e1608  Stunned action   (moved from functions_3E0000s.cpp)
- FUN_001236dc  Inactive action  (moved from functions_120000s.cpp; uses z_en_weiyer_anim.cpp accessor EnWeiyer_CurFramePtr)
- EnWeiyer_Draw (actor .cpp; opaque path + dead/transparent path with FUN_003687a8/FUN_003589cc/FUN_00358964)

## Not matched (kept as GLOBAL_ASM; C draft under #if 0 in actor .cpp where noted)
- FUN_0013f804 Die action (49 insns): 4 words differ. Draft under #if 0. Rounding timer `(s32)(0.5f + animLength*1.5f)` / `(s32)(animLength*1.5f - 0.5f)`: ROM keeps 0.5 in s2 and 1.5 in s3 with predicated vmlagt/vnmls; ~12 declaration/assignment/ternary forms tried.
- FUN_003461f0 SetupStuckOnFloor (41 insns): 6 words differ, same rounding-timer literal-order issue. Draft under #if 0 (the same block shape matches FUN_0034613c, so the difference is the velocity/regs around it).
- FUN_003dda10 StuckOnFloor-ish action (47 insns): 3 words differ (tail call to FUN_00364394 is right; home.y/pos.y compare load order). Draft under #if 0.
- EnWeiyer_OverrideLimbDraw (17 insns): 4 words differ (translate vector {0,0,2000}: ROM zero in s0, copy in s1). Draft under #if 0 with Vector3f.
- FUN_00121024 Hurt action (57 insns): NOT matched; first draft 38 words off (rounding of timer*2/3 feeds sinf; sizes differ). Left as GLOBAL_ASM, no draft kept. ROM literals: 2.0, 1/3, 0.5, pi/5, 5120.

## Notes
- Functions called from other TUs must not sit in z_en_weiyer.cpp (armcc --forceinline inlines same-TU callees). FUN_00364394, FUN_001c8264, FUN_001cca7c live in z_en_weiyer_setup.cpp.
- Callee names that are not the plain symbol matter: Animation_OnFrameImpl resolves to 0x3736fc but the ROM calls FUN_0036e5e0 (use the FUN_ name).
- Out-of-line accessor `EnWeiyer_CurFramePtr` (z_en_weiyer_anim.cpp) reproduces the ROM `add r0,#0x1a4; add r0,#0x3c; vldr` shape.
- Data: data_syms.s EQUs for the data in data/z_En_Weiyer.data.s (sColChkInfoInit 0x53014C, sCylinderInit 0x530154, sDamageTable 0x53018C, sInitChain 0x5301AC).
- Actor struct (header): actionFunc 0x228, timer 0x22C (s16), targetYaw 0x22E (s16), jointTable 0x230, morphTable 0x508, swimHeight 0x7E0, targetSwimHeight 0x7E4, collider 0x7E8 (size 0x840).
- EnWeiyer_Update is not in the prompt list; left as GLOBAL_ASM.
