# En_Ganon_Mant (stage 1, Haiku)

| Function | Status | Reason |
|---|---|---|
| EnGanonMant_Init (0x0026966C, 16 B) | MATCHED | `actor->flags &= ~1;` (literal, no ACTOR_FLAG_0 macro) |
| EnGanonMant_Destroy (0x0026967C, 192 B) | NOT matched, asm | Fixed-address static loader guard 0x55A21C / object 0x5BE5B8 with atexit; ROM 192 B vs draft 148 B, 27/48 words differ. Draft under #if 0. |
| EnGanonMant_Update (0x002925AC, 796 B) | NOT matched, asm | Same loader guard; embedded __FILE__ string inside function text; many unknown callees; inline struct init at actor+0x17BC. |

Workspace check: baseline only (FUN_00249af8).
Files touched: ws/En_Ganon_Mant/src/game/actors/En_Ganon_Mant/z_en_ganon_mant.cpp only. No include/ changes. oot3d/ untouched.
