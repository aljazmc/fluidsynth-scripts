#!/bin/bash

FORMATS=(
    aac ac3 aiff alac au caf dts eac3 flac m4a mka mp2 mp3 ogg opus tta
    w64 wav wma wv
)

status=0

require() {

    local bin
    if bin=$(command -v "$1"); then
        echo "$1 found at: $bin"
    else
        echo "$1 is required but was not found" >&2
        exit 1
    fi

}

projects() {

    find scripts -mindepth 1 -maxdepth 1 -type d ! -name __pycache__ ! -name '.*' -printf '%f\n' | sort

}

output() {

    case "$2" in
        npy) echo "npy/$1.npy" ;;
        alac) echo "build/$1-alac.m4a" ;;
        *) echo "build/$1.$2" ;;
    esac

}

run() {

    local script file
    [ "$2" = "npy" ] && script="savenpy" || script="export$2"
    file=$(output "$1" "$2")

    if [ -e "$file" ]; then
        echo "Skipping $file (already exists)"
        return
    fi

    python3 "scripts/$script.py" "$1" && echo "Created $file" || {
        echo "FAILED: $script for $1" >&2
        status=1
    }

}

remove() {

    local file
    file=$(output "$1" "$2")

    if [ -e "$file" ]; then
        rm -f "$file"
        echo "Removed $file"
    fi

}

process() {

    local format
    if [ "$2" = "all" ]; then
        for format in "${FORMATS[@]}" npy; do
            "$3" "$1" "$format"
        done
    else
        "$3" "$1" "$2"
    fi

}

clean() {

    rm -rf build npy

}

usage() {

    local IFS="|"
    echo "You should use: $0 clean" >&2
    echo "            or: $0 {all|<project>} {all|npy|${FORMATS[*]}}" >&2
    echo "            or: $0 {all|<project>} clean" >&2
    echo "            or: $0 {all|<project>} {npy|${FORMATS[*]}} clean" >&2
    echo "Projects: $(projects | paste -sd' ')" >&2
    exit 1

}

valid_format() {

    local format
    [ "$1" = "all" ] || [ "$1" = "npy" ] && return 0
    for format in "${FORMATS[@]}"; do
        [ "$1" = "$format" ] && return 0
    done
    return 1

}

[ "$1" = "clean" ] && [ $# -eq 1 ] && { clean; exit; }

if [ $# -eq 2 ] && [ "$2" = "clean" ]; then
    format="all"
    action="remove"
elif [ $# -eq 3 ] && [ "$3" = "clean" ]; then
    format="$2"
    action="remove"
elif [ $# -eq 2 ]; then
    format="$2"
    action="run"
else
    usage
fi

valid_format "$format" || usage

if [ "$1" = "all" ]; then
    mapfile -t targets < <(projects)
elif [ -d "scripts/$1" ]; then
    targets=("$1")
else
    usage
fi

if [ "$action" = "run" ]; then
    require python3
    require fluidsynth
    require ffmpeg
    python3 -c "import numpy" 2>/dev/null || { echo "numpy is required but was not found" >&2; exit 1; }
fi

for project in "${targets[@]}"; do
    process "$project" "$format" "$action"
done

exit "$status"
