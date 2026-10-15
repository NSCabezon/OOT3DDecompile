
<!-- merge 2026-10-14 15:50:41 -->
# En_Fr STATUS (cascade stage 1, Haiku, batch 1/4 + batch 2/4)

- MATCHED (in z_en_fr.cpp, ws_check baseline): FUN_00112fcc, FUN_002919d8, FUN_0026f2dc, FUN_00230a00, FUN_001905d4, FUN_002b6ac0
- MATCHED batch 2 (fastchk 0 words; GLOBAL_ASM removed from functions_*.cpp): FUN_0039bbcc (loop shape: literal bound, EnFr* frog local inside loop), FUN_00113698 (= N64 EnFr_DecrementBlinkTimerUpdate), FUN_00190550 (= N64 EnFr_ActivateCheckFrogSong, `u16* ev = En_Fr_sEventChkInf` read per test; the ROM base is gSaveContext+0xF00, but z3Dsave.hpp puts eventChkInf at 0xEEC, so `gSaveContext.eventChkInf[3]` links to the wrong literal; fastchk masks it, ws_check shows it)
- FAILED: FUN_002386c4 - 12 words: guard + GetModelManager() OK; vtable tail call (`ldr r0,=obj; ldr r1,[r0]; ldr r1,[r1,#0xc]; bx r1`) - armcc reloads obj into r0 after the vtable load. ~11 variants. GLOBAL_ASM (functions_200000s) + #if 0 draft. [stage 2 B: left alone]
- MATCHED (stage 2 Sonnet A, C enabled, 0 words): EnFr_Init (old stage-1 failure note dropped).
- MATCHED (stage 2 Sonnet A, C enabled, 0 words): FUN_003b3898 (old stage-1 failure note dropped).
- FAILED: FUN_003b3800 - 23 words (stage 1): armcc if-converts the float compare after `rotYRemaining == 0`; ROM keeps a real bne. GLOBAL_ASM (functions_3A0000s) + #if 0 draft (left alone in stage 2 B).
- MATCHED (stage 2 Sonnet A, C enabled, 0 words): FUN_00340b34 (old stage-1 failure note dropped).
- Debt: FUN_003b3898/FUN_00340b34 use actor-dir EQU data (En_Fr_sTimerJumpingOutOfWater 0x5238D5, En_Fr_sPitchTbl0..3 0x5238DB/E0/E5/EA); FUN_002386c4 uses En_Fr_gUnk5C1878 (0x5C1878, same address as End_Title's gUnk_005C1878); En_Fr_DecrementBlinkTimer = raw code 0x0012FFC4 (unlabeled, EQU in data_syms.s).
- MATCHED (stage 2 Sonnet A, C enabled, 0 words): EnFr_Destroy (old stage-1 failure note dropped).
- MATCHED (stage 2 Sonnet A, C enabled, 0 words): FUN_0014d56c (old stage-1 failure note dropped).
- Debt: FUN_00230a00 stores raw 0x0026F1F4 (unlabeled code, no symbol); FUN_0014d56c/raw 0x00599110 needs a data symbol.
- Header: z_en_fr.hpp EnFr now types 0x1A4 skelAnime, 0xA48 skelAnimeButterfly, 0xC04 actionFunc, 0xC08 lightNode, 0xC28 unk_C28, 0xC42 unk_C42, 0xC44 getItemId (SkelAnime = 0x84 bytes on 3DS).

# En_Fr batch 3/4 (cascade stage 1, Haiku)

- MATCHED (moved into z_en_fr.cpp, GLOBAL_ASM removed from functions_*.cpp; ws_check baseline): FUN_0026f230 (= EnFr_SetupReward-like: frog counter E4C, textId 0x40AC), FUN_00393e60 (textId 0x40A9, TRE_BOX sfx), FUN_0016c790 (= EnFr_Deactivate), FUN_001135a0 (= EnFr_ChooseJumpFromLogSpot, uses table 0x523978 LogSpotToFromWater)
- MATCHED (stage 2 Sonnet A, C enabled, 0 words): EnFr_SetReward (old stage-1 failure note dropped).
- FAILED FUN_0019062c - 10 words (= EnFr_Idle): Idle branch matches; inlined XZ-dist test compares operands in swapped regs. ~6 variants. GLOBAL_ASM (functions_180000s) + #if 0 draft. [stage 2 B: left alone]
- MATCHED (stage 2 Sonnet A, C enabled, 0 words): FUN_003811dc (old stage-1 failure note dropped).
- MATCHED (stage 2 Sonnet B, 0 words): FUN_003b36a8 = 3DS EnFr_JumpingUp-like state machine. Recipe: goto layout (`if (state==0) goto s0;` ... landing ... `return; s0: ...; goto lnd;`), shared `u8 st` set per arm + `goto set;` for the strb, extra tail block via `goto el`, `f32 yLogSpot = self->unk_C4C;` local before the sub.
- Debt: eventChkInf accessed via `gSaveContext.eventChkInf` local (ev = base, [3]); data_syms.s gained En_Fr_sUnk5238D0, En_Fr_sSongToFrog (0x523914 s32), En_Fr_sFrogSongFlags (0x523904 u16), En_Fr_sLogSpotToFromWater (0x523978), En_Fr_sOcarinaNotes (0x5238EF), En_Fr_sPtr54C8C0 (ptr var). Raw play offsets: ocarinaMode 0x2B7E, Player yaw 0x2220, Player unk_6A8 0x1740 (no typed fields in include/).
- Header: z_en_fr.hpp adds unk_C36 split (isDeactivating C38, isActive C39), unk_C3C/unk_C3D, isButterflyDrawn C64, unusedButterflyActor C60, unk_C4C (log spot Y), unk_E4C (s8), unk_C42 now s16.

# En_Fr batch 4/4 (cascade stage 1, Haiku) - last batch, 0 matched

- MATCHED (stage 2 Sonnet B, 0 words): FUN_00230a54 = EnFr_ListeningToOcarinaNotes 3DS. Recipe: `switch (masterQuestFlag) { default: <MQ switch, cases ordered 2,3,4,0,1>; break; case 0: <non-MQ switch>; break; }` (if/else gave the wrong block layout; the MQ case order decides which merged bodies are kept and in what order).
- NOT MATCHED FUN_003cebe4 (93 words, = JumpingUp 3DS; yTarget at unk_C4C+table.yDist; speedXZ 6.0f, playSpeed 0.0f, landing test vel.y < 0.0f - the stage 1 draft had wrong constants): 5 words differ, all prologue (ROM loads table base after params*3 into r0; ours hoists ldr r1,=table; ~30 variants). goto layout + `SkelAnime* sa` alias in the state-1 block match everything else. GLOBAL_ASM (functions_3C0000s) + #if 0 draft.
- MATCHED (stage 2 Sonnet B, 0 words): FUN_00389714 = EnFr_ChildSong 3DS. Recipe: reward path holds the shared tail behind a `tail:` label, the flag-set else path ends with `goto tail;` (cross-jump + nop placement), and `void (*next)(EnFr*, PlayState*) = FUN_0026f2dc;` + `u32 sfx = 0x01000487;` locals declared after the first early return (hoisted literal regs order).
- NOT MATCHED FUN_00102ccc (125 words, JumpingOutOfWater 3DS): ~9 insns / 4 bytes off after stage 2 B (goto layout, thisx alias on one zero store, actionFunc before unk_C58). Left: vec1.y stored straight from s16 and vec1.x via `vmov s0,s16` copy scheduled before the 1/0x8000 literal. GLOBAL_ASM (functions_100000s) + #if 0 draft.
- BLOCKED FUN_0034251c (110 words, engine range): callers are EnFr_Update (bl) and FUN_003cebe4 (tail b), both En_Fr; a BL-scan of the whole ROM found no other caller. Body uses a function-local static identity MTX34 behind a guard (guard 0x0055A210 / object 0x005BE29C) - the CLAUDE.md "guarded static" BLOCKER class (LOADER_RECIPE, orchestrator-only). Not drafted; GLOBAL_ASM("asm/FUN_0034251c.s") at the end of z_en_fr.cpp unchanged.
- Header: z_en_fr.hpp unk_C48 -> f32 posLogSpotX, unk_C50 -> f32 posLogSpotZ, adds unk_C54 (xz dist to log spot), unk_C58 (unusedFloat), unk_C5C pad.
- Debt: data_syms.s gained En_Fr_sSfxFreqVol (0x54AC20), En_Fr_sSfxReverb (0x54AC24), En_Fr_sJumpOrder (0x5238FC).
- Correction to FUN_00340b34 above: it is NOT a sole-caller function. FUN_00230a54 also calls it (case 1 of the ocarina switch, 5 call sites), so the "not shared" claim holds only for En_Fr's own functions.
- ws_check.sh En_Fr after batch 4: baseline only (FUN_00249af8), non-function bytes 0. Zero functions newly matched in batch 4.


# Stage 2 Sonnet B (2026-10-14)
- Matched: FUN_00230a54, FUN_00389714, FUN_003b36a8. Open: FUN_003cebe4 (5), FUN_00102ccc (~9 insns). Unattempted (no cfg tail, no guarded static; plain float-literal pools): FUN_001b09ac (Draw, 131), EnFr_Update (164), FUN_001c23a4 (222), FUN_001b0ea0 (245). FUN_0034251c: guarded static, skipped.
- Reusable: goto layout puts a state-0 block after the landing code (ROM `beq` to the end); dead `SkelAnime* sa = &self->skelAnime; sa->playSpeed = ..` alias stops if-conversion; `f32 yLogSpot = self->unk_C4C;` local fixes s1/s2 order. Float consts here: ROM s17 was 0.0f (not 1.0f) - read the pool before trusting a draft.
# Stage 3 Opus (2026-10-14)
- MATCHED FUN_00102ccc (0 words, C enabled, GLOBAL_ASM removed from functions_100000s): N64 `vec1.x = vec1.y = 0.0f;` + N64-order wrapper `EnFr_MultVec3f(src, dest, mtx)` around VEC3TransformAsm; real names Matrix_RotateY / VEC3TransformAsm.
- MATCHED FUN_002386c4 (0 words, GLOBAL_ASM removed from functions_200000s): 0x5C1878 = GetModelManager()::sInstance + 0x32C0; C-style vtable struct call `sub->vtbl->unk_0C(sub)`. Lives in its own TU `z_en_fr_mm.cpp` (in z_en_fr.cpp armcc inlined it into FUN_0014d56c). En_Fr_gUnk5C1878 EQU removed from data_syms.s.
- MATCHED FUN_003b3800 (0 words, GLOBAL_ASM removed from functions_3A0000s): `SkelAnime* sa = &self->skelAnime;` declared inside `if (rotYRemaining == 0)` and used for the curFrame/endFrame compare stops if-conversion.
- NOT MATCHED FUN_003cebe4 (5 words, prologue table-load scheduling): ~35 more variants + single-site alias mutation grid, no change. GLOBAL_ASM + #if 0 draft.
- ws_check: baseline only (FUN_00249af8), non-function bytes 0.
