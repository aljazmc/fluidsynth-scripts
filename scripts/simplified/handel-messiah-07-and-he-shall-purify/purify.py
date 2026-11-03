from orchestra import Orchestra

# Handel, Messiah, Part I, No. 7. And he shall purify (chorus). A from-memory
# arrangement for General MIDI baroque orchestra, the choir singing without
# words: a G minor fugal chorus whose long running semiquavers on "purify"
# pass from sopranos to altos, tenors and basses, ending in block chords "that
# they may offer unto the Lord", in Handel's manner; the notes are
# approximate.
SEED = 1747

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
SUBJECT = ("m4/4 d5:1 d5:1/2 d5:1/2 g5:1/4 f5 eb5 d5 c5 bb4 a4 g4 | "
           "a4:1/4 bb4 c5 d5 eb5 d5 c5 bb4 a4:1 r:1 |")
COUNTER = "m4/4 bb4:2 a4:2 | g4:1 f#4:1 g4:2 |"
OFFER_S = "m4/4 bb4:1 bb4:1 c5:1 d5:1 | eb5:2 d5:2 | c5:1 bb4:1 a4:2 | g4:4 |"
OFFER_A = "m4/4 g4:1 g4:1 g4:1 f4:1 | g4:2 g4:2 | g4:1 g4:1 f#4:2 | d4:4 |"
OFFER_T = "m4/4 d4:1 d4:1 eb4:1 d4:1 | bb3:2 bb3:2 | eb4:1 d4:1 d4:2 | bb3:4 |"
OFFER_B = "m4/4 g2:1 g3:1 c3:1 bb2:1 | eb2:2 g2:2 | c3:1 d3:1 d2:2 | g2:4 |"


def picture(orchestra):
    entries = [(0, "violins"), (-7, "violins 2"), (-12, "violas"), (-24, "cellos")]
    for i, (shift, part) in enumerate(entries):
        choir = []
        parts = {}
        for j, (s, p) in enumerate(entries[:i + 1]):
            text = ("!f " + SUBJECT) if j == i else ("!mf " + COUNTER)
            choir.append((text, s))
            parts[p] = (text, s)
        while len(choir) < 4:
            choir.append("m4/4 r:4 | r:4 |")
        parts["choir"] = choir
        parts["basses"] = ("!mf m4/4 g2:2 d2:2 | d2:2 g1:2 |", 0) if i < 3 else ("!f " + SUBJECT, -36)
        parts["harpsichord"] = "!mf m4/4 g2+bb2+d3:2 d2+f#2+a2:2 | d2+f#2+a2:2 g2+bb2+d3:2 |"
        orchestra.play(parts, bpm=100, label="entry")
    orchestra.play({"choir": [("!f " + SUBJECT, 0), ("!f " + SUBJECT, -7), ("!f " + COUNTER, -12), ("!f " + COUNTER, -24)],
                    "violins": "!f " + SUBJECT, "oboes": "!f " + SUBJECT, "violins 2": ("!f " + SUBJECT, -7),
                    "violas": ("!f " + COUNTER, -12), "cellos": ("!f " + COUNTER, -24), "basses": ("!f " + COUNTER, -36),
                    "bassoons": ("!f " + COUNTER, -24)}, bpm=100, label="stretto")
    orchestra.play({"choir": ["!f " + OFFER_S, "!f " + OFFER_A, "!f " + OFFER_T, "!f " + OFFER_B],
                    "violins": "!f " + OFFER_S, "oboes": "!f " + OFFER_S, "violins 2": "!f " + OFFER_A,
                    "violas": "!f " + OFFER_T, "cellos": "!f " + OFFER_B, "basses": ("!f " + OFFER_B, -12),
                    "bassoons": "!f " + OFFER_B, "harpsichord": "!f " + OFFER_B},
                   bpm=100, to=72, label="that they may offer")


def purify():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
