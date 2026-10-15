
<!-- merge 2026-10-15 16:23:24 -->
# Oceff_Storm (G31) — STATUS (Haiku + Sonnet passes)

ws_check: baseline only (FUN_00249af8), 0 non-function bytes.

| Function | Result | Notes |
|---|---|---|
| OceffStorm_Update (20) | MATCHED | |
| OceffStorm_UnkAction (21) | MATCHED | 3DS scaling `alpha = (u8)(alpha_f + 0.5f + R*(1/3)*5)` |
| OceffStorm_Destroy (62) | MATCHED | needs `_ZTI15OceffStormModel`/`_ZTI15OceffStormFreer` EQUs in src/game/shared_syms.s |
| OceffStorm_Draw (70) | MATCHED (Sonnet) | `buf` in an inner block (tail call `b OceffStorm_Draw2`), dead `OceffStorm* s2 = self;` used only for `s2->vtxAlpha` (self/i regs), `(Pause == 0) ? 1.0f : 0.0f`, model position stores through an inline `OceffStorm_SetPos(model, x, y, z)` (keeps `ldr model` once; locals x/y/z shape also works). |
| FUN_003f450c (117, = OceffStorm_DefaultAction, moved from functions_3E0000s.cpp) | MATCHED (Sonnet) | `(s32)` casts for primColorAlpha (no `(s8)` = no extra `and`), third arm: `scale.x = scale.z = 0.4f` BEFORE `vtxAlpha = 255`. GLOBAL_ASM removed from functions_3E0000s.cpp. |
| OceffStorm_Init (210) | MATCHED (Sonnet) | `__FILE__` string: write the literal `"d:\\home\\queen\\dailyBuild\\game_us\\sources\\z_oceff_storm.cpp"` and put it in a `const char* file` local right before the `Alloc` call (armcc emits it inside the function literal pool; the local keeps it ahead of the int literals as in the ROM) — this should also unlock the "`__FILE__`-in-.text" blocker class (EnGanonMant_Update, EffDust_Init, EnJsjutan_Update). Allocator slot 3 = `Alloc(size, file, line)` on the 0x55A1F8 object (`OceffStormFreer`, same _ZTI EQU as Destroy). GetModelManager() scoped per use. Dead `s2` alias on the first `FUN_00348a64` call fixes callee-saved numbering. Data: `OceffStorm_sUnk535E9C` EQU in new `data_syms.s`. |
| OceffStorm_Draw2 (133) | UNMATCHED big (~130w) | GLOBAL_ASM kept; draft under `#if 0`. Data flow decoded (rgba at obj+0xF0, two MTX34_MakeTrans scroll matrices at +0x110/+0x140, `FUN_00328350(mm+0x25F0, 2, obj, 0)`), but armcc store-forwards the colour/MTX temps instead of keeping them on the stack (ROM copies sp+0x14 → obj with ldm/stm); same VFP-numbering/hoisting class as OceffWipe*_Draw. |

## Shared-file edits
- `src/game/shared_syms.s`: `_ZTI15OceffStormModel EQU 0x7FFF0050`, `_ZTI15OceffStormFreer EQU 0x7FFF0051` (Haiku pass; apply to main).
- `src/functions/functions_3E0000s.cpp`: removed `GLOBAL_ASM("asm/FUN_003f450c.s")` (function now C in the actor .cpp).
- New `src/game/actors/Oceff_Storm/data_syms.s` (EQUs OceffStorm_sUnk535E9C, OceffStorm_sScroll); `.s` under src/ needs `git add -f`.
