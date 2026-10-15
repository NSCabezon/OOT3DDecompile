# Bg_Dodoago (Haiku stage 1) - STATUS

Actor file: `src/game/actors/Bg_Dodoago/z_bg_dodoago.cpp` (+ `.hpp`). ws_check: only baseline `FUN_00249af8` differs (non-function bytes 0 diff).

## Per function
| Function | State | Notes |
|---|---|---|
| BgDodoago_Destroy | MATCHED (C) | DynaPoly_DeleteBgActor, 3x Collider_DestroyCylinder, tail FUN_00350f34 |
| BgDodoago_Draw | MATCHED (C) | MTX34CopyAsm + SkeletonAnimationModel SetUnkAC/FUN_003721e0/FUN_00372170 |
| FUN_001832a8 (DoNothing, `bx lr`) | MATCHED, MOVED | Now defined in actor .cpp; GLOBAL_ASM line removed from `src/functions/functions_180000s.cpp` |
| BgDodoago_Init | NOT MATCHED, left as GLOBAL_ASM | C draft under `#if 0`. Matched (0 bad words) in a variant with ROM data in C, but that variant moved .data and broke 137 functions. Current variant (raw data addresses `0x510DE0..`) differs only in frame size (3DS needs `STACK_PAD`-like 4 extra bytes; ROM has `sub sp,#8`, `str r6,[sp,#4]` for colHeader) and literal reuse (`ldr r7` for the raw address instead of `ldr r3,[pc]`). Next: try a per-use raw pointer `(ColliderCylinderInit*)0x510DF0` without macro CSE. |
| BgDodoago_Update | NOT MATCHED, left as GLOBAL_ASM | C draft under `#if 0` (16 variants of reg/arg order/timer store tried, best still 69 words differ). ROM: `play` in r7, statics base in r6, zero in r5. Mine: play in r6. Bomb timer store in ROM is `add r0,r0,#0x200; strh [r0,#0x6c]` (i.e. bomb+0x26C via a 0x200-based member); mine folds to `mov r2,#0x26c; strh [r2,r0]`. Needs EnBom struct with a member at 0x200. |

## Not attempted (action functions, outside actor dir)
- `FUN_003f2fc4` (640 B, `functions_3E0000s.cpp`): BgDodoago_WaitExplosives action, calls OnePointCutscene_Init with FUN_003eead0 / FUN_0010d81c callbacks. Only referenced by this actor -> candidate to move; not done (time budget).
- `FUN_003eead0` (872 B, `functions_3E0000s.cpp`): BgDodoago_OpenJaw action (eye lighting, dust, sparkles, Math_SmoothStepToS jaw). Candidate to move.
- `FUN_0010d81c` (52 B, `functions_100000s.cpp`): BgDodoago_LightOneEye action. Candidate to move (small).
- `BgDodoago_SpawnSparkles` is inlined/out of asm; not separately tracked.

## Data
- Static data kept as `GLOBAL_ASM("data/z_Bg_Dodoago.data.s")` (0x00510DE0..0x00510E70). Referenced in C via raw-address macros (`sDisableBombCatcher`, `sTimer`, `sMainColliderCylinderInit`, `sLeftRightColliderCylinderInit`, `sInitChain`). Debt: should become real symbols.
- Putting the data in C (non-zero u32 arrays + zero statics) made the link shift: 137 functions differ. Do not do that without fixing the .data layout first.

## Facts learned (3DS vs N64)
- Struct: DynaPolyActor (0x1BC) + state s16 @0x1BC + 3x ColliderCylinder (0x58 each) @0x1C0/0x218/0x270 + actionFunc @0x2C8 + skelAnimModel @0x2CC (size 0x2D0).
- No ICHAIN culling macros in repo headers (Actor has no cullingVolume fields): init chain is raw words.
- Explosive category is `actor->type` (@0x2) on 3DS, not `category`. Bomb speed is `speedXZ`.
- Bomb catcher timer: `FRAMES(50)` = `50*3.0f/R_UPDATE_RATE + 0.5f` as s16.
- `FUN_00372f38` in include/functions.hpp is declared with 5 args and is called with 5 args here (6th/7th stack slot is the colHeader local, not an arg).
- Repo header Collider init enums (COL_MATERIAL_NONE, ELEM_MATERIAL_UNK2, AT_NONE, ...) are not defined; use raw words.

## Files touched
- `src/game/actors/Bg_Dodoago/z_bg_dodoago.cpp`, `z_bg_dodoago.hpp` (in ws only)
- `src/functions/functions_180000s.cpp` (removed GLOBAL_ASM FUN_001832a8; in ws only)
- `include/`: no changes.
