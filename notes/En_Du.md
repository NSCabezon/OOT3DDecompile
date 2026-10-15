
<!-- merge 2026-10-14 17:59:22 -->
# En_Du (G3, sonnet stage) STATUS

All functions matched in C (src/game/actors/En_Du/z_en_du.cpp): EnDu_Init, EnDu_Update, EnDu_Draw, FUN_00194824 (moved from functions_180000s.cpp), FUN_00216d44 (moved from functions_200000s.cpp), plus the earlier Haiku set.
Notes: EQU data symbols in data_syms.s (cylinder inits x3, colchk info, anim info, collider offsets 0x4D94C0). Header fields renamed (blinkTimer @0x510, unk_50A/B/C u8).
Idioms: SetFace helper (arg order), N64 MultVec3f wrapper + `void* thisx` 4th param (PostLimbDraw), SetupAction inline helper for >=6 branch, `{ s16 talkState = 0; ... }` for the 0x554 store, offsets copy in its own block (tail call), play2 alias.
ws_check En_Du: baseline only (FUN_00249af8).
