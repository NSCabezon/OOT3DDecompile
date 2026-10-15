#!/bin/sh
# Opus phase: merge ws/<A>; update pending; pop next from opus_queue.txt (governor permitting).
# usage: opus_merge.sh <A> "<UNMATCHED or none>"
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike; cd $D
A=$1; U=$2
sed -i '' "/^$A\t/d" pending_sonnet.tsv
sed -i '' "s/^$A\topus\trunning$/$A\topus\trunning/" night_state.tsv
scripts/night_merge.sh $A "$U" | head -3
grep -q "^$A	done	merged" night_state.tsv || { echo "NOT MERGED (see above)"; }
C=$(scripts/capacity.sh refill); case "$C" in HOLD*) echo "OPUS_NEXT= ($C)"; exit 0;; esac
N=$(head -1 opus_queue.txt); [ -z "$N" ] && { echo "OPUS_NEXT= (empty)"; exit 0; }
sed -i '' '1d' opus_queue.txt; printf '%s\topus\trunning\n' $N >> night_state.tsv
echo "OPUS_NEXT=$N"; grep "^$N	" opus_targets.tsv | cut -f3
