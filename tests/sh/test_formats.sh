#!/bin/bash
#
# The formats in project.sh, the exporters in scripts/ and the formats in the
# README agree: every format has an exporter that writes its own extension,
# every exporter is listed, and the README names every format.
#
# Run from anywhere: bash tests/sh/test_formats.sh

# shellcheck source=tests/sh/lib.sh
. "$(dirname "$0")/lib.sh"
cd "$ROOT" || exit 1

# the FORMATS array of project.sh, without running it
mapfile -t formats < <(sed -n '/^FORMATS=(/,/^)/p' project.sh | sed '1d;$d' | tr -s ' ' '\n' | sed '/^$/d')

if [ "${#formats[@]}" -lt 20 ]; then
    fail "read the FORMATS of project.sh, got ${#formats[@]}: ${formats[*]}"
fi

for format in "${formats[@]}"; do
    script="scripts/export$format.py"
    if [ ! -f "$script" ]; then
        fail "$format has no $script"
        continue
    fi
    # alac goes to <name>-alac.m4a, so it doesn't clash with m4a
    extension=".$format"
    [ "$format" = "alac" ] && extension="-alac.m4a"
    check "$script writes $extension" grep -qF "output + \"$extension\"" "$script"
    check "the README lists $format" grep -qE "^\|.*\`$format\`" README.md
done

for script in scripts/export*.py; do
    format=${script#scripts/export}
    format=${format%.py}
    listed=no
    for known in "${formats[@]}"; do
        [ "$known" = "$format" ] && listed=yes
    done
    check "$script is in the FORMATS of project.sh" [ "$listed" = yes ]
done

check "scripts/savenpy.py exists for npy" [ -f scripts/savenpy.py ]

finish
