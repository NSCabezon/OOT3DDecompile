
<!-- merge 2026-10-14 18:05:30 -->
# En_Encount2 (G5, haiku stage)
- EnEncount2_Init: MATCHED (dead `s32 pad;` local reproduces the ROM's 8-byte stack pad, frame 0x80).
- EnEncount2_Destroy: MATCHED (tail call FUN_0034fda8(actor, 30, models)).
- FUN_003f4210 (action = 3DS EnEncount2_Wait): MATCHED, moved into z_en_encount2.cpp (GLOBAL_ASM removed from src/functions/functions_3E0000s.cpp). Quake helpers declared locally. Its action pointer FUN_003c1924 (SpawnRocks) is out of scope, declared only.
- EnEncount2_Update / Draw: untouched (not in the list).
