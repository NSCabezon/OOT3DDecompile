# En_GeldB status (cascade stage 1, batch 1/3)

Header: `z_en_geldb.hpp` rewritten with the 3DS layout (size 0xDEC). Offsets derived from the ROM asm:
N64 fields after `skelAnime` shift by +0x8FC (action 0xBE8, actionFunc 0xBF0, timer 0xBFC, invisible 0xC14),
colliders/after by +0x908 (headRot 0xDE4). `SkelAnime` is 0x84 on 3DS.

| Function | Status | Note |
|---|---|---|
| EnGeldB_OverrideLimbDraw | MATCHED | linked, byte-exact |
| EnGeldB_SetupAdvance | MATCHED | linked, byte-exact |
| EnGeldB_SetupRollBack | MATCHED | linked, byte-exact (store order: speed, action, sfx, shape=world rot) |
| EnGeldB_SetupJump | MATCHED | linked, byte-exact (store order: timer, speed, velY, invisible, action, sfx) |
| EnGeldB_Stunned | MATCHED | linked, byte-exact. Uses `*(s16*)((u8*)self + 0x11A)` for actor colorFilterTimer (no named field in include/Actor) |
| EnGeldB_Destroy | NOT MATCHED | ROM has no call for Collider_DestroyCylinder/Quad: it sets the args then `mov r0,#1` (8-byte stub 'return 1' with its call elided). Ours emits `bl`; Collider_DestroyQuad is not in the link at all. Pure/const/inline stubs tried (args dropped, 6 words off). Left GLOBAL_ASM, draft under #if 0. |
| EnGeldB_SetupReady | NOT MATCHED | Two Rand calls + round-to-nearest pattern (0.5 accumulator in s17, vnmls in else). Size 236 vs 240; 36 words off. ~6 variants. Left GLOBAL_ASM, draft under #if 0. |
| EnGeldB_SetupSpinDodge | NOT MATCHED | Structure matches; constant regs swapped (ROM keeps -10.0 in s17, ours in s18), and func ptr/timer register order differs. 14 words off. ~8 variants. Left GLOBAL_ASM, draft under #if 0. |

ws_check.sh En_GeldB: baseline only (FUN_00249af8).

## Batch 2/3 (cascade stage 1)

| Function | Status | Note |
|---|---|---|
| EnGeldB_Flee | MATCHED | linked, byte-exact. Frame checks are float range compares (ROM: `10.2 < f < 10.4` sound, `f <= 2.0` dust); single combined range compare is not the ROM shape, so nested `if` is used |
| EnGeldB_Jump | MATCHED | linked, byte-exact. Sword flag written as `*(u8*)&self->swordCollider[0x10]` (the `self->swordCollider[0x10]` form misallocates regs) |
| EnGeldB_RollBack | MATCHED | linked, byte-exact. Same sword-flag form; spin-attack setup and `play->state.frames` breath check |
| EnGeldB_DodgeRanged | MATCHED | linked, byte-exact. Lives in its own file `z_en_geldb_dodge.cpp` (not in z_en_geldb.cpp), so the Setup helpers are not inlined into it. 2nd float arg of FUN_00346e2c is 1.0f (ROM pool) |
| EnGeldB_Defeated | NOT MATCHED | 6 words off: play and the 0 constant swapped between r6/r7 (ROM keeps play in r6). Tried play2 copies, Actor* signature (collides with prototype), range variants. Draft under #if 0 |
| EnGeldB_SetupBlock | NOT MATCHED | 34 words off: timer rounding branch uses vnmls in ROM; our float temp lands in s0 not s17; lastFrame/zero registers swapped (s19/s20). ~7 variants. Draft under #if 0 |
| EnGeldB_SetupCircle | NOT MATCHED | 23 words off: timer region float regs (30.0 in s18, 3.0 in s19, 0.5 in s16) and temp accumulator naming differ. Constants verified from ROM pool. ~8 variants. Draft under #if 0 |

