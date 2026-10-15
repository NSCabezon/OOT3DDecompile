# OoT3D decomp spike — REPORT (2026-10-12)

## Conclusion
- The zeldaret/oot3d decomp, which reproduces the original code.bin exactly, now runs on this Mac up to the compile step. Extraction, disassembly, splitting and cmake configure all work. Compiling stops only because RVCT 4.0 b821 needs a FlexLM license; licensing was not bypassed.
- Upstream is at **0.34 % of `.text` in C** (125 functions). Their own progress script prints 3.3 %, but that is a counting bug.
- The 18 pilot functions behave the same as the original bytes in a unicorn comparison: 1,000/1,000 equal runs each.
- For visionOS the realistic route is AOT recompilation, not a native port.

## Phase 1: extraction
- **Tool:** `scripts/extract.py`, a pure-Python extractor. Its output matches the repo's ctrtool byte for byte.
- **code.bin:** 4,567,040 B decompressed (it is compressed inside the ROM).

  | Segment | Address | Size |
  |---|---|---|
  | `.text` | 0x100000 | 3,971,496 B |
  | `.rodata` | 0x4CA000 | 189,256 B |
  | `.data` | 0x4F9000 | 397,856 B |
  | `.bss` | — | 443,368 B |

- **No dynamic modules:** RomFS (1,944 files, 470 MB) has no `.cro/.crs/.crr`. Actors are statically linked; there are no overlays.
- **SDK:** `CTR_SDK-1_2_0_200`, Firmware 02_27, Mobiclip Deblocker 1.0.3 / Dec 1.0.1 / MoflexDemuxer 1.0.2.
- **Source hints:** 49 assert paths of the form `d:\home\queen\...\sources\*.cpp`, plus an engine library called `gzw`.
- **USA vs EUR:** segment sizes are identical. 11,994 of 12,031 functions are the same apart from address shifts (EUR shifts +0x24/+0x20 between 0x419E18 and 0x4A5ADF); 36 differ.

## Phase 2: toolchain and compiler access
- **Compiler and flags:**
  - RVCT 4.0 Build 821, 100 % ARM, C++ written mostly as C.
  - Flags: `--cpu=MPCore --arm --fpmode=fast -O3 -Otime --split_sections`, no RTTI or exceptions.
  - The linker scatter file pins every function to its original address, so functions can be matched one at a time.
- **The user's RVCT package under `wibo-macos`:**
  - All tools run and report `--vsn`.
  - `armcc`, `armasm`, `armlink` and `fromelf` all need FlexLM features (`compiler`/`bsp_compiler`, `armasm`, `armlink`, `fromelf`, version 4.0). `armar` does not.
  - So the whole build is license-gated, not just compiling.
