# Demo_Tre_Lgt — Stage 1 (Haiku-only) status

Actor file: `src/game/actors/Demo_Tre_Lgt/z_demo_tre_lgt.cpp` (+ `.hpp` struct updated: cmb, zarInfo, skelAnimModel, action @0x580, unk_170/174 floats @0x584/0x588, status u8 @0x58C; size 0x590).
ws_check.sh: baseline only (FUN_00249af8). Nothing newly broken.

| Function | Status | Notes |
|---|---|---|
| DemoTreLgt_Init (248 B) | NOT matched, asm kept | C draft under `#if 0`. Byte-size 244 vs 248: the ROM keeps r8 live across the FUN_00337200 call (`ldr r8,[r4,#0x178]` after the `strb 0x19a`), my draft reloads it into r0 and uses 5 pushes. Tried 4 local-variable/ordering variants (unk178 local early/late, direct reads, cmb reload); none matched. |
| DemoTreLgt_Destroy (8 B) | NOT matched, asm kept | C draft (`GraphicsContext_UnknownStub` cast, the repo precedent) is byte-identical in fastchk, but in the full link the call becomes `b stub` where the ROM has `mov r0,r0` (armlink inlining of an empty callee in tail position). Needs the exact original callee shape (probably an empty SkelCurve_Destroy stub with a different tail form). |
| DemoTreLgt_Update (20 B) | NOT matched, asm kept | C draft (`actionFuncs[action](self, play)` with raw table 0x51C4D0) compiles but emits a `bl`-style call instead of the asm tail call `bx r2`. |
| DemoTreLgt_Draw (492 B in tsv) | NOT attempted (cfg-merged) | The tsv entry covers Draw **plus** the limb-draw callback `DemoTreLgt_OverrideLimbDraw` (its bytes sit after the literal pool at 0x002af308 in the dump). Needs a functions.tsv split before C can match. |

## Action functions (not moved)
- `FUN_001d2700` = N64 `func_8099375C` (WAIT action, calls `Animation_OnFrame`). Still GLOBAL_ASM in `src/functions/functions_1C0000s.cpp`. tsv size 2620 B is a merge artifact (asm file is 205 lines).
- `FUN_001d2588` = N64 `func_80993848` (ANIMATE action). Still GLOBAL_ASM in `functions_1C0000s.cpp`.
- Both are referenced only by `sActionFuncs` in the data dump (0x51C4D0), so they are candidates to move, but I did not get to it (time box).

## Data (GLOBAL_ASM `data/z_Demo_Tre_Lgt.data.s`, kept)
- 0x51C4C8: `s32` 3, 0x51C4CC: `s32` 4 (scalars, read by Init as the 5th arg of FUN_00337200; Init draft uses raw `*(s32*)0x0051C4C8`).
- 0x51C4D0: action table {FUN_001d2700, FUN_001d2588}.
- 0x51C4E0..: two info structs. Decoded from the dump they are {1.0, 136.0, 190.0, 50.0} and {1.0, 136.0, 220.0, 140.0}. N64 has {1,136,190,40} and {1,136,220,50}, so the 3DS values differ. Worth checking when the Draw/Update work is done.

## Raw-address debt
- Init draft: `*(s32*)0x0051C4C8` (scalar `3`).
- Update draft: `(DemoTreLgtActionFunc*)0x0051C4D0` table.

## 3DS-specific layout found (for the struct)
- 0x1A4 CMB pointer (ZAR_GetCMBByIndex), 0x1A8 opaque skel-curve block (FUN_003357dc / FUN_00337200 / FUN_003334b4), 0x1B0 `ZARInfo*`, 0x1B4 `SkeletonAnimationModel*`, 0x1F0 sub-block passed to FUN_00337200.
- Init sets `actor.unk_19A = 1`, `skelAnimModel->+0xAD = 0`, `unk_0C->+0x10 (animType) = 1`, unk_170 = unk_174 = 255.0f, status = 0, action = 0 (WAIT).
- Note `SkeletonAnimationModel::SetUnkAC` writes +0xAC in the header, but the 3DS code writes +0xAD (raw in the draft).
- Object status: bank < 0x13 and `play + bank*0x80 + 0x3A64 != 0`, ZARInfo at status+0x10 (NULL status gives the 0x10 offset seen in the asm).
