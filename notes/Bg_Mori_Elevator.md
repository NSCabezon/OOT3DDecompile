# Bg_Mori_Elevator: STATUS (Opus closing pass, 2026-10-13)

ws_check.sh: baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| FUN_0012adb4 (MoveIntoGround) | MATCHED | in new TU `z_bg_mori_elevator_move.cpp`; GLOBAL_ASM removed from functions_120000s.cpp |
| FUN_0012b7e8 (MoveAboveGround) | MATCHED | same TU; GLOBAL_ASM removed from functions_120000s.cpp |
| FUN_003f73b4 (StopMovement action, func_808A2008) | MATCHED | same TU; GLOBAL_ASM removed from functions_3E0000s.cpp |
| FUN_003bf708 (SetPosition) | NOT MATCHED (needs cfg split) | ROM region 576 B = 548 B code+pool + 28 B of an unrelated function at 0x003BF92C. Draft (#if 0 in main .cpp) is 548 B, 5 words off (r7/ip swap in IsPlayerRiding). |

Key finding: the move functions match with the plain N64 code, but only when compiled in a TU that does NOT
define FUN_003600e4/FUN_003600d4. In the same TU, armcc inlines FUN_003600d4 and uses intra-TU register
knowledge across the FUN_003600e4 call (0.0/1.0 in s6/s7 instead of s16/s17 + vpush {d8}).
