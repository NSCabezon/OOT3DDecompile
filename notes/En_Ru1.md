
<!-- merge 2026-10-14 15:56:51 -->
# En_Ru1 cascade stage 1 (batch 1/8) status

- MATCHED: FUN_0039b400 (empty stub), FUN_0039280c, FUN_0039d3f8, FUN_003927ec, EnRu1_Draw (draw table via actor data_syms.s EQU 0x52E640), FUN_001b9324, FUN_003a53d4.
- NOT MATCHED: FUN_0039be64 (6/17 words differ: callback ptr reg ip vs r4, and entry mov ip,r3 before push). Draft under #if 0 in z_en_ru1.cpp, GLOBAL_ASM kept in functions_380000s.cpp.

# En_Ru1 cascade stage 1 (batch 2/8) status

- MATCHED (C in z_en_ru1.cpp, GLOBAL_ASM removed): EnRu1_Destroy (typed header: standingCollider/sittingCollider, skelAnime at 0x1A4, FaceAnimations at 0x9E4), FUN_0039d788 (SapphireRoom_BeingAbducted), FUN_00347f48 (AnimationChange, anim is `s32*` index; callers only FUN_003a3fe0 in En_Ru1, not shared).
- NOT MATCHED, GLOBAL_ASM kept, draft under #if 0:
  - FUN_003264c8 (cfg tail): 0-word C, but ROM has `mov r0,r0` at 0x326524 after the final pop (separate cfg block); C is 92 B and shifts all later functions. Needs cfg split at 0x326524 (orchestrator).
  - FUN_00392198 (= BossRoom_RiseThroughBlueWarp): 1 word off; ROM keeps `ldr r1,[action]` before two identical FUN_00370734 calls, armcc drops it.
  - FUN_003a9e9c (= SapphireRoom_Waiting): 7 words; ROM reloads bigOctoPlatform for the cam store after the drawConfig/action stores, armcc forwards it.
  - FUN_00394288 (= PostLimbDraw, head focus): 25/30 words; ROM pushes {r4,lr} before the limb==10 compare, armcc shrink-wraps to `bxne lr`.
  - caseD_1_00294fb4 (= DrawOpa): 22/33 words; register allocation (skel r6, face r5, eyes/mouth via register offsets) not reproduced.
- Header typed (src/game/actors/En_Ru1/z_en_ru1.hpp): EnRu1BigOctoPlatform, EnRu1BlueWarp, eyes/mouth/blinkTimer, colliders, bigOctoPlatform/blueWarp pointers, FaceAnimations pad at 0x9E4.

# En_Ru1 cascade stage 1 (batch 3/8) status

- MATCHED (C, GLOBAL_ASM removed): EnRu1_Update (sActionFuncs/sfx EQUs in data_syms.s), FUN_003a3f1c (= SapphireRoom_DoneHolding; extra r1 = self->action in the FUN_00370734 call, see below), FUN_0039acb4 (= RiseWithLink).
- MATCHED, separate TU `z_en_ru1_interact.cpp`: FUN_0031a3dc (= TurnUpperBodyForward). Kept out of z_en_ru1.cpp because armcc inlined it into FUN_0039d788 (200 B vs 68 B) when in the same file.
- NOT MATCHED, GLOBAL_ASM kept, draft under #if 0 in z_en_ru1.cpp:
  - FUN_00391cbc (= SetupPositionForFirstEncounter): 29/35 words. ROM keeps csCtx in r6 and `mov r5,#0` before the call, then predicated `ldrne`; armcc emits a branch. ~12 variants.
  - FUN_002a5e68 (= ruto countdown/kill): 28/40 words. Zero-register choice (ROM moves play to r0, zeroes r1). ~6 variants.
  - caseD_2_00283a94 (draw with shadow alpha, no post-limb): 33/46 words. ROM uses reg-offset eyes/mouth loads, armcc folds them into base+imm.
  - FUN_0039b404 (= EndRetrievalCutscene tail): CFG TAIL (functions.tsv merges unrelated code after literal pool at 0x39B4D0; needs cfg split). Draft 28/124 words.
