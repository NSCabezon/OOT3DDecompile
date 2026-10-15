# Demo_Im — Stage 1 (Haiku-only) status

Actor dir: `src/game/actors/Demo_Im/` (z_demo_im.cpp, z_demo_im.hpp). ws_check.sh: baseline only (FUN_00249af8).

## Functions (actor dir)
| Function | Status | Notes |
|---|---|---|
| DemoIm_Destroy | MATCHED | SkelAnime_Free2(+0x1A4), FaceAnimations::Destroy(+0x9E0), Collider_DestroyCylinder(+0xBD8) |
| DemoIm_Update | MATCHED | action table @0x0051BD40 via raw address (no symbol yet) |
| DemoIm_Draw | MATCHED | drawConfig table @0x0051BDBC via raw address (no symbol yet) |
| DemoIm_Init | NOT MATCHED (asm) | 127-line asm; draft under `#if 0`. Needs ZAR_GetCMBByIndex/FUN_00353e78 arg setup, FUN_0036932c/FUN_0037266c face-anim calls, the jump-table switch, and the default path (FUN_00343088 with 0x004D878C). Not iterated. |

## Not in actor dir (not touched)
- Action funcs `FUN_*` / DrawSolid / DrawTranslucent / DrawNothing: referenced by the 0x0051BD40 / 0x0051BDBC tables (31 action entries, 3 draw entries). Not decompiled in this stage (time budget). Entries seen in the table: 0x27DE44, 0x27DD38, 0x245240, 0x28F274, 0x2A15EC, ... (full list in data dump `z_Demo_Im.data.s`, offsets 0x38..0xBC). Draw: 0x27DD34 (nothing), 0x2A144C (solid), 0x28F108 (translucent).
- Data `z_Demo_Im.data.s` stays GLOBAL_ASM.

## Struct
`DemoIm` in z_demo_im.hpp: fields action @0xBB4, drawConfig @0xBB8 (verified by matched code); skelAnime @0x1A4 and faceAnim @0x9E0 and collider @0xBD8 are padding-only for now. Size kept at 0xC5C.

## Notes for next stage
- 3DS actor differs from N64 ovl_Demo_Im (N64 has no FaceAnimations; 3DS uses ZAR/CMB model loading in Init).
- Table-by-raw-address is debt: add a symbol for 0x0051BD40 / 0x0051BDBC in the disassembly config.
- Matching trick that worked for Update/Draw: `if ((u32)x < N) { table = (T*)ADDR; if (table[x] != NULL) table[x](...); }` (table pointer declared inside the if; declaring it at function top hoists the literal load and fails).
