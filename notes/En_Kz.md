# En_Kz (stage 1, Haiku) status

Actor dir: src/game/actors/En_Kz/z_en_kz.cpp (no files outside the actor dir touched, no include/ edits).

| Function | Status | Notes |
|---|---|---|
| EnKz_Init, EnKz_Destroy, EnKz_PreMweepWait, EnKz_SetupMweep, EnKz_Mweep, EnKz_StopMweep, EnKz_Wait, EnKz_SetupGetItem, EnKz_StartTimer, EnKz_Draw, EnKz_OverrideLimbDraw, EnKz_PostLimbDraw, EnKz_GetText, FUN_00173370 | matched (C, already in tree) | |
| EnKz_Update | matched (C, fastchk 0/242 words differ) | Was GLOBAL_ASM("asm/EnKz_Update.s"). Helpers EnKz_UpdateEyes, EnKz_GetTalkText, EnKz_UpdateTalk (static, inlined). Adult text branch: 0x40B4 case returns before the player textId store (matches ROM). Threshold 245.0f (0x43750000). |

ws_check.sh En_Kz: baseline only (FUN_00249af8).
UNMATCHED: none
