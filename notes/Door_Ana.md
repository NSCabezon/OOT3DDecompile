
<!-- merge 2026-10-14 18:25:37 -->
# Door_Ana (G6, haiku stage) status

Matched (fastchk 0 words off, ws_check baseline):
- DoorAna_Update (2), DoorAna_Destroy (12), DoorAna_GrabLink (28), DoorAna_WaitClosed (64)
- FUN_00189628 (6): moved in place in src/functions/functions_180000s.cpp (C, needs global.hpp include there)
- FUN_001ce864 (15): moved into z_door_ana.cpp (GLOBAL_ASM line removed from functions_1C0000s.cpp)
- FUN_0027554c (23): moved into z_door_ana.cpp (GLOBAL_ASM line removed from functions_240000s.cpp)

Left as asm (draft under #if 0 + GLOBAL_ASM):
- DoorAna_WaitOpen (102): 4 words off, only the Math_StepToF float args. ROM loads target 0.0095f into s0 first,
  armcc emits the step load first. Tried ~20 variants (decl/assign order, wrapper helper, locals). Attention block matches.
- DoorAna_Draw (44): 38/46 words off. MTX34 translation stores and the shared constant-1 register (ROM `mov r5,#1`
  reused for SetUnkAC) not matched yet.

Header: z_door_ana.hpp now types collider (0x1A4), actionFunc (0x1FC), model (0x200), switchFlag (0x204); size unchanged 0x208.
Data: new data_syms.s with DoorAna_sGrottoEntrances EQU 0x004D87DC.
Not in this group's list (untouched): DoorAna_Init (GLOBAL_ASM).

## G6 sonnet stage
- DoorAna_WaitOpen: MATCHED (0 words). Fix: `f32 a, b; a = 0.0095f; b = 0.00094999996f;` before Math_StepToF (rounded literal for the
  step: 0.00095f gives 0x3a79096c, ROM has 0x3a79096b) + `{ u32 f = player->stateFlags1; player->stateFlags1 = f | 0x80000000; }` for the final flag set.
- DoorAna_Draw (44 insns): still asm. Best shape: DaVec `operator[]` helper (push {r4,r5,lr}, 0x3c frame, `mov r5,#1`) but ROM builds
  the identity+translate matrix with INTEGER-register stores (u32 puns reproduce them, not kept). Same class as Oceff_Wipe/Bg_Toki_Hikari. Draft #if 0.
- DoorAna_Init (130 insns): C draft under #if 0 (~100/137 words off). Structure OK (switch on params -> switchFlag; needs
  `DoorAna_sCylinderInit EQU 0x0051C538`); ROM keeps each case as predicated `moveq r1,#K; streq r1,[switchFlag]; beq` into the shared SetScale block, ours
  cross-jumps the stores. ~15 variants tried (flag local, dup bodies, thisx stores, signatures).
