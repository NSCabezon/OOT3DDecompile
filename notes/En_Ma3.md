
<!-- merge 2026-10-13 18:06:05 -->
# En_Ma3 — STATUS (solo barrido, Haiku)
- Matched (C): EnMa3_Destroy (0/11 words), EnMa3_OverrideLimbDraw (0/13 words; FUN_0034e01c limb helper, 0x458/0x45E offsets).
- Near: EnMa3_PostDrawLimb 2/18 words: ROM emits `addeq r0,r3,#0x3c` BEFORE `moveq r2,sp`; C emits the reverse. Draft under #if 0.
- Far: EnMa3_Init 98/127 words (3DS object-bank/ZAR path, SetFaceAnimations, inlined ChangeAnim with raw table 0x52C308, size 472 vs 508). Draft under #if 0.
- Not attempted (budget): EnMa3_Update (96 insns), EnMa3_Draw (49), FUN_003c6240 (53), FUN_001960e8 (58); FUN_00195eb8 (126 insns, big, sonnet-direct).
- Header: EnMa3 struct now has collider 0x3F8 (0x58), actionFunc 0x3F4, unk_450, unk_47A (size 0x484 verified vs ROM sizeof).
- Raw data refs: sCylinderInit 0x52C294, sColChkInfoInit 0x52C2CC, sAnimationInfo 0x52C308 (debt: data symbols).
- ws_check.sh: only FUN_00249af8 differs; non-function bytes 0.
