# Bg_Spot01_Idohashira (Opus closing pass)
- Init/Destroy/Update/Draw: matched (earlier); tables now via EQU symbols in data_syms.s (no raw addresses). ws_check baseline.
- caseD_1_003a7ae4, caseD_3_003a5da0: not matched (regalloc/const hoisting, best 24/33 words). Left asm.
- caseD_2_003a5b20, FUN_0039e58c: not attempted (budget). Left asm.
