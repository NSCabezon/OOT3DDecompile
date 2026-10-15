# Bg_Spot08_Bakudankabe (stage 1, Haiku) status

| Function | Status | Notes |
|---|---|---|
| BgSpot08Bakudankabe_Destroy | MATCHED (C) | 0/16 words differ |
| BgSpot08Bakudankabe_Draw | MATCHED (C) | 0/29 words differ; no NULL check on skelAnimModel (ROM has none) |
| BgSpot08Bakudankabe_Init | MATCHED (C, stage 2) | JntSph helper takes `Actor* thisx` and casts inside; `DynaPolyInfo_Alloc((DynaPolyActor*)actor, ...)` gives the r5(actor)/r4(copy) split |
| BgSpot08Bakudankabe_Update | NOT MATCHED, GLOBAL_ASM | Stage 2: draft is 10/183 words off (only s-reg numbering: 65/12 constant ROM s26, ours s21). Keys found: `s2 = self` inside the if, raw `(PlayState*)state` to CollisionCheck_SetAC, `rotationSpeed = (Rand_ZeroOne() < 0.4f) ? 65 : 33;` ternary. Draft under #if 0. ~25 variants. Stage 3 (Opus): ~35 more variants, still 10/183; finding: float s-reg numbering follows creation order of hoisted constants (statement order) — ROM has 65/12 created last (after 75/10) yet scheduled in block 1; no source shape found. Left as GLOBAL_ASM. |

Data: EQU symbols in data_syms.s (sJntSphInit 0x513880, burst positions 0x513890, sInitChain 0x5138B4). Element stride 0x50 (skel at 0x2CC).
ws_check.sh: baseline only (FUN_00249af8).
