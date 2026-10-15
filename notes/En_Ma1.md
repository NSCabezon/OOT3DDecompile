
<!-- merge 2026-10-14 10:47:18 -->
# En_Ma1 status (cascade stage 1, Haiku, batch 2/2)

Workspace ws/En_Ma1. ws_check.sh: baseline only (FUN_00249af8). Not committed.

## Batch 2 (this pass)
- MATCHED: FUN_00173710 (talk-state action, Player local), FUN_001c52cc (msg-state check, raw `play+0x2B7E`,
  misc store via `(u8*)0x00588E58`), FUN_00195cd8 (EnMa1_GetTextId; typed eventChkInf[1]/infTable[8]).
  Moved into z_en_ma1.cpp; GLOBAL_ASM removed from functions_1C0000s/140000s/180000s.
- NOT MATCHED (GLOBAL_ASM, draft under `#if 0`):
  - EnMa1_Draw: 17/44 words. Calls match in order; armcc schedules the camera/pos loads and the bgm literal
    differently (~6 variants: inline cam expr, s16 index, decl order, self-based pos).
  - FUN_003d2a14: 5/52 words. Calls/branches match; the 0x588758 flags literal is hoisted above the sceneNum ldrh
    (ROM: after). CHECK_QUEST_ITEM(QUEST_SONG_EPONA) fixed the mask order. ~11 variants.
  - FUN_00195b90 (EnMa1_UpdateTalkState): 62/82 words. Outer jump table matches; the inner textId switch is a tree
    rooted at 0x2048 in ROM, ours is a chain. ~5 variants.
  - FUN_003c6128 (cfg): 2/70 words off, but functions.tsv span (280 B) covers an unlabeled tail fn @0x003c6218 after
    the literal pool. Needs cfg split. Draft under `#if 0 // (cfg)`.
- Notes: FUN_00348800 needs `__attribute__((noinline))` on its prototype, otherwise --forceinline inlines it into
  FUN_003d2a14 / FUN_003c6128 (ROM calls it). Added eyeIndex/mouthIndex (interactInfo +0x0C/+0x0E) in z_en_ma1.hpp.
  FUN_00371680 decl now takes 3 args (ROM passes r2=0).

## Batch 1 matched (moved into src/game/actors/En_Ma1/z_en_ma1.cpp, GLOBAL_ASM removed from src/functions/*)
- EnMa1_Destroy (actor-owned, first try)
- FUN_003d2a10 (empty stub, `bx lr`) - from functions_3C0000s.cpp
- FUN_001e63ec (GiveItem weird egg) - from functions_1C0000s.cpp
- FUN_00348800 (animation change from table @0x0052C180) - from functions_340000s.cpp
- FUN_0013532c (flag + Message_GetState -> FUN_001c52cc) - from functions_120000s.cpp
- FUN_00233614 (OverrideLimbDraw, limb 7 torso / 6 head rot) - from functions_200000s.cpp
- FUN_00217274 (PostLimbDraw, focus pos via N64-order wrapper EnMa1_MultVec3f) - from functions_200000s.cpp

## Not matched / blocked
- FUN_001522b4 (functions_140000s.cpp): C draft matches the 76-byte body (0/50 words differ), but functions.tsv
  merges FUN_00152300 (referenced as a function pointer by FUN_001c5338) into the 200-byte range. Moving it would
  drop that code. Needs cfg split. Kept as GLOBAL_ASM, draft under `#if 0` in the actor .cpp.

## Shared check
- No listed FUN_ is called from C outside En_Ma1. Asm callers: EnMa1_Init/Update/Draw and FUN_003c6128, FUN_00173710,
  FUN_003d2a14, FUN_001c52cc, FUN_001522b4, FUN_001e63ec (all in the En_Ma1 chain). None shared.

## Notes
- z_en_ma1.hpp: EnMa1 now has named fields (skelAnime @0x95C, actionFunc @0xBAC, interactInfo @0xC00, size 0xC38);
  FaceAnimations and ColliderCylinder are accessed through casts on char arrays (0x9E0, 0xBB0).
- EnMa1_Init, EnMa1_Update, EnMa1_Draw, data/z_En_Ma1.data.s are still GLOBAL_ASM (not in this batch).
- Raw globals: 0x00588758 (+0xEE) and 0x0052C180 (anim table) used by address, as in En_Ma3/En_Heishi4.

## Stage 2 (Sonnet)
- MATCHED: FUN_003d2a14 (use `gSaveContext.eventChkInf[1]` symbol instead of raw 0x588758; moved GLOBAL_ASM removal in functions_3C0000s.cpp).
- NOT MATCHED, drafts under `#if 0` in z_en_ma1.cpp (GLOBAL_ASM kept):
  - FUN_00195b90: 4 words. Hoisting of &gSaveContext+0xE00/+0xF00 bases needs explicit base pointers + `PlayState* p = play` alias + `s32 tid` before pointers + case order 2043,2047,2041; remaining: ROM loads 0x2048 literal before the base literal. functions_180000s.cpp GLOBAL_ASM line restored.
  - EnMa1_Draw: 6 words. bgm literal is loaded before the pos vldr in ours (ROM after); needs EnMa1_SetFace inline helper for FaceAnimations arg order.
  - EnMa1_Update: 16 words. Tail (trackPos copy + talkState/anim compare) scheduled/predicated differently (ours moveq/beq/mov vs ROM movne/moveq). hpp: added singingDisabled (+8), blinkTimer (+0xA), trackPos (+0x28) to EnMa1InteractInfo.
  - EnMa1_Init: 10 words. rot.z / infTable-literal reg swap (r1/r2) + targetMode/talkState store regs. Needs `(Actor*, PlayState* play2)` + `PlayState* play = play2;` last, objBank helper at +0x3A5C/+0x3A64.

## Stage 3 (Opus)
- MATCHED: EnMa1_Init (N64 `static inline EnMa1_ShouldSpawn(self, play)` returning bools instead of goto chain; `self->actor.` stores),
  EnMa1_Update (N64 static inline helpers UpdateEyes/UpdateSinging/UpdateTracking with if/else trackingMode),
  EnMa1_Draw (N64 shape: activeCam local, `Math_Vec3f_DistXZ(&thisx->world.pos, ..)`, literal bgm arg, `&self->actor` in DrawOpa).
  Prototypes for Init/Update/Draw now `(Actor*, PlayState*)`; GLOBAL_ASM lines removed.
- NOT MATCHED: FUN_00195b90 still 4 words (literal order 0x2048 vs gSaveContext base + cross-jump target); draft under `#if 0`, GLOBAL_ASM kept in functions_180000s.cpp.
- Skipped (cfg-merged): FUN_003c6128, FUN_001522b4.
- ws_check.sh: baseline only.
