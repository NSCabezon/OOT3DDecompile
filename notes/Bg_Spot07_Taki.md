# Bg_Spot07_Taki — Stage 1 (Haiku) status

ws_check.sh: only baseline FUN_00249af8 differs (checked on final tree).

| Function | State | Notes |
|---|---|---|
| BgSpot07Taki_Destroy | MATCHED (C) | DynaPoly_DeleteBgActor + FUN_00350f34 (8-arg call via local `__asm("FUN_00350f34")` prototype). fastchk 0/20 words differ. |
| BgSpot07Taki_Update | MATCHED (C) | `actionFunc(self, play)`. fastchk 0/2. |
| BgSpot07Taki_DoNothing | MATCHED (C) | empty (`bx lr`). fastchk 0/1. |
| BgSpot07Taki_Init | NOT MATCHED, asm kept | C draft under `#if 0`. Full C compiles, but 79/130 words differ, size 564 vs 520. Remaining diffs: (1) ROM predicates `vstreq`+`bleq` on the `0x54C8CC` gate, armcc emits branches; (2) `GetCMABByIndex` -> `FUN_00372d94` call for model 0x1C0 hoists the `ldr r2,[r2,#0xc]` load (same OPEN PROBLEM as Bg_Spot03_Taki Init); (3) float reg assignment for the 3 frame values. Tried: local cmab var, pointer to 0x54C8CC, split predicated statements (worse, 600 B), frame locals in ROM order. |
| BgSpot07Taki_Draw | NOT MATCHED, asm kept | C draft under `#if 0`. 82/114 words differ, size 440 vs 456. ROM keeps the gSaveContext pointer in r6 and the mtx at sp+0; armcc does not reproduce that. Tried: decl order of mtx/speed, direct gSaveContext.linkAge read. |

## Layout (3DS, from asm)
- bgId 0x1A4 (DynaPolyActor), actionFunc 0x1BC, six SkeletonAnimationModel* at 0x1C0..0x1D4 (FUN_00372f38 fills them with idx 0..5). sizeof 0x1D8.
- Frame cache: PlayState+0x7C00+0x380 (3 floats). Read in Init, written in Draw. Raw offsets.
- sInitChain at 0x005137CC lives in the GLOBAL_ASM data block (data/z_Bg_Spot07_Taki.data.s). Init references it through raw address.

## Debt
- FUN_00372f38 (15-arg call: 6 (model,idx) pairs + 0) and FUN_00350f34 (8-arg call) are declared locally with `__asm` labels; include/functions.hpp prototypes are truncated.
- FUN_003586ec called with unk_0C, no prototype in include/. Declared locally.
- Global 0x0054C8CC and PlayState frame cache are raw addresses.
- Draw path uses `LINK_IS_ADULT` (gSaveContext.linkAge == 0).

## Files touched
- ws/Bg_Spot07_Taki/src/game/actors/Bg_Spot07_Taki/z_bg_spot07_taki.cpp
- ws/Bg_Spot07_Taki/src/game/actors/Bg_Spot07_Taki/z_bg_spot07_taki.hpp
- No edits outside the actor dir. No include/ edits. Nothing written under oot3d/.

## Stage 2 (Sonnet)
- Draw: C draft (under #if 0) now 8/114 words off (was 82): ROM order is `adult? {m2|m4}` then `child? {m0|m1 +speed; return}` then `{m3|m5 +speed}`, `speed = 1.0f; if (Pause) speed = 0` AFTER MTX34CopyAsm. Remaining diff = prologue scheduling only (ROM loads m0 into r0 after `cmp`, armcc hoists `ldr r2` before; add r0/ldr r6 order). Tried ~10 variants (locals, play/state, ternary, cache ptr, paused local).
- Init: draft 528 B vs 520. Gate predication (`ldr r1,[r8]; cmp; vstreq; bleq`) now matches by caching `p = model->unk_0C` in a block before the `if` and using EQU symbols (data_syms.s: BgSpot07Taki_gUnk54C8CC, BgSpot07Taki_sInitChain). Remaining: GetCMAB hoist (open problem, all 3 calls hoist; ROM only the 3rd), s17/s18 swap, r6/r8 swap.
- Both stay GLOBAL_ASM; drafts under #if 0. data_syms.s added in actor dir (symbols only used by draft).

## Stage 3 (Opus)
- BgSpot07Taki_Draw: MATCHED (C). Fix for the prologue scheduling: read model 0's anim pointer into a block-scoped local
  `{ SkeletonAnimationModel_unk_0C* anim0 = self->skelAnimModel[0]->unk_0C; SPOT07_FRAME(play, 0) = *(f32*)&anim0->curFrame; }`
  (model 1's store stays inline). fastchk 0/114; ws_check baseline only.
- BgSpot07Taki_Init: still GLOBAL_ASM. Best draft (in `#if 0`): 524 B vs 520, 61/130 words. `(Actor* thisx)` signature but
  `self->actor` everywhere (any later `thisx` use => every CMAB call hoists) + N64-style static inline
  `Spot07_SetupAnim(SkeletonAnimationModel** pm, ZARInfo*, s32 i, f32 frame)` fixes call 1 and the r6/r7/r8 allocation.
  Left: call 2 still hoists `ldr r2` (ROM: only call 3), and frame1/frame2 land in s18/s17 (ROM s17/s18).
  Tried with no effect: frame decl/read order, f32[3], Vec3f copy, cache pointer, play vs state, gSaveContext direct.
