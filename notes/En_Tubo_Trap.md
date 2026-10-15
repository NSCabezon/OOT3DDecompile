
<!-- merge 2026-10-15 16:59:17 -->
# En_Tubo_Trap (G34, Haiku first pass) — status

Baseline: `scripts/ws_check.sh En_Tubo_Trap` -> only FUN_00249af8 differs (OK).

| Function | Status | Notes |
|---|---|---|
| EnTuboTrap_Init (29) | MATCHED | `thisx->` for Actor-level calls (variant) |
| EnTuboTrap_Destroy (10) | MATCHED | Collider_DestroyCylinder stub inlined by armlink (fastchk shows bl vs mov only) |
| EnTuboTrap_Update (31) | MATCHED | Actor_MoveForward/UpdateBgCheckInfo/SetFocus/Collider_UpdateCylinder on `thisx` |
| EnTuboTrap_Draw (19) | MATCHED | 3DS draw = model (MTX34CopyAsm + FUN_003721e0 + FUN_00372170); no Gfx DL |
| EnTuboTrap_WaitForProximity (14, 0x11da78) | MATCHED | reads s16 at +0x1A8 (union with targetY); label looks wrong, shape matches |
| EnTuboTrap_Levitate (26) | MATCHED | fabs via `__fabsf` inline wrapper (plain ternary fails) |
| EnTuboTrap_WaitForProximity_003e6f88 (61) | MATCHED | 3DS extra early return: sceneNum==6 && room==0xF && yDiff>450 |
| EnTuboTrap_SpawnFragments (107) | MATCHED (Sonnet) | `PlayState* play2 = play;` at function scope, used for BOTH EffectSsKakera_Spawn and FUN_0037378c (flips the sin/cos VFP numbering; ~100 decl-order/operand variants did nothing). |
| EnTuboTrap_Fly (255) | MATCHED (Sonnet) | Inlines N64 HandleImpact + SpawnEffectsInWater + DropCollectible as static helpers. DropCollectible must re-read `self->actor.params` at each use (no `params` local). 3DS bgCheck mask 0x19 for wall/ground; only ONE sfx in the bounced/land paths (0x010001DE). `EffectSsGSplash_Spawn` declared locally (6 args). |

Data: `src/game/actors/En_Tubo_Trap/data_syms.s` (new): `EnTuboTrap_sCylinderInit EQU 0x0052FBD0` (ColliderCylinderInit in the data chunk, extern from C). Needs `git add -f` (`*.s` is ignored).
Header: actionFunc 0x1A4, targetY/spinSpeed union 0x1A8, originPos 0x1AC, collider 0x1B8, skelAnimModel 0x210 (size 0x214).
