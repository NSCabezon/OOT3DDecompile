# Solo runbook — one session, one actor at a time, NO subagents

Launch: open a session in `decomp-spike/`, pick the model (`/model`), say e.g.
**"Sigue RUNBOOK_SOLO.md, modo barrido"** (or "modo subida" / "modo grandes").

**This session IS the executor.** Do the work yourself with Bash/Read/Edit. Do NOT use the Agent,
Workflow or Artifact tools, even if a global CLAUDE.md says to delegate. No git commit/push
(night_merge.sh commits locally every 10 merges; never push).

Root `D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike`. Python: always `.venv/bin/python -P` or
`python3 -P` (`scripts/dis.py` shadows the stdlib without `-P`).

## Read once at start (short)
1. `AGENT_BRIEF.md` sections Tools / References / Rules (ignore Setup's "other agents" and Cascade stages).
2. `/Users/nscabezon/Apps/OOT3DDecompile/.claude/skills/oot3d-cascade/references/cheatsheet.md` — apply it BEFORE trying random variants.
3. `CLAUDE.md` (decomp) only via `grep -n "<keyword>" CLAUDE.md` when stuck; do not read it whole.

## Stop rules
- File `.solo_stop` exists → finish the current actor, then stop.
- Free disk < 10 GB (`df -h .`) → stop.
- After 5 actors in one session, or if the conversation is getting long: stop and tell the user
  "contexto lleno, /clear y relanza". Everything resumes from files (below).
- Never leave the main tree broken: only `night_merge.sh` writes to `oot3d/`.
- `.stop` must stay present (it stops night_merge from auto-popping the queue). Never delete it.

## Mode "barrido" (cheap model, e.g. Haiku) — loop over queue.txt
Per actor:
1. **Resume or pick.** If `night_state.tsv` has a line `<A>\tsolo\trunning` and `ws/<A>` exists → continue it.
   Else: `A=$(head -1 queue.txt)`; remove it from queue.txt (`sed -i '' '1d' queue.txt`);
   `printf '%s\tsolo\trunning\n' $A >> night_state.tsv`; `scripts/mkws.sh $A` (~90 s). Note start time `date '+%F %T'`.
2. **Plan.** `.venv/bin/python -P scripts/plan_batches.py $A` → functions with insn counts.
   - ≤120 insns: attempt them, smallest first.
   - >120 insns: do NOT attempt; they go to leftovers as `big`.
3. **Each function** (≤6 serious variants, ~5 min max):
   - asm: `ws/$A/disassembly/asm/<F>.s`; N64: `tools/repos/oot/src/overlays/actors/ovl_<A>/`.
   - write C in place of `GLOBAL_ASM("asm/<F>.s")`; check with
     `.venv/bin/python -P scripts/fastchk.py $A src/game/actors/$A/<file>.cpp <F>` (~1 s; prints differing words).
   - FUN_ in `src/functions/functions_*.cpp` that belong only to this actor: move into the actor .cpp
     with the exact name, delete its GLOBAL_ASM line.
   - fail → keep `GLOBAL_ASM`, best draft under `#if 0 … #endif`, remember its word count.
   - after every 2–3 matches: `scripts/ws_check.sh $A` must show only `FUN_00249af8`.
4. **Finish.** `scripts/ws_check.sh $A` at baseline; `grep -rn pragma ws/$A/src/game/actors/` must be empty.
   Write a 5-line `ws/$A/STATUS.md` (matched / left + why).
5. **Merge.** `scripts/night_merge.sh $A "<leftovers>"` where each item is `Func:words:tag`
   (words = differing words of best draft, `?` if none; tag: `near` ≤4, `far`, `big` not attempted,
   `cfg` needs cfg split, `static` guarded function-local static, + short cause). Example:
   `scripts/night_merge.sh En_Foo "EnFoo_Draw:2:near y/z order,EnFoo_Init:?:big,FUN_00123456:30:far"`.
   Use `""` if all matched. Must print `MERGED`. If `REVERTED`: read `build_fail_$A.log`, fix in ws, retry once;
   else leave it and mark the line `failed` in night_state.tsv.
6. **Log.** `printf "$A\tsolo-<model>\tall\t<start>\t<end>\t<n_attempted>\t<n_matched>\t-\t-\n" >> timing.tsv`.
   New general idiom found? Add ONE line to the cheatsheet table (not to CLAUDE.md).
7. Next actor.

## Mode "subida" (expensive model, e.g. Opus) — near-misses only
1. `python3 -P scripts/leftovers.py --max-words 4` → actors with near-miss functions.
   (Variant: `--tag "<pattern>"` to do one pattern across actors, e.g. `--tag SetUnkAC`.)
2. Per actor: `printf '%s\tsolo\trunning\n' $A >> night_state.tsv`; `scripts/mkws.sh $A` (re-opens the merged
   actor from the main tree; drafts are under `#if 0` next to each GLOBAL_ASM). Read `notes/$A.md`.
3. Work ONLY the listed functions, ~15 min each max. On match: `python3 -P scripts/leftovers.py --done <F>`.
   On fail: update its row via the merge list.
4. `scripts/night_merge.sh $A "<still-unmatched Func:words:tag>"`; append a STATUS/idiom note.
5. Solved a pattern (e.g. SetUnkAC y/z order)? Write the recipe in the cheatsheet + `CLAUDE.md`, then
   tell the user: a cheap "barrido" over `--tag <pattern>` can now apply it everywhere.

## Mode "grandes" (mid model, e.g. Sonnet) — big functions
`python3 -P scripts/leftovers.py --tag big` → same loop as "subida", ~25 min per function.

## Files (all resumable)
- `queue.txt` actors not started · `night_state.tsv` per-actor state · `leftovers.tsv` one row per unmatched
  function (`scripts/leftovers.py`) · `notes/<A>.md` per-actor history · `timing.tsv` time log.
- Skip `cfg` / `static` rows in every mode (orchestrator-only: `scripts/cfg_split.py`, `notes/LOADER_RECIPE.md`).
