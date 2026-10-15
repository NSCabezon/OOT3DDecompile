
<!-- merge 2026-10-14 19:09:49 -->
# En_Dekunuts (G11, haiku stage)

MATCHED (C, 0 words off):
- EnDekunuts_Destroy (actor .cpp). Signature (Actor*, GameState*) with PlayState* first; flower path = virtual Destroy on model (_ZTI17EnDekunutsModel EQU in syms.s).
- EnDekunuts_Draw (actor .cpp). Non-flower uses &self->actor.modelMtx and &self->actor (not thisx).
- FUN_00378aa8 (bx lr post-limb stub), moved to actor .cpp.
- FUN_001e8ac0 (SetupWait), FUN_001c82dc (SetupRun), FUN_00258b58 (SetupStand): in z_en_dekunuts_setup.cpp (own TU so armcc does not inline them into callers).
- FUN_003e0be8 (timer/gasp), FUN_001218c4, FUN_003dce00 (BeginRun), FUN_001cb604 (Burrow timer), FUN_003e1bac (Run timer): actor .cpp.
- FUN_001c6b54 (Stand), FUN_0011d56c (ThrowNut): actor .cpp.
- FUN_00176d30 (Burrow): actor .cpp.
- Link fix: Math_ApproachS in include/ is NOT FUN_00370084 (ROM symbol); use FUN_00370084 for the N64 Math_ApproachS calls.
- Class name length: _ZTI15EnDekunutsModel ("EnDekunutsModel" is 15 chars), a wrong length gave L6224E. Uses EnDekunuts_CurFramePtr from z_en_dekunuts_anim.cpp (own TU; ROM inlines the accessor as add #0x3c).

NOT MATCHED (left as GLOBAL_ASM):
- FUN_0037896c (limb override draw, limb 5 during ThrowNut): ~50 variants. Best = 3 words off, structural: ROM shares one y-copy (vmov s3,s1) in the common store block, ours adds an extra copy insn in the curFrame<=6 branch (shifts branch offsets). Draft under #if 0 in z_en_dekunuts.cpp.
- FUN_003d89c8 (EnDekunuts_Die, 90 insns; draft under #if 0 at the end of z_en_dekunuts.cpp, not compiled): uses a guarded function-local static Vec3f effectVelAndAccel (guard 0x00522028 in the actor data block, object 0x0059908C outside it). Needs a linker pin for the object (orchestrator-only, LOADER_RECIPE). Not attempted further.

Layout (3DS, from asm): actionFunc 0x1A4, playWalkSfx 0x1A8, runAwayCount 0x1A9, animFlagAndTimer 0x1AA (s16), runDirection 0x1AC, shotsPerRound 0x1AE, collider 0x1B0 (ColliderCylinder, dim.height at 0x1F4), skelAnime 0x208, jointTable 0x28C, morphTable 0x494 (inferred), model 0x69C (flower).
Data: sEnDekunutsAnimData = 0x00522000 (EQU in syms.s): word 0 = spit anim idx 0, word 2 = burrow 2, word 3 = 3 (Animation_PlayOnce in BeDamaged-like), word 6 = Up, word 8 = Stand, word 9 = Run/Gasp loop.
Animation_* take an animation INDEX (skel->zarInfo), not a pointer.
Notes: float-constant block-scoped locals (f32 morph = -5.0f inside the branch) fix pool order; FUN_003731e0 returns bool (cast to SkelAnimeUpdateFunc when the result is used).

ws_check.sh En_Dekunuts: baseline only (FUN_00249af8).
