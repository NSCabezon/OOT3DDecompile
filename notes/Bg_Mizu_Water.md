# Bg_Mizu_Water: decomp status (stage 3, Opus)

Workspace: ws/Bg_Mizu_Water. Check: scripts/ws_check.sh Bg_Mizu_Water -> baseline only (FUN_00249af8), non-function bytes 0.

| Function | Where | State | Notes |
|---|---|---|---|
| BgMizuWater_Init | actor .cpp | MATCHED (C) | all accesses through `Actor* thisx` (never `self->actor.`); fixes the r2-shaped GetCMABByIndex and the hoisted sInitChain load |
| BgMizuWater_Destroy | actor .cpp | MATCHED (C) | stage 1 |
| BgMizuWater_Update | actor .cpp | MATCHED (C) | first branch needs the intermediate `f32 t = (posY - B1) / (F1 - B1); unk1 = t * 200;` |
| FUN_003e78ac (WaitForAction) | MOVED into actor .cpp | MATCHED (C) | `(Actor* thisx, PlayState*)` signature, `thisx->params` / `thisx->world`; keeps the per-case stores unmerged. GLOBAL_ASM line removed from functions_3E0000s.cpp |
| FUN_003dfe64 (ChangeWaterLevel) | MOVED into actor .cpp | MATCHED (C) | same `thisx` signature; sfx tail: first compare reads `thisx->world.pos.y`, second `self->actor.world.pos.y` (re-read forces the second vldr). GLOBAL_ASM line removed from functions_3C0000s.cpp |
| BgMizuWater_Draw | actor .cpp (asm) | NOT MATCHED, GLOBAL_ASM | Opus: r5 cause found. ROM `mov r5,#1` = the int 1 CSE'd with another 1 that folds into an address (inline-helper/operator[] index param, same as matched BgJyaKanaami_ScaleCol col=1). An index-store helper for pos gives push {r4,r5,lr}/0x3c frame. Best draft under #if 0 = 2/41 words (y/z store order vs `mov r2,sp`), but it needs a reversed (z,y,x) param order + out-of-order stores -> not plausible, left asm. Natural helper still unknown. Same idiom likely blocks ~100 asm Draw fns (ArrowFire_Draw, DoorAna_Draw, EnBomChu_Draw, ...). |

Data: GLOBAL_ASM("data/z_Bg_Mizu_Water.data.s") kept; sInitChain (0x513160), sWaterLevels (0x513164), sWaterBoxIndices (0x513184) are referenced through absolute EQU symbols in src/game/actors/Bg_Mizu_Water/data_syms.s (same method as Bg_Mori_Rakkatenjo). Debt: they have no real symbols; could become C arrays once the data dump can be split.

Facts learned (3DS vs N64):
- Actor fields: actionFunc 0x1A4, type 0x1A8, targetY 0x1AC, baseY 0x1B0, switchFlag 0x1B4, SkeletonAnimationModel* 0x1B8, drawY 0x1BC (size 0x1C0).
- 3DS WaterBox entries are 0x10 bytes (repo WaterBox is 4): local `MizuWaterBox` {pad 2, s16 ySurface, pad 0xC}; helper loop var must be s32 (ROM uses blt).
- Action functions take `Actor*` (thisx) style: cast actionFunc `(BgMizuWaterActionFunc)FUN_xxx`.
- Update sets drawY = 0.0f, or -500.0f for type 3.
- Draw uses MTX34 Actor.modelMtx (0x148) and roomCtx.unk_7C0 as the s16 draw params array (DRAW_PARAMS); the Matrix_UpdatePosition + model calls are all inside `if (skelAnimModel != NULL)`.
- Rumble_Request is not in the 3DS code. The water-level sfx is FUN_0035ae08(actor, 0x010001B5).
- Message_CloseTextbox = FUN_003725e0.

Files changed: actor dir (z_bg_mizu_water.cpp, new data_syms.s, .hpp unchanged), src/functions/functions_3C0000s.cpp (removed FUN_003dfe64 GLOBAL_ASM), src/functions/functions_3E0000s.cpp (removed FUN_003e78ac GLOBAL_ASM). No include/ changes.
