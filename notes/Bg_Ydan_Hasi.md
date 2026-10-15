
<!-- merge 2026-10-14 12:25:57 -->
# Bg_Ydan_Hasi - cascade stage 1 (Haiku), batch 1/2

Functions in this batch (8):

| Function | Status | Note |
|---|---|---|
| BgYdanHasi_Destroy | matched (C) | |
| BgYdanHasi_InitWater | matched (C) | |
| BgYdanHasi_DecWaterTimer | matched (C) | |
| BgYdanHasi_Update | matched (C) | also bumps u16 at +0x1C6 (3DS-only counter, `unk_1C6`) |
| BgYdanHasi_SetupThreeBlocks | matched (C) | |
| BgYdanHasi_MoveWater | matched (C) | |
| BgYdanHasi_UpdateThreeBlocks | matched (C) | |
| BgYdanHasi_Draw | NOT matched (asm, draft under #if 0) | 5 words off: armcc puts thisx copy in r4 and reads params/model from it, ROM reads params from r0 and loads model into r1. Tried ~11 variants (model local, self alias, self-signature, ternary order, dead alias). |

Not in this batch (still asm): BgYdanHasi_Init, BgYdanHasi_UpdateFloatingBlock.

Layout notes (3DS): DynaPolyActor dyna @0x000 (bgId @0x1A4), actionFunc @0x1BC, model (SkeletonAnimationModel*) @0x1C0, timer s16 @0x1C4, type u8 @0x1C8, sizeof 0x1CC.
Sound ids passed to FUN_0035ae08: 0x010001B5 (water level down), 0x0100017B (elevator move).
Header change: `z_bg_ydan_hasi.hpp` (actor dir only). Added `BgYdanHasiWaterBox` (stride 0x10) because include/z3Dbgcheck.hpp WaterBox is 4 bytes.

ws_check.sh Bg_Ydan_Hasi: baseline only (FUN_00249af8).

## Batch 2/2 (cascade stage 1, Haiku)

| Function | Status | Note |
|---|---|---|
| BgYdanHasi_UpdateFloatingBlock | matched (C) | 0/65 words. Needed `(framesAfterMath * sin)` operand order, `% 383` on `unk_1C6`, pi/192 and pi/37.5 constants (timer 75). `#include <math.h>` for sinf. |
| BgYdanHasi_Init | matched (C) | 0/122 words, link baseline. Init chain via new `data_syms.s` EQU `BgYdanHasi_sInitChain = 0x00514180`. The 4-byte `modelIdx` table must be declared in its own block right before the FUN_00372f38 call (ROM builds it after unk_19A). `anim->unk_10` is `animType` (SetAnimType(1)). |

BgYdanHasi_Draw: matched (C), 0/27 words (stage 2, Sonnet). Idiom: `self` declared at top but the NULL test, params and unk_0C reads go through `((BgYdanHasi*)thisx)`/`thisx->params`; only the three model calls use `self`.
New file: `src/game/actors/Bg_Ydan_Hasi/data_syms.s` (actor dir only; must be merged with the actor).
ws_check.sh Bg_Ydan_Hasi: baseline only (FUN_00249af8).
