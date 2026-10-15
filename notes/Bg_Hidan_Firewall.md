# Bg_Hidan_Firewall — Opus closing pass

All 7 functions matched (C). ws_check.sh: baseline only (FUN_00249af8).

| Function | Status |
|---|---|
| BgHidanFirewall_Init / Destroy / Wait / Countdown / Erupt / Draw | matched (already in main tree) |
| BgHidanFirewall_Update | matched (Opus closing pass) |

Update fix: (1) `Vec3f playerRelativePos` scoped to an inner block that ends before
SetAT/SetOC/FUN_00373264 -> armcc emits the tail call `b FUN_00373264` + separate epilogue;
(2) signature `(BgHidanFirewall* self, PlayState* play)` (cast to ActorFunc in InitVars) fixed
the last 3-word register swap in the +70 clamp compare.
