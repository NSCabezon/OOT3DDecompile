
<!-- merge 2026-10-14 17:50:37 -->
# Oceff_Wipe4 (haiku stage 1)

- OceffWipe4_Update: MATCHED (3.0f / SREG(30) * 50.0f > timer; literal is 50.0)
- OceffWipe4_Destroy: MATCHED (no nayrus part; tail reorder gives mov r0,r0)
- Init, Draw: still GLOBAL_ASM
- ws_check: baseline only

## sonnet stage 2
- OceffWipe4_Init: MATCHED (defaults first, if(params == 1) override; SetAnimType(0); dead alias s2 for obj store).
- OceffWipe4_Draw: NOT matched (~185 words, far): same blocker (draft #if 0).
