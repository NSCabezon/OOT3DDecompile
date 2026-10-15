
<!-- merge 2026-10-14 11:05:22 -->
# En_Heishi2 — cascade stage 1 (Haiku), batch 1/5

## Batch functions
| Function | Status | Notes |
|---|---|---|
| FUN_0013f448 | MATCHED | empty stub (`bx lr`), N64 EnHeishi2_DoNothing1; moved to z_en_heishi2.cpp |
| FUN_00150888 | MATCHED | empty stub (`bx lr`), N64 EnHeishi_DoNothing2; moved to z_en_heishi2.cpp |
| FUN_002110e4 | MATCHED | `s32(s32 unused, s32 which, MTX34*, EnHeishi2*)`; state check at self+0x94A, FUN_0034e01c on self+0x8B8 (which==8) / self+0x8AC (which==0xF) |
| FUN_0024ba60 | MATCHED | copies 0x30-byte block to self+0xA04 when which==0xF |
| FUN_00269aa0 | MATCHED | `(Actor* thisx)`; SetUnkAC(1) on skelAnimModel, FUN_003721e0(&modelMtx), tail FUN_00372170(0). Signature via Actor* thisx was needed (EnHeishi2* param gave wrong reg for the 1-store) |
| FUN_0025a17c | MATCHED | action setter template (Animation_Change idx 0, -10 morph) -> FUN_001cbb1c |
| FUN_002742e8 | MATCHED | same template -> FUN_0038a670 |
| FUN_00298ef4 | MATCHED | same template -> FUN_0038a918 |

Note on FUN_0025a17c / FUN_002742e8 / FUN_00298ef4: identical templates (same as En_Heishi4 FUN_00180b24). They are referenced from asm of other unmatched FUN_ functions (FUN_00259ef4, FUN_0019bec4, FUN_002744b8, FUN_00238bc4, FUN_00238abc, FUN_00177c24, FUN_001e883c, FUN_001cbb1c). No src/ references; moved by name (linker-pinned).

## Header
`z_en_heishi2.hpp`: placeholder `unk_1A4[0x890]` replaced by typed fields (skelAnime 0x1A4, actionFunc 0x8A8, unk_94A, skelAnimModel 0x9FC, unk_A04 block). Size unchanged 0xA34.

## Checks
- fastchk: all 8 `0 words differ`.
- ws_check.sh En_Heishi2: only FUN_00249af8 differs (baseline).
- Actor GLOBAL_ASM data + 4 action funcs + InitVars present.
- GLOBAL_ASM lines removed from src/functions/functions_{120000s,140000s,200000s,240000s,280000s}.cpp for the 8 functions.

# En_Heishi2 — cascade stage 1 (Haiku), batch 2/5

| Function | Status | Notes |
|---|---|---|
| FUN_00259e98 | MATCHED | action setter: `unk_938 = GetLastFrame(skel,2)`, Animation_Change(skel,2,1,0,frames,2,-10) -> FUN_001ca460; moved to z_en_heishi2.cpp (1st try) |
| FUN_002063c4 | MATCHED | same template -> `unk_954 = 0` -> FUN_00156988 (1st try) |
| FUN_0021c8c4 | MATCHED | `Message_GetState == self->unk_94C && ShouldAdvance` -> FUN_0036e980(play,NULL,8), FUN_00370778(play) -> FUN_00259e98 (1st try) |
| FUN_002055b4 | MATCHED | same message template -> FUN_00288594 (1st try) |
| FUN_001cb90c | MATCHED | TEXT_STATE_EVENT(5) branch: textId 0x2021, Rupees_ChangeBy(15), ContinueTextbox -> FUN_00177c24 (1st try) |
| FUN_001cd6f4 | MATCHED | Math_SmoothStepToS / ApproachF on unk_930 (float->s16 step), `world.rot.z = shape.rot.z`, Actor_Kill tail (1st try) |
| EnHeishi2_Destroy | MATCHED | 3 variants: `ColliderCylinder* collider` local -> 9/24 words (base reg hoisted); `PlayState* play` local -> `mov r0,r1` scheduled late (5/24). Winner: no play local, `Collider_DestroyCylinder((PlayState*)state, &self->collider)`, 0/24. Tail `SkelAnime_Free2`. Confirmed by ws_check (armlink inlines the stub) |
| FUN_00288594 | NOT MATCHED (cfg) | functions.tsv range is 292 B: first 92 B = this fn (matches), 0x2885f0..0x288710 is a second real function merged in (cfg). Draft under `#if 0` in z_en_heishi2.cpp; GLOBAL_ASM kept in functions_280000s.cpp |

