# En_Tg — Opus closing pass (2026-10-13)

| Function | Status |
|---|---|
| EnTg_Init, EnTg_Destroy, EnTg_Draw, EnTg_OverrideLimbDraw | matched (earlier stage) |
| FUN_003ade94 (SpinIfNotTalking), FUN_001864dc (GetTextId) | matched + moved (earlier stage) |
| EnTg_PostLimbDraw | MATCHED (Opus): `Vector3f targetOffset(0,800,0)` + static inline N64-order `Matrix_MultVec3f(src, dest, mtx)` wrapper |
| FUN_0018645c (UpdateTalkState) | MATCHED + MOVED (Opus): full N64 case list (0,1,3..9 -> TALKING) gives the 3-entry jump table. GLOBAL_ASM removed from functions_180000s.cpp |
| EnTg_Update | NOT MATCHED, GLOBAL_ASM kept. Best draft 16/58 words (#if 0 in cpp). Register allocation of the this+0x800 base (r6) and float regs. |

ws_check.sh: baseline only (FUN_00249af8).
