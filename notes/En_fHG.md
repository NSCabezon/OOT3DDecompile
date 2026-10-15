
<!-- merge 2026-10-13 19:21:58 -->
# En_fHG — solo barrido
Matched 2/10: EnfHG_Destroy, FUN_0023929c (Approach). Struct filled (N64 +0x58; SkelAnime @0x26C).
Near/far (drafts #if 0): FUN_00362ab4 SetupApproach 3w (timer vdiv reg), EnfHG_Update 8w (kill-path mov r0,r4), EnfHG_Draw ~46w (fog color clamp regs).
Static: EnfHG_Init (guarded loader 0x55A21C, LOADER_RECIPE). Big: FUN_00126438, FUN_00126f50, FUN_0013ec58, FUN_0017a63c.
Rodata 0x4D95B4 (anims + oppositeIndex aligned(4) struct) via EQU in data_syms.s.
