# Bg_Bowl_Wall: STATUS (Haiku stage 1)

Matched: 5 / 9 functions (ws_check: baseline only, `FUN_00249af8`).

| Function | Status | Notes |
|---|---|---|
| BgBowlWall_Init | MATCHED (C in actor .cpp) | `ReadCollisionHeaderFromZsi(DynaPolyInfo_Alloc(...), &colHeader)` reproduces the ROM (no call emitted, store only). Two ZARInfo branches (idx 0/1). |
| BgBowlWall_Destroy | MATCHED | Tail call to `FUN_00350f34`. |
| BgBowlWall_Update | MATCHED | timer decrement + `actionFunc(self, state)`. |
| BgBowlWall_Draw | MATCHED | `speed = 1.0f` must be assigned AFTER `MTX34CopyAsm` (else vldr is hoisted). |
| FUN_00180e80 (BgBowlWall_InitImpl) | MATCHED, moved | Moved from `src/functions/functions_180000s.cpp` (GLOBAL_ASM line removed). Target-pos/rot tables by raw address 0x510C14 / 0x510C1C (locals, scoped to their blocks, needed for register match). `actionFunc = 0x3E699C` raw. |
| BgBowlWall_WaitTargetHit (0x3E699C) | NOT MATCHED | Lives inside `FUN_003E68C4` (Bg_Bom_Guard, cfg-merged tail after a literal pool; functions.tsv has no entry). Needs tsv split. Draft under `#if 0`. |
| BgBowlWall_Explode (0x1070AC) | NOT MATCHED | Raw `DCB` blob inside `FUN_00107054` (no disassembly for the body). Draft under `#if 0` (from N64 logic, unverified). |
| BgBowlWall_Disappear | NOT MATCHED | Address not located (candidate pointer in Explode's literal pool looked wrong, not used). Draft under `#if 0`. |
| BgBowlWall_WaitReappear | NOT MATCHED | Address not located. Draft under `#if 0`. |

## Layout (3DS) used in the actor header
- `bgId` 0x1A4, `actionFunc` 0x1BC, `homePos` 0x1C0, `effCenterPos` 0x1CC, `targetHit` u16 0x1D8 (ldrh in asm, type uncertain), `timer` s16 0x1DA, `bowlingGirl` 0x1DC, `skelAnimModel` 0x1E0; size 0x1E4 (unchanged).
- En_Wall_Tubo target: `effCenterPos` at +0x1AC (local view struct in the .cpp, not the En_Wall_Tubo header).

## Debt
- Raw data addresses 0x510C14 (sWallRots, s16[4]) and 0x510C1C (sWallTargetPositions, Vec3f[4]) should become EQU symbols in the data dump.
- Raw action pointer 0x3E699C (WaitTargetHit) should become a symbol once FUN_003E68C4 is split.
- `BgBowlWall_Explode` / `Disappear` / `WaitReappear` need the cfg split of FUN_00107054 and locating the others.

## Process notes
- Any function whose compiled size differs from ROM shifts everything after it in the link (ws_check shows ~10k diffs). Keep unmatched functions as GLOBAL_ASM; drafts under `#if 0` (tools/preproc.py ignores #if/#else).
- Per-function checker: `ws/Bg_Bowl_Wall/tmp/fast.py <actor.cpp> <Func...>` (compile actor file alone; `FASTV=-v` shows word diffs), `tmp/dis.py <Func> <addr> <size>` for side-by-side disassembly.
