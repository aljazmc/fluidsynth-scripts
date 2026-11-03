from orchestra import Orchestra

# Handel, Messiah, Part I, No. 16. And suddenly there was with the angel
# (accompanied recitative, soprano). A from-memory arrangement for General
# MIDI baroque orchestra, the soprano singing without words: the violins'
# rushing semiquavers as the heavenly host appears, in D major, leading
# straight into "Glory to God", in Handel's manner; the notes are approximate.
SEED = 1756

PARTS = ("soprano", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

RUSH = "m4/4 " + " ".join(f"{a}:1/4 {b} {c} {d} " * 4 + "|" for a, b, c, d in (
    ("d4", "f#4", "a4", "d5"), ("d4", "f#4", "a4", "d5"), ("e4", "g4", "b4", "e5"), ("c#4", "e4", "a4", "c#5"),
    ("d4", "f#4", "a4", "d5"), ("a3", "c#4", "e4", "a4")))
LINE = ("m4/4 r:2 a4:1/2 a4:1/2 d5:1 | a4:1/2 a4:1/2 f#4:1/2 g4:1/2 a4:1 r:1 | "
        "r:1 b4:1/2 c#5:1/2 d5:1 e5:1/2 b4:1/2 | c#5:1 a4:1 r:2 | "
        "r:1 f#5:1/2 e5:1/2 d5:1 a4:1/2 b4:1/2 | c#5:1/2 d5:1/2 e5:1 a4:2 |")
BASS = "m4/4 d3:4 | d3:4 | g2:4 | a2:4 | d3:4 | a2:4 |"


def picture(orchestra):
    orchestra.play({"soprano": "!f " + LINE, "violins": ("!mf " + RUSH, 12), "violins 2": "!mf " + RUSH,
                    "violas": "!p m4/4 a3:4 | a3:4 | b3:4 | a3:4 | a3:4 | a3:4 |", "cellos": "!mf " + BASS,
                    "basses": ("!mf " + BASS, -12)}, bpm=84, to=76, label="suddenly")
    orchestra.play({"violins": "!mf m4/4 a4+c#5+e5:2 r:2 |", "violas": "!mf m4/4 e4:2 r:2 |",
                    "cellos": "!mf m4/4 a2:2 r:2 |", "basses": "!mf m4/4 a1:2 r:2 |",
                    "harpsichord": "!mf m4/4 a2+c#3+e3+a3:2 r:2 |"}, bpm=76, label="half close")


def angel():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
