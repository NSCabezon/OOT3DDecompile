# Obj_Blockstop - Opus closing pass: ALL MATCHED

ws_check.sh: baseline only (FUN_00249af8).

| Function | Status |
|---|---|
| ObjBlockstop_Init | matched (earlier stage) |
| ObjBlockstop_Destroy | matched (earlier stage) |
| ObjBlockstop_Update | matched: N64 if/else with two Audio_PlaySoundGeneral calls (armcc cross-jumps them; the ternary left a `nop` placeholder + wrong literal order) |
| FUN_003aa608 (N64 BgCheck_EntityLineTest2) | matched, MOVED to src/game/z_bgcheck.cpp with N64 static helper BgCheck_GetBccFlags(..., chkDyna=1) inlined. Must live outside the actor TU, else armcc inlines it into Update. |
