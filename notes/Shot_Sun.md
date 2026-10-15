# Shot_Sun (Haiku stage 1) - status

Workspace: ws/Shot_Sun (mkws OK). ws_check.sh: baseline only (FUN_00249af8). Data bytes: 0 differing.

| Function | Status | Notes |
|---|---|---|
| ShotSun_Destroy | MATCHED (C) | `params & 0xFF`, Collider_DestroyCylinder |
| ShotSun_Update | MATCHED (C) | tail call through actionFunc (+0x1FC) |
| FUN_0038ce68 | MATCHED (C) | Vec3s -> Vec3f into ColliderCylinder dim.pos (+0x4C..+0x54) |
| ShotSun_Init | NOT MATCHED, asm | C draft under #if 0. Ops are right; compiler picks r0 instead of r1 for flag temps and lays the else block out-of-line (ROM shares one `str r0,[r4,#4]` tail). Tried 6 layouts (if/else swap, flags in local u32, combined |=, early assign). Fairy branch (params 0x40/0x41) calls FUN_00142894 as actionFunc. |
| ShotSun_UpdateHyliaSun | NOT MATCHED, asm | 700 B, 3DS-specific (FUN_00372244 / Audio_PlaySoundGeneral sfx, direct gSaveContext reads at 0x587958, inline sun-position math). C draft under #if 0 (N64 logic), not iterated. |
| FUN_00142894 | NOT ATTEMPTED | 580 B, lives in src/functions/functions_140000s.cpp. Only referenced by ShotSun_Init as the fairy-spawner action (N64 ShotSun_UpdateFairySpawner equivalent). Candidate for move-in, but large and not checked. |

Notes:
- Data `data/z_Shot_Sun.data.s` (sCylinderInit at 0x5495BC) stays GLOBAL_ASM; Init draft refers to sCylinderInit by name only inside #if 0.
- Header ShotSun now has ColliderCylinder @0x1A4, actionFunc @0x1FC (ShotSunActionFunc), fairySpawnerState @0x208; size 0x210.
- No files outside src/game/actors/Shot_Sun touched. No include/ edits.
- Fairy spawner functions from N64 (SpawnFairy/TriggerFairy/UpdateFairySpawner) are not separate functions in the 3DS build (not in functions.tsv).
