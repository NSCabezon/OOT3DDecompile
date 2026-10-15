
<!-- merge 2026-10-14 18:17:42 -->
# En_Ani (sonnet stage, G4) — STATUS

ws_check.sh: baseline only (FUN_00249af8).

## Matched (C, byte-identical under fastchk + ws_check)
- EnAni_OverrideLimbDraw, FUN_0015fb60, FUN_001a3850, FUN_00117324, FUN_00202634 (haiku)
- EnAni_Init (sInitChain/sCylinderInit EQUs in actor data_syms.s; N64 SetupAction static inline helper)
- EnAni_Draw (dead `f32 dummy = 0.0f;` local after the face pointer fixes the eyeIndex literal/arg order)
- EnAni_Update (cases inlined; static inline EnAni_WaitAnim for cases 1 and 3; matched first try)
- FUN_0015d56c = ADULT talk action (N64 func_809B07F8), FUN_001a1438 = CHILD talk action (N64 func_809B064C, mask reaction = Text_GetFaceReaction(play, 10)); Actor_ProcessTalkRequest = Actor_TalkOfferAccepted; FUN_0036bb28(actor, play, 100.0f) = Actor_OfferTalk (tail call, SetText inline)

## Not matched
- EnAni_Destroy: falls through into FUN_00189844 (cfg merge). Draft under #if 0.
- EnAni_PostLimbDraw: guarded function-local static sMultVec (static, LOADER_RECIPE).

## Layout notes
limbRot Vec3s 0x898 (N64 unk_29C), unk_89E Vec3s (N64 unk_2A2), unk_8A4 u16 flags (N64 unk_2A8), unk_8A6 u16 cutscene state (N64 unk_2AA), eyeIndex 0x8A8, blinkTimer 0x8AA, actionFunc 0x8AC, unk_8B0 s16 sfx timer.
