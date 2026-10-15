# Obj_Warp2block STATUS (Opus closing pass)
| Function | Status |
|---|---|
| ObjWarp2block_Init | MATCHED: params read via `thisx->params` (self->dyna.actor.params swaps r0/r1 on the literal loads); static inline setup helpers + inverted if |
| ObjWarp2block_Destroy | MATCHED: `self->dyna.actor.params`, `play` local, `&self->dyna.actor` to FUN_003508b8 |
| ObjWarp2block_Draw | MATCHED: inline `GET_PLAYER((PlayState*)state)` (no play local) keeps the 0x20ac literal |
| ObjWarp2block_Update / DoNothing | MATCHED (stage 1) |
| FUN_0025ac68 | NOT MATCHED (4 words: play/player r7/r8 swap). Draft under #if 0 in actor .cpp. Also needs raw addr 0x0020803C (cfg debt) |
| FUN_00184184, FUN_00185468 | not attempted (timebox) |
ws_check: baseline only.
