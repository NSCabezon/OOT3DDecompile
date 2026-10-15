# En_Kakasi3 - Opus closing pass (2026-10-13)

ws_check: baseline only (FUN_00249af8).

| Function | Status |
|---|---|
| EnKakasi3_Init / Destroy / Draw / OverrideLimbDraw / PostLimbDraw | matched (earlier stages) |
| EnKakasi3_Update | MATCHED: `(EnKakasi3*, PlayState*)` signature + `DECR()` in timer loop + `self->actor.` everywhere |
| FUN_00180b78 (N64 func_80A911F0) | MATCHED, moved from functions_180000s.cpp. Fix: FUN_00353020 prototype in N64 order (skel, anim, speed, start, end, mode, morph) |
| FUN_0029964c (N64 func_80A91284) | MATCHED, moved from functions_280000s.cpp. Fix: `(EnKakasi3*, PlayState*)` + N64 if/else for textId (not ternary) |
| FUN_003e56c0 (N64 func_80A91348) | NOT MATCHED, GLOBAL_ASM in functions_3E0000s.cpp. Draft under #if 0: one insn short (&skelAnime.curFrame folded to `add r0,r4,#0x1e4`, ROM does `add #0x1a8; add #0x3c`) |
