# En_Diving_Game: STATUS (stage 2, Sonnet) - ALL MATCHED

| Function | Status | Notes |
|---|---|---|
| FUN_00239714 (Reset) | MATCHED | stage 1 |
| EnDivingGame_Init | MATCHED 83/83 | `Actor_Kill(actor)` (raw param, not `&self->actor`) stops if-conversion of the tail call; limbCount is 21; first FUN_00372f38 call is 3 args (cast fn ptr) |
| EnDivingGame_Destroy | MATCHED 23/23 | `(Actor*, GameState*)` + `(PlayState*)state` inline (no play local) gives the `bne`; FUN_00350f34 called with 2 args via cast |
| EnDivingGame_Draw | MATCHED 21/21 | local `FaceAnimations* fa` for the first call only, second call re-derives it from `self` (forces `this` in r4 as index base) |
| FUN_00274ff8 (Idle, moved into actor .cpp) | MATCHED 94/94 | switch cases written 2,1,0 to get ROM block order |
| EnDivingGame_Update | MATCHED 159/159 | `eyeTexIndex > 2` (not >= 3); timer scale macro FR(n) = n*3/2 rounded; Vec3s torso copy via explicit `__ARM_common_memcpy2_6` (else duplicate symbol) |

Symbols: edgTimerBase/edgFlagsBase EQUs removed. They were gSaveContext fields: timer1State (+0x155E), timer1Value (+0x1560), eventChkInf[3] (+0xEF2). Only `edgCylinderInit` EQU (0x5222CC) remains in diving_syms.s.
Debt: play+0x7F78 raw offset (N64 sIsInitialized in PlayState), play+0x5BF4 (gameplayFrames), casts of FUN_00372f38/FUN_00350f34 to fewer-arg prototypes.
Outside actor dir: src/functions/functions_240000s.cpp (GLOBAL_ASM FUN_00274ff8 removed), plus functions_200000s.cpp (stage 1). include/: none.
