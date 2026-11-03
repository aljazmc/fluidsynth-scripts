from orchestra import Orchestra

# Handel, Messiah, Part I, No. 8. Behold, a virgin shall conceive (recitative,
# alto). A from-memory arrangement for General MIDI baroque orchestra, the
# alto singing without words over harpsichord and cello continuo, a short
# secco recitative in D major, in Handel's manner; the notes are approximate.
SEED = 1748

PARTS = ("alto", "harpsichord", "cellos", "basses")

LINE = ("m4/4 r:1 a4:1/2 a4:1/2 f#4:1 d4:1/2 e4:1/2 | f#4:1/2 f#4:1/2 g4:1/2 a4:1/2 d4:1 r:1 | "
        "r:1 b4:1/2 b4:1/2 g4:1 e4:1/2 f#4:1/2 | g4:1/2 g4:1/2 a4:1/2 b4:1/2 e4:1 r:1 | "
        "r:1/2 c#5:1/2 c#5:1/2 a4:1/2 f#4:1 g4:1/2 e4:1/2 | d4:1 r:3 |")
CHORDS = "m4/4 d3+f#3+a3:4 | d3+f#3+a3:4 | e3+g3+b3:4 | c#3+e3+a3:4 | a2+c#3+e3+g3:4 | d3+f#3+a3:4 |"
BASS = "m4/4 d3:4 | f#2:4 | e2:4 | a2:4 | a2:4 | d2:4 |"


def picture(orchestra):
    orchestra.play({"alto": "!mp " + LINE, "harpsichord": "!mp " + CHORDS, "cellos": "!mp " + BASS,
                    "basses": ("!p " + BASS, -12)}, bpm=76, label="recitative")
    orchestra.play({"harpsichord": "!mp m4/4 a2+c#3+e3+g3:1 d3+f#3+a3:1 r:2 |", "cellos": "!mp m4/4 a2:1 d2:1 r:2 |"},
                   bpm=76, label="cadence")


def conceive():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