Header (`z_en_heishi2.hpp`): typed 0x930 `f32 unk_930`, 0x938 `f32 unk_938`, 0x94C `s16 unk_94C`, 0x954 `u8 unk_954`, 0x9A4 `ColliderCylinder collider` (0x58, dim at +0x40 matches Destroy), 0xA00 `void* unk_A00`. Size unchanged 0xA34.

Moved into z_en_heishi2.cpp (by name): FUN_00259e98, FUN_002063c4, FUN_0021c8c4, FUN_002055b4, FUN_001cb90c, FUN_001cd6f4, EnHeishi2_Destroy. GLOBAL_ASM removed from functions_240000s.cpp (FUN_00259e98), functions_200000s.cpp (FUN_002063c4, FUN_002055b4, FUN_0021c8c4), functions_1C0000s.cpp (FUN_001cb90c, FUN_001cd6f4), and the EnHeishi2_Destroy GLOBAL_ASM from the actor .cpp.

Checks: ws_check.sh En_Heishi2 = baseline only (FUN_00249af8). Callees FUN_0035021c / FUN_00370778 / Rupees_ChangeBy are declared locally in z_en_heishi2.cpp (no include/ change).

# En_Heishi2 — cascade stage 1 (Haiku), batch 3/5

| Function | Status | Notes |
|---|---|---|
| FUN_001cbb1c | MATCHED | msg state template: `Message_GetState == unk_94C && ShouldAdvance` -> FUN_003725e0, then unk_94A 2 -> FUN_00298ef4 / 5 -> FUN_002742e8 (if/else-if) (1st try) |
| FUN_00238bc4 | MATCHED | TEXT_STATE_EVENT: `gSaveContext.infTable[7] \|= 0x40` (0x588858+0x1e; index 7, not 15), FUN_0036e980(play,NULL,7) -> FUN_002742e8 (2nd try, index fix) |
| FUN_00177c24 | MATCHED | TEXT_STATE_EVENT: `unk_95A == 0` -> unk_956=0, FUN_003725e0, -> FUN_002742e8; else FUN_00370778 -> FUN_002063c4 (1st try) |
| FUN_00180674 | MATCHED | `Math_SmoothStepToS(&shape.rot.z, -6100, 5, (s16)unk_930, 0)`, ApproachF(unk_930, 3000, 1, 500), world.rot.z copy, if rot.z < -6000: FUN_00367c7c(play,0x708f,NULL), flags\|=0x10000, unk_930=0, -> FUN_0019f4d4 (1st try) |
| FUN_001e883c | MATCHED | SubCam state: CameraSetAtEye(play,subCamId,&subCamAt,&subCamEye); `gate` local declared AFTER the call (before it: 16 words); `unk_93E == 0 \|\| gate->unk_168 == 0` -> ClearCamera, ChangeCameraStatus(0,7), FUN_003725e0, unk_958=1, FUN_0036e980(play,NULL,7) -> FUN_00298ef4 (3rd try) |
| EnHeishi2_Draw | MATCHED | `GraphicsContext_UnknownStub(play->state.gfxCtx)` (dead gfx load + empty stub), SkelAnime_DrawOpa(&skel, &modelMtx, FUN_002110e4, FUN_0024ba60, thisx, 0); if unk_94A==5 && infTable[7]&0x80 && Object_GetIndex(objectCtx,0x15)>=0: unk_A00->SetUnkAC(1), FUN_003721e0(&unk_A04), FUN_00372170(0). Moved from GLOBAL_ASM into z_en_heishi2.cpp (1st try) |
| FUN_001ca460 | NOT MATCHED | = N64 func_80A53638 (spear-hit gate search, sets gate unk_168=1). Same play-in-r4 issue as FUN_002054f8: ROM copies `play` to r4 at entry (`mov r4,r1` before vpush) and loads actorLists head through it; armcc keeps play in r1. Best 38/48 (SkelAnime* local variant). ~8 variants (play2/state/typed actor/order). Draft under `#if 0` in z_en_heishi2.cpp, GLOBAL_ASM kept in functions_1C0000s.cpp |
| FUN_002054f8 | NOT MATCHED | = N64 func_80A53F30-like gate wait (actor id 0x100 = ACTOR_BG_GATE_SHUTTER, openingState=1 u16 store at +0x1C0 -> FUN_002aa134). Same play-in-r4 entry copy; ROM loop 16 bytes longer than ours (172 vs 188). Best 37/47 (k2 draft). ~7 variants. Draft under `#if 0` at end of z_en_heishi2.cpp, GLOBAL_ASM kept in functions_200000s.cpp |

