from orchestra import Orchestra

# Handel, Messiah, Part I, No. 12. For unto us a child is born (chorus). A
# from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: the light G major running entries "For unto us a
# child is born" with long semiquaver runs, the dotted "and the government
# shall be upon his shoulder" and the hammered chords "Wonderful,
# Counsellor, the mighty God" over rushing strings follow Handel, the notes
# are approximate.
SEED = 1752

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Andante allegro, 4/4
FOR = "m4/4 r:1/2 d5:1/2 c5:1/2 b4:1/2 a4:1 g4:1 | r:1/2 d5:1/2 e5:1/2 f#5:1/2 g5:1 r:1 |"
BORN = ("m4/4 g5:1/4 f#5 e5 f#5 g5 f#5 e5 d5 e5 d5 c5 d5 e5 d5 c5 b4 | "
        "c5:1/4 b4 a4 b4 c5 b4 a4 g4 a4:1 r:1 |")
GOVERNMENT_S = "m4/4 d5:3/4 d5:1/4 d5:1 r:1 d5:3/4 d5:1/4 | e5:1 d5:1/2 c5:1/2 b4:1 r:1 |"
GOVERNMENT_A = "m4/4 b4:3/4 b4:1/4 b4:1 r:1 b4:3/4 b4:1/4 | c5:1 b4:1/2 a4:1/2 g4:1 r:1 |"
GOVERNMENT_T = "m4/4 g4:3/4 g4:1/4 g4:1 r:1 g4:3/4 g4:1/4 | g4:1 g4:1/2 f#4:1/2 d4:1 r:1 |"
GOVERNMENT_B = "m4/4 g3:3/4 g3:1/4 g3:1 r:1 g3:3/4 g3:1/4 | c3:1 d3:1/2 d3:1/2 g2:1 r:1 |"
# Wonderful! Counsellor! The mighty God, the everlasting Father, the Prince of Peace!
WONDER = {
    "s": "m4/4 g5:2^ r:2 | e5:2^ r:2 | d5:1 d5:1/2 d5:1/2 d5:1 c5:1 | b4:1 a4:1 g4:2 |",
    "a": "m4/4 d5:2^ r:2 | c5:2^ r:2 | b4:1 b4:1/2 b4:1/2 a4:1 a4:1 | g4:1 f#4:1 d4:2 |",
    "t": "m4/4 b4:2^ r:2 | g4:2^ r:2 | g4:1 g4:1/2 g4:1/2 f#4:1 e4:1 | d4:1 d4:1 b3:2 |",
    "b": "m4/4 g3:2^ r:2 | c3:2^ r:2 | g2:1 g2:1/2 g2:1/2 d3:1 c3:1 | d3:1 d2:1 g2:2 |",
}
RUSH = "m4/4 " + " ".join(f"{a}:1/4 {b} {c} {d} " * 4 + "|" for a, b, c, d in (
    ("g5", "d5", "b4", "d5"), ("e5", "c5", "g4", "c5"), ("d5", "b4", "g4", "b4"), ("d5", "a4", "f#4", "a4")))


def tutti(s, a, t, b, dynamic, strings=None):
    parts = {"choir": [f"!{dynamic} " + x for x in (s, a, t, b)], "oboes": f"!{dynamic} " + s,
             "violins 2": f"!{dynamic} " + a, "violas": f"!{dynamic} " + t, "cellos": f"!{dynamic} " + b,
             "basses": (f"!{dynamic} " + b, -12), "bassoons": f"!{dynamic} " + b, "harpsichord": "!mf " + b}
    parts["violins"] = f"!{dynamic} " + (strings or s)
    return parts


def picture(orchestra):
    orchestra.play({"violins": "!mf " + FOR + " " + BORN[5:], "violins 2": ("!mf " + FOR, -12),
                    "cellos": "!mf m4/4 g2:2 g3:2 | g2:2 g3:2 | c3:2 d3:2 | d2:2 g2:2 |", "basses": "!mf m4/4 g1:2 g2:2 | g1:2 g2:2 | c2:2 d2:2 | d1:2 g1:2 |",
                    "harpsichord": "!mf m4/4 g2+b2+d3:4 | g2+b2+d3:4 | c3+e3+g3:2 d3+f#3+a3:2 | d3+f#3+a3:2 g2+b2+d3:2 |"},
                   bpm=104, label="ritornello")
    # sopranos, then tenors, each with their run on "born"
    orchestra.play({"choir": ["!f " + FOR + " " + BORN[5:]], "violins": "!mf " + FOR + " " + BORN[5:],
                    "cellos": "!mf m4/4 g2:4 | g2:4 | c3:2 d3:2 | g2:4 |"}, bpm=104, label="sopranos")
    orchestra.play({"choir": [("!f " + FOR + " " + BORN[5:], -12)], "violas": ("!mf " + FOR + " " + BORN[5:], -12),
                    "cellos": "!mf m4/4 g2:4 | g2:4 | c3:2 d3:2 | g2:4 |"}, bpm=104, label="tenors")
    orchestra.play({"choir": [("!f " + FOR + " " + BORN[5:], -7), ("!f " + FOR + " " + BORN[5:], -24)],
                    "violins 2": ("!mf " + FOR + " " + BORN[5:], -7), "cellos": ("!mf " + FOR + " " + BORN[5:], -24),
                    "basses": ("!mf " + FOR + " " + BORN[5:], -36)}, bpm=104, label="altos and basses")
    orchestra.play(tutti(GOVERNMENT_S, GOVERNMENT_A, GOVERNMENT_T, GOVERNMENT_B, "f"), bpm=104, label="government")
    for dynamic in ("ff", "ff"):
        orchestra.play(tutti(WONDER["s"], WONDER["a"], WONDER["t"], WONDER["b"], dynamic, strings=RUSH),
                       bpm=104, label="Wonderful")
    alto = "m4/4 r:1/2 b4:1/2 a4:1/2 g4:1/2 f#4:1 d4:1 | r:1/2 b4:1/2 c5:1/2 a4:1/2 b4:1 r:1 | g4:4 | g4:2 f#4:2 |"
    orchestra.play(tutti(FOR + " " + BORN[5:], alto, "m4/4 b3:4 | b3:4 | c4:4 | d4:2 b3:2 |",
                         "m4/4 g2:4 | g2:4 | c3:2 d3:2 | d2:2 g2:2 |", "f"), bpm=104)
    orchestra.play(tutti(WONDER["s"], WONDER["a"], WONDER["t"], WONDER["b"], "ff", strings=RUSH), bpm=104, to=88)
    orchestra.play({"violins": "!f " + FOR, "violins 2": ("!f " + FOR, -12),
                    "cellos": "!f m4/4 g2:2 g3:2 | d3:2 g2:2 |", "basses": "!f m4/4 g1:2 g2:2 | d2:2 g1:2 |",
                    "harpsichord": "!f m4/4 g2+b2+d3:4 | d2+f#2+a2:2 g2+b2+d3:2 |"}, bpm=88, to=72, label="end")


def born():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
