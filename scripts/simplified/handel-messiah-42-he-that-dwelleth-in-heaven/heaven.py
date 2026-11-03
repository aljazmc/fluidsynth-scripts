from orchestra import Orchestra

# Handel, Messiah, Part II, No. 42. He that dwelleth in heaven shall laugh
# them to scorn (recitative, tenor). A from-memory arrangement for General
# MIDI baroque orchestra, the tenor singing without words over harpsichord
# and cello: a short secco recitative leading to A minor, in Handel's
# manner; the notes are approximate.
SEED = 1782

PARTS = ("tenor", "harpsichord", "cellos", "basses")

LINE = ("m4/4 r:1 e4:1/2 e4:1/2 a4:1 e4:1/2 c4:1/2 | d4:1/2 e4:1/2 f4:1 b3:1 r:1 | "
        "r:1 g#4:1/2 a4:1/2 b4:1 e4:1/2 f4:1/2 | d4:1/2 c4:1/2 b3:1 a3:1 r:1 |")
CHORDS = "m4/4 a2+c3+e3:4 | d3+f3+a3:2 g#2+b2+e3:2 | e3+g#3+b3:4 | f3+a3+d4:2 e3+g#3+b3:1 a2+c3+e3:1 |"
BASS = "m4/4 a2:4 | d3:2 g#2:2 | e2:4 | d2:2 e2:1 a1:1 |"


def picture(orchestra):
    orchestra.play({"tenor": "!mf " + LINE, "harpsichord": "!mp " + CHORDS, "cellos": "!mp " + BASS,
                    "basses": ("!p " + BASS, -12)}, bpm=80, label="recitative")


def heaven():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
