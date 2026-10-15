
<!-- merge 2026-10-15 09:43:19 -->
# En_Fhg_Fire — G26 haiku stage

Matched (C in z_en_fhg_fire.cpp, ws_check baseline):
- EnFhgFire_Update, EnFhgFire_Destroy
- FUN_003a424c (moved from functions_3A0000s.cpp, GLOBAL_ASM line removed; writes player fields)
- FUN_003d4b98 (LightningShock; moved from functions_3C0000s.cpp)
- FUN_001a08a8 (SpearLight; moved from functions_180000s.cpp)
- FUN_003ca984 (LightningTrail; moved from functions_3C0000s.cpp)

Not touched: EnFhgFire_Init, EnFhgFire_Draw (not in group list, still GLOBAL_ASM).

Notes:
- Header: 3DS layout. Collider 0x210 (ColliderCylinder 0x58), lightNode 0x1F4, models[4] at 0x274 (Destroy), work[] 0x1A8, fwork[] 0x1B8.
- FUN_001a08a8 needed: parent pointer read into a plain Actor* local, Vector3f zero-init locals (cast to Vec3f*) inside the
  if block (so the Actor_Kill tail call is kept).
- Light context accessed as (u8*)play + 0xA70 (PlayState has no lightCtx field yet).

## G26 sonnet stage
Matched (0 words, ws_check baseline): FUN_001096cc (LightningBurst, moved from functions_100000s.cpp), FUN_00156754 (PhantomWarp, moved from functions_140000s.cpp), EnFhgFire_Init (switch on params, spear/ball/shock/burst/warp/default order matters; `thisx->world.pos.z` on dzL, `thisx->speedXZ` in the ball arm).
New: src/game/shared_syms.s gets gCustomLensFlareOn/gLensFlareScale/gLensFlareGlareStrength/gLensFlareColorIntensity/gCustomLensFlarePos (0x531EBA/C2/C4/EC, 0x5A2AD4); actor data_syms.s EQU EnFhgFire_sCylinderInit (0x5236B8). Header: zarInfo@0x270, warpAnimMode@0x284, lightInfo@0x1F8.
Not matched (drafts under #if 0, GLOBAL_ASM kept):
- FUN_003ddcc0 (LightningStrike): NEAR 2 words (sp70 vector store order), size-exact.
- EnFhgFire_Draw: NEAR 13 words (else-branch translate vector VFP numbering).
- FUN_0019fe84 (EnergyBall): FAR, 186 of ~650 insns differ (full N64 port, size 2572 vs 2596).
