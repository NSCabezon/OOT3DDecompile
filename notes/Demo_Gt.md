
<!-- merge 2026-10-14 15:48:45 -->
# Demo_Gt STATUS - Opus stage 3 (fabs pattern)

- MATCHED (fastchk 0, ws_check baseline): caseD_7_002a0fd8, caseD_8_002a1130, caseD_1_002a0e08 (C in z_demo_gt.cpp, GLOBAL_ASM lines removed from functions_2A0000s.cpp).
- fabs rule: ROM `vabs s0,s0; vmov s18,s0` = the fabsf result reaches the call through an INLINED helper's float parameter (here `DemoGt_RotateAxis(mtx, angle, axis, mode)`, a Matrix_RotateAxis-like helper); passing it directly as a call argument gives `vabs s18,s0`. The helper body (`u8 apply = (mode == 1); Vec3f* ax = axis; FUN_003625f8(apply ? &rot : mtx, ...); if (apply) FUN_0036c174(...)`) also reproduces the early `mov r5,#1` and the r1-before-r0 arg setup.
- Still asm with the same pattern: caseD_4_0037d110 / caseD_5_0037d360 (592/588 B, no draft yet; should now be reachable with DemoGt_RotateAxis), caseD_6_0037d5ac (cfg tail).
- caseD_4_002aeda4 / caseD_5_002aeea8 do NOT carry the fabs pattern (self/play callee-saved swap only); untouched.

# Demo_Gt STATUS - Sonnet stage 2 part B (0 matched)

- caseD_7_002a0fd8 / caseD_8_002a1130: down to ONE insn (344 vs 340 B). Fixed ldrsh + `mov #0x4000; sxtah; sxth` with `sp60 = (s16)(kREG(74)+0x7FEC) + 0x4000` and sp64/sp62/sp60 assigned before the GRAPH decrement. Left: ROM `vabs s0,s0; vmov s18,s0` (r0=gfxCtx survives it, so intrinsic-like, not a bl) vs ours `vabs s18,s0`. ~40 fabs variants failed (fabsf/_fabsf/__fabsf/math.h/std::, ternary, noinline same-TU, real extern call, __hardfp_fabsf, __pure/const). Same 1-insn blocker in caseD_1/4/5/6 (all share it).
- FUN_00330768: added missing accel*=scale + `&env - 1` prim trick; only `ldrd r6,r7` arg5/life pair + pos=r8 regalloc left (~15 variants).
- caseD_e_0027da2c: ROM pre-computes &unk_1CA/&unk_1CC pointers (r0/r2) at entry; helper/pointer/signature variants (12) all 82-87 words off. Left asm.
- FUN_0032a6f4 (150): new draft (dust@220 + 2 explosions), same size as ROM, ~97 words off: self/&pos regs swapped, ROM reloads env literal per call (ours CSEs into sb), frame 0x38 vs 0x3c.
- Not attempted/skipped: caseD_0_0028e95c (cfg tail: code after literal pool), DemoGt_Init (cfg tail: code after pool at _001ab344), FUN_0032a998 (7-case Vec3s packing with uninitialised ip/r2 reads), FUN_00329d0c (guarded static), caseD_5/4_0037d (blocked on fabs), FUN_003291f4.

# Demo_Gt STATUS (cascade stage 1, Haiku, batch 1/5 + batch 2/5 + batch 3/5 + batch 4/5 + batch 5/5)

Batch 5 NOT matched (0 of 2; GLOBAL_ASM kept in functions_240000s.cpp, drafts under `#if 0` in z_demo_gt.cpp):
- caseD_f_0027dbb0 (N64 DemoGt_Update15 shape, ADJUST(154)): 31/98 words off after ~10 variants; pDir/pSpeed pointer regs swapped at entry (ROM r2=&unk_1CC, r0=&unk_1CA). Built 388 B vs ROM 392 B: the last word is a dead `bx lr` at 0x27dd34 after the literal pool (cfg tail).
- caseD_8_0027d884 (F280 + speed + cue ch1 + FUN_0032a6f4 + sfx 0x263 + seq 13 at ADJUST(527)): 33/106 words off after ~7 variants; ROM loads the 10.0f pool constant into two regs, speed constants unresolved (kREG(64)*10 variant was worse).

