
<!-- merge 2026-10-15 11:00:53 -->
# Bg_Haka_Ship (G27, sonnet stage) STATUS

Baseline ws_check: only FUN_00249af8 differs (OK, 2026-10-15).

| Function | Insns | State | Notes |
|---|---|---|---|
| BgHakaShip_Update | 11 | MATCHED (C) | |
| BgHakaShip_SetupCrash | 16 | MATCHED (C) | counter 60 (N64 40 x1.5) |
| BgHakaShip_ChildUpdatePosition | 18 | MATCHED (C) | |
| BgHakaShip_Destroy | 20 | MATCHED (C) | FUN_00350f34 with 4 model ptrs (0x1D0..0x1DC) |
| BgHakaShip_CrashShake | 21 | MATCHED (C) | `(counter % 4 - 2) * 3` form |
| BgHakaShip_CutsceneStationary | 26 | MATCHED (C) | phase const `M_PI * 2.0f / 75.0f` (not `(M_PI/25)*2/3`, 1 ulp off) |
| BgHakaShip_WaitForSong | 27 | MATCHED (C) | counter 195 |
| BgHakaShip_CrashFall | 38 | MATCHED (C) | |
| BgHakaShip_Init | 91 | MATCHED (C) | sInitChain now C static (data chunk GLOBAL_ASM removed); spawn uses block-local `PlayState* p2` |
| BgHakaShip_Move | 99 | MATCHED (C) | player-pos check reproduced as float compares |
| BgHakaShip_Draw | 117 | MATCHED (C) | G27 sonnet: translate consts were wrong in the draft (-4858/860/926, 0/0/-1852, bell -485.8/86); first model read via `((BgHakaShip*)actor)->` (r0 = param copy); `static inline` Vec3f-local translate helper; `s16 yo` + `f32 k` locals fix pi/int VFP numbering; bell const -485.80002f |

Struct (3DS): DynaPolyActor dyna @0, actionFunc @0x1BC, counter u8 @0x1C0, switchFlag u8 @0x1C1, yOffset s16 @0x1C2, bellSfxPos Vec3f @0x1C4, 4x SkeletonAnimationModel* @0x1D0..0x1DC; size 0x1E0.
Splits applied: none.
