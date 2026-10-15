# Demo_Du (Haiku stage 1) status

| Function | Status | Notes |
|---|---|---|
| DemoDu_Destroy (0x1aa91c) | MATCHED (C) | Tail FUN_001aa92c (add r0,r4,#0x228 + tail call) folded in: it is the second half of Destroy. `FaceAnimations::Destroy` tail. GLOBAL_ASM for FUN_001aa92c removed from src/functions/functions_180000s.cpp. |
| DemoDu_Update (0x1f0314) | MATCHED (C) | Dispatch via jump table 0x51B4C4 (raw address, debt). Action fns (29 entries, caseD_/FUN_ in functions_*.cpp) NOT moved: cfg-split + many shared, outside ~15 limit. |
| DemoDu_Draw (0x1f02ec) | MATCHED (C) | Dispatch via jump table 0x51B538 (raw address, debt). Draw fns (caseD_0_0027cf10-ish, 0x2a045c, 0x28e140) left as asm. |
| DemoDu_Init (0x1aa5bc) | NOT MATCHED (asm) | Draft in `#if 0` (switch form). 158/216 words differ: armcc hoists `mov r7,#0` / `mov r6,#3` out of the switch, ROM keeps them as shared values across the 2/3/default paths; register allocation differs. Not solved in 4 variants (plain if-chain, no hoisted skel, switch). |
| data z_Demo_Du.data.s | GLOBAL_ASM (kept) | |

Open leads for Sonnet:
- Init: ROM order is `cmp 1 / beq A; cmp 2 / mov r7,#0 / beq B; cmp 3 / mov r6,#3 / bne Default; [path 3]`. Try writing path 2/3/default with explicit `s32 zero = 0; s16 three = 3` locals declared before the chain, or N64-style nested if.
- Action functions for Update (updateIndex 0..28) and Draw (0..2) are the bulk of the actor. They need a cfg split; not attempted.
- Struct (header): unk_1A4 (FaceAnimations-related, skel at 0x1A4, face at 0x228), updateIndex 0x3FC, drawIndex 0x400, unk_3F4/3F8 s16.

## Sonnet stage 2
- DemoDu_Init: still NOT matched (best 158/216 words differ with plain switch; draft kept under #if 0). Branch order, 0/3 constant hoisting and per-path epilogues already match ROM. Remaining blocker: armcc hoists `add r6,r4,#0x300` as a shared base for the 0x3F4/0x3F8 s16 stores (ROM uses `mov r0,#0x3f8; strh r6,[r0,r4]`), costing one callee-saved reg and shifting allocation (lr used for p). Tried ~9 variants: per-case static helpers (tails merge), return vs break, ActorShape* local (global/per-case), raw s16 casts, volatile, N64 SetEyeTexIndex/SetMouthTexIndex inline helpers. 0x3F4/0x3F8 are N64 eyeTexIndex/mouthTexIndex.
- Action functions not attempted (cfg split + shared, see stage 1 notes).

## Opus stage 3
- DemoDu_Init: still NOT matched, left as GLOBAL_ASM; new draft under `#if 0` in z_demo_du.cpp: 216/216 words (size now equal), 13 words differ (was 158-165).
  - Key finding (solves the 0x300-base blocker): write eye/mouth via `s16* p = &self->unk_3F4; *p = v;` inline helpers -> armcc emits ROM's `mov r0,#0x3f4; strh rX,[r0,r4]` per store, no shared base. Same idiom in DemoSa_Init and caseD_9_003858a0 (Demo_Du action).
  - Draft also had wrong yOffset (0.0f): N64 is -10000.0f (literal 0xC61C4000 in ROM pool).
  - Per-case `ActorShape* shape` locals; skel as helper param for cases 2/3, computed inside helper for 1/default.
  - Remaining diffs: case 3 cmb/p reg swap (ip/fp) + 0x18 in r0 vs r1; default path schedules yOffset vstr after the strh's (N64 statement order fixes schedule but swaps shape/3 and zar/skel regs). ~460 permutations of statement order/helper forms/case order tried.
