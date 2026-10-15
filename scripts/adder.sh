#!/bin/sh
# Wait until the governor allows adding one agent, then pop 1 actor and exit (orchestrator launches it).
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike; cd $D
while :; do
  [ -f .stop ] && { echo "STOP flag"; exit 0; }
  case "$(scripts/capacity.sh add)" in ALLOW*) break;; esac
  sleep 60
done
N=$(head -1 queue.txt); [ -z "$N" ] && { echo "QUEUE EMPTY"; exit 0; }
date +%s > .last_add; sed -i '' '1d' queue.txt; printf '%s\thaiku\trunning\n' $N >> night_state.tsv
echo "POP $N $(uptime | awk -F'load averages: ' '{print $2}')"
