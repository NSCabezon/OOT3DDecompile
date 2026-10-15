# En_Pu_box — STATUS (cascade stage 1, Haiku)

Actor dir: `src/game/actors/En_Pu_box/` (z_en_pu_box.cpp, z_en_pu_box.hpp)

| Function | Status | Notes |
|---|---|---|
| EnPubox_Init | MATCHED | fastchk 0/85 words differ, ws_check baseline only |
| EnPubox_Destroy | MATCHED | fastchk 0/12 words differ |
| EnPubox_Update | MATCHED | fastchk 0/73 words differ |
| EnPubox_Draw | MATCHED | fastchk 0/17 words differ |

Matched: 4/4. Actions: none (this actor has no action funcs; it is a static stone cube).
Files touched outside the actor dir: none. `include/` untouched.
Header: `EnPubox` spelled out field-by-field (not `DynaPolyActor`) because Update loads unk_158 as u16 (`ldrh`).

Layout facts used (3DS vs N64):
- dyna.bgId 0x1A4, unk_150/154/158 -> 0x1A8/0x1AC/0x1B0, interactFlags 0x1B4, transformFlags 0x1B8, unused_164 -> 0x1BC, skelAnimModel 0x1C0.
- Init stores: unused=1, uncullZoneDownward=1200 (0x104), uncullZoneScale=720 (0x100) before colChkInfo radius/height; transformFlags before interactFlags; FUN_00372f38 before DynaPolyInfo_Alloc.
- Update: world.rot.y = unk_1B0 must be stored BEFORE speedXZ += unk_1A8.
- Audio call: `Audio_PlaySoundGeneral(0x01000161, &world.pos, 4, &FLOAT_0054ac20, &FLOAT_0054ac20, &DAT_0054ac24.unk_0)`.
- N64 `Actor_MoveXZGravity` maps to `Actor_MoveForward` here (same asm call).
- Actor_UpdateBgCheckInfo flags = 0x1D.

ws_check.sh: only FUN_00249af8 differs (baseline).
UNMATCHED: none
