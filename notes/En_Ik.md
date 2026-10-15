
<!-- merge 2026-10-14 13:34:46 -->
# En_Ik STATUS (cascade stage 1, Haiku, batch 1/3)

Workspace: ws/En_Ik (mkws done before this batch). ws_check.sh En_Ik = baseline only (FUN_00249af8).

## Matched (moved into actor dir, names kept)
- EnIk_Update: dispatch via `EnIk_sUpdateFuncs` (EQU 0x5282D8, data_syms.s), header `updateIndex` at 0xFE8.
- EnIk_Draw: same, `EnIk_sDrawFuncs` (EQU 0x5282F0), header `drawIndex` at 0xFEC.
- FUN_00357a70: returns `gUnk_004D86CC + idx*48` (EQU, table identity unknown).
- FUN_00379cac: counts actors with given id in `actorCtx->actorLists[type]` (uses `Actor::next` at 0x130).
- FUN_001c67f4: `if (FUN_003731e0(anim)) { FUN_003468fc(self); FUN_0036d188(self, play); }`. FUN_003731e0 is declared
  by include as void; called through a function-pointer cast to get the s32 result.
- FUN_003468fc: in its own TU `z_en_ik_anim.cpp` (if it shares a TU with FUN_001c67f4, armcc inlines it).
- FUN_00375f88: 2-insn `mov r2,#8` + call to empty `EnIk_EmptyCall` (z_en_ik_anim.cpp). The callee is declared
  `__attribute__((noreturn))` so armcc emits `bl` (not a tail `b`, which armlink does NOT inline); armlink then turns the
  bl into `mov r0,r0`. Verified by ws_check.

## Not matched
- FUN_003c43bc: GLOBAL_ASM stays in functions_3C0000s.cpp; draft under `#if 0` in z_en_ik.cpp. Cause: VFP register
  allocation. The ROM keeps 1/3 in s0, 0.5 in s1, rate*scale in s2, and an if-converted (vnmlsle/vmlagt) select; the
  closest C shape still differs in 19/31 words (regs and cur/target compare order). ~10 variants tried (local order,
  ternary vs if/else, deferred read of *pValue, float scale local).

## Shared-check
All target FUN_s are referenced only from En_Ik's own action graph (FUN_00136fc8 is the En_Ik action used by
FUN_0010b758/FUN_0013832c/FUN_003e9be4), so none were skipped as shared.

## Notes
- Actor header: `unk_1A4[0xC68]`, `unk_E0C` (u8), `actionFunc` (0xE1C, void*), `updateIndex`/`drawIndex`, size still 0xFFC.
- Not touched: EnIk_Init, FUN_0010b758 and the other En_Ik action FUN_s (other batches).

# En_Ik STATUS, batch 2/3 (cascade stage 1, Haiku)

ws_check En_Ik = baseline only (FUN_00249af8). Moved FUN_s out of functions_*.cpp (GLOBAL_ASM removed).

## Matched (batch 2)
- FUN_003a7a2c (-> `Actor_IsFacingAndNear`-style helper, dist < range && |yaw diff| < angle): moved to z_en_ik.cpp.
- FUN_00196ba8: moved to z_en_ik.cpp. Float-local `endFrame` before `unk_E0C = 8` fixed a `mov r0,#8` vs `r1` reg diff.
- EnIk_Destroy: in z_en_ik.cpp. The Cylinder/Quad destroys are 2-insn stubs in the ROM, so they go through
  `EnIk_ColliderDestroyStub` (z_en_ik_anim.cpp) and get inlined by armlink. Flag block uses `GET_PLAYER` + `+0x2000 +0x9B8`.
- FUN_0026c4a0: moved to z_en_ik.cpp. Args: r2/r3 = arg2/arg3, ctx struct at +0x1AC, ctx reloaded from +0x1C4 before FUN_00347774.
- FUN_0036d188: in z_en_ik_anim.cpp. Defining it in z_en_ik.cpp made armcc inline it into FUN_001c67f4 (56 -> 228 B).
- FUN_00181598: moved to z_en_ik.cpp. `EnIk_SetupAction` helper (static inline) for the action pointer.
- FUN_0014be68 (draw): moved to z_en_ik.cpp. FUN_00357a70 moved to z_en_ik_anim.cpp, else it is inlined into the draw.

## Not matched (batch 2)
- FUN_001374c0 (update, calls FUN_003c43bc / FUN_0036d188): GLOBAL_ASM stays in functions_120000s.cpp; draft under `#if 0`
  in z_en_ik.cpp. 6/63 words differ, all r5/r6 swap (play vs zero). Float-compare regs were fixed by hoisting the
  `self+0xE00` base above the compare. Tried: nested-if order, negated compare, play2 alias, zero local, zero stores.

