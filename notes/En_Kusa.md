# En_Kusa — Opus closing pass (2026-10-13 07:2x)
| Function | Status |
|---|---|
| EnKusa_Update | matched (earlier) |
| EnKusa_Destroy | MATCHED — 3rd call is FUN_0035021c(models[2]); `mov r0,r0` = tailreorder fall-through into FUN_0035021c (next fn) |
| FUN_00110450 (WaitForObject) | MATCHED, moved from functions_100000s.cpp |
| FUN_00111140 (type-2 lift-only main) | MATCHED, moved from functions_100000s.cpp (N64 SetupAction/SetupLiftedUp static helpers) |
| FUN_001f7510 (Draw) | MATCHED, moved from functions_1C0000s.cpp (`(EnKusa*, PlayState*)` signature fixed regs) |
| EnKusa_Init | asm (not targeted; draft under #if 0) |
| FUN_003bde20, FUN_003bb3c8, FUN_003cbcf0, FUN_003f7748, FUN_003bc564 | not targeted, still asm in functions_*.cpp |
ws_check.sh: baseline only (FUN_00249af8).
