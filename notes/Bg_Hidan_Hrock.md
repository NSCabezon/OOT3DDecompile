# Bg_Hidan_Hrock — Haiku stage 1 status

Actor dir: `src/game/actors/Bg_Hidan_Hrock/z_bg_hidan_hrock.cpp` (+ `.hpp` struct layout).
Final check: `scripts/ws_check.sh Bg_Hidan_Hrock` -> baseline only (FUN_00249af8).

| Function | Size (3DS) | Status | Notes |
|---|---|---|---|
| BgHidanHrock_Destroy | 64 B | MATCHED (C) | Uses `(char*)self + 0x1C4` for the collider address: the typed `&self->collider` makes armcc emit `add #0x100; add #0xc3` (7 words differ). Raw offset is debt. |
| BgHidanHrock_Update | 8 B | MATCHED (C) | `self->actionFunc(self, play)`, tail call. |
| BgHidanHrock_Draw | 0x30 B + model | MATCHED (C) | 3DS draws a SkeletonAnimationModel (not N64 dlist). SetUnkAC(1), FUN_003721e0, FUN_00372170(0). |
| BgHidanHrock_Init | 788 B | NOT MATCHED (asm + `#if 0` draft) | Blocked: reads data from the GLOBAL_ASM dump (sInitChain @0x5119FC, model idx table @0x511A04 = {0x11,0x12,0x12}, sTrisInit @0x511A10) and needs ColliderTris/Collider_InitTris/Collider_SetTris/ColliderTrisElement types, none in the repo. Draft is not compiled. |

## Not attempted (Haiku-only budget)
- Action functions referenced from Init, all still in `src/functions/`:
  - `FUN_003e7e50` (functions_3E0000s.cpp): `bx lr`, = N64 `func_808894A4` (empty). Shared stub probably; not moved.
  - `FUN_001c7cf8` (functions_1C0000s.cpp): = N64 `func_808896B8` (collider hit check, DynaPolyActor_IsPlayerOnTop). Not decompiled.
  - Also `func_808894B0` (shake, Rumble_Request/Actor_PlaySfx) and `func_8088960C` (fall) are reachable only through FUN_001c7cf8 / sub-actions; not located yet.
- Data: sTrisInit and sInitChain stay in the data dump. Moving them to C requires matching placement (data-before-InitVars rule).

## Debt / notes
- Struct: `ColliderTrisPlaceholder collider` (0x20) and `colliderElements[0xB8]` (2 x 0x5C) are placeholders until a ColliderTris type exists in include/.
- Shared with N64: dyna at 0, actionFunc 0x1BC, timer s16 0x1C0 (N64 unk_168), switchFlag u8 0x1C2 (N64 unk_16A), model ptr 0x29C.
- Init params handling per asm: `switchFlag = params & 0x3F; params = (params >> 8) & 0xFF`.
