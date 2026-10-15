# Bg_Mori_Kaitenkabe: STATUS (stage 1, Haiku-only)

Final: `ws_check.sh` shows baseline only (FUN_00249af8). 7 of 8 functions matched (5 actor-dir functions, 2 moved helpers, Rotate left as asm).

## Functions
| Function | Address | State | Notes |
|---|---|---|---|
| BgMoriKaitenkabe_Init | 0x0037ac68 | MATCHED (0/48 words) | ReadCollisionHeaderFromZsi(DynaPolyInfo_Alloc(...), &colHeader) form (armlink inlines it, no call in asm). First try with a plain cast left the frame 8 bytes short. |
| BgMoriKaitenkabe_Destroy | 0x0037ad28 | MATCHED (0/12) | tail call FUN_00350f34 |
| BgMoriKaitenkabe_Update | 0x0038ada8 | MATCHED (0/2) | |
| BgMoriKaitenkabe_Draw | 0x0038ace8 | MATCHED (0/48) | 3x3 part scaled by 1.002 per column, using a Vec3f scale {x,y,z}. Plain literal, loop, or single scalar gave wrong register use. |
| BgMoriKaitenkabe_Wait | 0x003bfa4c | MATCHED (0/73) | SetupRotate inlined by hand (actionFunc = FUN_003f61dc, rot speed/yaw = 0). |
| BgMoriKaitenkaby_WaitForMoriTex | 0x0011088c | MATCHED (0/19) | MOVED from functions_100000s.cpp (ld-pinned name kept, typo "Kaitenkaby" is in the symbol). |
| FUN_0010feb0 | 0x0010feb0 | MATCHED (0/6) | MOVED from functions_100000s.cpp. It is BgMoriKaitenkabe_SetupWait. Needs `__attribute__((noinline))` on the prototype, otherwise armcc inlines it into Rotate. |
| FUN_003f61dc | 0x003f61dc | NOT MATCHED, left as GLOBAL_ASM in functions_3E0000s.cpp | Rotate (BgMoriKaitenkabe_Rotate). Draft in actor .cpp under `#if 0`. |

## Rotate (FUN_003f61dc): attempts
Draft: 3 of 90 words differ, all at the same spot, the `fabs(unk_1A8) > 0.001f` test after the Audio call. The asm loads the 0.001 constant into r1 and compares r0 (fabs bits) against it. Ours loads into r0 and compares r1.
1. Draft as written (`__fabsf(x) > 0.001f`): 3 words differ (kept).
2. Operands swapped (`0.001f < __fabsf(x)`): no change.
3. Dropped the `Actor* thisx` local (use &self->dyna.actor): 61 words differ, reverted.
4. Swapped declaration order of player / thisx: no change.
5. Expanded compare (`x > 0.001f || x < -0.001f`): 50 words differ, reverted.
Stopped at the timebox. Leftover for a Sonnet pass: register choice for the final threshold compare (possibly needs a different declaration or statement order around the Audio_PlaySoundGeneral calls).

## Debt / 3DS notes
- `sInitChain` is a fixed address (0x00513394) in the data dump (GLOBAL_ASM "data/z_Bg_Mori_Kaitenkabe.data.s" kept). ICHAIN_F32 / ICHAIN_VEC3F_DIV1000 cannot be used here: the 3DS `Actor` struct has no cullingVolume* / scale members in the repo header. Raw-address hack, same as Bg_Mori_Rakkatenjo.
- `DEG_TO_BINANG` defined locally as `(s16)(deg * 182.04445f)` (asm constant 0x43360B61). Not in include/.
- Player_InCsMode, Object_GetIndex, Object_IsLoaded declared locally (not in include/).
- `Player::stateFlags2 &= ~0x10` used as a literal (PLAYER_STATE2_4 not defined).
- Header actor struct rewritten to the 3DS layout (DynaPolyActor 0x1BC; actionFunc 0x1BC, timer 0x1C0, rotDirection 0x1C4, rotSpeed 0x1C8, rotYdeg 0x1CC, lockedPlayerPos 0x1D0, moriTexObjectSlot 0x1DC, skelAnimModel 0x1E0; size 0x1E4). The old header was the N64 layout with an opaque char array.

## Files touched outside the actor dir (ws/ only)
- src/functions/functions_100000s.cpp: removed GLOBAL_ASM lines for asm/FUN_0010feb0.s and asm/BgMoriKaitenkaby_WaitForMoriTex.s
- src/functions/functions_3E0000s.cpp: unchanged vs main tree (FUN_003f61dc stays asm)
- include/: no changes

## Opus closing pass (2026-10-13)
- FUN_003f61dc (Rotate) MATCHED 0/90. Fix: `static __inline __pure float BgMoriKaitenkabe_Fabsf(float f) { return _fabsf(f); }` (+ `extern __pure float _fabsf(float);`) and `if (BgMoriKaitenkabe_Fabsf(self->dyna.unk_1A8) > 0.001f)`. Calling `__fabsf` directly swapped r0/r1 in the integer bit-compare. Wait unchanged (still `__fabsf`, matches).
- GLOBAL_ASM("asm/FUN_003f61dc.s") removed from src/functions/functions_3E0000s.cpp in ws. ws_check: baseline only. Actor now 8/8.
