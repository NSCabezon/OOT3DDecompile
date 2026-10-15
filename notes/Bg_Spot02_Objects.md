# Bg_Spot02_Objects (cascade stage 1 Haiku, stage 2 Sonnet)

| Function | Status | Notes |
|---|---|---|
| BgSpot02Objects_Destroy / Update / Draw | matched (C) | stage 1 |
| BgSpot02Objects_Init | matched (C) | stage 2. Fixes: `BgSpot02Quad quad` at function scope (struct copy from EQU `sQuad`=0x4D71AC, gives frame 0x50 and quad @sp+0x1c), `idx = 6; if (scene==0x5C) idx = 7;` AFTER DynaPolyActor_Init, y += 255 before actionFunc store, `n = 2` at start of the else branch, case 2: `n = 3;` before `actor->flags |=`, case 3/4: actionFunc store before draw store, real `gSaveContext.eventChkInf[1] & 0x2000` instead of raw 0x588758. |
| FUN_003e8b60 (N64 func_808AC8FC) | matched (C), moved | empty |
| FUN_00175404 (func_808ACAFC) | matched (C), moved | |
| FUN_001e8c0c (func_808ACC34) | matched (C), moved | |
| FUN_00207130 (func_808AD3D4) | matched (C), moved | |
| FUN_0019bb28 (func_808AC908) | matched (C), moved | function-local static Vec3f + guard: guard EQU 0x5136D0 (reached as sInitChain+4 for the test), vec EQU 0x569A88, ctor via inline helper, `__cxa_guard_release` from model_manager.cpp is linker-inlined to `mov r0,r0` |
| FUN_0023c210 (func_808AD450 draw) | NOT matched, asm | draft under `#if 0` (best 38/180 words). u32-word matrix build (Bg_Haka_Water trick) gives the right identity/translate shape; remaining: VFP reg/schedule (pos vcvt order, 0.1f hoisting). `if (animSpeed == 0.0f) {}` needed to keep 0.0 in a VFP reg. |
| FUN_0021f548 (func_808ACCB8 draw) | NOT attempted in C (asm) | 282 lines: inline Matrix_Translate/RotateZ(sin/cos)/Scale + float colour lerp; same matrix idiom as FUN_0023c210. |

Files outside the actor dir: src/functions/functions_{140000s,180000s,1C0000s,200000s,3E0000s}.cpp (GLOBAL_ASM lines for the 5 moved FUN_ removed). include/: none.
ws_check.sh: only baseline FUN_00249af8 differs.
