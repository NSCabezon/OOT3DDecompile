# Bg_Spot18_Shutter — Opus closing pass

ws_check: baseline only (FUN_00249af8).

| Function | Status |
|---|---|
| BgSpot18Shutter_Init | MATCHED. Raise path written as `actor->world.pos.y += 180.0f; self->actionFunc = DoNothing;` (pos via `actor`, not `self->dyna.actor`, else armcc sinks the actionFunc store into the slide path). Init chain now C (`sInitChain`, ICHAIN_VEC3F_DIV1000(scale, 100, STOP)) defined AFTER InitVars; data GLOBAL_ASM removed. |
| FUN_001995ec | MATCHED, moved from functions_180000s.cpp. `_fabsf` via a `static __inline __pure` wrapper (same trick as Bg_Bom_Guard). |
| FUN_00199688 | NOT MATCHED (skipped): asm entry contains block at 0x199700 referenced by other actors; needs functions.tsv split. |
| others | matched earlier (Destroy, Update, Draw, DoNothing, FUN_00175458, FUN_00138560). |
