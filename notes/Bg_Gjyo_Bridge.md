# Bg_Gjyo_Bridge: decomp status (stage 1, Haiku)

Result: 6/6 actor functions matched (ws_check.sh: baseline FUN_00249af8 only).

| Function | Status | Notes |
|---|---|---|
| BgGjyoBridge_Init | matched | init chain via raw address 0x00510F88 (data asm unlabeled) |
| BgGjyoBridge_Destroy | matched | |
| BgGjyoBridge_Update | matched | |
| BgGjyoBridge_Draw | matched | |
| BgGjyoBridge_TriggerCutscene | matched | cutscene cue/PlayState offsets raw in SpawnBridge (play+0x22E4) |
| BgGjyoBridge_SpawnBridge | matched | |
| FUN_003e1fb4 (moved from functions_3E0000s.cpp) | matched | N64 func_808787A4 (empty). Only referenced by this actor's Init |

Files touched outside the actor dir:
- src/functions/functions_3E0000s.cpp: GLOBAL_ASM("asm/FUN_003e1fb4.s") replaced by a comment (function moved into actor cpp).

include/ additions: none.

Debt:
- Init chain pointer is raw (0x00510F88); data/z_Bg_Gjyo_Bridge.data.s has no label.
- SpawnBridge reads csCtx.actorCues[2] by raw offset (play+0x22E4) because CutsceneContext lacks the field.
- Address-based globals: gSaveContext.eventChkInf[4] (0x2000) is the flag used by both Init and SpawnBridge.
