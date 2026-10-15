# Bg_Spot16_Doughnut (stage 1, Haiku)

| Function | Status | Notes |
|---|---|---|
| BgSpot16Doughnut_Destroy | matched (C) | tail call to FUN_00350f34 via 4-arg cast |
| BgSpot16Doughnut_Update | matched (C) | |
| BgSpot16Doughnut_Draw | matched (C) | |
| FUN_003a7b68 (expanding draw) | matched (C), moved from functions_3A0000s.cpp | only referenced by Init |
| FUN_003a7bf0 (expanding update) | matched (C), moved from functions_3A0000s.cpp | only referenced by Init |
| BgSpot16Doughnut_Init | NOT matched, left as GLOBAL_ASM | draft under `#if 0`; ROM is 8 bytes (one nop + ble) longer. Tried ~7 switch/case orderings and the fireFlag tail shape; none closed the gap |

Debt: raw data addresses for sInitChain (0x513E4C) and sScales (0x513E58) in the #if 0 draft; raw offsets for play->sceneId (+0x104), play+0x107, csCtx.actorCues[2] (+0x22E4).

## Stage 2 (Sonnet)
BgSpot16Doughnut_Init: still NOT matched. Draft matches every instruction except the switch (ROM has `cmp #0x51; beq; nop; ble default`
before the linear 0x52/0x63/0x6b tests = armcc binary partition with empty lower half). ~40 variants tried (case/label order,
stacking, extra default-equal/empty/same-body cases low+high, s32/s16/u16 locals, cast forms); a 4-case switch always compiles
linear, extra distinct cases produce a full binary tree (bigger). Left as GLOBAL_ASM.

## Stage 3 (Opus)
BgSpot16Doughnut_Init: **matched (C)**. Shape: `if (scene == 0x51) goto big; else if (scene <= 0x51) goto def;` then a
switch {0x6B: big: uncull; default: def: SetScale(0.1); 0x52; 0x63}. The scene local MUST be in its own `{}` block
ending before the fireFlag if/else (otherwise the tail compiles to orreq/bicne, +4 B). `play->unk_107[0]` breaks it
(3 words) -> kept raw `*(u8*)((u8*)play + 0x107)`. sInitChain/sScales now EQU symbols in actor-dir `data_syms.s`
(no more raw-address defines). ws_check: baseline only.