## Header (z_en_ik.hpp, batch 2 additions only)
- unk_E0E/E0F/E12/E13/E14/E15 typed as u8/char; ColliderCylinder bodyCollider @0xE34; axeCollider char[0x80] @0xE8C;
  shieldCollider char[0xDC] @0xF0C. Size still 0xFFC.

## Shared-check (batch 2)
- FUN_0036d188 callers: FUN_001c67f4, FUN_001374c0, FUN_003c6944, FUN_0010b758, FUN_003e9be4, all in En_Ik's outside list. Not shared.

# En_Ik STATUS, batch 3/3 (cascade stage 1, Haiku)

ws_check En_Ik = baseline only (FUN_00249af8). GLOBAL_ASM removed for the matched FUN_s (functions_3C0000s, functions_3E0000s, functions_120000s).

## Matched (batch 3)
- FUN_003c6944 (action, z_en_ik.cpp): `Math_SmoothStepToF(&speedXZ, 0, 1, 1, 0)`, yaw test needs u16 loads and a `s16 yawDiff` local (else `sxtah` folds). The in-range branch inlines the FUN_003468fc body (ROM has it inline) and tail-calls FUN_0036d188.
- FUN_003e45ac (action, z_en_ik.cpp): constants come from the pool (1.0 speed/E4, 5.0 and 2/3 for OnFrameImpl, -4.0 morph, 0.9/2.5 speeds). `vldr s17/s18` must be declared before the flags store, and `Actor* thisx` alias on `flags |= 5` fixes the reg order.
- FUN_00136fc8 (action, z_en_ik.cpp): `goto` layout (window block placed before the E12=0 block, `goto after`) and `!(x >= 0)`-style abs gave the right branch shapes. Plain `x<0 ? -x : x` gives `vneglo`, the ROM needs `vneglt` (early-return form `if (x >= 0) goto done; x = -x;`).
- FUN_00375f88: moved to z_en_ik_anim.cpp (it was inlined into FUN_003e45ac in the same TU). Its empty callee EnIk_EmptyCall now lives in z_en_ik.cpp, so armlink keeps the call.

## Not matched (batch 3)
- FUN_0010b758 (action): GLOBAL_ASM stays in functions_100000s.cpp; draft under `#if 0` in z_en_ik_act.cpp (new TU, so FUN_0036d188 is not inlined). The ROM keeps 150.0f bits in r3 from entry (int compares, 100.0f derived as r3-0x4e0000). We load it late, so 52/106 words flag (mostly one shifted insn). ~9 variants tried.
- FUN_0013832c (action): GLOBAL_ASM stays in functions_120000s.cpp; draft under `#if 0` in z_en_ik.cpp. 7/117 words differ: ROM does `ldr r0,[r0,r5]; mov r5,#6` (6 reuses the play reg after the flag load), ours hoists 6 into r6 and zero into r5. Flags local, play2 alias, cast alias: no change.

## Layout notes (batch 3)
- New TU `z_en_ik_act.cpp` holds FUN_0010b758's draft. It includes z_en_ik.hpp and the extern prototypes only, so it is still compiled. It is not a file the merge tools know about yet (the actor dir copy handles it).
- FUN_00181598, FUN_00136fc8, FUN_0013832c live in z_en_ik.cpp. FUN_0036d188, FUN_003468fc, FUN_00375f88 live in z_en_ik_anim.cpp. Keep these splits: same-TU callees get inlined.

# En_Ik STATUS, cascade stage 2 part A (Sonnet)

## Matched (stage 2)
- FUN_0010b758 (N64 EnIk_Idle): needs the N64 else-if/else pair (`ABS(yawDiff) <= 0x4000 && ABS(yDist) < 150` then SetupWalkOrRun in both arms; the second compare is dead but keeps 150.0f live from entry), early-return abs helper (`if (x >= 0) return x; return -x;`) and morph -6.0f in the B path. In z_en_ik_act.cpp.
- FUN_0013832c (N64 StopAndBlock): same N64 shape + `(self, PlayState* play2)` with `PlayState* play = play2;` (moves 6 into the play reg after the flag load). In z_en_ik.cpp.
- FUN_0011c7e0 (N64 VerticalAttack, z_en_ik_act.cpp): `Vec3f sparksPos` scoped in the else-if (shares slot with the SmoothStepToS stack arg), `!(f <= 22) { if (f < 28) {...; goto after;} }`, rounding written as `if (e > 0) t = (s32)(0.5f + (e*3.0f)*0.5f); else t = (s32)((e*3.0f)*0.5f - 0.5f);` (if/else + temp, not ternary).
- FUN_003d6f18 (N64 EnIk_Die, z_en_ik_act.cpp): effects only when `animationTimer % 3 != 0` (3DS), `Vector3f sp7C(0,0.5,0)` cast to Vec3f*, EffectSsDeadDb_Spawn unk2 = 0xB.

