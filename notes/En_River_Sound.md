
<!-- merge 2026-10-15 09:40:34 -->
# En_River_Sound (G25, haiku stage)

Matched (C, GLOBAL_ASM removed from actor .cpp / functions_*.cpp):
- EnRiverSound_Init (42 insns): needs `(u8)(params - 0xF8)` for FUN_00285f50 and `(u8)(params >> 8)` for pathIndex.
- EnRiverSound_Destroy (8)
- FUN_00214848 (4), FUN_0021485c (5), FUN_00285f34 (6), FUN_00285f50 (19), FUN_0014eef8 (34): moved to actor TU.
  FUN_00214848/FUN_0021485c/FUN_00285f34/FUN_00285f50 live in z_en_river_sound_state.cpp (separate TU: armcc inlined
  FUN_00285f34 into Destroy when they shared a TU).
- FUN_003232a4 (6): SurfaceType conveyor-speed helper, C in actor .cpp.

Shared state: data_syms.s EQUs (no image bytes): EnRiverSound_sState 0x0054AC48 (u80 ptr, f84 dist, u31/u33/u06/u35 bytes,
f80...), EnRiverSound_sGanonVolTable 0x0054AD3D, EnRiverSound_sSfxHandles 0x005AF450, EnRiverSound_sVolFade 0x005B12C8.

Not matched (draft under #if 0, GLOBAL_ASM kept):
- FUN_002549b4 (64 insns): 11 words off. Mapping decoded (pc-relative constants: 64.0, 0.64, 0.1, 1.0, 120.0, 1/280, 0.9, 127.0).
  Remaining diff is the VFP operand/order of the dist compare (ROM vcmpe s0(dist), s1(f84)) and the pan vmla constants.
- FUN_003232bc (46 insns): 37 words off (ROM keeps the line-segment math in s-regs with its own schedule).
- FUN_00404b20 (22): 7 words off (register order: ROM keeps sfxId in r4, ctx in r5).
- FUN_003ff980 (18): 15 words off (blne predication vs branch, and the 1/127 float).

Not attempted (budget):
- EnRiverSound_Draw (78): one transcription tried, did not compile (needs EQUs for the 0x0052E3A0 volume table and 0x0052E344
  sfx-id table and a `self->unk_1B1` field); still GLOBAL_ASM.
- FUN_00323378 (88): large; sqrt distance + Audio_QueueSeqCmd + FUN_00356018 path. Still GLOBAL_ASM.

ws_check.sh En_River_Sound: baseline only (FUN_00249af8).

## Sonnet stage (G25)
Matched: EnRiverSound_Update (GetSfxPos inlined as a plain `static`; prev/next segment positions in a `Vec3f[2]`; pos assigned BEFORE
path; dead h2/sp2/pts2/s2/play2 aliases), EnRiverSound_Draw (`thisx->` everywhere, `f32 w` scoped to the Sarias arm so the other calls
stay tail calls, `EnRiverSound_PlayCentered` inline helper), FUN_003232bc (Vec3f l0/l1/l2 locals), FUN_003ff980 (moved to
z_en_river_sound_state.cpp: separate TU so FUN_00404b20 is not inlined). FUN_0014eef8 and FUN_003232a4 also moved to the state TU
(callers would inline them otherwise). New EQUs in data_syms.s: EnRiverSound_sSoundEffects 0x52E344, EnRiverSound_sSfxFreqs 0x52E3A0.
Not matched (drafts under #if 0, GLOBAL_ASM kept): FUN_00404b20 (3 words: ROM schedules the ctx+0x180 load into r2 before mov r1,#0x1b;
dead `sfxId2` alias fixes r4/r5), FUN_002549b4 (9 words: r0/r1 numbering of the first unk_80 load + constant pool order),
FUN_00323378 (far: ROM keeps 0 in r7 and the BGM_SUB id 3 in r8, VFP numbering of the xz distance reversed).
