#!/bin/sh
# Rebuild workspace ws/<name> and print per-function diff. Usage: ws_check.sh <name> [function-name-filter-regex]
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike
W=$D/ws/$1
cd $W
export ARMCC_PATH=$D/tools/rvct839 RVCT40INC=$D/../821/include RVCT40LIB=$D/../821/lib WIBO=$D/tools/wibo/wibo-macos
cmake --build build -t code -j4 > build.log 2>&1 || { grep -E "Error|error" build.log | grep -v "parsing restarts" | head -30; exit 1; }
python3 $D/scripts/funcdiff.py disassembly/baserom/exefs/code.bin build/code.bin $D/analysis/aot/functions.tsv
