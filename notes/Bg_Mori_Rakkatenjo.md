# Bg_Mori_Rakkatenjo — Opus closing pass
10/10 matched. ws_check: baseline only.
- BgMoriRakkatenjo_Update: MATCHED (sCamSetting as EQU symbol → 0x18A kept in reg; `(BgMoriRakkatenjo*, PlayState*)` signature fixes r5 move)
- FUN_003bc350 (Fall): MATCHED, moved to actor .cpp (fabsf via `static __inline __pure` wrapper; sBounceVel EQU symbol); GLOBAL_ASM removed from functions_3A0000s.cpp
- Raw addresses 0x5133A4/0x5133A8/0x5133B4 replaced by EQU symbols in data_syms.s
