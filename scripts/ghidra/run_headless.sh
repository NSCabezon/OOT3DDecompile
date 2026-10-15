#!/bin/sh
# Import code.bin (USA) into Ghidra headless with the exheader segment layout, auto-analyse, export functions.
D=$(cd "$(dirname "$0")/../.." && pwd)
G="$D/tools/ghidra_dl/ghidra_12.1.4_PUBLIC"
mkdir -p "$D/analysis/ghidra/proj"
exec "$G/support/analyzeHeadless" "$D/analysis/ghidra/proj" oot3d_usa \
  -import "$D/extract/usa/code.bin" -overwrite \
  -loader BinaryLoader -loader-baseAddr 0x00100000 -processor ARM:LE:32:v6 \
  -scriptPath "$D/scripts/ghidra" -postScript ExportFuncs.java "$D/analysis/ghidra/functions_ghidra.tsv" \
  -max-cpu 6
