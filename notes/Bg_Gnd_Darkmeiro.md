# Bg_Gnd_Darkmeiro - Stage 1 (Haiku-only) status

ws_check.sh: baseline only (FUN_00249af8). Not merged into oot3d/.

## Actor dir functions
| Function | Status | Notes |
|---|---|---|
| BgGndDarkmeiro_Destroy (0x0029a69c) | MATCHED (C) | Needs `DynaPoly_DeleteBgActor(play2, ...)` and direct `thisx`/`play2` args; the `play` local + `self->` variant made armcc predicate the call (mismatch). |
| BgGndDarkmeiro_Update (0x00379cdc) | MATCHED (C) | Tail call through `updateFunc`. |
| BgGndDarkmeiro_Init (0x0029a3b4) | NOT MATCHED, asm + #if 0 draft | Draft compiles, 660 B vs 744 B ROM. Prologue differs (ROM `sub sp,#0xc`, `str r7,[sp,#8]` for colHeader; draft pushes r3). Case 1 branch shape and the `DynaPolyInfo_Alloc` size condition also differ. ~8 variants tried, none within budget. |

## Action/draw functions still in functions_*.cpp (asm, untouched, NOT moved)
| Function | Role | Status | Notes |
|---|---|---|---|
| FUN_001292d4 | UpdateBlockTimer | draft under #if 0, not compiled | Plays SFX via Audio_PlaySoundGeneral with raw data addrs 0x54AC20/24; calls FUN_0036d940. Not checked against ROM. |
| FUN_0012aad0 | UpdateSwitchBlock | draft under #if 0, not compiled | Uses timer3 (0x1C2) countdown that the N64 code lacks. Toggle block via FUN_0036b940 / FUN_0036d15c. Not checked. |
| FUN_00382314 | DrawInvisiblePath | draft under #if 0, not compiled | Uses SkeletonAnimationModel methods FUN_003721e0 / FUN_00372170(0). Not checked. |
| FUN_00382520 | DrawStaticBlock | draft under #if 0, not compiled | Same as above with arg 1. Not checked. |
| FUN_00382360 | DrawSwitchBlock | asm only, no draft | Uses Math_CosS, FUN_00357ed4, FUN_003695cc. |
| FUN_003f5450 | Noop | shared generic stub, left as is | |
| FUN_0012aacc | UpdateStaticBlock | shared generic stub (`bx lr`), left as is | |

## Struct notes (3DS)
- `DynaPolyActor dyna` at 0x000 (bgId 0x1A4). Fields after it: actionFlags 0x1BC (u16), timer1 0x1BE, timer2 0x1C0, timer3 0x1C2, updateFunc 0x1C4, skelAnimModel1 0x1C8, skelAnimModel2 0x1CC. Size kept at 0x1DC (pad) as before, not verified.
- Init case 1 reads `play->sceneNum` (0x104), play+0x4C30 byte == 0xB, gSaveContext[0xE] != 0 (raw in draft).

## Next steps for Sonnet pass
1. Init: fix prologue/register allocation (try `play` vs `play2` usage, colHeader declared in an inner block after the first FUN_00372f38 call).
2. Move FUN_001292d4 / FUN_0012aad0 / FUN_00382314 / FUN_00382520 into the actor .cpp once their drafts match (remove the GLOBAL_ASM lines in functions_120000s.cpp / functions_380000s.cpp only then).
3. DrawSwitchBlock draft (FUN_00382360).
