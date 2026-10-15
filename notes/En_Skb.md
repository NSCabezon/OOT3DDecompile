
<!-- merge 2026-10-15 00:26:38 -->
# En_Skb (G21, haiku stage) — status

ws_check.sh En_Skb: baseline only (FUN_00249af8).

| function | status | note |
|---|---|---|
| FUN_00126304 | MATCHED, moved from functions_120000s.cpp | action: anim done -> FUN_00366318 |
| EnSkb_Draw | MATCHED (C) | `flags` loaded before model ptr (order matters) |
| EnSkb_PostLimbDraw | MATCHED (C) | |
| FUN_003ca54c | MATCHED, moved from functions_3C0000s.cpp | Despawn action |
| FUN_00120460 | MATCHED, moved from functions_120000s.cpp | |
| FUN_001c722c | MATCHED, moved from functions_1C0000s.cpp | Rise action |
| FUN_003d6a44 | MATCHED, moved from functions_3C0000s.cpp | Death/drop action |
| FUN_00157844 | MATCHED, moved from functions_140000s.cpp | Death setup; BodyBreak_Alloc(bodyBreak, 0x1D, play) |
| FUN_0033ff3c | MATCHED, moved from functions_320000s.cpp | = EnSkb_SpawnDebris; Vector3f vel/accel + `PlayState* play2` around EffectSsHahen_Spawn |
| EnSkb_Destroy | NOT matched, #if 0 draft + GLOBAL_ASM | 7 words: parent-pointer register choice in the spawner block (`parent != NULL && parent->update != NULL`, count at parent+0x1AA). ~25 variants tried. |
| FUN_0011c4c8 | NOT matched, lives in functions_100000s (GLOBAL_ASM), #if 0 draft in actor .cpp | ~35 words: if/else-if on curFrame (3 / 6) and the Animation_Change start (curFrame-1.0f) const order. ~12 variants. |
| FUN_00366318 | NOT matched, lives in functions_360000s (GLOBAL_ASM), #if 0 draft in actor .cpp | 16 words, all in walk branch (0x12c+): 0.96f constant CSE with the scale multiply. Uses EQU `EnSkb_gUnk587958` (data_syms.s) for the IS_DAY-like check. |
| EnSkb_Init | NOT matched, #if 0 draft + GLOBAL_ASM | 12 words: damageTable/ActorShape_Init order, mass/health reg, flags/audio/action tail. Uses EQUs in data_syms.s (EnSkb_sInitChain 0x52EC4C, EnSkb_sJntSphInit 0x52EC54, EnSkb_sDamageTable 0x52EC64). |

Layout notes (3DS): actor.parent 0x124, update 0x13C, count-ish u16 0x90, f32 0x6C (speed), skel 0x1A4 (curFrame 0x1E0),
0xDF0 actionState, 0xDF1 flag, 0xDF3 breakFlags, 0xDF4 actionFunc, 0xDFC bodyBreak, 0xE10 collider, 0xE20 u8, colliderElements 0xE30.
Only matched functions are C; drafts sit under #if 0 with their GLOBAL_ASM lines.


## Sonnet stage (G2122)
- MATCHED: EnSkb_Destroy (signature `(EnSkb* self, PlayState* play)` + dead `Actor* actor = &self->actor`), EnSkb_Init (`thisx->colChkInfo.damageTable`), FUN_0011c4c8 (Animation_Change speed was -0.4f, curFrame cast re-read at each compare), FUN_00366318 (speed = scale.y * 160.0f, despawn speed -1.0f, 0.96000004f). data_syms.s fixed (END was before gUnk587958) and pulled in via GLOBAL_ASM.
- NOT matched: EnSkb_Update (281 insns). Draft under #if 0 in z_en_skb.cpp (CheckDamage + SetupDeath/Stunned/TakeDamage inlined). Instruction stream/layout is ROM-identical except: (1) ROM hoists the 0x010002A3 sfx into fp at entry and (2) VFP/GPR numbering (play r7 vs r8, fire loop ptrs, -6.0f/-4.0f in s16/s17 vs s18/s19). ~200 words, all register numbering. Key tricks found: `char unk_DF2` -> `u8` (avoids reload), site 2 of SetupDeath must `goto done` at end of the inlined CheckDamage to get the cross-jumped tail at the second site.
