# Bg_Hidan_Syoku: status (stage 1, Haiku)

Result: 9/9 functions matched, ws_check.sh shows baseline only (FUN_00249af8). Data dump unchanged.

## Matched (in actor dir, src/game/actors/Bg_Hidan_Syoku/z_bg_hidan_syoku.cpp)
- BgHidanSyoku_Init (0x002781a8)
- BgHidanSyoku_Destroy (0x00278254)
- BgHidanSyoku_Update (0x0029bdd0)
- BgHidanSyoku_Draw (0x0029bd84)

## Matched, moved from src/functions/ (GLOBAL_ASM lines removed there)
- FUN_003e7e54 (action, N64 func_8088F4B8), was functions_3E0000s.cpp
- FUN_003ba0e4 (action, N64 func_8088F514, 47C inlined), was functions_3A0000s.cpp
- FUN_003e1fbc (action, N64 func_8088F62C), was functions_3E0000s.cpp
- FUN_003d9a14 (action, N64 func_8088F5A0), was functions_3C0000s.cpp
- FUN_00180574 (N64 func_8088F47C helper, noinline), was functions_180000s.cpp

## Not matched
- none

## Data
- data/z_Bg_Hidan_Syoku.data.s kept as GLOBAL_ASM (layout shared with Bg_Ice_Objects).
- BgHidanSyoku_data.s: EQU BgHidanSyoku_sInitChain = 0x00511F80 (InitChain used by Init).

## Attempts log
- FUN_003d9a14: first compile 144 B vs 112 B; cause = armcc inlined FUN_00180574 into it. Fixed with __attribute__((noinline)) on the prototype. Then branch order fixed to `if (timer == 0)` first (N64 order). Matched.
