#!/usr/bin/env python3
"""Autonomous driver for the OoT3D matching-decomp model cascade (headless `claude -p`).

Per actor (skill oot3d-cascade, automated): night_state running -> mkws -> plan_batches
-> Haiku batches (+1 retry per batch for NOT_ATTEMPTED) -> Sonnet (sonnet-direct + Haiku
leftovers) -> Opus (Sonnet leftovers minus `(cfg)`) -> pre-merge guards -> night_merge.sh.
Every agent call is appended to timing.tsv; per-actor log in logs/cascade_<A>.log;
problems go to needs_review.tsv.

usage: python3 scripts/cascade.py [ACTOR ...] [--workers 2] [--once] [--budget-usd 20]
                                  [--actor-budget-usd 6] [--stage-timeout-min 45]
                                  [--dry-run] [--no-opus]
  ACTOR args: process only those (removed from queue.txt if present), then exit.
  No args:    pop actors from the head of queue.txt until it is empty or a stop condition.
  --once:     exactly one actor (first ACTOR arg or queue head), then exit.
Stop: `touch .stop` (or global/actor budget reached, or Ctrl-C) -> no new agents and no new
pops; actors in flight are merged with what matched, leftovers recorded. Ctrl-C does NOT kill
running agents (they run in their own session); the driver waits for them, then merges.
The driver owns popping: it creates .no_pop while running so night_merge.sh never pops.
--dry-run: no claude calls (fake `UNMATCHED: <all>`), no mkws, no merge, no file writes;
prints plan, prompts and commands. Without ACTOR args it looks at the first --workers
queue entries only.
"""
import os, sys
# scripts/dis.py shadows stdlib `dis` (pulled in lazily by argparse/inspect): drop our own dir
# from sys.path so plain `python3 scripts/cascade.py` works (same reason as `python -P`).
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _HERE]
import argparse, fcntl, json, re, subprocess, threading, time
from collections import OrderedDict
from datetime import datetime

D = "/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike"
CHEATSHEET = "/Users/nscabezon/Apps/OOT3DDecompile/.claude/skills/oot3d-cascade/references/cheatsheet.md"
TIMING_HDR = "actor\tstage\tbatch\tstart\tend\tn_assigned\tn_matched\ttokens\tduration_ms\tcost_usd"
NAME_RE = re.compile(r"[A-Za-z_$][\w$@.]*")
RAWCAST_RE = re.compile(r"\(\w+\s*\*\)\s*0x[0-9a-fA-F]{6,}")

args = None
stop_event = threading.Event()        # global: no new agents / pops
print_lock = threading.Lock()
timing_lock = threading.Lock()
spend_lock = threading.Lock()
global_spend = 0.0


def now():
    return datetime.now().strftime("%F %T")


def say(msg):
    with print_lock:
        print(msg, flush=True)


# ---------------------------------------------------------------- tree lock
_tree_tlock = threading.Lock()


