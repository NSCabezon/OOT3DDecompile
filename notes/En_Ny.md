
<!-- merge 2026-10-15 17:10:34 -->
# En_Ny (G36, Haiku + Sonnet passes) STATUS

Matched in C (actor dir z_en_ny.cpp / z_en_ny_move.cpp; GLOBAL_ASM lines removed from functions_*.cpp):
- Haiku: EnNy_Destroy, FUN_003b3ea8, FUN_003cf52c, FUN_003cf564, FUN_00103794, FUN_003af7a0, FUN_003ae2a0, FUN_001dc50c
- Sonnet: EnNy_Init (EQU data_syms.s for init chain / damage table / collider init; models loop needs `SkeletonAnimationModel* m`
  local for FUN_00372d94 and direct `->animType/->animSpeed` writes; mass store order + one `thisx->` toggle),
  FUN_00130dc0 (EnNy_Die; step scale from EQU EnNy_sWaterStep @0x52D258), FUN_00114930 (EnNy_SetupDie, cfg-split head),
  FUN_0016761c (EnNy_UpdateDeath, cfg-split tail of FUN_00167204), FUN_003ce888 (EnNy_SetupMove, 0 words: N64
  `EnNy_SetupAction` static inline helper; lives in z_en_ny_move.cpp so FUN_003cf564 keeps its `bl`).

Splits applied in this ws (both with cfg_split.py, no --tsv/--cfg):
- FUN_00167204 0x0016761c FUN_0016761c   (EnNy_UpdateDeath, 40 B)
- FUN_00114930 0x00114ba4 FUN_00114ba4   (48 B of unrelated tail code, stays asm)

Unmatched (GLOBAL_ASM kept, drafts under #if 0 in z_en_ny.cpp):
- EnNy_Update (277 insns): near, 7 insns off. Everything equal except layout of the two velocity-clamp blocks of the inlined
  gravity helper (ROM: branch 1 jumps forward to the clamp placed after branch 2 and shares branch 1's store block; ours
  does the opposite cross-jump). ~40 variants (structure, ternary, goto, return, static/inline, aliases, greedy toggles).
- EnNy_Draw (154 insns): near, ~21 insns off. ROM scales the matrix with `vmov s1,s0; vldr s2; vmul s1,s2,s1` for the x/y
  columns (z column uses s0 directly); plain/inline/mode/Vec3f-param helpers all give `vldr s1; vmul s1,s1,s0`. Also
  `ldr r5,=sFireOffsets` is scheduled before the 1st Rand call instead of after.
- FUN_00167204 (EnNy_DrawDeathEffect, 1048 B head after split): far (~177 insns off). Identity+translate via
  MTX34_MakeTrans matches, but ROM hoists only `mov sb,#1` (SetUnkAC) while ours hoists zero + 1.0f (extra fp/r7 regs).

Header: z_en_ny.hpp has 3DS offsets (models[15] @0x380 as SkeletonAnimationModel*, unk_320[8] Vec3f @0x320).
Notes: new hand-written .s in actor dir: data_syms.s (EQUs for the actor data chunk); colorFilterTimer is raw +0x11A (draft only).
ws_check.sh En_Ny: baseline only (FUN_00249af8), 0 non-function bytes.
