from orchestra import Orchestra

# Handel, Messiah, Part II, No. 28. He trusted in God that he would deliver
# him (chorus). A from-memory arrangement for General MIDI baroque orchestra,
# the choir singing without words: the crowd's jeering C minor fugue, its
# subject spat out by the basses first, and its stretto pile-up at the end,
# in Handel's manner; the notes are approximate.
SEED = 1768

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
SUBJECT = "m4/4 c3:1 g3:1/2 g3:1/2 ab3:1 g3:1 | f3:1/2 eb3:1/2 d3:1/2 c3:1/2 b2:1 g2:1 | c3:1/2 d3 eb3 f3 g3:1 c3:1 |"
COUNTER = "m4/4 eb3:2 d3:2 | c3:2 d3:2 | eb3:2 c3:2 |"
ENTRIES = (("bass", 0, "cellos"), ("tenor", 12, "violas"), ("alto", 19, "violins 2"), ("soprano", 24, "violins"))


def picture(orchestra):
    sung = []
    for name, shift, strings in ENTRIES:
        sung = [(COUNTER, s) for _, s in sung] + [(SUBJECT, shift)]
        parts = {"choir": [("!f " + text, s) for text, s in sung], strings: ("!f " + SUBJECT, shift),
                 "harpsichord": ("!mf " + COUNTER, 12)}
        if name == "bass":
            parts["basses"] = ("!f " + SUBJECT, -12)
            parts["bassoons"] = "!f " + SUBJECT
        orchestra.play(parts, bpm=112, label=f"{name} entry")
    orchestra.play({"choir": [("!ff " + SUBJECT, 24), ("!ff " + SUBJECT, 19), ("!ff " + SUBJECT, 12), "!ff " + SUBJECT],
                    "violins": ("!ff " + SUBJECT, 24), "oboes": ("!ff " + SUBJECT, 24), "violins 2": ("!ff " + SUBJECT, 19),
                    "violas": ("!ff " + SUBJECT, 12), "cellos": "!ff " + SUBJECT, "basses": ("!ff " + SUBJECT, -12),
                    "bassoons": "!ff " + SUBJECT}, bpm=112, label="stretto")
    orchestra.play({"choir": ["!f m4/4 g5:2 g5:2 | c6:4 |", "!f m4/4 d5:2 d5:2 | eb5:4 |", "!f m4/4 b4:2 b4:2 | c5:4 |",
                              "!f m4/4 g3:2 g2:2 | c3:4 |"], "violins": "!f m4/4 g5:2 g5:2 | c6:4 |",
                    "violins 2": "!f m4/4 d5:2 d5:2 | eb5:4 |", "violas": "!f m4/4 b4:2 b4:2 | c5:4 |",
                    "cellos": "!f m4/4 g3:2 g2:2 | c3:4 |", "basses": "!f m4/4 g2:2 g1:2 | c2:4 |",
                    "harpsichord": "!f m4/4 g2+b2+d3:4 | c3+eb3+g3:4 |"}, bpm=112, to=80, label="cadence")


def god():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
