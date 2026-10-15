# En_Wonder_Item (stage 1, Haiku)

Result: 1 / 4 actor functions matched; ws_check.sh shows baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| EnWonderItem_Destroy | MATCHED (C in actor .cpp) | 14/14 words. Collider dim is `Cylinderf` (float), so `radius/height != 0.0f`. |
| EnWonderItem_Update | NOT MATCHED, left as GLOBAL_ASM | C draft under `#if 0`. 14/32 words differ: ROM branches (`bne`) around the `Actor_SetFocus` block, compiler if-converts it. Tried `(u16)` cast, local temp, `else {}`, early-return restructure: no change. |
| EnWonderItem_Init (732 B) | NOT ATTEMPTED (timebox) | Switch on wonderMode (10 cases, jump table at 0x284cb8). 7 updateFunc targets loaded from literal pool. |
| EnWonderItem_InitVars | n/a | data stays GLOBAL_ASM("data/z_En_Wonder_Item.data.s") |

## Action functions (outside actor dir, NOT moved)
Pool values loaded by Init, each a FUN_ in functions_*.cpp (not in the actor dir):
- FUN_0012632c (268 B): uses `GET_PLAYER`, 50.0f check, probably MultitagFree or MultitagOrdered
- FUN_001cc3c0 (260 B): same family (sqrt loop), MultitagFree or MultitagOrdered
- FUN_001563ec (80 B), FUN_003e08a0 (112 B), FUN_0025a4b0 (100 B): 50.0f / 30.0f distance checks. ProximityDrop / ProximitySwitch / RollDrop (0025a4b0 reads player invincibilityTimer, likely RollDrop)
- FUN_0012880c (240 B): reads collider acFlags AC_HIT, Actor_Spawn of ACTOR_EN_HEISHI2, BombSoldier
- FUN_001c696c (32 B): AC_HIT then tail-calls FUN_00362cb0 (= EnWonderItem_DropCollectible, args (this, play, 0)), InteractSwitch

Not attempted (timebox). Mapping above is inferred, not verified.

## Layout
3DS `EnWonderItem` header now has the N64 layout shifted +0x58 (updateFunc 0x1A4, wonderMode 0x1AC, collider 0x1D8, size 0x230). Verified from asm offsets used by Init/Update.
