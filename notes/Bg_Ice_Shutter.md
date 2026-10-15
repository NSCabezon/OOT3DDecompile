# Bg_Ice_Shutter: STATUS (Opus closing pass)
All 7/7 functions MATCHED in C (4 actor + 3 moved FUN_s). ws_check: baseline only.
- BgIceShutter_Init: MATCHED. Fix = `CollisionHeader* colHeader = NULL;` at top + real `ReadCollisionHeaderFromZsi(...)` call (armlink inlines it to `str r0,[r1]`), FUN_00372f38(...,6,0) after params split, and `temp_f6 * Math_SinS/CosS(...)` operand order for vmla.
- Debt: sInitChain referenced as raw `(InitChainEntry*)0x0051215C` (data dump has no label; disassembly is read-only).
