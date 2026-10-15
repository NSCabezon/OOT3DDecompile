
<!-- merge 2026-10-15 10:58:23 -->
# Bg_Hidan_Fwbig (group G29, haiku stage) — status

ws_check: baseline only (FUN_00249af8).

Matched (C):
- BgHidanFwbig_Destroy, BgHidanFwbig_Rise, BgHidanFwbig_WaitForCs, BgHidanFwbig_Lower, BgHidanFwbig_Move, BgHidanFwbig_Draw (3DS model draw, same shape as Bg_Hidan_Firewall)
- BgHidanFwbig_WaitForPlayer: the ROM code at 0x0010AB74 is the N64 WaitForTimer body (timer 225 frames via Lower). Name kept because functions.tsv / the linker use it.

Not matched (draft under `#if 0`, GLOBAL_ASM kept):
- BgHidanFwbig_WaitForSwitch: 5 words at 0x20..0x38. The action-func store and the -99 cutscene arg are scheduled in different registers; ~25 variants tried.

Splits applied:
- BgHidanFwbig_WaitForPlayer @ 0x0010ABAC -> FUN_0010abac (cfg tail = Bg_Hidan_Curtain BgHidanCurtain_WaitForTimer code, 76 B).

Not attempted (not in this batch): BgHidanFwbig_Init, BgHidanFwbig_Update (still GLOBAL_ASM).
