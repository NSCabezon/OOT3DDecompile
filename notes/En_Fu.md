
<!-- merge 2026-10-15 09:38:41 -->
# En_Fu batch status

ws_check: baseline only (FUN_00249af8).

| Function | Status |
|---|---|
| FUN_00145a4c, FUN_001172d4, FUN_00104720 | MATCHED (moved) |
| EnFu_OverrideLimbDraw, EnFu_Destroy, EnFu_WaitForPlayback, EnFu_TeachSong, EnFu_WaitChild, EnFu_Init | MATCHED |
| FUN_001124c4 (moved) | MATCHED: Animation_Change_00375c08 declared in N64 arg order (skel, idx, speed, start, end, mode, morph) |
| EnFu_WaitAdult | MATCHED: function-local `static s16 yawDiff` lives in TU .data (0x523A1C), cut from the data chunk |
| EnFu_PostLimbDraw | MATCHED: guarded static Vector3f; guard 0x523A20 in TU .data, object 0x599128 pinned in .bss |
| EnFu_Draw | near miss, 8 words (#if 0 draft): ROM builds the face pointer from incoming r0 (+0x800,+0x48 -> r6) and a separate r4-based +0x800 (r5); every thisx/self CSEs them |
| EnFu_Update | near miss, 4 insns (#if 0 draft; was 54): ROM does `mov r1,#1; strb r1,[r0,#0x27d]; add r1,r0,#0x1a4` off the incoming r0 |

## Static pins (workspace infra)
python3 -P scripts/pin_static.py ws/En_Fu split 0x523A1C --size 8
python3 -P scripts/pin_static.py ws/En_Fu bss 0x599128 12 "z_en_fu.o(+BSS)" --label z_en_fu_PostLimbDraw
