# Bg_Haka — Opus closing pass

All functions matched (9/9). ws_check: baseline only (FUN_00249af8).

| Function | Status |
|---|---|
| BgHaka_Init / Destroy / Update | matched (earlier stage) |
| FUN_003e4064, FUN_003e1370, FUN_001e923c | matched (earlier stage, moved into actor .cpp) |
| BgHaka_Draw | matched (Opus): translate vector built in a `static inline BgHaka_Translate(MTX34*, f32 x, f32 y, f32 z)` helper (args land in s0/s1/s2 -> vmov s0,s1) |
| FUN_003de340 (BgHaka_Pull) | matched (Opus), moved into actor .cpp; GLOBAL_ASM line removed from src/functions/functions_3C0000s.cpp. Missing piece: 3DS-only `else if (sceneNum == LAKE_HYLIA && !FUN_0033caf8(GET_PLAYER(play)))` chime branch; also `minVelocityY * Math_SinS(..)` operand order |
