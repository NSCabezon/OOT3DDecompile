# Bg_Haka_Water: status (Haiku stage 1)

| Function | Status | Notes |
|---|---|---|
| BgHakaWater_Destroy | matched (C) | tail call FUN_00350f34 with &skelAnimModel, &skelAnimModel2, 0 |
| BgHakaWater_Update | matched (C) | `self->actionFunc(self, play)` |
| BgHakaWater_Init | NOT matched, GLOBAL_ASM (draft in `#if 0`) | 25/90 words differ at best; size 356 vs 360. Open: second CMAB call register temp (r2) and water-loop constant register (r1 vs r0). Local InitChainEntry array matches ROM (chain copied to stack). |
| BgHakaWater_Draw | NOT attempted, GLOBAL_ASM | 648 B, float-heavy, uses 3DS draw helper FUN_003695cc (prototype unknown) |

Header: `z_bg_haka_water.hpp` now has actionFunc @0x1A4, isLowered @0x1A8, skelAnimModel @0x1AC, skelAnimModel2 @0x1B0 (size 0x1C0).
Debt: repo `WaterBox` (z3Dbgcheck.hpp) is 4 bytes; 3DS entries are 0x10 stride. Worked around with local `BgHakaWaterBox` in the actor cpp (no include/ edit).

## Stage 2 (Sonnet)
- BgHakaWater_Init: still asm. Calling the 2nd FUN_00372d94 inline (no skel2 local) fixes the r6/r7 allocation; the only structural diff left is ROM `ldr r2,[model2]; mov r1,r0; ldr r2,[r2,#0xc]; mov r0,r2` after the 2nd GetCMABByIndex (+4 B) and the -8 const in r1. ~20 variants (locals, helpers, arg order) all give mine's `mov r1,r0; ldr r0..` shape.
- BgHakaWater_Draw: draft in `#if 0`: prototype `FUN_003695cc(model, idx, 4, 0, r, g, b, a)` (functions.hpp), 2nd model called with idx 0 and 1. Matrix = identity + translation (0,92,-1680) as u32 word stores, columns scaled by 0.1. 640 vs 648 B, 109/162 words differ (VFP reg numbering s18-s20 + matrix block schedule). Left as asm.

## Stage 3 (Opus)
- BgHakaWater_Init: still asm. Found what produces the `ldr r2,[self+off]; mov r1,r0; ldr r2,[r2,#0xc]; mov r0,r2` shape:
  it appears on EVERY CMAB call in the function when the register holding self IS the incoming parameter
  vreg (i.e. the `Actor* actor` param is used again after the calls, e.g. `Flags_GetSwitch(play, actor->params)`,
  or the signature is `(Self* self, PlayState*)`). When only the cast local `self` is used after the cast it
  becomes a copy vreg and every call gets the normal `mov r1,r0; ldr r0,..` shape.
  With `actor->params` the 2nd call + the -8/r1 loop constant match, but the 1st call also turns into the r2 shape
  (364 B). ROM wants mixed (normal on 1st call where zar stays live, r2 on the last). No source shape found for the
  mixed case (~40 variants: helpers, cmab locals, actor/self per access, N64 LowerWater helper). Best: 9 words diff
  at 360 B with `static inline HM(SkeletonAnimationModel* m, void* c)` for block 1 + `actor->params` (block 1 then
  preloads the model into r6). Experiments in tmp/o/.
- BgHakaWater_Draw: not attempted this stage (time).
