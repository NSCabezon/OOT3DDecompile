# Bg_Gate_Shutter — Opus closing pass
8/8 matched. FUN_003e858c (N64 func_8087828C) MATCHED and moved into actor .cpp; GLOBAL_ASM removed from src/functions/functions_3E0000s.cpp.
Fix: write the N64 else-if chain as three independent `if` blocks each ending with `return;` (plain stores, no helpers needed).
ws_check.sh: baseline only (FUN_00249af8).