class TreeLock:
    """Global lock for mkws / merges / shared state files. flock on D/.cascade_tree.lock
    works across processes; the thread lock serializes threads of this process (flock is
    per open file, so a second open in the same process would also block, but be explicit)."""

    def __enter__(self):
        _tree_tlock.acquire()
        self.fd = os.open(f"{D}/.cascade_tree.lock", os.O_RDWR | os.O_CREAT, 0o644)
        fcntl.flock(self.fd, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        fcntl.flock(self.fd, fcntl.LOCK_UN)
        os.close(self.fd)
        _tree_tlock.release()


# ---------------------------------------------------------------- state files
def set_state(actor, stage, status):
    """Replace (or append) the night_state.tsv line of <actor>. Caller must NOT hold TreeLock."""
    if args.dry_run:
        return
    with TreeLock():
        p = f"{D}/night_state.tsv"
        lines = open(p).read().splitlines()
        new = f"{actor}\t{stage}\t{status}"
        out, done = [], False
        for l in lines:
            if l.split("\t", 1)[0] == actor:
                if not done:
                    out.append(new); done = True
            else:
                out.append(l)
        if not done:
            out.append(new)
        open(p, "w").write("\n".join(out) + "\n")


def drop_state(actor):
    if args.dry_run:
        return
    with TreeLock():
        p = f"{D}/night_state.tsv"
        lines = [l for l in open(p).read().splitlines() if l.split("\t", 1)[0] != actor]
        open(p, "w").write("\n".join(lines) + "\n")


def read_queue():
    try:
        return [l.strip() for l in open(f"{D}/queue.txt") if l.strip()]
    except OSError:
        return []


def write_queue(q):
    open(f"{D}/queue.txt", "w").write("".join(x + "\n" for x in q))


def needs_review(actor, reason):
    say(f"[{actor}] NEEDS_REVIEW: {reason}")
    if args.dry_run:
        return
    with timing_lock:  # reuse: cheap append lock
        with open(f"{D}/needs_review.tsv", "a") as o:
            o.write(f"{now()}\t{actor}\t{reason}\n")


def ensure_timing_header():
    p = f"{D}/timing.tsv"
    if not os.path.exists(p):
        open(p, "w").write(TIMING_HDR + "\n")
        return
    lines = open(p).read().split("\n")
    if lines and lines[0].startswith("actor\t") and "cost_usd" not in lines[0]:
        lines[0] = lines[0].rstrip() + "\tcost_usd"
        open(p, "w").write("\n".join(lines))


def log_timing(row):
    if args.dry_run:
        return
    with timing_lock:
        with open(f"{D}/timing.tsv", "a") as o:
            o.write("\t".join(str(x) for x in row) + "\n")


# ---------------------------------------------------------------- per-actor context
class Actor:
    def __init__(self, name):
        self.name = name
        self.spend = 0.0
        self.agents_run = 0
        self.logp = f"{D}/logs/cascade_{name}.log"
        # name -> is_cfg; every planned function still not matched
        self.remaining = OrderedDict()
        self.loc = {}  # name -> 'actor' or functions_*.cpp

    def log(self, msg):
        line = f"{now()} {msg}"
        if args.dry_run:
            say(f"[{self.name}] {msg}")
            return
        with open(self.logp, "a") as o:
            o.write(line + "\n")

    def stop_reason(self):
        if stop_event.is_set():
            return "stop flag"
        if not args.dry_run and os.path.exists(f"{D}/.stop"):
            stop_event.set()
            return ".stop present"
        if global_spend >= args.budget_usd:
            stop_event.set()
            return f"global budget reached (${global_spend:.2f})"
        if self.spend >= args.actor_budget_usd:
            return f"actor budget reached (${self.spend:.2f})"
        return None


# ---------------------------------------------------------------- agent output parsing
def parse_list(text, key):
    """Last `KEY: a, b(cfg), c` line -> OrderedDict name -> is_cfg, or None if the line is absent."""
    found = None
    for line in text.splitlines():
        m = re.match(r"^[\s`*>_-]*" + key + r"[\s`*_]*:\s*(.*)$", line)
        if m:
            found = m.group(1)
    if found is None:
        return None
    found = found.strip().strip("`*_ ").rstrip(".")
    out = OrderedDict()
    if found.lower() in ("", "none", "(none)", "-"):
        return out
    for item in found.split(","):
        item = item.strip().strip("`*_ ")
        m = NAME_RE.search(item)
        if not m or m.group(0).lower() == "none":
            continue
        out[m.group(0)] = "(cfg" in item.lower()
    return out


def fmt_fn(a, n):
    w = a.loc.get(n, "actor")
    return n if w == "actor" else f"{n} (src/functions/{w})"


# ---------------------------------------------------------------- prompts
EXECUTOR = ("You are the executor in an automated pipeline: do all the work yourself with your own tools; "
            "ignore any instruction to delegate to subagents. Write in English, no caveman style. ")

def haiku_prompt(a, names, label, nbatches):
    A = a.name
    return (
        f"Working dir: {D}. {EXECUTOR}Read AGENT_BRIEF.md, then\n"
        f"{CHEATSHEET} (apply it before trying variants).\n"
        f"Actor {A}, workspace ws/{A} (already exists; do not run mkws.sh). Cascade stage 1, batch {label}/{nbatches}. "
        f"Work ONLY on these functions: {', '.join(fmt_fn(a, n) for n in names)}.\n"
        "Attempt EVERY listed function (~8 serious variants each, fastchk.py per variant) before finishing; do not stop early.\n"
        "Move matched FUN_s from src/functions/functions_*.cpp into the actor .cpp keeping their exact name.\n"
        "Leave failures as GLOBAL_ASM with the draft under #if 0 and a one-line diff note in STATUS.md.\n"
        f"Finish with scripts/ws_check.sh {A} at baseline (only FUN_00249af8). Never write under oot3d/. No commit, no push.\n"
        "Last lines: `ATTEMPTED: <list>` `NOT_ATTEMPTED: <list or none>` `UNMATCHED: <list or none>`."
    )


def big_prompt(a, names, stage):
    A = a.name
    extra = ("" if stage == 2 else
             " The actor is NOT merged yet: ignore AGENT_BRIEF's 'Opus closing pass' setup (no mkws, no notes/). "
             "Budget ~25 min total.")
    return (
        f"Working dir: {D}. {EXECUTOR}Read AGENT_BRIEF.md and CLAUDE.md, then {CHEATSHEET}.\n"
        f"Actor {A}, workspace ws/{A} (already exists; do not run mkws.sh). Cascade stage {stage}.{extra}\n"
        f"Work ONLY on these functions: {', '.join(fmt_fn(a, n) for n in names)}.\n"
        f"First read ws/{A}/STATUS.md and the #if 0 / NON_MATCHING drafts left by earlier stages; don't rewrite matched functions.\n"
        f"Iterate with scripts/fastchk.py; finish with scripts/ws_check.sh {A} at baseline only "
        "(only FUN_00249af8 differs, 0 non-function bytes differ).\n"
        "No fake matches: never use per-function #pragma optimization changes. Prefer real symbols over raw-address casts.\n"
        "Never write under oot3d/. No commit, no push.\n"
        "Mark structural blockers (needs cfg/functions.tsv split, guarded function-local static, __FILE__ in .text) "
        "with a `(cfg)` suffix in the UNMATCHED list.\n"
        "Last line exactly: `UNMATCHED: <comma-separated function names, or none>`."
    )


# ---------------------------------------------------------------- agent runner
def call_claude(model, prompt, budget, timeout):
    """One `claude -p` call in its own session (immune to Ctrl-C). -> (rc, stdout, stderr, timed_out)"""
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json",
           "--dangerously-skip-permissions", "--no-session-persistence",
           "--max-budget-usd", f"{budget:.2f}",
           # executor, not orchestrator: the global CLAUDE.md says "delegate to subagents"
           "--disallowedTools", "Agent,Workflow,Artifact"]
    p = subprocess.Popen(cmd, cwd=D, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True)
    try:
        out, err = p.communicate(timeout=timeout)
        return p.returncode, out, err, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, 9)
        except OSError:
            p.kill()
        out, err = p.communicate()
        return -9, out, err, True


