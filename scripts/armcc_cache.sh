#!/bin/sh
# Content-addressed object cache in front of armcc (RVCT 4.0 b839 via wibo). Opt-in: active only when
# ARMCC_CACHE_DIR is set; oot3d/tools/macos/armwrap.sh.in execs this script in that case.
#
#   armcc_cache.sh <armwrap-armcc> <armcc args...>   # compile through the cache
#   armcc_cache.sh --stamp <tree-root>               # print the tree's include stamp (see below)
#
# Key = sha256( stamp, sha256(source bytes), argv with the tree root rewritten to "@T" ), so
# ws/<name> and oot3d/ hit the same entry. The stamp = sha256 over the contents of every *.h/*.hpp/...
# under include/, library/3ds_sdk/include/, src/, library/3ds_sdk/src/ (sorted, relative paths), plus
# cmdshim/cmd.exe, the RVCT include dir listing (size+mtime) and armcc/armasm/wibo size+mtime.
# Drivers (mkws.sh, rebuild_check.sh) compute it once per build and export ARMCC_CACHE_STAMP, so a
# compile call costs ~10 ms; without it each call recomputes the stamp (~40 ms, still correct).
#
# Only "-c one-source -o obj" compiles are cached; the only output armcc produces here is the .o
# (Makefiles generator, no --depend/--list). Entries: $ARMCC_CACHE_DIR/<key>.o (+ .log with armcc's
# output if non-empty, .src with the source path). Written to a temp name then renamed, so concurrent
# builds are safe. Failures are never cached. $ARMCC_CACHE_DIR/log records HIT/MISS per call.
# Clear with: rm -rf decomp-spike/.armcc_cache

stamp() {
    cd "$1" || exit 1
    dirs=
    for d in include library/3ds_sdk/include src library/3ds_sdk/src; do
        [ -d "$d" ] && dirs="$dirs $d"
    done
    {
        # shellcheck disable=SC2086
        find $dirs -type f \( -name '*.h' -o -name '*.hpp' -o -name '*.hh' -o -name '*.inc' -o -name '*.inl' -o -name '*.def' \) -print0 \
            | LC_ALL=C sort -z | xargs -0 sha256sum
        [ -f tools/macos/cmdshim/cmd.exe ] && sha256sum tools/macos/cmdshim/cmd.exe
        echo "RVCT40INC=$RVCT40INC RVCT40LIB=$RVCT40LIB"
        [ -d "$RVCT40INC" ] && ( cd "$RVCT40INC" && find . -type f -exec stat -L -f '%N %z %m' {} + | LC_ALL=C sort )
        stat -L -f '%z %m' "$ARMCC_PATH/win_32-pentium/armcc.exe" "$ARMCC_PATH/win_32-pentium/armasm.exe" "$WIBO" 2>/dev/null
    } | sha256sum | cut -c1-64
}

# Key material: version, stamp, source hash, argv with the tree root rewritten to @T.
keymat() {
    printf 'armcc-cache-v1\n%s\n%s\n' "$STAMP" "$srchash"
    for a in "$@"; do
        case $a in
            "$ROOT"/*)   r=${a#"$ROOT"};   printf '@T%s\n' "$r" ;;
            -I"$ROOT"/*) r=${a#-I"$ROOT"}; printf -- '-I@T%s\n' "$r" ;;
            *)           printf '%s\n' "$a" ;;
        esac
    done
}

if [ "$1" = "--stamp" ]; then
    stamp "$2"
    exit $?
fi

CC=$1; shift
C=$ARMCC_CACHE_DIR
# Run the real compiler uncached. ARMCC_CACHE_DIR must be cleared: $CC is armwrap, which would
# otherwise exec this script again.
passthru() { ARMCC_CACHE_DIR=; export ARMCC_CACHE_DIR; exec "$CC" "$@"; }
[ -n "$C" ] || passthru "$@"

# Parse: need "-c", exactly one positional source, "-o <obj>"; bypass anything exotic.
src= out= cflag= prev= bypass=
for a in "$@"; do
    case $prev in
        -o) out=$a; prev=; continue ;;
    esac
    case $a in
        -c) cflag=1 ;;
        -o) prev=-o ;;
        -E|-S|-M|--asm|--list|--interleave|--depend*|--md|--via*|--preinclude*|--list_dir*|--asm_dir*) bypass=1 ;;
        -*) ;;
        *) if [ -n "$src" ]; then bypass=1; else src=$a; fi ;;
    esac
done
case $src in *.cpp|*.c|*.cc) ;; *) bypass=1 ;; esac
[ -n "$cflag" ] && [ -n "$out" ] && [ -z "$bypass" ] && [ -f "$src" ] || passthru "$@"

# Tree root from the source path (library/3ds_sdk/src/ first: it also contains "/src/").
case $src in
    */library/3ds_sdk/src/*) ROOT=${src%/library/3ds_sdk/src/*} ;;
    */src/*)                 ROOT=${src%/src/*} ;;
    */data/*)                ROOT=${src%/data/*} ;;
    *)                       passthru "$@" ;;
esac
[ -d "$ROOT/include" ] || passthru "$@"

STAMP=$ARMCC_CACHE_STAMP
[ -n "$STAMP" ] || STAMP=$("$0" --stamp "$ROOT")

srchash=$(sha256sum < "$src" | cut -c1-64)
key=$(keymat "$@" | sha256sum | cut -c1-64)
rel=@T${src#"$ROOT"}

if [ -f "$C/$key.o" ] && cp -f "$C/$key.o" "$out" 2>/dev/null; then
    [ -f "$C/$key.log" ] && cat "$C/$key.log"
    echo "HIT $key $rel" >> "$C/log"
    exit 0
fi

mkdir -p "$C"
tmp=$C/tmp.$key.$$
ARMCC_CACHE_DIR= "$CC" "$@" > "$tmp.out" 2> "$tmp.err"
rc=$?
cat "$tmp.out"; cat "$tmp.err" >&2
if [ $rc -eq 0 ] && [ -f "$out" ]; then
    cp "$out" "$tmp.o" && mv -f "$tmp.o" "$C/$key.o"
    if [ -s "$tmp.out" ] || [ -s "$tmp.err" ]; then
        cat "$tmp.out" "$tmp.err" > "$tmp.log" && mv -f "$tmp.log" "$C/$key.log"
    fi
    echo "$rel" > "$tmp.src" && mv -f "$tmp.src" "$C/$key.src"
    echo "MISS $key $rel" >> "$C/log"
else
    echo "FAIL $key $rel" >> "$C/log"
fi
rm -f "$tmp.out" "$tmp.err" "$tmp.o" "$tmp.log" "$tmp.src"
exit $rc
