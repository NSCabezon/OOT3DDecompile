
<!-- merge 2026-10-14 18:52:16 -->
# En_Zl1 (G8, sonnet stage)

Matched in C (ws_check baseline only): EnZl1_Destroy, EnZl1_PostDrawLimb, EnZl1_OverrideLimbDraw, EnZl1_Draw,
EnZl1_Update, EnZl1_Init, FUN_001467dc (moved), FUN_003adfac (moved). Header typed (skelAnime/faceAnims/actionFunc/collider).
Actor-local EQUs in data_syms.s (eye idx table 0x4D9624, cue anim idx tables, letterbox 0x549600, cylinder init 0x5258E0).

Drafts under #if 0 (GLOBAL_ASM stays in functions_*.cpp):
- FUN_003ad010 (N64 func_80B4B010): 28 words off. self r4/base r5 swapped vs ROM, VFP numbering of 3 Vec3f inits, hoisted 30.0f.
- FUN_001610c4 (func_80B4BC78): 41 words off. Everything lines up except ROM keeps `cue` in r4 and `self` in r5.
- FUN_003ac060 (func_80B4B8B4): ~55 words off. Same self/cue swap + hoisted 70.0f/0.0f/1.0f VFP numbering.
- FUN_003f7848 (func_80B4BF2C): ~146 words off (jump table, code is DCB blob). ROM cross-jumps every `strh unk_452` into one block
  and loads ldrsh unk_452 before the player.
- FUN_003ad41c (func_80B4B240): ~266 words off, big (10-case jump table in DCB blob; 25.0f hoisted into s16 in ROM).
