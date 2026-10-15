
<!-- merge 2026-10-14 22:24:28 -->
# Bg_Haka_Gate (G14, haiku stage) — STATUS

ws_check.sh: baseline only (FUN_00249af8). Struct size 0x1F0 (BgHakaGate in z_bg_haka_gate.hpp).

Matched (C in z_bg_haka_gate.cpp; FUN_ GLOBAL_ASM lines removed from functions_*.cpp):
- BgHakaGate_Destroy (3DS model frees + statics via one base ptr; EQU in data_syms.s)
- BgHakaGate_Update
- FUN_003e1f20 (empty, bx lr)
- FUN_00181c4c (StatueInactive)
- FUN_00176ac0 (GateWait), FUN_00176a54 (GateOpen), FUN_002070e8 (SkullOfTruth), FUN_0021dd58 (FalseSkull)
- FUN_001cd7ec (StatueTurn): fixed by SetFloat product order + unk_1A8 store moved after flags clear
- FUN_0019a798 (FloorOpen, 3DS void-out path; gSaveContext.respawnFlag = +0x14EC)

Not matched (left as GLOBAL_ASM; C draft under `#if 0` in z_bg_haka_gate.cpp):
- FUN_00181e38 (StatueIdle): 6 words differ, all in the playerDirection/forceDirection float block
  (ROM keeps pd in s2 and does vcmpe early; ours pd in s1). ~40 variants (stmt order, decl order, if/else, casts).
- FUN_0019ae14 (FloorClosed): 13 words differ. armcc folds the 110.0f/40.0f compares into `sub r1,r1,#0xbc0000`
  (ROM loads both literals). Tried compare reorders, locals, goto split: no change.

## Sonnet stage (G14)
Matched: BgHakaGate_Init (216 words, 0 diff). Recipe: ROM copies the 1-entry initchain from rodata 0x4D70E0 to the stack
(EQU `BgHakaGate_sInitChainRom` in data_syms.s) via `InitChainEntry sInitChain[1] = { rom };` declared BEFORE colHeader,
`PlayState* play2 = play;` after colHeader (found with greedy single-site mutation), 13-arg FUN_00372f38 via a local
function-pointer typedef, `thisx->world.pos.y += 80.0f` BEFORE the actionFunc store in the gate branch.
Not matched (GLOBAL_ASM kept, drafts under #if 0):
- BgHakaGate_Draw: 58 words (far). Structure matches (incl. nops); flame-matrix 9-element scale block needs per-element
  `vmov s1,s0; vmul s1,m,s1` copies for x/y (~20 helper shapes tried), plus s16/s17 literal-pool order.
- FUN_00181e38 (StatueIdle): still 6 words (pd in s1 vs ROM s2; ~300 more combos: decl order, ternary/if-else, aliases).
- FUN_0019ae14 (FloorClosed): still 13 words (armcc folds 110.0f/40.0f into `sub r1,r1,#0xbc0000`; ~20 more shapes tried).
