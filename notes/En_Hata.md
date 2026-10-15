
<!-- merge 2026-10-14 12:36:19 -->
# En_Hata status (cascade stage 1, Haiku, batch 1/1)

- EnHata_Destroy: MATCHED (fastchk 0/15 words). Condition `actor->params == -1` is inferred from the ROM (`ldrsh [+0x1C]; cmn #-1`), semantics not verified.
- EnHata_Draw: NOT MATCHED (33/50 words off, 188 vs 200 bytes). ROM copies the scale into s2 for the column-0 products (3 extra vmov); helper/param/local variants did not reproduce the register use. Draft under #if 0.
- EnHata_OverrideLimbDraw: NOT MATCHED (39/55 words off, 200 vs 220 bytes). ROM keeps the axis pointer in r5 and mtx in r6 and has extra 0.0f copies; Vector3f ctor, axis pointer and declaration-order variants did not match. Draft under #if 0.
- EnHata_Update: NOT MATCHED (96/109 words off, 440 vs 436 bytes). ROM keeps self in r4 and play in r6 (armcc picks the opposite); zeroVec stays on the stack (ROM scalarises it). Draft under #if 0.
- Stage 2 (Sonnet): Update 16/109 words (draft updated under #if 0: Pitch/Yaw as static inline with expression-form Yaw, ternary clamps, 436 B size now equal; remaining diff = armcc CSEs dx/dz between Pitch and Yaw (ROM recomputes) + zero/wind VFP reg numbering). Draw still 33/50 (ROM's vmov copy of scale for column 0 unreproducible; forwarded locals/param order/loops/Vector3f all identical). OverrideLimbDraw best ~33/55 (axis Vector3f reused + rot; ROM keeps axis in r5/mtx r6, limbs via self+0x200 base). Init not attempted.
- EnHata_Init: not in this batch, still GLOBAL_ASM.

Header: `z_en_hata.hpp` now lays out the 3DS struct (dyna 0x000, skelAnime 0x1BC, limbs 0x240, collider 0x2B8, invScale 0x310, maxStep 0x312, minStep 0x314, unk_316 0x316, unk_318 0x318; size 0x31C). `play->envCtx` is not typed in include/z3D.hpp, so wind fields are read through local structs at play+0x3200 / play+0x3000.

## Stage 3 (Opus)
- EnHata_Update: MATCHED (0/109). Pitch via header `Math_Vec3f_DistXZ` (`__sqrtf`), Yaw via header `Math_Vec3f_Yaw`: armcc then recomputes dx/dz like the ROM.
- EnHata_Init: MATCHED (0/137) first try (GetObjectStatus zar, FUN_00358ea8 skel init, Animation_GetLastFrame, two FUN_0036932c per params branch, ReadCollisionHeaderFromZsi only when params == -1).
- EnHata_OverrideLimbDraw: MATCHED (0/55). `Vec3f axis; Vec3f* p`, Set(x,y,z) helper for (1,0,0), `f32 angle` local for the 1st rotation, Set helper with param order (x,z,y) for (0,0,1), `EnHata_Rotate(mtx, axis, angle)` inline owning MTX34 rot; limbs read as `self->limbs[i].z` (gives +0x200 base, #0x44/#0x42).
- EnHata_Draw: NOT MATCHED (33/50, 188 vs 200 B). ROM re-copies scale into s2 before each column-0 product; ~60 generated variants (param permutations, Vec3f/Vector3f scale vectors, by-value, loops, const refs, modified params) all give the same 188 B. Draft under #if 0.
- ws_check: baseline (only FUN_00249af8).
