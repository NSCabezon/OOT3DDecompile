
<!-- merge 2026-10-15 17:57:37 -->
# Arrow_Light (G40 Haiku pass)
- ArrowLight_Charge: MATCHED (C, 0/42 words)
- ArrowLight_Update: MATCHED (C, 0/15) - msgMode via one local `s32 msgMode = GetMessageMode(state)`
- ArrowLight_Destroy: MATCHED (C, 0/13) - model virtual call slot 1, store NULL inside the null-check branch; _ZTI15ArrowLightModel EQU in shared_syms.s (0x7FFF0060)
- ArrowLight_Fly: NOT matched, draft under #if 0 (best 21/75). Diff: arrow/pos copy register naming (ROM keeps arrow in r0 + `movs r1,r0` copy, pushes r5/r6 for ldm temps) and the float compare (`<=` fixed one word). ~14 variants.
- ArrowLight_Hit: NOT matched, draft under #if 0 (best 53/87). Diff: code is 4 bytes longer than ROM (352 vs 348) - an extra compare/branch in the timer<16 / timer<8 tail; pool offsets shift. ~3 variants.
- Init / Draw: untouched (GLOBAL_ASM, not in the G40 list)
- Header: ArrowLight struct fields (radius 0x1A4, timer 0x1A6, alpha 0x1A8, unkPos 0x1AC, unk_160 0x1B8, unk_164 0x1BC, actionFunc 0x1C0, model 0x1C4) from the ROM.
- EnArrow offsets used: parent 0x124, update 0x13C, timer 0x304 (u8), hitFlags 0x305 (u8).
- ws_check.sh: baseline only (FUN_00249af8).
- Merge notes: shared_syms.s needs `_ZTI15ArrowLightModel EQU 0x7FFF0060` in the VFE block (before END); merge_ws.py does not handle shared_syms.s.
- Scratch: ws/Arrow_Light/tmp (var.py, variant files) - delete at end.
