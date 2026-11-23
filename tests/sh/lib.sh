#!/bin/bash
#
# Helpers for the tests of project.sh: a sandbox with a copy of project.sh, a
# few fake projects and stand-ins for python3, fluidsynth and ffmpeg, so a test
# can run project.sh without rendering anything or touching build/ and npy/.
#
# Source it from a test: . "$(dirname "$0")/lib.sh"

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
failures=0

# Make a sandbox and cd into it. The stand-in python3 writes each call to
# calls.log, answers "import numpy", and exits with $PYTHON_EXIT (default 0).
sandbox() {

    SANDBOX=$(mktemp -d)
    trap 'rm -rf "$SANDBOX"' EXIT
    cp "$ROOT/project.sh" "$SANDBOX/"
    cd "$SANDBOX" || exit 1

    local project
    for project in simplified/bach-prelude simplified/holst-the-planets-01-mars \
        soundscapes/nature-rain00 soundscapes/nature-rain01 soundscapes/cyberpunk-neon00 \
        solo-piece; do
        mkdir -p "scripts/$project"
        touch "scripts/$project/${project##*-}.py"
    done
    # a folder that is not a project: no <name>.py
    mkdir -p scripts/soundscapes/notes-draft

    mkdir bin
    cat > bin/python3 <<'EOF'
#!/bin/bash
[ "$1" = "-c" ] && exit 0
echo "python3 $*" >> calls.log
exit "${PYTHON_EXIT:-0}"
EOF
    printf '#!/bin/bash\nexit 0\n' > bin/fluidsynth
    printf '#!/bin/bash\nexit 0\n' > bin/ffmpeg
    chmod +x bin/*
    PATH="$SANDBOX/bin:$PATH"
    : > calls.log

}

pass() {
    echo "ok: $1"
}

fail() {
    echo "FAIL: $1" >&2
    failures=$((failures + 1))
}

# check <description> <command...>: passes if the command succeeds
check() {
    local description=$1
    shift
    if "$@"; then
        pass "$description"
    else
        fail "$description"
    fi
}

finish() {
    if [ "$failures" -gt 0 ]; then
        echo "FAILED: $failures" >&2
        exit 1
    fi
    echo "PASS"
}
