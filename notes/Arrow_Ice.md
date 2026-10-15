
<!-- merge 2026-10-15 17:45:08 -->
# Arrow_Ice (G39, Haiku + Sonnet)

MATCHED: ArrowIce_Destroy, Update, Charge, Hit, Fly (0/75), Init (0/134).
- Fly: dead alias `ArrowIceParentArrow* arrow2 = arrow;` used ONLY for the `arrow2->timer < 34` read gives ROM's
  `movs r1,r0` copy + r5/r6 saved for the Vec3f ldm/stm; clamp written `self->unk_1B8 = d; if (self->unk_1B8 < 1.0f)
  self->unk_1B8 = 1.0f;` (the local-based clamp gave vldrlt/vstrlt). The same two tricks should fix
  ArrowFire_Fly (ws/Arrow_Fire, main) and probably ArrowLight_Fly.
- Init: copy of ArrowFire_Init (GetModelManager() per use, `play->GetObjectStatus(...)->zarInfo`),
  `self->animCtl = model->unk_0C` stored in the actor (+0x1C8), CMB 0x27, CMAB 0x18.
- Data: `data_syms.s` EQU ArrowIce_sInitChain @0x5109C0 (GLOBAL_ASM data stays).
- shared_syms.s (ws only, VFE block before END): `_ZTI13ArrowIceModel EQU 0x7FFF0070` + EXPORT.
  MERGE NOTE: merge_ws.py does not touch shared_syms.s; add these two lines by hand in oot3d/src/game/shared_syms.s
  before END.

UNMATCHED: ArrowIce_Draw (270 insns, far/big: 235 of 288 words after ~15 variants, 1164 vs 1152 B).
  Clone of the ArrowFire_Draw draft. Structure, 0x40 frame and MakeTrans/Scale blocks match; ROM hoists 9.587e-5
  (s16) and 0.0 (s17/s18) across the body (vpush {d8,d9}), shares `mov r5,#1` (SetUnkAC/strb/unk_AD), the color
  block computes u*10/50/150 together before vcvt/and (local `f32 u` + three s32 temps shrinks it 1176->1160 B).
  Draft #if 0.
- ws_check.sh: baseline only (FUN_00249af8).
