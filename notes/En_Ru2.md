# En_Ru2 status (Haiku stage 1)

Actor: `src/game/actors/En_Ru2/z_en_ru2.cpp` (+ `z_en_ru2.hpp`, `syms.s`). Workspace: `ws/En_Ru2`.
Check: `scripts/ws_check.sh En_Ru2` -> only baseline `FUN_00249af8` differs. Done.

## Actor functions (4)
| Function | Status | Notes |
|---|---|---|
| EnRu2_Destroy | MATCHED (C) | `Collider_DestroyCylinder(state, &collider)` then `SkelAnime_Free2`, `faceAnims.Destroy()`. The ROM has the collider setup inlined (armlink), so the call is needed to get the arg setup. |
| EnRu2_Update | MATCHED (C) | Dispatch via absolute table `sEnRu2ActionFuncs` (EQU 0x0052E6A4 in syms.s), 20 entries. |
| EnRu2_Draw | MATCHED (C) | Dispatch via `sEnRu2DrawFuncs` (EQU 0x0052E6F4): DrawNothing 0x26DB78, DrawOpa 0x29529C, DrawXlu 0x283B4C. |
| EnRu2_Init | NOT MATCHED (asm, `#if 0` draft) | 528 B vs 552 B, 93/138 words differ after 7 variants (`tmp/`). See below. |

## Init attempts (7, timebox reached)
- v1: straight port (Zl2 pattern). Register r8 spilled for collider, extra push. 97/138 words off.
- v2: no skel local, `&self->skelAnime` inline. 111/138 (worse).
- v3: static inline helpers (InitWaterTrial/Credits/WaterTempleEncounter/ChamberOfSages) as an N64-style switch. 111/138.
- v4: collider local + `zarBase = NULL` in else. Compile error with duplicated helpers, fixed. Prologue then differs.
- v5: no collider local. 106/138.
- v6: shared shadowAlpha tail for types 2/3 (matches the ROM's shared `strb [r7,#0x14]`). Size 524 B, 105/138.
- v7: `ActorShape* shape` local, play before self. Size 528 B, 93/138. **Kept as the `#if 0` draft.**
Remaining mismatch: prologue register allocation (ROM push {r4-r7,lr}, play in r5, collider reg r6 reused as zar, r7 = shape ptr in the switch), and the ROM keeps FUN_00347ed4 calls and a zero reg (r6) from before the switch.
The Init 3DS flow is clear from the asm: ActorShape_Init(shape, 0, DrawCircle, 30); Collider_InitCylinder; Collider_SetCylinderType1(sCylinderInit 0x52E66C); zar from play+(objBankIndex<<7)+0x3A5C (+0x10); ZAR_GetCMBByIndex; FUN_00353e78(zar, play, skel, cmb, unk_178, -1, &unk_228, &unk_708, 0x18); SkelAnime_SetFaceAnimations(faceAnims, skel, 0, -1, -1); type = params & 0xFF: 2 crossing arms (action 7), 3 hands on hips (action 10, drawConfig 0), 4 idle (action 14, drawConfig 1) or Actor_Kill if Flags_GetSwitch(params>>8); default idle + yOffset -9984.0f. Common tail: unk_DD2 = 0, unk_DD3 = 3.

## Action functions (not in actor dir, still asm, NOT attempted in stage 1)
Limit (~15 functions) and Haiku budget. Listed for a Sonnet pass. Table order (sEnRu2ActionFuncs = N64 sActionFuncs order):
0 SetupWaterMedallionCutscene 0x26DC48 (176 B) · 1 AwaitBlueWarp 0x26DB7C (204 B) · 2 RiseThroughBlueWarp 0x22E48C (88 B) · 3 SageOfWaterDialog 0x283CC4 · 4 RaiseArms 0x2952F8 · 5 AwaitWaterMedallion 0x283BE0 · 6 FinishWaterMedallionCS 0x26DC08 · 7 WaterTrialInvisible 0x37F7E0 (596 B) · 8 WaterTrialFade 0x37F63C · 9 AwaitSpawnLightBall 0x37F87C · 10 CreditsInvisible 0x2A5F08 (240 B) · 11 CreditsFadeIn 0x2B375C · 12 CreditsVisible 0x2B3868 · 13 CreditsTurnHeadDownLeft 0x37F9C4 · 14 WaterTempleEncounterRangeCheck 0x2B3B48 (136 B) · 15 WaterTempleEncounterUnconditional 0x37FB38 · 16 WaterTempleEncounterBegin 0x271ED8 (1980 B, large) · 17 WaterTempleEncounterDialog 0x39B4D0 · 18 WaterTempleEncounterEnd 0x37FA34 (428 B) · 19 WaterTempleSwimmingUp 0x2B398C (444 B).
Draw table: DrawNothing 0x26DB78 · DrawOpa 0x29529C (172 B) · DrawXlu 0x283B4C (560 B).
Some of these are cfg-merged in functions.tsv (caseD_* names); check before moving. Also the N64 counterpart is `tools/repos/oot/src/overlays/actors/ovl_En_Ru2/z_en_ru2.c`.

## Files touched
- `src/game/actors/En_Ru2/z_en_ru2.cpp` (rewritten: Destroy/Update/Draw in C, Init GLOBAL_ASM with `#if 0` draft)
- `src/game/actors/En_Ru2/z_en_ru2.hpp` (3DS struct layout: skelAnime 0x1A4, faceAnims 0xBE8, action 0xDB8, drawConfig 0xDBC, unk_DD2/DD3, collider 0xDD8; size kept 0xE68)
- `src/game/actors/En_Ru2/syms.s` (new: EQU for action/draw tables, sCylinderInit, 3 anim headers)
- Nothing outside the actor dir. `include/` untouched. Scratch in `tmp/`.
