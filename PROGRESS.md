# OoT3D decomp spike — progress log

Rules: local only, no push/upload. ROM-derived data stays in decomp-spike/ (gitignored where tracked).

## 2026-10-12 ~20:00 — Phase 1 (extraction) DONE

Own pure-python extractor: `scripts/extract.py` (NCSD -> NCCH -> exheader/ExeFS/BLZ/RomFS listing).
Outputs: `extract/{usa,eur}/{code.bin,exheader.bin,info.json,romfs_listing.tsv,exefs/}`.

| | USA (AQEE rev0) | EUR (AQEP rev1) |
|---|---|---|
| code.bin (decompressed, BLZ flag set) | 4,567,040 B | 4,567,040 B |
| .text @0x00100000 | 0x3C99A8 (3,971,496 B, 970 pages) | identical size |
| .rodata @0x004CA000 | 189,256 B (47 pages) | identical |
| .data @0x004F9000 | 397,856 B (98 pages) | identical |
| .bss | 443,368 B | identical |
| RomFS | 1,944 files, 469.7 MB | 1,974 files, 475.3 MB |

- NCCH plain region: `CTR_SDK-1_2_0_200_none`, `Firmware-02_27`, Mobiclip Deblocker 1.0.3 / MobiclipDec 1.0.1 / MoflexDemuxer 1.0.2.
- **No .cro/.crs/.crr in RomFS** -> all game code lives in code.bin (actors statically linked, no overlays).
- USA vs EUR: rodata 47 words differ, data 66 words; text 14% of words differ only because of a
  +0x24/+0x20 shift after 0x419E18 (language-fetch function) — matches OoT3D_Randomizer's
  `address_conversion_info.txt`. => symbol porting USA->EUR is a trivial offset map.
- Strings: 49 unique `d:\home\queen\dailyBuild\game_us\sources\*.cpp` / `libraries\gzw\*.cpp` paths
  (assert __FILE__), codename "queen", engine lib "gzw". No compiler banner strings in code.bin.
- exheader services include debug `$hioFIO`, `$hostio0/1` (left from dev build config).

## 2026-10-12 ~20:05 — REDIRECT from coordinator

An existing public **matching** decomp exists: github.com/zeldaret/oot3d (CC0, USA, RVCT 4.0 b821).
Plan changed: leverage it instead of rebuilding from scratch. Cloned to `oot3d/` (+ submodules
`library/3ds_sdk`, `tools/asm-differ` via https). Earlier planned Ghidra/symbol phases are reduced to
what adds value beyond the repo (AOT stats, USA/EUR diff, pilot functions, estimates).

## 2026-10-12 ~20:40 — zeldaret/oot3d on macOS, AOT stats, pilot (in progress)

- `oot3d/` = zeldaret/oot3d @ a87ddae (2026-09-04). Submodules fetched via https (`library/3ds_sdk`, `tools/asm-differ`).
  `disassembly/baserom.3ds` = APFS clone (`cp -c`) of the USA ROM (no extra disk, original untouched).
- Repo facts: 12,031 functions in `disassembly/oot3d.cfg` (4,341 non-`FUN_` names), scatter file `data/oot3d.ld`
  pins **every function to its original address** (one `i.<Func>` section each). 494 .cpp, 12,254 `GLOBAL_ASM` refs;
  only ~25 source files contain any real C bodies -> project is at a very early stage.
- Bundled `ctrtool` / `n3dsdisasm` are Linux/Windows x86-64 binaries. Wrote macOS shims in `oot3d/tools/macos/`:
  `ctrtool` (pure python; outputs byte-identical to the real ctrtool, verified) and `n3dsdisasm` (runs the Linux
  binary in a linux/amd64 docker container; colima uses QEMU user-mode -> slow, still running >30 min).
- CMake patched: `WIBO` env -> generates `build/armwrap/{armcc,armasm,armlink,armar,fromelf}` wrappers that exec
  `$WIBO $ARMCC_PATH/win_32-pentium/<tool>.exe`; `python` -> `python3`; APPLE -> shims. progress.py posix fix.
- wibo 1.2.0 `wibo-macos` (x86_64, Rosetta 2) downloaded to `tools/wibo/`; verified with a self-built 32-bit PE
  (clang+lld-link, no third-party binary): runs, args + exit code OK, 0.04 s.
