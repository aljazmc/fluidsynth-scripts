#!/bin/bash
#
# project.sh runs the right exporter for each request: one project, a group,
# every project; it skips outputs that exist, reports a failed export with
# exit code 1, and stops when a program it needs is missing.
#
# Runs in a sandbox (see lib.sh) with a stand-in python3, so nothing renders.
# Run from anywhere: bash tests/sh/test_run.sh

# shellcheck source=tests/sh/lib.sh
. "$(dirname "$0")/lib.sh"
sandbox

# expect_calls <description> <expected calls.log> -- <project.sh arguments>
expect_calls() {

    local description=$1 expected=$2
    shift 3
    : > calls.log
    ./project.sh "$@" > output.log 2>&1
    if [ "$(cat calls.log)" = "$expected" ]; then
        pass "$description"
    else
        fail "$description: ./project.sh $* ran"$'\n'"$(cat calls.log)"$'\n'"expected"$'\n'"$expected"
    fi

}

expect_calls "one project, one format" \
    "python3 scripts/exportmp3.py simplified/bach-prelude" \
    -- simplified/bach-prelude mp3

expect_calls "npy runs savenpy.py" \
    "python3 scripts/savenpy.py soundscapes/nature-rain00" \
    -- soundscapes/nature-rain00 npy

expect_calls "a group runs each of its projects, sorted, and nothing else" \
    "python3 scripts/exportflac.py soundscapes/cyberpunk-neon00
python3 scripts/exportflac.py soundscapes/nature-rain00
python3 scripts/exportflac.py soundscapes/nature-rain01" \
    -- soundscapes all flac

expect_calls "all runs every project, and skips folders without <name>.py" \
    "python3 scripts/exportwav.py simplified/bach-prelude
python3 scripts/exportwav.py simplified/holst-the-planets-01-mars
python3 scripts/exportwav.py solo-piece
python3 scripts/exportwav.py soundscapes/cyberpunk-neon00
python3 scripts/exportwav.py soundscapes/nature-rain00
python3 scripts/exportwav.py soundscapes/nature-rain01" \
    -- all wav

: > calls.log
./project.sh solo-piece all > /dev/null 2>&1
formats=$(sed -n '/^FORMATS=(/,/^)/p' project.sh | sed '1d;$d' | wc -w)
check "<project> all runs every format and npy ($((formats + 1)) exports)" \
    [ "$(wc -l < calls.log)" -eq $((formats + 1)) ]

mkdir -p build
touch build/bach-prelude.ogg
expect_calls "an existing output is skipped" "" -- simplified/bach-prelude ogg
check "and says so" grep -q "Skipping build/bach-prelude.ogg" output.log
rm -rf build

PYTHON_EXIT=1 ./project.sh soundscapes all mp3 > output.log 2>&1
code=$?
check "a failed export exits with 1" [ "$code" -eq 1 ]
check "and names the project" grep -q "FAILED: exportmp3 for soundscapes/nature-rain01" output.log
check "and goes on with the other projects" [ "$(grep -c FAILED output.log)" -eq 3 ]

# no ffmpeg on the PATH: only the stand-ins and the basic tools project.sh uses
mkdir tools
for tool in bash find sort grep cut head paste sed; do
    ln -s "$(command -v "$tool")" "tools/$tool"
done
rm bin/ffmpeg
PATH="$SANDBOX/bin:$SANDBOX/tools" ./project.sh simplified/bach-prelude mp3 > output.log 2>&1
code=$?
check "a missing program exits with 1" [ "$code" -eq 1 ]
check "and names it" grep -q "ffmpeg is required" output.log

finish
