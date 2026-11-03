from orchestra import Orchestra

# Handel, Messiah, Part II, No. 32. But thou didst not leave his soul in hell
# (air, tenor). A from-memory arrangement for General MIDI baroque orchestra,
# the tenor singing without words: a hopeful A major air in 3/4, the tenor
# and the violins answering each other over a walking bass, in Handel's
# manner; the notes are approximate.
SEED = 1772

PARTS = ("tenor", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Andante larghetto, 3/4
TUNE = ("m3/4 e4:1 a4:1 c#5:1 | b4:3/2 a4:1/2 g#4:1 | a4:1 e4:1 f#4:1 | e4:3 | "
        "c#5:1 e5:1 d5:1 | c#5:3/2 b4:1/2 a4:1 | f#4:1 b4:1 g#4:1 | a4:3 |")
BASS = "m3/4 a2:1 c#3:1 a2:1 | e2:1 e3:1 e2:1 | f#2:1 c#2:1 d2:1 | e2:1 b1:1 e2:1 | " \
       "a2:1 c#3:1 b2:1 | a2:1 e2:1 f#2:1 | d2:1 e2:1 e1:1 | a1:3 |"
PAD = "m3/4 c#4+e4:3 | b3+e4:3 | a3+d4:3 | b3+d4:3 | c#4+e4:3 | c#4+e4:3 | a3+d4:3/2 b3+d4:3/2 | c#4+e4:3 |"


def picture(orchestra):
    strings = {"violins 2": "!pp " + PAD, "violas": ("!pp " + PAD, -12), "cellos": "!p " + BASS,
               "basses": ("!p " + BASS, -12), "harpsichord": "!pp " + PAD}
    orchestra.play({"violins": "!mf " + TUNE, **strings}, bpm=80, label="ritornello")
    orchestra.play({"tenor": "!mf " + TUNE, **strings}, bpm=80, label="but thou didst not leave")
    orchestra.play({"tenor": ("!mf " + TUNE, 7), "violins 2": ("!pp " + PAD, 7), "violas": ("!pp " + PAD, -5),
                    "cellos": ("!p " + BASS, 7), "basses": ("!p " + BASS, -5)}, bpm=80, label="in E major")
    orchestra.play({"tenor": "!mf " + TUNE, **strings}, bpm=80)
    orchestra.play({"violins": "!mf " + TUNE, **strings}, bpm=80, to=68, label="ritornello")


def leave():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
