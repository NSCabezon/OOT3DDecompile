
<!-- merge 2026-10-14 19:07:45 -->
# Obj_Comb (G11, haiku stage)

- ObjComb_Init: MATCHED (C, 0/30 words). Note: `thisx->unk_19B = 2` (not self->actor) matches.
- ObjComb_Destroy: MATCHED (C, 0/10). Signature `(Actor*, GameState*)` + `PlayState* play = (PlayState*)state` first.
- ObjComb_Update: MATCHED (C, 0/22). `thisx->shape.rot.x` / `thisx->home.rot.x` on final store.
- Layout (3DS): actionFunc 0x1A4, collider 0x1A8, elements 0x1C8, unk_218/unk_21A s16, skelAnimModel 0x21C.
- Data: data_syms.s EQU sObjCombInitChain 0x534F54, sObjCombJntSphInit 0x534F44.
- Still asm (not in list): ObjComb_Draw, ObjComb_Wait.
- ws_check.sh Obj_Comb: baseline only.
