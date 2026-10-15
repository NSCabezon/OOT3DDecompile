
<!-- merge 2026-10-14 18:04:34 -->
# En_Heishi3 (G5, haiku stage)
All 12 listed functions MATCHED (ws_check baseline OK).
- EnHeishi3_Init, _Destroy, _Update, _Draw, _OverrideLimbDraw, _CatchStart, _ResetAnimationToIdle, _SetupGuardType, _StandSentinelInGrounds, _StandSentinelInCastle: in z_en_heishi3.cpp.
- FUN_0010a998 (respawn, N64 func_80A55D00) and FUN_00107498 (catch-walk, N64 func_80A55BD4): moved from src/functions/functions_100000s.cpp into z_en_heishi3.cpp (GLOBAL_ASM lines removed).
- Notes: SetupGuardType/CatchStart use index-based Animation_GetLastFrame/Animation_Change_00375c08 (3DS). sPlayerCaught lives at PlayState+0x7FC4 (raw). Player flag 0x20000000 at +0x1710 gates the sentinel-in-grounds catch. SaveContext nextTransitionType is raw at +0x15AB. Data: data_syms.s EQU En_Heishi3_sCylinderInit = 0x0052630C.
