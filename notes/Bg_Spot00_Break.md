# Bg_Spot00_Break status — DONE (4/4 matched, stage 1 Haiku)

- BgSpot00Break_Init: matched (ReadCollisionHeaderFromZsi + DynaPolyInfo_Alloc per params; FUN_00372f38 7-arg call via cast; Actor_Kill if !LINK_IS_ADULT)
- BgSpot00Break_Destroy: matched (FUN_00350f34 4-arg call via cast)
- BgSpot00Break_Update: matched (empty)
- BgSpot00Break_Draw: matched (two branches on params, NULL check inside each)
- data/z_Bg_Spot00_Break.data.s: replaced by C sInitChain (ICHAIN_F32 uncullZoneScale/uncullZoneDownward/uncullZoneForward + VEC3F_DIV1000 scale), byte-identical
- No action FUN_ functions outside the actor dir; nothing moved, no include/ edits.

Notes (3DS vs N64):
- N64 `cullingVolume*` / `ICHAIN` values: 1200/1200/2000 + scale 1000 (N64 Init order matches the 3DS sInitChain).
- Params==1 selects the barbed-wire model/collision (index 1), otherwise the drawbridge (index 0). Both models are loaded in Init by FUN_00372f38.
- Tried a static inline SetColHeader helper: wrong stack shape. The real source uses ReadCollisionHeaderFromZsi (armlink --inline turns it into the str).
- ws_check: only FUN_00249af8 differs (baseline).
