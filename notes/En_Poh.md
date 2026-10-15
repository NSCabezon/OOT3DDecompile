
<!-- merge 2026-10-14 15:42:36 -->
# En_Poh cascade stage 1 (Haiku), batch 1/5

Matched (C in src/game/actors/En_Poh/z_en_poh.cpp, GLOBAL_ASM removed from functions_*.cpp):
- EnPoh_Destroy
- FUN_001cd5f8
- FUN_001807a0
- FUN_0013f9c4
- FUN_0021d620 (curFrame read via z_en_poh_anim.cpp accessor, armlink-inlined)

Not matched:
- FUN_00238c38: 5 words off (ROM loads fn literal into r1 and 0x920 base into r0; ours swaps them). Tried 7 variants (store order, timer via pointer/block, static inline setter, local timer, read-back). Draft under #if 0, GLOBAL_ASM kept.

Batch 2/5 (cascade stage 1, Haiku):
- Matched, moved into actor dir (GLOBAL_ASM removed from functions_*.cpp):
  - FUN_0036f32c (z_en_poh_anim.cpp; same-TU inline would hit FUN_0013f9c4, ROM calls it)
  - FUN_003e3f70 (Idle, z_en_poh.cpp)
  - FUN_0010abf8 (N64 func_80ADEF38 appear, z_en_poh.cpp; curFrame/playSpeed via accessors)
  - FUN_00120388 (N64 func_80ADEECC hurt/knock, z_en_poh.cpp; Animation_MorphToLoop = 0x370350)
  - FUN_0011c3f4 (N64 EnPoh_Attack, z_en_poh.cpp; zero store via `char* flag` pointer)