Header (`z_en_heishi2.hpp`): new typed fields 0x08CC `subCamAt`, 0x08D8 `subCamEye` (Vec3f), 0x093E `u16 unk_93E`, 0x0956 `u8 unk_956`, 0x0958 `u8 unk_958`, 0x095A `u16 unk_95A`, 0x095C `s16 subCamId`, 0x0960 `Actor* gate`; 0x0A00 retyped `SkeletonAnimationModel* unk_A00` (Draw calls its methods). Size unchanged 0xA34.

Moved into z_en_heishi2.cpp (by name): FUN_001cbb1c, FUN_00238bc4, FUN_00177c24, FUN_00180674, FUN_001e883c, EnHeishi2_Draw. GLOBAL_ASM removed from functions_1C0000s.cpp (FUN_001cbb1c, FUN_001e883c), functions_200000s.cpp (FUN_00238bc4), functions_140000s.cpp (FUN_00177c24), functions_180000s.cpp (FUN_00180674), and the EnHeishi2_Draw GLOBAL_ASM from the actor .cpp.

Includes: z_en_heishi2.cpp now includes `../Bg_Spot15_Saku/z_bg_spot15_saku.hpp` (BgSpot15Saku* cast for unk_168). Callee decls added locally: FUN_003725e0, FUN_0019f4d4, FUN_002743c0, GraphicsContext_UnknownStub, Object_GetIndex. No include/ change.

Checks: fastchk 0 words differ for all 6 matched + previous matches. ws_check.sh En_Heishi2 = baseline only (FUN_00249af8).

# En_Heishi2 — cascade stage 1 (Haiku), batch 4/5

