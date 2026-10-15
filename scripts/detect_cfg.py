#!/usr/bin/env python3
"""Find cfg-merged tails: code the disassembler left as DCB/DCD data after a function's
literal pool (unreachable from the head, reached via action/draw tables).

usage: detect_cfg.py <A> [--tree oot3d|ws/<A>]   -> one line per candidate:
       HEAD  ADDR  KIND  [ref]      (ref = address appears as a DCD in data/; strong sign)
       Candidates are HINTS: unreferenced bx_lr may be the end of a tail, and the entry may sit
       a few words before the push. Read the asm (decode DCB words) before splitting.
       detect_cfg.py --all          -> scan every asm function still referenced by GLOBAL_ASM
Run from decomp-spike/. Feed confirmed rows to cfg_split.py / apply_split_merge.sh.
"""
import glob, os, re, struct, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASM = [f"{D}/oot3d/disassembly/asm"]  # original (pre-split) files

def kind(w):
    if w == 0xE12FFF1E: return "bx_lr"
    if w == 0xE1A00000: return "nop_mov"
    if (w & 0xFFFF0000) == 0xE92D0000 and w & 0x4000: return "push"
    if (w & 0xFFBF0F00) == 0xED2D0B00: return "vpush"
    if (w & 0xFF000000) == 0xEA000000: return "b"
    return None

def words(path):
    """yield (addr, word) for DCB/DCD data in the file, tracking _xxxxxxxx labels."""
    addr, buf, out = None, b"", []
    def flush():
        nonlocal buf, addr
        if addr is None: buf = b""; return
        for i in range(0, len(buf) - 3, 4):
            out.append((addr + i, struct.unpack("<I", buf[i:i+4])[0]))
        addr += len(buf); buf = b""
    for line in open(path, errors="replace"):
        m = re.match(r"_([0-9a-f]{8})\b", line)
        if m:
            flush(); addr = int(m.group(1), 16)
            line = line[m.end():]
        s = line.strip()
        if s.startswith("DCB"):
            buf += bytes(int(x, 16) for x in re.findall(r"0x([0-9a-f]{2})", s))
        elif s.startswith("DCD"):
            v = re.findall(r"0x([0-9a-f]+)", s)
            buf += b"".join(struct.pack("<I", int(x, 16)) for x in v) if v else b"\0\0\0\0"
        elif s and not s.startswith(("AREA", "EXPORT", "END", ";")) and not re.match(r"[A-Za-z_]\w*$", s):
            flush(); addr = None  # code line: address unknown until next label
    flush()
    return out

_refs = None
def refs():
    global _refs
    if _refs is None:
        _refs = set()
        for f in glob.glob(f"{D}/oot3d/disassembly/data/*.s") + glob.glob(f"{D}/oot3d/src/**/*.s", recursive=True):
            for m in re.finditer(r"0x00([0-9a-f]{6})\b", open(f, errors="replace").read()):
                _refs.add(int(m.group(1), 16))
    return _refs

def scan(name):
    for d in ASM:
        p = f"{d}/{name}.s"
        if os.path.exists(p): break
    else: return []
    res = []
    for ad, w in words(p):
        k = kind(w)
        if k and ad % 4 == 0:
            # real entry may be a few insns before the push (pool ldr first): prefer a referenced addr
            st = next((ad - d for d in (0, 4, 8, 12, 16) if ad - d in refs()), ad)
            res.append((name, st, k, st in refs()))
    return res

def actor_funcs(A, T):
    ga = re.compile(r'GLOBAL_ASM\("(?:\.\./split/)?asm/([\w$@.]+)\.s"\)')
    names = set()
    for f in glob.glob(f"{T}/src/game/actors/{A}/*.cpp"):
        names |= set(ga.findall(open(f, errors="replace").read()))
    # action FUN_s outside the actor dir: reuse plan_batches' notion via --tsv
    import subprocess
    r = subprocess.run([sys.executable, "-P", f"{D}/scripts/plan_batches.py", A, "--tsv"],
                       capture_output=True, text=True, cwd=D)
    for l in r.stdout.splitlines():
        p = l.split("\t")
        if len(p) > 1: names.add(p[1])
    return sorted(names)

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args: sys.exit(__doc__)
    if args[0] == "--func":
        names = set(args[1:])
    elif args[0] == "--all":
        ga = re.compile(r'GLOBAL_ASM\("(?:\.\./split/)?asm/([\w$@.]+)\.s"\)')
        names = set()
        for f in glob.glob(f"{D}/oot3d/src/**/*.cpp", recursive=True):
            names |= set(ga.findall(open(f, errors="replace").read()))
    else:
        A = args[0]
        T = f"{D}/" + (args[args.index("--tree") + 1] if "--tree" in args else "oot3d")
        names = actor_funcs(A, T)
    for n in sorted(names):
        seen = set()
        for h, ad, k, r in scan(n):
            if ad in seen: continue
            seen.add(ad)
            # push/vpush/bx_lr after a pool = function start; lone nop_mov only if referenced
            if k in ("nop_mov", "b") and not r: continue
            print(f"{h}\t0x{ad:08X}\t{k}" + ("\tref" if r else ""))