- Infra notes: `FUN_00370734` is called with `self->action` in r1 in several ROM sites (signature unknown); written as a cast to `(s32(*)(SkelAnime*, s32))`. `FUN_00353020` is Animation_Change with a pointer anim (`EnRu1_sRutoChildWait2Anim EQU 0x4D9BAC`, data_syms.s, may be an index, unverified).
- Header additions: EnRu1InteractInfo (headRot/torsoRot at 0xCE4), xzDistToPlayerInBlueWarp (0xBD4), alpha (u32 0xC00), unk_BB0/unk_BB2 (0xBB0/0xBB2).
- ws_check.sh En_Ru1: baseline only (FUN_00249af8).

# En_Ru1 cascade stage 1 (batch 4/8) status

- MATCHED (C, GLOBAL_ASM removed): FUN_00391fd4 (action, anim 0x4D9BB4), FUN_0039ae7c (cutscene/room store, infTable[20] |= 0x10), FUN_0031cddc (ripple timer, moved to z_en_ru1_interact.cpp: armcc inlined it into FUN_00392200 when in z_en_ru1.cpp).
- NOT MATCHED, GLOBAL_ASM kept, draft under #if 0 in z_en_ru1.cpp:
  - FUN_0039d23c (8/57 words): play/cue register swap (ROM play r5, cue r6). ~8 variants.
  - FUN_0039d6ac (8/55 words): same play/cue swap as FUN_0039d23c.
  - FUN_00392200 (28/52 words): same play/cue swap plus animFinished reg (ROM r7, ours r8); SIZE 192 vs 208.
  - FUN_003a67e0 (14/54 words): play/pos reg swap (ROM play r5, pos r6); pos/alias/param-name variants tried.
  - FUN_0039d320 (6/54 words): EnRu1_SpawnBlueWarp-like (spawn ACTOR_DOOR_WARP1, params 5); float const loaded into s17 in ROM, ours s16.
- Header additions: unk_1CC (0x1CC void*), unk_219 (u8), unk_BC4 (f32 spawn/blue-warp timer), unk_BC8 (f32 ripple timer), unk_BDE (s8 room num).
- data_syms.s: EnRu1_sAnim4D9BB4/4D9BB8/4D9BC4/4D9BCC EQUs (anim pointers, addresses only).
- ws_check.sh En_Ru1 after batch 4: baseline only (FUN_00249af8).

# En_Ru1 cascade stage 1 (batch 5/8) status

- MATCHED (C, GLOBAL_ASM removed): FUN_003a6b64 (= EnRu1_Sitting_SinkingInWater, StopMoving/CheckHitBottomUnderwater/ResetBgCheckFlags inlined), FUN_0039d7cc (state fn, tail-calls FUN_00319b54; `Actor* thisx` alias on the BgCheck block).
- NOT MATCHED, GLOBAL_ASM kept, draft under #if 0 in z_en_ru1.cpp:
  - FUN_003920ac (= EnRu1_CheckStartFirstEncounter): 47/59 words; range test compiles as int compare (ROM vcmpe + bhi), float order swapped.
  - FUN_00319f20 (= func_80AED624): 13/61 words; 0x1AE literal derived from the 0x2E action reg (`addeq r0,r2,#0x180`).
  - FUN_00295038 (= EnRu1_ThroneRoom_Talk): 4/64 words, all in the closing-branch flag clear + action store (pre-indexed merge).
  - FUN_0039ad64 (= EnRu1_Sitting_DisappearingInWater): 6/70 words, kill branch register numbering (0x1AE from 0x2E).
  - FUN_003a28f8 (= EnRu1_BossRoom_WhatTookYouSoLong, AdvanceAngryAnimation inlined): 41/77 words, ROM reloads rutoWarpState; 12 bytes bigger.
  - FUN_003922d0 (3DS-only rise state, BgCheck + sound + AnimationContext_SetMoveActor tail): 54/88 words, 20 bytes short.
