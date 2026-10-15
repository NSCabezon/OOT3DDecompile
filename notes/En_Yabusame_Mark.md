# En_Yabusame_Mark status (Opus closing pass)

| Function | Status |
|---|---|
| EnYabusameMark_Destroy | MATCHED (earlier stage) |
| EnYabusameMark_Init | MATCHED: `(EnYabusameMark* self, ...)` signature, all accesses via `self->actor.`, params stored as `*(u16*)&self->typeIndex` (forces ldrh/strh + ldrsh reload) |
| EnYabusameMark_Update | MATCHED: `(Actor* thisx, ...)`, `self->actor.world.pos` reads, index table directly `sYabusameCollisionVertices[arrayIndex + n]` (no vertexArray pointer local) |
| FUN_0020761c (action) | NOT matched, 2/136 words: asm kept in functions_200000s.cpp, draft in #if 0. Size now matches with `Vector3f effectAccel(0.0f,0.0f,0.0f)` ctor + EffectSsExtra_Spawn `s16 scale, s16 type`. Remaining: ROM stores effectVelocity.x/.y from s1/s2 (reused from accel ctor regs), ours from s0. |
