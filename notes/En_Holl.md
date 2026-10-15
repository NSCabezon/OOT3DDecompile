# En_Holl (stage 2, Sonnet) — status

Actor dir: `src/game/actors/En_Holl/` — `z_en_holl.cpp`, `z_en_holl.hpp`, `z_en_holl_unk.cpp` (new), `data_syms.s` (new).
`ws_check.sh En_Holl` = baseline only (FUN_00249af8).

EnHoll struct: planeAlpha@0x1A4 (s16), side@0x1A6 (u8, was unk_1A6), resetBgCoverAlpha@0x1A7, actionFunc@0x1A8, skelAnimModel@0x1AC, unk_1B0 s8.

| Function | Status | Notes |
|---|---|---|
| EnHoll_Init | MATCHED (stage 2) | N64 shape: static inline `EnHoll_SetupAction` + `EnHoll_ChooseAction`; table/initchain now EQU symbols (the 1/0 regalloc problem was the raw-address casts) |
| EnHoll_Destroy / EnHoll_Update | MATCHED (stage 1) | |
| FUN_00339f0c | MATCHED, moved to `z_en_holl_unk.cpp` | own TU (in-file it is inlined into Update); reads `EnHoll_gUnk54ABD4[2]` (EQU 0x0054ABD4) |
| FUN_00239934 (V_DOWN_BGCOVER_LARGE) | MATCHED, moved into actor .cpp | GLOBAL_ASM line removed from functions_200000s.cpp; floats 3.476f / 0.39999998f (exact ROM bit patterns) |
| FUN_00275264 (V_INVISIBLE) | NOT matched, 2 words | draft under `#if 0`; only idx register differs (ROM `lsr r1,r1,#0xa; lsl r2,r1,#4`, build `lsr r2,r1`). Fixed on the way: nested `if (abs<200){if(abs>50)}` (not `&&`), local `yd` for the s0/s1 order |
| FUN_0021df78 (V_BGCOVER) | NOT matched, 2 words | same idx register issue |
| FUN_001eaab0 (H_BGCOVER_SWITCHFLAG) | NOT matched, 11 words | only callee-saved swap (play r5/r6 vs ROM r6/r5); the shared reset block needs a `goto reset` into the inner else (armcc otherwise merges into the first copy) |
| FUN_003f1d7c (H_VISIBLE_NARROW) | NOT matched, 10 words | everything but the planeAlpha store: ROM emits `mov r0,#0x1a4` right before `usat/strh`, build hoists it to the start of the block. 3DS-specific: `unk_1B0 = 15` after the request loop (`nn::svc::SleepThread(0)` inlined by linker), `unk_1B0 = 1` after a room swap |
| FUN_001eac68 (H_INVISIBLE) | NOT matched, ~60 words | needs play/actor in r5/r4 (build swaps), `isKokiri` kept live in r0 through a dead predicated `ldrsbne r0,[r4,#3]` I could not reproduce; compare chain (nested z range checks via `goto body`) is OK |
| EnHoll_Draw | NOT matched (draft `#if 0`) | 3DS-specific, not the N64 DL code: sets model colour (`FUN_003687a8/003589cc/00358964`), Y-rotates the model matrix by pi when `side == 0` (sinf/cosf not folded), and for scene 1 tints the two rooms (`FUN_003695cc`, jump table on room num). Structure and ~all instructions equal; ROM shares one `bl` after case 10 and keeps case 12 separate, keeps constant 1 in r7. All case orders tried |

Findings (3DS vs N64):
- Room/transition data are raw PlayState offsets: curRoom@0x4C30 (num s8 @+0), prevRoom@0x500C, size 0x3DC; roomCtx.status@0x5401; transition list ptr@0x5B8C (entries 0x10, `sides[2]` first, id@+4); bgCoverAlpha@0x5C30; player ptr@0x20AC.
- Room_RequestNewRoom = `FUN_0033b6bc(play, &roomCtx, num)`, followed on success by `FUN_0033b608()` (3DS extra) and `actionFunc = FUN_001ce6b8` (WaitRoomLoaded, still asm). Room_FinishRoomChange = `FUN_0036c520(play, &roomCtx)`.
- `FUN_001ce6b8` (WaitRoomLoaded) stays asm in functions_1C0000s.cpp (not in scope); thresholds differ from N64: V_DOWN uses 520/180 and alpha `(s16)(180-abs)*0.5f`; H_BGCOVER uses `255 - (s32)((abs-50)*(255/50.0f+0.8f))`.
- Visible-narrow trigger dists table 0x004D9664 (2x4 f32), debug-cam flag 0x00516EAC (EQU symbols).
