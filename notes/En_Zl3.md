# En_Zl3 (stage 1, Haiku-only) - status

Actor: `src/game/actors/En_Zl3/z_en_zl3.cpp` (+ `z_en_zl3.hpp`). Build: ws_check.sh shows baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| EnZl3_Destroy | MATCHED | C: SkelAnime_Free2, FaceAnimations::Destroy (via unk_228), Collider_DestroyCylinder. fastchk 0/12 words differ. |
| EnZl3_Update | NOT MATCHED (asm) | Draft under #if 0. Silent action-table dispatch, table at raw 0x005309F0. Tried 4 variants (bounds check before/after table pointer, local pointer, local action). Compiler emits `mov #0x530000` + `ldr [r,#0x9f0]` instead of ROM's literal-pool `ldr r3`. Needs a data symbol for the table, or a different expression. |
| EnZl3_Init | NOT MATCHED (asm) | Only a skeleton draft under #if 0 (unk_19A = 1). Full draft not done (time box). Known parts documented in the comment above the draft: ActorShape_Init, Collider init (cylinder type0x530994), FUN_00353e78 with ZAR_GetCMBByIndex, SkelAnime_SetFaceAnimations(face, skel, 1, 2, 0), params-based switch (Flags_GetSwitch 0x37, Audio_PlaySoundGeneral 0x010004E6). zarIndex computation (play + idx*0x80 + 0x3A6C) not understood. |
| EnZl3_Draw | NOT MATCHED (asm) | Only a skeleton draft under #if 0. Not attempted. |

Layout in z_en_zl3.hpp (3DS): Actor 0x000, SkelAnime 0x1A4, FaceAnimations in 0x228 (size <= 0x1CC, accessed via raw pad), 0xF54 zarIndex, 0xF60 action, 0xF64 drawConfig, 0xF6C f32, collider 0x108C, struct size 0x1140. Only fields used by the matched function are named; others are pads.

Not done: Init, Update, Draw. Notes for a later pass: the N64 reference (`tools/repos/oot/src/overlays/actors/ovl_En_Zl3/z_en_zl3.c`) is 2836 lines and its struct differs a lot from 3DS, so it is only a rough guide.
