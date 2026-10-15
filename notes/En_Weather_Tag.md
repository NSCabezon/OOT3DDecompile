# En_Weather_Tag — STATUS (Opus closing pass)

All 15 functions MATCHED (fastchk 0 diff each; ws_check baseline only).

| Function | Status | Key trick |
|---|---|---|
| EnWeatherTag_Init | MATCHED | `(EnWeatherTag*, PlayState*)` signature + inline object-bank lookup helper |
| EnWeatherTag_Destroy | MATCHED | `params` local for the switch, but re-read `self->actor.params` inside WEATHER_TAG_RANGE100 |
| EnWeatherTag_Update | MATCHED (earlier) | |
| FUN_00328ddc | MATCHED (earlier) | |
| FUN_001ea4f0 DisabledCloudyHyruleMarket | MATCHED (moved from functions_1C0000s.cpp) | |
| FUN_0025a7d8 EnabledCloudyHyruleMarket | MATCHED (moved from functions_240000s.cpp) | |
| FUN_00207200 DisabledCloudyLonLonRanch | MATCHED (moved from functions_200000s.cpp) | |
| FUN_0021de8c DisabledCloudyDeathMountain | MATCHED (moved from functions_200000s.cpp) | |
| FUN_001ea5ac DisabledCloudySnow | MATCHED (moved from functions_1C0000s.cpp) | N64 `EnWeatherTag_SetupAction` static inline fixes r4/r5 swap |
| FUN_001ea540 DisabledRainLakeHylia | MATCHED (moved from functions_1C0000s.cpp) | same |
| FUN_0025a824 EnabledRainLakeHylia | MATCHED (moved from functions_240000s.cpp) | same |
| FUN_00176c68 DisabledRainThunder | MATCHED (moved from functions_140000s.cpp) | |
| FUN_00299704 DisabledCloudyRainThunderKakariko | MATCHED (moved from functions_280000s.cpp) | `s32 lc = 2; s32 sky = 0; if (sceneNum == 0x53) {...}` |
| FUN_0038ac64 EnabledCloudyRainThunderKakariko | MATCHED (moved from functions_380000s.cpp) | `s32 lc = 2; if (...) lc = 0;` |
| FUN_0020724c SetSandstormIntensity | MATCHED (moved from functions_200000s.cpp) | `if (inRange | accum)` (bitwise or) |

Not attempted (other Enabled actions, outside the listed set): FUN_00275218, FUN_002890a8, FUN_0025a888, FUN_00206004.
