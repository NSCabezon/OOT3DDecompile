
<!-- merge 2026-10-14 11:33:30 -->
# En_Nb status (cascade stage 1, Haiku, batch 1/4)

## Matched (moved into src/game/actors/En_Nb/z_en_nb.cpp, names kept, GLOBAL_ASM removed from functions_*.cpp)
- EnNb_Destroy: C (Collider_DestroyCylinder inlined by armlink, SkelAnime_Free2, FaceAnimations::Destroy)
- EnNb_Update: C, table at 0x0052CF10 via local `ActorFunc* table` (action < 0x1F, tail call)
- EnNb_Draw: C, table at 0x0052CF8C via local `ActorFunc* table` (drawMode < 5, tail call)
- FUN_00297e90: `return 0` stub (limb draw callback used by caseD_4_002930a8)
- FUN_00271e18: C (callee of caseD_1_00281938; ip = self+0xD7C, FUN_0034e01c dispatch on id 9 / 0xA)
- FUN_0033526c: C, `__attribute__((noinline))` on the prototype (eye blink timer, Rand_S16Offset(60,60)); callers are En_Nb's own action table entries, so NOT shared
- caseD_2_002121a4 (action 2 = ComeUp): C, scoped `f32* yOffset` locals reproduce ROM register order

## Not matched
- caseD_e_003a9088 (action 14 = func_80AB2C18): asm kept (GLOBAL_ASM in z_en_nb.cpp), C draft under `#if 0`.
  Diff: 15 of 26 words. ROM keeps self in r5 and play in r4 (`mov r5,r0; mov r4,r1`); every variant built self in r4 / play in r5.
  Tried: (self,play) and (thisx,state) signatures, both local declaration orders, state passed directly, N64-style static inline helpers (func_80AB2688 / func_80AB1284), scoped play local, dead `Actor* actor` alias, thisx casts inline.
  Field note: flags byte at 0x1F6 is skelAnime.unk_50[2] (the SkelAnime struct has no movementFlags in the repo header).

## Batch 2/4 (cascade stage 1, Haiku)
Matched (moved into z_en_nb.cpp, GLOBAL_ASM removed):
- EnNb_SetCurrentAnim: C. Needs `Actor* thisx` signature + `EnNb* self = (EnNb*)thisx` and a local `SkelAnime* skelAnime`; the `EnNb*` signature put self in r4 (7 words off).
- caseD_a_00386c40 (action 10 = N64 func_80AB23A8): C, `(EnNb*, GameState*)` + `PlayState* play` and `CutsceneContext* csCtx = &play->csCtx` (a `frames` local folded the offset into a literal). Cry SFX when `csCtx->frames == (s32)(9.0f / SREG(30) + 0.5f)`, then tail call FUN_0031cfb8.

