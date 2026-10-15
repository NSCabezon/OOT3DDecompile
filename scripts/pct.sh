#!/bin/sh
# Quick progress: % of .text in C (main tree oot3d/). usage: scripts/pct.sh
D=$(cd "$(dirname "$0")/.." && pwd)
python3 "$D/scripts/progress.py" "$D/oot3d" "$D/analysis/aot/functions.tsv" | python3 -c '
import json,sys; d=json.load(sys.stdin)
print("%.3f %% .text en C (%d B) · %d/%d funciones (%.2f %%)" % (d["pct_bytes_in_c"], d["bytes_in_c"], d["functions_in_c"], d["functions"], d["pct_functions_in_c"]))'
