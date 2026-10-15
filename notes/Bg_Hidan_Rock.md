
<!-- merge 2026-10-14 19:14:43 -->
# Bg_Hidan_Rock (G9, haiku stage)

Header: struct rebuilt on DynaPolyActor (0x1BC) — actionFunc @0x1BC, type @0x1C0, timer @0x1C2, unk_1C4,
unk_1C8 (Vec3f), collider @0x1D4, skelAnimModel[3] @0x22C. Size 0x238.
Data: data_syms.s (actor dir) EQU D_8088BF60 = 0x005699D4 (Vec3f {3310,120,0}).

- BgHidanRock_Destroy: MATCHED (0/21).
- FUN_00128704 (N64 func_8088B90C): MATCHED (0/12). Moved from functions_120000s.cpp.
- FUN_0040cbe8: MATCHED (0/12). Kept in actor cpp (was its GLOBAL_ASM). Returns 1 when arg==0 and
  *(play+0x1708) == FUN_004c6d34. Its first arg is really a Player*-like pointer (the caller passes the player);
  the C type is PlayState* for now. No callers in the main tree.
- FUN_003e1f74 (func_8088B954): MATCHED (0/16). Moved from functions_3E0000s.cpp. velocity.y is stored before actionFunc.
- FUN_00176cdc (func_8088B634): MATCHED (0/21). Moved from functions_140000s.cpp. Timer literal 30 (3DS scale).
- BgHidanRock_Draw: NOT matched (43/66). Draft under `#if 0`. ROM keeps play in r5, frame 0x3c, predicated
  ldm/stm copies for the vector and model draws. Per-branch model calls and frame padding made it worse.
- FUN_003eb5ec (func_8088B69C shake): NOT matched (63/79). Draft under `#if 0`, asm kept in functions_3E0000s.
  ROM rounds Math_SinS/CosS args with predicated vnmls/vmla (sign taken from the int angle). Not solved.
- FUN_003d9534 (func_8088B79C): NOT matched (93/118). Draft under `#if 0`, asm kept. Adds a 3DS camera quake
  block (Quake_Add/SetSpeed/SetQuakeValues/SetCountdown) that the ROM hoists into r4-r8,sb,sl,fp.
- FUN_003b9ec0 (func_8088B990): NOT matched (90/115). Draft under `#if 0`, asm kept. Same register-layout issue.
- BgHidanRock_Init: NOT ATTEMPTED (no draft). Needs: 3-model FUN_00372f38 (9 args: this, play, &m0, 0x18,
  &m1, 8, &m2, 0xb, 0) returning ZARInfo, GetCMABByIndex(1) + FUN_00372d94 on unk_0C, DynaPolyInfo_Alloc,
  data 0x00511BCC (sInitChain) and 0x00511BD4 (sCylinderInit), FUN_003e0910 as B268 action.
- BgHidanRock_Update: NOT ATTEMPTED (no draft). Needs data 0x00511BC4 / 0x00511BD4, the player/FUN_0040cbe8
  check, FUN_0034a80c, DynaPoly_GetActor, VEC3TransformAsm.

Unlisted asm still in actor cpp: FUN_003d0830 (N64 func_8088BC40, flame draw).

## Sonnet stage (G9)
MATCHED (all 0 diff, ws_check baseline): BgHidanRock_Init, BgHidanRock_Update, BgHidanRock_Draw, FUN_003e0910 (moved from functions_3E0000s.cpp),
FUN_003eb5ec, FUN_003d9534, FUN_003b9ec0 (retry; GLOBAL_ASM removed from functions_3E0000s/3C0000s/3A0000s, C now in the actor cpp),
FUN_00176c38 and FUN_00140384 (new, from the two cfg splits below).
CFG SPLITS applied in this ws (replay on main): FUN_00176b04 0x00176c38 FUN_00176c38 ; FUN_00140218 0x00140384 FUN_00140384.
 - FUN_00176c38 = N64 func_8088B5F4; it tail-calls FUN_00140384 (= func_8088B24C, 1-arg). FUN_00140384 is declared `__attribute__((noinline))` on its prototype so armcc emits `b` instead of inlining.
 - FUN_0040cbe8 also needs `__attribute__((noinline))` (ROM calls it from Update).
New EQUs in actor data_syms.s: BgHidanRock_D_8088BFC0 (0x511BC4, f32[2]; [1]=500.0f), BgHidanRock_sInitChain (0x511BCC), BgHidanRock_sCylinderInit (0x511BD4).
Key tricks: FUN_003eb5ec 2/3-scaled sin/cos arg = `(s32)(ang > 0 ? half + (f32)ang*two*third : ... - half)` with f32 locals declared two,half,third and assigned two,third,half (VFP regs vs pool order).
 FUN_003d9534 quake call constants as separate s32 locals (`z1=0,z2=0,z3=0`, five, three, speed) + `f32 d = xzDistToPlayer` local + quake block INSIDE the bgCheckFlags&2 block + ternary clamp.
 FUN_003b9ec0 = N64 `(type==0 && Smooth<0.1) || (type!=0 && Smooth<0.1)`. Update: `play2`-style alias `PlayState* play2 = play` on the sceneNum read and `BgHidanRock* s2 = self` on the room read.
NOT matched: FUN_003d0830 (flame draw, ~116/158 words): draft under #if 0 in the cpp; blocker is the integer-store identity+translation MTX34 class (see comment there).