| Function | Status | Notes |
|---|---|---|
| FUN_002744b8 | MATCHED | choice state (SkelAnime_Update, TEXT_STATE_CHOICE, FUN_00369f3c switch); rupees check `gSaveContext.rupees >= 10`; 1st try |
| FUN_002743c0 | MATCHED | subcam setup: Animation_Change(idx 0, 1.0, 0.0, lastFrame, LOOP, -10), unk_93E[0]=300, CreateSubCamera, ChangeCameraStatus(0,1)/(sub,7), at/eye stores, -> FUN_001e883c; 1st try |
| FUN_00238abc | MATCHED | subcam wait: `gate` local BEFORE the `unk_93E[0]==0 \|\| gate->openingState==0` test (else 25 words); `if (unk_956 != 2)` nested with `==0` then else, rupee branch in the else (armcc layout) |
| FUN_0038a670 | MATCHED | choice-text state: `if (!(infTable[7]&0x80))` mask branch first (else 0x2020 block), `Player_GetMask==1` keaton test, face-reaction re-check; `var` declared then `var = 0` after `unk_957 = 0` (zero reg); mask test inverted (`== 1` first) |
| FUN_00156988 | NOT MATCHED | gate-shutter search (openingState -1/2, ACTOR_BG_GATE_SHUTTER). ROM copies play to r4 at entry and computes `self+0x1a4` then `+0x3c` for curFrame; any local/`(PlayState*)state` form folds the offset (49 words, 12 B short). Out-of-line `EnHeishi2_GetCurFrame` accessor (z_en_heishi2_anim.cpp, removed again) matched the frame load but its `vmov` makes the body 4 B too big (overlaps next fn). Draft under `#if 0`, GLOBAL_ASM kept |
| FUN_002aa134 | NOT MATCHED | subcam setup for gate shutter (same head as FUN_002743c0, + Vec3f copies at 0x908/0x8E4 then 0x8CC/0x8D8). Body matches except register numbering of the six pool constants (17/68 words, all `vldr/vstr` reg swaps). Tried: field stores (17), fields-from-fields copy (20), inline Vec3f setter (41). Draft under `#if 0`, GLOBAL_ASM kept |
| FUN_0019bec4 | NOT MATCHED | item-give choice (infTable[7] \|= 0x80, itemGetInf[3] \|= 0x100, FUN_00376a78(play,0x2c)). `switch` over choice 0/1 with `if (choice != 0)` layout + hoisted r6=1 / r7=FUN_00177c24 match; left: ROM predicates `strheq r0,[unk_95A]` on `unk_956==0` (armcc emits mov+strh), 4 B. 39/72 words. Draft under `#if 0`, GLOBAL_ASM kept |
| EnHeishi2_Update | NOT MATCHED | DECR loop (no unroll) is in the draft; remaining 11/73 words: loop index and unk_948 temp swap regs (ROM i=r0, ours r1). Earlier attempts: `Actor_SetFocus(thisx,..)` 64 words, timers local 55 words (unrolled loop, +40 B). Draft under `#if 0`, GLOBAL_ASM kept |

Header (`z_en_heishi2.hpp`): `unk_8E4` -> `Vec3f`, `unk_908` `Vec3f` (copies of subcam at/eye), `unk_92C` f32 (Update focus height), `unk_93E[5]` u16 (timers, Update views it as s16 via cast), `unk_948` u16 (frame counter), `unk_955`/`unk_957` u8. Size unchanged 0xA34.
Matched function touched: FUN_001e883c `self->unk_93E` -> `self->unk_93E[0]` (0 words diff, re-verified). FUN_002063c4 untouched.

Moved (by name) into z_en_heishi2.cpp: FUN_002744b8, FUN_002743c0, FUN_00238abc, FUN_0038a670. GLOBAL_ASM removed from functions_240000s.cpp (FUN_002743c0, FUN_002744b8), functions_200000s.cpp (FUN_00238abc), functions_380000s.cpp (FUN_0038a670). Kept as GLOBAL_ASM: functions_140000s.cpp (FUN_00156988), functions_2A0000s.cpp (FUN_002aa134), functions_180000s.cpp (FUN_0019bec4), actor cpp (EnHeishi2_Update).
Callee decls added locally: FUN_001e74ec, FUN_00259ef4, FUN_00345fcc, FUN_00376a78, FUN_0036bcc8, Player_GetMask. Includes: z_en_heishi2.cpp now includes `../Bg_Gate_Shutter/z_bg_gate_shutter.hpp`. No include/ change.

Checks: fastchk 0 words differ for all 26 C functions (4 new + 22 previous). ws_check.sh En_Heishi2 = baseline only (FUN_00249af8).

# En_Heishi2 — cascade stage 1 (Haiku), batch 5/5

