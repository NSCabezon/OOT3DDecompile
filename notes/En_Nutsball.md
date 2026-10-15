# En_Nutsball - STATUS (stage 3, Opus)

| Function | Status | Notes |
|---|---|---|
| EnNutsball_Init | MATCHED | Kill/actionFunc tail via `static inline EnNutsball_SetupWaitForObject(Actor* thisx, PlayState*)` with the cast inside -> ROM `ldrge r1`/`strge r1`. sObjectIds (0x4D9AFA) and sCylinderInit (0x52D168) are EQU symbols in actor-dir `data_syms.s` (no raw-address casts). |
| EnNutsball_Destroy | MATCHED | `(Actor*, GameState* state)`, `(PlayState*)state` inline, no play local -> model in r1, non-predicated call. |
| EnNutsball_Update | asm (skipped) | cfg-merged with Draw (functions.tsv size includes Draw); needs functions.tsv split. Draft under #if 0. |

ws_check.sh: baseline only (FUN_00249af8). Files touched: only src/game/actors/En_Nutsball/ (z_en_nutsball.cpp, new data_syms.s).
