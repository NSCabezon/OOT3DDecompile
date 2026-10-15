# Bg_Mori_Hashira4 — STATUS (Opus closing pass)

7/8 matched. ws_check.sh: baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| BgMoriHashira4_Init | MATCHED | N64 `BgMoriHashira4_InitDynaPoly` restored as `static` helper (inlined); colHeader's address-taken slot lives in the helper, so armcc tail-calls Actor_Kill. Two separate kill `if`s as in N64. |
| Destroy, Update, FUN_00110830, FUN_0012b610, FUN_0012b5d0, FUN_0037ac08 | MATCHED (earlier stages) | |
| PillarsRotate @0x003bf92c | LEFT AS ASM | cfg-merged inside FUN_003bf708; needs functions.tsv split |

Cleanup: sUnkTimer / sInitChain raw addresses replaced by EQU symbols `BgMoriHashira4_sUnkTimer` (0x00513314) / `BgMoriHashira4_sInitChain` (0x00513318) in actor-dir `data_syms.s`; pointer-local hack in GateWait removed.
