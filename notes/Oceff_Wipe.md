
<!-- merge 2026-10-14 17:48:56 -->
# Oceff_Wipe (haiku stage 1)

- OceffWipe_Update: MATCHED (timer < 240, 3DS literal)
- OceffWipe_Destroy: MATCHED (raw vtbl slot 1 call on model @0x1A8, tail FUN_00367c48 @0x1B0; GET_PLAYER((PlayState*)state) inline)
- Init, Draw: still GLOBAL_ASM (not in this batch)
- ws_check: baseline only

## sonnet stage 2
- OceffWipe_Init: MATCHED (GetModelManager x3, dead alias `s2` for `obj` store, `actor->objBankIndex`, if(params != 0) arm first).
- OceffWipe_Draw: NOT matched (~145 words, far): int-store identity MTX34 + SetUnkAC 1 (draft #if 0 in cpp).
