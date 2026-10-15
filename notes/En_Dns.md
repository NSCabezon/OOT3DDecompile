
<!-- merge 2026-10-15 09:50:48 -->
# En_Dns — G26 haiku stage

Matched (C in z_en_dns.cpp, ws_check baseline):
- EnDns_Destroy, EnDns_Draw, EnDns_SetupWait, EnDns_Wait, EnDns_SetupBurrow, EnDns_Burrow, EnDns_Talk
- FUN_0025697c, FUN_00256974, FUN_003c3bdc, FUN_003c3bf0, FUN_0010040c (moved from functions_*.cpp)
- FUN_00189644, FUN_00189668, FUN_001896a8 (moved from functions_180000s.cpp)
- FUN_0012e264 (SetupNoSaleBurrow). cfg split: tail FUN_0012e2c8 (8 B `mov r0,#0; bx lr`) split out
  (split/asm/*, tail line kept in functions_120000s.cpp; head GLOBAL_ASM line removed).

Not matched (drafts or asm, all baseline):
- FUN_0014953c (CanBuyDekuSeeds head, stays in functions_140000s.cpp): 4/8 words, slot load picks r1 vs ROM r2.
  Tail FUN_0014955c is a separate ROM entry (not in group list, asm).
- FUN_0014949c (CanBuyDekuNuts head, tail FUN_001494f0 asm): 15/21 words, capacity load / cmp order.
- FUN_001616f0 (CanBuyArrows): 11/60 words, gSaveContext base reg (r0 vs r1).
- FUN_0027f3f8 (func_80028990 dust, 76 insns): 52/83 words; draft under #if 0 (static helper variant).
- EnDns_Update: 3/55 words (textId store: ROM loads 0x116 offset into r1).
- EnDns_ChangeAnim: guarded function-local static (__cxa_guard at 0x522330 region). Blocked, infra (pin_static).
- EnDns_Init: 113 insns, guarded static loader (guard 0x55A21C, obj 0x5BE5B8, FUN_0036788c) + ZAR/SkelAnime_InitFlex. Blocked, infra.

Notes:
- Header: 3DS layout (collider 0x1A8, dnsItemEntry 0x208, skelAnime 0x210, jointTable 0x294, morphTable 0x5A0; size 0x8AC).
- Data via actor-dir data_syms.s EQUs: EnDns_sStartingTextIds (0x52236C), EnDns_sAnimPtrs (0x522324).
- New TU: z_en_dns_anim.cpp (EnDns_CurFramePtr accessor, inlined by armlink, used by SetupBurrow).
- DAT_00520234/DAT_00520238 are referenced as extern (defined by En_Horse data_syms.s; not re-EQU'd here to avoid L6200E).

## G26 sonnet stage
Matched (0 words, ws_check baseline): EnDns_Init, FUN_001616f0 (CanBuyArrows; needs the cfg split FUN_001616f0 @0x0016178c -> FUN_0016178c, applied in this ws), FUN_0014953c (CanBuyDekuSeeds) and FUN_0014949c (CanBuyDekuNuts).
- The last two are cfg JOINS: ROM lists head+tail as two functions (FUN_0014953c+FUN_0014955c, FUN_0014949c+FUN_001494f0) but each is ONE armcc function (180 B / 160 B, shared pool). C is the whole function; their GLOBAL_ASM lines are removed (the asm file held both labels, no ld block for the tails, nothing else references them). Both need a dead `EnDns* s2 = self;` at the top.
- EnDns_Init: model-manager guard (existing pin), `thisx->textId`, `s16 type` local for the item-entry index, dead `s2` alias on the actionFunc store. New EQUs in data_syms.s: EnDns_sInitChain 0x5223B0, EnDns_sCylinderInit 0x522334, EnDns_sItemEntries 0x522384.
Not matched (drafts under #if 0): EnDns_Update NEAR 3 words (textId offset literal order, ~35 variants); FUN_0027f3f8 NEAR 10 words but data blocker (ROM derives &DAT_00520234 from &DAT_00520238); EnDns_ChangeAnim static blocker (ROM addresses guard 0x522330 / object 0x5223BC relative to sAnimPtrs 0x522324 -> all TU statics must be real C data in ROM order; armcc puts the guard first). No pin_static applied.
