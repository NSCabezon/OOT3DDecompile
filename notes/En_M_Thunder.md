
<!-- merge 2026-10-15 17:46:51 -->
# En_M_Thunder (group G37, Sonnet pass) - status

| Function | Result | Notes |
|---|---|---|
| EnMThunder_Destroy | MATCHED (Haiku) | VFE virtual call; `_ZTI15EnMThunderFreer` now lives in src/game/shared_syms.s (VFE block, 0x7FFF0060) |
| EnMThunder_Update | MATCHED (Haiku) | |
| FUN_0010fa78 (EmptySpinAttack) | MATCHED (Haiku) | moved into the actor .cpp |
| FUN_00128c20 (SpinAttacking) | MATCHED, no volatile | `unk_244` is a `u16` field (ROM `ldrh`); armcc then reloads it after the `strh`, no volatile needed |
| FUN_00314988 (sword-charge SFX) | MATCHED | own TU `z_en_m_thunder_sfx.cpp` (same-TU def gets inlined into FUN_003f4d9c). Recipe: `u8 prev = st[5]; if (lvl != prev)`, `f32 vol = tbl[lvl]; u32 sfxId = ...` locals. State = `EnRiverSound_sState` (0x0054AC48, EQU in En_River_Sound/data_syms.s), float arg `FLOAT_0054acb0` EQU added to shared_syms.s. Raw offsets on the state (debt) |
| FUN_003f4d9c (ChargingSpinAttack) | MATCHED (0/302) | moved from functions_3E0000s.cpp. Recipes: `static inline EnMThunder_SetupAction(self, fn)` for the actionFunc store (fixes hoisted-const r2/r3 numbering), `if (swordType != 1) {4} else {2}` single-line arms, `s32 alpha` local before the chargeAlpha store, `f32 charge` local read once for the 3-level SFX chain. EmptySpinAttack is inlined from the same-TU FUN_0010fa78 |
| EnMThunder_Init | NOT MATCHED, 7 words (near) | draft under #if 0 (ROM size equal). Diff: r0/r1/r2 numbering at the `stateFlags2 &= ~0x20000` + `dmgFlags = tbl[swordType]` block (ROM keeps r0 busy: `ldr r1,[sl,#0x714]`, table in r2). ~45 single-site variants tried (dead aliases, locals, SetupAction, cond rewrites). Needs new data syms (data_syms.s: sCylinderInit, sDmgTable, sSfxIds, sSpinChargeScale) |
| EnMThunder_Draw | NOT MATCHED, far (~160 words) | draft under #if 0. Prologue allocation differs (ROM: self=r4, state=r5, player=r6, const 1=r7 and player via `ldr r0,=0x20ac`; ours state=r4, self=r5, `add r1,r1,#0x2000`); `Vector3f vec(x,y,z)` ctor temps fixed the stack frame |

Files outside the actor dir: `src/functions/functions_310000s.cpp` (FUN_00314988 GLOBAL_ASM removed), `functions_3E0000s.cpp` (FUN_003f4d9c removed), earlier `functions_100000s.cpp`/`functions_120000s.cpp`; `src/game/shared_syms.s` (+`_ZTI15EnMThunderFreer`, +`FLOAT_0054acb0`, both inserted before END). New files: `data_syms.s`, `z_en_m_thunder_sfx.cpp` (syms.s removed). Header: fields typed (swordType @0x233, attackStrength @0x232, spinChargePercent @0x224, unk_248/24C/250, unk_244 u16).
ws_check.sh: baseline only (FUN_00249af8).
