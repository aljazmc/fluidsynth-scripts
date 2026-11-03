from orchestra import Orchestra

# Handel, Messiah, Part II, No. 33. Lift up your heads, O ye gates (chorus). A
# from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: the F major chorus as a dialogue between high and
# low voices, "Lift up your heads" - "Who is this King of glory?" - "The Lord
# strong and mighty", growing to the full choir's "the King of glory", in
# Handel's manner; the notes are approximate.
SEED = 1773

PARTS = ("choir", "oboes", "bassoons", "horns", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# A tempo ordinario, 4/4
LIFT = "m4/4 c5:1 a4:1/2 c5:1/2 f5:2 | e5:1 d5:1/2 c5:1/2 d5:1 bb4:1 | c5:2 r:2 |"
LIFT_LOW = "m4/4 a4:1 f4:1/2 a4:1/2 c5:2 | c5:1 bb4:1/2 a4:1/2 bb4:1 g4:1 | a4:2 r:2 |"
WHO = "m4/4 r:1 c4:1/2 d4:1/2 e4:1 f4:1 | g4:1 g4:1/2 g4:1/2 c4:2 |"
WHO_LOW = "m4/4 r:1 e3:1/2 f3:1/2 g3:1 a3:1 | c3:1 c3:1/2 c3:1/2 c3:2 |"
MIGHTY = {"s": "m4/4 f5:1 f5:1/2 f5:1/2 c5:1 a4:1 | bb4:1 c5:1 f4:2 |",
          "a": "m4/4 c5:1 c5:1/2 c5:1/2 a4:1 f4:1 | f4:1 e4:1 c4:2 |",
          "t": "m4/4 a4:1 a4:1/2 a4:1/2 f4:1 c4:1 | d4:1 g4:1 a3:2 |",
          "b": "m4/4 f3:1 f3:1/2 f3:1/2 f3:1 f3:1 | bb2:1 c3:1 f2:2 |"}
KING = {"s": "m4/4 a5:2 g5:2 | f5:1 e5:1 d5:1 c5:1 | f5:4 |",
        "a": "m4/4 c5:2 c5:2 | a4:1 g4:1 bb4:1 a4:1 | a4:4 |",
        "t": "m4/4 f4:2 e4:2 | c4:1 c4:1 f4:1 e4:1 | f4:4 |",
        "b": "m4/4 f3:2 c3:2 | a2:1 c3:1 bb2:1 c3:1 | f2:4 |"}


def tutti(orchestra, voices, dynamic, label, **kwargs):
    orchestra.play({"choir": [f"!{dynamic} " + voices[v] for v in "satb"], "violins": f"!{dynamic} " + voices["s"],
                    "violins 2": f"!{dynamic} " + voices["a"], "violas": f"!{dynamic} " + voices["t"],
                    "cellos": f"!{dynamic} " + voices["b"], "basses": (f"!{dynamic} " + voices["b"], -12),
                    "oboes": f"!{dynamic} " + voices["s"], "bassoons": f"!{dynamic} " + voices["b"],
                    "horns": (f"!{dynamic} " + voices["t"], 0), "harpsichord": "!mf " + voices["b"]},
                   label=label, **kwargs)


def picture(orchestra):
    for _ in range(2):
        orchestra.play({"choir": ["!f " + LIFT, "!f " + LIFT_LOW], "violins": "!f " + LIFT, "violins 2": "!f " + LIFT_LOW,
                        "oboes": "!f " + LIFT, "cellos": "!mf m4/4 f3:2 a2:2 | c3:2 g2:2 | f2:2 r:2 |",
                        "harpsichord": "!mf m4/4 f3+a3+c4:2 f3+a3+c4:2 | c3+e3+g3:2 c3+e3+g3:2 | f3+a3+c4:2 r:2 |"},
                       bpm=96, label="lift up your heads")
        orchestra.play({"choir": [("!mf " + WHO, 12), "!mf " + WHO, "!mf " + WHO_LOW], "violas": "!mf " + WHO,
                        "cellos": "!mf " + WHO_LOW, "basses": ("!mf " + WHO_LOW, -12)}, bpm=96, label="who is this King")
        tutti(orchestra, MIGHTY, "f", "the Lord strong and mighty", bpm=96)
    tutti(orchestra, KING, "ff", "the King of glory", bpm=96)
    tutti(orchestra, MIGHTY, "ff", "the Lord of hosts", bpm=96)
    tutti(orchestra, KING, "ff", "he is the King of glory", bpm=96, to=72)


def heads():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
