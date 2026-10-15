# Obj_Mure — Opus closing pass (2026-10-13)
- FUN_003bc5dc (N64 ObjMure_CulledState + SpawnActors/0/1 inlined): MATCHED (0/139 words, ws_check baseline only).
  Keys: in SpawnActors0 a `play2` param + `PlayState* play = play2;` declared AFTER maxChildren, passing
  `&play2->actorCtx, play` (keeps play in r1 at entry); in SpawnActors1 `spawnPos = ObjMure_PosV(&actor->world.pos)`
  by-value Vec3f helper (hoists &spawnPos into r8).
- Actor has no GLOBAL_ASM left.
