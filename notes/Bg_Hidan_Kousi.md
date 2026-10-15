# Bg_Hidan_Kousi: status (Opus closing pass)

ws_check: baseline only (FUN_00249af8). All 9 functions matched in C.

| Function | Status |
|---|---|
| BgHidanKousi_Init | MATCHED (Opus) - real ReadCollisionHeaderFromZsi call; `shape.rot.y + D_80889E7C[..]` operand order |
| FUN_00176fb8 (N64 func_80889C90) | MATCHED (Opus) - moved from functions_140000s.cpp |
| Destroy / Update / Draw, FUN_0013ebdc, FUN_003e2880, FUN_001980c8, FUN_0019bdf8 | MATCHED (earlier stages) |
