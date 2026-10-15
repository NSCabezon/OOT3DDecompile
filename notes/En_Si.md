# En_Si - Opus closing pass
| Function | State |
|---|---|
| EnSi_Destroy / EnSi_Update / EnSi_Draw / FUN_003d0544 | matched (previous stages) |
| FUN_003adc80 (idle) | MATCHED, moved to z_en_si.cpp (GLOBAL_ASM removed from functions_3A0000s.cpp) |
| FUN_003ad218 (hookshot) | MATCHED, moved to z_en_si.cpp (GLOBAL_ASM removed from functions_3A0000s.cpp) |
| EnSi_Init | NOT MATCHED - asm. Inlined singleton accessor: guard 0x0055A21C, object 0x005BE5B8 (ctor FUN_0036788c, __aeabi_atexit dtor + __dso_handle). Needs real shared data symbols / linker pinning outside the actor dir (skipped per brief). |
ws_check: baseline only.
