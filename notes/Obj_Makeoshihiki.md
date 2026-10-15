# Obj_Makeoshihiki status (stage 1, Haiku)

| Function | Status | Notes |
|---|---|---|
| ObjMakeoshihiki_Init | matched (C, actor dir) | Byte-identical. `unk_19A = 1` first, `Actor_SpawnAsChild` args inline. Spawn pos read via `block->posVecs[typeIdx]` directly (a `Vec3f* spawnPos` local changed scheduling). |
| ObjMakeoshihiki_Draw | NOT matched, left as asm | Body is close but 10 words differ (register choice: block ptr vs float constant 0.001f in r1/r2; `eor` operand order for sfx conds). Also the cfg-merged tail: ROM Draw is 396 B, the last 8 B at 0x3815F0 are an unreferenced `mov r0,#0; bx lr` merged into Draw by functions.tsv (cfg `FUN_003815f8` starts after it). Draft kept under `#if 0`. |
| data (sBlocks, sFlags, sFlagSwitchFuncs) | matched (C, after InitVars) | Layout order at 0x535420 is sFlagSwitchFuncs, sBlocks, sFlags (not N64 order). `__attribute__((used))` kept because Draw (asm) references them. |

Tried for Draw (about 6 variants, all same 10-word diff): operand order of `^` for sfx conds; `cond = Flags_GetSwitch(..) != 0` form; inline dist expression with local `Vec3f* childPos`; `Vec3f* childPos` hoist; helper `static inline` for dist squared (current).

Not yet tried: `__attribute__((noinline))`-free forms with the block ptr hoisted before the loop via `Vec3f* posVecs` local, and the rotY-based `sBlocks` indexing done as `sBlocks + i` pointer arithmetic.

Notes:
- `child` cantMove write uses local `ObjOshihikiCantMove` (Obj_Oshihiki header has `unk_1A4[0x8C]`, cantMove at 0x22E).
- `FUN_00372244(&play->unk_5FCC, 0x0A, 0x100048c)` = Sfx_PlaySfxCentered(NA_SE_SY_TRE_BOX_APPEAR); no header change.
- No `include/` edits. No files outside `src/game/actors/Obj_Makeoshihiki/` touched.

Pending for Sonnet pass: ObjMakeoshihiki_Draw (see above; the 8-byte tail needs a cfg split, not a C fix).

Check: `scripts/ws_check.sh Obj_Makeoshihiki` shows baseline only (FUN_00249af8).
