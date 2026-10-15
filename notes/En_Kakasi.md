# En_Kakasi - Opus closing pass
- EnKakasi_Init / Destroy / Draw / Override / PostLimbDraw: matched (unchanged; Init now uses kaAnimRef symbol instead of raw 0x4D97A8 cast, still matches)
- EnKakasi_Update: MATCHED (DECR macro in loop + (EnKakasi*, PlayState*) signature)
- FUN_001808cc: MATCHED, moved from functions_180000s.cpp into actor .cpp (kaAnimRef EQU symbol + FUN_00353020 N64 arg order: speed, start, end, mode, morph)
- FUN_003e48f8 (talk action): not attempted (not in this pass's target list)
- ws_check: baseline only (FUN_00249af8)
