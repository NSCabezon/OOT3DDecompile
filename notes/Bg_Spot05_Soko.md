# Bg_Spot05_Soko: status (stage 1, Haiku)

Result: 5/5 functions matched, ws_check shows baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| BgSpot05Soko_Init | matched | switchFlag = `(u8)(params >> 8)` (the `PARAMS_GET_U` form and `(u32)(u16)<<16>>24` both mismatch). Model loader called via 7-arg function-pointer cast. |
| BgSpot05Soko_Destroy | matched | model free via 4-arg cast (tail call). |
| BgSpot05Soko_Update | matched | `actionFunc(self, play)`. |
| BgSpot05Soko_Draw | matched | params==0 and params!=0 branches written separately (one shared tail merged and mismatched). |
| BgSpot05Soko_DoNothing | matched | empty. |
| FUN_003e8214 (moved from functions_3E0000s.cpp) | matched | sets speedXZ before actionFunc (order matters). |
| FUN_003e0854 (moved from functions_3E0000s.cpp) | matched | action after FUN_003e8214 (N64 func_808AE630). |

Notes:
- The `data/z_Bg_Spot05_Soko.data.s` GLOBAL_ASM was replaced by `sBgSpot05SokoInitChain` (C, after InitVars). Bytes match.
- 3DS struct: DynaPolyActor dyna (0x000..0x1BC), actionFunc 0x1BC, switchFlag 0x1C0, skelAnimModel 0x1C4, skelAnimModel2 0x1C8 (size 0x1CC).
- Moved functions FUN_003e8214 and FUN_003e0854 out of `src/functions/functions_3E0000s.cpp` (GLOBAL_ASM lines deleted in ws only).
