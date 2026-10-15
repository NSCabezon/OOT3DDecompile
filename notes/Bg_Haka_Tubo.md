
<!-- merge 2026-10-15 17:43:48 -->
# Bg_Haka_Tubo (G39, Haiku + Sonnet)

MATCHED (C, 0 words): BgHakaTubo_Update, Destroy, Init, Draw, DropCollectible.
- Init: Object_GetIndex bank lookup inline (`BgHakaTubo_GetObjStatus`), `actor->` (the raw param) on the
  ProcessInitChain/FUN_00372f38/FUN_0036a924/SetBgActor/unk_19B accesses gives the r2-shaped GetCMABByIndex call.
- Draw: MTX34_MakeTrans via a `(m, x, y, z)` helper that fills a Vec3f then calls the shared helper (param order
  x,y,z; the Vector3f ctor / other orders gave 4+ words), Y rotate + 9 scale muls inline, Vec3f pos in the
  outgoing-arg slot (declared in a block).
- DropCollectible: 0.8f branch order 0xF (<0.8) / 8 (>=0.8).
- Data: actor-dir `data_syms.s` (EQUs at 0x5114C8 sData struct {sPotsDestroyed, sInitChain, zero-vec guard,
  burst floats}, 0x5114E0/0x511518 collider inits, 0x4D70E4 draw color rodata, 0x569998 zero vec in .bss).
  GLOBAL_ASM("data/z_Bg_Haka_Tubo.data.s") stays.

UNMATCHED:
- BgHakaTubo_Idle (near, 4 words): everything matches except that ROM emits `mov r3,#0xaf` before the three
  vldr of the EffectSsHahen_SpawnBurst floats (armcc schedules the vldrs first). Needs a guarded
  function-local `static Vec3f` (hand-written guard via EQU, like Bg_Spot02_Objects FUN_0019bb28; zero-vec built
  with placement-new `Vector3f(0,0,0)` which gives the exact ROM vmov/vstr shape). ~30 variants. Draft #if 0.
- EffectSsHahen_SpawnBurst_003a9460 (functions_3A0000s.cpp, 93 insns, near 1 insn): see comment above the draft.
  GLOBAL_ASM stays in functions_3A0000s.cpp.
- Cleanup note: `operator new` placement helper and the extern decls for Idle's static are only used by the
  disabled draft.
- ws_check.sh: baseline only (FUN_00249af8).
