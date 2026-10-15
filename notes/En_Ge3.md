
<!-- merge 2026-10-15 15:49:13 -->
# En_Ge3 — G32 Haiku pass (2026-10-15)

| Function | Status | Notes |
|---|---|---|
| EnGe3_OverrideLimbDraw (8) | MATCHED | head limb -> FUN_0034df48(mtx, &headRot). |
| EnGe3_Destroy (15) | MATCHED | Collider_DestroyCylinder, FUN_003508b8(model), SkelAnime_Free2, FaceAnimations::Destroy. |
| EnGe3_PostLimbDraw (16) | MATCHED | Needs static inline N64-order wrapper EnGe3_MultVec3f (predicated bleq otherwise). |
| EnGe3_WaitTillCardGiven (18) | MATCHED | GiveItem tail (0x3A, 10000, 50). |
| EnGe3_GiveCard (27) | MATCHED | |
| EnGe3_Draw (33) | MATCHED | GraphicsContext_UnknownStub(state->gfxCtx) first; FaceAnimations* alias for eyeIndex arg order. |
| EnGe3_WaitLookAtPlayer (61) | MATCHED | LookAtPlayer static inline; angleDiff = (s16)(...) local (not ABS on field directly). |
| EnGe3_Wait (62) | MATCHED | angleDiff computed AFTER the textbox check; world.rot.y store via `s16* p = &...` pointer. |
| EnGe3_ForceTalk (89) | MATCHED | |
| EnGe3_Init (84) | NOT MATCHED, draft under #if 0 (Sonnet pass: 13/97 words) | Fixes found: SetFaceAnimations is (face, skel, 0, -1, -1); N64 static EnGe3_ChangeAction(self, i) helper (incl. the dead `unk_30C &= ~2`) fixes pool order. Remaining 13 words: ROM computes the mode byte as `sub r0,r6,#8; ldrb r2,[r0]` from the sAnimations literal (sAnimationModes/sActionFuncs/sAnimations are adjacent real statics in the original; EQUs fold to `ldrb [r5,#-8]` and swap the r5/r6 zero/pointer regs). Needs real adjacent statics (zero-init modes byte would land in .bss) - ~25 variants tried. Old note: Remaining: SkelAnime_SetFaceAnimations stack arg (-1) scheduled early (ROM: late str r3,[sp]); zero kept in r6 vs ROM r5 (play reg reuse); anims pointer / mode via ((u8*)anims)[-8] matched sizes. Data via data_syms.s EQUs (0x524D08..14). |
| EnGe3_Update (52) | MATCHED (Sonnet) | N64 shape: static EnGe3_UpdateCollision + EnGe3_MoveAndBlink helpers; in UpdateCollision a dead alias `EnGe3* s2 = self;` used for the flag test AND the |= store but NOT for the FUN_00370734 arg (found by grid over test/arg/store accessor) stops the if-conversion. |
| EnGe3_UpdateWhenNotTalking (75) | MATCHED (Sonnet) | Same helpers; `self->actionFunc = EnGe3_Wait; thisx->update = EnGe3_Update;` and `thisx->textId = 0x6005;` (thisx-> on those two stores fixes pool order / regs). |

Layout (3DS, from ROM): collider 0x1A4, skelAnime 0x1FC (0x84), jointTable 0x280 (19), morphTable 0x65C (19), eyeIndex 0xA38, blinkTimer 0xA3A, headRot 0xA3C, unk_306 0xA42, unk_30C 0xA48, actionFunc 0xA4C, model 0xA50, FaceAnimations 0xA54. sizeof(EnGe3) == 0xC20 verified.
Data: En_Ge3 tables at 0x524D08 (sAnimationModes u8), 0x524D0C (sActionFuncs), 0x524D10 (sAnimations, s32 indices), 0x524D14 (sCylinderInit) via actor-dir data_syms.s EQUs (include kept).

ws_check En_Ge3: baseline only (FUN_00249af8), 0 non-function bytes.
