# En_M_Fire1 (Haiku stage 1)

Actor dir: `src/game/actors/En_M_Fire1/` (z_en_m_fire1.cpp, .hpp, sCylinderInit.s)
Baseline check: `ws_check.sh En_M_Fire1` shows only FUN_00249af8 (ok).

| Function | Status | Notes |
|---|---|---|
| EnMFire1_Init | MATCHED (C) | Calls `FUN_00372f38` with 3 args (cast to 3-arg proto, header proto has 5). `Actor_ChangeType` for params < 0. Cylinder init via `sCylinderInit`. |
| EnMFire1_Destroy | MATCHED (C) | Calls `FUN_003508b8(actor, NULL)` (cast, header proto has 3 args), then `Collider_DestroyCylinder`. 36 B, same as asm. |
| EnMFire1_Update | NOT MATCHED, left as asm | C draft under `#if 0`. First 0x58 bytes of the C version match ROM byte-for-byte. functions.tsv span is 504 B (0x2B1898..0x2B1A90) and includes an orphan 0x1A0-byte blob at 0x2B18F0 (no references in the dump). Dropping it from the link causes ~13k L6221E overlaps. Tried moving the blob into a separate asm file in the actor dir (same section name): still broken. Needs cfg split of functions.tsv. |

Data:
- `sCylinderInit` lives in the data dump `z_En_M_Fire1.data.s` at 0x0052C044 (kept as GLOBAL_ASM). C refers to it via an absolute symbol `sCylinderInit EQU 0x0052C044` in `sCylinderInit.s` (same pattern as En_Okarina_Effect gWeatherMode). Defining it in C instead shifted the whole link (7k+ diffs), so don't.

Header: `EnMFire1` now has `ColliderCylinder collider` at 0x1A4 and `f32 timer` at 0x1FC (size 0x200).

Files touched: only `src/game/actors/En_M_Fire1/` inside this workspace. No include/ or functions_*.cpp changes.

UNMATCHED stays: EnMFire1_Update.
