#!/bin/sh
# Regenerate every ROM-derived artifact of the spike from the two .3ds images (macOS, Apple Silicon).
# Idempotent; slow step = n3dsdisasm under linux/amd64 emulation (skip with SKIP_DISASM=1).
set -e
D=$(cd "$(dirname "$0")/.." && pwd)
TOP=$(cd "$D/.." && pwd)
USA="$TOP/Legend of Zelda, The - Ocarina of Time 3D (USA) (En,Fr,Es).3ds"
EUR="$TOP/Legend of Zelda, The - Ocarina of Time 3D (Europe) (En,Fr,De,Es,It) (Rev 1).3ds"
PY="$D/.venv/bin/python"
[ -x "$PY" ] || { python3 -m venv "$D/.venv"; "$D/.venv/bin/pip" install -q capstone unicorn; }

echo "== 1. extraction"
python3 -I "$D/scripts/extract.py" "$USA" "$D/extract/usa" >/dev/null
python3 -I "$D/scripts/extract.py" "$EUR" "$D/extract/eur" >/dev/null
strings -n 6 "$D/extract/usa/code.bin" > "$D/analysis/strings_usa.txt"

echo "== 2. zeldaret/oot3d baserom + disassembly pipeline (macOS shims)"
cd "$D/oot3d/disassembly"
[ -f baserom.3ds ] || cp -c "$USA" baserom.3ds
python3 -I ../tools/macos/ctrtool --exefsdir=baserom/exefs --exheader=baserom/exheader.bin \
    --plainrgn=baserom/plainrgn.bin baserom.3ds
if [ -z "$SKIP_DISASM" ] && [ ! -s baserom/baserom_before_fixes.s ]; then
    ../tools/macos/n3dsdisasm -c oot3d.cfg baserom/exefs/code.bin > baserom/baserom_before_fixes.s
fi
if [ -s baserom/baserom_before_fixes.s ]; then
    python3 -I tools/baserom_fixes.py baserom/baserom_before_fixes.s baserom/baserom.s
    python3 -I tools/gcc_to_arm_asm.py baserom/baserom.s asm
    python3 -I tools/split_arm_data_chunks.py
    touch split_asm.txt
fi
cd "$D"

echo "== 3. static stats for AOT + USA/EUR map"
"$PY" -I scripts/aot_stats.py extract/usa/code.bin oot3d/disassembly/oot3d.cfg analysis/aot > analysis/aot/aot_stats_stdout.json
python3 -I scripts/usa_eur_map.py extract/usa/code.bin extract/eur/code.bin oot3d/disassembly/oot3d.cfg > analysis/usa_eur_map.txt

echo "== 4. progress"
python3 -I scripts/progress.py oot3d analysis/aot/functions.tsv | tee analysis/progress.json

echo "== 5. pilot build + differential test"
sh pilot/build.sh
"$PY" -I scripts/difftest.py extract/usa/code.bin oot3d/disassembly/oot3d.cfg pilot/pilot.elf "${TRIALS:-300}" \
    | tee analysis/difftest_pilot.txt
