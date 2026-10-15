# En_Changer (Haiku stage 1)

Check: ws_check.sh En_Changer -> only baseline FUN_00249af8 differs.

| Function | Status | Notes |
|---|---|---|
| EnChanger_Destroy | matched (C, actor .cpp) | empty body |
| EnChanger_Update | matched (C, actor .cpp) | calls actionFunc(self, state), timer-- |
| FUN_0017963c (Wait) | matched (C, moved to actor .cpp) | GLOBAL_ASM removed from functions_140000s.cpp; name kept |
| FUN_00239264 (heart-piece flag) | matched (Opus stage 3, C, moved to actor .cpp) | Fix: use the real symbol `gSaveContext.itemGetInf[1]` (armcc emits literal &gSaveContext+0xF00, offset 0xA). The raw address 0x588862 was what swapped base/value regs. GLOBAL_ASM removed from functions_200000s.cpp; name kept |
| EnChanger_Init (1044 B) | skipped (Sonnet) | FUN_0020f064/FUN_0020f074 are cfg-merged tails of Init (use Init's r6/sp frame, shared epilogue, `bl`-less branches from Init; pool 0x20f084 inside). Needs functions.tsv merge/split. |
| FUN_00157298 (OpenChests, action) | matched (C, moved to actor .cpp) | Sonnet stage 2. Key: signature `(EnChanger*, PlayState* play)` (not GameState + local cast), `(EnChangerActionFunc)` cast at the actionFunc assignments in Wait. Spawn = Actor_Spawn(.., 0x168, x,y,z,0,0,0,params,1); GLOBAL_ASM removed from functions_140000s.cpp |

Struct layout (z_en_changer.hpp): actionFunc 0x1A4, leftChest 0x1A8, rightChest 0x1AC, finalChest 0x1B0,
leftChestNum 0x1B4, rightChestNum 0x1B6, leftChestGetItemId 0x1B8, rightChestGetItemId 0x1BA,
selectedChest 0x1BC, timer 0x1BE, roomChestsOpened 0x1C0.

Debt: EnBox "opened" flag read via raw offset +0x38C; ITEMGETINF now via gSaveContext.itemGetInf[1] (raw-address hack removed).
