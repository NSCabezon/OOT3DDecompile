# En_Horse status (Sonnet stage 2 + Opus stage 3)
Workspace: ws/En_Horse. Actor dir: src/game/actors/En_Horse/ (z_en_horse.cpp/.hpp, data_syms.s, NEW z_en_horse_anim.cpp, NEW z_en_horse_cull.cpp).
`scripts/ws_check.sh En_Horse`: baseline only (FUN_00249af8), 0 non-function bytes. No include/ or functions_*.cpp edits.

## Matched in C: 34 / 54 (Haiku 7 + Sonnet 26 + Opus 1)
Haiku: Destroy, RotateToPoint, FUN_0033258c, StartWalking, StartReversingInterruptable, StartBraking, SetFollowAnimation.
Sonnet: StickDirection, FUN_001ff084 (Audio sfx-flag check), FUN_0031d150 (= Actor_CullingVolumeTest; moved to z_en_horse_cull.cpp, name kept),
IdleAnimSounds, Idle, Inactive, FollowPlayer, PlayIdleAnimation, ResolveCollision, ObstructMovement, MountedIdleWhinneying, MountedIdle,
MountedTurn, MountedRearing, Stopping, LowJumpInit, HighJumpInit, StartMountedIdle, StartMovingAnimation, PlayWalkingSound, LowJump,
BgCheckBridgeJumpPoint, BridgeJumpInit, BridgeJump, UpdateIngoHorseAnim, UpdateIngoRace.
Opus: Spawn (table base local `EnHorseSpawnpoint* hs = EnHorse_sHorseSpawns;` inside the loop + N64 `Math3D_Vec3f_DistXYZ` wrapper in IsSpawnBlocked).

## Not matched (drafts kept under `#if 0` + GLOBAL_ASM, reason in the `#if 0` line)
Structural (cfg split needed, C is otherwise word-identical):
- EnHorse_PlayerCanMove: ROM span = 164 B, ends with an extra `mov r0,r0` word after the pool.
- EnHorse_Frozen: ROM span ends with an extra `bx lr` (unlabeled empty fn = N64 EnHorse_Stub*).
- EnHorse_HighJump: functions.tsv span is 1344 B (extra unlabeled code merged after the pool); first 476 B identical.
- EnHorse_FleePlayer: span includes ~84 B of another function as raw bytes after the pool (not attempted).
Near misses (structure right, only register allocation / const-hoisting / scheduling differ):
- Draw (2, was 10), PostLimbDraw (2), InitHorsebackArchery (2), CutsceneUpdate (6), UpdateHorsebackArchery (18, same size),
  FUN_0037308c (10; prim/env colors look like section-anchored statics -> needs data symbols), MountedTrot (71), MountedGallop (130),
  Reverse (133, block layout), MountedWalk (175), UpdateBgCheckInfo (254), UpdateSpeed (248).
  Opus stage 3 (~45 min): per-draft notes in the `#if 0` lines. Not reached: UpdateHorsebackArchery, MountedGallop/Reverse/MountedWalk, group 3.
Not attempted / too hard: Init (guarded static loader + collider data), Update (1523 insns), OverrideLimbDraw (float range compares),
FUN_00408828 (function-local static MTX34 with guard, 0xc70 frame).

## Learned (for CLAUDE.md "Learned about 3DS code")
- `add r0,rX,#SKIN; add r0,r0,#0x3c; vldr sN,[r0]` (skin.curFrame read) = call to a tiny OUT-OF-LINE accessor that armlink inlines. Define
  `f32* EnHorse_CurFramePtr(SkelAnime*) { return &s->curFrame; }` in its own .cpp (z_en_horse_anim.cpp) and use `*EnHorse_CurFramePtr(&self->skin)`.
  The call is also a memory barrier (stops armcc forwarding `animationIdx = K` into the later header-table index, which ROM reloads with ldrb).
  The accessor does not show up in the final link (inlined + removed). Fixed LowJumpInit/HighJumpInit/StartMountedIdle/MountedIdle/Ingo race.
- Same-TU callees are NOT opaque for armcc (it knows their VFP/GPR usage): FUN_0031d150 had to move to its own .cpp or Spawn/Idle got s4 instead of s18.
  Matched C functions defined in the same file are also INLINED into later callers: put `__attribute__((noinline))` on a prototype before the caller.
- `u8 anim` parameter (callers pass an s32 without masking -> call via a cast typedef) reproduces `strb r1; ands r1,r1,#0xff` (PlayIdleAnimation/StartMovingAnimation).
- `if (!(a < b)) return;` vs nesting: ROM `bhs/bhi` after vcmpe = the true-branch is the fall-through (nest the body instead of early return) (PlayWalkingSound).
- A dead `f32 curFrame = self->curFrame;` declared after the struct copy fixes the hoisted `add r3,r4,#0xc00` (PlayWalkingSound).
- Float clamp with a memory limit: `f32 hi = X; if (v > hi) v = hi;` in its own block gives `vcmpe v,s; vmovgt` (ternary / direct member give the reversed compare).
- N64 `play2` pattern (`PlayState* play = play2;`) sometimes reduces register-permutation diffs (UpdateHorsebackArchery 24 -> 18).
- Data: 3DS tunables/tables block at 0x5265BC (s16 snap, f4..f1C floats, face table +0x20, header ptrs +0x2C, playback speeds +0x54, ...) are separate EQU
  symbols in data_syms.s. When ROM derives one table from another (`add r5,r7,#0x2c`) use one struct view (`EnHorse_sDataAll`) in THAT function only.
- Float constants like 3.6000001f = 8*0.3f*1.5f (3DS 1.5x scaling of N64 values): write the literal that gives the ROM bit pattern.
- Struct (3DS): see z_en_horse.hpp; 0xE54 stateFlags, then N64 order: lastPos E58, lastYaw E64, curRaceWaypoint E68, boostSpeed E6C, playerControlled E70,
  animationIdx E74 (u8), curFrame E78, E7C unk, unk_E80/E8C Vec3f, E98, numBoosts E9C, boostRegenTime EA0, boostTimer EA4, postDrawFunc EA8,
  followTimer EB4 (s16), prevAction EB6 (u8), riderPos EB8, EC4 u8, curStick EC8, lastStick ED0, jumpStartY ED8, colliders EDC.., playerDir FFC (u8),
  angleToPlayer 1000, followPlayerTurnSpeed 1002, waitTimer 100A, cutsceneAction 100E (u8), inRace 1014, rider 1018, ingoRaceFlags 1020, ingoHorseMaxSpeed 1024,
  hbaStarted 102C, hbaFlags 1030, hbaTimer 1034, bridgeJump* 1038..1050, unk_1088 Vec3f, unk_1094 u8 (sfx gate).
- Animation index 3DS: GALLOP 7 (N64 6), 8 = trot->gallop, 9 = fast gallop variant, 10/11 = low/high jump landing, 12/13 = low/high jump.
- (Opus) Use the N64 wrapper `Math3D_Vec3f_DistXYZ` (sys_math3d.hpp) where N64 does: the extra inline level changes VFP reg naming vs calling
  `Math_Vec3f_DistXYZ` directly (Spawn). A table base pointer local declared inside the loop body fixes `ldr base; add i*5` operand order.
- (Opus) Draw: `(EnHorse*, PlayState*)` signature + `*pos = Vector3f(m->data[0][3], m->data[1][3], m->data[2][3])` gives ROM's
  "dest addr first, then 3 vldr, then 3 vstr" shape (separate f32 locals or Vec3f temp keep loads/stores but with r0/r1 swapped).
