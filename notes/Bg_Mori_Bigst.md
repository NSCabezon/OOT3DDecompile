# Bg_Mori_Bigst status (Opus closing pass)
All functions MATCHED: Init, Destroy, Update, FUN_0028c230 (Draw), FUN_001105e0 (WaitForMoriTex).
FUN_001105e0: moved from functions_100000s.cpp into actor .cpp; fixed by restoring N64 static inline helpers
(SetupAction / SetupNoop / SetupDone / SetupStalfosFight). StalfosFight (unlabeled 0x0015E1DC inside FUN_0015e154)
is an EQU symbol in BgMoriBigst_data.s (pulled in via GLOBAL_ASM). ws_check: baseline only.
