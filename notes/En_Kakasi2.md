# En_Kakasi2 — Opus closing pass
- FUN_003e1884: MATCHED (curFrame address via sub-struct at skelAnime+0x30)
- EnKakasi2_Update: MATCHED (flag -> timer=6; then `if (timer <= 0) SetAC else timer--`; SetOC)
- FUN_003e552c: MATCHED (Kk2_GetObjStatus + Kk2_InitSkel inline helpers, kk2_fabsf)
- EnKakasi2_Init: NOT MATCHED, 5/106 words (regalloc see-saw), GLOBAL_ASM + #if 0 draft
ws_check: baseline only.
