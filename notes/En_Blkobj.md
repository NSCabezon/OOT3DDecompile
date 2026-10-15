
<!-- merge 2026-10-14 12:20:14 -->
# En_Blkobj STATUS (cascade stage 2, Sonnet)

Actor .cpp: `src/game/actors/En_Blkobj/z_en_blkobj.cpp`. Header now has typed fields (bgId 0x1A4, alpha 0x1BC, timer 0x1BE, actionFunc 0x1C0, skel[2] 0x1C4); offset macros dropped.

## Functions
- DoNothing / Update (now `(EnBlkobj*, PlayState*)`) / Wait / SpawnDarkLink / DarkLinkFight: MATCHED
- EnBlkobj_Destroy: MATCHED. `(Actor*, GameState*)`, `PlayState* play` local declared FIRST, `self` second, and the FIRST call (DynaPoly_DeleteBgActor) takes raw `(PlayState*)state` for arg 0 (rest use `play`).
- EnBlkobj_Init: MATCHED. Dead alias `EnBlkobj* s2 = self;` used for the `skel[1]->unk_0C->FUN_00372d94(...)` line fixed the zar/1 swap.
- EnBlkobj_Draw: NOT ATTEMPTED (structural): 155 insns, SetUnkAC `strb 1,[model,#0xac]` r7/r0 merged-1 class + inline MTX34 + ~10 unnamed FUN_ callees, duplicated per-model block. Stays GLOBAL_ASM.

ws_check.sh En_Blkobj: baseline only (FUN_00249af8).
