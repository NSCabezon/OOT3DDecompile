# Eff_Dust: status (Haiku stage 1)

Check: `scripts/ws_check.sh Eff_Dust` -> only baseline FUN_00249af8 differs. OK.

| Function | State | Notes |
|---|---|---|
| EffDust_Update | MATCHED (C) | `self->actionFunc(self, play)`; fastchk 0/2 words |
| EffDust_Draw | MATCHED (C) | `self->drawFunc(actor, play)`; fastchk 0/2 words |
| EffDust_Destroy | NOT MATCHED, asm | Draft under `#if 0` in z_eff_dust.cpp: 31/48 words differ, 144 B vs 192 B. Blocked by the shared function-local static loader (guard 0x55A21C, object 0x5BE5B8) with inlined __cxa_atexit dtor block. Same class as Item_Inbox FUN_003a0e88 / En_Ganon_Mant Destroy. Needs a global fix. |
| EffDust_Init | NOT MATCHED, asm | Not drafted. 176 lines: same static loader guard, ZAR lookup (slot+0x3A64 idiom, ZAR_GetCTXBByIndex(zar+0x10, 5)), allocator vtable calls (vtbl[3] on 0x55A1F8, 0x1B8 bytes, __FILE__ string literal "d:\hoome\queen\dailyBuild\game_us\sources\z_eff_dust.cpp" embedded in text), 5-entry jump table on params, and R_UPDATE_RATE timer tail. Blocked by the shared loader and the in-text string. |

Layout (3DS, N64 +0x58 from 0x14C): distanceTraveled @0x1A4, initialPositions @0x2A4, index @0x5A4,
life @0x5A5, dx/dy/dz/scalingFactor @0x5A8..0x5B4, actionFunc @0x5B8, drawFunc @0x5BC, unk_5C0[2] @0x5C0 (3DS-only model pointers).
Header z_eff_dust.hpp rewritten to this layout (size 0x5C8). Actor is 0x1A4 bytes.

Files changed (all in ws/Eff_Dust/src/game/actors/Eff_Dust/): z_eff_dust.cpp, z_eff_dust.hpp.
Scratch: ws/Eff_Dust/tmp/draft/. Outside actor dir: none. include/ untouched.

Matched: 2/4 (Update, Draw). Leftover: EffDust_Init, EffDust_Destroy.
