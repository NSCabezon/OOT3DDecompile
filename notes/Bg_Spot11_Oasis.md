# Bg_Spot11_Oasis — Opus closing pass: 7/7 matched, ws_check baseline only (FUN_00249af8)

| Function | Status |
|---|---|
| BgSpot11Oasis_Init | matched |
| BgSpot11Oasis_Destroy | matched |
| BgSpot11Oasis_Update | matched (Opus): `self->actionFunc == FUN_003bf500` + write `draw` via `actor->` param (not `self->actor.`) -> r1 for the draw-pointer store |
| FUN_003bf500 / FUN_003af468 / FUN_003b307c | matched (moved from functions_3A0000s.cpp) |
| FUN_002ad270 (Draw) | matched (Opus), moved into actor .cpp; GLOBAL_ASM line deleted from functions_2A0000s.cpp. Fix: `f32 animSpeed;` uninitialized, `animSpeed = 1.0f;` written AFTER MTX34CopyAsm |

`__attribute__((used))` on sBubbleSpawnOffsets removed (Update now references it).
Files outside actor dir: src/functions/functions_3A0000s.cpp (3 lines removed, earlier pass), src/functions/functions_2A0000s.cpp (removed `GLOBAL_ASM("asm/FUN_002ad270.s")`).
