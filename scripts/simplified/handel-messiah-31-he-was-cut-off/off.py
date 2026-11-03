from orchestra import Orchestra

# Handel, Messiah, Part II, No. 31. He was cut off out of the land of the
# living (accompanied recitative, tenor). A from-memory arrangement for
# General MIDI baroque orchestra, the tenor singing without words: a few
# grave string chords moving from B minor towards the E major of the air to
# come, in Handel's manner; the notes are approximate.
SEED = 1771

PARTS = ("tenor", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

LINE = ("m4/4 r:1 f#4:1/2 f#4:1/2 b4:1 f#4:1/2 g4:1/2 | a4:1/2 g4:1/2 f#4:1 e4:1 r:1 | "
        "r:1 g#4:1/2 a4:1/2 b4:1 e5:1/2 b4:1/2 | c#5:1/2 b4:1/2 a4:1/2 g#4:1/2 a4:2 |")
CHORDS = "m4/4 d4+f#4+b4:4 | c#4+e4+a#4:2 b3+e4+g4:2 | b3+d4+g#4:4 | c#4+e4+a4:4 |"
BASS = "m4/4 b2:4 | f#2:2 e2:2 | e2:4 | a2:4 |"


def picture(orchestra):
    orchestra.play({"tenor": "!mp " + LINE, "violins": ("!pp " + CHORDS, 12), "violins 2": "!pp " + CHORDS,
                    "violas": ("!pp " + CHORDS, -12), "cellos": "!p " + BASS, "basses": ("!p " + BASS, -12),
                    "harpsichord": "!pp " + CHORDS}, bpm=56, to=50, label="he was cut off")


def off():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render(tail=3.0)