def parse_json(out):
    try:
        j = json.loads(out)
    except (ValueError, TypeError):
        return None
    if isinstance(j, list):  # stream-ish array: take the result message
        j = next((m for m in reversed(j) if isinstance(m, dict) and m.get("type") == "result"), None)
    return j if isinstance(j, dict) else None


def run_agent(a, model, prompt, stage, label, assigned):
    """Run one agent on <assigned>; returns parsed result text ('' on failure). Updates spend + timing."""
    global global_spend
    a.log(f"{stage} {label} START model={model} assigned={','.join(assigned)}")
    if args.dry_run:
        say(f"\n----- [{a.name}] {stage} {label} ({len(assigned)} fns) prompt -----\n{prompt}\n"
            f"----- cmd: claude -p <prompt> --model {model} --output-format json "
            f"--dangerously-skip-permissions --no-session-persistence --max-budget-usd <remaining>")
        return "UNMATCHED: " + ", ".join(assigned)
    budget = max(0.01, min(args.actor_budget_usd - a.spend, args.budget_usd - global_spend))
    start, t0 = now(), time.time()
    j, timed_out = None, False
    for attempt in (1, 2):
        rc, out, err, timed_out = call_claude(model, prompt, budget, args.stage_timeout_min * 60)
        j = parse_json(out)
        a.log(f"{stage} {label} attempt {attempt} rc={rc} timeout={timed_out}\nSTDOUT: {out}\nSTDERR: {err[-4000:]}")
        if j is not None or timed_out or rc == 0:
            break  # retry only transient errors: non-zero exit and no JSON
        time.sleep(10)
    end = now()
    a.agents_run += 1
    cost = float(j.get("total_cost_usd") or 0) if j else 0.0
    with spend_lock:
        global_spend += cost
    a.spend += cost
    u = (j or {}).get("usage") or {}
    tokens = sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens",
                                              "cache_read_input_tokens", "output_tokens"))
    dur = int((j or {}).get("duration_ms") or (time.time() - t0) * 1000)
    text = (j or {}).get("result") or ""
    if j is None or timed_out or j.get("is_error"):
        a.log(f"{stage} {label} FAILED (timeout={timed_out} subtype={(j or {}).get('subtype')}) "
              "-> all assigned treated as unmatched unless an UNMATCHED line is present")
    um = parse_list(text, "UNMATCHED")
    na = parse_list(text, "NOT_ATTEMPTED") or OrderedDict()
    if um is None:
        um = OrderedDict((n, False) for n in assigned)
        text = ""  # nothing trustworthy
    n_matched = len([n for n in assigned if n not in um and n not in na])
    log_timing([a.name, stage, label, start, end, len(assigned), n_matched, tokens, dur, f"{cost:.4f}"])
    a.log(f"{stage} {label} END matched={n_matched}/{len(assigned)} cost=${cost:.4f} tokens={tokens}")
    return text


