# Bg_Haka_Zou: decomp status (stage 1, Haiku-only)

Baseline check (`scripts/ws_check.sh Bg_Haka_Zou`): only FUN_00249af8 differs (known). No new differences.

| Function | Address | Size | Status | Notes |
|---|---|---|---|---|
| BgHakaZou_Init | 0x00220E20 | 600 | MATCHED (actor .cpp) | Calls sInitChain / sCylinderInit via raw data-dump addresses 0x511570 / 0x511578 (data dump kept as GLOBAL_ASM). Actor uses 3DS uncull fields (0xFC/0x100/0x104). |
| BgHakaZou_Destroy | 0x00221078 | 76 | MATCHED (actor .cpp) | Frees skeleton via FUN_00350f34(actor, &skelAnimModel, 0). |
| BgHakaZou_Update | 0x0025E360 | 44 | MATCHED (actor .cpp) | Calls actionFunc; Actor_MoveForward for skull-wall rubble (3DS, not MoveXZGravity). |
| FUN_001546ec (BgHakaZou_WaitForObject) | 0x001546EC | 536 | MATCHED, MOVED | Moved from functions_140000s.cpp into the actor .cpp, name kept. Literal 0x003E1A70 used for DoNothing (unlabeled). |
| FUN_0025e314 (BgHakaZou_Draw) | 0x0025E314 | 76 | MATCHED, MOVED | Moved from functions_240000s.cpp into the actor .cpp, name kept. |
| FUN_00109fc4 (BgHakaZou_CrumbleSkullWall) | 0x00109FC4 | 192 | MATCHED, MOVED | Moved from functions_100000s.cpp into the actor .cpp, name kept. |
| FUN_003e5ad8 (BgHakaZou_WaitForHit) | 0x003E5AD8 | 752 | NOT MATCHED, left as GLOBAL_ASM | Stays in functions_*.cpp. Draft (N64 logic, unverified) under `#if 0` in the actor .cpp. Attempts not made (budget, Haiku-only). Helpers SpawnSkullWallRubble / SpawnRubbleParticles / BirdStatueAnim_Explode unresolved. |
| BgHakaZou_DoNothing | 0x003E1A70 | ? | NOT a function in the repo | Raw address literal used in WaitForObject (unlabeled). Tech debt. |

Data: `GLOBAL_ASM("data/z_Bg_Haka_Zou.data.s")` kept. C data arrays would shift the layout (see CLAUDE.md), so raw addresses are used.
Raw-address debt: 0x00511570 (InitChain), 0x00511578 (ColliderCylinderInit), 0x003E1A70 (DoNothing).

Files touched outside the actor dir (in this workspace only):
- src/functions/functions_100000s.cpp: removed GLOBAL_ASM("asm/FUN_00109fc4.s")
- src/functions/functions_140000s.cpp: removed GLOBAL_ASM("asm/FUN_001546ec.s")
- src/functions/functions_240000s.cpp: removed GLOBAL_ASM("asm/FUN_0025e314.s")
include/: untouched.
