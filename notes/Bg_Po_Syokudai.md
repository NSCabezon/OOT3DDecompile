
<!-- merge 2026-10-14 17:51:22 -->
# Bg_Po_Syokudai (haiku stage 1)

- BgPoSyokudai_Destroy: MATCHED (LightContext_RemoveLight, Collider_DestroyCylinder, env byte 0x3237 = 0xFF, FUN_00350f34, tail FUN_0035046c)
- BgPoSyokudai_Update: MATCHED (room compare uses thisx->room; SetAC/SetOC with inline collider ptr)
- Init, Draw: still GLOBAL_ASM
- Header: fields added (flameTextureScroll 0x1A6, lightNode 0x1A8, collider region 0x1C4 as raw, skelAnim 0x21C)
- ws_check: baseline only

## sonnet stage 2
- BgPoSyokudai_Init: MATCHED (data_syms.s EQUs for sInitChain/sCylinderInit/flame idx/prim colors; no `env` local; rand * 30.0f).
- BgPoSyokudai_Draw: NOT matched (35 words, far-ish; ~60 variants). Draft #if 0: GPR numbering (play r7/1 r6) + translate vec VFP regs + pause tail.
