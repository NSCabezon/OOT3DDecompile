# Bg_Gnd_Soulmeiro — status (cascade stage 1, Haiku-only)

ws_check.sh: only baseline `FUN_00249af8` differs. Build clean.

## Functions
| Function | Where | Status | Notes |
|---|---|---|---|
| BgGndSoulmeiro_Init | actor .cpp | MATCHED | sInitChain (0x511080) and sCylinderInit (0x511048) referenced as raw addresses (data stays GLOBAL_ASM `data/z_Bg_Gnd_Soulmeiro.data.s`) |
| BgGndSoulmeiro_Destroy | actor .cpp | MATCHED | Collider_DestroyCylinder call compiles to the expected dead-arg form |
| BgGndSoulmeiro_Update | actor .cpp | MATCHED | |
| BgGndSoulmeiro_Draw | actor .cpp | MATCHED | 3DS draw uses SkeletonAnimationModel calls, not N64 DLists |
| FUN_003f5500 | moved from functions_3E0000s.cpp into actor .cpp | MATCHED | N64 func_8087B284 (case 0 action, AC_HIT check) |
| FUN_0010fb78 | moved from functions_100000s.cpp into actor .cpp | MATCHED | N64 func_8087B350 (case 1/2 action); needed Actor* local + ternary store |
| FUN_003f84d4 | still GLOBAL_ASM in functions_3E0000s.cpp | NOT MATCHED | N64 func_8087AF38 (web break countdown, 724 B). Draft under `#if 0` in actor .cpp |

## FUN_003f84d4 attempts
- Attempt 1: full C draft (timer countdown, Rand spiral loop of 6, EffectSsDeadDb_Spawn x16 args). Compiles once a local prototype for EffectSsDeadDb_Spawn is present. Blocked at link: `static Vec3f zeroVec` is zero-initialised, goes to .bss, linker reports `L6224E Could not place z_bg_gnd_soulmeiro.o(.bss)`. The asm instead uses a function-local guard at 0x00511044 and the zero vector at 0x00569950 (guard_acquire / store / guard_release path). Matching needs either an ld rule for that .bss or a symbol for 0x569950 plus the guard code shape.
- Not tried further (budget). Next step: Sonnet/Opus, decide how to express the 0x569950 static (non-zero trick is not allowed; prefer EQU/extern symbol + guard shape).
- Also noted: the asm timer threshold is 30 (0x1E), not the N64 value 20; timer lives at actor+0x1FC; action pointer +0x200; SkeletonAnimationModel* +0x204.

## Layout / struct
- `z_bg_gnd_soulmeiro.hpp` rewritten for 3DS: collider at 0x1A4 (ColliderCylinder 0x58), timer 0x1FC, actionFunc 0x200, skelAnimModel 0x204, size 0x208.
- Local `PARAMS_GET_U` macro (u16 variant, same as other actors) in the .cpp.

## Files touched outside actor dir (ws only)
- ws/Bg_Gnd_Soulmeiro/src/functions/functions_3E0000s.cpp: removed `GLOBAL_ASM("asm/FUN_003f5500.s")`
- ws/Bg_Gnd_Soulmeiro/src/functions/functions_100000s.cpp: removed `GLOBAL_ASM("asm/FUN_0010fb78.s")`
- include/: no changes.
