# Actor_1D7 (stage 1, Haiku) status

Baseline check (scripts/ws_check.sh Actor_1D7): only FUN_00249af8 differs (known). No regressions.

| Function | Status | Notes |
|---|---|---|
| Actor1D7_Init | MATCHED (C) | Flag test uses gSaveContext+0x1000+0x360 (folds to ROM literal 0x588958 + ldr #0x360). `params` local as s16 needed for register order. |
| Actor1D7_Destroy | MATCHED (C) | Tail call to FUN_00350f34 kept. |
| Actor1D7_Draw | MATCHED (C) | Uses SkeletonAnimationModel methods (SetUnkAC, FUN_003721e0, FUN_00372170). |
| Actor1D7_Update | NOT MATCHED, left as GLOBAL_ASM | Logic understood (see draft under #if 0). Compiles, but register allocation / constant placement differs (147/161 words). Tried: constant local order, pos copy placement, Player* typing, ACTORCAT_ITEMACTION for the 0x9F-actor list (0x20D4 head = ACTORCAT_ITEMACTION, not ENEMY). |

Update logic (for next pass):
- if timer != 0 return. Player = GET_PLAYER (state+0x20AC). If player[0x1A9]==6 && u16 player[0x2248]!=0: player pos at player+0x22A8, d2=dx^2+dz^2 in [61504,82944], dy in [0,400], angle=atan2(dz,dx)(+2pi if <0), |angle - tbl[params]| < 0.75 (tbl = 0x514340) -> set unk_1C4 = player y (+0x22AC), unk_1C8 = angle, done.
- else loop actorLists[ACTORCAT_ITEMACTION] (next at 0x130), id 0x9F: R = 288 + scale.x*325 (288 = tbl_0x51432C[0]*40), ring (R-40)^2 <= d2 <= R^2, dy in [0,400], |angle - tbl[params]| < 1.2 -> unk_1C4 = other y, unk_1C8 = angle, done.
- done: timer = 60, actor->update = FUN_0037bb4c, unk_1CC = 0.0f.

Left as asm:
- FUN_0037bb4c (action fn set by Update, lives in src/functions/functions_370000s.cpp, GLOBAL_ASM). Large (guard-acquire static init, Rand, particle-like loop). Not attempted at stage 1.
- FUN_0037c168 (next in functions_370000s.cpp) not inspected.

Debt / notes:
- Raw data tables: 0x0051432C (f32 table) and 0x00514340 (angle table) used by raw pointer casts in the #if 0 draft. Need EQU data symbols in the actor dir for Update.
- Init chain at raw 0x0051434C.
- Data GLOBAL_ASM("data/z_Actor_1D7.data.s") left as is.


## Stage 2 (Sonnet)
- Raw addresses replaced: `src/game/actors/Actor_1D7/data_syms.s` (EQU Actor1D7_sConsts 0x51432C, Actor1D7_sAngles 0x514340, Actor1D7_sInitChain 0x51434C), pulled in via GLOBAL_ASM("../src/...") like Bg_Mori_Rakkatenjo. Init/Destroy/Draw still 0 words off; ws_check = baseline only.
- Actor1D7_Update: NOT MATCHED, 147 -> 37/161 words off (draft under #if 0, GLOBAL_ASM kept). Findings: ROM consts are 40*c[0] (=288 base radius), c[1]*40 (=400 loop max dy, same var as the literal 400 of the player branch), c[3]*325; the player-branch ring check is the loop check with radius=288.0f constant-folded (82944/61504) -- writing `radius = 288.0f; radius*radius`/`(radius-40)^2` kills the int-compare range merge; loop test in positive form (`distSq <= r*r && distSq >= ... && dy >= 0 && dy <= maxDy`) gives ROM's blt/bhi; shared finish via `goto done`; consts declared AFTER `player = GET_PLAYER` (hoists land after the timer check); fabs helper taking the `zero` local. Remaining: float s-reg numbering (ROM dy=s16, distSq=s17, 400=s18, 2pi=s20, 40=s21, 0=s22; ours puts zero in s16) and finish-block order (ROM: mov/strh/ldr FUN/vstr/str).
- FUN_0037bb4c: NOT attempted. Not the shared model loader: its guard (0x514334) sits in this actor's data dump and the guarded static is a zeroed Vec3f at bss 0x569B24 (no symbol); a C static would create its own guard/object and shift layout. Big function (Rand, particles, cosf/sinf, spawn) -> left as asm.

## Stage 3 (Opus)
- Actor1D7_Update: still NOT MATCHED, 37 -> 33/161 words (draft under #if 0; GLOBAL_ASM kept). Finish block order fixed (`timer = 60; unk_1CC = zero; update = FUN_0037bb4c;` gives ROM mov/strh/ldr/vstr/str).
- Remaining: float reg numbering + loop radius. armcc (fpmode=fast) always reassociates `scale.x * (c[3] * 325.0f)` into `(scale.x*c[3])*325` (tried ~15 operand orders, temp local, double literal, 8.125*ringWidth); ROM computes `c[3]*325` first then `vmla radius, scale, k`. Probably the real source shape differs there (unknown).
- Tried: all 24 orders of the const locals, local vs literal for each const, block-scoped vs function-scoped dx/dy/dz/distSq/angle (no effect), per-use literal 0.0f mix (size changes), inline check-helper shared by both branches (much worse). Replacing `zero` everywhere by literal 0.0f + plain fabs makes the player branch dy=s16/distSq=s17/400=s18 match ROM, but moves play+0x2000 to r8 (35 words) -> kept the 33-word draft.
- FUN_0037bb4c: skipped (function-local static guard at 0x514334 in data dump).
