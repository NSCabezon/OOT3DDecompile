
<!-- merge 2026-10-14 14:59:41 -->
# Door_Warp1 (cascade stage 1, Haiku, batch 1/1)
- DoorWarp1_Destroy: NOT matched (GLOBAL_ASM, draft #if 0). 11/34 words off: loop reg numbering (ROM i=r0, zero=r3 copy; ours i=r1). Store order and env view struct tried.
- DoorWarp1_Update: NOT matched (GLOBAL_ASM, draft #if 0). 8/34 words off: ROM saves play (r5) before self (r4) and uses r1 as temp; ours always moves actor first. Tried early-return guards, play2 pattern, typed self sig.
- DoorWarp1_Draw: NOT attempted in C (structural): dispatch is a jump table; BlueCrystal body is inlined, DrawWarp=FUN_002af310 and DrawPurpleCrystal=FUN_003a0ae8 are tail calls; the repo has no gfx macros (OPEN_DISPS, POLY_XLU_DISP, gDPSetPrimColor) nor SkelAnime_Draw prototype.
- Header (z_door_warp1.hpp) left untouched: 3DS fields used via raw offsets (actionFunc 0x490, upperLight 0x494, lowerLight 0x4B0, scale f32 0x47C, env arrays in PlayState 0x31FC/0x3202/0x320A).

## Stage 2 (Sonnet)
- DoorWarp1_Update: MATCHED (0/34). `(Actor* thisx, PlayState* play2)`, `PlayState* play = play2;`, plus dead alias `PlayState* p2 = play;` used only for the FUN_00374be8 arg (found by single-site mutation search).
- Header z_door_warp1.hpp: typed (zarInfo/skelAnimModel/cmabs/actionFunc/lights/f32 scale...), size 0x4D0 kept.
- DoorWarp1_Destroy: NOT matched (11/34): ROM counter r0 + zero copy r3, ours i=r1/zero=r0; ~700 variants (types, loop forms, zero locals, env aliases, play2, GameState*) no change. Draft #if 0.
- DoorWarp1_Init: NOT matched (~67/197 words; shape and all switch cases match, ROM keeps thisx in sl + self in r4, fp/sb temps for &skelCurve per arm). Full draft #if 0 (needs EQU DoorWarp1_sInitChain=0x0051C748, ZAR_GetCSABByIndex=0x00372f0c).
- FUN_0015b904: not attempted (388 insns, 13-way jump table with undecoded case bodies = cfg tail; unknown inlined SetupX helpers).

## Stage 3 (Opus)
- DoorWarp1_Init: NOT matched, 96→28/197 words. `thisx->` for ProcessInitChain, &shape, world.pos, the 6/7 and switch params reads and unk_19A gives ROM's sl(thisx)/r4(self) split; N64-style per-arm `DoorWarp1_SetupA/B` inline helpers (SetupB with `void* u = unk_178` local) fix size. Left: armcc hoists `&skelCurve`/unk_178 above the 6/7 branch; ROM materialises them per arm into fp/sb and cross-jumps the FUN_00337200 call (+ fp in push, 0xc frame). Draft updated under #if 0.
- DoorWarp1_Destroy: NOT matched (11/34). Store order fixed (chain `ambient = light1 = fog = 0`), but i=r0/zero=r3 never moves across ~400 more variants (inline helpers w/ play/env/counter param, s32/u32 counters, zero locals at top/mid/in-loop, raw/flat/sub-struct accesses, play2, GameState*).
