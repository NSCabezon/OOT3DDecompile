
<!-- merge 2026-10-13 18:33:55 -->
# En_Anubice_Fire (solo-haiku, 2026-10-13) — merged
- Matched: EnAnubiceFire_Init (72 words), EnAnubiceFire_Destroy (15). hpp: actionFunc@0x1A4, unk_1A8/1AC f32, unk_200 (cylinder), unk_258 (malloc'd obj).
- Init keys: store 0x1AC before 0x1A8; `u8* base = self+0x100` for the 0x1B2/0x1B6 s16 stores, 0x1B6=0 AFTER the 6 Vec3f copies; `src`/`dst` Vec3f* locals (gives r6 + 0x10 frame).
- Destroy: inlined Collider_DestroyCylinder (dead `mov r0,#1`) must be written as a call.
- Update: draft under #if 0, 84/114 words (pool consts 0.6/-0.75/-15/30 hoisted into s16; history shift 0x1B8..0x1F4 order is right).
- Not attempted: Draw, FUN_00108774, FUN_00178728; FUN_003e04b8 big.
