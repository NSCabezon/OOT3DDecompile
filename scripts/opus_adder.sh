#!/bin/sh
# Wait until governor allows a refill, then pop next Opus target and exit.
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike; cd $D
while :; do
  [ -f .stop ] && { echo "STOP flag"; exit 0; }
  case "$(scripts/capacity.sh refill)" in ALLOW*) break;; esac
  sleep 30
done
N=$(head -1 opus_queue.txt); [ -z "$N" ] && { echo "EMPTY"; exit 0; }
sed -i '' '1d' opus_queue.txt; printf '%s\topus\trunning\n' $N >> night_state.tsv
echo "POP $N"; grep "^$N	" opus_targets.tsv | cut -f3