## Not matched (stage 2)
- FUN_001374c0: 6/63 words, play r5 vs zero r6 swap (ROM play r6, zero r5). ~60 more variants (play2 forms, zero locals of 4 types at 3 positions x 15 use-sets, dead aliases at every site via greedy mutation) no change.
- FUN_003c43bc: draft now 12/31 (VFP numbering and arithmetic match; ROM loads 1/3 and 0.5 up front, cur in ip, d0 in r3). ~1800 decl-order permutations.
- FUN_00232fac (= N64 BodyBreak_SpawnParts, shared helper): draft in z_en_ik_act.cpp under #if 0, 85/125 words (register allocation only: ROM keeps zero hoisted in sl via `moveq r0,sl` NULL phi and spills `type` through `push {r0-r3,..}`).

# En_Ik STATUS, cascade stage 2 part B (Sonnet)

## Matched (part B)
- EnIk_Init (z_en_ik_act.cpp, own TU): N64 shape split into static inlines EnIk_InitImpl / EnIk_SetupStandUp / EnIk_CsInit (+ EnIk_SetupAction). Blure init struct with 16 `EnIkBlureVtx` elements whose empty ctor is FUN_003fd780 (EQU `_ZN12EnIkBlureVtxC1Ev` in data_syms.s, same trick as Bg_Haka_Sgami). `blureInit` is declared in InitImpl (after the skel init, shares the outgoing-arg slots). Params switch flag `(params >> 8) & 0xFF`, `PlayState* play2 = play;` passed to InitImpl, dead `EnIk* s2 = self` for `unk_E14 = 0`, `EnIk_InitShape(shape, 30.0f)` wrapper (float arg order). Data EQUs added: EnIk_sCylinderInit/TrisInit/QuadInit/DamageTable (0x528130/168/178/1C8).

## Not matched (part B)
- FUN_003e9be4 (N64 EnIk_WalkOrRun): draft under #if 0 in z_en_ik_act.cpp. Everything before and after the inlined EnIk_FindBreakableProp loop is byte-identical; only the loop block layout differs (ROM: latch `ldr r5,[r5,#0x130]` after the found-body, NULL exit falls into the else branch). ~25 loop shapes + single-site mutations: no change (62 words, all shifts).
- FUN_001008b4 (N64 EnIk_UpdateEnemy + inlined UpdateDamage/StartDefeatCutscene/SetupDie/SetupReactToAttack): draft under #if 0 (2020 B vs 2024). Entry hoisting (r8=&world.pos, sb=0xE00, fp=1, sl=0) and play spill [sp,#0x10] differ; greedy alias search stalled.
- FUN_0016ee30 (post-limb draw): 4 inlined `__cxa_guard_acquire` guarded function-local statics -> (structural), not attempted.

# En_Ik STATUS, cascade stage 3 (Opus)

ws_check En_Ik = baseline only (FUN_00249af8), 0 non-function bytes. GLOBAL_ASM lines removed from functions_120000s,
functions_200000s, functions_3C0000s, functions_3E0000s.

## Matched (stage 3)
- FUN_001374c0 (N64 EnIk_SingleHorizontalAttack, z_en_ik.cpp): N64 shape with static inline
  EnIk_SetupRecoverFromHorizontalAttack (`unk_E13 = unk_E12 = 0`); range test as nested ifs + `goto done` sharing one
  `unk_E12 = 0` store (`&&` folds into an unsigned float-bits range compare; nested if/else gave the r5/r6 swap).
- FUN_003c43bc (N64 Math_StepUntilS with step*R_UPDATE_RATE/3 rounding, z_en_ik_anim.cpp so the caller keeps `bl`):
  `s16 step` param, rounding as if/else into an `s32` temp, `*pValue += s`.
- FUN_003e9be4 (N64 EnIk_WalkOrRun, z_en_ik_act.cpp): literal N64 EnIk_FindBreakableProp (return prop / return NULL)
  and the caller tests `EnIk_FindBreakableProp(...) != NULL` directly (no `prop` local).
- FUN_00232fac (N64 BodyBreak_SpawnParts, z_en_ik_act.cpp; only caller FUN_003c6944): 5th arg goes to FUN_0026c4a0
  (draft passed `type`); Actor_SpawnAsChild as plain `static` (non-inline) helper + `s8 bank = actor->objBankIndex;`
  local before the call.

## Not matched
- FUN_001008b4 (~300 words, big), FUN_0016ee30 (structural: guarded statics) — not attempted, drafts unchanged.
