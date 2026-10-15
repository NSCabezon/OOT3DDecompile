
<!-- merge 2026-10-15 16:38:56 -->
# En_Fire_Rock (G33, Haiku + Sonnet passes)

- FUN_003a30b8 (Actor_SetPlayerKnockbackSmall: play, actor, yaw, type, speed, yVel): MATCHED (Haiku). Now lives in its own TU
  `z_en_fire_rock_knockback.cpp` (same file inlined it into Update; ROM tail-calls it).
- EnFireRock_Destroy, FUN_0010cb10 (SpawnMoreBrokenPieces): MATCHED (Haiku).
- EnFireRock_Update: MATCHED (Sonnet, 0/157). Tricks: second GET_PLAYER read written separately, block-scoped `PlayState* play2` for
  Actor_UpdateBgCheckInfo, `Collider* col = &collider.base` for the AT_BOUNCED clear, thisx->/self->actor. mix on shadowScale/gravity,
  speedXZ stored before velocity.y. Header filled in (angularVelocity, rockRotation, actionFunc, relativePos, timers, flameTimer 0x1E7).
- FUN_003eda98 (EnFireRock_Fall): MATCHED (Sonnet, 0/206), moved from functions_3E0000s.cpp (GLOBAL_ASM line deleted there).
  3DS: flame spawn gated by `DECR(flameTimer)` (u8 at 0x1E7), landing spawns 2 flames (N64 5), extra EffectSsEnFire arg by sceneNum
  (0xE/0xF/0x1A -> 2 else 1), no BROKEN_PIECE1 sfx; `play2` alias on the GET_PLAYER read.
- EnFireRock_Draw: MATCHED (Sonnet, 0/179). MTX34_MakeTrans + inline X/Y/Z rotations (angle != 0 skip) + elementwise scale; SetUnkAC(1) in r5 via an
  `FRV` vector with `operator[]` inside `FR_Trans(m, actor, rel)` (CLAUDE.md SetUnkAC recipe), locals `y,z,x` declared in that order and
  computed x,y,z; `zero`, `deg` f32 locals (declared zero,deg; assigned zero,deg) for the s17/s18 numbering; scale in sx,sy,sz locals.
- EnFireRock_Init: NOT MATCHED, 36/238 words off, GLOBAL_ASM + draft under #if 0. Structure, jump table and pool order match; only the
  hoisted-constant VFP numbering differs (ROM s18=0.01 s19=0.02 s20=65535 s21=3 s22=4 s23=1 s24=2; ours rotated; locals-for-constants variants
  made it worse, 60-75). Draft needs EQUs in data_syms.s (collider inits at 0x523710/0x523748). Two actions still asm and not in the list:
  FUN_001e7cd8 (WaitSpawnRocksFromCeiling), FUN_0019af78 (WaitOnFloor).
- ws_check.sh En_Fire_Rock: baseline only (FUN_00249af8).
