
<!-- merge 2026-10-14 22:07:38 -->
# Bg_Hidan_Kowarerukabe (G13, haiku stage) - status

- BgHidanKowarerukabe_Destroy (16 insns): MATCHED (`FUN_00350f34` 3-arg form, Collider_DestroyJntSph).
- BgHidanKowarerukabe_Draw (23 insns): MATCHED (MTX34CopyAsm, SetUnkAC/FUN_003721e0/FUN_00372170, Collider_UpdateSpheres(0, collider, &mtx) inside the model-null guard).
- BgHidanKowarerukabe_Init (101 insns): NOT MATCHED. Draft under `#if 0` (~76 words off in fastchk; partly expected because fastchk cannot see the real ReadCollisionHeaderFromZsi call vs ROM's inlined `str`). Header typed: collider 0x1BC, elements 0x1DC, model 0x230. Data (EQU candidates, not wired): model index table 0x511B08, dyna info table 0x511B2C, JntSph init 0x511B1C, init chain 0x511B68, sphere radii (s16) 0x511B40, sphere Y (s16) 0x511B4A, Y offsets (f32) 0x511B54. Open: colHeader stack-slot placement and register order of the param (Actor*/PlayState* variants both tried).
- Stage2: Init draft now 20 words off (only r0/r1 swap in tail table ladder); syms.s created (not wired, draft under #if 0).
