# Night run 2026-10-12 → 2026-10-13 08:00

Branch `decomp-night` in `oot3d/` (local commits only). Cascade Haiku → Sonnet → Opus, 4 actors in parallel (user cap), queue `queue.txt`.
Start: 24 actors merged, 0.95 % .text in C (316 functions).

## Hourly reports

## Orchestrator procedure (for me, survives context compaction)
- **HAIKU ONLY, adaptive concurrency (user 00:47):** `scripts/capacity.sh add|refill`. Refill on completion unless load1>30 or thermal warning (shrinks). Add +1 extra only if load1<12, load5<15, no thermal warning, ≥5 min since last launch; max 14. Background adder loop (`scripts/adder.sh`) exits with POP <actor> → launch it, re-arm. `night_merge.sh <A> "<UNMATCHED>"` records leftovers in `pending_sonnet.tsv`.
- On agent done: parse `UNMATCHED:` line.
  - none → `python3 scripts/merge_ws.py <A>` → `scripts/rebuild_check.sh` (must show baseline only; if not, revert actor files via `git checkout -- src/game/actors/<A> src/functions` in oot3d and mark failed) → `rm -rf ws/<A>` → state merged → pop next from `queue.txt`, launch Haiku.
  - some, stage haiku → launch Sonnet (`model: sonnet`), prompt "AGENT_BRIEF … cascade stage 2, actor X".
  - some, stage sonnet → launch Opus (`model: opus`), stage 3.
  - after Opus → merge whatever matches.
- Every 10 merges: commit in oot3d (branch decomp-night, never push).
- Progress on demand: `scripts/pct.sh` (no timers, no scheduled reports).
- Stop: `touch .stop` (adder/merge stop popping); finish in-flight, final commit + summary.
- Pending Opus fixes in main tree: Actor1DA_Init, FUN_0015b3cc (Bg_Mjin), FUN_003e68c4 (Bg_Bom_Guard, also cfg-merged fn), FUN_003bc5dc (Obj_Mure).
- 00:13 — 1.182 % .text en C · 398 funciones (3.308 %) · 37 actores (13 esta noche) · cola 374

## 06:00 strategy switch (user, 00:48)
- 06:00: stop popping queue.txt (kill adder). Launch **Opus** on `pending_sonnet.tsv` actors (fresh `mkws.sh <A>` from main; prompt: stage 3, target only listed functions, drafts in actor .cpp #if 0 / NON_MATCHING + `notes/<A>.md`). Most-pending first. Same governor.
- Haiku actors still running at 06:00: full cascade on finish (Sonnet → Opus), merge after.
- Opus pending fixes: also the old ones (Actor1DA_Init, Bg_Mjin FUN_0015b3cc, Bg_Bom_Guard FUN_003e68c4, Obj_Mure FUN_003bc5dc, Bg_Haka_Huta, En_Okarina_Tag leftovers...).
- 07:35: no new launches. 08:00: merge what matched, final commit, summary in NIGHT.md + chat.
- 01:13 — 1.428 % .text en C · 474 funciones (3.94 %) · 50 actores (26 esta noche) · 8 actores con pendientes · cola 361
- 02:13 — 1.73 % .text en C · 585 funciones (4.862 %) · 74 actores (50 esta noche) · 26 actores con pendientes · cola 337
- 03:13 — 2.041 % .text en C · 702 funciones (5.835 %) · 106 actores (82 esta noche) · 56 actores con pendientes · cola 304
- 06:00 Opus phase started. Queue `opus_queue.txt` (from `opus_targets.tsv`, closest misses first). On Opus done: `scripts/night_merge.sh <A>` (.no_pop set, no queue pops) then launch next from opus_queue.txt if before 07:35 and `capacity.sh refill` = ALLOW. Prompt: "AGENT_BRIEF Opus closing pass, actor X, targets = row of opus_targets.tsv".
- 03:26–05:16 subagents hit weekly rate limit (reset 05:00); session resumed 05:16; interrupted ws salvaged (Bg_Haka_Sgami merged), rest requeued.
- 07:00 — 2.756 % .text en C · 864 funciones (7.181 %) · 133 actores · 146 integraciones esta noche

## Final (07:30)
- **2.928 % of .text in C** (116,292 B), 890 functions (7.40 %). Start of night (23:00): 0.95 %, 316 functions.
- 133 actors with merged work; 63 actors still have leftovers (`pending_sonnet.tsv`, notes in `notes/`).
- Branch `decomp-night`, 22 local commits, final `6ffd13e`. Full clean rebuild verified: only baseline FUN_00249af8 differs.
- Phases: Haiku 23:10–03:26 (8→12→4→adaptive), rate-limit pause 03:26–05:16, Haiku 05:16–05:48, Opus closing pass 06:00–07:30 (~45 actors, ~20 completed).
- Incidents: revert used git HEAD and wiped uncommitted merges (fixed: snapshot restore); merge copy preserved mtimes → stale objects (fixed: shutil.copy + full touch rebuild).
- Remaining blockers (see CLAUDE.md): functions.tsv cfg splits, data-dump splits / linker rules, shared static model loader, GetCMABByIndex register pattern.

# Day run 2026-10-13 (from 08:50)
- User: "Sigue, modo cascada". Haiku → Sonnet → Opus per actor on same ws, then night_merge.sh. Same governor (capacity.sh). 08:00 gate replaced by `.stop` flag file. Start 2.928 %.
- NOTE: `.tree.lock` is a DIRECTORY taken by merge_ws.py/mkws.sh — never `touch` it from outside (deadlocked merge 08:53–09:04). night_merge.sh needs no outer lock.
- 10:20 — 3.276 % .text en C · 975 funciones (8.10 %) · loader compartido resuelto + cfg_split operativo
- ~10:45 pause (user). 3.693 % .text en C · 1062 funciones (8.83 %). Day run 08:50–10:45: +0.77 pts, +172 funciones.
  Infra: shared ModelManager loader solved (notes/LOADER_RECIPE.md), scripts/cfg_split.py (notes/CFG_SPLIT.md), GetCMAB r2-shape rule, ~12 new tricks in CLAUDE.md.
  Open: En_Jsjutan ws kept (merge reverted: 2 non-function bytes differ in main tree, ws check was clean → investigate); Demo_Sa Sonnet still running at pause.
- Paused, all closed: 3.728 % · 1075 funciones (8.93 %). Last commit dee8662. .stop flag set (rm .stop to resume).