Not matched (drafts under #if 0 in z_en_nb.cpp, asm kept in functions_*.cpp):
- FUN_00256384 (PostLimbDraw): 17 words. Frame shape: ROM does `mov r0,r1` / `push` / `cmp` / `sub sp,0x18`, while ours tail-returns before the push. Tried struct literal at top, explicit assigns, zero local, limb copy.
- caseD_1_00281938 (draw 1, DrawDefault): 3 words. Only the FaceAnimations call: ROM sets `this` in r0 before eyeIdx/0 (ours sets it last). Tried eyeIdx s16/s32, face local, `&self->faceAnimations`, static inline helper.
- caseD_4_002930a8 (draw 4): 3 words, same FaceAnimations argument order.
- caseD_3_00281a5c (draw 3): 8 words. Face and skel pointer scheduling (ROM interleaves the +0x800 / +0x1a4 adds). Both declaration orders tried.
- caseD_1_0024cdf4 (action 1, SetupChamberWarp + SpawnBlueWarp inline): 7 words. ROM keeps csCtx in r6 across GetCutsceneState and loads `npcActions[1]` predicated from it; ours folds to play+literal. Tried csCtx inside guard (31 words, worse).
- caseD_7_002b1a90 (action 7 = SetupHide body): 19 words. ROM hoists 0 into r1 before the cmpne and uses it for alpha/shadowAlpha and the NULL pos; ours materialises it later. Tried zero local and NULL pos local (20 words).
- Shared: none. FUN_00256384 is only referenced by caseD_1_00281938 (draw table idx 1 -> caseD_1).

Check: scripts/ws_check.sh En_Nb = baseline only (FUN_00249af8).

## Batch 3/4 (cascade stage 1, Haiku)
Matched (C in z_en_nb.cpp, GLOBAL_ASM removed from functions_3A0000s.cpp):
- caseD_11_003aa4c4 (LookLeft-like: eyes, skel update, anim 5 loop on finish, move + bg check, FUN_00318010). Needed: speed local declared AFTER the SkelUpdate call, play2 scoped around Actor_UpdateBgCheckInfo and around SetMoveActor/flags, skel local scoped inside the `if`. Skel update via `((EnNbSkelUpdateFunc)FUN_003731e0)` (typedef, as En_Horse does; header declares it void).

Not matched (drafts under #if 0 in z_en_nb.cpp, GLOBAL_ASM kept in functions_*.cpp; caseD_14 GLOBAL_ASM now in z_en_nb.cpp):
- caseD_14_00293124 (credits cue 15/16): 52 words. ROM keeps self in r5 and play in sb (7 callee-saved regs); every variant had 5. Tried ternary/NULL cue, csCtx local, Actor* signature, N64 GetCue/SetStartPos static inlines, self aliases.
- caseD_2_0026b1dc (draw 2, transparency): 3 words. Only the FaceAnimations call: ROM puts this in r0 before eyeIdx (ours sets r2 first). Tried s16/s32 eyeIdx, face local, inline face helper.
- caseD_0_0024cec0 (SetupChamberCsImpl): 38 words. Shape right (GetObjectStatus(actor.objBankIndex)->zarInfo, FUN_0037573c, Item_Give 0x69). Remaining: ROM uses one gSaveContext base literal in r7; ours splits literals (ldrb [r0,#0xa3]). Tried SaveContext* local (worse), reordered checks (worse), play2 in guard.
- caseD_10_003aa694 (Kneel-like, anim 7, drawMode 4, bound SFX via Audio_PlaySoundGeneral): 7 words. Only the `unk_50[0x20] == 2` mode check schedule differs (ROM ldrb r1 then add r0 before cmp).
- caseD_b_003a22b4 (cry SFX frames 9 and 1260 over SREG(30)): 9 words. ROM keeps play in r6 and gGameInfo in r7; vdiv operand order differs (K in s1 in ours).
- caseD_c_00386b28 (MovingInPortal: anim 19, Environment_LerpWeightAccelDecel + pos lerp, FUN_0031cfb8 tail): 12 words. ROM computes csCtx (r8) early; ours folds to play+offset.
- caseD_15_002a4170 (Fade: alpha ramp with kREG(21), action 0x16): 46 words. ROM literal order / &self->alpha pointer scheduling differs; ROM has alphaTimer address computed after the Animation/eye calls.

## Layout (3DS)
- Actor 0x1A4; skelAnime at 0x1A4 (0x84); FaceAnimations at 0xB18; eyeIdx s16 0xCE4; blinkTimer s16 0xCE6; action 0xCE8; drawMode 0xCEC; collider at 0xD04; unk_D5C; unk_D7C (ip base); total 0xDA8.
- Action table (0x52CF10): idx 0..30; idx 2 = caseD_2, idx 14 = caseD_e. Draw table (0x52CF8C): idx 1 = caseD_1 (DrawDefault), idx 4 = caseD_4.

## Batch 4/4 (cascade stage 1, Haiku, last batch)
Matched (C in z_en_nb.cpp, GLOBAL_ASM removed from functions_3A0000s.cpp):
- caseD_f_003a51b8 (Kneel-like, anim 8, drawMode 3, bound SFX on OnFrame 18/25 in ONCE mode, move + bg check, FUN_00318010 tail): 0/82 words. Needed a `SkelAnime* skel = &self->skelAnime;` declared AFTER the mode read (ROM `add r6` between ldrb and cmp).

Not matched (asm kept, GLOBAL_ASM still in functions_*.cpp, draft under #if 0 in z_en_nb.cpp):
- caseD_12_003a36c0 (frame-9 cry SFX pair, OnFrame SFX, move + bg check, one-shot Demo_6K spawn gated by 0xCF8): 2 words off. Everything matches except the spawn-flag store: ROM `mov r1,#1; str r1,[r4,#0xcf8]` after the Actor_Spawn call, ours `mov r0,#1`. Tried plain store, a `s32* spawned` pointer (worse: r6 reused), a dummy `+ (s32)pos->x*0` (rejected, not real code). Header: unk_CF8 is now `s32` in z_en_nb.hpp (same size).
- FUN_0031cfb8 (EnNb_CheckKidnapCsMode, cue 1/7/8/9 on channel 1): 88 words off. ROM hoists sb=0 and r8=1 before the cue NULL check, keeps csCtx in sl and play copy in r7, and loads cue->action / self->cueId unconditionally after a predicated `ldrne/moveq` cue select; armcc if-converts the `ldrhne` / `cmpne` pair in every form tried (ternary, early return, split compares, N64-style locals). Case bodies: ROM case 1 keeps the shape pointer in r8 (`add r8,r4,#0xbc`, shadowAlpha at +0x14); case 7/8 constants are speed 1.0f (s18), start 0.0f (s17), morph -8.0f (s16) with a 3-way pool share. Draft in #if 0 (`EnNb_SetupCaptureState` + `FUN_0031cfb8`).

## Check
- scripts/ws_check.sh En_Nb: only FUN_00249af8 differs (baseline), 2026-10-14 after batch 4.

## Part B (cascade stage 2, Sonnet) - none matched, all drafts kept under #if 0
- cfg tails (unlabeled code after the literal pool; do not count on merging): caseD_0_0024cec0 (356 B in tsv vs 176 B body), caseD_15_002a4170 (556 vs 296), EnNb_Init (960 B, jump table + tail code; not attempted). Clean: caseD_14_00293124, FUN_0031cfb8, FUN_00318010, caseD_1c_002a439c.
- caseD_14_00293124: N64 GetCue/SetupCreditsFadeIn/HeadTurn as static inlines + `EnNb* s2/s3 = self` aliases give ROM's 8-reg push list and the two self copies; still ROM-specific: r4=0 hoisted for the cue select (predicated moveq), self=r5, play=sb, csCtx=r8, cueId=r6 (ours r6/r8/r7/r5). ~50 words, all reg shifts. Left GLOBAL_ASM.
- caseD_15_002a4170 (cfg tail): kREG is (17) not (21). Pointer locals `s32* alphaPtr=&self->alpha; u8* shadowAlpha=&self->actor.shape.shadowAlpha; f32* alphaTimer=&self->alphaTimer;` plus a scoped second `alphaTimer2` pointer for the final compare => 16 words, only r0/r2 swap (timer ptr vs alpha ptr). Decl order grid (6 perms) doesn't change it.
- FUN_0031cfb8: 88 -> structurally ~93%: N64 inline helpers (GetCue, SetStartPosRotFromCue, Setup*), `switch`, `PlayState* play2 = play` used only for the case-1 inline, `EnNb* s2 = self` alias for the final cueId store, `SkelAnime* skelAnime` local in cases 7/8. Remaining: armcc if-converts `ldrh/ldr/cmp` after the cue NULL test (ROM branches with beq), ROM reg order play2=r7, csCtx=sl, 0=sb, 1=r8 vs ours reversed; case 1 needs `ActorShape* shape = &self->actor.shape; shape->shadowAlpha = 0` (ROM `add r8,r4,#0xbc; strb [r8,#0x14]`) - applied only in FUN_00318010 draft.
- FUN_00318010 (EnNb_CheckConfrontationCsMode, N64 lines ~850-920): full draft with 7 Setup helpers (692 of 700 B). `ActorShape* shape = &self->actor.shape` in each helper reproduces ROM's `add rX,r4,#0xbc` + `strb [rX,#0x14]` (__typeof__ is not available in armcc). Remaining: same cue/cueId if-conversion, float hoist order (ROM 0.0=s16, 1.0=s18, lastFrame s17), ROM keeps `&skelAnime` in a stack slot in case 10, `3` not hoisted.
- caseD_1c_002a439c (action 28 = EnNb_FollowPath: timer++/lerp, BgCheck, collider, SmoothStepToS x5, skel update, eyes, walk-anim check): draft ~84% structural. Needs z_en_nb.hpp typed fields (added: initialPos 0xD60, finalPos 0xD6C, pathYaw 0xD78, movementTimer 0xD7A, headRot 0xD84, torsoRot 0xD8A; unk_D7C now 8 bytes, same total size). Frame scaling = `n>0 ? (s32)(0.5f+(n*3.0f)*0.5f) : (s32)((n*3.0f)*0.5f-0.5f)` on `(u16)(kREG(17)+25)` as a MACRO (expression repeated; inline fn with u16 param folds the zero test differently). Remaining: ROM saves only r4-sl (no fp), keeps pointer computations inside the if, 2 hoisted float consts (s16/s17) not 3.
- ws_check.sh En_Nb: baseline only (FUN_00249af8). ws/En_Nb/tmp deleted.

## Stage 3 (Opus, 2026-10-14)
Matched (C in z_en_nb.cpp, GLOBAL_ASM removed):
- caseD_e_003a9088: `SkelAnime* skelAnime = &self->skelAnime;` local inside the scoped-play2 block for the flag store (ROM `add r2` before `orr`, mov r0,play hoisted).
- caseD_c_00386b28 (GLOBAL_ASM removed from functions_380000s.cpp): N64 GetCue (csCtx local) + SetPosInPortal static inlines, a second `csCtx` local in SetPosInPortal for `frames`, `pos` declared inside the `if (cue != NULL)` before lerp/startPos/endPos, `{ PlayState* play2 = play; EnNb_SetPosInPortalC(self, play2); }`.
Not matched (drafts improved, #if 0):
- FUN_0031cfb8: 88 -> 27 words, shape exact; `EnNb* s2 = self;` INSIDE `if (cue != NULL)` stops armcc if-converting the cueId test. Only callee-saved numbering left.
- FUN_00318010: 152 -> 105 words, size now 700 = ROM. Missing ROM's self copy (r6), float regs, 3 hoisted.
- caseD_14_00293124: ~50 -> 29 words.
- caseD_1c_002a439c: unchanged (188/232, 920 vs 928 B); moving pointer locals into the `if` made it worse.
Check: ws_check.sh En_Nb = baseline only (FUN_00249af8).
