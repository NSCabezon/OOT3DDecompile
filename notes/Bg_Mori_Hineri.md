# Bg_Mori_Hineri — STATUS (Opus closing pass)

Check: `scripts/ws_check.sh Bg_Mori_Hineri` -> baseline only (FUN_00249af8).

| Function | Status |
|---|---|
| BgMoriHineri_Init | MATCHED (Opus). Fix: access params via `thisx->` in the hallway-param block, but `self->dyna.actor.params += 4` and `Actor_Kill(&self->dyna.actor)` at the end. sInitChain now defined in C (before InitVars), data GLOBAL_ASM removed. |
| BgMoriHineri_Destroy | MATCHED (earlier stage) |
| BgMoriHineri_Update | MATCHED (earlier stage) |
| FUN_00154dac | MATCHED (Opus), moved from functions_140000s.cpp. Per-case locals assigned as `idx0 = 0; obj0 = X; idx1 = 0; obj1 = Y;` (order matters). Uses GraphicsContext_UnknownStub cast for the empty Actor_SetObjectDependency (repo precedent, Bg_Haka_Megane). |
| FUN_001280fc | MATCHED (Opus), moved from functions_120000s.cpp. Fix: `Actor* thisx = &self->dyna.actor;` local; arithmetic unchanged. |
| FUN_00174e04 | MATCHED (Opus), moved from functions_140000s.cpp. Fix: `Actor* thisx` local for draw store and OnePointCutscene args. |
| FUN_00174cb0 | MATCHED (earlier stage) |
| FUN_003e7f14 | MATCHED (earlier stage) |
| FUN_001e9198 | asm: cfg-merged 32-byte tail after literal pool (needs functions.tsv split) |
| FUN_0029d22c | asm: 876-byte draw, not attempted (skipped per brief) |
