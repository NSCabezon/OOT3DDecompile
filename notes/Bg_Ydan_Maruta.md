# Bg_Ydan_Maruta: status (stage 1, Haiku)

ws_check.sh: only the baseline (FUN_00249af8) differs.

## Functions (6 of 7 matched)
| Function | 3DS name | Where | Status |
|---|---|---|---|
| BgYdanMaruta_Destroy | | actor .cpp | matched |
| BgYdanMaruta_Update | | actor .cpp | matched |
| BgYdanMaruta_Draw | | actor .cpp | matched (needs `SetUnkAC(1)` + `&self->dyna.actor.modelMtx`; `unk_AC = 1` variant mismatched) |
| BgYdanMaruta_DoNothing | FUN_001ca96c | actor .cpp (moved, GLOBAL_ASM removed from functions_1C0000s.cpp) | matched |
| func_808BEFF4 (spike roll) | FUN_00128194 | actor .cpp (moved, GLOBAL_ASM removed from functions_120000s.cpp) | matched |
| func_808BF078 (wait for AC hit) | FUN_001ca970 | actor .cpp (moved, GLOBAL_ASM removed from functions_1C0000s.cpp) | matched |
| func_808BF108 (shake) | FUN_001ca9fc | actor .cpp (moved, GLOBAL_ASM removed from functions_1C0000s.cpp) | matched (timer is s16; `homeX + temp*cos` operand order) |
| BgYdanMaruta_Init | (asm/BgYdanMaruta_Init.s) | actor .cpp | NOT matched: left as GLOBAL_ASM; no draft yet |

Not moved: func_808BF1EC (ladder fall) = FUN_001ca91c (80 B, in functions.tsv). Only reached through FUN_001ca9fc's
actionFunc store, so it was left in functions_1C0000s.cpp as GLOBAL_ASM (not attempted, out of budget).

## Init (open)
- Init uses data tables from the data dump (`GLOBAL_ASM("data/z_Bg_Ydan_Maruta.data.s")`): ColliderTrisInit
  sTrisElementsInit / sTrisInit / sInitChain and gDTFallingLadderCol. They need symbols or C definitions after
  `_InitVars` before a C Init can reference them.
- Asm reads: params (+0x1C) split into switchFlag (+0x29E, low byte) and params>>8; `FUN_00372f38(actor, play,
  &model, idx, 0)` with idx from a 2-byte table {3,7}; two branches (spike: actionFunc=FUN_00128194; ladder:
  DynaPolyActor_Init + DynaPoly_SetBgActor + home.y -= 280).
- Not attempted for lack of time.

## Layout (3DS)
- DynaPolyActor (0x1BC) → actionFunc 0x1BC, skelAnimModel 0x1C0, collider (ColliderTris) 0x1C4, colliderElements
  0x1E4 (2 × 0x5C), unk_29C (s16 timer) 0x29C, switchFlag 0x29E. Size 0x2A0.
- Collider types (ColliderTris, ColliderTrisInit, ...) copied locally from Bg_Haka_Sgami (not in shared headers).
- Prototypes declared locally in the .cpp: Collider_DestroyTris, CollisionCheck_SetAT/AC, Flags_SetSwitch,
  OnePointCutscene_Init, FUN_00373264, FUN_00372244, FUN_00374bb8, FUN_001ca91c/9fc.

## Files touched (ws only, nothing in oot3d/)
- ws/Bg_Ydan_Maruta/src/game/actors/Bg_Ydan_Maruta/z_bg_ydan_maruta.cpp
- ws/Bg_Ydan_Maruta/src/game/actors/Bg_Ydan_Maruta/z_bg_ydan_maruta.hpp
- ws/Bg_Ydan_Maruta/src/functions/functions_120000s.cpp (1 GLOBAL_ASM line removed: FUN_00128194)
- ws/Bg_Ydan_Maruta/src/functions/functions_1C0000s.cpp (3 GLOBAL_ASM lines removed: FUN_001ca96c, FUN_001ca970, FUN_001ca9fc)
- include/: no changes.
