# Obj_Hana status (Haiku stage 1)

| Function | Status | Notes |
|---|---|---|
| ObjHana_Init | matched | C in z_obj_hana.cpp |
| ObjHana_Destroy | matched | C |
| ObjHana_Update | matched | C |
| ObjHana_Draw | matched | C |
| data (sCylinderInit, sColChkInfoInit, sHanaParams, sInitChain) | matched | was GLOBAL_ASM("data/z_Obj_Hana.data.s"), now C |

Result: ws_check.sh shows only the baseline (FUN_00249af8). No functions left as asm. No files outside the actor dir touched. No include/ edits.

3DS-specific notes:
- Actor fields: collider at 0x1A4 (ColliderCylinder, 0x58), skelAnimModel at 0x1FC (struct size 0x200).
- sHanaParams[].dList (N64 Gfx*) is a model index (s32) on 3DS, passed to FUN_00372f38 as arg3.
- sInitChain uses raw ICHAIN words (cullingVolume* members absent in 3DS Actor), cast to InitChainEntry*.
- Destroy: the `if (radius >= 0) Collider_DestroyCylinder` branch compiles to odd arg-setup in the binary; the plain C form matches.
- eventChkInf check = gSaveContext.eventChkInf[4] & 0x1 (ldrh at gSaveContext+0xEF4).
