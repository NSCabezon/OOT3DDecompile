# Brief: matching decomp of one OoT3D actor (RVCT 4.0 b839 under wibo, macOS)

Replace `<A>` below with your actor name. Root: `/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike` (= `$D`).

## Setup (first step)
- If `$D/ws/<A>/build/code.bin` doesn't exist: run `$D/scripts/mkws.sh <A>` (~80 s). It creates your isolated workspace `$D/ws/<A>/`.
- `mkws.sh` (which copies oot3d/ into your workspace) is REQUIRED. After that, never manually copy individual files from oot3d/ into your workspace.
- Edit ONLY inside `$D/ws/<A>/`. `disassembly/` there is symlinked and READ-ONLY. Never touch `$D/oot3d/` or other `ws/*`. No git commit/push.

## Task
1. In `src/game/actors/<A>/*.cpp`, replace every `GLOBAL_ASM("asm/<Func>.s")` with C that compiles byte-identical. Asm: `disassembly/asm/<Func>.s`.
2. Action functions of the actor often live OUTSIDE the actor dir, as `FUN_xxxxxxxx` `GLOBAL_ASM` lines in `src/functions/functions_*.cpp` (find them via function pointers the actor stores, e.g. actionFunc set in Init). If they clearly belong to this actor (only referenced from it; N64 counterpart exists in the same N64 actor file), decompile them too: MOVE the definition into the actor's .cpp right where it fits and delete the GLOBAL_ASM line from functions_*.cpp — but ONLY if the link still matches (the scatter file pins functions by name, so moving files is fine). If unsure, decompile in place in functions_*.cpp. Limit: ~15 functions total — unless the prompt gives an explicit function list (batch mode): then do exactly that list, all of it.
3. `GLOBAL_ASM("data/...")` may stay.

## Tools
- Check: `$D/scripts/ws_check.sh <A>` (1–5 s). Baseline = only `FUN_00249af8` differs (known, ignore). Goal: no NEW differing function. `L6221E ... overlaps` = your function is too big.
- Fast iteration (~1 s, no link): `cd $D && .venv/bin/python -P scripts/fastchk.py <A> src/game/actors/<A>/<file>.cpp FUNC [FUNC...]` (`SIDE=FUNC` env for side-by-side). Always finish with ws_check.sh.
- Side-by-side: `cd $D && .venv/bin/python -P scripts/asmdiff.py ws/<A>/disassembly/baserom/exefs/code.bin ws/<A>/build/code.bin analysis/aot/functions.tsv <Func>` (`-P` required).
- Flags: `-O3 -Otime --cpu=MPCore --arm --fpmode=fast`, C++ inside `extern "C" {}`.

## References
- N64 decomp: `$D/tools/repos/oot/src/overlays/actors/ovl_<A>/` (near 1:1 logic).
- Matching examples: `src/game/actors/{Obj_Roomtimer,En_Wall_Tubo,Obj_Makekinsuta,En_Anubice_Tag,En_Bom_Bowl_Pit}/`.
- Known 3DS differences: `Actor` is 0x1A4 bytes (N64 0x14C) → actor fields shifted +0x58; Init often sets `actor.unk_19A = 1` first; extra `Actor_Spawn` arg; timers scaled by `R_UPDATE_RATE`; some N64 statics moved into PlayState; debug draw stripped; some N64 actors are empty `bx lr` stubs.
- Unknown callees: grep `include/` for an existing declaration first; else declare `FUN_xxxxxxxx` locally in the .cpp with a plausible prototype. Prefer local declarations over editing `include/` (other agents work in parallel; shared header edits cause merge conflicts). If you MUST edit `include/`, only ADD lines and list them in your report.

## Rules
- Scratch files: ONLY inside `$D/ws/<A>/tmp/` (never the shared session scratchpad — other agents clobber it).
- Timebox: ~8 serious attempts per function, then leave it as GLOBAL_ASM. Never leave the build broken.
- Keep `$D/ws/<A>/STATUS.md` current (user watches it): per function matched / not matched (reason) / in progress.
- Finish with ws_check.sh showing only the baseline.

## Report (short)
matched/total (actor dir + moved FUN_s), left as asm + reason, files touched outside the actor dir (exact list), `include/` additions, notable 3DS-vs-N64 findings.

## Cascade stages
- Stage 1 (Haiku): batch mode — only the functions listed in the prompt (planned by `scripts/plan_batches.py`; see skill `oot3d-cascade`). Read `/Users/nscabezon/Apps/OOT3DDecompile/.claude/skills/oot3d-cascade/references/cheatsheet.md` first. Without a list: full actor as above.
- Stage 2/3 (Sonnet/Opus): the workspace `ws/<A>` already exists from the previous stage. Read `ws/<A>/STATUS.md` and the `#ifdef NON_MATCHING` / `#if 0` attempts. Work ONLY on functions not yet matched (incl. obvious action FUN_s the previous stage skipped). Don't rewrite matched functions. Also replace raw-address hacks with something cleaner if you can do it within the actor dir.
- Never use per-function `#pragma` optimization changes (fake match).
- Last line of your final report, exactly: `UNMATCHED: <comma-separated function names, or none>`

## Opus closing pass
- The actor is ALREADY merged in oot3d/ with matched functions in C; leftovers are GLOBAL_ASM with drafts under `#if 0` in the actor .cpp. Read `notes/<A>.md` (previous attempts) first.
- Run `scripts/mkws.sh <A>` (fresh workspace from the current main tree).
- Target ONLY the listed functions. Use `scripts/fastchk.py` to iterate quickly; budget ~25 minutes total.
- Skip anything that needs a functions.tsv/cfg split, a linker-script change, or a new data symbol outside the actor dir.
- No fake matches (no per-function pragmas, no invented constructors). `volatile` only as last resort and say so.
- Final: ws_check.sh baseline only. Report `UNMATCHED: ...` as usual.
