# Demo_Ext — Opus closing pass (2026-10-13)

| Function | Status |
|---|---|
| DemoExt_Init | matched (C, earlier pass) |
| DemoExt_Draw | matched (C); dispatch table now via EQU symbol `DemoExt_sDrawFuncs` (data_syms.s) |
| DemoExt_Destroy | asm: span includes 3 trailing `bx lr` words (likely 3 unlabeled empty fns) -> needs cfg split (skipped) |
| DemoExt_Update | asm: cfg-merged 172 B blob (skipped); draft uses `DemoExt_sUpdateFuncs` |
| caseD_0_001f0880 (Wait) | NOT matched: 30/55 words, 212 vs 220 B (ROM `mov r1, r4` self copy for cue-2 stores) |
| caseD_1_00245094 (Maintain) | NOT matched: 54/107 (same HandleCues issue + reg swaps) |
| caseD_2_001f0678 (Dispell) | NOT matched: 10/130 (scheduling/reg choice, see draft comment) |
| caseD_1_002247f8 (vortex draw) | skipped (out of scope) |

ws_check.sh: baseline only (FUN_00249af8).
