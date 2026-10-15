
<!-- merge 2026-10-14 12:13:44 -->
# Oceff_Wipe3 status (batch 1/1, Haiku stage 1)

- OceffWipe3_Destroy: MATCHED (C, 0 words differ in fastchk; ws_check clean). Variant 2 fixed the flag OR: `u8* playerBase = (u8*)player + 0x1000; playerBase[0x72A] |= 0x40;` (ROM reuses the +0x1000 base). Raw `(u8*)thisx + 0x1A8` vtable call (slot 1) and `+0x1B0` tail call to FUN_00367c48; no `_ZTI` EQU, no header edits.
- OceffWipe3_Update: MATCHED (C, 0 words differ in fastchk; ws_check clean). Counter is the s16 at actor+0x1A4 (not in header, accessed by raw offset). Limit is `3.0f / R_UPDATE_RATE * 100.0f` (ROM order: 3/rate, then *100), compare `counter < limit` then `counter++`, else tail `Actor_Kill`.
- OceffWipe3_Init / OceffWipe3_Draw: untouched (GLOBAL_ASM, outside this batch).

Header `z_oceff_wipe3.hpp` not edited (fields at 0x1A4/0x1A8/0x1B0 accessed by offset in the .cpp).

## Stage 2 (Sonnet)
- OceffWipe3_Init: MATCHED (0 words, ws_check baseline). GetModelManager() x3 scoped `ModelManager& mm` (LOADER_RECIPE infra already in ws); local order `self` before `play` fixed the r4/r5 entry swap. Header now has counter/model/cmb/camObj fields (0x1A4..0x1B0).
- OceffWipe3_Draw: NOT matched (structural: SetUnkAC 1 in callee-saved reg + inline MTX34 translate/rotate/scale). GLOBAL_ASM kept, rough draft under #if 0 (170 words).
