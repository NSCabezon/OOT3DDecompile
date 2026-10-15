#!/bin/sh
# Night pipeline: merge ws/<A> into oot3d, verify, revert on failure, clean up, commit every 10, pop next actor.
# usage: night_merge.sh <A> ["unmatched,list"]  -> prints MERGED/REVERTED and NEXT=<actor or empty>
# Unmatched functions are recorded in pending_sonnet.tsv and, one row per function, in leftovers.tsv
# (list items may be "Func", "Func(tag)" or "Func:words:tag"; tags: near, far, big, cfg, static, ...).
# STATUS.md is appended to notes/<A>.md (re-opened actors keep earlier notes).
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike
A=$1
U=$2
cd $D
# set night_state.tsv row of actor $1 to state $2 (awk: BSD sed has no \t)
setstate() { awk -v a="$1" -v s="$2" 'BEGIN{FS=OFS="\t"} $1==a{$0=a "\t" s} {print}' night_state.tsv > night_state.tmp && mv night_state.tmp night_state.tsv; }
SNAP=/tmp/nm_snap_$$; rm -rf $SNAP; mkdir -p $SNAP
cp -R oot3d/src/functions $SNAP/functions; cp -R oot3d/include $SNAP/include
[ -d oot3d/src/game/actors/$A ] && cp -R oot3d/src/game/actors/$A $SNAP/actor
python3 scripts/merge_ws.py $A > /tmp/nm_$$.log 2>&1
[ -f oot3d/split/splits.tsv ] && python3 scripts/cfg_split.py oot3d --reapply --tsv analysis/aot/functions.tsv >> /tmp/nm_$$.log 2>&1
grep WARN /tmp/nm_$$.log && echo "MERGE-WARN (C or extra lines outside actor dir?)"
R=$(scripts/rebuild_check.sh)
if echo "$R" | grep -q "^functions differing: 1 / " && echo "$R" | grep -q "non-function bytes differing: 0"; then
  echo "MERGED $A"; setstate "$A" "done\tmerged"
  [ -f ws/$A/STATUS.md ] && { printf '\n<!-- merge %s -->\n' "$(date '+%F %T')"; cat ws/$A/STATUS.md; } >> notes/$A.md
  if [ -n "$U" ] && [ "$U" != "none" ]; then
    printf "%s\t%s\t%s\n" "$A" "$U" "$(date +%F)" >> pending_sonnet.tsv
    python3 -P scripts/leftovers.py --record "$A" "$U"
  fi
  rm -rf ws/$A
  n=$(grep -c "merged$" night_state.tsv)
  if [ $((n % 10)) -eq 0 ]; then
    (cd oot3d && git add -A src include data split && git commit -q -m "Decompile night batch: $n actors merged

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FFwXtKGkAFkBREH5VexMyQ" && echo "COMMITTED at $n")
  fi
else
  echo "REVERTED $A — check failed:"; echo "$R" | tail -5; cp build.log build_fail_$A.log; grep -E "Error:|error:" build.log | head -8
  # restore pre-merge snapshot (NOT git HEAD: that would undo other uncommitted merges)
  rm -rf oot3d/src/functions oot3d/include oot3d/src/game/actors/$A
  cp -R $SNAP/functions oot3d/src/functions; cp -R $SNAP/include oot3d/include; cp -R $SNAP/actor oot3d/src/game/actors/$A
  sed -i '' '$d' merged.txt
  setstate "$A" "failed\treverted"
  scripts/rebuild_check.sh | tail -2
fi
[ -f .stop ] && { echo "NEXT= (stop)"; exit 0; }
RUN=$(awk -F"\t" 'NR>1 && $3=="running"' night_state.tsv | wc -l | tr -d " ")
[ -f .no_pop ] && { echo "NEXT= (no_pop)"; exit 0; }
C=$(scripts/capacity.sh refill); case "$C" in HOLD*) echo "NEXT= ($C)"; exit 0;; esac
N=$(head -1 queue.txt); [ -n "$N" ] && sed -i '' '1d' queue.txt && printf '%s\thaiku\trunning\n' $N >> night_state.tsv
echo "NEXT=$N"
