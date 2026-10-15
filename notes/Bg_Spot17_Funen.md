# Bg_Spot17_Funen: status (cascade stage 1, Haiku)

| Function | Status | Notes |
|---|---|---|
| BgSpot17Funen_Init (0x0028caec) | MATCHED | C, fastchk 25/25 words, ws_check baseline |
| BgSpot17Funen_Destroy (0x0028cb50) | MATCHED | C, tail call to FUN_00350f34, fastchk 3/3 words |
| BgSpot17Funen_Update (0x0039c168) | NOT MATCHED (asm) | functions.tsv merges 0x3b8 bytes of unlabeled code (0x39c184..0x39c53c) after the 5-instruction Update. Needs functions.tsv/cfg split before it can become C. Its update ptr 0x002ad610 is the trailing `bx lr` of FUN_002ad4d4. |
| FUN_002ad4d4 (Draw, functions_2A0000s.cpp) | NOT MATCHED (asm) | Actor draw (N64 func_808B7478), referenced only from Update. Its cfg entry also contains the empty update func at 0x002ad610 (`bx lr`), which Update points at, so it cannot leave asm without the cfg split. Not attempted. |

Data: `GLOBAL_ASM("data/z_Bg_Spot17_Funen.data.s")` kept. sInitChain (0x00513EB4) is exposed via `data_syms.s` (EQU).

Files changed (inside ws/Bg_Spot17_Funen only):
- src/game/actors/Bg_Spot17_Funen/z_bg_spot17_funen.cpp (Init, Destroy in C)
- src/game/actors/Bg_Spot17_Funen/z_bg_spot17_funen.hpp (0x1A4 = skelAnimModel pointer)
- src/game/actors/Bg_Spot17_Funen/data_syms.s (new, EQU sInitChain)

ws_check.sh: baseline only (FUN_00249af8).
