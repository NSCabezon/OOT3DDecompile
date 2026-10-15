# Demo_Shd: status (stage 1, Haiku)

Actor: Demo_Shd (Bongo Bongo's shadow). N64 ref: `tools/repos/oot/src/overlays/actors/ovl_Demo_Shd/`.
Last check: `scripts/ws_check.sh Demo_Shd` -> only baseline FUN_00249af8 differs. No merge yet (orchestrator).

## Functions
| Function | Size | Status | Notes |
|---|---|---|---|
| DemoShd_Init | 244 | MATCHED | 3DS: unk_14C at 0x1A4, actionFunc 0x1A8, skel[2] 0x1AC, cmab[2] 0x1B4. Calls 7-arg FUN_00372f38 via cast. |
| DemoShd_Destroy | 16 | MATCHED | tail call FUN_00350f34 (4 args, cast; header declares 3). |
| DemoShd_Update | 8 | MATCHED | tail call actionFunc. |
| DemoShd_Draw | 196 | MATCHED | Only 3DS draw: frame = unk_14E % frameCount (FUN_00368d94 returns quotient:remainder in r0:r1, declared u64). N64 display-list draw is gone. |
| FUN_003f1fd8 (action, moved from functions_3E0000s.cpp) | 360 | MATCHED | Moved into z_demo_shd.cpp; GLOBAL_ASM line removed from functions_3E0000s.cpp. |

Count: 5/5 matched (4 actor functions + 1 moved FUN_ action).

## Attempts / learnings
- Draw: first versions were 228 and 204 bytes. The original predicates the `gate == 0` store+call (vstreq/bleq), and converts to float before the gate test. Matched with `fFrame = (f32)frame;` computed before `if (gate == 0)`. A static-inline helper gave 208 bytes (worse).
- `%` on s32 generated a call to `__aeabi_uidivmod`, which collides with the project's own copy (functions_320000s GLOBAL_ASM). Calling the game's FUN_00368d94 directly avoids it.
- `this` is a C++ keyword: named the param `self`.
- CutsceneContext in the repo header has no `actorCues`; the 3DS cue pointers sit at csCtx+0x44/+0x48, which is `npcActions[0]/[1]` in the header. Cue id is read as `*(u16*)cue` (CsCmdActorAction has no `id` field).
- Action FUN_003f1fd8 differs from N64: unk_14E = 0xFFFF on cue start (not startPos.x), and cutscene sound cues are at FRAMES(800)->seq 9 and FRAMES(1069)->seq 8 with FRAMES(n) = n*3.0f/R_UPDATE_RATE + 0.5f (same macro as Obj_Mure).

## Debt / notes (for the orchestrator)
- Gate global 0x0054C8CC (`DAT_0054c8cc_DemoShd`): absolute EQU in `src/game/actors/Demo_Shd/DAT_0054c8cc.s`, same technique as Bg_Mjin. Should become a real data symbol (same debt as Bg_Mjin / Unknown global list).
- FUN_00372f38 / FUN_00350f34: casts to local typedefs because the header prototypes are truncated (see learnings).
- FUN_003674e4 (cutscene effect seq) and FUN_003586ec declared locally in the .cpp; no existing prototypes in include/.
- Header `z_demo_shd.hpp` (actor dir) rewritten: struct fields replace `char unk_1A4[0x18]`. Size stays 0x1BC.

## Files touched
- `src/game/actors/Demo_Shd/z_demo_shd.cpp`, `z_demo_shd.hpp` (actor dir)
- `src/game/actors/Demo_Shd/DAT_0054c8cc.s` (new, actor dir)
- `src/functions/functions_3E0000s.cpp` (outside actor dir: GLOBAL_ASM("asm/FUN_003f1fd8.s") line removed)
- `include/`: untouched.

UNMATCHED: none
