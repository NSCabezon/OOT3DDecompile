# En_Lightbox (stage 1, Haiku) status

Actor: En_Lightbox (src/game/actors/En_Lightbox/z_en_lightbox.cpp). Functions: 3 of 4 matched.

| Function | Status | Notes |
|---|---|---|
| EnLightbox_Init | MATCHED | fastchk 0/84 words differ. Needed a local `f32 yOffset = 0.0f` passed to ActorShape_Init (without it armcc hoists the 0.0f into s16 and the build differs). |
| EnLightbox_Destroy | MATCHED | tail call to FUN_00350f34 |
| EnLightbox_Draw | MATCHED | uses SkeletonAnimationModel::SetUnkAC(1) |
| EnLightbox_Update | NOT MATCHED (GLOBAL_ASM) | Logic matches. Only diff: armcc if-converts `if (speedXZ) { if (bgCheckFlags & WALL) ... }` into ldrhne/tstne (ROM keeps 2 branches), 4 bytes short. Tried: fold of wallYaw expression (applied), `!= 0.0f` compare, `!= 0` on flags, local flags var, combined && condition, store removal probe. Draft under `#if 0`. |

Struct: EnLightbox { DynaPolyActor dyna (0x1BC); SkeletonAnimationModel* skelAnimModel @0x1BC } size 0x1C0.
Deviation from N64 source: wall-yaw line written as `rot.y = wallYaw` (armcc folds `(rot.y + wallYaw) - rot.y` to the same ROM code).

ws_check.sh: baseline only (FUN_00249af8).

Stage 2 (Sonnet): ~25 more variants of EnLightbox_Update (goto, negated early-outs, else branch, for/break, switch, ternary, local flags/speed, __builtin_expect, volatile flag read, inline Bounce helper, unfolded N64 wallYaw expr). armcc always emits ldrhne/tstne (552 B vs ROM 556), even with a volatile read. Still NOT MATCHED; variants in tmp/variants/. Also ROM uses r1 for the wallYaw/bic temp.

Stage 3 (Opus, ~25 min): ~45 more variants (harness: tmp/o/run.sh + tmp/o/*.c). Still NOT MATCHED.
- Tried: (EnLightbox*, PlayState*) signature with `self->dyna.actor.` everywhere; bitfield accessor struct for bgCheckFlags (test + clear);
  inline/static helpers (early-return, yaw/flags passed as params, IsWall bool); flag test forms (>>3&1, <<28<0, /8&1, bool/u8 locals,
  casts); outer speed forms (zero local, double literal, negations, </> pair); foldable wallYaw exprs ((W-R)+R etc.); flags local reused for the clear.
- Findings: a 3-instr inner test (`and; lsrs #3`, e.g. `u8 w = (f & 8) != 0`) is NOT if-converted, but ROM has a 2-instr `tst`.
  `(f >> 3) & 1` / `(f << 28) < 0` give the right SIZE (556) but emit `ldrhne; lslne; cmpne` (8 words differ).
- When the flags value stays live into the body (probe without the sound call), armcc picks r1 for wallYaw like ROM -> ROM likely keeps the
  loaded flags live in r0 into the wall block (as in the unmatched sibling FUN_0039db30 = EnBom move, same `beq; ldrh; tst; beq` shape),
  but with the call in between armcc spills such a value to a callee-saved reg instead of reloading. Same shape also in EnBombf_Update (asm).
  Solving either of those two would likely solve this one.
