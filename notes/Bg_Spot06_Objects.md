
<!-- merge 2026-10-15 09:39:24 -->
# Bg_Spot06_Objects (G25, haiku stage)

Matched (C in actor .cpp, GLOBAL_ASM removed from functions_*.cpp):
- BgSpot06Objects_Update (15 insns), BgSpot06Objects_Destroy (35 insns, was asm in actor dir)
- FUN_0019fe24 (19 insns) -> moved into actor .cpp (name kept)
- FUN_00182158 (38 insns) -> moved into actor .cpp (name kept). Cfg split applied: head 0x00182158..0x001821fc (164 B), tail FUN_001821fc (asm).
  Note: first split attempt at 0x1821f4 was wrong (the 0x3e060a92 float constant of the head pool lives there); redone at 0x1821fc.
  Constant: `(M_PI / 16.0f) * 2.0f / 3.0f` (= 0x3e060a92), 3DS 2/3 phase scale.

Not matched (draft under #if 0 in actor .cpp, GLOBAL_ASM kept in functions_*.cpp):
- FUN_0019f87c (38 insns, WaterPlaneCutsceneRise): 11 words off. Draft matches the body; diff is prologue register
  order (ROM `mov r5,r1` (play) first, self moved into r4 late) and the reload of lakeHyliaWaterLevel after the pos.y store
  is only reproduced with the `Actor* thisx = &self->dyna.actor` alias. ~8 variants tried.
- FUN_00182064 (51 insns, LockPullOutward): 4 words off. Diff is the actionFunc / flags store ordering
  (ROM loads FUN_001288fc into r2 before the flags clear, ours into r0). ~12 variants tried.
- FUN_00159930 (113 insns, LockWait): big. Head is ~528 B of C vs ROM; also a cfg tail (push at 0x159B2C).
  Register numbering differs (ROM self in r5, loop counter r4). Signature variants tried (8), 83 words off over the 1588-B tsv range. Left.

Other facts:
- Struct BgSpot06Objects size 0x248 (sizeof used by ActorInit; a 0x244 size broke ws_check non-function bytes).
- Local JntSph collider typedef in the header (repo has none yet).
- gameplayFrames (play+0x5BF4) read via raw-offset helper (repo PlayState lacks the field).
- Sfx: FUN_0019fe24 / FUN_0019f87c use the standard Audio_PlaySoundGeneral(..., &FLOAT_0054ac20, ...) tail.
- ws_check.sh Bg_Spot06_Objects: baseline only (FUN_00249af8).

## Sonnet stage (G25)
Matched (C in actor .cpp, GLOBAL_ASM removed from functions_*.cpp): FUN_0019f87c (all pos accesses through `Actor* thisx`),
FUN_00182064 (dead `s2` alias for the actionFunc store; LockSpawnBubbles is a plain `static`, not inline),
FUN_001288fc (dead `s2` alias on pos.y += vel.y and flags clear), FUN_00159930 (head, after the cfg split; dead s2/s3/thisx aliases +
`((BgSpot06Objects*)thisx)->actionFunc = FUN_00182064`; FUN_00372244 is the chime call, not Audio_PlaySoundGeneral),
BgSpot06Objects_Draw (case 0/3 as separate arms; `BgSpot06Objects_PlayByte(play, off)` with `u8* q = (u8*)play + off` gives the
literal+register-offset load; room pair pointer as a local; EQU BgSpot06Objects_sDrawColor 0x4D71DC in data_syms.s).
cfg split applied: FUN_00159930 0x00159b2c FUN_00159b2c (tail stays asm).
Not matched: BgSpot06Objects_Init (306 insns, far). Draft under #if 0: dispatch/cases are right, but ROM hoists 0x1F into fp and
-1313.0f into s16 in the prologue, keeps one shared "open" body per case, and uses the mixed GetCMABByIndex r2 shape; ours hoists 1 instead.
