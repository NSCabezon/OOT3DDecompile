
<!-- merge 2026-10-14 23:48:46 -->
# Bg_Hidan_Sima (G17, haiku stage)
- BgHidanSima_Destroy: MATCHED (C; fastchk 0/24). Header now types dyna/actionFunc/timer/collider/skelAnimModel.
- BgHidanSima_Update: MATCHED (C; fastchk 0/86) after collider loop was unrolled (ROM has no loop, no (s16) cast).
- FUN_00128734 (SinkingPlatform_Sink): MATCHED, moved into z_bg_hidan_sima.cpp; GLOBAL_ASM removed from functions_120000s.cpp.
  Link-level diff was one literal: home.y - 105.0f (not 100.0f). ws_check baseline.
- FUN_0017a578 (SinkingPlatform_Idle): MATCHED, moved into actor cpp; GLOBAL_ASM removed from functions_140000s.cpp.
  Needed early-return form (`if (y >= home.y) { action = FUN_003eb728; return; } action = FUN_00128734;`) for the
  NaN-aware lt/ge compare (fpmode=fast).
- FUN_003eb728 (SinkingPlatform_WarningShake): UNMATCHED, 41/80 words, size 228 vs 320. ROM has float angle rounding on the
  s16 Math_SinS/CosS argument (vnmlsle/vmlagt, sxth) that the draft lacks. Draft under #if 0; asm still in functions_3E0000s.cpp.
- FUN_003dfd44 (MovingPlatform_Move): UNMATCHED, 46/72 words, size 256 vs 288 (ROM uses 3DS timing: 90 - timer, 0x5a).
  Draft under #if 0; asm still in functions_3C0000s.cpp. Raw-address debt: MovingPlatform_Idle = 0x00159670 (inside an
  unlabeled cfg tail, not in functions.tsv), so the draft casts that address.

## Sonnet stage (G17)
- BgHidanSima_Init: MATCHED (data_syms.s EQUs for sInitChain/sJntSphInit; direct field stores animType/animSpeed keep 1 and 2.0 hoisted).
- FUN_003dfd44: MATCHED, moved into actor cpp (3DS timing 90 frames, *2/3 sine arg; vmla order dist*sin).
- FUN_003eb728: MATCHED, moved (angle*2.0f/3.0f rounding helper returning s32; `% 6`; world.rot.y).
- BgHidanSima_Draw: NOT matched, identity MTX34 guard (0x55A210/0x5BE29C) + matrix loop: tagged static/matrix blocker, not attempted.
