# Bg_Bdan_Objects: cascade stage 1, batch 1/2

Workspace: ws/Bg_Bdan_Objects. Baseline check: ws_check.sh shows only FUN_00249af8 (known).

| Function | Status | Notes |
|---|---|---|
| BgBdanObjects_DoNothing | MATCHED | empty C body, `bx lr` |
| BgBdanObjects_Update | MATCHED | `((BgBdanObjects*)thisx)->actionFunc(...)` cast form; the `self` local version swaps mov r4/r5 |
| BgBdanObjects_Destroy | MATCHED | 6-arg call to FUN_00350f34 via fn-pointer cast (4 skel ptrs at 0x220..0x22c); collider stub inlined by armlink |
| FUN_0019fde4 (WaitForSwitch) | MATCHED | moved to actor .cpp |
| FUN_0019fba8 (ChangeWaterBoxLevel) | MATCHED | moved; SFX call duplicated in both branches (armcc merges it, gives the nop); waterBox stride 0x10 via local struct |
| FUN_0019fc94 (WaitForTimerExpired) | MATCHED | moved to actor .cpp |
| FUN_00177914 (FallToLowerPos) | MATCHED | moved; cos constant is M_PI/75 (2/3 speed) |
| FUN_00177bb0 (WaitForPlayerOnTop) | NOT MATCHED | 7/29 words differ: r0/r1 swapped for the timer store addr vs value, fn-ptr load and play mov. ~16 variants tried (order permutations, locals, early return, actor ptr). Draft under #if 0 in actor .cpp; GLOBAL_ASM left in functions_140000s.cpp. |

Changes:
- actor header: BgBdanObjects now uses DynaPolyActor dyna (0x1BC), actionFunc 0x1BC, switchFlag 0x1C0, timer 0x1C2, collider 0x1C4, skelAnimModel[4] 0x220, unk_230 (struct size unchanged 0x234).
- functions_180000s.cpp: GLOBAL_ASM lines for FUN_0019fba8, FUN_0019fc94, FUN_0019fde4 removed (defined in actor .cpp).
- functions_140000s.cpp: GLOBAL_ASM line for FUN_00177914 removed.
- Open questions: unk_230 (set 1 in WaitForSwitch, 0 in WaitForTimerExpired) purpose unknown.

## Batch 2/2

| Function | Status | Notes |
|---|---|---|
| FUN_00155374 | MATCHED | moved to actor .cpp (from functions_140000s.cpp). N64 OctoPlatform_RaiseToUpperPosition; Math_SmoothStepToF(target home.y+500, 0.5, 7.5, 1.0); 0 words differ |
| FUN_0019975c | MATCHED | moved to actor .cpp (from functions_180000s.cpp). N64 ElevatorOscillate; sinf arg is timer*(M_PI/384), timer reset to 768 (2/3 speed) |
| FUN_0019a1b0 | NOT MATCHED | N64 OctoPlatform_WaitForRutoToStartCutscene. 27/82 words differ, size 312 vs 328: ROM has 2 extra `nop` after the Audio_PlayActorSound2 call, and GetProperty(NORMAL0) is materialised as movne/moveq bool at the Gameplay_InCsMode check (variants tried: bool local, bool helper, nested branch). Draft under #if 0 in actor .cpp; GLOBAL_ASM left in functions_180000s.cpp |
| FUN_001c832c | NOT MATCHED | N64 OctoPlatform_WaitForRutoToAdvanceCutscene. 13/77 words differ, size OK; all diffs are register permutation (timer base this+0x100 in r7 vs r6, play+0xa00 in r8 vs r7, quakeIndex in r6 vs r8). Variants tried: quake local scoping, camera via activeCamera, camId local, `&&` timer form. Draft under #if 0; GLOBAL_ASM left in functions_1C0000s.cpp |
| BgBdanObjects_Draw | NOT MATCHED | best draft 296 vs 312 bytes, 53/78 words differ: ROM duplicates the params==2 tail (no shared epilogue) and keeps the slot pointer in r4 for the general path; first MTX/PauseContext ordering and translate stack layout are fixed. ~12 variants tried. Draft under #if 0; GLOBAL_ASM kept |

