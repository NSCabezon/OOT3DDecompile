
<!-- merge 2026-10-15 10:59:14 -->
# En_Ba (G28 haiku stage)

Matched (C, fastchk 0 words; ws_check baseline only):
- FUN_0036651c (functions_360000s.cpp -> actor .cpp, GLOBAL_ASM removed)
- FUN_003664d4 (functions_360000s.cpp -> actor .cpp, GLOBAL_ASM removed)
- EnBa_Destroy (actor .cpp)
- FUN_00106ecc (functions_100000s.cpp -> actor .cpp, GLOBAL_ASM removed)

Not matched (left as asm, draft under #if 0):
- FUN_003d51ec (31 insns, 3 words): ROM uses `sxth r2,r1` into a fresh reg for the s16 timer; every timer form tried (~15 variants: s16/u16/s32 temp, sub-struct alias, single-site alias, play2) keeps sxth in place. Still GLOBAL_ASM in functions_3C0000s.cpp.
- EnBa_Draw (40 insns, ~30 words): PauseContext if/else stores match, but the ROM shares one epilogue between the `unk_C48 != 0` early exit and the small-branch path (ours duplicates it, +8 bytes). Tried ~10 layouts (guard nesting, reversed branch, early returns, pointer locals, MTX34 scope) without fixing.
- FUN_003159f8 (51 insns, 29 words, size +12 bytes): Math_SmoothStepToF chain; ROM keeps s0 zero return and reads src into s5/s4/s7 first; header Math_Vec3f_DistXYZ gives same size mismatch. Still GLOBAL_ASM in functions_310000s.cpp.

Notes: header z_en_ba.hpp now types the 3DS layout (EnBaSub at 0xB00, FaceAnimations 0x7DC, model at 0xC3C, state at 0x9A8 = N64 unk_14C + 0x85C shift). No cfg splits.

## G28 sonnet stage
Matched (moved into actor .cpp, GLOBAL_ASM removed): EnBa_Draw (single if-tree, `p = self->unk_7D8` re-read in each pause arm, arms swapped: `PauseContext_GetState() != 0` first), FUN_003159f8 (`f32 ret = 0.0f` first local, `ret = A; ret += B; ret += C`).
Header: typed 0x9B0..0xB74 (upperParams, unk_158/unk_200 Vec3f[14], unk_2A8 Vec3s[14]), sub moved to 0xB74 (s16 unk_7A), camId/unk_C44, unk_7D8 = SkeletonAnimationModel_unk_0C*, unk_B7C u8[]. data_syms.s: EnBa_sBaseRot 0x520A34, sJntSphInit 0x520A3C, sInitChain 0x520A4C, sFaceTable 0x4D9260 (EQU).
Drafts under #if 0 in z_en_ba.cpp: FUN_003d51ec 3w (needs `(EnBa*, PlayState*)` + s16 field), EnBa_Init 32w, EnBa_Update 145-157w (armcc folds the play2 copies), FUN_00232dac 54w. Skipped (identity+translate integer-store MTX34 = `matrix`): FUN_00198c20, FUN_003c6320, FUN_00108948.
