
<!-- merge 2026-10-14 14:25:43 -->
# Bg_Hidan_Dalm: cascade stage 1 (Haiku), batch 1/1

- BgHidanDalm_Update: matched (0/18)
- BgHidanDalm_Destroy: matched (0/17)
- EffectSsKiraKira_SpawnSmallYellow: matched (0/24, link-level too). Moved from functions_380000s.cpp to ef_kirakira_small_yellow.cpp (own TU so it is not inlined into Shrink). Color pair pinned via EQU 0x004D916C in data_syms.s. Only caller is BgHidanDalm_Shrink (shared check: none).
- BgHidanDalm_Init: matched (0/66)
- BgHidanDalm_Wait: matched (0/82)
- BgHidanDalm_Shrink: NOT linkable as C. C matches (0/95 words, with the ctor-initialized `static Vector3f accel` reproducing the guard), but that static lands in .bss and the link fails with L6224E ("could not place z_bg_hidan_dalm.o(.bss)"). Draft under `#if 0`, GLOBAL_ASM kept. Needs a data/oot3d.ld pin for the static (ROM 0x005699C8) to be enabled.
- BgHidanDalm_Draw: matched (0/104, stage 2 Sonnet): static inline N64-order wrapper `MultVec3f(src, dest, mtx)` around VEC3TransformAsm (also 0 with param orders msd/smd).

Notes: header is DynaPolyActor-based (actionFunc 0x1BC, switchFlag 0x1C0, collider 0x1C4, elements 0x1E4, skelAnimModel 0x354). Data symbols via data_syms.s (EQU 0x5116BC / 0x5117B4 / 0x5116C4 / 0x4D916C).
ws_check.sh: baseline only (FUN_00249af8).
