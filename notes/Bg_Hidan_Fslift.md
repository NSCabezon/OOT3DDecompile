# Bg_Hidan_Fslift — STATUS (cascade stage 1, Haiku)

Result: 7/7 functions matched (4 actor functions + 3 action functions moved from functions_*.cpp). ws_check.sh shows baseline only (FUN_00249af8).

| Function | Where | Status | Notes |
|---|---|---|---|
| BgHidanFslift_Init | actor .cpp | matched | Syoku-style DynaPoly setup; spawn call needed `play` declared before `self` in locals (Init(Actor*, GameState*)) |
| BgHidanFslift_Destroy | actor .cpp | matched | |
| BgHidanFslift_Update | actor .cpp | matched | |
| BgHidanFslift_Draw | actor .cpp | matched | Same as Bg_Hidan_Syoku Draw |
| FUN_003e85ec (N64 BgHidanFslift_Idle) | moved into actor .cpp | matched | GLOBAL_ASM removed from functions_3E0000s.cpp |
| FUN_003d9eb4 (N64 BgHidanFslift_Descend) | moved into actor .cpp | matched | GLOBAL_ASM removed from functions_3C0000s.cpp |
| FUN_003ba174 (N64 BgHidanFslift_Ascend) | moved into actor .cpp | matched | GLOBAL_ASM removed from functions_3A0000s.cpp |

Data:
- `GLOBAL_ASM("data/z_Bg_Hidan_Fslift.data.s")` kept (raw dump at 0x511844).
- `BgHidanFslift_sInitChain` EQU 0x00511844 in `BgHidanFslift_data.s` (same pattern as Bg_Hidan_Syoku).

3DS layout: Actor world.pos at +0x28/+0x2C/+0x30, home.pos.y at +0xC (from the Descend/Ascend asm); actionFunc +0x1BC, timer +0x1C0, cameraSetting +0x1C2, skelAnimModel +0x1C4.

Not merged into oot3d/ (workspace only, per brief).
