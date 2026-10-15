
<!-- merge 2026-10-15 16:13:25 -->
# En_Sa (G31) — STATUS (Haiku + Sonnet passes)

ws_check: baseline only (FUN_00249af8), 0 non-function bytes.

| Function | Result | Notes |
|---|---|---|
| EnSa_Destroy (11) | MATCHED | `Collider_DestroyCylinder` linker-inlined stub; `play` declared before `self`. |
| FUN_00185964 (EnSa_GetTextId, moved from functions_180000s.cpp) | MATCHED | |
| FUN_00185884 (EnSa_UpdateTalkState, moved from functions_180000s.cpp) | MATCHED | FULL case list 0,1,3..9 for the `ldrlo pc` table. |
| EnSa_Draw (57) | MATCHED (Sonnet) | Typed header (SkelAnime/FaceAnimations/ColliderCylinder members) + each FaceAnimations call in its own `{ FaceAnimations* fa = &self->faceAnim; ... }` block (En_Md recipe). |
| EnSa_Init (215) | MATCHED (Sonnet) | `(Actor* thisx, PlayState*)`, N64 EnSa_GetType inlined (scene 0x55/0x56/0x29 checks), 6-way switch, `thisx->targetMode = 6`, `play->GetObjectStatus(..)->zarInfo`, `GetQDBByIndex(1)` for the greeting cutscene, `__ARM_common_memcpy2_6` for initRot (struct copy would emit a duplicate helper). cutscene flag/`unk_C49` store order swapped vs first guess. |
| EnSa_Update (242) | MATCHED (Sonnet) | Inlined Blink/UpdateTalking/UpdateTrackingMode; 3 anim-end checks (`curFrame` local before `FUN_003603c0`), `thisx->shape.shadowAlpha` (ldr/sxth shape), `thisx->world.pos.x +=`, `unk_C48` read via `(u8*)self + 0xC00` base, `yawDiff` comma-assign inside the `||` (u16 loads, sxth/add pair), `thisx->shape.rot.y`. |
| FUN_0023bca4 (37, = EnSa_OverrideLimbDraw, functions_200000s.cpp) | UNMATCHED far (24w) | GLOBAL_ASM kept; draft under `#if 0` in z_en_sa.cpp. ROM keeps limb==10 as a real branch with its own `bl FUN_0034e01c` and predicates only limb==9; armcc cross-jumps both calls and predicates both. ~45 variants (else-if, two ifs, switch, aliases, typed self param, thisx casts). |

## Notes
- `z_en_sa.hpp` rewritten with the real layout (skelAnime 0x1A4, faceAnim 0x228, actionFunc 0x3F4, collider 0x3F8, interactInfo 0x450, blink 0x47C, cueId 0x47E, eye idx 0x480/0x482, alpha 0x484, initRot 0x486, joint/morph tables, zar 0xC44, unk_C48/C49). sizeof 0xC4C.
- `data_syms.s` EQUs: EnSa_sFaceRemap, EnSa_sRgbaConst, EnSa_sCylinderInit (0x52E740), EnSa_sColChkInfoInit (0x52E778).
- Shared-file edits: functions_180000s.cpp (removed GLOBAL_ASM FUN_00185884, FUN_00185964) — merge tool must also drop these.
- Callees used but still asm (not in the G31 list): FUN_0035fbb0 (EnSa_ChangeAnim), FUN_003c2094 (Idle), FUN_003c1e30 (HandleCutscene), FUN_0012c8d0 (AwaitTeachingSariasSong).
