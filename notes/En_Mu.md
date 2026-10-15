# En_Mu (Haiku stage 1) status

Actor dir: `src/game/actors/En_Mu/z_en_mu.cpp` (+ `z_en_mu.hpp` layout). Check: `ws_check.sh En_Mu` = baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| EnMu_Init | matched (C) | 0/59 words (fastchk), link ok |
| EnMu_Destroy | matched (C) | |
| EnMu_Pose | matched (C) | tail call to FUN_00370f5c (fall-through, shows as mov r0,r0) |
| EnMu_Update | NOT matched (asm) | best draft 13/57 words off: struct copy of world.pos gets r0 as ldm temp, ROM keeps play in r6 before the copy. Draft under `#if 0`. |
| EnMu_Draw | matched (C) | colors/face tables read from raw ROM addresses 0x4D99E4 / 0x4D99DC (debt, see below) |
| EnMu_Interact | matched (C) | uses gSaveContext.eventInf[2] bits 0..4 |
| EnMu_CheckDialogState | matched (C) | |
| EnMu_GetFaceReaction | matched (C) | |
| EnMu_OverrideDrawLimb | matched (C) | |
| EnMu_PostDrawLimb | matched (C) | |

Layout notes (3DS): actionFunc 0x568, collider 0x56C, npcInfo 0x5C4, defaultTextId 0x5EC, fidgetTableY 0x5EE, fidgetTableZ 0x60E, skelAnimModel 0x630, size 0x634.

Debt: Draw uses raw ROM addresses (`0x004D99E4` colors via struct copy, `0x004D99DC` face table) because armcc places a file-scope table in an unpinned .constdata section (0x832xxx) instead of the ROM rodata. Collider/CollisionCheck init data also raw (`0x0052CDF8`, `0x0052CE30`), same as En_Tg.

Files touched outside the actor dir: none. include/: none. Commit/push: none.

Remaining for a later stage: EnMu_Update (see draft under `#if 0`).
