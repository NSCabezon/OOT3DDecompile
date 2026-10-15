
<!-- merge 2026-10-14 23:53:23 -->
# Arms_Hook (G21, haiku stage) — status

ws_check.sh Arms_Hook: baseline only (FUN_00249af8).

| function | status | note |
|---|---|---|
| ArmsHook_Destroy | MATCHED (C in z_arms_hook.cpp) | |
| FUN_0010cf2c | MATCHED, moved from functions_100000s.cpp into actor .cpp | Wait action; GLOBAL_ASM line removed in ws functions_100000s.cpp |
| ArmsHook_Init | MATCHED (C) | needs `ArmsHook_sQuadInit` EQU in data_syms.s (new file) |
| ArmsHook_Update | NOT matched, asm + #if 0 draft | 2 guarded function-local static Vector3f {0,0.5,0} (guards at 0x51090C/0x510910 inside z_Arms_Hook.data, objects 0x5698A8/0x5698B4). Needs pin_static recipe (guard/bss pins). Code shape otherwise matches; 13 words differ (VFP numbering of the Vector3f init + guard order). |

Infra touched: new `src/game/actors/Arms_Hook/data_syms.s` (EQU 0x0051092C).
