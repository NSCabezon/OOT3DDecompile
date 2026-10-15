
<!-- merge 2026-10-14 22:06:40 -->
# Bg_Mizu_Movebg (G13, haiku stage) - status

- BgMizuMovebg_Update (2 insns): MATCHED (C: `self->actionFunc(self, play)`; `BgMizuMovebg` header now typed: actionFunc 0x1BC, homeY 0x1C0, sfxFlags 0x1D4, dList 0x1DC, models 0x1E4/0x1E8).
- BgMizuMovebg_Destroy (32 insns): MATCHED. Uses actor-local `data_syms.s` EQU `BgMizuMovebg_sUnkFlags` = 0x00512FF8 (the D_8089EE40 global) and a 4-arg `FUN_00350f34` declared with `__asm("FUN_00350f34")` (include/functions.hpp only has the 3-arg form; the 4-arg overload can't coexist in extern "C").
- BgMizuMovebg_Draw (75 insns): NOT MATCHED. Draft under `#if 0` (~58-60 words off, fastchk). Blocker: the inlined identity+translate MTX34 is built with integer stores (CLAUDE.md "Integer-store identity+translate MTX34"), plus frame layout (ROM frame 0x6c, Vec3f trans at sp+0). Tried 6 variants (decl order x4, alpha as if / ternary). Draft kept for later.
