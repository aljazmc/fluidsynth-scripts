#!/bin/bash
#
# project.sh names its outputs as the README says, and its clean commands
# remove exactly those: simplified/<name> -> build/<name>.<format>, other
# groups keep their name as a prefix, alac -> <name>-alac.m4a, npy -> npy/.
#
# Runs in a sandbox (see lib.sh), so it never touches the real build/ or npy/.
# Run from anywhere: bash tests/sh/test_outputs.sh

# shellcheck source=tests/sh/lib.sh
. "$(dirname "$0")/lib.sh"
sandbox

# expect_output <project> <format> <file>: clean removes <file> and no other
expect_output() {

    mkdir -p build npy
    touch "$3" build/keep.mp3 npy/keep.npy
    ./project.sh "$1" "$2" clean > /dev/null 2>&1
    if [ -e "$3" ]; then
        fail "./project.sh $1 $2 clean should remove $3"
    elif [ ! -e build/keep.mp3 ] || [ ! -e npy/keep.npy ]; then
        fail "./project.sh $1 $2 clean removed other files"
    else
        pass "$1 $2 -> $3"
    fi
    rm -rf build npy

}

expect_output simplified/bach-prelude mp3 build/bach-prelude.mp3
expect_output simplified/holst-the-planets-01-mars flac build/holst-the-planets-01-mars.flac
expect_output soundscapes/nature-rain00 ogg build/soundscapes-nature-rain00.ogg
expect_output solo-piece wav build/solo-piece.wav
expect_output simplified/bach-prelude alac build/bach-prelude-alac.m4a
expect_output simplified/bach-prelude m4a build/bach-prelude.m4a
expect_output soundscapes/nature-rain01 npy npy/soundscapes-nature-rain01.npy
expect_output soundscapes/cyberpunk-neon00 mp4 build/soundscapes-cyberpunk-neon00.mp4

# <project> clean removes every format of that project, and only that project
mkdir -p build npy
touch build/bach-prelude.mp3 build/bach-prelude.wav build/bach-prelude-alac.m4a \
    npy/bach-prelude.npy build/soundscapes-nature-rain00.mp3
./project.sh simplified/bach-prelude clean > /dev/null 2>&1
check "<project> clean removes all its outputs" \
    [ -z "$(find build npy -name 'bach-prelude*')" ]
check "<project> clean keeps other projects' outputs" \
    [ -e build/soundscapes-nature-rain00.mp3 ]

# clean removes build/ and npy/
./project.sh clean > /dev/null 2>&1
check "clean removes build/" [ ! -e build ]
check "clean removes npy/" [ ! -e npy ]

finish
