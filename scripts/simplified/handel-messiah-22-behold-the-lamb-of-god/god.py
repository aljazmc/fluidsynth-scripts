from orchestra import Orchestra

# Handel, Messiah, Part II, No. 22. Behold the Lamb of God (chorus). A
# from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: the solemn G minor Largo opening Part II, its
# dotted rhythms weighing on every step, in Handel's manner; the notes are
# approximate.
SEED = 1762

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "organ", "violins", "violins 2", "violas", "cellos", "basses")

# Largo, 4/4
S = ("m4/4 d5:3/2 d5:1/2 g5:3/2 f#5:1/2 | g5:2 d5:2 | eb5:3/2 eb5:1/2 c5:3/2 bb4:1/2 | a4:4 | "
     "bb4:3/2 c5:1/2 d5:3/2 eb5:1/2 | f5:3/2 eb5:1/2 d5:1 c5:1 | bb4:1 a4:1 g4:1 f#4:1 | g4:4 |")
A = ("m4/4 bb4:3/2 bb4:1/2 bb4:3/2 a4:1/2 | bb4:2 a4:2 | g4:3/2 g4:1/2 a4:3/2 g4:1/2 | f#4:4 | "
     "g4:3/2 a4:1/2 bb4:3/2 c5:1/2 | d5:3/2 c5:1/2 bb4:1 a4:1 | g4:1 f#4:1 eb4:1 d4:1 | d4:4 |")
T = ("m4/4 g4:3/2 g4:1/2 d4:3/2 d4:1/2 | d4:2 f#4:2 | eb4:3/2 eb4:1/2 eb4:3/2 d4:1/2 | d4:4 | "
     "d4:3/2 eb4:1/2 f4:3/2 g4:1/2 | a4:3/2 g4:1/2 f4:1 eb4:1 | d4:1 c4:1 bb3:1 a3:1 | bb3:4 |")
B = ("m4/4 g3:3/2 g3:1/2 bb2:3/2 d3:1/2 | g2:2 d3:2 | c3:3/2 c3:1/2 f#2:3/2 g2:1/2 | d3:4 | "
     "g2:3/2 f2:1/2 bb2:3/2 c3:1/2 | d3:3/2 eb3:1/2 f3:1 f2:1 | g2:1 a2:1 c3:1 d3:1 | g2:4 |")


def picture(orchestra):
    orchestra.play({"violins": "!mf " + S, "violins 2": "!mf " + A, "violas": "!mf " + T, "cellos": "!mf " + B,
                    "basses": ("!mf " + B, -12), "oboes": "!mf " + S, "harpsichord": "!p " + B}, bpm=54, label="ritornello")
    for dynamic in ("f", "mf"):
        orchestra.play({"choir": [f"!{dynamic} " + x for x in (S, A, T, B)], "violins": f"!{dynamic} " + S,
                        "violins 2": f"!{dynamic} " + A, "violas": f"!{dynamic} " + T, "cellos": f"!{dynamic} " + B,
                        "basses": (f"!{dynamic} " + B, -12), "oboes": f"!{dynamic} " + S, "bassoons": f"!{dynamic} " + B,
                        "organ": ("!p " + B, 12)}, bpm=54, to=48 if dynamic == "mf" else None, label="behold the Lamb")


def god():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render()
