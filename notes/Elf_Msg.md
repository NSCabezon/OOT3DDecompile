# Elf_Msg: cascade stage 1 (batch 1/1)

Workspace: ws/Elf_Msg. Final ws_check.sh Elf_Msg: only baseline FUN_00249af8 differs.

| Function | Status | Notes |
|---|---|---|
| ElfMsg_Destroy | matched (C) | Empty (`bx lr`). |
| ElfMsg_CallNaviCuboid | matched (C) | Navi pointer hoisted to top; Y test written as `player.y >= this.y` (ROM operand order). |
| ElfMsg_CallNaviCylinder | matched (C) | `fabsf` via `_fabsf` static inline wrapper. |
| ElfMsg_Update | asm, draft #if 0 | C body matches under fastchk, but functions.tsv sizes it at 308 B: 12 trailing bytes at 0x001F2E74 (`ldr r0,[r0,#0x50c]; mov r1,#0; b FUN_00372170`, unreferenced). The 296 B C body shifts every later function (9650 differ), so it stays asm until the cfg is split (cfg_split.py). |
| ElfMsg_Init | matched (C), stage 3 | Key: rot.x block = one `f32 scale` assigned AND stored (z then x) inside EACH arm (gives shared s0 + per-arm stores, no if-conversion); action tail = `if (params & 0x4000) Cylinder else Cuboid` (N64 order inverted) via inline SetupAction with `thisx->params`. Stage 1/2 drafts (25-26/91 off, ~80 variants) superseded. |
| ElfMsg_Draw | asm, draft #if 0 | 45/52 words off. ROM uses the function-local static guard 0x0055A21C (GetModelManager-style, ctor FUN_0036788c), FUN_0033a754 writes an Mtx34 at sp+0x10, FUN_0033a638 gets 0x5C1858 (guess: ModelManager+0x32A0). Draft structure does not match; 4 variants tried. |

Files touched: ws/Elf_Msg/src/game/actors/Elf_Msg/z_elf_msg.cpp, z_elf_msg.hpp (ElfMsg gets `ElfMsgActionFunc actionFunc` at 0x1A4, size unchanged). No changes outside the actor dir, no include/ edits.
