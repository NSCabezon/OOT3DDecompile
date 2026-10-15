# En_Yukabyun: Stage 1 (Haiku-only) status

Actor dir: `src/game/actors/En_Yukabyun/` (z_en_yukabyun.cpp, z_en_yukabyun.hpp). Header now has the 3DS layout
(Actor 0x1A4, actionFunc 0x1A4, timer 0x1A8, modelIdx 0x1AA, ColliderCylinder 0x1AC, skelAnimModel 0x204, size 0x208).

| Function | Status | Notes |
|---|---|---|
| EnYukabyun_Init | MATCHED (fastchk 0/56, ws_check baseline) | Init chain / cylinder init read via raw data addresses 0x530658 / 0x530660 (debt: data dump has no symbols). Timer formula `(10*params+20)*3.0*0.5+0.5`. |
| EnYukabyun_Destroy | MATCHED (fastchk 0/10) | Calls Collider_DestroyCylinder + FUN_003508b8. |
| EnYukabyun_Draw | MATCHED (fastchk 0/14) | First arg load kept via GraphicsContext_UnknownStub(play->state.gfxCtx) (inlined to nop). |
| EnYukabyun_Update | NOT MATCHED, left GLOBAL_ASM | Draft under #if 0. asm has `EnTuboTrap_WaitForProximity` as the compared action (En_Tubo_Trap's function, not declared in C), a FUN_003741e4 effect call, and raw collider-info reads at 0x1D2 / 0x1E8 not understood yet. |
| FUN_003e6880 (Wait action, functions_3E0000s.cpp) | NOT MATCHED, left GLOBAL_ASM | Draft under #if 0 in actor .cpp: 3 words differ (0x4, 0x14, 0x18), probably register/flags store shape. Needs moving the GLOBAL_ASM out of functions_3E0000s.cpp when matched. |
| FUN_003b9e3c (Rise action, functions_3A0000s.cpp) | NOT STARTED | Sets actionFunc = EnTuboTrap_WaitForProximity. Shared with En_Tubo_Trap logic, cross-check first. |
| FUN_00107054 (Break, functions_100000s.cpp) | NOT STARTED | Matches N64 EnYukabyun_Break (EffectSsHahen_SpawnBurst + Actor_Kill). Could move into actor dir if only this actor refers to it. |
| data/z_En_Yukabyun.data.s | kept as GLOBAL_ASM | Brief allows. |

Pending for a Sonnet pass: Update (biggest), FUN_003e6880, FUN_003b9e3c, FUN_00107054.
