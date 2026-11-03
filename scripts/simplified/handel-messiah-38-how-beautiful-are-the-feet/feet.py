from orchestra import Orchestra

# Handel, Messiah, Part II, No. 38. How beautiful are the feet of them that
# preach the gospel of peace (air, soprano). A from-memory arrangement for
# General MIDI baroque orchestra, the soprano singing without words: a tender
# G minor pastoral in 12/8, the violins and the soprano in gentle dialogue,
# in Handel's manner; the notes are approximate.
SEED = 1778

PARTS = ("soprano", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Larghetto, 12/8 (six crotchet beats)
LINE = ("m12/8 d5:3/2 bb4:1/2 c5:1 d5:3/2 g5:1/2 d5:1 | eb5:3/2 d5:1/2 c5:1 bb4:3/2 a4:1/2 g4:1 | "
        "a4:3/2 bb4:1/2 c5:1 d5:1 c5:1/2 bb4:1 a4:1/2 | bb4:3 a4:3 | "
        "d5:3/2 eb5:1/2 f5:1 eb5:3/2 d5:1/2 c5:1 | bb4:3/2 c5:1/2 d5:1 a4:3/2 bb4:1/2 g4:1 | "
        "c5:1 bb4:1/2 a4:1 g4:1/2 bb4:3/2 a4:1/2 g4:1 | g4:6 |")
BASS = "m12/8 g2:3 g2:3 | c3:3 g2:3 | f2:3 f#2:3 | g2:3 d2:3 | bb2:3 c3:3 | g2:3 d3:3 | eb3:3/2 c3:3/2 d3:3 | g2:6 |"
PAD = "m12/8 bb3+d4:6 | c4+eb4:3 bb3+d4:3 | c4+f4:3 a3+d4:3 | bb3+d4:3 a3+c4:3 | bb3+d4:3 g3+c4:3 | bb3+d4:3 a3+c4:3 | g3+c4:3/2 a3+c4:3/2 a3+c4:3 | bb3+d4:6 |"


def picture(orchestra):
    strings = {"violins 2": "!pp " + PAD, "violas": ("!pp " + PAD, -12), "cellos": "!p " + BASS,
               "basses": ("!p " + BASS, -12), "harpsichord": "!pp " + PAD}
    orchestra.play({"violins": "!mp " + LINE, **strings}, bpm=78, label="ritornello")
    orchestra.play({"soprano": "!mp " + LINE, **strings}, bpm=78, label="how beautiful")
    orchestra.play({"soprano": ("!mp " + LINE, 3), "violins 2": ("!pp " + PAD, 3), "violas": ("!pp " + PAD, -9),
                    "cellos": ("!p " + BASS, 3), "basses": ("!p " + BASS, -9)}, bpm=78, label="in B-flat")
    orchestra.play({"violins": "!p " + LINE, **strings}, bpm=78, to=66, label="ritornello")


def feet():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
