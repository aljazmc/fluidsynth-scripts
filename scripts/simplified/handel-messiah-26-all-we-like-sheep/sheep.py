from orchestra import Orchestra

# Handel, Messiah, Part II, No. 26. All we like sheep have gone astray
# (chorus). A from-memory arrangement for General MIDI baroque orchestra, the
# choir singing without words: the cheerful F major "All we like sheep", the
# voices wandering off in runs "have gone astray", "we have turned every one
# to his own way", and the sudden Adagio in F minor "and the Lord hath laid on
# him the iniquity of us all" follow Handel, the notes are approximate.
SEED = 1766

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "organ", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro moderato, 4/4
SHEEP = {"s": "m4/4 c5:1 c5:1/2 c5:1/2 a4:1 f4:1 | r:1 f5:1 e5:1 d5:1 | c5:2 r:2 |",
         "a": "m4/4 a4:1 a4:1/2 a4:1/2 f4:1 c4:1 | r:1 a4:1 g4:1 f4:1 | e4:2 r:2 |",
         "t": "m4/4 f4:1 f4:1/2 f4:1/2 c4:1 a3:1 | r:1 d4:1 c4:1 bb3:1 | g3:2 r:2 |",
         "b": "m4/4 f3:1 f3:1/2 f3:1/2 f2:1 f2:1 | r:1 bb2:1 c3:1 c3:1 | c3:2 r:2 |"}
ASTRAY = {"s": "m4/4 a4:1/4 bb4 c5 d5 e5 f5 g5 a5 g5 f5 e5 d5 c5 bb4 a4 g4 | f4:2 r:2 |",
          "a": "m4/4 f4:1/4 e4 d4 c4 d4 e4 f4 g4 a4 g4 f4 e4 d4 e4 f4 d4 | c4:2 r:2 |",
          "t": "m4/4 c4:1/4 d4 e4 f4 g4 f4 e4 d4 c4 bb3 a3 g3 a3 bb3 c4 bb3 | a3:2 r:2 |",
          "b": "m4/4 f2:1/4 g2 a2 bb2 c3 bb2 a2 g2 f2 e2 d2 c2 d2 e2 f2 c2 | f2:2 r:2 |"}
TURNED = {"s": "m4/4 c5:1 c5:1 bb4:1/2 a4:1/2 g4:1 | a4:1 bb4:1/2 a4:1/2 g4:2 | f4:2 r:2 |",
          "a": "m4/4 a4:1 a4:1 g4:1/2 f4:1/2 e4:1 | f4:1 g4:1/2 f4:1/2 e4:2 | c4:2 r:2 |",
          "t": "m4/4 f4:1 f4:1 d4:1/2 c4:1/2 c4:1 | c4:1 d4:1/2 c4:1/2 bb3:2 | a3:2 r:2 |",
          "b": "m4/4 f3:1 f3:1 bb2:1/2 c3:1/2 c3:1 | f2:1 bb2:1/2 f2:1/2 c3:2 | f2:2 r:2 |"}
# Adagio: and the Lord hath laid on him the iniquity of us all
LAID = {"s": "m4/4 c5:2 db5:2 | c5:2 bb4:2 | ab4:2 g4:2 | f4:4 | e4:4 |",
        "a": "m4/4 ab4:2 bb4:2 | ab4:2 g4:2 | f4:2 e4:2 | f4:4 | c4:4 |",
        "t": "m4/4 f4:2 f4:2 | f4:2 e4:2 | c4:2 c4:2 | db4:4 | c4:4 |",
        "b": "m4/4 f3:2 bb2:2 | c3:2 c3:2 | db3:2 c3:2 | bb2:4 | c3:4 |"}


def chorus(orchestra, voices, dynamic, label, **kwargs):
    orchestra.play({"choir": [f"!{dynamic} " + voices[v] for v in "satb"], "violins": f"!{dynamic} " + voices["s"],
                    "violins 2": f"!{dynamic} " + voices["a"], "violas": f"!{dynamic} " + voices["t"],
                    "cellos": f"!{dynamic} " + voices["b"], "basses": (f"!{dynamic} " + voices["b"], -12),
                    "oboes": f"!{dynamic} " + voices["s"], "bassoons": f"!{dynamic} " + voices["b"],
                    "harpsichord": f"!mf " + voices["b"]}, label=label, **kwargs)


def picture(orchestra):
    chorus(orchestra, SHEEP, "f", "all we like sheep", bpm=104)
    chorus(orchestra, ASTRAY, "f", "have gone astray", bpm=104)
    chorus(orchestra, SHEEP, "f", "all we like sheep", bpm=104, shift=-5)
    chorus(orchestra, ASTRAY, "f", "have gone astray", bpm=104, shift=-5)
    chorus(orchestra, TURNED, "f", "we have turned", bpm=104)
    chorus(orchestra, ASTRAY, "f", "every one to his own way", bpm=104)
    chorus(orchestra, SHEEP, "f", "all we like sheep", bpm=104, to=96)
    orchestra.play({"choir": [f"!p " + LAID[v] for v in "satb"], "violins 2": "!p " + LAID["a"],
                    "violas": "!p " + LAID["t"], "cellos": "!p " + LAID["b"], "basses": ("!p " + LAID["b"], -12),
                    "organ": ("!pp " + LAID["b"], 12)}, bpm=48, to=40, label="and the Lord hath laid on him")


def sheep():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render()
