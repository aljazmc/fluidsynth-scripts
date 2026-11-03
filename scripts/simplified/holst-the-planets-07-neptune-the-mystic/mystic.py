import re

from orchestra import Orchestra
from score import FIRST_BAR, LAST_BAR, METERS, PARTS

# Holst, The Planets, VII. Neptune, the Mystic, simplified.

SEED = 1921

# (first bar, pulse per minute, pulse at the end of the passage or None); the
# pulse is a crotchet, or a dotted crotchet in 6/8. From the score's markings,
# the values are my choice (as in the transcribed version)
TEMPI = (
    (1, 66, None),       # Andante (5/4 throughout)
    (50, 80, None),      # Allegretto
)

# the last bar is "repeated until the sound is lost in the distance"
REPEATS = 4

DYNAMIC = re.compile(r"!([<>]?)(ppp|pp|p|mp|mf|fff|ff|f)\b")


def pulse(meter):
    """The pulse in crotchets: a dotted crotchet in compound time."""
    top, bottom = map(int, meter.split("/"))
    return 1.5 if bottom == 8 and top % 3 == 0 and top > 3 else 1.0


def crotchets(meter):
    top, bottom = map(int, meter.split("/"))
    return top * 4 / bottom


def current_dynamic(bars):
    """The last dynamic marking in a run of bars, as a token to start with."""
    for bar in reversed(bars):
        found = DYNAMIC.findall(bar)
        if found:
            return "!" + found[-1][1] + " "
    return ""


def section(first, last):
    """{part: [voices]} for bars first..last, each voice starting at its dynamic."""
    out = {}
    for part, lines in PARTS.items():
        for line in lines:
            bars = line[first - FIRST_BAR:last - FIRST_BAR + 1]
            if not any(re.search(r"(?<![!r:/])\b\d+(?:\+\d+)*:", b) for b in bars):
                continue  # silent for the whole passage
            start = current_dynamic(line[:first - FIRST_BAR])
            out.setdefault(part, []).append(start + " ".join(bars))
    return out


def passages(last_bar):
    """Runs of bars with one tempo entry and one pulse."""
    for k, (first, rate, to) in enumerate(TEMPI):
        last = TEMPI[k + 1][0] - 1 if k + 1 < len(TEMPI) else last_bar
        start = first
        for bar in range(first + 1, last + 2):
            if bar > last or pulse(METERS[bar - FIRST_BAR]) != pulse(METERS[start - FIRST_BAR]):
                yield start, bar - 1, rate, to if bar > last else None
                start = bar


def picture(orchestra):
    for first, last, rate, to in passages(LAST_BAR - 1):
        beat = pulse(METERS[first - FIRST_BAR])
        parts = section(first, last)
        if parts:
            orchestra.play(parts, bpm=rate * beat, to=to * beat if to else None, label=f"bars {first}-{last}")
        else:  # everyone silent
            orchestra.rest(60 / rate * sum(crotchets(m) for m in METERS[first - FIRST_BAR:last - FIRST_BAR + 1]))
    # the last bar, sung over and over from pp, dying away to nothing
    rate = TEMPI[-1][1]
    ending = {part: ["!pp " + " ".join([DYNAMIC.sub("", voice).strip()] * REPEATS) + " !>n"
                     for voice in voices]
              for part, voices in section(LAST_BAR, LAST_BAR).items()}
    orchestra.play(ending, bpm=rate, to=rate * 0.85, label=f"bar {LAST_BAR}, repeated")


def mystic():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render(tail=6.0)
