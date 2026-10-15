
<!-- merge 2026-10-14 12:25:19 -->
# En_A_Obj STATUS (stage 1, Haiku, batch 1/1)

Scope: FUN_003a5768, FUN_003e2548, EnAObj_Destroy, FUN_00393d44, EnAObj_Draw, EnAObj_Update.

| Function | Result | Notes |
|---|---|---|
| FUN_003a5768 | matched | `self->actionFunc = FUN_00393d44`. `__attribute__((noinline))` on prototype keeps the tail call (armcc inlined it otherwise). |
| FUN_003e2548 | matched | Tail call to FUN_003a5768 with `params` as 2nd arg. |
| EnAObj_Destroy | matched | `Collider_DestroyCylinder` is linker-inlined to `mov r0,#1` as in ROM. |
| FUN_00393d44 | matched | Action function (talk request). Uses `actor.textId`, `yawTowardsPlayer`, `shape.rot.y`. |
| EnAObj_Draw | matched | Needs `thisx` alias for the null check so the model load goes to r1 (ROM shape). Color constant copied from `EnAObj_sDrawColor` (data_syms.s, EQU 0x004D920C). |
| EnAObj_Update | matched | Gravity check uses `actor->gravity`; 0.0f is also the ceilingCheckHeight arg (s2 reused from compare). |

EnAObj_Init (stage 2, Sonnet): not matched, 10 words off (structural) — draft under #if 0, GLOBAL_ASM kept. Cause: ROM hoists the action-func literal into r0 early in cases 3/4 and 6 (mine loads into r1 late; store order bgId/action swapped in case 6); BlockRot action 0x00393c34 is an unlabeled tail inside caseD_3_00393ae4 (needs cfg split, raw address in draft). Rest (switches, jump tables, model/colIdx arrays, DynaPoly) matches.

Unresolved callees (declared locally, not in include/): FUN_00369a48, FUN_00363cb8, FUN_003687a8, FUN_003589cc, FUN_00358964.

Files touched: src/game/actors/En_A_Obj/z_en_a_obj.cpp, z_en_a_obj.hpp (EnAObj fields), data_syms.s (new); src/functions/functions_3A0000s.cpp, functions_3E0000s.cpp, functions_380000s.cpp (GLOBAL_ASM lines removed).

EnAObj_Init (stage 3, Opus): MATCHED (0 words), GLOBAL_ASM removed. Fixes: (1) the raw `(ActorFunc)0x00393c34` cast caused the case 3/4 action-ptr reg/schedule diff — replaced by EQU symbol `EnAObj_BlockRot EQU 0x00393C34` in data_syms.s (still debt: unlabeled tail inside caseD_3_00393ae4, needs cfg split for a real symbol); (2) case 6: `self->actor.flags |= 1;` (not `thisx->flags`), plain order unk_208, flags, gravity, SetupAction, `bgId = 5` (no `id` local). Prototype now `EnAObj_Init(Actor*, PlayState*)`. ws_check baseline. All 7 functions matched.
