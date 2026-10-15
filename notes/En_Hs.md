# En_Hs — stage 3 (Opus closing pass)
- EnHs_Init: MATCHED (fastchk 0/77, ws_check baseline only). Fix: `self->actor.targetMode = 6` instead of `thisx->targetMode`
  (with thisx-> armcc hoists/merges both actionFunc stores and puts 6 in r1). N64 static inline SetActionFunc helper in both branches.
- EnHs_PostLimbDraw: skipped (function-local static + __cxa_guard; same as En_Hs2), stays asm.
- All other functions already matched (C) in main tree.
