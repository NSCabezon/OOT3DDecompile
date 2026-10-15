# Elf_Msg2 (Haiku stage 1)

Workspace: ws/Elf_Msg2 (snapshot of oot3d taken at mkws time).
Final ws_check: only baseline FUN_00249af8 differs. All 6 functions match.

| Function | Status | Notes |
|---|---|---|
| ElfMsg2_Init | matched | Chain pointer is raw `(InitChainEntry*)0x00520364` (data/z_Elf_Msg2.data.s kept via GLOBAL_ASM). Needed a dummy `s32 unused = 0;` local in ElfMsg2_KillCheck to keep play in r6. |
| ElfMsg2_Update | matched | Same KillCheck as Init. |
| ElfMsg2_Destroy | matched | Empty (`bx lr`). |
| FUN_003ee7b0 | matched (moved) | WaitForTextRead. Moved from functions_3E0000s.cpp. |
| FUN_003f2314 | matched (moved) | WaitUntilActivated. Moved from functions_3E0000s.cpp. |
| FUN_003f9384 | matched (moved) | WaitForTextClose. Moved from functions_3E0000s.cpp. Calls FUN_00369a48 (N64 Actor_TextboxIsClosing), declared locally. |

Tried: naming a switchFlag local in KillCheck instead of the dummy local -> huge layout breakage (Init grows past 324 B). Rejected.

Files touched outside actor dir:
- src/functions/functions_3E0000s.cpp: removed 3 GLOBAL_ASM lines (FUN_003ee7b0, FUN_003f2314, FUN_003f9384).
include/: no changes.

Struct: ElfMsg2 unk_1A4[4] replaced by `ElfMsg2ActionFunc actionFunc` at 0x1A4 (size 0x1A8 unchanged).

Debt:
- sInitChain raw address (0x00520364) instead of a named symbol.
- Dummy local `s32 unused = 0;` in ElfMsg2_KillCheck (register allocation hack).

UNMATCHED: none
