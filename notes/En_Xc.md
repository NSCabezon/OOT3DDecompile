# En_Xc (Sheik) - cascade stage 2 (Sonnet) status

Workspace: ws/En_Xc (nothing merged into oot3d/; no commit/push).
Check: `scripts/ws_check.sh En_Xc` -> baseline only (FUN_00249af8), 0 non-function bytes.

## Matched in C (stage 1 + stage 2)
Stage 1 (Haiku): EnXc_Draw, caseD_43, caseD_48, caseD_29, caseD_21_0037e91c, caseD_26, caseD_23_0039d078, caseD_45, caseD_4b.

Stage 2 (this pass), all moved from src/functions/functions_*.cpp into src/game/actors/En_Xc/z_en_xc.cpp keeping the
ld-pinned names (GLOBAL_ASM lines deleted from functions_240000s/280000s/2A0000s/310000s/320000s/370000s/380000s/3A0000s):
EnXc_Init (case 9 solved), caseD_3a, caseD_3b, caseD_40, caseD_7_0026c28c, caseD_b_002b21a4, caseD_c, caseD_9_0026c1d8, caseD_20, caseD_24_0039a91c, caseD_25, caseD_22_002b2390, caseD_6_00281bd4, caseD_1f, caseD_36, caseD_d_00320fa0, caseD_38, caseD_3f, caseD_1e, caseD_35, caseD_3_003a24d0, caseD_e_00386ce0, caseD_27_003a26f4, caseD_f_0037e71c, caseD_42, caseD_44, caseD_41, caseD_49, caseD_5_003a25a0, caseD_10_0031a46c, caseD_30, caseD_8_003238ac, caseD_31, caseD_37, caseD_4_0039ce8c.

Total C now: 9 (stage 1) + 35 (stage 2) = 44 functions.

## Left as asm
Near misses (drafts under `#if 0` at the end of z_en_xc.cpp, with notes):
- caseD_0_0026c328: 15 words (identical instruction stream, only `mov r0,play` scheduling + scratch reg).
- caseD_2_002932ec: 21 words (only fp/int scratch register naming).
- caseD_2f: 10 words (gGameInfo ptr/csCtx r7/r8 swapped, r0/r1 temp).
- caseD_12_0026bf1c, caseD_2b, caseD_4d, caseD_33: ROM hoists a callee-saved `mov rN,#0` (zero for drawMode/shadowAlpha) to the
  function entry; the build rematerializes it. ~30 variants tried (not fixed).
- caseD_a_0031c07c: block structure/stream identical; callee-saved assignment differs (ROM self=r6/play=r5/cue=r4).
- caseD_11_003236d4: stream matches; fp callee-saved naming (s16/s17) and r0/r1 temp.
- caseD_1d: stream matches; self/play swapped + literal scratch regs (CHECK_OWNED_EQUIP loads).
- caseD_3c: ROM keeps csCtx (play+0x2298) in a register for the frame read.
- caseD_3d: not matched (needs frame table EQU at 0x0052D2C8; shared-bl SFX chain not reproduced).
- EnXc_Destroy: the dead `mov r0,#1` is armlink --inline of the 2-insn stub `Collider_DestroyCylinder` (returns 1). A plain
  call sequence in C is right; the ROM additionally schedules `mov r2,r1; add r1,r0,#0xc00` before `push {r4,lr}`. 5 variants.
- caseD_1_0026bfc4: not attempted beyond reading (532 B, 3DS-specific skeleton table accesses, long).

