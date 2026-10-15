#!/usr/bin/env python3
"""Plan cascade batches for one actor.

Lists every function of <A> still in asm (actor-dir GLOBAL_ASM + action FUN_s in
src/functions/*.cpp that are referenced only from this actor), with size, and splits
them into Haiku batches (small functions) and a Sonnet-direct list (large ones).

usage: plan_batches.py <A> [--tree oot3d|ws/<A>] [--max-insns 120] [--batch 8]
                            [--batch-insns 500] [--tsv]
Run from decomp-spike/. Default tree: ws/<A> if it exists, else oot3d.
"""
import argparse, glob, os, re, sys
from collections import defaultdict

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("actor")
ap.add_argument("--tree")
ap.add_argument("--max-insns", type=int, default=120)
ap.add_argument("--batch", type=int, default=8)
ap.add_argument("--batch-insns", type=int, default=500)
ap.add_argument("--tsv", action="store_true")
a = ap.parse_args()
A = a.actor
tree = a.tree or (f"ws/{A}" if os.path.isdir(f"{D}/ws/{A}/src") else "oot3d")
T = os.path.join(D, tree)

# functions.tsv: addr -> (name, insns)
by_addr, by_name = {}, {}
for line in open(f"{D}/analysis/aot/functions.tsv"):
    p = line.rstrip("\n").split("\t")
    if p[0] == "addr":
        continue
    ad, nm, ins = int(p[0], 16), p[1], int(p[3])
    by_addr[ad] = (nm, ins)
    by_name[nm] = (ad, ins)
lo, hi = min(by_addr), max(by_addr)

ga = re.compile(r'GLOBAL_ASM\("((?:asm|data)/[^"]+)\.s"\)')
actor_dir = f"{T}/src/game/actors/{A}"
if not os.path.isdir(actor_dir):
    sys.exit(f"no actor dir {actor_dir}")
actor_asm, actor_data = [], []
for f in sorted(glob.glob(f"{actor_dir}/*.cpp")):
    for m in ga.finditer(open(f, errors="replace").read()):
        k, n = m.group(1).split("/", 1)
        (actor_asm if k == "asm" else actor_data).append(n)

# asm still living in src/functions/*.cpp
func_asm = {}
for f in glob.glob(f"{T}/src/functions/functions_*.cpp"):
    for m in ga.finditer(open(f, errors="replace").read()):
        k, n = m.group(1).split("/", 1)
        if k == "asm":
            func_asm[n] = os.path.basename(f)

dis = f"{D}/oot3d/disassembly"
ref_re = re.compile(r"DCD 0x([0-9a-fA-F]{8})|(?:DCD|\bb(?:l|lx)?(?:eq|ne|lt|gt|le|ge|lo|hi|ls|hs)?)\s+([A-Za-z_][\w]*)")

def refs(path):
    out = set()
    try:
        txt = open(path, errors="replace").read()
    except OSError:
        return out
    for m in ref_re.finditer(txt):
        if m.group(1):
            v = int(m.group(1), 16) & ~1
            if lo <= v <= hi and v in by_addr:
                out.add(by_addr[v][0])
        elif m.group(2) in by_name:
            out.add(m.group(2))
    return out

# global index: who references each candidate (only files that mention a candidate)
cands = set(func_asm)
referrers = defaultdict(set)
for path in glob.glob(f"{dis}/asm/*.s") + glob.glob(f"{dis}/data/*.s"):
    src = os.path.basename(path)[:-2]
    for r in refs(path) & cands:
        if r != src:
            referrers[r].add(src)

# own = actor-dir asm/data + every <Prefix>_* asm (functions already in C still have their .s)
prefix = A.replace("_", "") + "_"
own = set(actor_asm) | set(actor_data)
own |= {os.path.basename(p)[:-2] for p in glob.glob(f"{dis}/asm/{prefix}*.s")}

def src_path(src):
    p = f"{dis}/asm/{src}.s"
    return p if os.path.exists(p) else f"{dis}/data/{src}.s"

# 1) everything reachable from the actor through still-asm functions/*.cpp candidates
reach, frontier = set(), list(own)
while frontier:
    nxt = [r for s in frontier for r in refs(src_path(s)) & cands if r not in reach and r not in own]
    reach |= set(nxt)
    frontier = nxt
# 2) prune to a fixed point: keep only those referenced from nowhere but actor ∪ kept
found = set(reach)
while True:
    drop = {r for r in found if referrers[r] - own - found}
    if not drop:
        break
    found -= drop
found = sorted(found)

rows = [(n, by_name.get(n, (0, 0))[1], "actor") for n in actor_asm]
rows += [(n, by_name.get(n, (0, 0))[1], func_asm[n]) for n in found]
rows.sort(key=lambda r: r[1])

small = [r for r in rows if r[1] <= a.max_insns]
big = [r for r in rows if r[1] > a.max_insns]
batches, cur, ci = [], [], 0
for r in small:
    if cur and (len(cur) >= a.batch or ci + r[1] > a.batch_insns):
        batches.append(cur); cur, ci = [], 0
    cur.append(r); ci += r[1]
if cur:
    batches.append(cur)

if a.tsv:
    for i, b in enumerate(batches, 1):
        for n, ins, w in b:
            print(f"haiku{i}\t{n}\t{ins}\t{w}")
    for n, ins, w in big:
        print(f"sonnet\t{n}\t{ins}\t{w}")
    sys.exit()

print(f"{A} (tree {tree}): {len(rows)} asm functions, {sum(r[1] for r in rows)} insns "
      f"({len(actor_asm)} actor dir, {len(found)} action FUN_s outside)")
for i, b in enumerate(batches, 1):
    print(f"haiku{i} ({sum(r[1] for r in b)} insns): " + ", ".join(f"{n}[{ins}]" for n, ins, _ in b))
print(f"sonnet-direct ({sum(r[1] for r in big)} insns): " + ", ".join(f"{n}[{ins}]" for n, ins, _ in big))
outside = [r for r in rows if r[2] != "actor"]
if outside:
    print("outside actor dir: " + ", ".join(f"{n}@{w}" for n, _, w in outside))
