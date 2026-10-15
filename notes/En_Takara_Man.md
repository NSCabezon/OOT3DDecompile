# En_Takara_Man: Stage 1 (Haiku-only) status

Baseline check (ws_check.sh): only FUN_00249af8 differs (known baseline). Build OK.

## Actor functions (src/game/actors/En_Takara_Man/z_en_takara_man.cpp)
| Function | Status | Notes |
|---|---|---|
| EnTakaraMan_Destroy | MATCHED (C) | FaceAnimations::Destroy, FUN_003508b8(model), SkelAnime_Free2 |
| EnTakaraMan_OverrideLimbDraw | MATCHED (C) | limb 7 -> unk_22C, limb 0 -> unk_232 (N64 limbs 8/1), FUN_0034df48(mtx, rot) |
| EnTakaraMan_Init | NOT MATCHED, GLOBAL_ASM + #if 0 draft | Draft logic written from asm. Not yet compared; the flag at PlayState+0x7F94 and the mapIndex/dungeonKeys store are unverified. Not iterated. |
| EnTakaraMan_Update | NOT MATCHED, GLOBAL_ASM + #if 0 draft | 10 words differ. Tried: play-before-self declaration, local eyeTimer. Reg allocation still differs (ROM keeps play in r6, reloads eyeTimer via ldrsh r2). |
| EnTakaraMan_Draw | NOT MATCHED, GLOBAL_ASM + #if 0 draft | Only 4 words differ (fastchk; the GraphicsContext_UnknownStub call is inlined at link time, so its bl is expected). ROM loads eyeTextureIdx with `ldr r1,=0x5d6; ldrsh r2,[r1,r4]` and computes faceAnims ptr (r0) after; C does not reproduce that ordering yet. |

## Not touched (outside the actor dir)
- Action chain: Init sets actionFunc = FUN_001810fc (0x001810fc, src/functions/functions_180000s.cpp, N64 func_80B176E0), which sets actionFunc = FUN_003e7af4. Remaining chain functions (N64 func_80B1778C, 80B17934, 80B17A6C, 80B17AC4, 80B17B14) not identified yet. Not moved. Limit of ~15 functions was not reached; time budget was the constraint.

## 3DS layout notes
- Actor fields: N64 X maps to 3DS X+0x3C8 for the eye/dialog fields (dialogState 0x5D4, eyeTextureIdx 0x5D6, eyeTimer 0x5D8, unk_212 0x5DA, unk_214 0x5DC, originalRoomNum 0x5DE, height 0x5E4, pos 0x5E8, unk_22C 0x5F4, unk_232 0x5FA). actionFunc is at 0x5D0.
- SkelAnime at 0x1A4 (0x84 bytes), jointTable 0x228, morphTable 0x3FC, skelAnimModel 0x600, FaceAnimations 0x604. Size 0x7D0.
- Static "sTakaraIsInitialized" is a byte in PlayState at +0x7F94 on 3DS. The header has no field for it, so the draft uses a raw offset.
- play->actorCtx.flags.chest is at PlayState+0x2238.
