# En_Dy_Extra: stage 1 (Haiku-only) status

Actor dir: `src/game/actors/En_Dy_Extra/z_en_dy_extra.cpp` (+ `.hpp` struct layout). No functions moved from `functions_*.cpp` (all action fns already named `EnDyExtra_*`).

| Function | Size (ROM) | Status | Notes |
|---|---|---|---|
| EnDyExtra_Destroy | 12 B | MATCHED | tail call `FUN_00350f34(actor, &skelAnimModel, 0)` |
| EnDyExtra_WaitForTrigger | 140 B | MATCHED | fastchk 0 words differ; ws_check baseline only |
| EnDyExtra_FallAndKill | 196 B | MATCHED | fastchk 0 words differ; ws_check baseline only |
| EnDyExtra_Update | 72 B | NOT MATCHED (asm) | Draft under `#if 0`. Only 3 words differ: stores to `actor->scale` use r0 in ROM, our codegen uses r4. Tried ~7 statement-order/variable variants (timer via local, `&self->actor`, `Actor*` vs `self`); best = 3 diffs. The tail call to `Actor_MoveXZGravity` shows as `mov r0,r0` in ROM (expected). |
| EnDyExtra_Init | 236 B | NOT MATCHED (asm) | Draft under `#if 0`. Compiles to 244 B vs 236 B, ~50/59 words differ. Not iterated. Known: timer 90 (60 scaled), WaitForTrigger action, FUN_00372f38(actor, play, &skel, 2, 0) then GetCMABByIndex(2 or 3) by type, animType=1, animSpeed=2.0f. Constants from pool: scale 0.025/0.039/0.025, gravity -0.2, alpha 1.0. |
| EnDyExtra_Draw | 208 B | NOT MATCHED (asm) | No draft written (time). Uses MTX34CopyAsm(actor+0x148), PauseContext_GetState (speed = paused ? const : const), FUN_00358778 x2 (GLOBAL_ASM), a 16-byte constant copied from global 0x004D94CC, SkeletonAnimationModel::FUN_003721e0 / FUN_00372170. |

## Struct (z_en_dy_extra.hpp)
EnDyExtra: actionFunc @0x1A4, type @0x1A8 (s16, from params), startDisappearing @0x1AA (s16), timer @0x1AC (s16), alphaFac @0x1B0, scale @0x1B4, homePos @0x1C0 (= world.pos), skelAnimModel @0x1CC. Size 0x1D0 unchanged.

## Notes
- `Actor_MoveXZGravity` is declared locally (no definition in repo; only referenced by the `#if 0` Update draft).
- `FUN_00350f34` / `FUN_00372f38` declared locally in the .cpp (already in include/functions.hpp; local decl kept to match brief style).
- `include/` untouched. No files outside the actor dir touched.
