# Obj_Tsubo STATUS (Opus closing pass, 2026-10-13)
ws_check.sh: baseline only (FUN_00249af8).

| Function | Status |
|---|---|
| ObjTsubo_Init | MATCHED (EQU data symbols in data_syms.s + static inline SetupWaitForObject(Actor*)) |
| ObjTsubo_Destroy | MATCHED (`(ObjTsubo* self, PlayState* play)` signature; linker inlines Collider_DestroyCylinder -> `mov r0,#1`) |
| ObjTsubo_Update | MATCHED (static inline SetMode(Actor*, u8) in both branches) |
| FUN_0011055c (WaitForObject) | MATCHED, moved into actor .cpp (GLOBAL_ASM removed from functions_100000s.cpp) |
| FUN_002318b4 (Draw) | MATCHED (earlier stage) |
| FUN_003be8e4 (Idle, 708 B) | NOT MATCHED, asm in functions_3A0000s.cpp; draft #if 0 in actor .cpp (62/177 words) |
