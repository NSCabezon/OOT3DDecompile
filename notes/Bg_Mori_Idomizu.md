# Bg_Mori_Idomizu (stage 1, Haiku-only) — STATUS

Final `ws_check.sh Bg_Mori_Idomizu`: only baseline `FUN_00249af8` differs. Non-function bytes: 0 differing.

## Functions (6 total, all matched)

| Function | Where | Status | Notes |
|---|---|---|---|
| BgMoriIdomizu_Init | actor .cpp | MATCHED | scale z/y store order matters; WaterBox stride workaround |
| BgMoriIdomizu_Destroy | actor .cpp | MATCHED | 3-arg FUN_00350f34 call (r3 untouched by 3DS code) |
| BgMoriIdomizu_Update | actor .cpp | MATCHED | |
| FUN_0011076c | moved from functions_100000s.cpp into actor .cpp | MATCHED | wait-for-object action; only referenced by Init |
| FUN_003f7224 | moved from functions_3E0000s.cpp into actor .cpp | MATCHED | main drain action; only referenced by FUN_0011076c. Needed the N64 if/else with duplicated sfx call to get the literal-pool order right |
| FUN_002ac5a0 | moved from functions_2A0000s.cpp into actor .cpp | MATCHED | draw (actor.draw at +0x140); only referenced by FUN_0011076c |

Data `z_Bg_Mori_Idomizu.data.s` (`DCD 0xFFFF0000` @0x513350) replaced by C struct `sData { s16 isSpawned; s16 unk_02 = -1 }`, placed before InitVars. Matches.

## Debt / things to know
- `play->roomCtx.unk_00[0]` used for `curRoom.num` (repo RoomContext has no curRoom; offset 0x4C30).
- WaterBox: repo type is 4 bytes, 3DS stride is 0x10 → indices written as `waterBox[n * 4]`.
- Magic numbers for not-yet-defined symbols: OBJECT_MORI_TEX = 0x73, CAM_ID_MAIN = 0, csId 3240, sfx 0x10001B5.
- Draw/Main/wait funcs keep their FUN_ names (ld-pinned).

## Files touched (relative to ws/Bg_Mori_Idomizu)
- src/game/actors/Bg_Mori_Idomizu/z_bg_mori_idomizu.cpp
- src/game/actors/Bg_Mori_Idomizu/z_bg_mori_idomizu.hpp
- src/functions/functions_100000s.cpp (GLOBAL_ASM FUN_0011076c removed)
- src/functions/functions_3E0000s.cpp (GLOBAL_ASM FUN_003f7224 removed)
- src/functions/functions_2A0000s.cpp (GLOBAL_ASM FUN_002ac5a0 removed)
No include/ changes. No commit/push.
