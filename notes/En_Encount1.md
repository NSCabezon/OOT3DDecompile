# En_Encount1 — Opus closing pass (2026-10-13)

| Function | Status |
|---|---|
| EnEncount1_Init / Destroy / Update | matched (already merged, untouched except field rename bigLeever@0x1C8 -> mqActor) |
| FUN_0019f354 (SpawnTektites, 384 B) | MATCHED, moved into z_en_encount1.cpp |
| FUN_001cc77c (SpawnLeevers, 768 B) | MATCHED, moved into z_en_encount1.cpp (tables via EQU data_syms.s) |
| FUN_0021bd40 (SpawnStalchildOrWolfos, 892 B) | NOT matched: 12/223 words, float const reg numbering only; `#if 0` draft in actor .cpp, GLOBAL_ASM kept |
| FUN_001c8260 | skipped (shared bx lr stub) |

ws_check.sh: baseline only (FUN_00249af8).
