
<!-- merge 2026-10-14 23:19:08 -->
# En_Light (G18, haiku stage) status

MATCHED (C):
- EnLight_Destroy: real virtual call on model @0x1A4, slot 1 (`EnLightModel::Destroy`), class key `_ZTI12EnLightModel` EQU in actor syms.s (value 0x7FFF0050). Should move to shared_syms.s (main) with a unique value.

NOT MATCHED (drafts under #if 0, GLOBAL_ASM kept):
- EnLight_Update: 13 words off (radius*scale schedule: ROM does the radius ternary before loading scale; timer register r1 vs r0). FlameParams stride is 12 bytes; table at EnLight_sFlameParams (0x52BF64, syms.s).
- EnLight_Draw: 4 words off (yaw - rot.y register pair before Matrix_RotateY; ROM loads rot.y into r1). Uses SkeletonAnimationModel members via _ZN22SkeletonAnimationModel12FUN_003721e0EP5MTX34 / FUN_00372170 aliases.

NOT ATTEMPTED: Init, UpdateSwitch (not in this batch).
Verification: fastchk only. ws_check currently fails for every workspace (main-tree data_chunks.txt / data/oot3d.ld changed 23:03).
