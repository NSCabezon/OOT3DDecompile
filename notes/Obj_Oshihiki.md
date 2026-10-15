
<!-- merge 2026-10-15 15:50:03 -->
# Obj_Oshihiki — G32 Haiku pass (2026-10-15)

| Function | Status | Notes |
|---|---|---|
| FUN_0034aae0 (4 insns) | MATCHED (C, actor dir) | `DynaPolyActor::unk_1B8 |= 8`. Was already GLOBAL_ASM in the actor .cpp; no functions_*.cpp change. |
| ObjOshihiki_Destroy (12) | MATCHED (C, actor dir) | DynaPoly_DeleteBgActor + tail FUN_00350f34(actor, &skelAnimModel, 0). |
| ObjOshihiki_Update (28) | MATCHED (C, actor dir) | stateFlags/timer/yaw sin-cos, actionFunc tail call. |

Header (actor dir only): `z_obj_oshihiki.hpp` now has the 3DS layout derived from ROM: dyna (DynaPolyActor, bgId 0x1A4, unk_1B0 yaw), actionFunc 0x1BC, skelAnimModel 0x1C0, stateFlags 0x1C4, timer 0x1C6, yawSin 0x1C8, yawCos 0x1CC, cantMove 0x22E. Size 0x230 unchanged.

ws_check Obj_Oshihiki: baseline only (FUN_00249af8), 0 non-function bytes.

## Sonnet pass (G32)
All three remaining functions left as GLOBAL_ASM with drafts under `#if 0` in z_obj_oshihiki.cpp (header now has the 3DS field layout: pushDist/pushSpeed/direction/blockUnder/underDistX/Z 0x1D0..0x1E4, floorBgIds[5] 0x1F0, floorHeights 0x204, floorPolys 0x218, highestFloor 0x22C).
| Function | Status | Notes |
|---|---|---|
| ObjOshihiki_Init (137) | NOT MATCHED, ~25 insns off (far) | Structure matches ROM (InitDynapoly via play->GetObjectStatus(objBankIndex)->zarInfo.FUN_003532c0(1), type switch -> model kind, per-scene model table, 5x floorBgIds=0x32, stateFlags|=8, SetupOnActor). Needs EQUs: sScales 0x4DBB78, sSceneIds 0x4DBB98 (s8[9]), sModels 0x535604 (s8*[9]), sInitChain 0x535628. Open: ROM keeps `mov r6,r5` play copy (armcc copy-propagates every play2 alias tried), kind in r3 with `mov ip,r4`, scene-id regs. |
| ObjOshihiki_OnActor (181) | NOT MATCHED, ~90 diff lines (far) | Draft = N64 OnActor with inlined StrongEnough/NoSwitchPress/SetupOnScene/Fall/Push. ROM hoists the action-fn literal into r7 and shares one `str r7,[r4,#0x1bc]` tail; block order and reg numbering differ. Callees still asm: FUN_00359464 (SetGround), FUN_0034aaf0/FUN_0034aae0, FUN_003513fc (strength), FUN_0034a944 (CheckWall), actions FUN_00184ec8/FUN_003bc024/FUN_003bd348. Jump-table-embedded code after the `ldrlo pc` tables is real code (decode with capstone). |
| ObjOshihiki_Draw (192) | NOT MATCHED, ~55 diff lines (far) | Draft = inlined GetBlockUnder/MoveWithBlockUnder/UpdateInitPos + Matrix_UpdatePosition. ROM keeps Actor* thisx (r5) and self (r4) separate, NULL in sl, `1` for SetUnkAC in sb; vector block float scheduling differs. |
ws_check: baseline only.
