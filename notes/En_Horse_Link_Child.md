
<!-- merge 2026-10-14 10:38:44 -->
# En_Horse_Link_Child: cascade stage 1 (Haiku), batch 1/1

ws_check.sh at the end: baseline only (FUN_00249af8). 

| Function | Status | Notes |
|---|---|---|
| EnHorseLinkChild_Destroy | MATCHED (C in actor .cpp) | 1 variant, exact |
| EnHorseLinkChild_Draw | MATCHED (C in actor .cpp) | (Actor*, GameState*) sig: 5 words off (regs swapped). (EnHorseLinkChild*, PlayState*) sig: exact |
| FUN_0037e568 (N64 func_80A698F4) | NOT MATCHED, draft #if 0, GLOBAL_ASM in functions_370000s.cpp | cfg-merged: functions.tsv entry 436 B includes the separate fn at 0x37e5e0 (after literal pool). First 120 B match exactly. Needs functions.tsv split. |
| FUN_0039099c (N64 func_80A699FC) | NOT MATCHED, draft #if 0, GLOBAL_ASM in functions_380000s.cpp | 2 words (0xc8/0xcc): strb/and order of animationIdx store vs table lookup. 8 variants (ternary vs if/else, store order, u8 index, newIdx lookup, cast store). |
| FUN_002874b0 (N64 OverrideLimbDraw) | NOT MATCHED, draft #if 0, GLOBAL_ASM in functions_280000s.cpp | 2 words (0x1c/0x20): ROM does add r0,r4,#0xc00 before mov r1,#0 for the FaceAnimations call; armcc hoists the constant. 8 variants. |
| FUN_001e1dfc (N64 PostDraw) | NOT MATCHED, draft #if 0, GLOBAL_ASM in functions_1C0000s.cpp | 52/63 words. ROM frame is 0x28 (pad + center + newCenter + copy), armcc gives 0x18. Struct copy, pointer, padding and array variants tried (8). |
| FUN_00348854 (anim speed helper) | NOT_ATTEMPTED (shared) | Called by En_Horse, En_Sth, En_Heishi4, En_Ma3, En_Guest, En_Js, En_GeldB, En_Hs, and FUN_00390760/FUN_0039c5e0/FUN_00292b50/FUN_003a0ffc. |

Other changes in the actor dir:
- z_en_horse_link_child.hpp: opaque char blob replaced by typed fields (skin at 0x1A8 with skelAnime at +0x10, bodyCollider, headCollider, eyeTexIndex). Size still 0xEA8.
- data_syms.s (new): EnHorseLinkChild_sAnimations = 0x0052711C, EnHorseLinkChild_sEyeIndexOrder = 0x00527108 (absolute, from the ROM literals).
- No functions_*.cpp edits (no FUN_ was matched).

## Cascade stage 2 (Sonnet), part A
| Function | Status | Notes |
|---|---|---|
| FUN_001e1dfc (PostDraw) | MATCHED (moved into actor .cpp) | Needs a member-init temp class `EnHorseLinkChildVecCopy(const Vec3f*)` + `center = *(Vec3f*)&Temp(...)`: gives the interleaved vldr/vstr temp + ldm/stm copy and the 0x28 frame. |
| FUN_00390760 (N64 func_80A6A5A4) | MATCHED (moved) | `DREG(53)` = R_EPONAS_SONG_PLAYED; new header fields timer/unk_1E8 (0xDCC/0xDD0); speed scale table EQU sSpeedScale. |
| EnHorseLinkChild_Init | MATCHED | func_80A69EC0 as static inline w/ 3 call sites; focus.pos via `thisx->`; colliders/chain data addressed as sAnimations +0x14/+0x4C/-0x10 (ROM shares one base reg); header fields unk_1F0/unk_2A0 added. |
| FUN_0039099c | NOT MATCHED, draft #if 0 | 2 words (0xc8/0xcc strb/and order); ~25 variants incl. assign-in-index, u8/u16/s16 newIdx, casts. |
| FUN_002874b0 | NOT MATCHED, draft #if 0 | 2 words (0x1c/0x20 add r0 / mov r1,#0 order); ~15 variants (typed field, locals, inline helper, folded zero). |
| EnHorseLinkChild_Update | NOT MATCHED, draft #if 0 | 3 words: eyeTexIndex=1 reg (r0 vs r1) and shared Audio tail cross-jump target; `EnHorse_CurFramePtr` (linker-inlined) needed for curFrame; clamp as `z <= -2400 ? -2400 : z`. |

## Cascade stage 2 (Sonnet), part B
| Function | Status | Notes |
|---|---|---|
| FUN_003a0ffc (N64 func_80A6A7D0) | MATCHED (moved into actor .cpp) | 3DS differs from N64: speeds 5/4/2 (not 6/4/2), RotateToPoint turn 200, extra `distFromHome > 600 -> unk_1E8 = 1` and `distFromHome > 500 -> speedXZ = 150` in the far branch. `u8 newAnimationIdx` fixes the strb/and order (also worth trying in FUN_0039099c). |
| FUN_0039c5e0 (N64 func_80A69C18) | NOT LINKABLE, draft #if 0 | Body matches 100% (716 B, `u8` idx and helper param `u8`), but functions.tsv entry is 1004 B (cfg-merged with an unreferenced fn at 0x39c8ac) -> needs functions.tsv split. 3DS: `dist > 1000 || distFromHome > 600` -> SetupWait(0); speeds 5/4/2. |
| FUN_00292b50 (N64 func_80A6A068 + func_80A69F5C/A724/A4DC inlined) | NOT MATCHED, draft #if 0 | Logic complete (EnHorse_CurFramePtr for curFrame). ~180 words off from layout: armcc moves the far-home yaw else block out of line (ROM keeps `b join`) and does not jump-thread the idle toggle. ~12 variants. |

## Cascade stage 3 (Opus)
ws_check.sh at the end: baseline only (FUN_00249af8), 0 non-function bytes.

| Function | Status | Notes |
|---|---|---|
| FUN_0039099c | MATCHED (moved; GLOBAL_ASM removed from functions_380000s.cpp) | `u8 newAnimationIdx` declared INSIDE the else block (function-scope u8 fixes strb/and but swaps s16/s17). |
| FUN_002874b0 | MATCHED (moved; GLOBAL_ASM removed from functions_280000s.cpp) | `u8 index = ...;` then `FaceAnimations* fa = (FaceAnimations*)self->unk_C00;` declared after it, `fa->FUN_0035e3a4(0, index)`, second call re-casts `self->unk_C00` -> ROM `add r0; mov r1,#0` order. |
| EnHorseLinkChild_Update | MATCHED (GLOBAL_ASM removed) | N64 func_80A6948C/func_80A693D0 as static inline helpers -> correct cross-jump target; `Collider_UpdateCylinder(thisx, ...)` (dead-alias style) -> r1 for eyeTexIndex=1. |
| FUN_00292b50 | MATCHED (moved; GLOBAL_ASM removed from functions_280000s.cpp) | N64 helpers func_80A69F5C/func_80A6A4DC/func_80A6A724 as static inlines (A724 stores speedXZ before unk_1E8); idle toggles as if/else (not ternary); distLinkFromHome via `Math_Vec3f_DistXYZ` directly (distFromHome keeps Math3D_ wrapper). |
| FUN_0037e568, FUN_0039c5e0 | SKIPPED (need functions.tsv cfg split) | drafts unchanged under #if 0. |
