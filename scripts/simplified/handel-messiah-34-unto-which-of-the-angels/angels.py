from orchestra import Orchestra

# Handel, Messiah, Part II, No. 34. Unto which of the angels said he at any
# time (recitative, tenor). A from-memory arrangement for General MIDI
# baroque orchestra, the tenor singing without words over harpsichord and
# cello: a short secco recitative closing in D major, in Handel's manner; the
# notes are approximate.
SEED = 1774

PARTS = ("tenor", "harpsichord", "cellos", "basses")

LINE = ("m4/4 r:1 a3:1/2 a3:1/2 d4:1 a3:1/2 b3:1/2 | c#4:1/2 d4:1/2 e4:1 a3:1 r:1 | "
        "r:1 e4:1/2 f#4:1/2 g4:1 e4:1/2 c#4:1/2 | d4:1/2 e4:1/2 f#4:1 d4:1 r:1 |")
CHORDS = "m4/4 d3+f#3+a3:4 | a2+c#3+e3:4 | a2+c#3+e3+g3:4 | d3+f#3+a3:4 |"
BASS = "m4/4 d3:4 | c#3:4 | a2:4 | d3:4 |"


def picture(orchestra):
    orchestra.play({"tenor": "!mf " + LINE, "harpsichord": "!mp " + CHORDS, "cellos": "!mp " + BASS,
                    "basses": ("!p " + BASS, -12)}, bpm=80, label="recitative")
    orchestra.play({"harpsichord": "!mp m4/4 a2+c#3+e3+g3:1 d3+f#3+a3:1 r:2 |", "cellos": "!mp m4/4 a2:1 d2:1 r:2 |"},
                   bpm=80, label="cadence")


def angels():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
