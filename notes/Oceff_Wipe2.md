
<!-- merge 2026-10-14 17:49:41 -->
# Oceff_Wipe2 (haiku stage 1)

- OceffWipe2_Update: MATCHED (3.0f / SREG(30) * 100.0f > timer)
- OceffWipe2_Destroy: MATCHED (same as Oceff_Wipe)
- Init, Draw: still GLOBAL_ASM
- ws_check: baseline only

## sonnet stage 2
- OceffWipe2_Init: MATCHED (Wipe3 Init shape, cmb 0x35 / cmab 0x20).
- OceffWipe2_Draw: NOT matched (~170 words, far): same blocker as OceffWipe_Draw (draft #if 0).
