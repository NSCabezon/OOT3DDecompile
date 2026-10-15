# Bg_Bombwall STATUS (Haiku stage 1, 2026-10-13) -- ws_check: baseline only (FUN_00249af8)

| Function | Status |
|---|---|
| BgBombwall_Destroy | MATCHED (C, 31/31 words) |
| BgBombwall_Update | MATCHED (C, 5/5 words) |
| BgBombwall_Draw | MATCHED (C, 19/19 words) |
| BgBombwall_Init | NOT MATCHED, asm (GLOBAL_ASM). Draft in `#if 0`: size 748 vs 752, 93/188 words differ. Diffs: tris loop register choice (ROM keeps r7=&sTrisInit, sb/sl/r8 offsets), colHeader frame slot (ROM sp+8, ours sp+0xc), `bic r1` flag clears. ~10 variants tried (scene-check order, colHeader scope, sp80 vs direct locals, RotateVec helper). |
| FUN_003f5a3c (action, Wait; N64 func_8086ED70 + EDFC + EB5C inlined) | NOT MATCHED, asm (functions_3E0000s.cpp). Draft in `#if 0` in actor .cpp: size 532 vs 512, 110/128 words differ. Not iterated further. |
| FUN_003cc660 (action, Timer/broken; N64 func_8086EE40 + EE94) | NOT MATCHED, asm (functions_3C0000s.cpp). Draft in `#if 0`: 4/44 words differ (only the `bic r1,r0,#2` flag-clear pattern). Same C as Destroy's clear matches there, so the difference is context. |

Data: the 3DS tables (0x00510AD8 tris elements, 0x00510B8C tris init, 0x00510B9C init chain, 0x00510BA8 dust offsets)
are emitted by `data/z_Bg_Bom_Guard.data.s` (Bg_Bom_Guard's data chunk). Referenced here via EQU file `bb_symbols.s`
(do NOT redefine them in C: that would duplicate bytes and shift layout).

Files touched outside the actor dir (in ws only): none net. functions_3E0000s.cpp and functions_3C0000s.cpp are
identical to main tree (GLOBAL_ASM lines kept).
include/: no changes.

Next (Sonnet): Init (draft above), FUN_003f5a3c, FUN_003cc660 (4-word diff).


## Sonnet stage 2 (2026-10-13) -- ws_check: baseline only
- BgBombwall_Init: MATCHED (C, 188/188). Needed N64 static helpers (InitDynapoly(Actor* thisx,..) w/ `BgBombwall* self=(BgBombwall*)thisx` used only for the bgId store,
  DestroyCollision(Actor* thisx,..), SetBroken, RotateVec), `((BgBombwall*)actor)->colFlags |= 2`, `actor->world.pos` in the vecs += lines, `i < 3`.
  Rule found: `bic r1,r0` appears when a SECOND pointer vreg (Actor* thisx param) is live in the helper; plain `self` gives `bic r0`.
- FUN_003cc660: MATCHED (C, 44/44, in actor .cpp; GLOBAL_ASM removed from functions_3C0000s.cpp). Uses SetBroken(self, play) helper (inlined).
- FUN_003f5a3c: NOT MATCHED, asm. Draft under #if 0: 6/128 words differ, size matches (512). Left: first `ldrb r1/bic r0,r1` regs and final `ldr r1,=600.0f; vmov r2,s0; cmp` regs.
  Dust: hoist `fx=off.x; fz=off.z` locals, `fz*sin`, `fx*sin` operand order, `off.y + pos->y`, `pos` declared before sin/cos.

## Opus stage 3 (2026-10-13) -- ws_check: baseline only
- FUN_003f5a3c: MATCHED (C, 128/128, in actor .cpp; GLOBAL_ASM removed from functions_3E0000s.cpp).
  Fix: N64 play2 pattern `void FUN_003f5a3c(BgBombwall* self, PlayState* play2) { PlayState* play = play2; ... }`
  with `play2` passed directly as arg0 to CollisionCheck_SetAC (all other uses via `play`). Using `play` there too
  keeps the 6-word diff (acFlags byte in r0, 600.0f compare in r0/r1).
- Actor complete: Init, Destroy, Update, Draw, FUN_003cc660, FUN_003f5a3c all C.
