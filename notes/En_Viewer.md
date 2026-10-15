
## Loader pass (Sonnet)
- EnViewer_Init: still GLOBAL_ASM. Draft in z_en_viewer.cpp under #if 0 (GetModelManager scoped refs, ZAR, indirect Create, %60) compiles; 114/172 words differ: state/type regs swapped (ROM r4/r5), ROM keeps const 1 in sl, +8 bytes.
- Raw 0x52FF0C / 0x50C058 replaced by EQU symbols (data_syms.s); ws_check = baseline only.
