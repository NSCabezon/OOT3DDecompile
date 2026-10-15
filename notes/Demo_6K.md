
<!-- merge 2026-10-14 18:08:35 -->
# Demo_6K (G5, haiku stage)
- Demo6K_Update: MATCHED (C: `self->actionFunc(actor, state)` tail call).
- Demo6K_Destroy: MATCHED (C switch on params; model slots through a variadic cast of FUN_00350f34, NULL-terminated; case-block order matters: 0,1,2,3-11/14-19,12,13).
- Demo6K_Init: NOT MATCHED (1236 B). C draft kept under `#if 0` in z_demo_6k.cpp, GLOBAL_ASM("asm/Demo6K_Init.s") still active.
  Draft: 46 of 282 instructions differ. Remaining diffs:
  * play/table register swap: ROM keeps play in sb and the Demo6K_sModelIndex table in sl; ours is the reverse (sb/sl). Declaration order, block-scoped play2, and table-pointer locals did not change it.
  * actionFunc literal (FUN_003f1510) loaded in ROM before `cmp params,#0x14`; ours compares later.
  * case 13: ROM loads the action pointer into r0 before the draw store; ours loads it late (only a 1-line gain from reordering).
  * 3DS-only code in func_80967A04 (inlined in case 0): `if (unk_36C) { zar->GetCMABByIndex(...); skelAnimModel[8+i]->unk_0C->FUN_00372d94(...) }`. Matches.
- Header: z_demo_6k.hpp has the 3DS layout (initActionFunc 0x1A4, lightInfo 0x1A8, lightNode 0x1C0, unk_164..unk_170, unk_174..unk_274 arrays, drawFunc 0x2E4, actionFunc 0x2E8, flags/timers/requiredObjectSlot/unk_293, models 0x2F8..0x368, zarInfo 0x36C).
- data_syms.s (actor dir): Demo6K_sObjectIds (0x51B3D8), Demo6K_sModelIndex (0x51B3B0).
