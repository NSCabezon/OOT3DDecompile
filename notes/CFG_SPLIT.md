# cfg split recipe (cfg-merged functions)

## How a function boundary is defined
1. `oot3d/disassembly/oot3d.cfg` `arm_func <addr> <name> force` -> n3dsdisasm -> `baserom.s` -> `gcc_to_arm_asm.py`
   -> one `disassembly/asm/<name>.s` per cfg entry (`AREA |i.<name>|` + `EXPORT <name>`); everything up to the next
   cfg entry lands in that file (that is how unlabeled functions get merged, usually as raw DCB after a literal pool).
2. `.cpp` `GLOBAL_ASM("asm/<name>.s")` -> `tools/preproc.py` writes `build/nonmatch/<cpp>.s` = `GET <disassembly>/<path>`
   (path is relative to `<tree>/disassembly/`, so `../split/asm/X.s` works). CMake asm deps are computed at configure
   time -> touch the .cpp after changing what it GETs.
3. Placement: `data/oot3d.ld` (scatter) pins every section `i.<name>` at its ROM address; `data/keep_symbols.txt`
   `--keep=<name>` stops `armlink --remove` from dropping unreferenced functions. Both are tree-local (copied by mkws).
4. Checking: `analysis/aot/functions.tsv` (addr, name, span) drives funcdiff.py (ws_check/rebuild_check), fastchk.py,
   asmdiff.py, progress.py. Not used by the build. A merged span still compares equal bytes when split -> only the
   reporting granularity changes.

## Split = 
- tail asm as its own AREA `|i.<new>|` + EXPORT, head asm shrunk (tree-local copies under `<tree>/split/asm/`;
  shared `disassembly/asm/<head>.s` untouched so other workspaces still build),
- cpp: `GLOBAL_ASM("../split/asm/<head>.s")` + `GLOBAL_ASM("../split/asm/<new>.s")` (next line),
- scatter region `<new> <addr> { * (i.<new>) }` right after the head's, `--keep=<new>`,
- functions.tsv row split (+ oot3d.cfg arm_func line for a future regen) — shared, optional, harmless.

## Script
```
python3 scripts/cfg_split.py <tree> <head_func> <split_addr> <new_name> [--tsv FUNCTIONS_TSV] [--cfg OOT3D_CFG] [--dry-run]
python3 scripts/cfg_split.py <tree> --reapply [--tsv ..] [--cfg ..]     # replay <tree>/split/splits.tsv in order
```
Idempotent; records each split in `<tree>/split/splits.tsv`. Handles splits mid-DCB, chained splits (split a tail
again), moves EXPORTs of labels that fall in the tail, first tail word emitted as `DCI` so the symbol is typed ARM
Code, refuses cross-half label references. Name the tail with the name the C will use (scatter pins by name;
renaming later = redo). Once the head is C, delete its GLOBAL_ASM line as usual; keep the tail line.

## Proven here (ws/Bg_Spot17_Bakudankabe)
- `BgSpot17Bakudankabe_Update 0x0039F204 FUN_0039f204` + exact C enabled -> ws_check baseline only.
- `ItemInbox_Destroy 0x00213D80 FUN_00213d80` + draft C enabled -> ws_check baseline only (48 B C).
- funcdiff with the split tsv (`tmp/functions.tsv`, 12033 rows): baseline only.

## Applying to the main tree (orchestrator, sequential with merges)
```
python3 scripts/cfg_split.py oot3d <head> <addr> <new> --tsv analysis/aot/functions.tsv --cfg oot3d/disassembly/oot3d.cfg
scripts/rebuild_check.sh            # must be baseline only
```
then merge the actor (merge_ws.py copies the actor cpp, which already has the split GLOBAL_ASM lines).
Files touched: oot3d/split/asm/*.s, oot3d/split/splits.tsv, the cpp holding the head GLOBAL_ASM,
oot3d/data/oot3d.ld, oot3d/data/keep_symbols.txt, analysis/aot/functions.tsv, oot3d/disassembly/oot3d.cfg.
After merging an actor from an OLD workspace (made before the split) run `python3 scripts/cfg_split.py oot3d --reapply`
(its cpp reverts to `asm/<head>.s`; reapply rewrites it). scripts/progress.py regex must also count
`../split/asm/` paths (see report).
