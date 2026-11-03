from orchestra import Orchestra

# Handel, Messiah, Part III, No. 45. I know that my redeemer liveth (air,
# soprano). A from-memory arrangement for General MIDI baroque orchestra, the
# soprano singing without words: the serene E major Larghetto in 3/4 that
# opens Part III, the soprano rising confidently over a simple violin and
# continuo texture, in Handel's manner; the notes are approximate.
SEED = 1785

PARTS = ("soprano", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Larghetto, 3/4
LINE = ("m3/4 b4:2 e5:1 | e5:3/2 f#5:1/2 g#5:1 | f#5:1 e5:1 d#5:1 | e5:2 b4:1 | "
        "c#5:1 b4:1 a4:1 | g#4:3/2 a4:1/2 b4:1 | a4:1 g#4:1 f#4:1 | e4:3 | "
        "g#4:1 b4:1 e5:1 | a5:2 g#5:1 | f#5:1 e5:1 d#5:1 | e5:2 c#5:1 | "
        "b4:1 a4:1 g#4:1 | f#4:3/2 e4:1/2 f#4:1 | e4:3 |")
BASS = ("m3/4 e3:3 | e3:3 | b2:3 | e3:3 | a2:3 | e2:3 | b2:3 | e2:3 | e3:3 | c#3:3 | b2:3 | c#3:3 | "
        "d#3:2 e3:1 | b2:3 | e2:3 |")
PAD = ("m3/4 g#3+b3:3 | g#3+b3:3 | f#3+a3:3 | g#3+b3:3 | a3+c#4:3 | g#3+b3:3 | f#3+a3:3 | g#3+b3:3 | "
       "g#3+b3:3 | a3+c#4:3 | f#3+a3:3 | g#3+c#4:3 | f#3+a3:2 g#3+b3:1 | f#3+a3:3 | g#3+b3:3 |")


def picture(orchestra):
    strings = {"violins 2": "!pp " + PAD, "violas": ("!pp " + PAD, -12), "cellos": "!p " + BASS,
               "basses": ("!p " + BASS, -12), "harpsichord": "!pp " + PAD}
    orchestra.play({"violins": "!mp " + LINE, **strings}, bpm=66, label="ritornello")
    orchestra.play({"soprano": "!mf " + LINE, **strings}, bpm=66, label="I know that my redeemer liveth")
    orchestra.play({"soprano": ("!mf " + LINE, 7), "violins 2": ("!pp " + PAD, 7), "violas": ("!pp " + PAD, -5),
                    "cellos": ("!p " + BASS, 7), "basses": ("!p " + BASS, -5)}, bpm=66, label="in B major")
    orchestra.play({"soprano": "!mf " + LINE, **strings}, bpm=66, to=58)
    orchestra.play({"violins": "!p " + LINE, **strings}, bpm=60, to=52, label="ritornello")


def liveth():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
