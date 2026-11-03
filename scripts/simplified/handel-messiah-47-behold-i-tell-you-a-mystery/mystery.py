from orchestra import Orchestra

# Handel, Messiah, Part III, No. 47. Behold, I tell you a mystery
# (accompanied recitative, bass). A from-memory arrangement for General MIDI
# baroque orchestra, the bass singing without words: quiet sustained strings,
# then a stir "in a moment, in the twinkling of an eye, at the last trumpet",
# leading to D major, in Handel's manner; the notes are approximate.
SEED = 1787

PARTS = ("bass voice", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

LINE = ("m4/4 r:1 d3:1/2 d3:1/2 a3:1 f#3:1/2 g3:1/2 | a3:1 b3:1 e3:2 | "
        "r:1 c#4:1/2 c#4:1/2 a3:1 e3:1/2 f#3:1/2 | g3:1/2 g3:1/2 f#3:1/2 e3:1/2 f#3:1 r:1 | "
        "r:1/2 a3:1/2 a3:1/2 a3:1/2 d4:1 a3:1 | f#3:1/2 g3:1/2 a3:1 d3:2 |")
CHORDS = "m4/4 d3+f#3+a3:4 | e3+g3+b3:4 | e3+a3+c#4:4 | d3+a3+d4:4 | f#3+a3+d4:4 | e3+g3+a3:2 f#3+a3+d4:2 |"
BASS = "m4/4 d3:4 | g2:4 | a2:4 | f#2:4 | d3:4 | a2:2 d2:2 |"


def picture(orchestra):
    orchestra.play({"bass voice": "!mf " + LINE, "violins": ("!pp " + CHORDS, 12), "violins 2": "!pp " + CHORDS,
                    "violas": ("!pp " + CHORDS, -12), "cellos": "!p " + BASS, "basses": ("!p " + BASS, -12),
                    "harpsichord": "!pp " + CHORDS}, bpm=66, to=58, label="mystery")


def mystery():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render(tail=3.0)
