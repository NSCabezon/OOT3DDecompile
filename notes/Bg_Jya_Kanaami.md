# Bg_Jya_Kanaami: Opus closing pass (2026-10-13)
All functions matched; ws_check baseline only.
- FUN_003bc4b8 (rise action): MATCHED, moved into actor .cpp (GLOBAL_ASM line removed from functions_3A0000s.cpp). Key: block-scoped `Actor* thisx = &self->dyna.actor;` inside the if, used for rot.x store + Audio call.
- BgJyaKanaami_Draw: MATCHED. Key: `Vec3f scale` with x/y/z = 10.0f assigned separately, then `ScaleCol(&mtx, 0, scale.x)`, (1, scale.y), (2, scale.z) via static inline.
