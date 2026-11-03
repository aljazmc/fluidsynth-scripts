from orchestra import Orchestra

# Handel, Messiah, Part II, No. 39. Their sound is gone out into all lands
# (chorus). A from-memory arrangement for General MIDI baroque orchestra, the
# choir singing without words: a short, flowing E-flat major chorus whose
# entries spread out "unto the ends of the world", in Handel's manner; the
# notes are approximate.
SEED = 1779

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# A tempo ordinario, 4/4
SOUND = "m4/4 eb5:1 bb4:1/2 c5:1/2 d5:1 eb5:1 | f5:1/2 g5 ab5 g5 f5:1 bb4:1 | eb5:1/2 d5 c5 bb4 ab4:1 g4:1 | f4:2 r:2 |"
HOLD = "m4/4 bb4:4 | bb4:4 | ab4:2 g4:2 | f4:2 r:2 |"
ENDS = {"s": "m4/4 g5:2 f5:2 | eb5:1 d5:1 c5:1 bb4:1 | c5:1 bb4:1 bb4:1 ab4:1 | g4:4 |",
        "a": "m4/4 eb5:2 d5:2 | c5:1 bb4:1 ab4:1 g4:1 | ab4:1 g4:1 f4:2 | eb4:4 |",
        "t": "m4/4 bb4:2 bb4:2 | g4:2 eb4:2 | eb4:2 d4:2 | bb3:4 |",
        "b": "m4/4 eb3:2 bb2:2 | c3:2 g2:2 | ab2:2 bb2:2 | eb2:4 |"}


def picture(orchestra):
    entries = [(0, "violins"), (-5, "violins 2"), (-12, "violas"), (-24, "cellos")]
    for i in range(4):
        choir = [(("!f " + SOUND) if j == i else ("!mf " + HOLD), entries[j][0]) for j in range(i + 1)]
        parts = {"choir": choir, entries[i][1]: ("!f " + SOUND, entries[i][0]),
                 "harpsichord": "!mf m4/4 eb3+g3+bb3:4 | bb2+d3+f3:4 | ab2+c3+eb3:4 | bb2+d3+f3:4 |"}
        if i == 3:
            parts["basses"] = ("!f " + SOUND, -36)
        orchestra.play(parts, bpm=96, label="their sound is gone out")
    orchestra.play({"choir": [f"!f " + ENDS[v] for v in "satb"], "violins": "!f " + ENDS["s"], "oboes": "!f " + ENDS["s"],
                    "violins 2": "!f " + ENDS["a"], "violas": "!f " + ENDS["t"], "cellos": "!f " + ENDS["b"],
                    "basses": ("!f " + ENDS["b"], -12), "bassoons": "!f " + ENDS["b"], "harpsichord": "!f " + ENDS["b"]},
                   bpm=96, to=72, label="unto the ends of the world")


def out():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
