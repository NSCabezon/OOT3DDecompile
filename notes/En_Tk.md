
<!-- merge 2026-10-14 18:26:21 -->
# En_Tk (G6, haiku stage) status

Matched (fastchk 0 words off, ws_check baseline):
- EnTk_Destroy (25): z_en_tk.cpp. Header EnTk now has skelAnimModel (0x102C), FaceAnimations at 0x1030, heap ptr (0x11FC).
- FUN_00186680 (11): moved in place in src/functions/functions_180000s.cpp (C, uses gSaveContext.infTable[13]).
- FUN_003158ac (24): in place in src/functions/functions_310000s.cpp (C).

Left as asm:
- FUN_00273eac (29): draft under #if 0 in functions_240000s.cpp. 19/31 words off (literal pool layout, Vec3f
  constant ordering, predicated call args). Variants tried: vector init orders, return/else control flow.
- FUN_00186540 (72): not attempted in this pass. Jump-table switch on Message_GetState (cases 0..5) with
  SET_INFTABLE bit writes at raw gSaveContext offsets (0x588858 base + 0x2BA) and Rupees/Message calls.
  Port source: tools/repos/oot/src/overlays/actors/ovl_En_Tk/z_en_tk.c (EnTk_UpdateTalkState).
- EnTk_Update (116): not attempted in this pass.

Build plumbing: functions_180000s.cpp and functions_240000s.cpp and functions_310000s.cpp now include global.hpp
(wrapped in extern "C" in 180000s and 240000s/310000s pattern as used there).

## G6 sonnet stage
- FUN_00186540 (EnTk_UpdateTalkState): MATCHED. Needs `switch (thisx->textId) { case 0x5018: case 0x5019: ... }` (ROM computes `subs r0,#0x5018; cmpne r0,#1`)
  and a `switch` for the 0x5028 test too; full N64 case list 0..9 (jump table).
- EnTk_Update: MATCHED (header typed to 3DS layout: actionFunc 0xB18, collider 0xB1C, eff[20] at 0xBCC, v3f_304 at 0xBC0, `eyeTextureIdx >= 3`).
- EnTk_Init: MATCHED. Needs `(Actor* thisx, GameState* state)` + `PlayState* play = (PlayState*)state` and RAW `state` for the FUN_0034fea8 call;
  `(u32)(dayTime - 0xC001) >= 0x1FFF` range test. Data via EQU: EnTk_sCylinderInit 0x52F92C, EnTk_sColChkInfoInit 0x52F964 (data_syms.s).
- EnTk_Draw: asm, draft #if 0 (~78/134 words). 3DS particle batch API (FUN_0035619c/00342988/003693b4/00371eac) guessed; ROM allocates self=r7, base(self+0x1000)=r8, play=sb
  (ours self=r8, base=r7) and keeps three scale stores before the `*=40` multiplies. EnTk_OverrideLimbDraw = `mov r0,#0; bx lr` at 0x2882EC (unlabeled, EQU).
