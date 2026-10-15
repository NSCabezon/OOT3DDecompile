# Bg_Spot12_Saku: status (cascade stage 1, Haiku)

Workspace: ws/Bg_Spot12_Saku. ws_check.sh: only baseline FUN_00249af8 differs. Build OK.

| Function | Location | Status | Notes |
|---|---|---|---|
| BgSpot12Saku_Init | actor .cpp | MATCHED | Init chain moved to C (sBgSpot12SakuInitChain), replaces data GLOBAL_ASM |
| BgSpot12Saku_Destroy | actor .cpp | MATCHED | |
| BgSpot12Saku_Update | actor .cpp | MATCHED | |
| BgSpot12Saku_Draw | actor .cpp | MATCHED | |
| BgSpot12Saku_DoNothing | actor .cpp | MATCHED | |
| FUN_003c0afc | moved from functions_3C0000s.cpp into actor .cpp | MATCHED | wait action (N64 func_808B357C); keeps ld name |
| FUN_003cc43c | moved from functions_3C0000s.cpp into actor .cpp | MATCHED | open action (N64 func_808B3604); keeps ld name |

Attempts on FUN_003cc43c:
- `fabsf` undefined without `__fabsf`; `x<0?-x:x` produced vneg + branch (size 308 > 296 slot, L6221E overlap).
- Bit-mask `(bits & 0x7FFFFFFF) < 0x38d1b717` matched size but compare shape differed.
- Final: `__fabsf(temp_ret) < 0.0001f` (vabs path) and `temp_f18 * Math_SinS(...)` operand order. Matches.

Files outside the actor dir: src/functions/functions_3C0000s.cpp (2 GLOBAL_ASM lines removed). include/: none.
Not committed.
