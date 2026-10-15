#!/bin/sh
# Rebuild code.bin with RVCT b839 via wibo and print per-function diff summary.
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike
cd $D/oot3d
export ARMCC_PATH=$D/tools/rvct839 RVCT40INC=$D/../821/include RVCT40LIB=$D/../821/lib WIBO=$D/tools/wibo/wibo-macos
cmake --build build -t code -j8 > $D/build.log 2>&1 || { grep -iE "error" $D/build.log | head -20; exit 1; }
python3 $D/scripts/funcdiff.py disassembly/baserom/exefs/code.bin build/code.bin $D/analysis/aot/functions.tsv $D/analysis/aot/decompiled_functions.txt
