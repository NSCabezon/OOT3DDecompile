
<!-- merge 2026-10-15 16:37:28 -->
# Oceff_Spot (G33, Haiku + Sonnet passes)

- OceffSpot_Wait / GrowCylinder / End / Destroy: MATCHED (Haiku).
- OceffSpot_Update: MATCHED (Sonnet, 0/140). Only needed `PlayState* play2 = play;` used for the GET_PLAYER read (gen.py single-site search).
  FUN_0036bee0 = Environment_AdjustLights(play, temp*0.5, 800.0, 0.0, 0.9) on 3DS.
- OceffSpot_Draw: MATCHED (Sonnet, 0/118). SetUnkAC(1)-in-r6 recipe: the matrix rows are read/written through a row view with
  `operator[]` (`MRow`, `R(&mtx, row)[col]`) for ALL rotation accesses -> the constant index 1 stays live in r6 (shared with the
  SetUnkAC(1)/unk_AD stores) and the frame becomes push {r4-r7,lr}/0x34. Then `Camera_GetCamDirYaw(camera) - thisx->shape.rot.y`
  (thisx, not self->actor) fixes the ldrh/sub schedule.
- OceffSpot_Init: NOT MATCHED, 8/201 words off, left as GLOBAL_ASM with the C draft under #if 0. Everything matches except zar/cmb
  callee-saved registers (ROM zar=r8, cmb=r7; ours swapped). ~35 variants + greedy/pair single-site search (s2, play2, thisx,
  decl order, local forms) did not move it. Draft needs `OceffSpot_sInitChain EQU 0x00535E30` (kept in data_syms.s).
- gTimeSpeed EQU moved to src/game/shared_syms.s (ws); data_syms.s keeps only _ZTI14OceffSpotModel + OceffSpot_sInitChain.
- ws_check.sh Oceff_Spot: baseline only (FUN_00249af8).
