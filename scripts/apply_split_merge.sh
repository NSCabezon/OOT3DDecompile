#!/bin/sh
# usage: apply_split_merge.sh <Actor> "<leftovers>" HEAD ADDR NEW [HEAD ADDR NEW ...]
# Applies cfg splits to the MAIN tree (under .tree.lock, --tsv), then night_merge.sh <Actor>.
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike; cd $D
A=$1; U=$2; shift 2
until mkdir $D/.tree.lock 2>/dev/null; do sleep 3; done
while [ $# -ge 3 ]; do
  python3 -P scripts/cfg_split.py oot3d $1 $2 $3 --tsv analysis/aot/functions.tsv | tail -1
  echo "$A $1 $2 $3" >> logs/cfgsweep_splits.txt
  shift 3
done
rmdir $D/.tree.lock
scripts/night_merge.sh $A "$U"
