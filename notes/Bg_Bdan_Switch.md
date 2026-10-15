
<!-- merge 2026-10-14 23:46:34 -->
# Bg_Bdan_Switch (G17, haiku stage)
- BgBdanSwitch_Destroy: MATCHED (C in z_bg_bdan_switch.cpp, fastchk 0/28; ws_check baseline).
- BgBdanSwitch_Draw: C matches ROM (fastchk 0/78, dead `f32 zz` local + pos block needed for VFP/arg order), BUT the
  function-local guarded static Vector3f (guard 0x510A98 / object 0x569908) needs a data/oot3d.ld pin (pin_static, infra);
  link fails (L6224E) without it. Kept as #if 0 draft + GLOBAL_ASM.
- BgBdanSwitch_Update: UNMATCHED, 80/136 words (draft 512 B vs 544 B). Inlined func_8086D0EC switch with per-case float
  scheduling differs. Draft under #if 0 + GLOBAL_ASM.
- BgBdanSwitch_Init: not in this batch (earlier draft, still #if 0).

## Sonnet stage (G17)
- BgBdanSwitch_Draw: MATCHED, moved to own TU z_bg_bdan_switch_draw.cpp (guard = anon .data of that TU, pinned after the asm data chunk).
  pin_static: `pin --guard 0x510A98 --guard-sel "z_bg_bdan_switch_draw.o(+DATA)" --obj 0x569908 --obj-size 12 --obj-sel "z_bg_bdan_switch_draw.o(+BSS)" --label z_bg_bdan_switch_draw`
- BgBdanSwitch_Update: MATCHED (unk_1D0 = ...*0.005*1C8 then `*= 0.95f` for types 0-2; radius is (s16) cast).
- BgBdanSwitch_Init: UNMATCHED 27/172 words (far): play2 copy placement; copying play2 at entry gets CSE'd (134 words). #if 0 draft.
