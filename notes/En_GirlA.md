
<!-- merge 2026-10-15 01:12:53 -->
# En_GirlA (G24, haiku stage) status

ws_check (final, 2026-10-15): baseline only (FUN_00249af8). Build links.

## Matched in C (46 of 52 listed)
Actor file (`src/game/actors/En_GirlA/z_en_girla.cpp`) + shop file (`z_en_girla_shop.cpp`, new):
- EnGirlA_Update (2), EnGirlA_Destroy (10), func_80A3BEE0 (23, UpdateStockedItem; Actor* thisx signature), EnGirlA_TryChangeShopItem (58, jump table, moved to z_en_girla_shop.cpp), EnGirlA_InitItem (21, moved to shop file)
- FUN_003f87a8 (1), FUN_00103778 (2), FUN_00114194 (2), FUN_001311c8 (2)
- FUN_00103780, FUN_001c27b0, FUN_001c33e0, FUN_003cf518 (5 each, Rupees)
- FUN_001041f0, FUN_0011370c, FUN_00114908, FUN_001167a4, FUN_0012e0c4, FUN_00130c78, FUN_00376a38, FUN_003c4180 (10 each, Item_Give + Rupees)
- FUN_003ce7c0 (10), FUN_00113734 (12), FUN_003cf3a0 (9)
- FUN_00103398 (14, head after cfg split)
- FUN_00114c78, FUN_00130d80, FUN_0011419c, FUN_003ceb34, FUN_003ceb8c, FUN_003cff9c (CanBuy, 15-21)
- FUN_001002c4, FUN_0010320c, FUN_00103264, FUN_00104198 (CanBuy bottle, 21)
- FUN_00112e88, FUN_00149340, FUN_0014d9e0, FUN_0013002c, FUN_00130098, FUN_00131770, FUN_003ce7e8 (CanBuy 22-40)
- ItemGive_DekuNuts (15), FUN_003c3b88 (21, bombs ItemGive)
- BuyEvent_ShieldDiscount (26), FUN_00188d38 (28, ObtainBombchuPack)

All moved FUN_s were unhooked from src/functions/functions_*.cpp in this ws.

## cfg splits applied (ws only; merge with cfg_split replay)
- FUN_00103398: head 0x00103398 (60 B) matched; tail FUN_001033d4 (0x001033d4..0x0010360c) kept as asm (`../split/asm/FUN_001033d4.s`).
- ItemGive_DekuNuts: head 0x003ce8dc (60 B) matched; tail FUN_003ce918 (20 B) kept as asm.

## New actor-dir files
- `data_syms.s`: EQU `sShopItemEntries` 0x00524F50, `sShieldDiscounts` 0x005258B0 (absolute, no image bytes).
- `z_en_girla_shop.cpp`: TryChangeShopItem + InitItem (kept out of the main TU; in the same TU `--forceinline` inlined them into func_80A3BEE0 and changed the caller's regs).

## G24 Sonnet stage (2026-10-15)
Matched now (moved into z_en_girla.cpp, GLOBAL_ASM removed from functions_*.cpp): EnGirlA_Init (`(EnGirlA*, PlayState*)` signature), FUN_001032bc (`Vec3s* r = &shape.rot; r->x = 0;` block), FUN_00161554 (`(PlayState*, Actor* thisx)` + cases in order 7,8,9,A,27,28,29,2B,2A), FUN_00112ef0, FUN_00100228, FUN_003cfc54 (all `(PlayState*, Actor* thisx)` signature, `CUR_CAPACITY(n) <= AMMO(x)` inline, no cap local).
cfg split applied: FUN_00112ef0 @0x00112f90 -> FUN_00112f90 (60 B tail kept asm).

## Not matched (drafts under `#if 0` in z_en_girla.cpp, GLOBAL_ASM kept)
- EnGirlA_Draw (134 insns): 69 of 142 words. Layout/frame/branches match (mtx declared before Vec3f; struct copy for 2nd matrix); remaining: VFP numbering/pool order of 360/(1/65536)/DEG consts, hoisted `mov r6,#1`, s17 load after cmp. ~8 variants + 72-way const perm brute force.
- EnGirlA_InitializeItemAction (192 insns): 181 of 215 words, big. Decoded semantics (mask text ids 0x70B4..0x70BB via itemGetInf[3] bits, sold-out mask table @0x524f34, model/anim setup); draft uses raw offsets (debt).

## 3DS layout facts (from ROM)
- Actor fields: actionFunc 0x1A4, requiredObjectSlot s8 0x1A8, actionFunc2 0x1AC, isInvisible s16 0x1BC, isSelected s16 0x1C8, yRotation s16 0x1CC, basePrice s16 0x1DC, itemCount s16 0x1DE, skel model ptrs 0x1E8/0x1EC, unk_1FC f32 (Init sets 1.0f).
- ShopItemEntry stride 0x30 on 3DS (objID s16 @0, itemDescTextId u16 @0x0E).
- Bottle/CanBuy shape: `if (Item_CheckObtainability(id) == ITEM_NONE) return 0; return 1;` matches; the `!= ITEM_NONE` value form gives subs.
- healthCapacity is compared as s16 in ROM: `(s16)gSaveContext.healthCapacity`.
- gSaveContext+0x4A sword-health store is raw (`*(u16*)((char*)&gSaveContext + 0x4A)`), no named field. Debt.
- Shop flag reads use `gSaveContext.itemGetInf[0]` / `infTable[7]` directly; they match.
