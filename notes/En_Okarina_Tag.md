# En_Okarina_Tag: Opus closing pass

ws_check.sh: baseline only (FUN_00249af8). 9/9 functions are C.

| Function | Status | Key |
|---|---|---|
| EnOkarinaTag_Init | MATCHED (Opus) | `type = (params >> 10) & 0x3F` (s16 shift keeps lsl16/lsr26); ocarinaSong/switchFlag via PARAMS_GET_U; `self->actor.` everywhere; early `return` after Actor_Kill (no else) fixes the case 7/5 tail-merge |
| FUN_00274900 | MATCHED (Opus) | early-return draft + `static __inline __pure EnOkarinaTag_Fabsf` wrapper fixes VFP regs |
| FUN_00274acc | MATCHED (Opus) | read `OCARINA_MODE(play)` at each compare (no local) fixes sl/fp; `return` at end of mode==3 block + plain `if` (not else-if) for the 5..13 range puts shared tail in the else path; FUN_0034e4fc is `(f32 tempo, u32 bgmId)`; ZAR slot byte inline |
| FUN_00288d0c | MATCHED | still uses `*(volatile u16*)&self->ocarinaSong` (debt; ~8 non-volatile forms all CSE the reload) |
| others | MATCHED (earlier stages) | |

Moved out of functions_240000s.cpp: FUN_00274900, FUN_00274acc (GLOBAL_ASM lines deleted).
