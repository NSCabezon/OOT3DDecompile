# Demo_Sa (Haiku stage 1, Sonnet stage 2) status

| Function | Status | Notes |
|---|---|---|
| DemoSa_Destroy | MATCHED (C) | |
| DemoSa_Update | MATCHED (C) | Table via EQU `DemoSa_sUpdateFuncs` (data_syms.s), no raw address. |
| DemoSa_Draw | MATCHED (C, Sonnet) | Face setter through static inline `DemoSa_FaceSet(face, i, v)` wrapper fixed the add r0 / mov r1 order. Table via EQU `DemoSa_sDrawFuncs`. |
| DemoSa_Init | NOT MATCHED (asm) | Draft under `#if 0`: 25/253 words, size equal. Only register allocation left (ROM: hoisted `2` in sb and shape in r8; C puts `2` in r8). Pointer-store helpers for updateIndex/drawIndex fixed the r0/r1 temps (43 -> 25). |
| caseD_2_00245298, caseD_6_0027dfb0, caseD_12_00385bec, caseD_13_0037db6c, caseD_a_0038d81c, caseD_d_0037dad4, caseD_e_00385a0c, caseD_4_002a1980, caseD_f_0039a6f8, caseD_14_0037dbb4 | MATCHED (C, Sonnet) | Moved from functions_*.cpp into z_demo_sa.cpp (GLOBAL_ASM lines deleted). `play2` pattern for Actor_UpdateBgCheckInfo, `DemoSa_Blink(Actor*)` inline, FUN_00370734 s32-return cast. |
| caseD_1_0027df24 | asm (5/35 words) | Draft under `#if 0`; cue ptr in r1 + arg move order. |
| caseD_3_0028ff60 | asm (6/45) | csCtx pointer reuses play reg in ROM. |
| caseD_5_0028fe84 | asm (7/55) | player-pos arg order. |
| caseD_0, 7, 8, c, 11 | not attempted | caseD_9 shared with Demo_Du. |
