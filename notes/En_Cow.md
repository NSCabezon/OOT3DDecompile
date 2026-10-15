
<!-- merge 2026-10-15 17:59:54 -->
# En_Cow (G40 Haiku pass)
MATCHED (C in actor .cpp, ws_check clean):
- FUN_00249044 (1 insn, empty stub; EnCow draw of tail) - moved from functions_240000s.cpp
- FUN_00249048 (UpdateTail) - moved from functions_240000s.cpp
- FUN_00183a84 (GiveMilkEnd) - moved from functions_180000s.cpp
- FUN_003ee340 (GiveMilkWait) - moved from functions_3E0000s.cpp
- FUN_0010f308 (GiveMilk) - moved from functions_100000s.cpp
- FUN_0015d0fc (TalkEnd) - moved from functions_140000s.cpp
- FUN_003ebed4 (Talk) - moved from functions_3E0000s.cpp
- FUN_003f062c (CheckForEmptyBottle) - moved from functions_3E0000s.cpp
- EnCow_Destroy: 2x Collider_DestroyCylinder (linker-inlined to mov r0,#1) + Collider_DestroyJntSph, then SkelAnime_Free2 (tail)

NOT MATCHED (draft in actor .cpp under #if 0, GLOBAL_ASM kept or original GLOBAL in functions_*):
- EnCow_Draw: C draft matches all code; only 2 literal-pool words differ (FUN_0014ff48/FUN_0016d584 pool order: ROM loads r3=FUN_0014ff48 first). ~6 variants with local fn-pointer vars failed. Left as asm (#if 0 draft in z_en_cow.cpp).
- FUN_0033ddbc (9-float copy, ROM vldmia/vstmia s0-s8, 24 B): struct copies give 32 B with ldm/stm; per-element copies 52 B. 3 variants, unsolved. Left asm.
- FUN_00314cfc (UpdateAnimation, 93 insns): 3 words off, all in the scale.y breath angle literal (ROM `lsl #26; add #0xC0000000; asr #16`). 6 variants. Draft #if 0 in functions_310000s? NO: still GLOBAL in functions_310000s.cpp, C draft lives in z_en_cow.cpp #if 0.
- FUN_003f0504 (IdleTail, 66 insns): 7 words off (second distance check register order: ROM yaw in r1). 8 variants. Draft #if 0.
- FUN_003f1244 (Idle, 56 insns): 52 words off (eponas flag block register allocation). 3 variants. Draft #if 0; asm stays in functions_3E0000s.cpp.
- FUN_00349008 (SetColliderPos-like, 51 insns, JntSph pos at +0x1F0 / +0x248): 31 words off (vec rotation op order / reloads). 3 variants. Draft #if 0.
- FUN_0014ff48 (PostLimbDraw-ish, 37 insns): function-local static Vec3f guarded by __cxa_guard (guard 0x521A1C, obj 0x598FCC). Blocker: LOADER/guard recipe = orchestrator-only (pin_static.py). Not attempted further.
- FUN_0016d584 (83 insns, limb draw with sinf/cosf on headRot): only read the head; not attempted in depth.

Notes for merge:
- Struct EnCow in z_en_cow.hpp: actionFunc at 0x7B8, rest opaque (0x1A4..0x7B8). Local EnCowTailState at this+0x700 (flags 0xAE, timer 0xB0, breathTimer 0xB2).
- Collider_DestroyJntSph is declared locally in the .cpp (not in include/).
- Removed GLOBAL_ASM lines for matched FUNs from ws copies of src/functions/functions_{240000s,3E0000s,100000s,140000s,180000s}.cpp (merge_ws.py handles these).
- ws_check.sh En_Cow: baseline only (FUN_00249af8).
- Scratch in ws/En_Cow/tmp removed at end.