- AOT stats (`scripts/aot_stats.py`, `analysis/aot/`): 100% ARM (0 Thumb funcs), 885k insns decoded, 52.8k direct
  calls, 1,818 indirect calls (blx reg), 316 `bx reg` non-return jumps, 420 jump tables (`ldrls pc,[pc,rN,lsl#2]`,
  5,656 entries, 10 unbounded), 325 svc sites. Median function 144 B, p90 744 B, max 24.5 KB.
- Pilot: 18 functions (ObjRoomtimer x5, EnEg x5, ObjMakekinsuta x4, EnWallTubo x4) decompiled in repo style;
  compiles with clang (`pilot/build.sh`, needs only `-include pilot/clang_shim.h` for `__sqrtf`);
  **differential test in unicorn vs original bytes: 18/18 equal over 1000 randomized trials each**
  (`scripts/difftest.py`, `analysis/difftest_pilot.txt`).

## 2026-10-12 ~20:50 — disassembly pipeline done, compiler wired, reassembly experiment

- n3dsdisasm (Linux x86-64 under colima QEMU user-mode): **44 min**, 984,525 lines, 12,031 functions.
  baserom_fixes / gcc_to_arm_asm / split_arm_data_chunks (python3, unchanged): 11,962 `asm/*.s` + 418 `data/*.s`.
  preproc.py for all 494 .cpp -> build/nonmatch OK.
- User-supplied RVCT 4.0 b821 (Windows pkg) runs under wibo-macos; `--vsn` OK for armcc/armasm/armlink/armar/fromelf,
  but **armcc, armasm, armlink and fromelf all require FlexLM features** (compiler/bsp_compiler, armasm, armlink,
  fromelf, version >= 4.0). Build blocked only on a license; not bypassed.
- CMake (`WIBO` env) now configures cleanly on macOS: Generic system (no `-arch arm64`), `.o` objects,
  armlink/armar rules mirrored from CMake's ARMCC module via `tools/macos/rules_override.cmake`.
  A real compile is attempted and stops at C9932E (license) -> wiring verified.
- Progress, precise: 143 functions / 13,480 B = **0.34 %** of .text in C (incl. my 18 pilot functions;
  upstream before pilot: 125). Upstream `tools/progress.py` prints 3.3 % because its line-based asm size
  ignores labelled `DCD` literal-pool lines -> overstates.
- Reassembly experiment: n3dsdisasm GNU-syntax output + 8-line macro prelude assembles with **clang** with 0 errors;
  ld.lld at 0x100000 -> .text identical to original except **13 words** (all capstone printing conditional
  `add<cc> rX, pc, #imm` without the condition — the same 13 cases gcc_to_arm_asm.py hard-codes) + 0x1F0-byte
  .ARM.exidx tail. => a GNU/LLVM non-matching build path is viable. Literal pools: 12,317 numeric pointers into
  rodata/data/bss + 266 into text are NOT symbolized (blocker for a shiftable build), 5,679 symbolic.
- Ghidra 12.1.4 headless (raw import @0x100000, ARM v6 LE, no native decompiler on mac_arm_64): 9,153 functions,
  9,119 shared with cfg, 34 Ghidra-only (all mid-function), 2,912 cfg-only (pointer-only reachable functions).
- cfg contains 306 Ghidra `caseD_*` pseudo-functions (switch-case fragments split off as functions).
- OoT3D_Randomizer oot.ld: 442 symbols; 363 at cfg function starts, 103 of them still `FUN_` in the repo
  (`analysis/rando_new_names.tsv`), 62 data symbols.
- USA vs EUR Rev1: 11,994/12,031 functions identical modulo relocation with the randomizer's offset map; 36 differ.

## 2026-10-12 ~22:10 — matching build working on macOS (RVCT 4.0 b839)

- User-supplied toolchain in `../821/` (bin/include/lib). Despite the folder name, every tool reports
  **RVCT4.0 [Build 839]** and runs without a FlexLM license. Hooked up via symlink `tools/rvct839/win_32-pentium -> ../../../821/bin`.
- Two wibo fixes needed:
  - `--multibyte-chars --locale=japanese` fails under wibo (`#869`). Under `WIBO` those flags are now dropped
    (root `CMakeLists.txt` + `library/CMakeLists.txt`). All sources are ASCII, so codegen is unchanged.
  - Embedded `__asm` functions make armcc run `%COMSPEC% /c armasm.exe ...`. Added a 2.5 KB PE `cmd.exe`
    (`oot3d/tools/macos/cmdshim/`, built with clang+lld-link) and put it on the wrapper's PATH (`armwrap.sh.in`).
