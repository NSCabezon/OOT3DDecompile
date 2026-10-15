# En_Hs2 (Carpenter's Son, child) — stage 1 (Haiku)

| Function | Status | Notes |
|---|---|---|
| EnHs2_Init | matched (C) | fastchk 0/58 words; ws_check clean |
| EnHs2_Destroy | matched (C) | fastchk 0/12; the `mov r0,#1` is the linker-inlined Collider_DestroyCylinder; ws_check clean |
| EnHs2_Update | matched (C) | fastchk 0/91; ws_check clean |
| EnHs2_Draw | matched (C) | fastchk 0/17; ws_check clean |
| EnHs2_OverrideLimbDraw | matched (C, stage 3) | see Stage 3 notes |
| EnHs2_PostLimbDraw | NOT matched (asm) | ROM has __cxa_guard_acquire on 0x5273DC around function-local static sFocusOffset (0x59AFFC = {300,1000,0}); plain C static does not generate the guard. Needs a C++ guard pattern |
| FUN_003ae5f8 (EnHs2_Idle, action) | NOT matched (asm, in functions_3A0000s.cpp) | Draft under #if 0 in z_en_hs2.cpp: 29/48 words differ. Issues: ldr of FUN_00112564 placement, distance check (ROM: ldrh/sxth then add 0x2150, bhi) |
| FUN_00112564 (EnHs2_Talking, action) | NOT attempted (asm, functions_100000s.cpp) | Not moved; outside actor dir |

Layout (3DS, from ROM): collider 0x1A4, skelAnime 0x1FC, jointTable 0x280, morphTable 0x4BC, headRot 0x6F8, torsoRot 0x6FE, trackingFlags 0x704, actionFunc 0x708, skelAnimModel 0x710, size 0x714.
Data: sCylinderInit at 0x5273E0 (syms.s), PostLimbDraw guard 0x5273DC.

Notes for next stage:
- The Idle action: `Text_GetFaceReaction(play, 9)`, `Actor_ProcessTalkRequest`, Talking pointer loaded after the textId block (ROM `ldr r6` before the process call), `FUN_0036bb28` tail-call.
- FUN_00370734 returns SkelAnime_Update result; include declares it void, so Update uses a static-inline cast wrapper.
- Init passes 11 as limbCount (ROM), not 16 (N64).
- Files touched: only ws/En_Hs2/src/game/actors/En_Hs2/{z_en_hs2.cpp,z_en_hs2.hpp,syms.s}. No include/ edits. Nothing moved out of functions_*.cpp.

ws_check.sh En_Hs2: only baseline FUN_00249af8 differs.

## Stage 2 (Sonnet)
- FUN_00112564 (Talking): matched (C, moved into z_en_hs2.cpp; GLOBAL_ASM removed from functions_100000s.cpp). FUN_00369a48 = Actor_TextboxIsClosing.
- FUN_003ae5f8 (Idle): matched (C, moved; GLOBAL_ASM removed from functions_3A0000s.cpp). Key: `Actor* actor = &self->actor` local + `s16 d = yawTowardsPlayer - shape.rot.y; ABS(d) < 0x2151` (inline `(s16)(...)` cast gives sxtah).
- EnHs2_OverrideLimbDraw: still asm; draft under #if 0 is 21/51 words (only reg alloc r4/r5/r6 + s16/s17 swap); ~30 variants.
- EnHs2_PostLimbDraw: still asm; ctor-based local static gives identical code but guard/object land in own .data/.bss (L6224E) -> needs link change.
- ws_check: baseline only.

## Stage 3 (Opus)
- EnHs2_OverrideLimbDraw: matched (C, 0/51). Key: `Vector3f axis(1,0,0)` (z3Dvec ctor, vldr+vmov stores) + `Vec3f* p = (Vec3f*)&axis` (r6) + headRot.y angle hoisted into its own `f32` local before the 1st FUN_003625f8 call (fixes s1/s2 swap on the first axis store); declare `rotX` before `rotZ`; reassign `axis = Vector3f(0,0,1)` for the 2nd call. No pad needed.
- Removed stale "Not matching yet (PostLimbDraw ...)" comment.
- EnHs2_PostLimbDraw: still asm (needs link change for guarded local static, see note in cpp).
- ws_check: baseline only.
