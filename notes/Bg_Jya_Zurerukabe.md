# Bg_Jya_Zurerukabe — STATUS (stage 1, Haiku)

Matched 3/4 actor functions (ws_check.sh: baseline only, FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| BgJyaZurerukabe_Init | MATCHED (C) | `static inline` setter for `actionFunc = 0x003bf9b0` was needed to get the register order right (plain assignment put the constant in r2). |
| BgJyaZurerukabe_Destroy | MATCHED (C) | |
| BgJyaZurerukabe_Draw | MATCHED (C) | Same body as Jya_Amishutter Draw (skeleton model). |
| BgJyaZurerukabe_Update | NOT MATCHED (asm, draft under `#if 0`) | Draft in the .cpp. Blocker: the N64 `func_8089B4C8` (player knockback check) is inlined after the switch jump table inside the ROM Update asm. The knockback callee (`Actor_SetPlayerKnockbackLarge` equivalent) is not identified in the repo (no prototype, no symbol). The draft leaves the call as a comment. Player offsets used in the draft are raw (stateFlags1 +0x1710, wallPoly +0x78, world.pos.y +0x2C). Not compiled, so not verified. |

## Embedded action functions (not in actor dir, left as raw bytes)
- `func_8089B7C4` (N64 wait) at `0x003bf9b0`, and the rest of this actor's action code (func_8089B80C, func_8089B870) are raw DCB bytes inside `disassembly/asm/FUN_003bf948.s` (pulled by `src/functions/functions_3A0000s.cpp`). This is a cfg-merge: FUN_003bf948 (OnePointCutscene switch) contains them after its literal pool. Not movable without a cfg split, so Init references the address (`ZUR_ACTION_WAIT`), same approach as Bg_Mori_Hashira4.
- Consequence: func_8089B870 etc. can't be decompiled in the actor dir until the cfg is split.

## Data
- Tables (D_8089B9F0, D_8089B9F8, D_8089BA18, D_8089BA30, sInitChain, and float D_8089B9C0 at 0x569A40) stay in `data/z_Bg_Jya_Zurerukabe.data.s`. They are referenced via absolute EQU symbols in `z_bg_jya_zurerukabe_syms.s` (same pattern as En_Okarina_Effect/gWeatherMode.s).

## Files changed (ws only)
- `src/game/actors/Bg_Jya_Zurerukabe/z_bg_jya_zurerukabe.cpp`
- `src/game/actors/Bg_Jya_Zurerukabe/z_bg_jya_zurerukabe.hpp` (struct fields: dyna, actionFunc @0x1BC, unk_1C0/1C2/1C4/1C6, skelAnimModel @0x1C8, size 0x1CC)
- `src/game/actors/Bg_Jya_Zurerukabe/z_bg_jya_zurerukabe_syms.s` (new)

No include/ edits. No changes outside the actor dir.

## Next (Sonnet/Opus stage)
1. Identify the knockback callee at the switch in Update (look for its `bl` in the raw bytes of BgJyaZurerukabe_Update.s, the tail after the jump table at 0x382ED8).
2. Try the draft under `#if 0`, switching Update to C, then check with fastchk.
3. Consider a cfg split of FUN_003bf948 so the action functions can be moved into the actor dir.
