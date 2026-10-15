
<!-- merge 2026-10-15 09:38:40 -->
# En_Ta (G23 sonnet stage) status

Baseline: ws_check.sh En_Ta -> only FUN_00249af8 differs.

## Matched (C in z_en_ta.cpp, GLOBAL_ASM removed from functions_*.cpp)
FUN_00145c0c FUN_00145c3c FUN_00145c6c FUN_0012cfac FUN_0012cfec FUN_002336b0 FUN_001a3638
FUN_003c15c4 FUN_003c14fc FUN_001cf750 FUN_0014594c FUN_003af690 FUN_003cd668 FUN_00112594 FUN_001043ec
FUN_003af700 FUN_003af754 (cfg splits)
Sonnet stage: EnTa_Draw, EnTa_Destroy, EnTa_Update ((Actor*, PlayState*) signature), FUN_0021734c (guarded static Vector3f, pinned),
FUN_003b04b8 (N64 EnTa_RequestTalk helper with an s16 yawDiff local), FUN_003af8f4, FUN_003b021c.

## Splits (workspace only; apply to main with cfg_split.py if merged)
- FUN_003af690 @0x003af700 -> FUN_003af700
- FUN_003af700 @0x003af754 -> FUN_003af754

## Static pin (workspace infra, must be replayed/copied on merge)
python3 -P scripts/pin_static.py ws/En_Ta pin --guard 0x52F58C --obj 0x59B668 --obj-size 12 --obj-sel "z_en_ta.o(+BSS)" --label z_en_ta_FUN_0021734c

## Parked (C kept under #if 0)
- EnTa_Init: body matches modulo layout; ROM dumps the literal pool in the middle of the Actor_Spawn block (b over pool) and we dump it after the
  Actor_Kill tail (~91 insns displaced); a few day-branch store schedules differ too. far/layout.

## Not attempted / not matched (outside this group's list)
FUN_003b963c FUN_001167cc FUN_00145b60 FUN_00185fe4 FUN_00104078 FUN_003685f4 FUN_00186090 FUN_003ae400 FUN_003c1620 FUN_003ae6b8
FUN_003af83c FUN_00114f78 FUN_00202678 FUN_0011260c FUN_003ae784 FUN_00145a6c FUN_0015f828 FUN_001453f8 FUN_001cf7d0 FUN_003b0360 FUN_003cd4b8
