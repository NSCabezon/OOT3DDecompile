# Bg_Zg — Opus closing pass (2026-10-13)

ws_check.sh Bg_Zg: baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| BgZg_Draw | MATCHED (C) | fix: sDrawFuncs as real EQU symbol (BgZg_data.s) instead of raw-address cast |
| BgZg_Init | NOT MATCHED (asm, draft #if 0) | 4 words: register pair of the params type check (ldrsh r1/and r0 vs r0/r1). Stack slot fixed (late `colHeader = NULL` + real ReadCollisionHeaderFromZsi, armlink-inlined) |
| caseD_0_001a6260 | NOT MATCHED (asm in functions_180000s.cpp, draft #if 0) | 3 words: ldrh temp register (r2 vs r1) |
| BgZg_Update / FallAway | skipped | cfg-merged |

Files: src/game/actors/Bg_Zg/z_bg_zg.cpp, src/game/actors/Bg_Zg/BgZg_data.s (new, EQU symbols). Nothing outside the actor dir.
