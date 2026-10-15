#!/bin/sh
# Create an isolated workspace ws/<name>: copy of oot3d (src/include/library/data/tools) with the
# 638 MB disassembly/ symlinked, plus its own build dir. Usage: mkws.sh <name>
set -e
D=/Users/nscabezon/Apps/OOT3DDecompile/decomp-spike
W=$D/ws/$1
mkdir -p $W
# serialize with merges into oot3d/ (scripts/merge_ws.py takes the same lock)
until mkdir $D/.tree.lock 2>/dev/null; do sleep 2; done
trap 'rmdir $D/.tree.lock' EXIT
rsync -a --exclude build --exclude disassembly --exclude .git $D/oot3d/ $W/
mkdir -p $W/disassembly
for f in $D/oot3d/disassembly/*; do ln -sfn "$f" "$W/disassembly/$(basename $f)"; done
rm -f $W/disassembly/CMakeLists.txt && cp $D/oot3d/disassembly/CMakeLists.txt $W/disassembly/
# freeze data chunks: private copies of {data,rodata}_chunks.txt and per-file symlinks in data/ so a later
# chunk split/regen in main (pin_static.py) can't shift this ws's layout under its own oot3d.ld
.venv/bin/python -P -c "import sys; sys.path.insert(0, '$D/scripts'); import pin_static as p; p.materialise('$W')" > /dev/null
for f in $D/oot3d/disassembly/data/*.s; do b=$(basename $f); [ -L $W/disassembly/data/$b ] && { rm $W/disassembly/data/$b; cp $f $W/disassembly/data/$b; }; done
rmdir $D/.tree.lock; trap - EXIT
cd $W
export ARMCC_PATH=$D/tools/rvct839 RVCT40INC=$D/../821/include RVCT40LIB=$D/../821/lib WIBO=$D/tools/wibo/wibo-macos
cmake -B build -S . > build-configure.log 2>&1
cmake --build build -t code -j4 > build.log 2>&1
echo "workspace ready: $W"
