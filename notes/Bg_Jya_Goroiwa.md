# Bg_Jya_Goroiwa — Opus closing pass

ws_check.sh: baseline only (FUN_00249af8). 7/7 matched.

| Function | Status |
|---|---|
| BgJyaGoroiwa_Init | matched (now uses EQU data symbols from data_syms.s, no raw addresses) |
| BgJyaGoroiwa_Destroy | matched |
| BgJyaGoroiwa_Update | matched (Opus): rotation written inline with `f32 x = pos.x; f32 xDiff = x - prevPos.x; rot.z -= K * xDiff; checkPos.x = x;` |
| BgJyaGoroiwa_Draw | matched |
| FUN_00144638 (SetupMove) | matched |
| FUN_003bf308 (Wait) | matched |
| FUN_003c1124 (Move) | matched (Opus), moved from functions_3C0000s.cpp into actor .cpp |
