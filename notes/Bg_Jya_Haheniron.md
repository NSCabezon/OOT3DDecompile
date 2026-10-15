# Bg_Jya_Haheniron: stage 1 (Haiku), batch 1/1

| Function | Status | Notes |
|---|---|---|
| BgJyaHaheniron_Init | MATCHED (C) | fastchk 0/58 words; ws_check baseline |
| BgJyaHaheniron_Destroy | MATCHED (C) | fastchk 0/12 words; tail call to FUN_00350f34 kept |
| BgJyaHaheniron_Update | MATCHED (C) | fastchk 0/6 words |
| BgJyaHaheniron_Draw | MATCHED (C) | fastchk 0/26 words |
| BgJyaHaheniron_ChairCrumble | MATCHED (C) | fastchk 0/74 words; timer threshold 90 (N64 60, x1.5 for 3DS) |
| FUN_0036a154 (SpawnFragments) | MATCHED (C), in actor .cpp | fastchk 0/98 words; angle is `s32` loop-carried, computed after the first Rand call |
| BgJyaHaheniron_PillarCrumble | NOT LINKED (asm + draft under #if 0) | Draft matches fastchk (0/35 words). Blocker: function-local static Vector3f at 0x569A10 with guard 0x5128D8. Needs a scatter pin in data/oot3d.ld plus model_manager-style infra outside the actor dir. Link fails with L6224E without it. |
| BgJyaHaheniron_RubbleCollide | NOT LINKED (asm + draft under #if 0) | Same blocker as PillarCrumble: static Vector3f at 0x569A1C with guard 0x5128DC. Draft matches fastchk (0/43 words). |

Files: `z_bg_jya_haheniron.cpp`, `z_bg_jya_haheniron.hpp`, new `data_syms.s` (EQU for sObjIndex 0x5128E0, sJntSphInit 0x5128EC, sKakeraScales 0x5128FC, sInitChain 0x512908, sScales 0x51291C). Nothing outside the actor dir was touched; include/ untouched.

ws_check.sh Bg_Jya_Haheniron: baseline only (FUN_00249af8).
