# En_Attack_Niw: cascade stage 1 (batch 1/1, Haiku executor)

Baseline check: `scripts/ws_check.sh En_Attack_Niw` -> only FUN_00249af8 differs (known).

| Function | Status | Notes |
|---|---|---|
| EnAttackNiw_Init | MATCHED (C, actor cpp) | Uses `(InitChainEntry*)0x005209a8` raw chain address (same as Actor1D9). FUN_00353e78 / ZAR_GetCMBByIndex / FUN_00205a40 declared locally. |
| EnAttackNiw_Destroy | MATCHED (C, actor cpp) | Parent-timer decrement written as nested ifs with `base + 0x600 + 0x16` (only form that matched; 3 other forms did not). |
| EnAttackNiw_Draw | MATCHED (C, actor cpp) | `SkelAnime_DrawOpa(skel, &modelMtx, FUN_00389c20, NULL, actor, 0)`. |
| FUN_001255e4 | MATCHED, moved from functions_120000s.cpp | Action fn (func_809B5C18 counterpart). On-screen check inlined as static helper. Screen limits in the ROM are -1000/1320/1240 and z < -1020 (not N64 values); the x check is one unsigned compare `(u32)(x+1000) > 2320`. |
| FUN_00389c20 | NOT MATCHED, left as GLOBAL_ASM in functions_380000s.cpp | Draft under `#if 0` in the actor cpp. Diff: the layout (rot at sp+4, mtx at sp+0x10) now matches, and so do branch structure and limb-4/6 math, but the float constants are allocated differently. ROM hoists 0.0 into s2 and copies it with `vmov s1,s2` (limb 7), and loads ±pi/32768 (`ANGLE_UNIT`) and the -pi/32768 variant into different regs. Also ROM has 2 extra insns before the limb-4 `b`. Tried ~7 variants: rot decl order, zero locals, z-first, load-first locals for limb 4. None closed the gap. Opus or a hand look at the pool order may do it. |

Attempted: EnAttackNiw_Init, EnAttackNiw_Destroy, EnAttackNiw_Draw, FUN_001255e4, FUN_00389c20.
Header: `z_en_attack_niw.hpp` now has real 3DS offsets (fields after 0x1A4 shifted; later fields at N64 offset + 0x380; size stays 0x668).
Not touched: EnAttackNiw_Update (GLOBAL_ASM, not in this batch).

## Stage 2 (Sonnet)

| Function | Status | Notes |
|---|---|---|
| FUN_00206b30 (func_809B59B0) | MATCHED, moved from functions_200000s.cpp | Gravity store before timers; zero chain `2D0=26C=268=284=27C=0` then 14000 pair; `unk_25C == (s32)FRAMES(50)` (int compare, no extra sxth). |
| FUN_00363604 (func_809B5268) | NOT MATCHED (asm stays in functions_360000s.cpp), draft under #if 0 | Bytes identical except VFP constant registers: ROM 0.0=s16, 7000=s17, -10000=s18, 0.5=s19, 9.0=s20; ours 7000=s16, -10000=s17, 0.5=s18, 0.0=s19. Needed: `FRAMES((s16)Rand_ZeroFloat(30.0f))`, `unk_268 = unk_26C = 7000.0f` chain, Approach compares written `if (target != field)` (target loaded second). Tried ternary / zero local / swapped if: worse. Pure regalloc. |
| FUN_00205a40 (func_809B5670) | NOT MATCHED, draft under #if 0 | 3DS differs from N64: "at" is eye + normalize(lookAt-eye)*160 (view eye 0x1B8, lookAt 0x1C4 in PlayState). ROM reloads eye.x/y/z from play (r6) after the sqrt/div block instead of CSE; ours keeps them in regs (968 vs 988 bytes). fabsf via `_fabsf`. |
| EnAttackNiw_Update | NOT MATCHED, draft under #if 0 | Only diff: ROM r6=play r7=player, ours swapped (14 words). Needs `thisx` for FUN_0033bd9c/Actor_MoveForward calls and signature `(Actor*, PlayState*)`. Water block chain `unk_2DC = gravity = unk_2E0 = 0.0f`. `(play2 = play)` local gives right regs but wrong prologue schedule (worse). |
| FUN_00389c20 | NOT MATCHED, draft under #if 0 | Layout fixed by declaring `MTX34 rotMtx` before `Vec3f rot`. Remaining: ROM hoists 0.0 into s2 (not s1) and stores x from a `vmov` copy of it; pool has separate -pi/32768. Size 352 vs 360. Chains/initializers did not change it. |

## Stage 3 (Opus)

| Function | Status | Notes |
|---|---|---|
| EnAttackNiw_Update | MATCHED (C, actor cpp) | `{ PlayState* play2 = play; self->actionFunc(self, play2); }` (scoped copy only at the actionFunc call) fixes r6/r7, and `shape.shadowScale = 15.0f` must come BEFORE `shape.rot = world.rot`. ws_check baseline. |
| FUN_00363604 | NOT MATCHED (asm in functions_360000s.cpp), draft #if 0 | VFP const numbering is source-sensitive but chaotic: unused `f32 dummy = 0.0f` / zero local / helper splits / literal forms / case order / own TU all tried, none put 0.0 in s16. |
| FUN_00389c20 | NOT MATCHED (asm in functions_380000s.cpp), best draft #if 0 (2 words) | Per-limb `f32 x_=a; f32 y_=b; f32 z_=c; rot.* = *_;` temps get size 360 and the ROM's batched stores. ~250 combos of decl/store order searched: the regs only come out right when limb 7 stores are z,y,x (ROM stores x,y,z). Temp `Vec3f t_; rot = t_;` and Vector3f ctor are worse. |
| FUN_00205a40 | skipped (time) | |
