# En_Toryo (Haiku stage 1) status

Workspace: ws/En_Toryo (mkws.sh, built). Check: ws_check.sh En_Toryo -> baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| EnToryo_Draw | MATCHED (C) | `GraphicsContext_UnknownStub(play->state.gfxCtx)` = N64 Gfx_SetupDL_25Opa (empty on 3DS), then SkelAnime_DrawOpa. |
| EnToryo_OverrideLimbDraw | MATCHED (C) | limb 9 -> FUN_0034e01c(mtx, torsoRot), limb 10 -> headRot. |
| EnToryo_Update | NOT MATCHED (asm, draft #if 0) | 6/68 words differ: stores `unk_80[1]=1` (0x225) — armcc puts the #1 in r0 instead of r1 (scheduling). Yaw/shape operand order fixed via s16 locals; DEG_TO_BINANG2 = (f32)(s16)(deg*182.04445f) (ROM constant is exactly +/-14563.0f). Tried: collider local (worse), byte-store form (same). |
| EnToryo_Destroy | NOT MATCHED (asm, draft #if 0) | ROM contains a dead 0xA4-byte struct copy from +0xB4C to stack (memcpy4) before FUN_003508b8(actor, m1, m2, m3) and SkelAnime_Free2 tail. Struct meaning unknown. C draft without the copy is 56 vs 92 bytes. |
| EnToryo_Init | NOT MATCHED (asm) | Blocked on data: sCylinderInit (0x52FA04), sColChkInfoInit (0x52FA3C), sDamageTable (0x59B6F8), sEnToryoAnimation (0x52FA48) are in data/z_En_Toryo.data.s with no symbols. Needs data symbols (EQU) or a split of that data chunk. Object-bank lookup: base = play+idx*0x80+0x3A5C if idx<0x13 && *(s32*)(play+idx*0x80+0x3A64), zar = base+0x10 (NULL+0x10 when not loaded). |
| EnToryo_PostLimbDraw | NOT MATCHED (asm) | Function-local guarded static Vec3f sMultVec (guard 0x52FA00, data 0x59B718). Needs LOADER_RECIPE-style pinning or EQU symbols. |
| FUN_00178af8 (EnToryo_Idle action) | NOT MOVED (asm in functions_140000s.cpp) | Large talk state machine (jump table at 0x178b84). Not attempted in stage 1. |

Layout (actor-dir header): skelAnime @0x1A4, jointTable @0x228, morphTable @0x66C, actionFunc @0xAB0, collider @0xAB4 (0x58), stateFlags @0xB14 (u16), interactInfo @0xB18 (0x28: headRot @+8, torsoRot @+0xE, trackPos @+0x18), skelAnimModel x3 @0xB40/44/48.

Unknown: skelAnime.unk_80[1] = 1 (0x225) written in Update; purpose unknown.
FUN_003508b8 real prototype takes 4 args; include decl is truncated, so the call casts the pointer to a 4-arg typedef.
Files touched outside actor dir: none. include/ additions: none.