- Header additions: EnRu1 zarInfo (0x9E0), roomNum1/roomNum2 (0xBDC/0xBDD), sinkTimer (0xBFC), isSittingOCActive (0xCBC); EnRu1InteractInfo yOffset/trackPos (size 0x24, EnRu1 pad moved to 0xD08); EnRu1PlayerSub speedXZ (0x221C).
- data_syms.s: EnRu1_sAnim4D9BE8 / 4D9BF8 / 4D9BFC EQUs.
- ws_check.sh En_Ru1 after batch 5: baseline only (FUN_00249af8).

# En_Ru1 cascade stage 1 (batch 6/7 + 8 partial) status

- MATCHED (C in z_en_ru1.cpp, GLOBAL_ASM removed): FUN_003a2c98 (= EnRu1_SpeakableJabu_TakingSeat). infTable write is `(u16*)((u8*)&gSaveContext + 0xF00)[28]` = gSaveContext.infTable[20] |= 8 (INFTABLE_RUTO_LET_LINK_CARRY 0x143); the plain `gSaveContext.infTable[20]` form gives a different literal (ws_check showed the diff). Debt: raw base-offset cast.
- NOT MATCHED, GLOBAL_ASM kept, draft under #if 0 in z_en_ru1.cpp:
  - FUN_003a2dfc (= EnRu1_SapphireRoom_ThrownOntoPlatform): 60/98 words; ROM pushes sb/sl (csCtx + spare reg), predicated cue load, 392 B vs 308 B.
  - FUN_003a3fe0 (= EnRu1_SapphireRoom_ReadyToGoHome): 48/90 words; play in r6 (ROM r5), zero in r5 (ROM r6). FUN_00347f48 and FUN_0031a3dc are real calls: must not share a TU with them (armcc inlines).
  - FUN_00295138 (= EnRu1_ThroneRoom_Idle): 31/89 words; textId store reg (ROM keeps return in r0, stores via r1 = self+0x100), standing-collider base reg.
  - FUN_003a5604 (= EnRu1_BossRoom_LinkWalksToPointInBlueWarp): 63/89 words; player/linkPos reg plan and float copy order.
  - FUN_003a3d88 (= EnRu1_SpeakableJabu_Talking): 54/101 words; play in r6 (ROM r5), interact copy regs.
- NOT ATTEMPTED (budget/context): EnRu1_Init (88; switch with inline case bodies + ldrlo jump table, calls ZAR_GetCMBByIndex/FUN_00353e78/SkelAnime_SetFaceAnimations), FUN_003a3be0 (93; = EnRu1_Meeting_FallingDownHole, AccelerateDownHole/RespondToFalling/PlayStepSfx/CheckStartFalling inlined), FUN_0039b244 (100), FUN_00387850 (102), FUN_00387e08 (102).
- Header: unk_BE0 (f32, 0x0BE0, cleared by func_80AED6DC in ROM).
- data_syms.s: EQUs + EXPORTs added for EnRu1_sAnim4D9BD4, 4D9BD8, 4D9BF4, 4D9BBC.
- ws_check.sh En_Ru1 after batch 6/7 pass: baseline only (FUN_00249af8).

# En_Ru1 cascade stage 2 (Sonnet, near-miss pass)

- MATCHED (C enabled, GLOBAL_ASM removed): FUN_00392198 (FUN_00370734 takes (skel, action)), FUN_00295038 (`u32 flags` writeback), FUN_0039be64 (callback typed Actor*, in a local), FUN_0039d320 (`Vec3f* p2 = pos` used for y only), FUN_003a9e9c (helper arg `(EnRu1*)thisx` forces the reload), FUN_0039d23c + FUN_0039d6ac (cue helper: csCtx, cue, then `play2 = play`), FUN_00319f20 (`!(flag & 1)` arm first, dead `s2` on action != 0x21, timer before alpha), FUN_003a67e0 (constants were wrong: BC4 = 0.0f, offset 30.0f).
- NOT MATCHED: FUN_0039ad64 (6 words, kill branch: ROM mov r1,#0x2e; add r2,r1,#0x180 before the action store; ~100 variants incl. shared StartKill helper). Draft under #if 0. FUN_00392200 draft now 23/52 words (was 28), still under #if 0.
