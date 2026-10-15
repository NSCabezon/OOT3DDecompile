# Bg_Spot08_Iceblock - cascade stage 1 (Haiku), batch 1/1

Functions (batch list):
- BgSpot08Iceblock_Destroy: MATCHED (variant 1, fastchk + ws_check clean)
- BgSpot08Iceblock_Draw: MATCHED (variant 1, fastchk + ws_check clean)
- BgSpot08Iceblock_Update: MATCHED (variant 1; link-level fix: RNG call is `Rand_S16Offset` @0x368b68, not the `_003702c8` alias)

Notes:
- Header `z_bg_spot08_iceblock.hpp`: struct expanded from `Actor + char[0x58]` to `DynaPolyActor dyna` + offsets from asm (actionFunc 0x1BC, bob phases/increments 0x1E4-0x1EA, skelAnimModel1/2 0x1F4/0x1F8). Field names are provisional.
- Destroy calls `FUN_00350f34` through a `void(*)(Actor*, ...)` cast: the ROM callee is variadic (walks pointer args until NULL), while functions.hpp declares it with 3 fixed args.
- Init, and the GLOBAL_ASM for Init, untouched (not in this batch).
- Variants beyond the first were not needed: all three matched first try.

ws_check.sh Bg_Spot08_Iceblock: baseline only (FUN_00249af8).

## Stage 2 (Sonnet): BgSpot08Iceblock_Init
- NOT matched (212/214 words in fastchk). Draft under `#if 0` in the actor .cpp; GLOBAL_ASM restored. ws_check: baseline only.
- Diff left: inlined SpawnTwinFloe, arg setup order `mov r2,r6; mov r1,r4` (ROM) vs `mov r1,r4; mov r2,r6` (ours) before Actor_SpawnAsChild. Tried ~15 variants (actor/self/cast parent, play casts, helper vs inline, local order): none flips it; some change Init-wide reg alloc.
- Structure learned: Init inlines CheckParams, InitDynaPoly (static helper w/ `colHeader = NULL` + ReadCollisionHeaderFromZsi), SetupFloatNonrotating/Rotating/OrbitingTwins/NoAction (actionFunc = FUN_003bcd9c / FUN_003b35c8 / FUN_003c0460 / NULL). Jump table at 0x37b6dc is in the function body (ROM bytes).
- Idioms: CheckParams needs full case list incl. 0xFF; second `switch(params & 0xF)` must read through a `u16 t = params` local to get ldrh r0; `Collision* = NULL` local at top gives the `mov r5,#0`; z store through `actor->` (not self->dyna.actor) prevents tail-merging of the vstr in SpawnTwinFloe; sInitChain via data_syms.s EQU 0x00513914 (draft needs it).
- Header got unk_1C4/unk_1D8 f32 (set to 1.0f in Init).

## Stage 3 (Opus): BgSpot08Iceblock_Init
- MATCHED (214/214, fastchk + ws_check baseline only). Actor fully matched 4/4.
- Fix: in SpawnTwinFloe, wrap the call in a block with `PlayState* play2 = play;` and use `play2` for BOTH `&play2->actorCtx` and the play arg (using it only for the play arg breaks reg alloc Init-wide). This flips `mov r1,r4; mov r2,r6` to the ROM's `mov r2,r6; mov r1,r4`.
- Draft `#if 0` removed; GLOBAL_ASM for Init removed.
