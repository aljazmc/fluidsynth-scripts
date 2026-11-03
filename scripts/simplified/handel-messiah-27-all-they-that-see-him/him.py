from orchestra import Orchestra

# Handel, Messiah, Part II, No. 27. All they that see him laugh him to scorn
# (accompanied recitative, tenor). A from-memory arrangement for General MIDI
# baroque orchestra, the tenor singing without words: the strings' mocking,
# jerky dotted figures in B-flat minor around the tenor's declamation, in
# Handel's manner; the notes are approximate.
SEED = 1767

PARTS = ("tenor", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

MOCK = "m4/4 " + " ".join(f"r:1/4 {a}:3/4 r:1/4 {b}:3/4 r:1/4 {a}:3/4 r:1/4 {b}:3/4 |" for a, b in (
    ("db5", "bb4"), ("eb5", "c5"), ("f5", "db5"), ("e5", "c5")))
LINE = ("m4/4 r:1 f4:1/2 f4:1/2 bb4:1 f4:1/2 db4:1/2 | eb4:1/2 f4:1/2 gb4:1 c4:1 r:1 | "
        "r:1 ab4:1/2 ab4:1/2 db5:1 bb4:1/2 gb4:1/2 | g4:1 c5:1 f4:2 |")
BASS = "m4/4 bb2:4 | a2:4 | bb2:4 | c3:2 f2:2 |"


def picture(orchestra):
    orchestra.play({"tenor": "!mf " + LINE, "violins": "!mf " + MOCK, "violins 2": ("!mf " + MOCK, -5),
                    "violas": "!p m4/4 f3+bb3:4 | f3+c4:4 | f3+db4:4 | e3+g3:2 f3+a3:2 |",
                    "cellos": "!mf " + BASS, "basses": ("!mf " + BASS, -12)}, bpm=66, label="laugh him to scorn")
    orchestra.play({"violins": "!mf m4/4 a4+c5:2 r:2 |", "violas": "!mf m4/4 f3+c4:2 r:2 |",
                    "cellos": "!mf m4/4 f2:2 r:2 |", "harpsichord": "!mf m4/4 f2+a2+c3+f3:2 r:2 |"}, bpm=66)


def him():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render(tail=3.0)