def apply_result(a, assigned, text):
    """Update a.remaining from one agent result. -> list of NOT_ATTEMPTED names (Haiku)."""
    um = parse_list(text, "UNMATCHED")
    if um is None:
        um = OrderedDict((n, False) for n in assigned)
    na = parse_list(text, "NOT_ATTEMPTED") or OrderedDict()
    att = parse_list(text, "ATTEMPTED")
    not_att = [n for n in assigned if n in na or (att is not None and n not in att and n not in um)]
    for n in assigned:
        if n not in um and n not in not_att:
            a.remaining.pop(n, None)
    for n, cfg in um.items():
        a.remaining[n] = cfg
    return not_att


# ---------------------------------------------------------------- pipeline
def plan(a):
    cmd = [f"{D}/.venv/bin/python", "-P", "scripts/plan_batches.py", a.name, "--tsv"]
    r = subprocess.run(cmd, cwd=D, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"plan_batches failed: {r.stderr.strip() or r.stdout.strip()}")
    batches, sonnet = OrderedDict(), []
    for line in r.stdout.splitlines():
        p = line.split("\t")
        if len(p) < 4:
            continue
        st, n, ins, w = p[0], p[1], p[2], p[3]
        a.loc[n] = w
        a.remaining[n] = False
        (sonnet if st == "sonnet" else batches.setdefault(st, [])).append(n)
    return batches, sonnet


