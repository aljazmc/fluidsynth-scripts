from orchestra import Orchestra

# Handel, Messiah, Part III, No. 51. But thanks be to God (chorus). A
# from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: an energetic E-flat major chorus that grows straight
# out of the duet, entries piling up on "but thanks, thanks be to God, who
# giveth us the victory", in Handel's manner; the notes are approximate.
SEED = 1791

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
THANKS = "m4/4 bb4:1 bb4:1/2 bb4:1/2 eb5:1 eb5:1 | d5:1/2 c5:1/2 bb4:1 ab4:1 g4:1 | f4:1/2 g4:1/2 ab4:1 g4:2 |"
HOLD = "m4/4 g4:4 | f4:4 | eb4:4 |"
VICTORY = {"s": "m4/4 eb5:1 f5:1 g5:1 eb5:1 | ab5:2 g5:1 f5:1 | eb5:1 d5:1 eb5:2 |",
           "a": "m4/4 bb4:1 bb4:1 bb4:1 bb4:1 | c5:2 bb4:1 ab4:1 | g4:1 f4:1 g4:2 |",
           "t": "m4/4 g4:1 f4:1 eb4:1 g4:1 | eb4:2 eb4:1 d4:1 | bb3:1 bb3:1 bb3:2 |",
           "b": "m4/4 eb3:1 d3:1 c3:1 g2:1 | ab2:2 bb2:2 | bb2:1 bb1:1 eb2:2 |"}


def picture(orchestra):
    entries = [(0, "violins"), (-5, "violins 2"), (-12, "violas"), (-24, "cellos")]
    for i in range(4):
        choir = [(("!f " + THANKS) if j == i else ("!mf " + HOLD), entries[j][0]) for j in range(i + 1)]
        parts = {"choir": choir, entries[i][1]: ("!f " + THANKS, entries[i][0]),
                 "harpsichord": "!mf m4/4 eb3+g3+bb3:4 | bb2+d3+f3:4 | eb3+g3+bb3:4 |"}
        if i == 3:
            parts["basses"] = ("!f " + THANKS, -36)
            parts["bassoons"] = ("!f " + THANKS, -24)
        orchestra.play(parts, bpm=112, label="but thanks be to God")
    for dynamic in ("f", "ff"):
        orchestra.play({"choir": [f"!{dynamic} " + VICTORY[v] for v in "satb"], "violins": f"!{dynamic} " + VICTORY["s"],
                        "oboes": f"!{dynamic} " + VICTORY["s"], "violins 2": f"!{dynamic} " + VICTORY["a"],
                        "violas": f"!{dynamic} " + VICTORY["t"], "cellos": f"!{dynamic} " + VICTORY["b"],
                        "basses": (f"!{dynamic} " + VICTORY["b"], -12), "bassoons": f"!{dynamic} " + VICTORY["b"],
                        "harpsichord": f"!{dynamic} " + VICTORY["b"]}, bpm=112, to=88 if dynamic == "ff" else None,
                       label="the victory")


def god():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
