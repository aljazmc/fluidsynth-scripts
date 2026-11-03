from orchestra import Orchestra

# Handel, Messiah, Part III, No. 53. Worthy is the Lamb that was slain - Amen
# (chorus). A from-memory arrangement for General MIDI baroque orchestra, the
# choir singing without words: the majestic D major Largo "Worthy is the
# Lamb", the flowing Andante "and hath redeemed us", the fugal "Blessing and
# honour, glory and power", and the great Amen fugue climbing from the basses
# to the whole choir with trumpets and drums, ending Adagio, follow Handel;
# the notes are approximate.
SEED = 1793

PARTS = ("choir", "oboes", "bassoons", "trumpets", "timpani", "harpsichord", "organ",
         "violins", "violins 2", "violas", "cellos", "basses")

WORTHY = {"s": "m4/4 d5:3/2 d5:1/2 d5:1 c#5:1 | d5:4 |",
          "a": "m4/4 a4:3/2 a4:1/2 a4:1 a4:1 | a4:4 |",
          "t": "m4/4 f#4:3/2 f#4:1/2 f#4:1 e4:1 | f#4:4 |",
          "b": "m4/4 d3:3/2 d3:1/2 d3:1 a2:1 | d3:4 |",
          "timpani": "m4/4 d3:3/2 d3:1/2 d3:1 a2:1 | d3:4 |"}
REDEEMED = {"s": "m4/4 a4:1 b4:1/2 c#5:1/2 d5:1 e5:1 | f#5:1 e5:1/2 d5:1/2 c#5:1 b4:1 | a4:2 r:2 |",
            "a": "m4/4 f#4:1 g4:1/2 a4:1/2 a4:1 a4:1 | a4:1 a4:1 a4:1 g#4:1 | e4:2 r:2 |",
            "t": "m4/4 d4:1 d4:1/2 e4:1/2 f#4:1 c#4:1 | d4:1 e4:1/2 f#4:1/2 e4:1 e4:1 | c#4:2 r:2 |",
            "b": "m4/4 d3:1 g2:1/2 a2:1/2 b2:1 a2:1 | d3:1 c#3:1/2 b2:1/2 e3:1 e2:1 | a2:2 r:2 |"}
BLESSING = "m4/4 a3:2 d4:1 a3:1 | b3:1 c#4:1/2 d4:1/2 e4:1 a3:1 | d4:1/2 e4 f#4 g4 a4:1 a3:1 | d4:2 r:2 |"
AMEN = "m4/4 d3:2 a3:2 | f#3:1 g3:1 a3:1 b3:1 | a3:1 g3:1 f#3:1 e3:1 | d3:1 e3:1 f#3:2 | e3:1 d3:1 c#3:1 d3:1 | e3:2 a2:2 |"
AMEN_HOLD = "m4/4 a3:4 | a3:4 | a3:4 | a3:4 | a3:4 | a3:4 |"


def chorus(orchestra, voices, dynamic, label, **kwargs):
    parts = {"choir": [f"!{dynamic} " + voices[v] for v in "satb"], "violins": f"!{dynamic} " + voices["s"],
             "oboes": f"!{dynamic} " + voices["s"], "violins 2": f"!{dynamic} " + voices["a"],
             "violas": f"!{dynamic} " + voices["t"], "cellos": f"!{dynamic} " + voices["b"],
             "basses": (f"!{dynamic} " + voices["b"], -12), "bassoons": f"!{dynamic} " + voices["b"],
             "organ": (f"!mf " + voices["t"], 0), "harpsichord": "!mf " + voices["b"]}
    if "timpani" in voices:
        parts["timpani"] = f"!{dynamic} " + voices["timpani"]
        parts["trumpets"] = f"!{dynamic} " + voices["s"]
    orchestra.play(parts, label=label, **kwargs)


