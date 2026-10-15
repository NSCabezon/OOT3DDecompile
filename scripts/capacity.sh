#!/bin/sh
# Load/thermal governor for the night run (M1 Max, 10 cores).
# usage: capacity.sh add|refill  -> prints ALLOW or HOLD <reason>
#   add:    may we add ONE extra agent? (cool + 5 min since last launch)
#   refill: may we replace a finished agent? (not hot)
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike
MAX=14
RUN=$(awk -F'\t' 'NR>1 && $3=="running"' $D/night_state.tsv | wc -l | tr -d ' ')
L=$(uptime | awk -F'load averages: ' '{print $2}' | tr ',' '.')
L1=$(echo $L | awk '{print int($1)}'); L5=$(echo $L | awk '{print int($2)}')
T=$(pmset -g therm 2>/dev/null | grep -v "^Note" | grep -iE "warning|limit" | head -1)
[ -n "$T" ] && { echo "HOLD thermal: $T"; exit 0; }
[ "$RUN" -ge $MAX ] && { echo "HOLD max $MAX (running $RUN)"; exit 0; }
if [ "$1" = refill ]; then
  [ "$L1" -gt 30 ] && { echo "HOLD hot load1=$L1 (shrinking, running $RUN)"; exit 0; }
  echo "ALLOW refill load1=$L1 running $RUN"; exit 0
fi
LAST=$(cat $D/.last_add 2>/dev/null || echo 0); AGE=$(( $(date +%s) - LAST ))
[ "$AGE" -lt 300 ] && { echo "HOLD last launch ${AGE}s ago"; exit 0; }
[ "$L1" -ge 12 ] && { echo "HOLD load1=$L1"; exit 0; }
[ "$L5" -ge 15 ] && { echo "HOLD load5=$L5"; exit 0; }
echo "ALLOW add load1=$L1 load5=$L5 running $RUN"
