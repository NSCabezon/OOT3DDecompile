
<!-- merge 2026-10-15 17:48:15 -->
# Bg_Mizu_Shutter (group G37, Sonnet pass) - status

| Function | Result | Notes |
|---|---|---|
| Update / Destroy / WaitForCutscene / Draw / WaitForTimer | MATCHED (Haiku) | |
| BgMizuShutter_Init | MATCHED (0/212) | struct fixed (maxSpeed @0x1C8, closedPos @0x1CC, openPos @0x1D8). Matrix_RotateY(new)/X/Z(apply) inlined by hand (`BgMizuShutter_RotY/X/Z`, same bodies as the ROM Matrix_Rotate* fns), `size` local for the `size == 0 || size == 1` test, N64-order `BgMizuShutter_MultVec3f(src, dest, mtx)` wrapper fixes arg setup. Data via EQUs in new data_syms.s |
| BgMizuShutter_WaitForSwitch | MATCHED (0/178) | 3DS-only MQ water temple player box + player-push block. Recipes: `Vector3f lim(500.0f, 800.0f, 100.0f)` ctor object and `local.x > -lim.x` keep the float compares unfolded (raw literals fold `x > -500` into integer compares), `s32 csId = 4510;` inside the masterQuest block with the 4511 call as `csId + 1` (pool order + `sub r1,r8,r2,asr #7`) and a literal 4510 at the final call |
| BgMizuShutter_Move | NOT MATCHED, 30 words (size equal) | draft under #if 0. Same player-push block as WaitForSwitch (matches). Remaining: the `pos == target` chains (3 x `vcmp; bne`) get if-converted (`vldreq/vcmpeq`) by armcc while the ROM keeps plain `bne` branches; ~25 forms tried (nested ifs, early returns, `&&`, Vector3f ptrs, helpers, volatile) + 3 reg words (lim numbering) |

Header (`z_bg_mizu_shutter.hpp`): corrected field offsets. New `data_syms.s` (EQUs for the data dump). Prototypes declared locally: `FUN_0034a80c`, `FUN_0032d870` (box test: pos, centre xyz, half-extents xyz), `OnePointCutscene_*`, `sinf/cosf`.
ws_check.sh: baseline only (FUN_00249af8).
