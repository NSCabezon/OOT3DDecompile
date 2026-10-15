
<!-- merge 2026-10-15 00:27:22 -->
# En_Reeba (G22, haiku stage) status

Matched (C in src/game/actors/En_Reeba/z_en_reeba.cpp, GLOBAL_ASM removed from functions_*.cpp):
- FUN_00287980 (empty stub), FUN_00299348, FUN_001754b0, FUN_001ca60c, FUN_0021c0bc, FUN_001c7c90,
  FUN_00174660, FUN_00154564, FUN_003de24c, FUN_003d6118, FUN_0021d4e8, FUN_001747a4 (head only after split)
- EnReeba_Destroy, EnReeba_Draw

Split applied: FUN_001747a4 at 0x001748C4 -> FUN_001748c4 (48 B tail, cfg tail after literal pool).

Not matched (GLOBAL_ASM left, draft under #if 0 in the actor .cpp):
- EnReeba_Init: 64/117 words differ (register allocation of play/self, base regs r4/r6, first stores).
  Draft uses N64 shape; 3DS gravity/naviEnemyId/targetMode/focus order matched by statement order only.
- FUN_0011ff28: 5/84 words differ. Tail reads unk_498/unk_499 via r5 (self+0x400) in ROM, we use r4.
- FUN_003d4cb0: 9/112 words differ. Zero-init VFP, Math_ApproachZeroF(const,const) gives 2 loads in ROM,
  literal pool order/size off by one word (ROM 448 B, ours 444 B).
- FUN_00181394 (SetupSurface): 52/73 words differ. Timer tail (round(A*3/2) then /3 via 0x55555556) not understood.

Debt / notes:
- Raw addresses: FUN_00174660/FUN_001c7c90 (0x4D9B88 anim), FUN_0021c0bc (0x4D9B84), FUN_00154564 path,
  Draw (0x287978 override limb = mid-function label inside FUN_00287938, 0x4D9B8C color table),
  Init (sCylinderInit 0x52E2CC, sDamageTable 0x52E2AC).
- Struct: z_en_reeba.hpp now 3DS layout (SkelAnime at 0x1A4, action fields at 0x4A0+, collider at 0x4C4, size 0x51C).
- Raw offsets in EnReeba_Destroy/FUN_003d4cb0 for EnEncount1 spawner fields (+0x1AA, +0x1BC, +0x1C4, +0x1B6).
- Declared locally: FUN_0034c3e4, FUN_00353020, FUN_0035ea34, FUN_0036f00c, FUN_003687a8, FUN_003589cc,
  FUN_00358964, FUN_00375b70, EffectSsEnIce_SpawnFlyingVec3f, EffectSsDeadDb_Spawn (Vector3f*), _fabsf, Actor_SetColorFilter.


## Sonnet stage (G2122)
- MATCHED: EnReeba_Init (typed `(EnReeba* self, PlayState* play)` signature, `thisx->gravity`, `(u16)` type via u16 field, `ChangeType(.., thisx, 5)`, ActorShape_Init arg = self->yOffsetTarget; sCylinderInit/sDamageTable are EQUs in new data_syms.s), FUN_003d4cb0 (ApproachZeroF(&scale, 0.1f, 0.01f)), FUN_00181394 (timer = ((TX>0 ? (s32)(0.5f+(TX*3)*0.5f) : (s32)((TX*3)*0.5f-0.5f)))/3 with TX = 20 - (s16)fabsf(speed)*2 written out 3 times; pos.y before flags).
- NOT matched: EnReeba_Update (draft under #if 0; stream identical to ROM, 35 words = r7/r8 swap of play vs FUN_00299348 literal). FUN_0011ff28 (5 words: ROM reads unk_499/unk_498 via the self+0x400 base r5 but the first unk_498 test via r4; ~30 variants incl. s2 alias, typed Hi* view, raw u8 offsets).
- Update tricks: stunType=0 BEFORE the rot stores (else armcc forwards the constant), hitPos as `Vector3f hitPos(hp->x,hp->y,hp->z)` after acFlags clear, hitPos scoped inside the AC_HIT block (tail call to CollisionCheck_SetAT), `s2->actionfunc` for the Damaged setup + FUN_00154564 compare, focus.y arms via `thisx->`/`s2->`.
- hpp: `type` is u16 now.
