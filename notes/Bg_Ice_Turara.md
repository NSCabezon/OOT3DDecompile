
<!-- merge 2026-10-14 18:16:11 -->
# Bg_Ice_Turara (haiku stage, G2)

MATCHED (C in z_bg_ice_turara.cpp, ws_check baseline OK):
- BgIceTurara_Update (2), BgIceTurara_Wait (11), BgIceTurara_Regrow (13), BgIceTurara_Destroy (16),
  BgIceTurara_Stalagmite (17), BgIceTurara_Draw (19), BgIceTurara_Init (58, 0/63 words; actor->unk_19B store),
  BgIceTurara_Fall (68, 0/72 words; calls Actor_MoveForward symbol, FUN_0036b940/FUN_0036d15c for DynaPoly enable/disable)

NEAR-MISS (draft under #if 0, GLOBAL_ASM kept):
- BgIceTurara_Shiver (72): 18 words, VFP temp reg for the shiver offset (ROM t in s18, ours s17); % 6 timer, not % 4

BLOCKED (GLOBAL_ASM kept, draft under #if 0):
- BgIceTurara_Break (86): ROM uses a function-local static (`accel`, guard 0x512160 / obj 0x5699F8) => __cxa_guard_acquire.
  Needs LOADER_RECIPE-style pinning of the guard + object (orchestrator-only). Draft is 60 words off because of that.

Data: src/game/actors/Bg_Ice_Turara/data_syms.s (new): EQU sCylinderInit=0x51216C, sInitChain=0x5121A4.

Sonnet G2: BgIceTurara_Shiver still 18 words after ~40 variants: ROM numbers t1=s18/t2=s17 (we get s17/s18) and loads pos AFTER the sign vcvt (s0 free, `vmov s0,r0; vcvt s1,s0`); ours hoists the vldr before cmp. Decl order, sign as s32/f32/if-else, static inline helper (worse) did not change it.
