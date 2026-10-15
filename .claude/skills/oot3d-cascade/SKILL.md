---
name: oot3d-cascade
description: Run the OoT3D matching-decomp model cascade on one or more actors (Haiku in small size-routed batches → Sonnet → Opus → merge), with timing. Use when the user says "haz un par de clases/actores más", "siguiente actor", "decompila <Actor>", "cascada", or invokes /oot3d-cascade. Args: actor names, "N actores", "grande", "solo haiku".
---

# OoT3D cascade (orchestrator)

> **Retired 2026-10-13 (cost).** Current mode: `decomp-spike/RUNBOOK_SOLO.md` — single session, no subagents. Use this skill only if the user explicitly asks for the subagent cascade. The cheatsheet in `references/` is still the shared idiom table.

Root `$D = /Users/nscabezon/Apps/OOT3DDecompile/decomp-spike`. Read `$D/CLAUDE.md` "Resume" + "Workflow" once per session. The user decided the model order (Haiku → Sonnet → Opus); don't change it, change only how work is split.

## Why batches
Haiku matches as well as Sonnet on small scopes (A/B: 4–7 functions per agent) but on whole large actors it stops early and skips most functions (2026-10-13: En_Horse 7/54, En_Xc 9/~85). So Haiku gets batches of ≤8 small functions; large functions go straight to Sonnet.

## Steps per actor
1. **Pick**: next from `queue.txt` (or what the user named / "grande" = largest by `plan_batches.py` total). Remove it from queue.txt, add `<A>\thaiku\trunning` to `night_state.tsv`. Keep `.stop` present unless the user wants autopop.
2. **Workspace**: `scripts/mkws.sh <A>` — sequentially, never while a merge runs.
3. **Plan**: `.venv/bin/python -P scripts/plan_batches.py <A>` → `haikuN` batches (≤120 insns per fn, ≤8 fns / ≤500 insns per batch) + `sonnet-direct` list + action FUN_s found outside the actor dir. Defaults are tunable (`--max-insns`, `--batch`).
4. **Haiku batches**: one `general-purpose` agent with `model: haiku` per batch, **sequential on the same ws** (they edit the same .cpp). Prompt template below. Haiku batches of one actor can run in parallel with other actors' agents.
5. **Sonnet**: one agent (`model: sonnet`) on the `sonnet-direct` list + everything Haiku left in `UNMATCHED`. Can start in parallel with the Haiku batches only if it is put in a different .cpp — default: run after the Haiku batches.
6. **Opus**: on Sonnet's leftovers, skipping structural ones (`(cfg)`, guarded statics, `__FILE__` in .text).
7. **Merge**: `scripts/night_merge.sh <A> "<final leftovers>"` (one at a time). It verifies baseline and reverts on failure.
8. **Timing**: append to `$D/timing.tsv` one line per agent: `actor stage batch start end n_assigned n_matched tokens duration_ms` (start/end via `date '+%F %T'`; tokens/duration from the task notification).

## Haiku batch prompt (template)
```
Working dir: /Users/nscabezon/Apps/OOT3DDecompile/decomp-spike. Read AGENT_BRIEF.md, then
/Users/nscabezon/Apps/OOT3DDecompile/.claude/skills/oot3d-cascade/references/cheatsheet.md (apply it before trying variants).
Actor <A>, workspace ws/<A>. Cascade stage 1, batch <k>/<n>. Work ONLY on these functions: <list with file for each FUN_ outside the actor dir>.
Attempt EVERY listed function (~8 serious variants each, fastchk.py per variant) before finishing; do not stop early.
Move matched FUN_s from src/functions/functions_*.cpp into the actor .cpp keeping their exact name.
Leave failures as GLOBAL_ASM with the draft under #if 0 and a one-line diff note in STATUS.md.
Finish with scripts/ws_check.sh <A> at baseline (only FUN_00249af8). Never write under oot3d/. No commit, no push.
Last lines: `ATTEMPTED: <list>` `NOT_ATTEMPTED: <list or none>` `UNMATCHED: <list or none>`.
```
If `NOT_ATTEMPTED` is non-empty, resend those to a new Haiku batch before moving to Sonnet.

## Sonnet/Opus prompt
As in `$D/CLAUDE.md` Resume step 3, plus the explicit function list and "read ws/<A>/STATUS.md and the #if 0 drafts". Mark structural blockers with `(cfg)`.

## Report to the user
Per actor: matched/total per stage, time per stage, tokens, what was left and why. Spanish, short. % only if asked (`scripts/pct.sh`).
