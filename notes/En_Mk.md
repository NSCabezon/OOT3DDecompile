
<!-- merge 2026-10-14 18:49:54 -->
# En_Mk (G7, haiku stage)

Matched (C, 0 words off in fastchk, ws_check baseline):
- EnMk_Init, EnMk_Destroy, EnMk_Draw, EnMk_OverrideLimbDraw
- FUN_003f9354, FUN_003f9588, FUN_0010d7d4, FUN_001459a8, FUN_001459f4, FUN_00141ebc, FUN_00112414, FUN_0010d6b8, FUN_0010d5e8, FUN_00111fac, FUN_00112050, FUN_001120f8 (moved from functions_*.cpp, names kept)

Not matched:
- EnMk_PostLimbDraw: C draft matches (0/34) but needs a function-local static Vector3f with a guarded ctor (object 0x59B44C). Needs a data pin (LOADER_RECIPE, data/oot3d.ld) -> L6224E without it. Draft kept under #if 0. Left as GLOBAL_ASM.

Not in this batch (still GLOBAL_ASM): EnMk_Update, EnMk_Wait.

Debt: FUN_00112414 writes eventInf[1] bit 0 (EVENTINF marathon flag) via the real symbol; Data: data_syms.s EnMk_sCylinderInit = 0x52C6FC.

## G7 sonnet stage
- EnMk_Update: MATCHED (0 words). Tail call to FUN_00372244 needs `Vec3s vec` scoped inside the `if (flags & 1)` block; FUN_00370734 called via `(s32(*)(SkelAnime*))` cast (header proto is void).
- EnMk_Wait: left asm, draft under #if 0 (27 words off; ~20 variants). With `u8 item = INV_CONTENT(ITEM_ODD_MUSHROOM)` local + `default:` placed between case 0 and case 13 the head/switch layout matches ROM, but case-0 arms get duplicated `str r2,[r4,#0x83c]; pop` tails instead of ROM's predicated `bne` to the shared tail (+16 B).
- EnMk_PostLimbDraw: skipped (guarded function-local static, needs ld pin) -> static.
