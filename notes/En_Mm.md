
<!-- merge 2026-10-15 11:01:39 -->
# En_Mm (G27, sonnet stage) STATUS

Baseline ws_check: only FUN_00249af8 differs (OK, 2026-10-15, after the sonnet stage).

| Function | Insns | State | Notes |
|---|---|---|---|
| EnMm_OverrideLimbDraw | 16 | MATCHED (C) | |
| EnMm_Destroy | 17 | MATCHED (C) | FUN_0035021c takes ONE arg (the stray r1 = collider arg of the linker-inlined Collider_DestroyCylinder stub) |
| FUN_001e93d4 | 24 | MATCHED (C) | store order speedXZ, actionFunc, 8A4, 8A0, flags|=1, 89C; moved, GLOBAL_ASM line removed from functions_1C0000s.cpp |
| FUN_001e943c | 28 | MATCHED (C) | |
| FUN_00288b84 | 30 | MATCHED (C) | |
| FUN_00353aa4 | 49 | MATCHED (C) | = N64 EnMm_ChangeAnim; sAnimationInfo @0x52C7A0 via EQU EnMm_sAnimationInfo (data_syms.s); moved |
| FUN_00157108 | 50 | MATCHED (C) | = N64 func_80AAE598; IsDay inline: scene 0x63 + cutsceneIndex 0xFFF4 early `return 1`, then dayTime 0x3555 < t <= 0xD556; moved |
| EnMm_Draw | 43 | MATCHED (C) | `GraphicsContext_UnknownStub(play->state.gfxCtx)` after FaceAnimations call; `FaceAnimations* fa` local (matches `add r0,r0,#0x8e0` after the stack adjust); model re-read at every use |
| EnMm_PostLimbDraw | 33 | MATCHED (C) | function-local static Vector3f @ .bss 0x59B478 pinned (see below); guard hand-written on EQU words (base 0x52C754 `[1]` for the test, 0x52C758 for acquire/release), because armcc only addresses the guard as "InitChain + 4" when sInitChain is referenced by C code (Init still asm). `f32 x,y,z` locals before the member stores give the vldr,vldr,vldr,vstr... order; N64-order MultVec3f wrapper + `Actor* actor` local give `ldr r2; add r0; mov r1` |
| EnMm_Update | 197 | NEAR, 8 words, GLOBAL_ASM | draft under #if 0 (all structure matches incl. jump table, tail call to CollisionCheck_SetOC; sp26/sp24 must be scoped in the last else-block). Left: cases 4 and 6 flag RMW (`ldr r0; bic/orr r1,r0,#1; str r1; ldr r2,[sp,#8]; mov r1,#N`) - ours `mov r1,#N` hoisted, RMW dest r0. ~40 variants (aliases, forms, helper typing) did not move it |
| EnMm_Init | 191 | NEAR (4 words with a local ctor, 23 with the shared one), GLOBAL_ASM | draft under #if 0. Everything matches except the VFP numbering of the inlined MTX34_Identity() guard block. Local MTX34Init ctor with params in cell order [1,4,5,2,0,3,6,7,8,9,11,10] (cells row-major) leaves only 4 words (x02/x10 get s8/s0 instead of s0/s8). ~1500 compile variants (param/store permutations, aliases) did not close it |

Struct: Actor @0, SkelAnime @0x1A4, jointTable @0x228, morphTable @0x534, actionFunc @0x840, collider @0x844 (ColliderCylinder, 0x58), unk_89C(unk_1E0) text state, unk_8A0 mouthTexIndex, unk_8A4, unk_8A8 path, unk_8AC, unk_8BC speedXZ, unk_8C0 objBank, unk_8C4/8CA Vec3s head/torso rot, flags @0x8D0 (bit0 = draw override on), curAnimIndex @0x8D4, unk_8D8, model @0x8DC, FaceAnimations @0x8E0, unk_AAC (bunny-hood model), unk_AB0 MTX34; size 0xAE0.

Splits applied: none.

## Pin applied in this workspace
`python3 -P scripts/pin_static.py ws/En_Mm bss 0x59B478 12 "z_en_mm.o(+BSS)" --label z_en_mm`
(adds region `z_en_mm.bss 0x0059B478 { *z_en_mm.o(+BSS) }` to data/oot3d.ld; no data chunk split: the guard word stays in the asm chunk and is reached through EQUs EnMm_sData / EnMm_sHeadOffsetGuard).

## Follow-up when EnMm_Init becomes C
Define `static InitChainEntry sInitChain[]` (0x52C754) in C, `pin_static.py <tree> split 0x52C754 --size 8`, then PostLimbDraw can use a real `static Vector3f headOffset(200, 800, 0)` (guard lands at +4 of sInitChain's section) and the EQUs EnMm_sData/EnMm_sHeadOffsetGuard go away.
