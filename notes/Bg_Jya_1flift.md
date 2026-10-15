# Bg_Jya_1flift (stage 1, Haiku) status

ws_check.sh: baseline only (FUN_00249af8). Build OK.

| Function | Status | Notes |
|---|---|---|
| BgJya1flift_Destroy | matched (C) | |
| BgJya1flift_Update | matched (C) | room check via raw s8 at play+0x4C30 |
| BgJya1flift_Draw | matched (C) | |
| BgJya1flift_Move | matched (C) | |
| BgJya1flift_DelayMove | matched (C) | `if (moveDelay > 20)` form; tail call to FUN_00185384 now via plain prototype (noinline removed, see below) |
| BgJya1flift_DoNothing | matched (C) | empty |
| FUN_00185384 (ChangeDirection, moved from functions_180000s.cpp) | matched (C) | body written out (no helper: 40 B overflowed the 32 B slot) |
| FUN_003c0a58 (WaitForSwitch, moved from functions_3C0000s.cpp) | matched (C) | ChangeDirection body inlined |
| BgJya1flift_Init | matched (C) | Stage 2 (Sonnet): second typed copy `BgJya1flift* s2 = self;` used for Collider_SetCylinder gives the ROM's extra `mov r5, r4`. 372 B, 0 words differ |

## noinline removal
- FUN_00185384 (ChangeDirection) moved to its own TU `z_bg_jya_1flift_dir.cpp` in the actor dir: armcc can no longer inline it into DelayMove, so the tail call matches with a plain prototype. Without the split (same TU, plain prototype) it inlined (68 B vs 36 B).

## Data
- `data_syms.s` (actor dir, new): EQU for sIsSpawned 0x5121F4, sFinalPositions 0x5121F8, sCylinderInit 0x512200, sInitChain 0x512238.
- Data GLOBAL_ASM kept.

## Files outside the actor dir (ws only)
- src/functions/functions_3C0000s.cpp: removed `GLOBAL_ASM("asm/FUN_003c0a58.s")`
- src/functions/functions_180000s.cpp: removed `GLOBAL_ASM("asm/FUN_00185384.s")`
- include/: untouched
