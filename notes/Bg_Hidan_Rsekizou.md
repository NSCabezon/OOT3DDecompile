
<!-- merge 2026-10-14 23:47:40 -->
# Bg_Hidan_Rsekizou (G17, haiku stage)
- BgHidanRsekizou_Destroy: MATCHED (C, fastchk 0/29; ws_check baseline).
- BgHidanRsekizou_Update: NEAR-MISS 4/58 words (z-component VFP reg swap s2/s3 of modelX/modelZ). ~6 variants. #if 0 draft + GLOBAL_ASM.
- BgHidanRsekizou_Draw: UNMATCHED 92/125 words. Inlined identity MTX34 guard (VFP numbering, known blocker, see mtx34_identity.hpp). #if 0 draft + GLOBAL_ASM.
- FUN_0031de1c (fireball draw): UNMATCHED first draft 93/107. #if 0 draft + GLOBAL_ASM.

## Sonnet stage (G17)
- BgHidanRsekizou_Update: MATCHED via static inline RotZ(h, s, c, z, x) (param order sets VFP numbering).
- FUN_0031de1c: MATCHED (speed=1.0 / PauseContext 0.0; `s2` alias for all self-> except the model index line; play2 on FUN_00371fac call).
- BgHidanRsekizou_Draw: UNMATCHED, identity-MTX34 guard VFP numbering blocker (tag static/matrix). #if 0 draft.
