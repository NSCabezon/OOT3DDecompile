#!/bin/sh
# One-off serial merge of the pending workspaces after the lock deadlock (2026-10-15).
# Step 1 merges En_Ta + En_Fu together (their static pins are already in main, so each alone fails the check).
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike
cd $D
setstate() { awk -v a="$1" -v s="$2" 'BEGIN{FS=OFS="\t"} $1==a{$0=a "\t" s} {print}' night_state.tsv > night_state.tmp && mv night_state.tmp night_state.tsv; }
book() { # A leftovers
  A=$1; U=$2
  setstate "$A" "done\tmerged"
  [ -f ws/$A/STATUS.md ] && { printf '\n<!-- merge %s -->\n' "$(date '+%F %T')"; cat ws/$A/STATUS.md; } >> notes/$A.md
  if [ -n "$U" ] && [ "$U" != "none" ]; then
    printf "%s\t%s\t%s\n" "$A" "$U" "$(date +%F)" >> pending_sonnet.tsv
    python3 -P scripts/leftovers.py --record "$A" "$U"
  fi
  rm -rf ws/$A
}
echo "== step 1: En_Ta + En_Fu"
python3 scripts/merge_ws.py En_Ta | grep -v '^merged'
python3 scripts/merge_ws.py En_Fu | grep -v '^merged'
python3 scripts/cfg_split.py oot3d --reapply --tsv analysis/aot/functions.tsv > /dev/null 2>&1
until mkdir .tree.lock 2>/dev/null; do sleep 2; done
R=$(scripts/rebuild_check.sh); rmdir .tree.lock
echo "$R" | grep -E "functions differing|non-function"
if echo "$R" | grep -q "^functions differing: 1 / " && echo "$R" | grep -q "non-function bytes differing: 0"; then
  echo "MERGED En_Ta+En_Fu"
  book En_Ta "EnTa_Init:91:far literal pool dumped mid-function (layout)"
  book En_Fu "EnFu_Draw:8:near face ptr from incoming r0 + base from r4 (60 variants),EnFu_Update:4:near strb off incoming r0 (35 variants)"
else
  echo "FAILED En_Ta+En_Fu — stopping"; echo "$R" | tail -5; grep -E "Error:" build.log | grep -v "0 errors" | head -5; exit 1
fi
echo "== step 2: G25"
echo "Bg_Spot06_Objects: $(scripts/night_merge.sh Bg_Spot06_Objects 'BgSpot06Objects_Init:306:far' | grep -E 'MERGED|REVERTED')"
echo "En_River_Sound: $(scripts/night_merge.sh En_River_Sound 'FUN_00404b20:3:near,FUN_002549b4:9:near,FUN_00323378:far ROM keeps 0 in r7 / 3 in r8 + VFP reversed' | grep -E 'MERGED|REVERTED')"
echo "== step 3: G26"
scripts/apply_split_merge.sh En_Dns "EnDns_Update:3:near textId store reg,FUN_0027f3f8:10:static DAT_00520234 derived from DAT_00520238 (En_Horse externs),EnDns_ChangeAnim:28:static guard 0x522330/obj 0x5223BC relative to sAnimPtrs 0x522324 (all TU statics in C)" FUN_001616f0 0x0016178C FUN_0016178c > logs/merge_En_Dns.log 2>&1
echo "En_Dns: $(grep -E 'MERGED|REVERTED' logs/merge_En_Dns.log)"
cp ws/En_Fhg_Fire/src/game/shared_syms.s oot3d/src/game/shared_syms.s
echo "En_Fhg_Fire: $(scripts/night_merge.sh En_Fhg_Fire 'FUN_003ddcc0:2:near,EnFhgFire_Draw:13:near,FUN_0019fe84:186:big' | grep -E 'MERGED|REVERTED')"
S=/private/tmp/claude-501/-Users-nscabezon-Apps-OOT3DDecompile/380d8f01-c0c4-4376-a388-1335aca69b99/scratchpad/dnt_demo_bak; mkdir -p $S; cp oot3d/data/oot3d.ld oot3d/disassembly/data_chunks.txt $S/
python3 - <<'EOF'
import re
p="oot3d/data/oot3d.ld"; s=open(p).read(); n=len(s)
s=re.sub(r"\n    z_En_Dnt_Demo_ASM\.data \+0\n    \{\n        \*\(i\.z_En_Dnt_Demo\.data\)\n    \}", "", s); print("ld removed", n-len(s)); open(p,"w").write(s)
p="oot3d/disassembly/data_chunks.txt"; t=open(p).read(); t2=t.replace("z_En_Dnt_Demo.data,005224B0,00522598\n",""); print("chunk removed", t!=t2); open(p,"w").write(t2)
EOF
R=$(scripts/night_merge.sh En_Dnt_Demo none | grep -E 'MERGED|REVERTED'); echo "En_Dnt_Demo: $R"
case "$R" in REVERTED*) cp $S/oot3d.ld oot3d/data/oot3d.ld; cp $S/data_chunks.txt oot3d/disassembly/data_chunks.txt; echo "restored ld/chunks from backup";; esac
for A in Bg_Spot06_Objects En_River_Sound En_Dns En_Fhg_Fire En_Dnt_Demo; do [ -f build_fail_$A.log ] && { echo "-- $A"; grep -E "Error:" build_fail_$A.log | grep -v "0 errors" | head -3; }; done
scripts/pct.sh | tail -1
