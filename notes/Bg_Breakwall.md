# Bg_Breakwall STATUS (Opus closing pass, 2026-10-13) -- ws_check: baseline only
| Function | Status |
|---|---|
| BgBreakwall_Init | MATCHED (Actor* thisx signature; Flags_GetSwitch params, pos.y and unk_19B written via thisx) |
| BgBreakwall_Destroy | MATCHED (earlier) |
| BgBreakwall_Update | MATCHED (earlier) |
| FUN_002768c4 (Draw) | MATCHED, moved from functions_240000s.cpp |
| FUN_003f471c (Wait) | MATCHED, moved from functions_3E0000s.cpp |
| FUN_0015c004 (WaitForObject) | NOT MATCHED, GLOBAL_ASM in functions_140000s.cpp; draft under #if 0 (17/85 words) |
| LavaCover 0x001EA8C8, SpawnFragments FUN_00104da8 | skipped (out of scope) |
