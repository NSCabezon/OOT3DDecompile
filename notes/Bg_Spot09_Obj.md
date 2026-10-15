# Bg_Spot09_Obj: status (cascade stage 1, Haiku)

Result: 7/7 functions matched. ws_check.sh shows only the baseline (FUN_00249af8). Not merged into oot3d/ (merge after cascade).

| Function | Size | Status | Notes |
|---|---|---|---|
| BgSpot09Obj_Init | 228 B | matched | 3-entry setup table loop (`u32 i`, `ARRAY_COUNTU`); variadic FUN_00372f38 call with 6 model slots (NULL-terminated ptr/index pairs) |
| BgSpot09Obj_Destroy | 92 B | matched | variadic FUN_00350f34 with 6 model slots |
| BgSpot09Obj_Update | 4 B | matched | empty |
| BgSpot09Obj_Draw | 120 B | matched | `self->skelAnimModel[actor->params]` repeated (other forms add an extra insn and break the 120-byte slot); tent draws model[5] |
| FUN_00257b4c (moved, setup 0: DynaPoly init) | 120 B | matched | moved from functions_240000s.cpp; takes `GameState*` (register order), `sDynaColIdx` table |
| FUN_00257ab0 (moved, setup 1: bridge/tent visibility) | 156 B | matched | moved from functions_240000s.cpp; `gSaveContext.sceneSetupIndex >= 4` = IS_CUTSCENE_LAYER, `eventChkInf[9] & 0xF` = carpenters rescued |
| FUN_001ffcd8 (moved, setup 2: scale) | 40 B | matched | moved from functions_1C0000s.cpp |

Data: `GLOBAL_ASM("data/z_Bg_Spot09_Obj.data.s")` removed; tables now C (`sDynaColIdx`, `sSetupFuncs`, `sInitChain1/2`) and match byte-for-byte.

Files touched outside the actor dir: `src/functions/functions_240000s.cpp` (2 GLOBAL_ASM lines removed), `src/functions/functions_1C0000s.cpp` (1 GLOBAL_ASM line removed). No `include/` edits.

3DS notes:
- Model array lives at +0x1C0 (after DynaPolyActor 0x1BC + 4 pad), 6 pointers, size 0x1D8.
- DynaPoly collision index table is `s32 {-1,1,0,3,2}` (N64 had CollisionHeader* table); -1 = no collision.
- Cull-zone ICHAIN members on 3DS are `uncullZone*`.
- FUN_00372f38 / FUN_00350f34 are variadic on 3DS; declared locally via function-pointer casts (include/ prototypes are truncated).
