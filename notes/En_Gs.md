
<!-- merge 2026-10-14 22:25:10 -->
# En_Gs (G14, haiku stage) — STATUS

ws_check.sh: baseline only (FUN_00249af8).

Matched (C in z_en_gs.cpp): EnGs_Destroy, EnGs_Init.
- EnGs_Init uses GetModelManager() (include/model_manager.hpp) for the owner reset.
- Data: data_syms.s EQUs (InitChain 0x526024, CylinderInit 0x526048, shared base 0x526080 for
  sColChkInfoInit (+0) and sDamageTable (+0xA); shared base is what makes armcc emit one literal).
- EnGs struct (z_en_gs.hpp) rewritten with 3DS offsets; size 0x284.

## Sonnet stage (G14)
Matched: EnGs_Update (0 words; inlined N64 func_80A4E648/E3EC as static inline; per-case `unk_19F = 0` stores; `goto cont`
from the ==2 arm into the ==1 arm; inner switch on textId gives `sub #0x2000; subs #0x54`). EQU En_Gs_sColor = 0x5260B2.
Not matched: EnGs_Draw (148 words, far; draft #if 0): ROM hoists the SetUnkAC `mov r6,#1` above the `flags&1` branch (play in r7,
base r5=self+0x200); ours sinks it. Index-helper tricks hoist it but lose immediate offsets.
Struct EnGs hpp now has typed fields (unk_19C..19F, unk_1A0[3], flashColor, model ptrs, unk_280).
