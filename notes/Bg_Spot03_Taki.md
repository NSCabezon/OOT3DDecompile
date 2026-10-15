# Bg_Spot03_Taki — Stage 1 (Haiku) status

ws_check.sh: only baseline FUN_00249af8 differs. Functions (6 incl. action FUN_003e7f18): 2 matched in C.

| Function | State | Notes |
|---|---|---|
| BgSpot03Taki_Destroy | MATCHED (C) | DynaPoly_DeleteBgActor + tail call FUN_00350f34 via `__asm` label (truncated prototype). |
| BgSpot03Taki_Update | MATCHED (C) | `actionFunc(self, play)`. |
| BgSpot03Taki_Init | NOT MATCHED, asm kept | C draft under `#if 0`. 38/69 words differ, size 280 vs 276. Remaining diff: GetCMABByIndex/FUN_00372d94 call pattern (compiler loads the skel->unk_0C pointer into r2 instead of r0 and keeps zar in r7 instead of r8). Tried: ReadCollisionHeaderFromZsi (fixed the colHeader stack slot), GameState* signature + local PlayState* (fixed play/zero regs), local `cmab` var, direct `animType` store. Not tried: reordering the two model blocks, plain struct-member temporaries. |
| BgSpot03Taki_Draw | NOT ATTEMPTED, asm kept | 3DS model-based draw (SkeletonAnimationModel + FUN_003695cc + PauseContext_GetState), not a display list like N64. Time-boxed out. |
| FUN_00323f04 | NOT ATTEMPTED, asm kept | Waterfall SFX helper (sound 0x0100015e, static state at 0x005b12d8, Audio_PlaySoundGeneral). Called from Draw only. |
| FUN_003e7f18 | NOT ATTEMPTED, in place | The waterfall action function (206-line asm, state machine on 0x1C2/0x1C8/0x1C0). Lives in src/functions/functions_3E0000s.cpp, referenced only by this actor (set in Init). Candidate to move into the actor .cpp in stage 2. |

## Layout (3DS, from asm)
- actionFunc 0x1BC, timer s16 0x1C0, state u8 0x1C2, switchFlag u16 0x1C4, openingAlpha f32 0x1C8, bufferIndex u8 0x1CC.
- skelAnimModel1 0x1D0, skelAnimModel0 0x1D8 (FUN_00372f38 fills them with idx 1 / idx 0).
- bgId at 0x1A4 (DynaPolyActor). sizeof = 0x1DC.

## Debt
- sInitChain lives in the GLOBAL_ASM data block (`data/z_Bg_Spot03_Taki.data.s`, 0x005136F4). Init (asm and #if 0 draft) uses it through a raw address 0x005136F4 in the draft. Split data to make it a C symbol.
- Prototypes for FUN_00372f38 (7 args) and FUN_00350f34 (4 args) are declared locally with `__asm` labels because include/functions.hpp has them truncated.

## Files touched
- ws/Bg_Spot03_Taki/src/game/actors/Bg_Spot03_Taki/z_bg_spot03_taki.cpp
- ws/Bg_Spot03_Taki/src/game/actors/Bg_Spot03_Taki/z_bg_spot03_taki.hpp
- No edits outside the actor dir. No include/ edits.
