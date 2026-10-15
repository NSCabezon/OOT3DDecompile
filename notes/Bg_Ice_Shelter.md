
<!-- merge 2026-10-14 15:01:22 -->
# Bg_Ice_Shelter — cascade stage 1 (Haiku), batch 1/1

Baseline ws_check: only FUN_00249af8 differs (known). Init (asm) and data (`data/z_Bg_Ice_Shelter.data.s`) left as GLOBAL_ASM.

| Function | Status | Note |
|---|---|---|
| BgIceShelter_Update | MATCHED | N64 `actionFunc(this, play)` |
| BgIceShelter_Destroy | MATCHED | 3-model FUN_00350f34 call via typed cast (include prototype has 3 args) |
| FUN_003bf214 (N64 Idle) | MATCHED | moved into actor .cpp, GLOBAL_ASM removed from functions_3A0000s.cpp |
| FUN_003f5f00 (N64 Melt) | MATCHED | moved into actor .cpp, GLOBAL_ASM removed from functions_3E0000s.cpp; flag test as `(params >> 6) & 1` |
| BgIceShelter_Draw | MATCHED | 3DS model draw (MTX34CopyAsm + FUN_00358778 + SetUnkAC per case) |
| FUN_001a2fa0 (N64 SpawnSteamAround) | MATCHED (stage 3, Opus) | moved into actor .cpp, GLOBAL_ASM removed from functions_180000s.cpp. Needs prim/env colors as REAL statics after InitVars (armcc derives prim = env - 4) + actor-local data tail `z_Bg_Ice_Shelter_data_tail.s` (= disassembly data chunk minus first 8 bytes; image-neutral, ws_check baseline). FUN_00366150 params (.., s16 scale, s16 life) |
| FUN_001cf550 (N64 SpawnSteamAlong) | NOT MATCHED (stage 3) | 29 words (draft #if 0): real color statics fixed env/450 hoisting; left = const hoist set (ROM 20/40, ours 0.2/0.0) + GPR rotation. Needs signs[]+sSteamLinePositions as real statics too → whole data chunk to 0x5120F0 in C incl. Init's guard word → data split |
| BgIceShelter_Init | NOT MATCHED (stage 2) | draft under #if 0 (inline InitColliders/InitDynaPoly, guard + Vec3f ctor, 0x5xxxxx EQUs in data.s); ROM keeps two actor-pointer copies (mov r4,r0; mov r5,r0), not reproduced (~132 words) |

Notes:
- Tables live in `BgIceShelter_data.s` as absolute EQU symbols (0x512028..0x51213C, draw color 0x4D7140). Separate symbols keep Melt matching; with raw casts armcc folded the three tables into one base.
- Header: DynaPolyActor base (0x1BC), actionFunc 0x1BC, cylinders 0x1C0/0x218, alpha 0x270, skelAnimModel[3] at 0x274.

Stage 3 (Opus): debt = `z_Bg_Ice_Shelter_data_tail.s` is a trimmed copy of disassembly/data/z_Bg_Ice_Shelter.data.s (proper fix: split in data_chunks.txt). Merge must copy the new actor-dir .s.