Changes:
- header: `unk_21C` changed from `char[4]` to `s32` (cameraSetting / stage value, used by FUN_00155374, FUN_0019975c, FUN_0019a1b0, FUN_001c832c).
- actor .cpp: local prototypes added for sinf, Gameplay_InCsMode, Camera_ChangeSetting, FUN_0036762c, FUN_00367618, Quake_*, FUN_0036ae48, FUN_001c832c, FUN_00155374. No include/ edits.
- functions_140000s.cpp: GLOBAL_ASM("asm/FUN_00155374.s") removed.
- functions_180000s.cpp: GLOBAL_ASM("asm/FUN_0019975c.s") removed.
- Notes: the action pointer FUN_001998f4 (0x001998f4) is not a symbol in functions.tsv; FUN_001c832c's draft uses the raw address cast `(BgBdanObjectsActionFunc)0x001998F4` (only inside #if 0, so not linked yet). Needs a real symbol before it can be matched.

## Cascade stage 2 (Sonnet)

| Function | Status | Notes |
|---|---|---|
| BgBdanObjects_Init | MATCHED | `(Actor* thisx, PlayState*)` + `self` cast; params via `thisx->`, rest via `thisx->`/`self->` like N64 (this alone fixed the params reload / lsl-lsr order). initChain/cylinder init (0x00510A08/0x00510A10) as EQU symbols in actor `data_syms.s`. FUN_00372f38 called via 11-arg fn-pointer cast; DynaPolyInfo_Alloc takes `(GameState*)play` |
| FUN_0019a1b0 | MATCHED | moved to actor .cpp. The two nops were armcc-emitted (no issue). Tail: `bool ok = true; if (!Gameplay_InCsMode(play)) ok = (unk_21C == 1); if (ok) y = home-79-5; else y = home-79;` gives the `movne r0,#0; cmp r0,#0` materialisation |
| FUN_00177bb0 | NOT MATCHED | 4/29 words with `s16* p=&self->timer; *p=v;` setter helper (fixes the 0x1c2 offset/value regs). Left: ROM loads FUN_00177914 in r1 and `mov r0,r5` before the home.y vstr. Draft #if 0 |
| FUN_001c832c | NOT MATCHED (cfg) | 13/77, pure register permutation (quakeIndex r6 / timer base r7 / play+0xa00 r8 in ROM). Action ptr 0x001998f4 is the unsplit function after EnWallmas_JumpToCeiling (its tail bytes are data in the disasm; functions.tsv has no entry) -> needs cfg split; EQU `FUN_001998f4` in data_syms.s stands in. Draft #if 0 |
| BgBdanObjects_Draw | NOT MATCHED | size right (312) with `s16 idx` + 3x `self->skelAnimModel[idx]`; left: ROM shares one 0.0f pool word/register (vmov copy) between animSpeed and translate.x/z, ours loads 0.0f twice. Draft #if 0 |

## Cascade stage 3 (Opus)

| Function | Status | Notes |
|---|---|---|
| FUN_00177bb0 | MATCHED | moved to actor .cpp (GLOBAL_ASM removed from functions_140000s.cpp). Fix: `{ PlayState* play2 = play; self->actionFunc = FUN_00177914; OnePointCutscene_Init(play2, ...); }` (+ the s16* timer setter) |
| BgBdanObjects_Draw | NOT MATCHED | 4/78. Inline translate helper `(mtx, y, x, z)` storing x,y,z fixes 0.0f sharing + translate regs. Left: compare float reg swap (home.y s3 / 5.0f s1 in ROM). Draft #if 0 |
| FUN_001c832c | SKIPPED | cfg (FUN_001998f4 needs functions.tsv split) |
