
<!-- merge 2026-10-14 19:13:38 -->
# En_Niw_Girl (G9, haiku stage)

- EnNiwGirl_Destroy: MATCHED (0/11). Girl struct: skelAnime @0x1A4, skelAnimModel @0x954, FaceAnimations @0x958.
- EnNiwGirl_OverrideLimbDraw: MATCHED (0/13). Limb 9 -> &unk_8AC, limb 8 -> &unk_8B2 (FUN_0034df48).
- FUN_001584a8 (N64 Jump): MATCHED (0/24). Moved from src/functions/functions_140000s.cpp into the actor cpp.
- EnNiwGirl_Draw: NOT matched (30/39 words). Draft under `#if 0`, asm kept. ROM preloads the 0.2f constant
  into s2 before the push and copies it with vmov (ours loads it after the push); eyeIndex base reg differs.
  ~16 variants tried (const init forms, eye/fa load order, dead aliases).
- EnNiwGirl_Talk: MATCHED (0/67).
- FUN_003e6778 (N64 talk state): MATCHED (0/66). Moved from functions_3E0000s.cpp.
- FUN_003ca608 (N64 chase state): MATCHED (0/106). Moved from functions_3C0000s.cpp. Key: distance in a
  local `f32 dist` with `dist < 70.0f` / `dist > 150.0f` (not repeated sqrtf) and no `Actor* chased` local.

Header: z_en_niw_girl.hpp extended (skelAnime, actionFunc @0x8A8, unk_8AC/8B2, eyeIndex @0x8BE, path @0x8C2,
unk_27A @0x8C6, unk_27C @0x8C8, chasedEnNiw @0x8D0, skelAnimModel @0x954, faceAnims @0x958). Size unchanged 0xB28.
Remaining asm in this actor (not in this batch): Init, Update, Draw (draft), FUN_003d0830 is not ours.

## Sonnet stage (G9)
- EnNiwGirl_Draw: MATCHED (0/39). Vector3f ctor for the 0.2f vec + `{ FaceAnimations* fa = (FaceAnimations*)((EnNiwGirl*)thisx)->faceAnims; fa->FUN_0035e3a4(0, self->eyeIndex); }` block, second call re-casts from `self`.
- EnNiwGirl_Update: MATCHED (0/153). Header gained collider @0x8D4, interactInfo @0x92C, unkUpTimer/blinkTimer/unk_280/unk_B24. Torso copy must be the explicit `__ARM_common_memcpy2_6` call (struct copy emits a duplicate symbol). Key: dead `EnNiwGirl* s2 = self;` used only on the `blinkTimer = (s16)Rand...` store (greedy single-site search).
- EnNiwGirl_Init: NOT matched (static): inlined `__cxa_guard_acquire` of a function-local static identity MTX34 (guard 0x0055A210, obj 0x005BE29C, same as EnHeishi2_Init/End_Title). Needs LOADER_RECIPE (ld pin + data chunk split), orchestrator only. No draft.
