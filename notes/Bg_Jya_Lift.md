# Bg_Jya_Lift: STATUS (cascade stage 1, Haiku)

| Function | Status | Notes |
|---|---|---|
| BgJyaLift_Init | matched | C in actor .cpp |
| BgJyaLift_Destroy | matched | tail-calls FUN_00350f34 |
| BgJyaLift_Update | matched | |
| BgJyaLift_Draw | matched | calls FUN_00331284 (2-arg, not in include/) |
| BgJyaLift_DelayMove | matched | |
| BgJyaLift_Move | matched | Camera callee is FUN_0036ae48 (Camera_SetFinishedFlag not a ROM symbol) |

Data: `data/z_Bg_Jya_Lift.data.s` kept as GLOBAL_ASM; `data_syms.s` adds EQU symbols
`BgJyaLift_sIsSpawned` (0x512A90) and `BgJyaLift_sInitChain` (0x512A94).

Files outside actor dir: none. include/ additions: none.
ws_check.sh: baseline only (FUN_00249af8).
Debt: raw offsets for play->roomCtx.curRoom.num (0x4C30), GET_ACTIVE_CAM (0xA64), camera setting (0x18A).

UNMATCHED: none
