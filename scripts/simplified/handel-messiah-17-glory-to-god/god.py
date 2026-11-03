from orchestra import Orchestra

# Handel, Messiah, Part I, No. 17. Glory to God (chorus). A from-memory
# arrangement for General MIDI baroque orchestra, the choir singing without
# words: the trumpets' first entry in the work, the high voices' bright
# "Glory to God in the highest" answered by the low "and peace on earth",
# the fugal "good will towards men" and the strings fading away at the end
# follow Handel, the notes are approximate.
SEED = 1757

PARTS = ("choir", "oboes", "bassoons", "trumpets", "timpani", "harpsichord",
         "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
GLORY = {"s": "m4/4 d5:1 d5:1/2 e5:1/2 f#5:1 e5:1/2 d5:1/2 | a5:2 r:2 |",
         "a": "m4/4 a4:1 a4:1/2 a4:1/2 a4:1 a4:1/2 a4:1/2 | c#5:2 r:2 |",
         "t": "m4/4 f#4:1 f#4:1/2 g4:1/2 a4:1 g4:1/2 f#4:1/2 | e4:2 r:2 |"}
PEACE = "m4/4 a2:1 a2:1/2 a2:1/2 a2:1 a2:1 | d2:2 r:2 |"
GOODWILL = "m4/4 d5:1/2 a4 b4 c#5 d5:1 a4:1 | b4:1/2 c#5 d5 e5 f#5:1 e5:1 | d5:1/2 c#5 b4 a4 g4:1 c#5:1 | d5:2 r:2 |"
HOLD = "m4/4 d5:4 | d5:4 | d5:2 c#5:2 | d5:2 r:2 |"
FLUTTER = "m4/4 " + " ".join(f"{a}:1/4 {b} {a} {b} " * 4 + "|" for a, b in (("d5", "f#5"), ("a4", "c#5"), ("d5", "f#5"), ("a4", "e5")))


def picture(orchestra):
    for _ in range(2):
        orchestra.play({"choir": ["!f " + GLORY["s"], "!f " + GLORY["a"], "!f " + GLORY["t"]],
                        "trumpets": "!f " + GLORY["s"], "violins": "!f " + GLORY["s"],
                        "violins 2": "!f " + GLORY["a"], "violas": "!f " + GLORY["t"], "oboes": "!f " + GLORY["s"],
                        "timpani": "!f m4/4 d3:1 d3:1/2 d3:1/2 a2:1 d3:1 | a2:2 r:2 |"}, bpm=112, label="glory")
        orchestra.play({"choir": [("!p " + PEACE, 24), ("!p " + PEACE, 12), "!p " + PEACE],
                        "cellos": "!p " + PEACE, "basses": ("!p " + PEACE, -12), "bassoons": "!p " + PEACE,
                        "harpsichord": "!p m4/4 a2+c#3+e3:4 | d3+f#3+a3:2 r:2 |"}, bpm=112, label="peace on earth")
    entries = [(0, "violins"), (-7, "violins 2"), (-12, "violas"), (-24, "cellos")]
    for i in range(4):
        # the newest entry sings the subject, the earlier ones hold on
        choir = [(("!f " + GOODWILL) if j == i else ("!mf " + HOLD), entries[j][0]) for j in range(i + 1)]
        parts = {"choir": choir, entries[i][1]: ("!f " + GOODWILL, entries[i][0]),
                 "harpsichord": "!mf m4/4 d3+f#3+a3:4 | g2+b2+d3:4 | e3+g3+a3:4 | d3+f#3+a3:2 r:2 |"}
        if i == 3:
            parts["basses"] = ("!f " + GOODWILL, -36)
        orchestra.play(parts, bpm=112, label="good will towards men")
    orchestra.play({"choir": ["!f " + GLORY["s"], "!f " + GLORY["a"], "!f " + GLORY["t"], ("!f " + PEACE, 12)],
                    "trumpets": "!f " + GLORY["s"], "violins": "!f " + GLORY["s"], "violins 2": "!f " + GLORY["a"],
                    "violas": "!f " + GLORY["t"], "cellos": ("!f " + PEACE, 12), "basses": "!f " + PEACE,
                    "timpani": "!f m4/4 d3:1 d3:1/2 d3:1/2 a2:1 d3:1 | a2:2 r:2 |"}, bpm=112)
    # the heavenly host fades away
    orchestra.play({"violins": "!mp " + FLUTTER + " !>pp", "violins 2": ("!p " + FLUTTER, -12),
                    "cellos": "!p m4/4 d3:4 | a2:4 | d3:4 | a2:4 |"}, bpm=112, to=96, label="fading")
    orchestra.play({"violins": "!pp m4/4 d5+f#5:4 |", "violins 2": "!pp m4/4 a4:4 |", "cellos": "!pp m4/4 d3:4 |"},
                   bpm=96)


def god():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
