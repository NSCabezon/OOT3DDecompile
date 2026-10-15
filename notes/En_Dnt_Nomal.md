
<!-- merge 2026-10-13 19:38:43 -->
# En_Dnt_Nomal (solo barrido, Opus 2026-10-13)
Matched 20/29: Destroy + 19 action FUN_s moved into actor .cpp (struct fully mapped: N64 0x258.. block = 3DS -0x70; curFrame accessor in z_en_dnt_nomal_anim.cpp; anim idx globals via EQU data_syms.s).
Near: FUN_00259440 WaitForObject 2w (type ldrh r0 vs r1), FUN_0021cde4 SetupTargetTalk 5w (play/anim ptr r6/r7 swap).
cfg: EnDntNomal_Init (ROM symbol includes trailing `return 0` stub @0x249364 = OverrideLimbDraw used by DrawStage; draft 1 insn off), FUN_0028033c DrawStage (uses 0x249364), FUN_0038639c DrawTarget (override fn 0x37e448 unlabeled inside FUN_0037e434).
Big (not attempted): EnDntNomal_Update, FUN_00177dd0 TargetWait, FUN_00174efc StageCelebrate, FUN_001990c8 StageDance.
- 2026-10-15 R9 MakeScale (Opus): FUN_0038639c GLOBAL_ASM moved into z_en_dnt_nomal.cpp beside draft (uses MTX34_MakeScale), 35w: frame + both store blocks match, one insn short (missing zero re-mov).
