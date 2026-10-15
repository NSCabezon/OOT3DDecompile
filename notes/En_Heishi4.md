# En_Heishi4 (stage 1, Haiku) status

Baseline check (scripts/ws_check.sh En_Heishi4): only FUN_00249af8 differs (known). Non-function bytes: 0 differing.

| Function | Status | Notes |
|---|---|---|
| EnHeishi4_Update | MATCHED (C) | (Actor*, GameState*) signature; `__ARM_common_memcpy2_6` for torsoRot copy |
| EnHeishi4_Destroy | MATCHED (C) | Collider_DestroyCylinder call (linker-inlined to `mov r0,#1`) |
| EnHeishi4_Draw | MATCHED (C) | GraphicsContext_UnknownStub(play->state.gfxCtx) = N64 Gfx_SetupDL_25Opa (empty on 3DS) |
| FUN_00211524 (limb cb, moved from functions_200000s.cpp) | MATCHED (C) | name kept (ld-pinned) |
| EnHeishi4_Init | MATCHED (C, stage 2 Sonnet) | `EnHeishi4ActionFunc fn` join var: `if (type==0\|\|type==4) fn=A; else switch(type){case 7: radius/height stores BEFORE `u8* flags = ...` (pool order), kill-first `if (a\|\|!b) {Actor_Kill; return;} fn=C; break; case 8: fn=D; self->actionFunc=fn; default: goto done;}` then `self->actionFunc = fn`. |

Action functions (stage 2, all MATCHED in C, moved into z_en_heishi4.cpp, GLOBAL_ASM lines removed from functions_180000s/200000s/280000s/380000s.cpp):
FUN_00180b24 (func_80A56328), FUN_002057dc (func_80A56544), FUN_0021c1d0 (func_80A5673C), FUN_00299518 (func_80A563BC), FUN_0038a814 (func_80A56614).
Still asm (not in scope): FUN_0025a074 (func_80A56B40), FUN_001748f4 (func_80A56874); N64 func_80A56900/994/A50/ACC not located.
Globals: 0x00588758+0xF4/0xFC = gSaveContext.eventChkInf[4]&0x20 (master sword) / [8]&1 (Zelda fled); +0x1C of 0x588858 = infTable[6]&0x1000; 0x587958 = gSaveContext (linkAge +4, nightFlag +0x10). 3DS addition: FUN_0038a814 sets textId 0x7206 if eventChkInf[8]&1 on day outside market guard house/night.

Data: `GLOBAL_ASM("data/z_En_Heishi4.data.s")` kept. syms.s EQUs: sCylinderInit 0x0052636C, sMaskReactionSets 0x00526364, EnHeishi4_sGameFlags 0x00588758 (unnamed 3DS global; used by Init draft, bytes 0xF4 and 0xFC).

3DS differences found: case-7 collider height is 30.0f in ROM (N64: 5). Actor_MoveForward replaces Actor_MoveXZGravity. Limb indices 8/15 (N64 9/16). Dying-guard anim via FUN_00353c9c csabIndex 3.

Struct: EnHeishi4 offsets are 3DS (actionFunc 0x8A8, headRot 0x8AC, torsoRot 0x8B2, pos 0x8B8, type 0x8CC, collider 0x908, skelAnimModel 0x960).
