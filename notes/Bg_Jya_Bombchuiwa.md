
<!-- merge 2026-10-14 23:21:57 -->
# Bg_Jya_Bombchuiwa (G18, haiku stage) status

MATCHED (C):
- BgJyaBombchuiwa_Update (5 insns, tail call through actionFunc @0x1A4).
- BgJyaBombchuiwa_Destroy (C; virtual Remove via manager @0x55A1A8, shared with Bg_Jya_Bigmirror; the 5-arg FUN_00350f34 call uses a cast).
- FUN_003bce94 = func_808949B8 (moved from functions_3A0000s.cpp; GLOBAL_ASM removed). Includes SpawnLightRay inline (Actor_Spawn unk arg = 1).

NOT ATTEMPTED / OUT OF SCOPE: Init, Draw, WaitForExplosion (not in this batch).

DEPENDENCY NOTE: Destroy uses `extern BgJyaBigmirror_sManager` (EQU 0x0055A1A8). The main-tree Bg_Jya_Bigmirror/syms.s no longer defines it (changed on disk during this run) and shared_syms.s has no alias for it -> link will fail on merge until one is added.
A workspace-local EQU (syms.s) broke layout in the ws build; not kept.
Verification: fastchk only (0 words). ws_check currently fails for every workspace (main-tree data_chunks.txt / data/oot3d.ld changed 23:03).
