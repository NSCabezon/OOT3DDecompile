# Item_Inbox (Opus, loader-static task)

| Function | State |
|---|---|
| ItemInbox_Init/Update/Draw/Wait | MATCHED (unchanged; Init now passes raw `state` to FUN_003a0e88) |
| FUN_003a0e88 | MATCHED (C) via shared `GetModelManager()` static, see LOADER_RECIPE.md |
| ItemInbox_Destroy | asm (cfg-merged span, needs functions.tsv split) |

ws_check: only baseline FUN_00249af8.
Infra outside actor dir: include/model_manager.hpp (new), src/game/model_manager/{model_manager.cpp,model_manager_syms.s} (new),
src/functions/functions_300000s.cpp (-GLOBAL_ASM __aeabi_atexit), data/oot3d.ld (+2 regions),
src/data/data.cpp + src/data/data_54AC28.s (trimmed dump; in main do a data_chunks.txt split instead).
