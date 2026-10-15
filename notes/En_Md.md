
<!-- merge 2026-10-14 23:35:25 -->
# En_Md (G20, haiku stage) status

Baseline ws_check: only FUN_00249af8 differs (OK), 0 non-function bytes.

| Function | Result |
|---|---|
| EnMd_Destroy | MATCHED (C in z_en_md.cpp) |
| EnMd_OverrideLimbDraw (0x23bc70, 52 B) | MATCHED. Absorbs the old FUN_0023bc80 tail (16 B head fell through into it). See layout note. |
| FUN_001c4ddc | MATCHED with raw table address 0x0050CBA4 (debt: no symbol; table shared, used by FUN_0034c664). |
| FUN_003707dc | MATCHED (moved from functions_370000s.cpp; tail-calls FUN_00370818). |
| FUN_00370cf4 | MATCHED (moved from functions_370000s.cpp; tail-calls FUN_00370d60). |
| EnMd_PostLimbDraw | NOT matched: 14/19 words, ROM keeps `mov r0,r1`/frame before the limb compare, built pushes r4/r5 or if-converts. ~13 variants. Draft under #if 0. |
| EnMd_Draw | NOT matched: 6/46 words, prologue scheduling only (ROM `mov r4,r0; add r5,r4,#0x400` then `sub sp` before ldrsh). ~15 variants. Draft under #if 0. |
| FUN_00196354 (functions_180000s.cpp) | NOT matched: 7/44 words, play/sub-struct register swap (ROM play=r5, base+0x2B00=r6). Draft under #if 0 in actor cpp; GLOBAL_ASM left in functions_180000s.cpp. |
| FUN_00173778, FUN_001738c4, FUN_003d2ae4, FUN_00370d60 | NOT ATTEMPTED (haiku stage: large functions, Sonnet). |

## Layout note (orchestrator must apply by hand, merge_ws does not copy data/oot3d.ld)
- FUN_0023bc80 no longer exists as its own function: removed its GLOBAL_ASM from functions_200000s.cpp and its pin block from data/oot3d.ld (between EnMd_OverrideLimbDraw and FUN_0023bca4). `--keep=FUN_0023bc80` in data/keep_symbols.txt can be dropped too.

## 3DS layout facts (actor)
- Fields after the collider/interact info: N64 offset + 0x270 (e.g. eyeTexIndex 0x47E, alpha 0x480, animSequence 0x47B, fidgetTableY 0x484, fidgetTableZ 0x4A8). actionFunc at 0x3F4.
- Limb count for fidget tables is 0x12 (18).
- FUN_00370d60 (116 insns): FAR. Draft (N64 WithTalking, case order 102F,1046,group,1033) under #if 0 in z_en_md.cpp: right size, ~35 insns off (hoisted const regs r1/r3 swapped, 1033/1046 shared-store layout). ~30 variants (case permutations x else-if).

## Sonnet stage (G20)
Matched (all 0 words, ws_check baseline): EnMd_PostLimbDraw (after cfg split FUN_0021e968 @0x0021e968), EnMd_Draw, FUN_00196354, FUN_001738c4, FUN_00173778, FUN_00105bd0, FUN_003d2ae4, EnMd_Init, EnMd_Update, FUN_00370818.
Left: FUN_00370d60 (far). Extra files: src/game/actors/En_Md/data_syms.s (EQUs), z_en_md_tbl.cpp (FUN_001c4ddc own TU so Update does not inline it).
Infra in ws: rodata chunk split at 0x4D99CC (16 B, EnMd_Draw color const) + z_en_md.rodata region (pin_static split/place) -> must be applied to main (oot3d.ld, src/data/rodata.cpp, rodata_chunks.txt, regenerated rodata_4D9728.s/rodata_4D99DC.s).
