# En_Stream: STATUS (Opus closing pass)

All 6 functions matched; ws_check.sh = baseline only (FUN_00249af8).

| Function | State |
|---|---|
| EnStream_Init / Destroy / Update / Draw / WaitForPlayer | matched (already in oot3d/) |
| EnStream_SuckPlayer | **matched** (Opus) |

## SuckPlayer fix
- `EnStream_PlayerIsInRange` now writes `*posDifference = EnStream_VecSub(playerWorldPos, vortexWorldPos);`
  (static inline returning a Vec3f by value). The struct temporary makes armcc keep per-component load order and
  reload pos.y after the helper, as the ROM does (102 -> 22 differing words). WaitForPlayer still matches.
- `Math_FAtan2F` called through `static inline f32 EnStream_Atan(f32, f32)` wrapper -> ROM register choice (22 -> 0).
- Both are needed (Atan wrapper alone: 95 words differ).
- Only file changed: src/game/actors/En_Stream/z_en_stream.cpp. No include/ edits.
