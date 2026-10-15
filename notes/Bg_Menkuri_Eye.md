
<!-- merge 2026-10-14 09:58:51 -->
# Bg_Menkuri_Eye: cascade stage 1 (Haiku), batch 1/1

- BgMenkuriEye_Init: MATCHED (C, fastchk 0/44 words; ws_check baseline).
- BgMenkuriEye_Destroy: MATCHED (C, fastchk 0/10 words; ws_check baseline).
- BgMenkuriEye_Update: NOT MATCHED, draft under `#if 0` + GLOBAL_ASM. Diff: 5 words at 0x74-0x84, the `ABS((s16)(ac->world.rot.y - shape.rot.y)) > 0x5000` check. ROM does ldrh+ldrh, sub, explicit sxth, add 0x5000; ours folds the sxth into the add (sxtah) with the 0x5000 preloaded. Tried about 10 variants (s16/s32/u16 casts, operand order, s16 local, ac alias, ternary form), none closed it.
- Other notes: framesUntilDisable is 624 in the ROM (416 scaled by 3/2 for the 3DS rate). Init and Update share the literal base 0x512D88 for sNumEyesShot (at +4), so the data is one struct in C (`BgMenkuriEyeData`) and the symbol is an EQU in `data_syms.s`. Header layout: collider 0x1A8, elements 0x1C8, skelAnimModel 0x218, size 0x21C.

## Stage 2 (Sonnet)
- BgMenkuriEye_Update: MATCHED (fastchk 0/83). Fix: `s16 yawDiff;` declared at function top, assigned inside the condition via comma expression `(yawDiff = ac->world.rot.y - actor->shape.rot.y, ABS(yawDiff) > 0x5000)`. Casts/helpers/inline all failed; only the top-level s16 local + comma expr works.
- BgMenkuriEye_Draw: NOT MATCHED, 199/218 words (structural). ROM inlines translate+RotateZYX (sinf/cosf)+scale into MTX34 at sp+0xc with an address-taken Vec3f at sp, SetUnkAC 1 in r5, color consts hoisted (0.784,1.0,0.0) into s0/s3/s17. Draft under `#if 0`. (structural)