| Function | Status | Notes |
|---|---|---|
| FUN_001e74ec | MATCHED | = N64 func_80A53AD4 (talk-request state). `Player* player = GET_PLAYER(play)` local; textId 0x200E when first face-reaction call is 0, else a second Text call; FUN_0036bc84 == 1 -> player textId 0x2010, 94C=5, -> FUN_002055b4; != 0 -> player textId 0x200F; no talk and in range -> tail FUN_0036bbd0(actor, play, 1, 100.0f). 1st try. Moved from functions_1C0000s.cpp |
| FUN_0019f4d4 | MATCHED | = N64 func_80A5455C (bomb spawn after message). Needs `unk_8C0` Vec3f (header: was padding, unk_274 in N64). `(Actor* thisx)` signature + cast inside: the `EnHeishi2*` signature was 19 words off (self/base regs swapped). Cast added in FUN_00180674. Moved from functions_180000s.cpp |
| FUN_0038a918 | NOT MATCHED | Choice/face-reaction state (no direct N64 twin). Size off by 8 B (ROM 328, ours 336); self/base regs swapped (ROM self=r4, 0x900 base=r5). Tried: EnHeishi2* and Actor* signatures, faceReaction local vs inline, store order, early returns in 7006/7002 paths, 7029 as last else, play2 copy. Best 43/82 words. Draft under `#if 0`, GLOBAL_ASM kept in functions_380000s.cpp |
| FUN_00259ef4 | NOT MATCHED | = N64 func_80A5475C-like talk-offer state (types 2/5). Same size; ROM shares the action-store tails (0x259fa8 for FUN_0038a918, 0x259fc4 for FUN_0038a670) between pre-talk and post-talk paths, ours duplicates them. Tried: if/else chain for talk block (55 words), ternary for 2744b8/0038a918 (24), yaw temp fix (kept). Best 21/96 words. Draft under `#if 0`, GLOBAL_ASM kept in functions_240000s.cpp |

Prototype note: FUN_00259ef4 keeps a declaration (used by matched FUN_0038a670); FUN_0038a918 keeps its `EnHeishi2*` prototype (matched FUN_00298ef4 unchanged).
Header (`z_en_heishi2.hpp`): `unk_8BE[0xE]` split into `unk_8BE[0x2]` + `Vec3f unk_8C0` (0x8C0). Size unchanged 0xA34.

Checks: fastchk 0 words differ for FUN_001e74ec, FUN_0019f4d4 and all earlier matched functions. ws_check.sh En_Heishi2 = baseline only (FUN_00249af8).

# En_Heishi2 — cascade stage 3 (Opus)

| Function | Status | Notes |
|---|---|---|
| EnHeishi2_Update | MATCHED | `(EnHeishi2* self, PlayState* play)` signature (prototype + `(ActorFunc)` InitVars) + N64 `for (i = 0; i != 5; i++) DECR(...)`. GLOBAL_ASM removed from actor .cpp |
| FUN_0038a918 | MATCHED | = N64 func_80A53278. Literal N64 shape: actionFunc stored in EVERY branch, 7071/7072 as if/else, `(EnHeishi2*, PlayState*)` sig; only 7006/7002 blocks keep an explicit `return;` (gives ROM's separate pop tails). GLOBAL_ASM removed from functions_380000s.cpp |
| FUN_002aa134 | NOT MATCHED (8/68) | = N64 func_80A53DF8 (908 = subCamEyeInit, 8E4 = subCamAtInit). Only the six pool-constant VFP regs differ. Searched const/copy-from-Init-field/f32-local per component (729 variants): best copies subCamAt.y/.z + subCamEye.x from the Init fields (x1/y1 swap left). Placement-new Vector3f, struct copy, chained, N64 interleaved order all worse. Draft `#if 0`, GLOBAL_ASM kept |
| EnHeishi2_Init | BLOCKED (infra) | inlines a guarded function-local static identity MTX34 (guard 0x0055A210 inside the .data dump, object 0x005BE29C .bss, `__cxa_guard_acquire` + linker-inlined release). Needs pinned COMDAT in data/oot3d.ld + data chunk split (LOADER_RECIPE) — same blocker as End_Title FUN_00250540. GLOBAL_ASM kept |
| FUN_00288594 | skipped | cfg-merged |

Checks: fastchk 0 words for all 34 C functions in z_en_heishi2.cpp; ws_check.sh En_Heishi2 = baseline only (FUN_00249af8), 0 non-function bytes.
