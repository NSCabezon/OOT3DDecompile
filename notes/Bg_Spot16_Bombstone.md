# Bg_Spot16_Bombstone: status (stage 1 Haiku, stage 2 Sonnet, stage 3 Opus)

| Function | Status | Notes |
|---|---|---|
| BgSpot16Bombstone_Update | matched (C) | 9/9 words |
| BgSpot16Bombstone_Destroy | matched (C) | 15/15 words; FUN_00357248 tail call |
| BgSpot16Bombstone_Draw | matched (C) | 26/26; the two params branches are written out separately (needed to match ROM) |
| FUN_0011093c (wait for Bombiwa object, action) | matched (C), moved into actor .cpp | 26/26; GLOBAL_ASM line removed from src/functions/functions_100000s.cpp (ws copy only) |
| BgSpot16Bombstone_Init | NOT matched, left as GLOBAL_ASM | stage 3 (Opus) draft in `#if 0`: size now 836 = ROM. Intact path matches incl. the `mov r5,r4` copy: InitIntact helper takes `Actor* actor` + local `self` cast; ProcessInitChain and sin/cos/skel/draw/action stores via `self`, SetScale/mass/collider helpers/rot loads/FUN_0036a924 arg via `actor`. Debris: inline `row[2] * (1.0f / 600.0f)` (no scaleFactor local) stops s17 hoist. Helpers take `PlayState*`, Init has `play` local. Remaining: shouldLive phi coalesces with zero const (ours zero r6 / 1 in r8; ROM zero r8, shouldLive r6=1, fail `mov r6,r8`) + 0x1aa pool ldr scheduled later. ~35 variants (return types s16/bool, if/else/do shapes, local order, Actor* debris param, Self*/PlayState* Init sig) all leave it. |
| FUN_003bfb70 (intact action, 740 B) | matched (C), moved into actor .cpp | 185/185 (stage 2). Needs N64 helpers PushPlayer/TrackBomb/SpawnRocks as static fns, `play2` copy passed to TrackBomb only, `actor` alias in PushPlayer, ABS on the raw expression, sTimer/sPlayerBomb as one extern struct (single literal base). GLOBAL_ASM line removed from functions_3A0000s.cpp |
| FUN_003cb7cc (debris action, 760 B) | matched (C), moved into actor .cpp | 190/190 (stage 2). `index = index + 0;` no-op needed so armcc keeps the `cmp r5,#5` loop guard (debt). Timer check is `(s16)unk_154 > 90`. GLOBAL_ASM line removed from functions_3C0000s.cpp |

Other workspace changes:
- `src/game/actors/Bg_Spot16_Bombstone/z_bg_spot16_bombstone.hpp`: struct with 3DS layout (JntSph/cylinder/actionFunc/skelAnimModel offsets), local JntSph typedefs.
- `src/game/actors/Bg_Spot16_Bombstone/data_syms.s`: EQU for 0x513B60 (sTimer), 0x513B64 (sPlayerBomb), 0x513B70 (debris table), 0x513D9C/0x513DA8 (init chains), 0x513BE8 (JntSph init), 0x513BF8 (cylinder init).
- `src/data_syms.s` additions (actor dir): EQU sFragmentScales 0x513DBC, sFragmentParams 0x513DD0, sStatics 0x513B60 (struct {s16 timer; Actor* playerBomb @+4}).
- `src/functions/functions_3A0000s.cpp` / `functions_3C0000s.cpp`: GLOBAL_ASM lines for FUN_003bfb70 / FUN_003cb7cc replaced by comments (moved).
- Not attempted (time budget): FUN_003bcf7c (boulder-broken action, N64 func_808B5A94 + func_808B5240).
- FUN_003cb7cc `index = index + 0;` hack: N64 forms (`if (index < 5) do {} while (index != 5 / < 5)`, plain for/while, `index = 0` before if) all fail (752 B). Only `for (index = index; index < 5; index++)` also matches (0/190) - equally a no-op, so the original hack was kept.
- `src/functions/functions_100000s.cpp`: one GLOBAL_ASM line replaced by a comment (FUN_0011093c moved).

ws_check.sh: baseline only (FUN_00249af8).

UNMATCHED: BgSpot16Bombstone_Init
