# Bg_Relay_Objects — stage 1 (Haiku-only)

Final check: `scripts/ws_check.sh Bg_Relay_Objects` shows baseline only (FUN_00249af8). No regressions.

## Functions (actor dir `src/game/actors/Bg_Relay_Objects/z_bg_relay_objects.cpp`)
| Function | Status | Notes |
|---|---|---|
| BgRelayObjects_Destroy | MATCHED (C) | 0/28 words differ |
| BgRelayObjects_Update | MATCHED (C) | 0/2 words differ |
| FUN_00214874 (windmill BGM helper) | MATCHED (C) | 0/12 words differ; `__attribute__((noinline))` on the prototype keeps it a separate call from Init |
| BgRelayObjects_Init | NOT MATCHED, GLOBAL_ASM + `#if 0` draft | 18/145 words differ. Dampe-race branch: ROM merges the two `Actor_Kill` blocks into one; the C duplicates them. Tried 2 branch structures (the other one was worse, 33 words). Rotating-gear path matches. |
| BgRelayObjects_Draw | NOT MATCHED, GLOBAL_ASM + `#if 0` draft | 7/30 words differ. ROM hoists `mov r1,#1` and picks a different register pair for params/1. Tried a shared constant and an inverted branch (worse, 12 words). |

## Not attempted (out of stage-1 time budget)
Action functions outside the actor dir, GLOBAL_ASM in functions_*.cpp (not moved):
- FUN_003cacd0 (168 B): rotating gear action, N64 `func_808A939C`
- FUN_00181f38 (152 B): dampe wait, N64 `func_808A90F4`
- FUN_001596b8 (124 B): dampe closing, N64 `func_808A91AC`
- FUN_00181c84 (4 B, `bx lr`): N64 `BgRelayObjects_DoNothing`
Unlabeled N64 funcs reached only through these: `func_808A9234`, `func_808A932C` (not in the Init list).

## Layout and debt
- struct: DynaPolyActor (0x1BC) + actionFunc 0x1BC, switchFlag 0x1C0, unk_1C1 (room id) 0x1C1, timer 0x1C2, skelAnimModel 0x1C4, skelAnimModel2 0x1C8; size 0x1CC.
- Init chain data is at raw 0x0051355C (`#define sInitChain ((InitChainEntry*)0x0051355C)`). Needs a symbol.
- Save/PlayState statics by raw offset: `*(u32*)(play+0x7F70)` = the N64 `D_808A9508` bit flags; EVENTCHKINF_65 = `gSaveContext+0x800+0xF8` bit 0x20 (raw, unverified name).
- Local prototype casts instead of redeclaring: `FUN_00372f38` (7 args) and `FUN_00350f34` (4 args). include/functions.hpp has truncated decls. Left include/ untouched.
- Draw calls `MTX34CopyAsm(&mtx, actor+0x148)` (raw offset, unverified).

## Files touched
Only inside `ws/Bg_Relay_Objects/`: the actor dir `z_bg_relay_objects.cpp` and `.hpp` (struct fixed, `unk_1A4[0x28]` removed). No changes outside the actor dir, no include/ edits.