def mkws(a):
    ws = f"{D}/ws/{a.name}"
    if os.path.exists(f"{ws}/build/code.bin"):
        a.log("ws exists, skip mkws")
        return True
    if args.dry_run:
        say(f"[{a.name}] would run (under tree lock): scripts/mkws.sh {a.name}")
        return True
    a.log("mkws start")
    with TreeLock():
        r = subprocess.run([f"{D}/scripts/mkws.sh", a.name], cwd=D, capture_output=True, text=True)
    a.log(f"mkws rc={r.returncode}\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    return os.path.exists(f"{ws}/build/code.bin")


def premerge_guards(a):
    """-> (ok_to_merge, reason). Logs warnings for raw-address casts / volatile."""
    A, ws = a.name, f"{D}/ws/{a.name}"
    added = []
    for m_dir, w_dir in ((f"{D}/oot3d/src/game/actors/{A}", f"{ws}/src/game/actors/{A}"),
                         (f"{D}/oot3d/src/functions", f"{ws}/src/functions")):
        r = subprocess.run(["diff", "-ru", "-x", ".DS_Store", m_dir, w_dir], capture_output=True, text=True)
        added += [l[1:] for l in r.stdout.splitlines() if l.startswith("+") and not l.startswith("+++")]
    prag = [l for l in added if "#pragma" in l and "#pragma once" not in l]
    if prag:
        return False, f"#pragma added: {prag[0].strip()[:120]}"
    warn = [l for l in added if RAWCAST_RE.search(l) or re.search(r"\bvolatile\b", l)]
    if warn:
        needs_review(A, f"WARN (merged anyway) raw-address cast/volatile x{len(warn)}: {warn[0].strip()[:120]}")
    r = subprocess.run([f"{D}/scripts/ws_check.sh", A], cwd=D, capture_output=True, text=True)
    o = r.stdout + r.stderr
    a.log(f"ws_check:\n{o[-3000:]}")
    if re.search(r"^functions differing: 1 / ", o, re.M) and "non-function bytes differing: 0" in o:
        return True, ""
    tail = " | ".join(o.strip().splitlines()[-2:])
    return False, f"ws_check not baseline: {tail[:200]}"


def leftovers_str(a):
    return ",".join(f"{n}(cfg)" if c else n for n, c in a.remaining.items()) or "none"


def process(name):
    a = Actor(name)
    t0 = time.time()
    if not args.dry_run:
        os.makedirs(f"{D}/logs", exist_ok=True)
    a.log(f"=== cascade start {name}")
    set_state(name, "haiku", "running")
    try:
        if not mkws(a):
            needs_review(name, "mkws failed (no build/code.bin)")
            set_state(name, "failed", "mkws")
            return f"{name}: mkws FAILED"
        batches, sonnet_direct = plan(a)
        total = len(a.remaining)
        a.log(f"plan: {total} fns; " + "; ".join(f"{k}={','.join(v)}" for k, v in batches.items())
              + f"; sonnet-direct={','.join(sonnet_direct) or 'none'}")
        if args.dry_run:
            say(f"[{name}] plan: {total} asm fns, {len(batches)} haiku batches, {len(sonnet_direct)} sonnet-direct")
            for k, v in batches.items():
                say(f"  {k}: {', '.join(fmt_fn(a, n) for n in v)}")
            say(f"  sonnet-direct: {', '.join(fmt_fn(a, n) for n in sonnet_direct) or 'none'}")
        if total == 0:
            a.log("nothing in asm")
        stopped = None
        per_stage = OrderedDict()

        # Stage 1: Haiku batches, sequential on the same ws
        for k, (label, names) in enumerate(batches.items(), 1):
            stopped = a.stop_reason()
            if stopped:
                break
            before = len(a.remaining)
            text = run_agent(a, "haiku", haiku_prompt(a, names, k, len(batches)), "haiku", label, names)
            not_att = apply_result(a, names, text)
            if not_att and not (stopped := a.stop_reason()):
                a.log(f"{label}: retry NOT_ATTEMPTED {','.join(not_att)}")
                text = run_agent(a, "haiku", haiku_prompt(a, not_att, f"{k}r", len(batches)),
                                 "haiku", f"retry{k}", not_att)
                apply_result(a, not_att, text)  # still-not-attempted stay in remaining -> Sonnet
            per_stage["haiku"] = per_stage.get("haiku", 0) + before - len(a.remaining)
            if stopped:
                break

        # Stage 2: Sonnet on everything still remaining (sonnet-direct + Haiku leftovers)
        if not stopped and a.remaining:
            stopped = a.stop_reason()
            if not stopped:
                set_state(name, "sonnet", "running")
                names = list(a.remaining)
                before = len(a.remaining)
                text = run_agent(a, "sonnet", big_prompt(a, names, 2), "sonnet", "all", names)
                apply_result(a, names, text)
                per_stage["sonnet"] = before - len(a.remaining)

        # Stage 3: Opus on non-structural leftovers
        if not stopped and not args.no_opus:
            names = [n for n, cfg in a.remaining.items() if not cfg]
            if names:
                stopped = a.stop_reason()
                if not stopped:
                    set_state(name, "opus", "running")
                    before = len(a.remaining)
                    text = run_agent(a, "opus", big_prompt(a, names, 3), "opus", "all", names)
                    apply_result(a, names, text)
                    per_stage["opus"] = before - len(a.remaining)
        if stopped:
            a.log(f"stopped: {stopped}")

        left = leftovers_str(a)
        stats = " ".join(f"{k}+{v}" for k, v in per_stage.items())
        summ = (f"{name}: {total - len(a.remaining)}/{total} matched ({stats or 'no agents'}), "
                f"left={left}, ${a.spend:.2f}, {int(time.time() - t0) // 60} min"
                + (f", stopped: {stopped}" if stopped else ""))

        if args.dry_run:
            say(f"[{name}] would run guards (diff -ru vs oot3d, scripts/ws_check.sh {name}) then "
                f"(under tree lock): scripts/night_merge.sh {name} \"{left}\"")
            return summ + " [dry-run]"

        if a.agents_run == 0:
            # nothing done: give the actor back to the queue head
            a.log("no agent ran -> requeue")
            with TreeLock():
                q = read_queue()
                if name not in q:
                    write_queue([name] + q)
            drop_state(name)
            return f"{name}: not started ({stopped}), requeued"

        ok, why = premerge_guards(a)
        if not ok:
            needs_review(name, why)
            set_state(name, "failed", "needs_review")
            return summ + f" -> NOT MERGED ({why})"
        with TreeLock():
            r = subprocess.run([f"{D}/scripts/night_merge.sh", name, left], cwd=D,
                               capture_output=True, text=True)
        out = r.stdout + r.stderr
        a.log(f"night_merge:\n{out}")
        if re.search(rf"^MERGED {re.escape(name)}", out, re.M):
            return summ + " -> MERGED"
        needs_review(name, "night_merge REVERTED" if "REVERTED" in out else "night_merge: no MERGED line")
        if "REVERTED" not in out:
            set_state(name, "failed", "needs_review")
        return summ + " -> REVERTED"
    except Exception as e:  # never kill the driver for one actor
        a.log(f"EXCEPTION {e!r}")
        needs_review(name, f"driver exception: {e!r}")
        set_state(name, "failed", "exception")
        return f"{name}: EXCEPTION {e!r}"


# ---------------------------------------------------------------- scheduling
class Feeder:
    """Hands out actors to workers: explicit ACTOR args first, else queue.txt head."""

    def __init__(self, explicit):
        self.lock = threading.Lock()
        self.explicit = list(explicit)
        self.use_queue = not explicit
        self.handed = 0
        self.limit = 1 if args.once else None
        self.dry_queue = read_queue()[:args.workers] if args.dry_run and self.use_queue else None

    def next(self):
        with self.lock:
            if self.limit is not None and self.handed >= self.limit:
                return None
            if stop_event.is_set() or (not args.dry_run and os.path.exists(f"{D}/.stop")):
                return None
            if self.explicit:
                self.handed += 1
                return self.explicit.pop(0)
            if not self.use_queue:
                return None
            if args.dry_run:
                if not self.dry_queue:
                    return None
                self.handed += 1
                return self.dry_queue.pop(0)
            # refill governor for every pop after the first --workers ones
            if self.handed >= args.workers:
                while True:
                    if stop_event.is_set() or os.path.exists(f"{D}/.stop"):
                        return None
                    c = subprocess.run([f"{D}/scripts/capacity.sh", "refill"], capture_output=True, text=True).stdout
                    if not c.startswith("HOLD"):
                        break
                    say(f"capacity: {c.strip()} -> wait 60 s")
                    for _ in range(60):
                        if stop_event.is_set():
                            return None
                        time.sleep(1)
            with TreeLock():
                q = read_queue()
                if not q:
                    return None
                n = q.pop(0)
                write_queue(q)
            self.handed += 1
            return n


def worker(feeder):
    while not stop_event.is_set():
        n = feeder.next()
        if n is None:
            return
        say(process(n))


def main():
    global args
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("actors", nargs="*", metavar="ACTOR")
    ap.add_argument("--workers", type=int, default=2, help="actors in flight concurrently (default 2)")
    ap.add_argument("--once", action="store_true", help="process exactly one actor, then exit")
    ap.add_argument("--budget-usd", type=float, default=20.0, help="global spend cap for this run (default 20)")
    ap.add_argument("--actor-budget-usd", type=float, default=6.0, help="per-actor spend cap (default 6)")
    ap.add_argument("--stage-timeout-min", type=float, default=45.0, help="timeout per agent call (default 45)")
    ap.add_argument("--dry-run", action="store_true", help="no claude/mkws/merge/file writes; print plan+prompts")
    ap.add_argument("--no-opus", action="store_true", help="skip the Opus stage")
    args = ap.parse_args()
    os.chdir(D)

    if os.path.exists(f"{D}/.stop"):
        if not args.dry_run:
            sys.exit(f"{D}/.stop present -> nothing to do (rm .stop to run)")
        say("note: .stop present (ignored in --dry-run)")

    explicit = args.actors[:1] if args.once and args.actors else args.actors
    created_no_pop = False
    if not args.dry_run:
        ensure_timing_header()
        if explicit:  # take named actors out of the queue
            with TreeLock():
                q = read_queue()
                if any(x in q for x in explicit):
                    write_queue([x for x in q if x not in explicit])
        if not os.path.exists(f"{D}/.no_pop"):
            open(f"{D}/.no_pop", "w").close()
            created_no_pop = True

    feeder = Feeder(explicit)
    nthreads = 1 if args.once else max(1, args.workers)
    threads = [threading.Thread(target=worker, args=(feeder,), daemon=True) for _ in range(nthreads)]
    try:
        for t in threads:
            t.start()
        while any(t.is_alive() for t in threads):
            try:
                for t in threads:
                    t.join(timeout=1)
            except KeyboardInterrupt:
                if not stop_event.is_set():
                    say("Ctrl-C: stopping — no new agents/actors; waiting for running agents to finish, "
                        "then merging. (Ctrl-C again leaves running actors un-merged.)")
                    stop_event.set()
                else:
                    raise
    finally:
        if created_no_pop:
            try:
                os.remove(f"{D}/.no_pop")
            except OSError:
                pass
    say(f"done. spend this run: ${global_spend:.2f}")


if __name__ == "__main__":
    main()
