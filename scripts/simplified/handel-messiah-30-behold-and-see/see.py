from orchestra import Orchestra

# Handel, Messiah, Part II, No. 30. Behold, and see if there be any sorrow
# (arioso, tenor). A from-memory arrangement for General MIDI baroque
# orchestra, the tenor singing without words: a brief, desolate E minor
# Largo with sighing strings, in Handel's manner; the notes are approximate.
SEED = 1770

PARTS = ("tenor", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

LINE = ("m4/4 r:1 b4:1 e5:1 d#5:1 | e5:2 r:1 g4:1 | a4:1 c5:1 b4:1 a4:1 | g4:2 f#4:2 | "
        "r:1 b4:1 c5:1 a4:1 | f#4:1 g4:1 a4:1 c5:1 | b4:1 a4:1/2 g4:1/2 f#4:1 e4:1 | e4:4 |")
SIGHS = "m4/4 " + " ".join(f"r:1/2 {c}:1/2 r:1/2 {c}:1/2 r:1/2 {c}:1/2 r:1/2 {c}:1/2 |" for c in (
    "g4+b4", "g4+b4", "e4+a4", "d#4+a4", "e4+g4", "d#4+a4", "e4+g4", "e4+g4"))
BASS = "m4/4 e3:4 | e3:2 e2:2 | a2:4 | b2:4 | c3:2 a2:2 | b2:4 | b2:2 b1:2 | e2:4 |"


def picture(orchestra):
    orchestra.play({"violins": "!p " + LINE, "violins 2": ("!pp " + SIGHS, 0), "violas": ("!pp " + SIGHS, -12),
                    "cellos": "!p " + BASS, "basses": ("!p " + BASS, -12)}, bpm=50, label="ritornello")
    orchestra.play({"tenor": "!mp " + LINE, "violins": ("!pp " + SIGHS, 12), "violins 2": "!pp " + SIGHS,
                    "violas": ("!pp " + SIGHS, -12), "cellos": "!p " + BASS, "basses": ("!p " + BASS, -12),
                    "harpsichord": "!pp " + BASS}, bpm=50, to=44, label="behold and see")


def see():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render(tail=4.0)
