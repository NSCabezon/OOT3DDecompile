
<!-- merge 2026-10-14 18:51:04 -->
# En_Anubice (G7, haiku stage)

Matched (C, 0 words off in fastchk, ws_check baseline):
- EnAnubice_Init, EnAnubice_Destroy, EnAnubice_Draw
- FUN_00378924 (PostLimbDraw, eyes), FUN_002a94f4 (OverrideLimbDraw, head pitch as Z rotation of mtx columns 0/1), FUN_001746d4 (SetupDie) (moved from functions_*.cpp, names kept)

Not in this batch (still GLOBAL_ASM): EnAnubice_Update (not in the prompt list).

Struct: EnAnubice rewritten with ROM offsets (3DS = N64 + 0x3E8 after the skeleton tables; skelAnime 0x1A4, jointTable 0x228, morphTable 0x430, actionFunc 0x638, headPitch 0x660, headPos 0x668, collider 0x6B0, size 0x708).

Debt: EnAnubice_Init calls FUN_00372f38 through a function-pointer cast with 3 args (ROM passes only r2 = 0, no stack args); Destroy calls FUN_003508b8 the same way with 2 args. Both match; the cast is a workaround for the truncated prototypes in include/functions.hpp.
Data: data_syms.s EnAnubice_sCylinderInit = 0x520608, EnAnubice_sDamageTable = 0x520640.

## G7 sonnet stage
- EnAnubice_Update: left asm, draft under #if 0 (~35 instr-lines off via difflib; fastchk word count cascades). Matching: stack layout (decl order base, rotated, hitPos, mtx; 3DS knockbackTimer = 15), knockback zero chain `base.x = base.y = rot.x = rot.y = rot.z = 0`. Open: 10.0f/0.1f hoisted to entry (ROM reloads), sl/sb swap (acHitInfo vs sound const), flameCircle ptr in r2 vs r1 (ROM `add r1,#0x100; ldrh [r1,#0xac]`), Vec3s->Vec3f hitPos load order, bic r1 for acFlags clear.
