# En_Siofuki: stage 1, batch 1/1 (EnSiofuki_Update, EnSiofuki_Destroy, EnSiofuki_Draw)

- EnSiofuki_Update: MATCHED (fastchk 0/2 words, ws_check clean). C: `self->actionFunc(self, (PlayState*)state)`.
- EnSiofuki_Destroy: MATCHED (fastchk 0/12 words, ws_check clean). C: DynaPoly_DeleteBgActor(bgId) + FUN_00350f34(actor, &skelAnimModel, 0).
- EnSiofuki_Draw: NOT MATCHED. Draft under #if 0 with GLOBAL_ASM kept.
  - Diff: 100 of 113 words differ. Frame is 0x40 in ROM, ours 0x3c/0x40 (size 456 vs 452).
  - ROM holds constant 1 for SetUnkAC in r6 (push {r4-r6,lr}); ours re-materializes it late (`mov r1,#1`). Same unsolved class as CLAUDE.md "strb rN,[r0,#0xac]".
  - Local declaration order and scale caching did not change the layout.
  - Variants tried (~11): base, cached scale, pad, 5 decl orders, ternary animSpeed/compound translate, SetUnkAC hoist, volume local, 1/x scale.
  - Sfx gate reads play->sceneNum (PlayState+0x104, s16) == 2 with ratio < 0.35f -> return.

## Struct (z_en_siofuki.hpp)
- Rewritten to 3DS offsets (N64 +0x58 shift): actionFunc 0x1BC, unk_170 0x1C8, currentHeight 0x1D8, maxHeight 0x1F0, sfxFlags 0x1F4, skelAnimModel 0x1F8, unk_200 Vec3f (per-column scale). sizeof stays 0x20C.
- Added EnSiofukiType enum (RAISING/LOWERING).

## Stage 2 (Sonnet)
- EnSiofuki_Init: MATCHED (ws_check clean). Keys: sInitChain via EQU in data_syms.s; type test written inline `(u16)params >> 12 == 0/1` (NOT a local: armcc folds `cmp r6, r0, lsr #12`, which forces the constant 1 into r6 shared with SetAnimType(1)); masterQuestFlag == 1; scale stores in z,y,x order; 0.147f (not 0.1465f).
- EnSiofuki_Draw: NOT MATCHED, 2 words off (draft under #if 0). Frame/regs/tail all match; only the y/z store order of the translate vec ([sp+8] vs [sp+0xc]) is swapped (scheduler puts z first).
  - SetUnkAC `1` in r6 + 0x40 frame SOLVED: pass translate through a static inline helper writing an operator[] vec (`pos[0]=x; pos[2]=z; pos[1]=y; Matrix_UpdatePosition(mtx,mtx,(Vec3f*)&pos)`, called with (0.0f, unk_170, 0.0f)). Plain locals/arrays/Vector3f ctor do not hoist the 1.
  - Tail: switch with case LOWERING before case RAISING, `u32 sfxId=0x01000198; f32 vol=1.0f;` locals before the switch, call `FUN_0036ef10(&world, sfxId, heightRatio + vol)`.
  - Tried all 36 param-order x store-order helper permutations, member vs index stores, y hoists: y/z order stays swapped (same as BgMizuWater_Draw).

## Stage 3 (Opus) — EnSiofuki_Draw still NOT MATCHED (2 words, draft #if 0 unchanged)
- ~150 variants (harness: tmp/o/run.sh + t*.py). Findings:
  - armcc never reorders the three vec stores relative to each other: final store order == source store order. Store kind (member vs operator[]) is irrelevant as long as y goes through an index (needed for r6=1).
  - The vmov copy comes from inline-param binding (two 0.0f params); the earlier-positioned 0.0f param becomes the copy.
  - Register NUMBERING depends only on store order (+ param order), not on roles: stores x,y,z -> x=s2,y=s0,z=s1 (ROM wants x=s1,y=s0,z=s2); stores x,z,y -> x=s1,z=s2,y=s0 (ROM regs, wrong order). Param orders zyx/zxy give x=s0,y=s1,z=s2.
  - No effect: out-param helper SetV(SV*,..), member Set(), ctor body/init-list, temp passed by value/const&, f32 v[3] member, u32 index, operator f32*, MTX34&, nested helpers, y via local/thisx/self param, ternary animSpeed, chained `pos[0]=pos[2]=0`, ScaleCol(mtx,col,s) helper for the scale part (puts the 1 in r1 after the call, not r6).
  - Next idea not tried: make y's live range extend past the z store (allocator colors as in xzy case) without an extra emitted use.
