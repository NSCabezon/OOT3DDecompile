# Bg_Haka_MeganeBG — stage 1 (Haiku-only) status

Check: `scripts/ws_check.sh Bg_Haka_MeganeBG` → only baseline (FUN_00249af8). Final file is the hybrid below.

| Function | Status | Notes |
|---|---|---|
| BgHakaMeganeBG_Destroy | MATCHED (C, in actor .cpp) | link check clean |
| BgHakaMeganeBG_Update | MATCHED (C, in actor .cpp) | link check clean |
| BgHakaMeganeBG_Init | NOT MATCHED, GLOBAL_ASM | C draft under `#if 0`. Compile-only diff shows the calls reproduce (ReadCollisionHeaderFromZsi = nop in ROM, bl in fastchk). Full link with C Init shifts layout (non-function bytes differ, ~7800 functions flagged), so the C version was NOT kept. Next step: find which construct changes data/layout (likely the static sInitChain placement, see CLAUDE.md data-before-InitVars note) and retry. |
| BgHakaMeganeBG_Draw | NOT MATCHED, GLOBAL_ASM | C draft under `#if 0`, 3 words differ (ROM reloads `params` and the model pointer in the else branch; compiler CSEs them). Not yet linked in the actor file; try the link check next. |

Not decompiled (action functions in functions_*.cpp, left as GLOBAL_ASM):
- FUN_0019d0d4 (hidden platform idle, 72 B, functions_180000s.cpp)
- FUN_001779b0 (elevator drop, 252 B, functions_140000s.cpp)
- FUN_001e9a08 (rotating spin, 164 B, functions_1C0000s.cpp)
- FUN_002597d4 (gate do-nothing = `bx lr`, functions_240000s.cpp) trivial, easy next
- FUN_002597d8 (gate wait for switch, 176 B, functions_240000s.cpp)

Layout facts from the asm (3DS):
- Model slots: 4 SkeletonAnimationModel* at actor+0x1C4..0x1D0, loaded by FUN_00372f38 (11-arg form) with indices 0x11,0x13,0x15,0; freed by FUN_00350f34 (6-arg form). Draw uses slot[params].
- switchFlag u8 at 0x1C0 (params>>8), timer s16 at 0x1C2, actionFunc at 0x1BC, bgId at 0x1A4 (DynaPolyActor).
- params: 0 hidden platform (flag 0x80, timer 30, DynaPoly idx 0xB); 1 elevator (timer 120, idx 0xD, culling 3000); 2 rotating (flag 0x10, idx 0xF, culling downward += 500); 3 gate (home.y += 100, idx 0).
- Init tail uses ReadCollisionHeaderFromZsi(DynaPolyInfo_Alloc(...), &colHeader); the call is a nop in the ROM (linker --inline).

Files touched (ws only): src/game/actors/Bg_Haka_MeganeBG/z_bg_haka_meganebg.{cpp,hpp}. Nothing outside the actor dir.
