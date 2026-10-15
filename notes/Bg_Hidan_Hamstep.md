# Bg_Hidan_Hamstep: cascade stage 1 (batch 1/1)

Scope: BgHidanHamstep_Update, BgHidanHamstep_Destroy, BgHidanHamstep_Draw, FUN_002070e4, FUN_001e9f50.

| Function | Result | Notes |
|---|---|---|
| BgHidanHamstep_Update | MATCHED | `self->actionFunc(self, play)` tail call |
| BgHidanHamstep_Destroy | MATCHED | DynaPoly_DeleteBgActor + Collider_DestroyTris + variadic FUN_00350f34 (skel0, skel1, 0) |
| BgHidanHamstep_Draw | MATCHED | two duplicated branches on params&0xFF (compiler needs the duplicated body, a ternary merges and is 88 vs 136 bytes) |
| FUN_002070e4 | MATCHED, moved | `bx lr` stub (DoNothing action). Moved into actor .cpp; GLOBAL_ASM removed from functions_200000s.cpp |
| FUN_001e9f50 | NOT MATCHED, left as GLOBAL_ASM | action 0 (wait for hammer hit). Draft under `#if 0` in actor .cpp. Diff: only the 4 prologue words differ (ROM does `mov r5,r1` before `ldrb r1,[r0,#0x1cd]`; ours loads acFlags into r0 first). Tried ~15 variants: this/thisx params, collider/actor local pointers, inverted if, flags local, u32/u8 table cast; the table must be the extern `BgHidanHamstep_sActionFuncs` (raw 0x5118D8 cast folds to a different offset). |

Structure notes (3DS): actionFunc 0x294, action 0x298, skelAnimModel[2] 0x2A0, collider 0x1BC (ColliderTris), colliderElements[2] 0x1DC.
BgHidanHamstep_Init left as GLOBAL_ASM (not in this batch).

ws_check.sh Bg_Hidan_Hamstep: baseline only (FUN_00249af8).

## Stage 2 (Sonnet): BgHidanHamstep_Init, FUN_00109acc, FUN_00123038, FUN_001e9f50

| Function | Result | Notes |
|---|---|---|
| FUN_00109acc (action 1) | MATCHED, moved | Child effects loop must be written INLINE (a static inline helper swaps r7/r8 and FP regs); `Vec3f* vel = &actor.velocity; vel->y *= -0.24f;` forces the reload of unk_29C after the float store; `unk_29C > 6` (not `>= 7`). |
| FUN_00123038 (action 3) | NOT matched, GLOBAL_ASM | Best draft (56 words) in `#if 0` in actor .cpp: all fields via `Actor* thisx`. ROM: self r5/play r7/table r8, extra `mov r6,r5` copy for the effects block, params reloaded after the unk_29C store. |
| FUN_001e9f50 (action 0) | NOT matched | 4 prologue words (ROM `mov r5,r1; ldrb r1,..; mov r4,r0`); ~20 more variants tried (helper SetupAction, thisx, play copy, Collider* local, inverted if). |
| BgHidanHamstep_Init | NOT matched | Draft (230 words differ, 1020 vs 1060 B) in `#if 0`. ROM spills play twice ([sp+0x58], copy [sp+0x38]), `mov r4,r0` first, DynaPolyInfo_Alloc result stored via inlined `str r0,[r1]` + nops. |

New: `data_syms.s` in the actor dir (EQU symbols for sInitChain/sYPosOffsets/sTrisInit/sActionFuncs/sEffectPositions at 0x5118B0..). hpp: unk_29C is now s32.
ws_check.sh: baseline only (FUN_00249af8).

## Stage 3 (Opus): FUN_001e9f50, FUN_00123038

| Function | Result | Notes |
|---|---|---|
| FUN_00123038 (action 3) | MATCHED, moved | N64 helpers func_80888694/func_808884C8 written inline; `(Actor* thisx)` for fields, child clamp as `if (child->y > thisx->y)` (operand order), `home.pos.y + sYPosOffsets[..]` (not reversed), plain `thisx->velocity.y *= -0.24f` (no Vec3f* trick), and the effects block gets its own `BgHidanHamstep* step = self;` (ROM r6). GLOBAL_ASM removed from functions_120000s.cpp. |
| FUN_001e9f50 (action 0) | NOT matched | Still 4 prologue words. ~30 more variants (see comment above the `#if 0` draft). |
| BgHidanHamstep_Init | skipped | |

ws_check.sh: baseline only (FUN_00249af8).