Batch 4 NOT matched (0 of 5; GLOBAL_ASM kept in functions_*.cpp, drafts under `#if 0` in z_demo_gt.cpp; ws_check baseline only):
- caseD_7_002a0fd8 (N64 DemoGt_Draw7, unk_210[1], 54/86 words off): ROM computes fabs(sp78) before the sp60 add and GRAPH decrement, ours after; ROM keeps `ldrsh` on kREG(74) where ours is `ldrh`; sxtah(r1,#0x4000,r1) in ROM vs add+sxth in ours (one insn short). ~10 variants.
- caseD_8_002a1130 (N64 DemoGt_Draw8, unk_210[2]): same shape and same 54-word diff as caseD_7. ~3 variants.
- caseD_1_002a0e08 (Draw1-shape, two models unk_200[0..1], 53/90 words off): prologue regs match; only diff is ROM `vabs s0,s0; vmov s18,s0` (fabs then copy) vs ours direct `vabs s18`, which is one insn short. `mov r5,#1` hoist also differs. ~8 variants.
- FUN_0032aee0 (N64 func_8097F280 shape, ADJUST 160/170, 4/96 words off): only the 480.0f const and SREG(30) take swapped s0/s1 in the ADJUST divide (ROM const in s0). Tried ADJUST macro, literal 480, local num/rate, operand swaps. Matched structure otherwise; header gained `unk_1E0[3]`.
- caseD_e_0027da2c (N64 func_80981D20 + cue ch7 + E824(7) + sfx ADJUST(183)): rounding is predicated vnmlsle/vmlagt as ROM (OK); still off: prologue self/play order (needs `(Actor* thisx, PlayState* play2)`, now set), temp read ldrsh vs ldrh, `ldr r6` gGameInfo/play reg order. Header gained `unk_1CC` as s16.
- Debt/notes: the ROM 2/3 speed step in caseD_e is `unk_1CA += (s32)(unk_1CC*2.0f/3.0f +/- 0.5f)` (fastmath turns /3 into *0.3333), sign of unk_1CC picks the branch.

Batch 3 matched (0 words differ in fastchk; ws_check baseline only):
- FUN_0032ae1c (cue lerp, moved from functions_320000s.cpp; float loads must be per-field locals, not Vec3f struct copy)
- FUN_003308a4 (explosion + 6-entry sfx pick; sfx table is ROM rodata EQU `Demo_Gt_sSfxIds` 0x4D869C, copied by value; `Vector3f` ctor for zero vectors; s16 scale computed before the spawn call)
- FUN_0032a5d0 (env colour, N64 func_8097FDDC; `unk_1D0`/`unk_1F0` fields added to DemoGt in z_demo_gt.hpp, `unk_1CA` s16 added too)

Batch 3 not matched (GLOBAL_ASM kept in functions_*.cpp, C draft under `#if 0` in z_demo_gt.cpp):
- caseD_4_002aeda4 (38/65 words off, best): self/play callee-saved swap at entry; a csCtx pointer local moves the csCtx base reg and reshuffles the prologue (variants with thisx, play2, block-scoped play2, csCtx pointer, frames local tried, ~12).
- caseD_5_002aeea8 (37/65 words off, best): same shape as caseD_4 (cue 6, frame 845, modes 13/18). Only ~3 variants, mirrored from caseD_4.
- FUN_00330768 (66/79 words off): N64 func_8097D7D8 with DemoGt_SpawnDust inlined. Prologue reg numbering: ROM pos=r8, arg5=r6, life=r7 via `ldrd`; ours pos=r7. Life as s32 made it worse (58 -> no; reverted). ~5 variants.
- caseD_6_0037d5ac (cfg tail, 55/245 words off): functions.tsv says 980 B but the real head is ~0x13C B; the rest is unrelated code after the pop, so a whole-function match needs a cfg split (orchestrator task). Head draft (N64 DemoGt_Draw6-like, `unk_210[0]` model) under `#if 0`, pool offsets differ by 8 B.

Matched (fastchk 0 words differ; ws_check baseline only FUN_00249af8):
- DemoGt_Update, DemoGt_Draw (dispatch via `data_syms.s` EQU tables 0x51BBB0 / 0x51BBFC)
- caseD_a_003291c4, caseD_9_00329cd0 (moved from functions_320000s.cpp)
- caseD_2_002a0f70, caseD_3_002a0fa4 (moved from functions_2A0000s.cpp)
- caseD_2_0028ee64, caseD_1_0028ee04 (moved from functions_280000s.cpp)
- batch 2: DemoGt_Destroy (in actor .cpp, 9-arg FUN_00350f34 call via fn-pointer cast), caseD_b_002a1288 (moved from functions_2A0000s.cpp), FUN_003430fc (in actor .cpp; only caller is DemoGt_Init, not shared; `DemoGt_CollisionHeaderGetVirtual` lives in new `z_demo_gt_colhdr.cpp` so armlink inlines it with the ROM stack-slot shape)

Not matched (batch 2, GLOBAL_ASM kept in functions_*.cpp, C draft under `#if 0` in z_demo_gt.cpp):
- caseD_c_002a12f8 (13 words): only diff is r0/r1 swap of the two literal address loads (gGameInfo vs csCtx frames offset); tried compare flip, target local, play2/thisx signatures, self/play alias, inline SREG, block alias.
- caseD_d_002a13a0: same 13-word swap, plus cfg tail: ROM size 172, body 168, last word 0xea021642 is a branch after the literal pool.
- caseD_7_0028ef90 (15 words) and caseD_6_0028eebc (15 words): self/play callee-saved swap at entry (ROM `mov r7,self; mov r6,play`); ~5 variants.
- caseD_3_002aecd8 (8 words): self/play swap at entry; cue logic matches (`cue->id==2` -> 11 else `id==3` -> 16, two stores not merged). ~8 variants.

Debt:
- Cutscene cue lookup reads `play->csCtx.npcActions[ch]` (same offset as `actorCues[ch]`, 0x44). The repo `CutsceneContext` has no actorCues field; a real field would belong in include/z3D.hpp.
- Dispatch tables are EQU symbols in data_syms.s (data chunk z_Demo_Gt.data has no labels).
- Callees named FUN_0032a5d0 / FUN_0032ae1c / FUN_0032a998 / FUN_00329d0c / FUN_003291f4 are declared locally in z_demo_gt.cpp (N64 func_8097FDDC / func_8097E744 / func_8097E824 / func_8097FD70 / func_80980C90).