- **Result:** full build links; `code.bin` differs from the original in **1 function out of 12,031**:
  `FUN_00249af8` (my EnEg pilot), 4 words, which is `mov r5, r1` scheduled 3 instructions early.
  All upstream C functions match, and so do 17 of 18 pilot functions. 12 source variants tried with no change;
  it may be a b821-vs-b839 scheduling difference. Left as-is.
- Loop: `scripts/rebuild_check.sh` rebuilds and runs `scripts/funcdiff.py`, which reports which functions differ.
  `scripts/asmdiff.py <name>` shows a side-by-side disassembly; run it with `.venv/bin/python -P` because local
  `scripts/dis.py` shadows the stdlib `dis` module.

## 2026-10-12 ~late — first parallel batches (24 actors) + model A/B

- 24 actors merged into `oot3d/` (see `merged.txt`). The build check shows only the baseline (`FUN_00249af8`).
- Progress (`scripts/progress.py`): **316 functions / 37,748 B in C = 0.95 % of .text** (2.63 % of functions), up from 143 functions / 0.34 %.
- A/B on 4 actors (`ab_results.tsv`):

  | Model | Functions matched | Tokens | Time |
  |---|---|---|---|
  | Sonnet 5.5 | 22/22 | 323k | 46 min |
  | Haiku 5.5 | 19/21 | 495k | 65 min |

  At current list prices, Haiku costs about 7–8 % of Sonnet even with the extra tokens.
- Not matched (left as asm or `NON_MATCHING`): `Actor1DA_Init`, `FUN_0015b3cc` (Bg_Mjin), `FUN_003e68c4` (Bg_Bom_Guard), `FUN_003bc5dc` (Obj_Mure). All are register-allocation or scheduling diffs.
- Tech debt lives in `CLAUDE.md`: raw-address references in Obj_Mure3, Demo_Geff, Demo_Ec and En_Bird; the `gWeatherMode` EQU; `functions.tsv` merging separate functions.

## 2026-10-13 night run (23:00 → 07:30)
- 0.95 % → **2.93 %** of .text in C (316 → 890 functions). Details in `NIGHT.md`, learned tricks in `CLAUDE.md`.

## 2026-10-14 (day: cfg sweep → lote 4 groups → recipe sweeps → static infra)
- 4.85 % (17:00 on 10-13) → 6.78 % (lotes 1–3) → **8.68 %** of .text in C (1230 → 1928 fns).
- cfg sweep: ~60 splits in ~20 actors (`scripts/apply_split_merge.sh`, `detect_cfg.py`).
- Lote 4 = 16 group lanes (Haiku small fns → Sonnet rest) + recipe sweeps: GetCMAB alias (4/12), near-miss generator (10/14, 3/11), guarded statics infra `scripts/pin_static.py` (18/32 + MTX34Identity; removed the two trimmed data copies).
- Researched and ruled out ~30 float shapes for the integer-store identity+translate MTX34 (= inlined FUN_003713fc); only a u32 word copy matches — pending user decision.
- Known: metric inflated ~0.45 pt (83 fns without C definition); debt in EQU symbols/raw offsets/prototype casts.

## 2026-10-15 (night+morning: lote 5 groups G13–G30, recipes, infra)
- 8.23 % (corrected metric) → **9.51 %** of .text in C (1845 → 2128 fns). Metric fixed (progress.py requires a C definition).
- Tech-debt pass (shared_syms.s, 75 EQUs → real data, 158 casts removed, variadic prototypes), MakeTrans helper + FUN_003713fc in C, guarded-static pins via pin_static.py (En_Ta, En_Fu, Bdan_Switch, En_Mm…), first cfg JOIN (En_Md).
- Incidents: 8 h lock deadlock (merge_ws inside my own lock), ws drift after main chunk regen (mkws now freezes data), regex damage on 3 merged files (hand-repaired). All recorded in CLAUDE.md.
- MTX34_MakeScale accepted as exception (same as MakeTrans), user 2026-10-15; listed in CLAUDE.md Tech debt → Accepted exceptions for a future clean rewrite.

## 2026-10-15 (afternoon: R9 MakeScale, R10/R11 near-miss sweeps)
- 9.51 % → **9.62 %** (2128 → 2141 fns). Near-miss sweeps 13/29 matched. MakeScale helper added (0 matches: zero-rematerialisation regalloc blocker). Queue groups PAUSED by user; tree at baseline, no ws left (except En_Jsjutan).
