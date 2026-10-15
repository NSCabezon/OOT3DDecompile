
<!-- merge 2026-10-14 23:22:41 -->
# En_Goroiwa (haiku stage, G19) status

Baseline: ws_check.sh En_Goroiwa -> only FUN_00249af8 differs, 0 non-function bytes.

## Matched (moved into actor .cpp, GLOBAL_ASM removed from functions_*.cpp)
- EnGoroiwa_Destroy (0/10), EnGoroiwa_Draw (0/13)
- FUN_00359420 = SetupRoll (0/12)
- FUN_00143374 = SetupMoveAndFallToGround (0/26)
- FUN_001a3154 = MoveAndFall (0/47); static inline copy used inside MoveAndFallToGround
- FUN_003af238 = MoveUp (0/81). Needs `__attribute__((noinline))` on FUN_00359420 proto, otherwise armlink-style inlining changes the tail

## Split applied
- FUN_00144074 @ 0x001440fc -> FUN_001440fc (Wait action, raw code after literal pool). split/asm/*, functions_140000s.cpp, data/oot3d.ld, data/keep_symbols.txt

## Not matched
- FUN_00316c64 (SetupWait): 10/34 words off. Draft under #if 0. 3.0f/0.5f consts hoisted to prologue; table base reg differs. ~30 variants (stmt order, table ptr, helper, ternary/if-else).
- FUN_003ba7ac (MoveAndFallToGround): 40/87 off. Draft under #if 0. Early-exit pop tail and predicated velocity compare differ; ReverseDirection order variants tried.
- EnGoroiwa_Update: 2/97 off (0x118/0x11c: ldrb flags into r1 vs ROM r0). Draft under #if 0, asm still linked. ~15 variants.
- FUN_0021ee20 (EnGoroiwa_Move): 92/114 off. Draft under #if 0, only 5 variants tried.
- FUN_00317708 (EnGoroiwa_NextWaypoint): 73/95 off. Draft under #if 0, 2 variants (signed params read did nothing).

## Data symbols (actor data_syms.s, EQU into the actor .data chunk)
- EnGoroiwa_sWaitDurations 0x525FA0 (s16[2] {20,6}), EnGoroiwa_sSpeeds 0x525FAC (f32[2]), EnGoroiwa_sYOffsets 0x525FB4 (f32[2])

## Sonnet stage (G19)
- Matched: EnGoroiwa_Init (actor.shadowAlpha via `actor->`; EQUs sInitChain/sJntSphInit/sColChkInfoInit/sInitYOffsets), FUN_003ba7ac (shared MoveAndFall inline: `Vec3f* p=&pos; p->y += vel.y`; ReverseDirection `next = current + dir`; FUN_00316c64 must stay extern asm for the tail call).
- Near: EnGoroiwa_Update 2 words (ldrb r1 vs r0), FUN_00316c64 10 words (3.0f/0.5f hoist + table reg).
- Far: FUN_0021ee20 (90), FUN_00317708 (73). static/big: FUN_001eb56c (guarded static Vec3f).