- **wibo test:** `wibo-macos` 1.2.0 was tested with a small self-built 32-bit Windows program. Arguments, exit codes, environment variables, and Unix, `Z:\` and relative paths all work.
- **Legitimate license routes:**
  - An Arm support case or Arm tools distributor, for a legacy node-locked or floating license. Arm staff say legacy compilers don't support UBL but older license types can still be bought.
  - Whether an Arm Development Studio (Gold, UBL) license covers RVCT 4.0's FlexLM features is unclear; ask Arm before buying.
  - A node-locked license's host-ID check under wibo is untested. The fallback is the Linux i386 package in a linux/386 container.
- **decomp.me:** it offers `n3ds` / `armcc_40_821` for matching single functions today. Using it means uploading that function's assembly, which is ROM-derived, to a public site. That is the user's call; it was not done.

## Ready-to-build setup once a license exists
```sh
cd decomp-spike/oot3d
R=/Users/nscabezon/Apps/OOT3DDecompile/standard-win_32-pentium-rel
export ARMCC_PATH=$R RVCT40INC=$R/include/windows RVCT40LIB=$R/lib WIBO=$PWD/../tools/wibo/wibo-macos
export ARMLMD_LICENSE_FILE=/path/license.dat   # or LM_LICENSE_FILE=port@server
build/armwrap/armcc --vsn                      # then a 1-line test compile to confirm the license
rm -rf build && cmake -B build -S . -G "Unix Makefiles" && cmake --build build -t check -j8
```
- **What the macOS patch changes** (`patches/0001`):
  - Setting `WIBO` makes CMake generate `build/armwrap/*` wrappers.
  - It forces a Generic target, so CMake stops adding `-arch arm64`.
  - It forces `.o` object names and the armlink/armar rules.
  - It switches `python` to `python3` and adds macOS shims for the two bundled Linux/Windows tools.
- **Already verified:** configure succeeds and a real compile reaches `C9932E`, the license error.
- **Not yet tested:** the `md5sum -c` step in the `check` target.

## Phase 3: static analysis and AOT statistics
Source: `scripts/aot_stats.py`, output in `analysis/aot/`.

| Metric | Value |
|---|---|
| Functions / instructions | 12,031 functions, 899,718 instructions |
| Direct calls / tail calls | 58,522 / 3,691; 23 call targets are not known function starts |
| Indirect calls (`blx reg`) | 1,833 |
| Indirect jumps (`bx reg`) | 317 |
| Switch tables (`ldrlo pc,[pc,rN,lsl#2]`) | 446, with 5,607 entries; 10 have no bound found |
| Other computed jumps | 51 |
| SVC sites | 327 |
| Function size | median 144 B, p90 744 B, max 24.5 KB |

- **Ghidra 12.1.4 headless** found 9,153 functions; 2,912 that the repo's function list has are reachable only through pointers, so Ghidra alone misses about 24 %.
- **Cleanup needed:** the repo's function list includes 306 Ghidra `caseD_*` switch-case fragments that should be merged back into their parent functions.
- **Running the repo's disassembler:** the bundled `n3dsdisasm` is a Linux binary, and under colima's emulation it took 44 minutes.

## Phase 4: symbols
- **zeldaret function list:** 4,341 named functions, 2,756 of them actor functions. Actors already have one source file each.
- **OoT3D_Randomizer `oot.ld`:** 442 symbols. 103 are still unnamed `FUN_` upstream; they are listed in `analysis/rando_new_names.tsv`.
- **N64 decomp:** actor logic maps almost one to one.

## Phase 5: pilot
- **Functions:** 18 across ObjRoomtimer, EnEg, ObjMakekinsuta and EnWallTubo, decompiled in the repo's style.
- **Build:** they compile with clang, needing only a one-line shim for `__sqrtf`.
- **Checking with `scripts/difftest.py`:**
  - The clang build is linked at 0x07000000 with external symbols resolved to their original addresses.
  - It runs side by side with the original bytes in unicorn, from identical randomized memory, with all called functions stubbed.
  - It compares the called-function trace (including float and stack arguments) and all writable memory.
  - **Result: 18/18 equal, 1,000 runs each.**
- **3DS-specific differences found:** an extra `Actor_Spawn` argument, timers scaled by `R_UPDATE_RATE`, a Master Quest special case, and En_Eg's static `sVoided` flag moved to PlayState+0x7FA0.
- **Distance from matching:** six functions already have the same instruction sequence; the rest differ in register allocation and literal sharing. Code size is 1,012 B original vs 1,236 B from clang.

## Phase 6: project setup and non-matching build path
- **Layout:** `oot3d/` is the repo with both patches applied. `scripts/regen_all.sh` rebuilds everything from the ROMs, and `scripts/progress.py` is the accurate progress metric.
- A GCC/clang build that runs the same but doesn't match byte for byte looks feasible.
- **Disassembly reassembles:** the GNU-syntax disassembly builds with clang and `ld.lld` to the original `.text` except 13 words. All 13 are conditional `adr` instructions that capstone prints wrongly, and the repo already patches exactly these.
- **Easy variant (functions stay at original addresses):** link clang objects for decompiled functions and the asm for the rest at the original addresses. The output runs in an emulator.
- **Hard variant (code can move):** 12,317 literal-pool words hold raw addresses into rodata/data/bss, and 266 into text. The data sections are raw dumps containing function pointers. All of this needs symbol recovery first.
- **ABI:** calling convention and float passing match; checked in the pilot.
- **Runtime library:** the ARM C runtime (`__aeabi_*`, scatter-load init) has to stay as asm or be reimplemented.
- **libctru** is irrelevant; the game statically links Nintendo's nn:: SDK.

## Phase 7: estimates
Basis: about 10,300 game functions; about 45 % have an N64 counterpart.

| Goal | Estimate |
|---|---|
| (a) Non-matching full decomp | About 900 person-days manually. With an LLM drafting functions plus the automated difftest, about 200–300 person-days |
| (b) Matching decomp | About 2,000–2,700 person-days; needs a license or decomp.me |
| (c) AOT recompilation for visionOS (no JIT) | Prototype 2–3 person-months, robust 4–6 person-months, independent of decomp progress |
| Native port like Ship of Harkinian | (a) complete, plus 1–2 person-years for Metal rendering, audio and SDK services. Not near-term at 0.34 % |

How (c) would work:
- the repo's function list and scatter file give the units to recompile;
- the jump tables become switch statements;
- indirect calls go through a dispatch table keyed by original function address;
- an interpreter handles the 51 computed jumps and 23 unknown targets;
- SVCs go to Azahar's existing HLE.

## Next steps
1. Ask Arm (support case or distributor) about an RVCT 4.0 FlexLM license, then run the setup block above.
2. Until then, validate functions with `difftest.py`, and optionally decomp.me.
3. Possible local contributions: the macOS patch, the 103 randomizer names, the progress-count fix, and the pilot functions.
4. For visionOS, build the AOT recompiler from these outputs.

## Risks
- FlexLM host-ID checks under wibo are untested.
- `md5sum -c` on macOS in the `check` target is untested.
- Estimates are ±50 %.
- The difftest is strong evidence of equivalence, not proof.

## Files
All under `decomp-spike/`:
- `PROGRESS.md`, `REPORT.md`
- `patches/0001-macos-build-support.patch`
- `patches/0002-pilot-decomp-18-functions.patch`
- `oot3d/`, with the macOS shims in `oot3d/tools/macos/`
- `scripts/` (`extract.py`, `aot_stats.py`, `difftest.py`, `progress.py`, `usa_eur_map.py`, `dis.py`, `regen_all.sh`)
- `scripts/ghidra/`
- `pilot/`
- `analysis/` (`aot/`, `ghidra/`, `difftest_pilot.txt`, `rando_new_names.tsv`, `usa_eur_map.txt`, `progress.json`)
- `tools/wibo/wibo-macos`

No commits, no push, nothing uploaded.
