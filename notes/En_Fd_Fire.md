
<!-- merge 2026-10-14 12:34:22 -->
# En_Fd_Fire STATUS (cascade stage 1, Haiku, batch 1/1)

ws_check.sh En_Fd_Fire: baseline only (FUN_00249af8).

| Function | Result | Notes |
|---|---|---|
| EnFdFire_Destroy | MATCHED (C, actor cpp) | 0/9 words off |
| FUN_003abdcc | MATCHED (C, moved to actor cpp) | 0/13 words off; GLOBAL_ASM removed from functions_3A0000s.cpp |
| FUN_003abfb8 | MATCHED (C, moved to actor cpp) | 0/42 words off; GLOBAL_ASM removed from functions_3A0000s.cpp |
| FUN_003ace80 | MATCHED (C, moved to actor cpp) | 0/100 words off; GLOBAL_ASM removed from functions_3A0000s.cpp |
| EnFdFire_Init | MATCHED (C) stage 2 | 0/75 words. Fix: `thisx->flags &= ~0x1;` (clear through the entry `thisx` param, not `self->actor.flags`). |
| EnFdFire_Update | MATCHED (C) stage 3 (Opus) | 0/57. Fix: in the inlined CheckCollider, test via `self->` but clear via a second alias `EnFdFire* s2 = self;` (`s2->collider.base.acFlags &= ~AC_HIT`) -> fresh bic dest r1; then `(Actor* thisx, PlayState* play2)` + `PlayState* play = play2;` fixes the r5/r6 play/const swap. |
| FUN_003ac4c4 | MATCHED (C, moved to actor cpp) stage 3 (Opus) | 0/95; GLOBAL_ASM removed from functions_3A0000s.cpp. Fixes: diffs declared first and assigned in separate statements; clamp as `if (vy_field >= min) return; vy_field = min;` (vstrlt); caller `if (!(flags & 1) || velocity.y > 0.0f) return;` (bgt); velocity copy via `Vec3f* vel = &self->actor.velocity; *vel = *(Vec3f*)&velocity;` (fixes zero vmov order). |
| EnFdFire_Draw | NOT MATCHED (structural) | SetUnkAC `strb r5,[r0,#0xac]` + inline MTX34 rotations (d8-d11 frame 0x3c); see SetUnkAC recipe in CLAUDE.md. |

Key 3DS facts found:
- EnFdFire layout: actionFunc 0x1A4, ColliderCylinder 0x1A8 (0x58), spawnRadius 0x200, scale 0x204, deathTimer s16 0x20A, tile2Y s16 0x20C, model object 0x210 (12 B; ctor FUN_0034f94c, dtor FUN_0035046c). sizeof 0x21C.
- Actor velocity 0x60, speedXZ 0x6C, gravity 0x70, minVelocityY 0x74, bgCheckFlags 0x90, rot.y 0x36.
- Data symbols via data_syms.s (EQU): sCylinderInit 0x00523540, sColChkInit 0x00523578, sDamageTable 0x00523582 (armcc derives it as `add r1,r2,#0xa` from sColChkInit, reproduced with a pointer offset), sAngles 0x004D9584 (rodata, copied as a struct).
- Action ids: FUN_003abfb8 = Disappear, FUN_003ac4c4 = wait-for-ground (N64 func_80A0E70C), FUN_003ace80 = dance-towards-player (params bit 15 selects it; deathTimer 300), FUN_003abdcc = wait-to-die (deathTimer 450). The 3DS timers differ from N64 (N64: 200 dance / 300 wait).
- `this` is a C++ keyword in this build: action params are named `self`.
- Helpers not in include/: `_fabsf` (extern __pure), `sinf`/`cosf` declared locally, Actor flag/bgcheck values written as literals (0x1, 0x0001, 0x1|0x4).