cfg-blocked (functions.tsv span contains another function's code; need cfg split by the orchestrator):
EnXc_Update (+EnXc_DrawSquintingEyes tail), caseD_2a (+0x37e95c), caseD_15_0037e9a8 (+0x37ea2c), caseD_16_003870dc (+0x3871a4),
caseD_17_003a3b0c (+0x3a3bdc), caseD_28 (+0x39d074), caseD_2e (+0x391440), caseD_32 (+0x3a28f0, +0x3a28f4), caseD_4a (+0x391558),
caseD_4c (+0x2a4a44, +0x2a4b88), and the stubs inside FUN_0032cc6c (0x32cd64), Math3D_TriLineIntersect (0x319560),
FUN_003264c8 (0x326524).

## Learned (add to CLAUDE.md)
- Prototype `Animation_Change_00375c08(skel, idx, speed, start, end, mode, morph)` in N64 argument ORDER (floats and the mode int
  interleaved): lexical order drives armcc's arg scheduling; the "natural" (skel,idx,mode,f,f,f,f) order produced 2-word diffs.
- `PlayState* play2 = play;` aliases: block-scoped around `Actor_UpdateBgCheckInfo` (puts `mov r0,play` first), and
  `PlayState* play2 = play; CutsceneContext* csCtx = &play2->csCtx; ... play2->GetCutsceneState()` gives the in-place
  `mov r0,rN; add rN,rN,#0x2000; add rN,rN,#0x298` csCtx shape. Cue lookup forms: nested `if (GetCutsceneState()) { cue = ...; if (cue && ...) }`
  (no NULL reg) vs N64 `EnXc_GetCue` (cue=NULL, `ldrne`).
- Wrapper `if (action != K) action = K+1;` after an inlined block that stores `action` is tail-duplicated by armcc unless the
  compare reads a separate local first: `s32 a = self->action; if (a != K) self->action = K + 1;` (predicated ldr/cmp/movne/strne).
- Pointer locals that armcc then folds away still RESERVE registers and change temp choice: `Actor* thisx = &self->actor` (used for
  speedXZ/gravity/xzDistToPlayer), `PosRot* posRot = &actor.world; ActorShape* shape = &actor.shape` (cue pos copy), `f32* timer = &self->timer`.
  Try subsets of these when the diff is only scratch-register naming.
- Faithful N64 inline helpers matter (EnXc_ChangeAnimation with reverseFlag/morph arg, EnXc_Sfx wrapper `(pos, sfxId)` for arg order).
- `s32 frames = play->csCtx.frames;` as a separate statement BEFORE a `(s32)(K / R_UPDATE_RATE + 0.5f)` compare fixes literal-load order.
- 3DS timers: N64 12.0f frames -> `36.0f / R_UPDATE_RATE` (R_UPDATE_RATE = SREG(30)); speeds `kREG(2) * 0.01f + 1.2f`, no extra scaling.
- Init: use gSaveContext fields (`eventChkInf[5/12/4]`, `linkAge`, `cutsceneTrigger`) not raw EQU addresses; N64 block order of
  Actor_Kill branches (float/anim branch before the final kill) fixes armcc's shared-tail placement. Dropped EnXc_sGameFlags/
  sSaveFlags/sSaveNextFlags EQUs from data_syms.s.
- `Item_Give` is the real name for FUN_00376a78; `FUN_00326528` returns s32 (EnXc_SetupNocturneState).

## Stage 3 (Opus, 2026-10-13)
Matched (moved into z_en_xc.cpp, GLOBAL_ASM lines deleted from functions_240000s / functions_2A0000s; EnXc_Destroy
replaces asm/EnXc_Destroy.s in the actor file): EnXc_Destroy, caseD_0_0026c328, caseD_1d. Total C now 47.
ws_check.sh: baseline only (FUN_00249af8), 0 non-function bytes.
- EnXc_Destroy: N64-style helper `EnXc_DestroyCollider(Actor* thisx, PlayState* play)` (self cast inside) -> the
  collider address is computed from the incoming r0 before the push (ROM `mov r2,r1; add r1,r0,#0xc00`).
- caseD_0 / caseD_1d: `PlayState* play2 = play;` declared INSIDE the `params == N` block, passed to Gameplay_InCsMode
  (and to GET_PLAYER for Serenade) -> `mov r0,play` scheduled into the compare block, play in the ROM register.
Still asm (drafts under #if 0, notes there): caseD_2f (10 w), caseD_a_0031c07c (33 w, skelAnime ptr placement + reg
permutation), caseD_12_0026bf1c / caseD_2b / caseD_4d / caseD_33 (zero hoist unsolved, ~45 more variants),
caseD_2_002932ec, caseD_11_003236d4, caseD_3c, caseD_3d, caseD_1_0026bfc4 (not attempted, out of time).
