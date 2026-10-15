
<!-- merge 2026-10-15 19:21:33 -->
# Obj_Bean (G42 Haiku pass) status

Baseline: ws_check.sh = only FUN_00249af8, 0 non-function bytes (2026-10-15).

| Function | Status | Notes |
|---|---|---|
| ObjBean_Destroy | MATCHED (fastchk 0/34) | D_80B90E30 = EQU in src/game/actors/Obj_Bean/data_syms.s (0x534DC0) |
| FUN_001a23f4 | MATCHED 0/9 | moved to src/game/actors/Obj_Bean/z_obj_bean_setup.cpp (separate TU: otherwise armcc inlines it into FUN_0036ac40, ROM keeps bleq) |
| FUN_001100a0 | MATCHED 0/30 | Camera_ChangeSetting ternary `(sceneNum != 0x5B) ? 0x2C : 0x2D` (ROM movne/moveq order) |
| FUN_0036ac40 | MATCHED 0/9 | |
| FUN_001eb198 | MATCHED 0/43 | horse-trample check inline, timer 150/45 (3DS values) |
| FUN_00239e24 | MATCHED 0/102 | late store of action pointer `ObjBeanActionFunc setup = FUN_001100a0;` ... `self->actionFunc = setup;` |
| FUN_00143684 | MATCHED 0/16 | NEW split: cfg tail of ObjLightswitch_Disappear (0x143684, 64 B) = Obj_Bean func_80B8FE3C. Split applied in ws (cfg_split.py), GLOBAL_ASM removed from Obj_Lightswitch ws cpp |
| FUN_0015e154 | NOT MATCHED (near, 6 words) | Sonnet: NEW cfg split (see below). Draft under #if 0. ROM emits `mov r0,#0x228` (timer address) after the draw-mode RMW so r0/r1 alternate; we hoist it above the `str actionFunc`. ~40 variants (ptr-early local, all 6 stmt orders x 2, inline helper with Actor*/ObjBean* param, static helper, greedy s2 alias) |
| FUN_00289334 | MATCHED 0/51 (Sonnet) | moved to z_obj_bean.cpp. Fixes: Actor_SetScale(0.0f) (was 0.1f), second path access as block-scoped `Path* path = &play->setupPathList[idx]; ...path->points` |
| FUN_0036ac64 | MATCHED 0/100 (Sonnet, not in the Sonnet list) | moved to z_obj_bean.cpp. Key: NO temp_f20 locals; direct left-to-right call expressions (`Math_SinS(z*5)*0.06f + Math_SinS(y*8)*0.01f + 1.07f`, `1.0f + Math_CosS(..)*0.2f`, `(f32)home.rot.y + Sin(x*3)*1000 + Sin((s16)(z*2))*2100`), `f32 k` kept |

Sonnet pass (G42):
| ObjBean_Update | NOT MATCHED (near, 2 words) | draft under #if 0 (ObjBean_Break inlined). Remaining: ROM `and r1,r5,#1` (dlist index in r1) vs ours r0, 5 words earlier cascade fixed by: thisx for Move/shadowDraw/SetFocus, `s32 forty = 40` local at fn top (gets 0x28 into sb), `void* dl = (void*)sBreakDlists[i&1]` local before EffectSsKakera_Spawn, `if (rnd<0.1f) arg5=0x60 else 0x40; gravity=-80` order. ~60 variants + greedy alias search |
| ObjBean_Init | NOT MATCHED (84 words, structurally close) | draft under #if 0 with N64 helpers. Remaining: ROM hoists `ldrh params; and #0x3f; mov r0,play` above the age branch (both Flags_GetSwitch calls), 2 param-copy movs (`mov r5,r6` for play in DynaPoly, `mov r5,r4` for the collider this), action ptr in r1 (we get r0), ActorShape_Init pool order. Needed: no `play` local (raw `(PlayState*)state` everywhere), `thisx->unk_19A = 1`, `Collider_UpdateCylinder(&self->dyna.actor, &((ObjBean*)thisx)->collider)` (this one thisx use fixes the size and the path reload order). ~50 variants |
| ObjBean_Draw | NOT MATCHED (far, 123 words) | draft under #if 0. VFP numbering of the translate matrix fixed (ObjBeanVec operator[] helper, x,y,z -> s2,s0,s1) and Matrix_RotateY/scale-column helper OK; remaining: armcc hoists the identity 0 / 1.0f constants into r6/r7 (ROM keeps r4=self, r5=param copy `mov r5,r4`, r6=1 for SetUnkAC and rematerialises 0/1.0f per block) and stack layout (Vec3f at sp+4, mtx at sp+0x10). ~25 variants |

Split applied in this ws (Sonnet): FUN_0015e154 0x0015e1dc FUN_0015e1dc (head 136 B stays asm; tail 112 B = unlabeled cfg tail, asm).
Data: data_syms.s now also exports sObjBeanBreakDlists (0x534DC4), sObjBeanCylinderInit (0x534DCC), sObjBeanSpeeds (0x534E04), sObjBeanInitChain (0x534E24) as EQUs (unique names; only the drafts use them).
Header: models unk_218/21C/220/224 are now `SkeletonAnimationModel*`.

Debt / notes:
- z_obj_bean.hpp is now typed (3DS offsets: N64 +0x58 up to collider, +0x74 from timer on; collider 0x1C0..0x218; models 0x218..0x227; stateFlags 0x26B). Verified against ROM offsets.
- FUN_001436c4 (action target of the split tail) is referenced by pointer only.
- data_syms.s is .s under src/ -> must be committed with git add -f.
