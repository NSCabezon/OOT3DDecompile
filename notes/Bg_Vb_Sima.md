
<!-- merge 2026-10-14 10:11:44 -->
# Bg_Vb_Sima STATUS (cascade stage 1, Haiku, batch 1/1)

| Function | Status | Notes |
|---|---|---|
| BgVbSima_Init | MATCHED (C) | Attempt 1 (word-level 0/34; ws_check clean). Needs `sInitChain` EQU (data_syms.s, 0x00514154). Collision header via real `ReadCollisionHeaderFromZsi(DynaPolyInfo_Alloc(..), &colHeader)`, linker-inlined as in ROM. |
| BgVbSima_Destroy | MATCHED (C) | Attempt 1. Same shape as Bg_Gate_Shutter Destroy (`FUN_00350f34(actor, &skelAnimModel, 0)` tail). |
| BgVbSima_Draw | MATCHED (C) | Attempt 1 (typed `self` local, MTX34CopyAsm + SetUnkAC(1) + FUN_003721e0 + FUN_00372170(0)). Same as Bg_Spot12_Gate Draw. |
| FUN_003a3200 | MATCHED (C) | Attempt 1. Local struct `BgVbSimaModelState` (model ptr at 0x00, flags 0x36..0x43); FUN_0036932c/FUN_0037266c declared locally. |
| BgVbSima_Update | MATCHED (C, Opus stage 3) | 0/275. Fixes: helper (inlined N64 SpawnEmber) loop counter `s32 i` (s16 added sxth, +4 B); `s32 emberScaleBase = 8;` declared right after `if (platformSignal != 0) {` and used as `(s16)Rand_ZeroFloat(2.0f) + emberScaleBase` → `mov r8,#8` hoisted to outer preheader. |

Header change: `BgVbSima` now `DynaPolyActor dyna` + `skelAnimModel` at 0x1D4 (size 0x1D8 unchanged).

UNMATCHED: none (all 5 functions matched)
