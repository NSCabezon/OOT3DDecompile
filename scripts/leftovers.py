#!/usr/bin/env python3
"""Central list of unmatched functions: leftovers.tsv (one row per function).

  leftovers.py --record <A> "<list>"   list items: Func | Func(tag) | Func:words:tag  (night_merge calls this)
  leftovers.py --done <Func>            drop a row after a later pass matched it
  leftovers.py [--max-words N] [--tag T] [--actor A] [--skip-tags cfg,static]
                                        print rows grouped by actor (default skips cfg,static)

Columns: actor  func  words  tag  date      words = differing words of best draft, "?" if unknown.
Tags: near (<=4 words), far, big (>120 insns, not attempted), cfg (needs cfg_split), static (guarded
function-local static / LOADER recipe), or free text.
"""
import argparse, os, re, sys, datetime
from collections import defaultdict

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(D, "leftovers.tsv")
HDR = "actor\tfunc\twords\ttag\tdate\n"

def load():
    if not os.path.exists(F):
        return []
    rows = []
    for line in open(F):
        p = line.rstrip("\n").split("\t")
        if p[0] == "actor" or len(p) < 5:
            continue
        rows.append(p[:5])
    return rows

def save(rows):
    with open(F, "w") as f:
        f.write(HDR)
        for r in rows:
            f.write("\t".join(r) + "\n")

def parse_item(it):
    it = it.strip()
    if not it:
        return None
    m = re.match(r"^([A-Za-z_]\w*)\((.*)\)$", it)
    if m:
        return m.group(1), "?", m.group(2)
    p = it.split(":")
    fn = p[0]
    words = p[1] if len(p) > 1 and p[1] else "?"
    tag = ":".join(p[2:]) if len(p) > 2 else ""
    if not tag and words.isdigit():
        tag = "near" if int(words) <= 4 else "far"
    return fn, words, tag

ap = argparse.ArgumentParser()
ap.add_argument("--record", nargs=2, metavar=("ACTOR", "LIST"))
ap.add_argument("--done")
ap.add_argument("--max-words", type=int)
ap.add_argument("--tag")
ap.add_argument("--actor")
ap.add_argument("--skip-tags", default="cfg,static")
a = ap.parse_args()
rows = load()

if a.record:
    A, lst = a.record
    today = datetime.date.today().isoformat()
    # split on commas not inside parentheses
    items, depth, cur = [], 0, ""
    for ch in lst:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            items.append(cur); cur = ""
        else:
            cur += ch
    items.append(cur)
    for it in items:
        r = parse_item(it)
        if not r:
            continue
        rows = [x for x in rows if not (x[0] == A and x[1] == r[0])]
        rows.append([A, r[0], r[1], r[2], today])
    save(rows)
    sys.exit()

if a.done:
    n = len(rows)
    rows = [x for x in rows if x[1] != a.done]
    save(rows)
    print(f"removed {n - len(rows)}")
    sys.exit()

skip = set(t for t in a.skip_tags.split(",") if t) if not a.tag else set()
by = defaultdict(list)
for r in rows:
    if a.actor and r[0] != a.actor:
        continue
    if a.tag and a.tag not in r[3]:
        continue
    if any(s in r[3] for s in skip):
        continue
    if a.max_words is not None and not (r[2].isdigit() and int(r[2]) <= a.max_words):
        continue
    by[r[0]].append(r)
tot = 0
for A in sorted(by):
    print(A + ": " + ", ".join(f"{r[1]}[{r[2]}{(' ' + r[3]) if r[3] else ''}]" for r in by[A]))
    tot += len(by[A])
print(f"-- {tot} functions in {len(by)} actors")
