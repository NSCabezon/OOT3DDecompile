# End_Title status (cascade stage 1, batch 1/1)

Target: EndTitle_Init, EndTitle_Destroy, EndTitle_Update, FUN_003fda88, FUN_003fdad0, FUN_002504ac.
ws_check.sh End_Title: baseline only (FUN_00249af8), non-function bytes 0.

## Functions
- EndTitle_Update: MATCHED (C, empty body).
- EndTitle_Destroy: MATCHED (C).
- EndTitle_Init: MATCHED (C). Needed: `z_end_title.hpp` struct (skelAnimModel @0x1A4, zarCtxb[4] @0x1A8, unk_1B8, f32 alphas @0x1BC/0x1C0/0x1C4, size 0x1CC);
  `data_syms.s` EQU `gUnk_005C1878 = 0x005C1878` for the switch selector at +0xF3C (plain raw-address casts folded to a different pool literal).
- FUN_003fda88 (wrapper: FUN_003fdad0(a0..a3, 0.0f, a4..a7)): MATCHED, moved into actor .cpp; GLOBAL_ASM line removed from src/functions/functions_3E0000s.cpp.
- FUN_002504ac (= Nintendo-logo draw/alpha fade, set as actor->draw for params==1): NOT MATCHED. Draft under `#if 0`
  (`FUN_002504ac_draft`), 28/37 words differ: threshold/alpha math is right, but ROM preloads 1100.0f/1.0f into s4/s2 and uses
  a different register for the rate/1/255 operands. ~12 variants (expression forms, frames local vs inline, ternary/if forms) tried.
  GLOBAL_ASM("asm/FUN_002504ac.s") kept in src/functions/functions_240000s.cpp.
- FUN_003fdad0 (list-append helper: a0 ctx with per-list count at +0x14+idx*4, total at +0x10, pool at +0x1B4, 3x24 pointer tables at +0x214/+0x4B4): NOT MATCHED. Draft under `#if 0` in the actor .cpp, best 86/108 words differ. Frame is 0x54 in ROM vs 0x3C-0x48 built; ROM keeps center/size vectors on the stack. ~12 variants (local order, struct copies, address-taken helper, parameter types) tried. GLOBAL_ASM("asm/FUN_003fdad0.s") kept in src/functions/functions_3E0000s.cpp.
- EndTitle_Draw: not in scope; still GLOBAL_ASM.

## Notes
- FUN_00250540 (params==2 draw) is referenced by Init; not in this batch, still GLOBAL_ASM.
- Files outside the actor dir touched: src/functions/functions_3E0000s.cpp (removed GLOBAL_ASM FUN_003fda88 line only).
- include/: nothing touched.

## Stage 2 (Sonnet) - nothing new matched; ws_check.sh = baseline only
- EndTitle_Draw: NOT MATCHED, GLOBAL_ASM kept, draft under `#if 0`. Structure/constants now right (pos via index helper `SetComp` gives
  r6=1 idiom; `ScaleCol` helper; sinf/cosf with `ang` local inside a block fixes rotation regs). Real constants: thresholds 0.5+(3/R)*{890,810,850}
  for endAlpha/tlozAlpha/ootAlpha, clamp 0.7843138f, rates `R*2.3333333f*(1/255)` (end) and `R*5.0f*(1/255)` (tloz, oot). Left: ~half of the
  tail words (const reg alloc: ROM s3=3.0,s1=0.5,s4=mult vs mine s1,s2,s4) + 2 insns longer in ROM. `gUnk_005311b0` (u32 @0, f32 @4) EQU added to data_syms.s.
- FUN_002504ac: NOT MATCHED (28/37). ROM preloads 3.0,1100,1.0 before the vdiv and keeps clamp store separate (vstrge) - tried ptr alias, thisx, >= order, rate local.
- FUN_003fdad0: NOT MATCHED, best 64/108 (scoped Vector3f temps). Body matches; frame 0x54 needs center/size in separate slots (armcc shares them).
- FUN_00250540: STRUCTURAL BLOCKER (cfg/data): two guarded function-local statics (guard 0x0055A210 + 12-float matrix @0x005BE29C, model-manager guard
  0x0055A21C) -> needs new pinned data symbols in oot3d.ld (LOADER_RECIPE) outside actor dir. Not attempted.

## Stage 3 (Opus) - nothing new matched; ws_check.sh = baseline only
- FUN_002504ac: NOT MATCHED, best 12/37 (was 28). `f32 step = 1.0f/255.0f; f32 max = 1.0f;` locals fix pool order, the early 1.0 preload
  and the separate clamp store; `s32 frames` then `f32 t`, `if (t < frames)`, `f32 a = self->endAlpha` read. Left: armcc hoists the
  frames int->float conversion next to the ldrh; ROM does it after the vdiv (reuses s1). Draft under `#if 0`.
- FUN_003fdad0: NOT MATCHED, best 6/108 (was 64). Typed ctx struct (count[idx] re-read via pointer), Vector3f locals at point of use and
  `MTX34 mtx` declared AFTER them -> frame 0x54 with ROM slot layout. Left: 48-byte copy to +0x110 is 6+6 regs in ROM (zero for +0x170
  already in r0, dst in r7) vs 7+5 in armcc. Draft (with struct defs) under `#if 0`.
- GLOBAL_ASM for both kept in src/functions/functions_{240000s,3E0000s}.cpp.
