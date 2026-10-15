
<!-- merge 2026-10-14 19:06:32 -->
# En_Dodojr (haiku stage, G10) status

ws_check: baseline only (FUN_00249af8), 0 non-function bytes.

## Matched (17/20)
- Actor dir: EnDodojr_Init, EnDodojr_Destroy, EnDodojr_Draw
- Moved to z_en_dodojr.cpp (GLOBAL_ASM removed from functions_*.cpp):
  FUN_003b7c64 (DropItem), FUN_003d069c (JumpAttackBounce), FUN_003d05e4 (EmergeFromGround),
  FUN_00104594 (EatBomb), FUN_0035d0bc (UpdateBounces), FUN_0013336c (StandardDeathBounce),
  FUN_0016e964 (StunnedBounce), FUN_00194634 (SwallowedBombDeathBounce), FUN_00104648 (WaitFreezeFrames),
  FUN_003d0744 (Stunned), FUN_00219450 (WaitUnderground), FUN_00133434 (DeathSequence),
  FUN_0019454c (DeathSequence copy, SwallowedBombDeathSequence), FUN_001c429c (SwallowBomb)

## Not matched (left as GLOBAL_ASM, draft under #if 0)
- FUN_003b7cb4 (Despawn): 8 words. Timer rounding (2/3 scale, +/-0.5 select) reg/const order; ~16 variants.
- FUN_003179d0 (SpawnLargeDust): 12 words. play in r8 vs ROM r7; const s17/s18 swapped; division
  must be FUN_00368d94 (the `/` form links against __aeabi_uidivmod and fails).
- EnDodojr_OverrideLimbDraw: 54 words, 12-byte size gap (limb-1 scale copies via vmov).

## Notes
- 3DS layout: skelAnime 0x1A4, actionFunc 0x498, collider 0x49C, bomb 0x4F4, headPos 0x4F8,
  dustPos 0x504, counter/stunTimer/freezeFrameTimer/timer/crawlSfxTimer 0x510..0x518, rootScale 0x51C.
- colorFilterTimer is u16 at actor+0x11A (no header field; raw macro in the .cpp).
- Data refs via data_syms.s EQUs: sCylinderInit 0x5226E4, sColChkInit 0x52271C.

## Sonnet stage (G10)
- MATCHED: EnDodojr_Update (inlined CheckDamaged/UpdateCollider, first try), FUN_003b7cb4 (`t = (s32)((timer * 2.0f / 3.0f) +/- 0.5f)` in if/else, no f32 const locals).
- UNMATCHED: EnDodojr_OverrideLimbDraw 54 words (ROM adds a vmov copy of the x/z scale per column-0 product, 12 B; same blocker as En_Poh PostLimbDraw, ~25 variants).
- UNMATCHED: FUN_003179d0 12 words (guarded + FUN_00368d94 step; play r8 vs r7, s17/s18 swap). Plain `/` form matches in fastchk but links __aeabi_uidivmod (L6200E).
