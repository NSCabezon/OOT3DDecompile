
<!-- merge 2026-10-15 10:29:19 -->
# Bg_Mizu_Bwall (G30, haiku stage)
- FUN_001980c4 (DoNothing, moved from functions_180000s.cpp): MATCHED 1/1
- BgMizuBwall_Update: MATCHED 2/2
- FUN_001741a8 (Break timer, moved from functions_140000s.cpp): MATCHED 8/8
- BgMizuBwall_Destroy: MATCHED 16/16
- BgMizuBwall_Draw: MATCHED 50/50 (speed float loaded after MTX34CopyAsm; alpha/type cond as `if (type==1) {..} else if (type==2 && alpha==255)`)
- BgMizuBwall_Init: not in this batch, still GLOBAL_ASM
- Header: 3DS layout (N64 +0x58), ColliderTris types copied from Bg_Bombwall. sizeof unchanged (0x318).
- ws_check: baseline only (FUN_00249af8)
