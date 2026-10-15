
<!-- merge 2026-10-15 17:22:13 -->
# Arrow_Fire (G38, Haiku pass)

- MATCHED (C, 0 words off): ArrowFire_Destroy, ArrowFire_Update, ArrowFire_Charge, ArrowFire_Hit
- UNMATCHED: ArrowFire_Fly (37/75 words off, draft under #if 0). Diff: ROM keeps the arrow pointer in r1 for the else branch and pushes r5/r6 for the Vec3 copy (dst computed after the NULL test); tried pos-pointer placement, explicit diffs first, `<=` vs `<`, struct copy vs pointer copy, arrow alias variants. Not solved.
- Init/Draw not in the batch list: untouched (GLOBAL_ASM).
- Splits: none. Infra: `_ZTI14ArrowFireModel EQU 0x7FFF0060` added to ws src/game/shared_syms.s (before END); must be merged into main shared_syms.s by hand (VFE key for Destroy's virtual call on +0x1C4). Header z_arrow_fire.hpp typed (unk_F8 used for projectedW, not in Actor header).

## Sonnet pass (G38)
- MATCHED (0 words, ws_check baseline): ArrowFire_Fly (N64 Math_Vec3f_DistXYZ + ArrowFire_Step inline; 2nd alias `a2 = arrow` used for `a2->timer`; `distanceScaled = (d <= 1.0f) ? 1.0f : d` + unconditional 2nd store), ArrowFire_Init (GetModelManager x3 in separate scopes, `alloc = mm.allocator` before ZAR_GetCMBByIndex, `actor->unk_178`; sInitChain = ICHAIN_F32(uncullZoneForward, 2000, STOP) as real static after InitVars; GLOBAL_ASM("data/z_Arrow_Fire.data.s") removed -> orchestrator: drop chunk row z_Arrow_Fire.data (0051099C) + ld region if main needs it; ws_check still baseline).
- UNMATCHED: ArrowFire_Draw (big, ~237/276 words, draft under #if 0): frame/stack layout (0x40) now matches; remaining = VFP/GPR numbering (ROM hoists 0.0f into s17 and `mov r5,#1`), if/else vstreq shape, MakeTrans/SetUnkAC family.
- Infra for merge: `_ZTI14ArrowFireModel EQU 0x7FFF0060` still must go into main src/game/shared_syms.s (before END). `#include "mtx34_trans.hpp"` added (draft only).
