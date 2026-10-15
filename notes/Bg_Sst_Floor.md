# Bg_Sst_Floor: status (cascade stage 1, Haiku)

Actor dir: `src/game/actors/Bg_Sst_Floor/` (z_bg_sst_floor.cpp, z_bg_sst_floor.hpp, data_syms.s)

| Function | Status | Notes |
|---|---|---|
| BgSstFloor_Init | MATCHED (0/35 words differ) | DynaPoly init, `sInitChain` via data_syms.s EQU (0x00514048). Colheader store order: `self->colHeader = (CollisionHeader*)DynaPolyInfo_Alloc(...)` before `ReadCollisionHeaderFromZsi` |
| BgSstFloor_Destroy | MATCHED (0/12) | tail call to FUN_00350f34 |
| BgSstFloor_Draw | MATCHED (0/54) | Matrix_Scale inlined as `BgSstFloor_ScaleMtx` (column scale, y = drumHeight * -0.0025f computed after MTX34CopyAsm) |
| BgSstFloor_Update | MATCHED (0/182, cascade stage 2 Sonnet) | Keys: clamp as ternary `d = (d > 350.0f) ? 350.0f : d` (fixes literal reg order); `distFromRim * 9.0f * (1.0f/350.0f)`; read `actor->yDistToPlayer` via the Actor* param (fixes r6/r7 order); rounding `n = (s32)(p > 0 ? 0.5f + ph*2.0f/3.0f : ph*2.0f/3.0f - 0.5f)`; `f32 sn = sinf(..); drumHeight = -((f32)drumAmp * sn)` (sin in own local fixes vnmul operand order). |

Struct (3DS layout, header): drumPhase 0x1BC, drumAmp 0x1BE, drumHeight 0x1C0, skelAnimModel 0x1C4, colHeader 0x1C8, size 0x1CC.
Rounding in Update: `n = (s32)(phase > 0 ? 0.5f + p2*(1/3) : 0.5f - p2*(1/3))` with `p2 = phase*2.0f`. Matches shape (predicated vmla/vnmls) but literal regs differ.
CollisionHeader in include/ has no vtxList: the actor uses a local `BgSstFloorCollHeader` view (vtxList at +0x18).

Files touched outside the actor dir: none (the workspace is an isolated copy). include/ additions: none.
ws_check.sh: baseline only (FUN_00249af8).
