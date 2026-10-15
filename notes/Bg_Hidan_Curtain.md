
<!-- merge 2026-10-14 10:16:00 -->
# Bg_Hidan_Curtain: batch 1/2 (cascade stage 1, Haiku)

ws_check.sh: baseline only (FUN_00249af8).

| Function | Where | Status | Notes |
|---|---|---|---|
| FUN_003d5fd4 | moved to actor .cpp | MATCHED (1st variant) | N64 BgHidanCurtain_WaitForCutscene |
| FUN_0010b9d0 | moved to actor .cpp | MATCHED (1st variant) | N64 BgHidanCurtain_WaitForClear |
| FUN_0010bdc8 | moved to actor .cpp | MATCHED (1st variant) | N64 BgHidanCurtain_WaitForSwitchOff |
| FUN_003ba250 | moved to actor .cpp | MATCHED (1st variant) | N64 BgHidanCurtain_TurnOn |
| FUN_003e8738 | moved to actor .cpp | MATCHED (1st variant) | N64 BgHidanCurtain_WaitForSwitchOn; timers 75/45 (N64 50/30 x1.5) |
| FUN_003d9f6c | moved to actor .cpp | MATCHED (1st variant) | N64 BgHidanCurtain_TurnOff; timers 600/300/240/450 |
| BgHidanCurtain_Destroy | actor .cpp | MATCHED (1st variant) | Collider_DestroyCylinder + FUN_00350f34(actor, &model, 0) tail call |
| BgHidanCurtain_Draw | actor .cpp | MATCHED (2nd variant) | 1st variant had the speed literal loaded before MTX34CopyAsm; ROM loads it after |

## Debt / notes
- `BgHidanCurtain_WaitForTimer` (N64 name) has no symbol: code at 0x0010ABAC sits inside `BgHidanFwbig_WaitForPlayer` (cfg-merged, unlabeled). Referenced via `EQU` in `BgHidanCurtain_data.s`. Needs a cfg split to become a real function.
- `sHCParams` lives in the data dump at 0x00511648; referenced via `EQU` in `BgHidanCurtain_data.s`.
- Struct now typed: actionFunc 0x1A4, type/treasureFlag/size/alpha 0x1A8..0x1AB, timer 0x1AC, texScroll 0x1AE, collider 0x1B0 (0x58), model 0x208. Size 0x20C unchanged.
- BgHidanCurtain_Init: MATCHED (stage 2, Sonnet). Idioms: sCylinderInit derived as `(u8*)sHCParams - 0x38` (ROM `sub r3,r8,#0x38`), sCcInfoInit via EQU 0x00511608, animSpeed 2.0f, MQ (masterQuestFlag==1, sceneNum 6, room 0x1A) uses sHCParams[2].scale and radius*1.5, `((BgHidanCurtain*)thisx)->actionFunc` for the type==0 store, `thisx->` for the pos.y store, size via if/else, texScroll rounding macro (no gGameInfo).

# Batch 2/2 (cascade stage 1, Haiku)

| Function | Where | Status | Notes |
|---|---|---|---|
| BgHidanCurtain_Update | actor .cpp, GLOBAL_ASM + `#if 0` draft | NOT MATCHED (2 words, 0x48/0x4c) | Cause: ROM puts the AT_HIT-clear result in r1 (`bic r1,r0,#2`), armcc keeps it in r0 across ~8 variants (plain/`(u8)`/temp local/`!= 0`/explicit assign). Camera `setting` via `u8* cam = cameraPtrs[0] + 0x100; *(s16*)(cam+0x8A)` matches the ROM add+ldrsh form. |

- Stage 2 (Sonnet): Update still 2 words (0x48/0x4c, bic r1 vs r0), ~35 more variants failed (play2 routing, thisx casts, flag locals, helpers, camera double-read, yaw locals); kept GLOBAL_ASM + #if 0 draft.
- Update draft uses `FUN_00374bb8` (knockback), `FUN_00373264` (Actor_PlaySfx_Flagged, sfx 0x010001FA), `gSaveContext.sceneSetupIndex < 4` (= !IS_CUTSCENE_LAYER, ROM reads gSaveContext+0x14E8), camera setting 0x28/0x38 raw offset 0x18A.
- ws_check.sh: baseline only (FUN_00249af8).

## Files touched outside the actor dir
- none in batch 2 (only the actor .cpp and this STATUS.md)

## Files touched outside the actor dir
- src/functions/functions_100000s.cpp (GLOBAL_ASM lines FUN_0010b9d0, FUN_0010bdc8 removed)
- src/functions/functions_3C0000s.cpp (FUN_003d5fd4, FUN_003d9f6c removed)
- src/functions/functions_3E0000s.cpp (FUN_003e8738 removed)
- src/functions/functions_3A0000s.cpp (FUN_003ba250 removed)
- include/: none
- Stage 3 (Opus): Update still 2 words (0x48/0x4c). ~45 more variants failed: full play/play2 brute force (all ≤3-swap combos), thisx-cast brute force on the 3 atFlags accesses, inverted cs branch, switch, early return, `^=`/`-=`/0xFD clears, shift/==/!! checks, collider/base pointers (scoped and function-wide), clear-helpers (self/Collider*/ColliderCylinder*/Actor*), whole-check and whole-body inline helpers, arg locals, comma-in-arg, merged `cs || hit` clear, top-level atFlags local, hcParams placement, s32 setting/reused temp. Only forms that keep `thisx` live in r0 produce `bic r1` (but then atFlags moves to r2 → 12+ words). Kept GLOBAL_ASM + draft.
