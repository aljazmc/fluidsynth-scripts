from orchestra import Orchestra

# Handel, Messiah, Part II, No. 35. Let all the angels of God worship him
# (chorus). A from-memory arrangement for General MIDI baroque orchestra, the
# choir singing without words: a brisk D major double fugue, two subjects
# heard together from the start, in Handel's manner; the notes are
# approximate.
SEED = 1775

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
FIRST = "m4/4 d5:1 a4:1 b4:1/2 c#5:1/2 d5:1 | e5:1 a4:1 f#5:1 e5:1 | d5:1/2 c#5 b4 a4 g4:1 c#5:1 | d5:2 r:2 |"
SECOND = "m4/4 r:2 f#4:1/2 g4 a4 f#4 | g4:1/2 a4 b4 g4 a4:1 a4:1 | b4:1 e4:1 e4:1 a4:1 | f#4:2 r:2 |"
BASS = "m4/4 d3:1 f#3:1 g3:1 f#3:1 | c#3:1 a2:1 d3:1 a2:1 | b2:1 g2:1 a2:1 a2:1 | d2:2 r:2 |"


def picture(orchestra):
    plan = [(FIRST, 0, SECOND, -12), (FIRST, -12, SECOND, -12), (FIRST, -7, SECOND, 5), (FIRST, -24, SECOND, -12)]
    names = ("soprano and alto", "tenor and alto", "alto and soprano", "bass and tenor")
    for (a, sa, b, sb), name in zip(plan, names):
        orchestra.play({"choir": [("!f " + a, sa), ("!f " + b, sb)], "violins": ("!f " + a, max(sa, 0)),
                        "violins 2": ("!f " + b, sb), "violas": ("!mf " + BASS, 12), "cellos": "!f " + BASS,
                        "basses": ("!f " + BASS, -12), "harpsichord": ("!mf " + BASS, 12)}, bpm=116, label=name)
    orchestra.play({"choir": ["!ff " + FIRST, ("!ff " + SECOND, 0), ("!ff " + FIRST, -12), ("!ff " + BASS, 0)],
                    "violins": "!ff " + FIRST, "oboes": "!ff " + FIRST, "violins 2": "!ff " + SECOND,
                    "violas": ("!ff " + FIRST, -12), "cellos": "!ff " + BASS, "basses": ("!ff " + BASS, -12),
                    "bassoons": "!ff " + BASS}, bpm=116, to=96, label="all together")
    orchestra.play({"choir": ["!f m4/4 d5:4 |", "!f m4/4 a4:4 |", "!f m4/4 f#4:4 |", "!f m4/4 d3:4 |"],
                    "violins": "!f m4/4 d5+f#5:4 |", "violas": "!f m4/4 a4:4 |", "cellos": "!f m4/4 d3:4 |",
                    "basses": "!f m4/4 d2:4 |", "harpsichord": "!f m4/4 d3+f#3+a3:4 |"}, bpm=96, label="end")


def him():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
