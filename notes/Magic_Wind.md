# Magic_Wind - Opus closing pass (2026-10-13)

ws_check.sh: baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| MagicWind_Destroy | MATCHED | Magic_Reset is FUN_0034708c (NOT empty), placed right after Destroy; armlink --tailreorder turns the tail `b` into `mov r0, r0`. Just tail-call FUN_0034708c(play). |
| FUN_0021e310 (FadeOut) | MATCHED (moved into z_magic_wind.cpp, GLOBAL_ASM removed from functions_200000s.cpp) | alpha = (s32)((f32)timer * R_UPDATE_RATE / 3.0f + 0.5f) * (1/30) via inline UpdateAlpha, N64 if/else shape. |
| MagicWind_Init | NOT matched, 2/116 words (asm kept, draft under #if 0) | Only case 0: ROM `vmov s0,s2; vmov s3,s16`, ours swapped. Needs: inline 7-arg SkelCurve init wrapper, zar-slot inline returning NULL, case 0 via 3-float SetAnim wrapper (cur=start), case 1 via 4-float one. |

Files outside actor dir: src/functions/functions_200000s.cpp (removed GLOBAL_ASM("asm/FUN_0021e310.s")).
