from orchestra import Orchestra

# Handel, Messiah, Part I, No. 21. His yoke is easy, and his burthen is light
# (chorus). A from-memory arrangement for General MIDI baroque orchestra, the
# choir singing without words: the light B-flat major fugal chorus with long,
# easy runs on "easy" passed between the voices, closing Part I with a broad
# cadence, in Handel's manner; the notes are approximate.
SEED = 1761

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
YOKE = ("m4/4 bb4:1 d5:1/2 c5:1/2 bb4:1/4 c5 d5 eb5 f5 eb5 d5 c5 | "
        "d5:1/4 eb5 f5 g5 f5 eb5 d5 c5 bb4:1 r:1 |")
BURTHEN = "m4/4 f5:1 f5:1/2 eb5:1/2 d5:1 c5:1 | bb4:2 r:2 |"
HOLD = "m4/4 f4:4 | f4:2 r:2 |"
HOLD_D = "m4/4 d4:4 | d4:2 r:2 |"
CADENCE = {"s": "m4/4 d5:2 eb5:2 | c5:2 c5:1 bb4:1 | bb4:4 |",
           "a": "m4/4 bb4:2 bb4:2 | a4:2 a4:1 f4:1 | f4:4 |",
           "t": "m4/4 f4:2 g4:2 | f4:2 eb4:2 | d4:4 |",
           "b": "m4/4 bb2:2 eb3:2 | f3:2 f2:2 | bb2:4 |"}


def picture(orchestra):
    entries = [(0, "violins"), (-5, "violins 2"), (-12, "violas"), (-24, "cellos")]
    for i in range(4):
        # the newest entry sings the subject, the earlier ones hold on
        choir = [(("!f " + YOKE) if j == i else ("!mf " + HOLD), entries[j][0]) for j in range(i + 1)]
        parts = {"choir": choir, entries[i][1]: ("!f " + YOKE, entries[i][0]),
                 "harpsichord": "!mf m4/4 bb2+d3+f3:4 | f2+a2+c3:2 bb2+d3+f3:2 |"}
        if i == 3:
            parts["basses"] = ("!f " + YOKE, -36)
            parts["bassoons"] = ("!f " + YOKE, -24)
        orchestra.play(parts, bpm=108, label="his yoke is easy")
    orchestra.play({"choir": [("!f " + BURTHEN, 0), ("!f " + BURTHEN, -5), ("!f " + BURTHEN, -12), ("!f " + BURTHEN, -24)],
                    "violins": "!f " + BURTHEN, "oboes": "!f " + BURTHEN, "violins 2": ("!f " + BURTHEN, -5),
                    "violas": ("!f " + BURTHEN, -12), "cellos": ("!f " + BURTHEN, -24), "basses": ("!f " + BURTHEN, -36)},
                   bpm=108, label="his burthen is light")
    orchestra.play({"choir": [("!f " + YOKE, 0), ("!f " + YOKE, -5), "!f " + HOLD_D, ("!f " + HOLD, -24)],
                    "violins": "!f " + YOKE, "oboes": "!f " + YOKE, "violins 2": ("!f " + YOKE, -5),
                    "violas": "!f m4/4 d4:4 | d4:2 r:2 |", "cellos": ("!f " + HOLD, -24), "basses": ("!f " + HOLD, -36)},
                   bpm=108)
    orchestra.play({"choir": ["!f " + CADENCE[v] for v in "satb"], "violins": "!f " + CADENCE["s"],
                    "oboes": "!f " + CADENCE["s"], "violins 2": "!f " + CADENCE["a"], "violas": "!f " + CADENCE["t"],
                    "cellos": "!f " + CADENCE["b"], "basses": ("!f " + CADENCE["b"], -12), "bassoons": "!f " + CADENCE["b"],
                    "harpsichord": "!f " + CADENCE["b"]}, bpm=108, to=72, label="adagio close")


def easy():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
