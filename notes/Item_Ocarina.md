
<!-- merge 2026-10-14 18:55:01 -->
# Item_Ocarina (G8, sonnet stage)

Matched in C (ws_check baseline only):
- ItemOcarina_DoNothing, Update, Draw, GetThrown, StartSoTCutscene, WaitInWater, FUN_0010fb2c (moved earlier)
- ItemOcarina_Fly (`(ItemOcarina* self, PlayState* play)` signature + `self->actor.` everywhere; macro ternary for the rounding)
- FUN_0010e2ec (moved from functions_100000s.cpp, GLOBAL_ASM removed)
- header: spinRotOffset s16 @0x1A8

Left as asm:
- ItemOcarina_Init: draft under #if 0, 2 words off (`mov r0,#1; strb r0,[r4,#0x19a]` after the spin store: we emit r1). Key
  findings: switch with `case 0: case 1:` + ternary SetupAction gives the ROM's shared actionFunc store; block-scoped
  `s16 v = 0x400; self->spinRotOffset = v;` gives `mov r1,#0x1a8; mov r0,#0x400; strh`. ~55 variants.
- ItemOcarina_Destroy: cfg (split of tail FUN_00253a4c breaks link with L6221E at MagicDark_DiamondDraw); skipped by request.