def picture(orchestra):
    for _ in range(2):
        chorus(orchestra, WORTHY, "ff", "worthy is the Lamb", bpm=52)
        chorus(orchestra, REDEEMED, "f", "and hath redeemed us", bpm=84)
    # Blessing and honour, glory and power: basses and tenors, then all
    orchestra.play({"choir": [("!f " + BLESSING, 0), ("!f " + BLESSING, -12)], "violas": ("!f " + BLESSING, 0),
                    "cellos": ("!f " + BLESSING, -12), "basses": ("!f " + BLESSING, -24),
                    "harpsichord": "!mf m4/4 d3+f#3+a3:4 | e3+g3+b3:2 a2+c#3+e3:2 | d3+f#3+a3:2 a2+c#3+e3:2 | d3+f#3+a3:2 r:2 |"},
                   bpm=100, label="blessing and honour")
    orchestra.play({"choir": [("!f " + BLESSING, 24), ("!f " + BLESSING, 12), ("!f " + BLESSING, 0), ("!f " + BLESSING, -12)],
                    "violins": ("!f " + BLESSING, 24), "violins 2": ("!f " + BLESSING, 12), "violas": "!f " + BLESSING,
                    "cellos": ("!f " + BLESSING, -12), "basses": ("!f " + BLESSING, -24), "trumpets": ("!f " + BLESSING, 24),
                    "timpani": "!f m4/4 d3:2 a2:2 | a2:2 a2:2 | d3:1 d3 a2 a2 | d3:2 r:2 |"}, bpm=100)

    # the Amen fugue, from the basses up
    entries = [(-12, "cellos"), (0, "violas"), (7, "violins 2"), (12, "violins")]
    for i in range(4):
        # the newest entry sings the subject, the earlier ones hold on
        choir = [(("!f " + AMEN) if j == i else ("!mf " + AMEN_HOLD), entries[j][0]) for j in range(i + 1)]
        parts = {"choir": choir, entries[i][1]: ("!f " + AMEN, entries[i][0]), "organ": ("!mf " + AMEN_HOLD, -12),
                 "harpsichord": "!mf m4/4 d3+f#3+a3:4 | d3+g3+b3:4 | d3+f#3+a3:4 | d3+f#3+a3:4 | a2+c#3+e3:4 | a2+c#3+e3:4 |"}
        if i == 0:
            parts["basses"] = ("!f " + AMEN, -24)
            parts["bassoons"] = ("!f " + AMEN, -12)
        orchestra.play(parts, bpm=88, label="amen")
    orchestra.play({"choir": [("!ff " + AMEN, 12), ("!ff " + AMEN, 7), ("!ff " + AMEN, 0), ("!ff " + AMEN, -12)],
                    "violins": ("!ff " + AMEN, 12), "oboes": ("!ff " + AMEN, 12), "violins 2": ("!ff " + AMEN, 7),
                    "violas": "!ff " + AMEN, "cellos": ("!ff " + AMEN, -12), "basses": ("!ff " + AMEN, -24),
                    "trumpets": ("!ff " + AMEN, 12), "organ": ("!f " + AMEN, -12),
                    "timpani": "!ff m4/4 d3:2 a2:2 | d3:1 a2 d3 a2 | a2:1 a2 d3 a2 | d3:1 a2 d3:2 | a2:1 d3 a2 d3 | a2:2 a2:2 |"},
                   bpm=88, label="amen, all")
    # the last Amen, Adagio, with a pause before it
    final = {"s": "m4/4 d5:2 d5:2 | e5:4 | d5:4 |", "a": "m4/4 a4:2 b4:2 | a4:4 | a4:4 |",
             "t": "m4/4 f#4:2 g4:2 | e4:4 | f#4:4 |", "b": "m4/4 d3:2 g2:2 | a2:4 | d2:4 |",
             "timpani": "m4/4 d3:2 d3:2 | a2:4 | d3:4 |"}
    orchestra.rest(0.8)
    chorus(orchestra, final, "fff", "adagio amen", bpm=44, to=36)


def amen():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=105)
    picture(orchestra)
    return orchestra.render(tail=6.0)
