# Bg_Spot17_Bakudankabe (stage 1, Haiku)

| Function | Status | Notes |
|---|---|---|
| BgSpot17Bakudankabe_Init | MATCHED (C) | 45/45 words. sInitChain via EQU in data_syms.s (0x00513E84). |
| BgSpot17Bakudankabe_Destroy | MATCHED (C) | 12/12 words. |
| BgSpot17Bakudankabe_Draw | MATCHED (C) | 19/19 words. |
| BgSpot17Bakudankabe_Update | NOT MATCHED, left as GLOBAL_ASM | ROM 744 B; best C variant 740 B (tail call to Actor_Kill ok, 124 words differ). Remaining diffs: armcc hoists -420 into a reg (ROM loads it from literal pool via ldrge), s22/s23 float reg swap for constants (30.0 / temp1), r6/r7 scale/gravity swap, actor/self register copies (ROM keeps actor in r8). C draft kept under #if 0 in the actor .cpp. |

Workspace check: ws_check.sh shows only the baseline (FUN_00249af8).
Files touched (in this workspace only): z_bg_spot17_bakudankabe.cpp, z_bg_spot17_bakudankabe.hpp, data_syms.s (new).

## Stage 2 (Sonnet) - BgSpot17Bakudankabe_Update: still NOT matched
Best draft 736 B vs 744, 52/186 words off (was 740 B / 124). Gains: N64 `func_808B6BC0` helper (static __inline, inlined)
and `s16 rotationSpeed` (removes sxth). Root cause of the rest: ROM keeps `actor` in r8 and a copy `self` in r5;
armcc merges them (tried: thisx/self locals, (Self*,..) signatures, void*/u8* casts, helper taking Actor*, all-via-self,
inline kinds). With r8 free armcc hoists -420 (ROM has no free reg -> ldrge from pool) and reg swaps follow.
Draft in .cpp under #if 0 and tmp/upd_body.c; harness tmp/h/run.sh.

## Stage 3 (Opus) - BgSpot17Bakudankabe_Update: C is instruction-exact, still GLOBAL_ASM (cfg-merge blocker)
fastchk: 0/186 words differ, built 740 B vs ROM 744. The extra 4 B = `bx lr` at 0x0039F204, a SEPARATE empty
function (referenced by address from FUN_0037bb4c's table, collision code) merged into Update by functions.tsv/cfg.
With C, CollisionCheck_AC_CylVsCyl etc. shift by 4 -> needs cfg split (`arm_func 0x0039f204`) -> out of scope.
Fixes found: 2nd typed local `BgSpot17Bakudankabe* s2 = self;` used only in the inlined helper call + `thisx->` for
all outer accesses (ROM r8 = thisx, r5 = self copy); `FUN_00346d94((PlayState*)state, thisx)` (play stays in r0);
`s16 scale;` declared before `s16 gravityInfluence;`.
Verified but NOT adopted (placement hack): empty `void FUN_0039f204(void) {}` under
`#pragma arm section code = "i.BgSpot17Bakudankabe_Update"` after Update -> ws_check baseline. Exact C is under #if 0.
ws_check: baseline only.
