# En_Mm2 status (cascade stage 2, Sonnet)

ws_check.sh En_Mm2: only FUN_00249af8 differs (baseline). PASS.

## Actor functions
- MATCHED (C): EnMm2_Init, EnMm2_Destroy, EnMm2_Update, EnMm2_Draw, EnMm2_OverrideLimbDraw,
  FUN_003539d8 (own file z_en_mm2_text.cpp, no noinline), FUN_001570ac (N64 func_80AAF2BC),
  FUN_001e94b4 (func_80AAF330), FUN_003f93e4 (func_80AAF5EC), FUN_001788b8 (func_80AAF668), FUN_003cdc40 (func_80AAF3C0).
  The six FUN_ moved here; their GLOBAL_ASM lines were deleted from functions_{140000s,1C0000s,350000s,3C0000s,3E0000s}.cpp.
- NOT matched: FUN_001571d8 (func_80AAF57C): 3 words (0x64-0x6c): ROM `ldrh r1,[+0x92]; ldrh r0,[+0xbe]; sub r0,r1,r0`,
  we emit r0/r1 swapped. ~30 variants (locals, casts, Actor* alias, helper shapes, switch). C draft under #if 0, asm kept in functions_140000s.cpp.
  (In FUN_001788b8 the same shape matches because r1 is live there from a hoisted `mov r1,#0`.)
- NOT attempted: EnMm2_PostLimbDraw (function-local guarded static).

## Tricks found
- Destroy: the "dead arg setup" is NOT a removed call: it is Collider_DestroyCylinder(play,&collider) (returns 1; linker inlines it to
  `mov r0,#1`). Needs (EnMm2*, PlayState*) signature to get the ROM register order.
- Init: (Actor* thisx, PlayState*) signature; BOTH actionFunc stores via `((EnMm2*)thisx)->actionFunc` stop armcc merging the two stores
  and give ROM's ldreq/streq/beq + r1 register.
- Draw: `FaceAnimations* fa = &self->faceAnim; s32 mouth = self->mouthTexIndex; fa->FUN_0035e3a4(1, mouth);` and the tail call via
  `self->faceAnim.FUN_0035e330()`.
- FUN_003cdc40: `textId == 0x607F` in the default case must be a one-case `switch` (an `if` makes armcc hoist 0x607F into r9).
- FUN_001788b8: hi-score min as `s32 t=timer2Value, h=unk_EE0; if (t > h) t = h; unk_EE0 = t;` (always stores).
- SkelAnime_Update (FUN_003731e0) returns s32 but include/functions.hpp declares void: used a function-pointer cast locally.
- 3DS timer scaling: unk_8B2 > 90 (N64 60).

## Data
- data/z_En_Mm2.data.s (GLOBAL_ASM) kept. syms.s (EQU) exposes mm2InitChain 0x52C870, mm2CylinderInit 0x52C878, mm2AnimInfo 0x52C8B0.
- Note: AnimationSpeedInfo layout in the draft: {anim ptr, f32 speed, u8 mode, f32 morph} = 0x10 bytes (confirmed from Init asm offsets).

## Files touched outside the actor dir
- src/functions/functions_350000s.cpp: GLOBAL_ASM("asm/FUN_003539d8.s") commented out (function now lives in En_Mm2/z_en_mm2.cpp).
- No include/ changes. No oot3d/ writes.

## Layout notes (3DS)
- EnMm2 struct: actor 0x000, skelAnime 0x1A4, jointTable 0x228, morphTable 0x534, actionFunc 0x840, collider 0x844, mouthTexIndex 0x89C, unk_8A4/unk_8AA Vec3s (head/torso), flags u16 0x8B0, previousAnimation 0x8B4, skelAnimModel 0x8B8, FaceAnimations 0x8BC.
- Actor_TrackPlayer = FUN_0036bcc8 (6 args incl. s16 yawLimit 0x4300 on the stack).
- Init's LINK_IS_ADULT = gSaveContext.linkAge == 0; INFTABLE_17F = infTable[23] & 0x8000; EVENTINF_MARATHON_ACTIVE = eventInf[1] & 1; HS_MARATHON = unk_EE0; subTimerState = timer2State.