Other notes:
- ROM pool decoding (vldr/ldr [pc,#off] targets) was the fastest way to get float constants; two constants were wrong in first drafts (Defeated Animation_Change speed -2.0f / morph -4.0f).
- Added prototypes at the top of z_en_geldb.cpp (no include/ edits). Helpers without a FUN_ name in the link use the ROM asm symbol names (Actor_WorldYawTowardActor, Actor_WorldDistXYZToPoint, Animation_PlayOnce).
- New file: `src/game/actors/En_GeldB/z_en_geldb_dodge.cpp` (picked up by the GLOB_RECURSE in CMake).

ws_check.sh En_GeldB: baseline only (FUN_00249af8).

## Batch 3/3 (cascade stage 1)

| Function | Status | Note |
|---|---|---|
| EnGeldB_Pivot | MATCHED | linked, byte-exact. The ROM inlines SetupAdvance into Pivot, so its body is written out inline. turnRate needs an if/else (a ternary gets if-converted to predicated vmla). Breath-sound frame check uses `*(u32*)((u8*)play + 0x5BF4)` (ROM loads it via a literal pool) |
| EnGeldB_Wait | MATCHED | linked, byte-exact. Added `u8 unk_C17` at 0xC17 to z_en_geldb.hpp (ROM byte: set to 1 when the fight starts, gates the move-down condition `xzDist > 300 && C17 == 0`). Store order: pos.y before rot.y; flags before playSpeed in the ground-touch block |
| EnGeldB_Damaged | MATCHED | linked, byte-exact. Lives in z_en_geldb_dodge.cpp: in z_en_geldb.cpp armcc inlined SetupJump/SetupRollBack (676 vs 476 bytes) where ROM tail-calls them. Added `BGCHECKFLAG_WALL` define |
| EnGeldB_RollForward | NOT MATCHED | 2 words off (0xD8, 0xDC): in the negative timer branch ROM accumulates `5+r*5` into the original 5.0 register (vmla s19,s0,s20), ours into the copy. Draft (2 words) under #if 0 in z_en_geldb.cpp. Must live in the dodge file if made live (SetupAdvance would otherwise be inlined) |
| EnGeldB_SetupSideStep | NOT MATCHED | Timer is `(s32)(0.5f + x*3.0f*0.5f)` / `x*3.0f*0.5f - 0.5f` with literal constants (no gGameInfo load in ROM). Common-store shape (s32 local) gets 5.0/3.0 literals in s20/s19 where ROM has s19/s20 (66 words off). Per-branch stores fix the registers (31 words off) but add a store per branch. ROM also reloads speedXZ at the join. ~13 variants incl. dodge-file placement and swapped branches. Draft (31 words) under #if 0 |

Notes:
- `z_en_geldb_dodge.cpp` now also holds EnGeldB_Damaged (matched).
- Helper for splicing per-function bodies lives in ws/En_GeldB/tmp/g3 (scratch only).

ws_check.sh En_GeldB: baseline only (FUN_00249af8).

## Stage 2 (Sonnet) -- Haiku leftovers + large functions

ws_check.sh En_GeldB: baseline only (FUN_00249af8), 0 non-function bytes.

| Function | Status | Note |
|---|---|---|
| EnGeldB_Destroy | MATCHED | `Collider_DestroyCylinder` (real C fn in z_collision_check.cpp) and `FUN_0034eaf8` (= Collider_DestroyQuad) are 8-byte `return 1` stubs that armlink inlines (dead `mov r0,#1`). `FUN_0034eaf8` was a GLOBAL_ASM in functions_340000s.cpp: it must be C in a file other than the caller or armlink does not inline it. Moved to z_en_geldb_dodge.cpp as `s32 FUN_0034eaf8(PlayState*, void*) { return 1; }`; the GLOBAL_ASM line was deleted from src/functions/functions_340000s.cpp (only edit outside the actor dir) |
| EnGeldB_SetupReady | MATCHED | timer = ternary with the Rand expression repeated in each arm (see idioms); `s16 yaw = shape.rot.y; world.rot.y = yaw;` fixes the tail scheduling (pool load of the action fn) |
| EnGeldB_Defeated | MATCHED | signature `(Actor* thisx, PlayState* play)` + `thisx->` for Actor fields: play in r6, hoisted 0 in r7 (prototype/assignment cast `(EnGeldBActionFunc)`) |
| EnGeldB_SetupBlock | MATCHED | ternary timer + dead `EnGeldB* s2 = self; Actor* thisx = &s2->actor;` (keeps 0.0f in s19 / lastFrame in s20); speedXZ stored via thisx |
| EnGeldB_SetupCircle | MATCHED (dodge file) | timer via `s32 t; if (..>0) t=A; else t=B; self->timer=t;` (ternary variant is 12 words off). Must live outside z_en_geldb.cpp or it is inlined into Pivot |
| EnGeldB_SetupSideStep | MATCHED (dodge file) | `f32 v` for the 2nd/3rd speed arms, playSpeed read through `thisx->speedXZ` (ROM reloads speedXZ), ternary timer |
| EnGeldB_RollForward | MATCHED (dodge file) | plain ternary timer (the Haiku `if` form was 2 words off) |
| EnGeldB_Ready | MATCHED | SetupAdvance/RollForward/SpinAttack/Pivot setups inlined by hand (as the ROM); `angle = yaw - (shape.rot.y + headRot.y)`; one read of shape.rot.y through `Actor* thisx` fixes r0/r1 order; `world.rot.y = shape.rot.y = yaw` (N64 order) |
| EnGeldB_SpinDodge | MATCHED (dodge file) | `Actor* thisx` alias read for the first `xzDistToPlayer <= 45.0f`; `SkelAnime* sa; sa->playSpeed = ..` (store through another pointer => ROM reload in the clamp); `afterPrevFrame >= 1` / `>= 6` instead of `> 0` / `> 5` |
| EnGeldB_Sidestep | MATCHED (dodge file) | same sa/playSpeed idiom; NO `f32 dist` local (it flips the compare registers); SetupSlash / SetupRollForward / SetupSpinAttack written out inline |
| EnGeldB_SetupSpinDodge | NOT MATCHED, 9 words | all code identical except the literal-pool load of EnGeldB_SpinDodge (ROM: after the vstr's using r0; ours: hoisted into ip). ~60 variants incl. statement permutations, thisx/s2 aliasing. Draft under #if 0 |
| EnGeldB_Block | NOT MATCHED, 10 words | pure register swap: ROM base(play+0x5000)=r5, player=r6; ours player=r5, base=r6. Same tie-break problem as ReactToPlayer/Update (see below). Draft under #if 0 |
| EnGeldB_Slash | NOT MATCHED, ~10 words | everything matches except the first timer block: ROM has no `vmov s19,s18` copy before its condition (block 2 does). Draft under #if 0 |
| EnGeldB_SpinAttack | NOT MATCHED, ~8 words | frame-13 block store order (ROM: speedXZ, then swordState) and 6.0f hoisted to the entry (needs `f32 six = 6.0f` local, which then shifts the pool order). Draft under #if 0 |
| EnGeldB_Circle | NOT MATCHED, 3 words | second `xzDistToPlayer > 40.0f` integer compare has r0/r1 swapped. Draft under #if 0 |
| EnGeldB_Advance | NOT MATCHED, 4 words | register naming of the 150 < xzDist < 210 range-check literals (r0/r1). Draft under #if 0 |
| EnGeldB_ReactToPlayer | NOT MATCHED, 29 words | same size/layout; callee-saved regs of player/base (r6/r7) and arg2/angleToLink (sl/fp) swapped. Draft under #if 0 |
| EnGeldB_Update | NOT MATCHED, ~100 words | draft with CollisionCheck + TurnHead inlined is within 8 bytes; play (r8) / self+0xB00 base (r7) swapped, lookTimer rounding is sign-conditional in the ROM, Damaged/Defeated setup store order. Draft under #if 0 |
| EnGeldB_Init | NOT ATTEMPTED | needs 0x24-byte effect struct array with ctor FUN_003fd780 (`__aeabi_vec_ctor_nocookie_nodtor`), raw data addresses (0x00524E48/28/D90/DC8/DD8) and unnamed tables |
| EnGeldB_Draw | NOT ATTEMPTED | raw global addresses (0x0053CC44, 0x005879E4, 0x00588858: BGM/cutscene state), table 0x00524E54 |
| EnGeldB_PostLimbDraw | NOT ATTEMPTED | 9 guarded function-local statics (`__cxa_guard_acquire`) = LOADER_RECIPE class, needs data-chunk split |

Idioms / facts learned (details in the final report): timer-rounding shape, `s16 yaw` trick, thisx/s2 aliasing, store-through-other-pointer to force a reload, ROM `frames % 3`, `Animation_OnFrameImpl(skel, frame, 1.0f)` for `(s32)curFrame == N` (frames scaled 3DS-rate), unknown callee names:
FUN_0035b950 (func_800354B4), FUN_0035e600 (Actor_TestFloorInDirection), FUN_0035f228 (Actor_IsLockedOn), FUN_00369608 (Actor_OtherIsLockedOn), FUN_00374bb8 (Actor_SetPlayerKnockbackLargeNoDamage), FUN_0036e980, FUN_00367c7c (Message_StartTextbox), FUN_00375fd0 (Actor_SetDropFlag), FUN_00375b70 (Enemy_StartFinishingBlow), FUN_0034eaf8 (Collider_DestroyQuad).
Scratch: ws/En_GeldB/tmp/t (harness: pre2.h + gen.py/mini.py/gridgen*.py), drafts in tmp/draft_*.txt.

## Stage 3 (Opus) -- near-miss pass

ws_check.sh En_GeldB: baseline only (FUN_00249af8).

| Function | Status | Note |
|---|---|---|
| EnGeldB_SetupSpinDodge | MATCHED | N64 helper `static inline void EnGeldB_SetupAction(EnGeldB*, EnGeldBActionFunc)` (added at the top of z_en_geldb.cpp) for the actionFunc store: the literal-pool load of the function address is then scheduled late (r0) instead of hoisted into ip |
| EnGeldB_Circle | NOT MATCHED, 3 words (dodge file) | `ldr r0,=40.0; vmov r1,s0` vs ours `ldr r1; vmov r0`: int-reg tie in the `> 40.0f` bit compare. Insensitive to operand order, `!(<=)`, thisx/self reads, dist local, file position, SetupAction |
| EnGeldB_Advance | NOT MATCHED, 4 words (dodge file) | same tie class in the unsigned range check `150 < x < 210` (offset literal r0 vs r1). Insensitive to operand order/sides and SetupAction |
| EnGeldB_SpinAttack | NOT MATCHED, 8 words (dodge file) | pool order (ROM: 0.0 before 6.0; needs `f32 six` for 6.0 hoist which puts 6.0 first) + swordState/speedXZ store order; any change of six placement or store order explodes (115-199 words) |
| EnGeldB_Slash | NOT MATCHED, 10 words (dodge file) | same literal/float int-reg tie at the `curFrame > 0.6f` compare (+ ABS sxth schedule), plus 2nd-block timer diffs; not attempted further (time) |
| EnGeldB_Block | NOT MATCHED, 10 words (dodge file) | unchanged (r5/r6 base/player tie); SetupAction no effect |
| EnGeldB_ReactToPlayer | NOT MATCHED | not attempted (time); SetupAction no effect |

Harness: ws/En_GeldB/tmp/o/h.py FUNC [variant.c] (DODGE=1 to compile the variant appended to z_en_geldb_dodge.cpp).
