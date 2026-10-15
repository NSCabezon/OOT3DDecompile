# En_Guest — Opus closing pass
All functions matched; ws_check baseline only (FUN_00249af8).
- EnGuest_Init: MATCHED — Actor_Kill(thisx) via param; `if (slot < 0) return;` (stripped N64 assert branch) keeps the sxtb.
- EnGuest_Destroy: MATCHED (earlier)
- EnGuest_Update: MATCHED — flags/ProcessInitChain via `thisx->`; callee is Collider_SetCylinderType1 (draft wrongly used Collider_SetCylinder).
- FUN_00210678 (draw): MATCHED (earlier)
- FUN_002108ac (update action): MATCHED, moved from functions_200000s.cpp — yOffset written as ternary `LINK_IS_ADULT ? 10.0f : 20.0f` produces the armcc `nop` (e320f000).
