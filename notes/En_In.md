
<!-- merge 2026-10-14 18:15:25 -->
# En_In (haiku stage + sonnet stage G2)

MATCHED (C, ws_check baseline OK):
- EnIn_OverrideLimbDraw, EnIn_Destroy, EnIn_PostLimbDraw, FUN_003b8e48 (empty), FUN_00171660 (haiku)
- EnIn_Draw (2nd FaceAnimations call: separate `FaceAnimations* f2` local for the 2nd call)
- EnIn_Init (`thisx->params` on the params compare)
- FUN_00171370 (= UpdateTalkState with Closing/Choice/Event inlined as static inline; Event written as a one-case switch)
- FUN_003b8684 (= EnIn_WaitForObject, with StartingRace + GetStartMode inlined; 0/340 words; sCylinderInit/sColChkInfoInit/sHorsebackAnimations via EQU in data_syms.s)
- FUN_00105440 (= EndRentalPeriod; `u16 a = x | 0x800; store; u16 b = ...; store` for the two flag ORs)

UNMATCHED (GLOBAL_ASM kept, draft under #if 0 in z_en_in.cpp):
- EnIn_Update (23 words): Stagger float/flags regs (5) + Fidget loop numbering (ROM f=r0,i=r1,ptr=ip; ours f=r1,i=ip,ptr=r0)
- FUN_003b8bd4 (= EnIn_Racing, 144 insns): ROM is 1 insn longer; the `animationType == 0xF` A-block is not if-converted in ROM (bne;..;b), ours predicates it
- FUN_003c54f0 (= EnIn_RentalPeriod + RentalTimeExpired + StartTransition inlined, 5 words): ROM keeps the first eventInf store (horse type) and
  tail-merges the 2nd store with the else branch; ours drops the dead first store

Header: z_en_in.hpp now has typed fields (skelAnime@0x1A4, collider@0x400, interactInfo@0xD88, fidgetVec@0xDB0 ...).