- Not matched (GLOBAL_ASM kept, draft under #if 0):
  - FUN_0036f364 (N64 EnPoh_MoveTowardsPlayerHeight, z_en_poh_anim.cpp): 4 words off. Constants as locals after the
    Math_StepToF call hoist the pool loads like ROM, but load order (s2=2.0, s1=1/3) and pool order (2.0, 1/3, 0.5)
    disagree with the declaration order that gets the registers right. Field unk_91D (0x91D) typed in header.
  - FUN_00175170 (N64 EnPoh_Disappear, z_en_poh.cpp draft): 4 words off, same constant-order blocker as above.
  - FUN_0011b150 (N64 EnPoh_Appear, z_en_poh.cpp draft): 27 words off. ROM keeps a zero in r6 shared by the
    phase select and the counter reset; no variant got it.
- Header additions: unk_91C u8 (0x91C), unk_91D u8, unk_948 void* (anim ptr). Accessors in z_en_poh_anim.cpp:
  EnPoh_CurFramePtr, EnPoh_PlaySpeedPtr, FUN_0036f32c, FUN_0036f364 (draft).
- Shared-helper rule: FUN_0036f364 (called from FUN_0013f9c4, FUN_003e3f70, FUN_0011b150, FUN_00175170, FUN_0011c3f4)
  stays GLOBAL_ASM until it matches; the helpers it calls are cross-TU.
- ws_check En_Poh: baseline only (FUN_00249af8).

Notes:
- Header: EnPoh now has typed fields at 0x1A4 (SkelAnime), 0x910 (skelAnimModel[2]), 0x918 (actionFunc), 0x920/0x922/0x924 (s16), 0x929 (lightColorA), 0x93C/0x940 (anim ptrs), 0x958 (lightNode), 0x974 (colliderCylinder); rest padded. Size still 0xA6C.
- Data: data_syms.s EQU EnPoh_sRupeeCount = 0x0052E0C0 (Destroy rupee counter).
- No cfg tails found in the matched set (compiled size == ROM size).
- ws_check En_Poh: baseline only (FUN_00249af8).

Batch 3/5 (cascade stage 1, Haiku):
- Matched, moved into actor dir (GLOBAL_ASM removed from functions_*.cpp; all in z_en_poh.cpp):
  - FUN_00282e88 (N64 func_80AE089C env colour + action call; `s2` alias on unk_922++ fixes base reg)
  - FUN_001589a8 (N64 EnPoh_TalkRegular)
  - FUN_0033d000 (N64 func_80AE067C light colour step; callers FUN_001dd6c0/FUN_00297e98 are En_Poh functions)
  - FUN_00353804 (N64 func_80ADFA90 alpha/scale/light; callers FUN_001cd5f8/FUN_001589a8 are En_Poh functions)
  - FUN_003c70bc (N64 EnPoh_Idle; FUN_001807a0 called with 1 arg, via fn-pointer cast; speed 2.0f on attack branch)
- Not matched (GLOBAL_ASM kept, draft under #if 0):
  - FUN_001234c4 (N64 func_80ADF894 flee): 5 words off. 2/3 phase constants: ROM loads 2.0/1/3/0.5 into s1/s2/s0,
    armcc gives s0/s1/s2 for the same pool order; every declaration order tried failed.
  - FUN_003e2570 (N64 EnPoh_TalkComposer): 59 words off. self/play/sfx land in r5/r7/r6 vs ROM r4/r8/r6-ish; the
    hoisted `sub sb,r8,#0xfc` (laugh sfx) and the shared 0x2674 tail (goto) do not reproduce the ROM frame.
  - FUN_001e8ef4 (N64 EnPoh_Death): 52 words off. Lights_PointNoGlowSetInfo x/y/z float args come out as vmov
    copies (static inline, Vec3f*, locals all tried); ROM stores the two zero stack args, then loads z,y,x straight into s2,s1,s0.
- Header additions: envColorR/G/B/A (0x92A-0x92D), lightColorR/G/B (0x926-0x928, replaces unk_926), infoLightR/G/B
  (0x933-0x935, the 3DS info colour block read by the light helpers), infoIdx (0x91F), lanternDisplayList (0x954),
  lightInfo[0x18] (0x95C, Lights_PointNoGlowSetInfo target). Raw offset used for colorFilterTimer (0x11A, inside Actor).
- Local prototypes (no include/ edits): Lights_PointNoGlowSetInfo(9 args: light, x,y,z, r,g,b, radius, pad),
  Inventory_HasEmptyBottle, Item_Give, FUN_00369a48, FUN_003ff758, Actor_WorldDistXZToPoint, Actor_WorldYawTowardPoint.
- ws_check En_Poh: baseline only (FUN_00249af8).

Batches 4+5 (cascade stage 1, Haiku):
- Matched, moved into actor dir (GLOBAL_ASM removed from functions_*.cpp):
  - FUN_00107ae4 (N64 func_80ADEC9C approach; attack setup inlined; `char* flag` store for SkelAnime unk_80[1]=1, z_en_poh.cpp)
  - FUN_00282cc8 (N64 EnPoh_DrawSoul; soul colour copied from EQU EnPoh_sSoulColor 0x4D9B74 in data_syms.s; play2 scoped to camera yaw)
- Not matched (GLOBAL_ASM kept, draft under #if 0):
  - FUN_001cd374 (N64 func_80ADFE28 + EnPoh_Talk inlined, 21 words off): all textId/else-if layouts tried; the
    0x5012 path is placed out of line in ROM and armcc keeps it as fall-through.
  - FUN_00256980 (3DS PostLimbDrawOpa, 79 words off): ROM has self in r5/mtx in r4 and emits a vmov copy per
    Matrix_Scale element; reg order would not flip with decl/param order.
  - FUN_003e0e38 (N64 func_80ADFE80 talk wait, 4 words off): the phase constants load in s2,s1,s0 order in ROM;
    armcc always loads the first-declared constant first.
- Header additions: limbIndexToGlow (0x936), jntSphElements (0x9E8, EnPohJntSphElement), limbMtxCopy (0xA3C MTX34),
  skelAnimModelDeath (0x94C), skelAnimModelSoul (0x950). data_syms.s: EnPoh_sSoulColor EQU 0x004D9B74.
- ws_check En_Poh: baseline only (FUN_00249af8).

Stage 2 (Sonnet, part A):
- Matched: FUN_0036f364, FUN_00175170, FUN_001234c4, FUN_003e0e38 (phase constants: `f32 half, third, two;` declared in
  one order, ASSIGNED two/third/half -> declaration order picks VFP regs, assignment order the pool order),
  FUN_0011b150 (early-return `EnPoh_Phase(u32)` static inline keeps zero in r6), FUN_00238c38 (`s16* p = &self->unk_920`
  declared after the unused Rand call).
- Not matched: FUN_001cd374 (21 words: 0x5012 block out of line in ROM; ~40 layout variants failed).

Stage 2 (Sonnet, part B):
- Matched: FUN_001e8ef4 (EnPoh_Death: `Actor* thisx = &self->actor;` alias for the Lights_PointNoGlowSetInfo pos floats removes the vmov copies; zero stores in ROM order: yOffset first, home.y before scale zeros). GLOBAL_ASM removed from functions_1C0000s.cpp.
- Not matched: FUN_003e2570 (59 -> 14 words; play/next callee-saved regs r6/r7 swapped; draft with play2 + thisx alias under #if 0), FUN_00256980 (79; Matrix_Scale per-element vmov copies, ~30 helper forms failed, same as En_Hata Draw), EnPoh_Update (121/157, draft under #if 0; needs 7-arg FUN_00372f38 alias, header unk_91E now s8).
- Not attempted: FUN_001dd6c0, EnPoh_Init, FUN_00297e98, FUN_001dd974, FUN_003d64a4 (static: guarded local statics, 2 __cxa_guard refs).

Stage 3 (Opus):
- Matched: FUN_003e2570 (N64 EnPoh_TalkComposer written literally — nested ifs, no early returns/locals — plus N64 func_80ADE950 as `static inline EnPoh_StopCryAndLaugh(self, 1)`; GLOBAL_ASM removed from functions_3E0000s.cpp).
- Matched: FUN_001cd374 (N64 else-if chain written literally inside a `static inline EnPoh_Talk(self, play)` helper called from func_80ADFE28; GLOBAL_ASM removed from functions_1C0000s.cpp).
- ws_check En_Poh: baseline only (FUN_00249af8).
