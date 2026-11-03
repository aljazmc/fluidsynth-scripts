from orchestra import Orchestra

# Handel, Messiah, Part I, No. 15. And the angel said unto them (recitative,
# soprano). A from-memory arrangement for General MIDI baroque orchestra, the
# soprano singing without words over harpsichord and cello: "Fear not, for
# behold, I bring you good tidings of great joy", a short secco recitative,
# in Handel's manner; the notes are approximate.
SEED = 1755

PARTS = ("soprano", "harpsichord", "cellos", "basses")

LINE = ("m4/4 r:1 d5:1/2 a4:1/2 f#4:1 a4:1/2 b4:1/2 | a4:1 r:1 a4:1/2 a4:1/2 d5:1 | "
        "c#5:1/2 c#5:1/2 b4:1/2 a4:1/2 g#4:1 a4:1/2 b4:1/2 | c#5:1 a4:1 r:2 | "
        "r:1 e5:1/2 c#5:1/2 a4:1 g4:1/2 f#4:1/2 | g4:1/2 a4:1/2 b4:1/2 g4:1/2 e4:1 a4:1 | "
        "d4:1/2 e4:1/2 f#4:1 r:2 |")
CHORDS = "m4/4 d3+f#3+a3:4 | f#3+a3+d4:4 | e3+g#3+b3:4 | a2+c#3+e3:4 | c#3+e3+g3+a3:4 | e3+g3+b3:2 a2+c#3+e3+g3:2 | d3+f#3+a3:4 |"
BASS = "m4/4 d3:4 | d3:4 | e3:4 | a2:4 | a2:4 | g2:2 a2:2 | d2:4 |"


def picture(orchestra):
    orchestra.play({"soprano": "!mf " + LINE, "harpsichord": "!mp " + CHORDS, "cellos": "!mp " + BASS,
                    "basses": ("!p " + BASS, -12)}, bpm=80, label="recitative")
    orchestra.play({"harpsichord": "!mp m4/4 a2+c#3+e3+g3:1 d3+f#3+a3:1 r:2 |", "cellos": "!mp m4/4 a2:1 d2:1 r:2 |"},
                   bpm=80, label="cadence")


def them():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
