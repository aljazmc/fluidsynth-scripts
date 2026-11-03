from orchestra import Orchestra

# Handel, Messiah, Part II, No. 29. Thy rebuke hath broken his heart
# (accompanied recitative, tenor). A from-memory arrangement for General MIDI
# baroque orchestra, the tenor singing without words: slow, aching string
# chords that wander through remote keys while the tenor laments, in
# Handel's manner; the notes are approximate.
SEED = 1769

PARTS = ("tenor", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

LINE = ("m4/4 r:1 eb4:1 ab4:1 c5:1/2 bb4:1/2 | ab4:1 g4:1 r:2 | r:1 bb4:1 db5:1 c5:1/2 bb4:1/2 | a4:2 r:2 | "
        "r:1 c5:1 e5:1 d5:1/2 c5:1/2 | b4:1 a4:1 g#4:2 | r:1 b4:1 d#5:1 c#5:1/2 b4:1/2 | b4:4 |")
CHORDS = "m4/4 " + " ".join(f"{c}:4 |" for c in ("ab3+c4+eb4", "g3+bb3+eb4", "bb3+db4+f4", "a3+c4+f4",
                                                   "a3+c4+e4", "f#3+a3+d#4", "f#3+b3+d#4", "f#3+b3+d#4"))
BASS = "m4/4 ab2:4 | eb2:4 | bb2:4 | f2:4 | a2:4 | b2:2 e2:2 | b2:4 | b1:4 |"


def picture(orchestra):
    orchestra.play({"tenor": "!mp " + LINE, "violins": ("!pp " + CHORDS, 12), "violins 2": "!pp " + CHORDS,
                    "violas": ("!pp " + CHORDS, -12), "cellos": "!p " + BASS, "basses": ("!p " + BASS, -12)},
                   bpm=48, to=44, label="thy rebuke")


def heart():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render(tail=4.0)
