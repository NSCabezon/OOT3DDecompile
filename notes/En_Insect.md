
<!-- merge 2026-10-15 17:00:43 -->
# En_Insect (G34, Haiku first pass) — status

Baseline: `scripts/ws_check.sh En_Insect` -> only FUN_00249af8 differs (OK).

Name map (ROM -> N64 role, by content): FUN_00352c20 SetupDig, FUN_00352b58 SetupSlowDown, FUN_00352ce8 SetupWalkOnWater, FUN_00317908 SetupRunFromPlayer, FUN_003cc0c4 Caught, FUN_003bd1ec Drown, FUN_003ba2a0 RunFromPlayer, FUN_003be100 SlowDown, FUN_003bcadc Dig, FUN_003be100->FUN_003aea04 Crawl, FUN_003bfe54 WalkOnWater, FUN_0021ea58 UpdateCrawlSfx.

| Function | Status | Notes |
|---|---|---|
| EnInsect_Destroy (19) | MATCHED | sDroppedCount is in PlayState at +0x7F5A (macro) |
| EnInsect_Draw (22) | MATCHED | sCaughtCount in PlayState at +0x7F58; GraphicsContext_UnknownStub = Gfx_SetupDL_25Opa |
| FUN_00352c20 SetupDig (41) | MATCHED | moved to z_en_insect_setup.cpp (own TU) |
| FUN_00317908 SetupRunFromPlayer (42) | MATCHED | moved to z_en_insect_setup.cpp |
| FUN_00352b58 SetupSlowDown (42) | MATCHED | moved to z_en_insect_setup.cpp |
| FUN_00352ce8 SetupWalkOnWater (45) | MATCHED | moved to z_en_insect_setup.cpp; unk_318 stored before unk_316 |
| FUN_003cc0c4 Caught (54) | MATCHED | in z_en_insect.cpp; timer<20 is `(f32)timer < 0.5+(3/R)*20` |
| FUN_0021ea58 UpdateCrawlSfx (52) | NOT MATCHED (asm + draft) | ~15 insns off: threshold select / float copy order. ~17 variants. |
| FUN_003bd1ec Drown (72) | NOT MATCHED (asm + draft) | 19 words: rot.x/rot.y step `(0.5+R/3)*500/200`, scale clamp order. Local `k` makes it worse (73). |
| FUN_003ba2a0 RunFromPlayer (116) | NOT MATCHED (asm + draft) | ~35 insns off: dist/timer compare register assignment, play in r7, add 0x600 base ordering. |
| FUN_003be100 SlowDown (118) | NOT MATCHED (asm + draft) | ~14 insns off: speed*1.2 VFP numbering, playSpeed store base (add r0,#0x244). |

Lessons: same-TU helpers get inlined by armcc (lost tail calls) -> setups moved to z_en_insect_setup.cpp. Timers: FRAMES(n)=(s16)(0.5f+(3.0f/R)*n) = EN_INSECT_FRAMES. Animation_Change_00375c08(skel, 10, 1.0f, 0, 0, 1, 0). Dig playSpeed = 1.9f*2.0f/3.0f.
Header: actionFunc 0x640, insectFlags 0x644, unk_316 0x646, unk_318 0x648, actionTimer 0x64A, lifeTimer 0x64C, crawlSoundDelay 0x64E, soilActor 0x650, unk_324 0x654, unk_328 0x658, unk_32A 0x65A (size 0x65C). Collider is opaque `char collider[0x70]` at 0x1A4 (debt: no ColliderJntSph type in ws include).
Files touched outside the actor dir: src/functions/functions_310000s.cpp (GLOBAL_ASM FUN_00317908 removed), src/functions/functions_350000s.cpp (FUN_00352b58/20c20/ce8 removed), src/functions/functions_3C0000s.cpp (FUN_003cc0c4 removed). include/: none.
New actor file: src/game/actors/En_Insect/z_en_insect_setup.cpp (needs `git add -f`, *.s rule not relevant but new .cpp is fine).


## Sonnet pass (G34)
Nothing new matched; every listed function got 40+ variants (scripts + greedy single-site mutation search); best drafts under `#if 0` in z_en_insect.cpp with the findings in comments.

| Function | Status | Gap |
|---|---|---|
| FUN_0021ea58 (UpdateCrawlSfx, 52) | NOT MATCHED, near | 9 insns: ROM hoists the 2.0f literal as s3 to the top block (ours s2, later); structure right (float select via vmovlo). |
| EnInsect_Update (183) | NOT MATCHED | 14 insns: inlined InBottleRange keeps `this` in a `mov r5,r4` copy and the player in r8 (ours: this=r4, player=r5). Dead alias `s2` fixes the zero VFP number; `thisx->` on HasParent/xzDist gives the `mov r0,r4` base. Helper taking `Actor*` gives the copy but swaps play/zero (r6/r7). |
| EnInsect_Init (277) | NOT MATCHED | 14 insns, 3 VFP-numbering clusters (lifeTimer 200.0f hoist; 0.5 copy / 10.0f literal s1<->s2 in the crawl arm). Needs data_syms.s EQUs sInitChain 0x52CEC8, sInitInsectFlags 0x52CEB0, sColliderJntSphInit 0x52CEB8 when enabled. |
| FUN_003be100 (SlowDown, 118) | NOT MATCHED, 2 words | `ldrh r1`/`strh r1` temp for `shape.rot.y = world.rot.y` after the SkelAnime update call (ours r0). |
| FUN_003ba2a0 (RunFromPlayer, 116) | NOT MATCHED | ~22 insns (XZ distance load/VFP numbering, final `&&` is a real branch in the ROM). |
| FUN_003bd1ec (Drown, 72) | NOT MATCHED | 17 insns, VFP numbering of 0.5/third copies; locals in all 120 decl orders did not help. |
| FUN_003aea04 / FUN_003bcadc / FUN_003bfe54 | not attempted | |

New reusable findings:
- playSpeed store `add r0,r4,#0x244; vstr s0,[r0,#0x10]` = block-scoped `AnimCtl* ac = (AnimCtl*)&self->skelAnime.animationType; ac->playSpeed = v;` (struct `{s32 type; char p[8]; f32 curFrame; f32 playSpeed;}` at SkelAnime+0x30).
- `{ f32* sp = &self->actor.speedXZ; Math_SmoothStepToF(sp, ...); }` fixes the prologue VFP numbering; `{ EnInsectActionFunc* pf = &self->actionFunc; *pf = F; }` fixes the r0/r1 pool-load of an action pointer.
- N64 `Math3D_Dist2DSq`-style helper with FLOAT params (`Dist2DSq(x0,z0,x1,z1)`, dx/dz temps) reproduces the "load all four, then subtract" shape (matches the soil search loop).
- Header prototypes of EnInsect_Init/Update changed to (Actor*, PlayState*) in z_en_insect.cpp (InitVars casts to ActorFunc, link unaffected).
