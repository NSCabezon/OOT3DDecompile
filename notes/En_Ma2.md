
<!-- merge 2026-10-14 14:26:23 -->
# En_Ma2 STATUS (cascade stage 1, Haiku, batch 1/1)

Matched in C (ws_check: only FUN_00249af8 differs):
- EnMa2_Destroy (11 insns)
- FUN_00233648 (OverrideLimbDraw, limbs 8/7 -> interactInfo.torsoRot/headRot)
- FUN_002172bc (PostLimbDraw, limb 8, N64-order MultVec3f wrapper)
- FUN_001c53ec (WaitForOcarina)
- EnMa2_Draw (adds the animationType==2 FUN_0037266c/FUN_0036932c branch before the face calls)
- EnMa2_Update (interact-info/eye/singing/tracking helpers inlined in N64 order)

Not matched:
- FUN_00195dac (UpdateTalkState): body (0x80 B incl. literal pool) matches 0/32 words in fastchk, but the tsv span (268 B) also covers the unlabeled GetTextId (EnMa2_GetTextId @0x195E2C, 140 B). Needs cfg split (orchestrator). Draft under #if 0; still GLOBAL_ASM.

Header (z_en_ma2.hpp) now types: skelAnime 0x1A4, face 0x228 (cast), actionFunc 0x3F4, collider 0x3F8, interactInfo 0x450 (talkState/torsoRot/headRot/yOffset/trackPos), timer 0x478, singingDisabled 0x47A, blinkTimer 0x47C, eyeIndex 0x47E, mouthIndex 0x480.


Stage 2 (Sonnet): matched FUN_001c5338 (static inline EnMa2_Msg(play) accessor called at every use gives self=r4/msg=r5) and EnMa2_Init (inlined GetSpawnIndex/ChangeAnim, p2 alias on FUN_00353e78, `((EnMa2*)thisx)->actionFunc` in the ranch case, tables via actor-dir data_syms.s EQUs). Only FUN_00195dac left (needs cfg split).
