from orchestra import Orchestra

# Handel, Messiah, Part II, No. 24. Surely he hath borne our griefs (chorus).
# A from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: the F minor Largo e staccato, block chords over the
# strings' insistent dotted rhythm, and the chromatic, shuddering "he was
# wounded for our transgressions", follows Handel; the notes are
# approximate.
SEED = 1764

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "organ", "violins", "violins 2", "violas", "cellos", "basses")

# Largo e staccato, 4/4
SURELY = {"s": "m4/4 c5:2 r:1 c5:1 | db5:2 r:1 bb4:1 | c5:1 c5:1 f5:1 e5:1 | f5:2 r:2 |",
          "a": "m4/4 ab4:2 r:1 ab4:1 | bb4:2 r:1 g4:1 | ab4:1 ab4:1 ab4:1 g4:1 | ab4:2 r:2 |",
          "t": "m4/4 f4:2 r:1 f4:1 | f4:2 r:1 e4:1 | f4:1 f4:1 db4:1 c4:1 | c4:2 r:2 |",
          "b": "m4/4 f3:2 r:1 f3:1 | bb2:2 r:1 c3:1 | f2:1 ab2:1 bb2:1 c3:1 | f2:2 r:2 |"}
DOTS = "m4/4 " + " ".join(f"{c}:3/4 {c}:1/4 " * 4 + "|" for c in ("ab4+c5", "bb4+db5", "ab4+c5", "ab4+c5"))
WOUNDED = {"s": "m4/4 c5:1 db5:1 d5:1 eb5:1 | e5:2 f5:2 | db5:1 c5:1 bb4:1 ab4:1 | g4:4 |",
           "a": "m4/4 ab4:1 bb4:1 b4:1 c5:1 | c5:2 c5:2 | bb4:1 ab4:1 g4:1 f4:1 | e4:4 |",
           "t": "m4/4 f4:1 f4:1 f4:1 g4:1 | g4:2 ab4:2 | f4:1 f4:1 e4:1 db4:1 | c4:4 |",
           "b": "m4/4 f3:1 f3:1 f3:1 f3:1 | c3:2 f3:2 | bb2:1 bb2:1 c3:1 c3:1 | c3:4 |"}


def chorus(orchestra, voices, dynamic, label, **kwargs):
    orchestra.play({"choir": [f"!{dynamic} " + voices[v] for v in "satb"], "violins": ("!f " + DOTS, 0),
                    "violins 2": f"!{dynamic} " + voices["a"], "violas": f"!{dynamic} " + voices["t"],
                    "cellos": f"!{dynamic} " + voices["b"], "basses": (f"!{dynamic} " + voices["b"], -12),
                    "oboes": f"!{dynamic} " + voices["s"], "bassoons": f"!{dynamic} " + voices["b"],
                    "organ": ("!p " + voices["b"], 12)}, bpm=52, label=label, **kwargs)


def picture(orchestra):
    chorus(orchestra, SURELY, "f", "surely")
    chorus(orchestra, SURELY, "f", "surely", shift=3)
    chorus(orchestra, WOUNDED, "mf", "he was wounded")
    chorus(orchestra, WOUNDED, "p", "bruised for our iniquities", shift=-2)
    chorus(orchestra, SURELY, "f", "the chastisement", to=44)
    orchestra.play({"choir": ["!f m4/4 c5:4 |", "!f m4/4 g4:4 |", "!f m4/4 e4:4 |", "!f m4/4 c3:4 |"],
                    "violins": "!f m4/4 c5+e5:4 |", "violas": "!f m4/4 g4:4 |", "cellos": "!f m4/4 c3:4 |",
                    "basses": "!f m4/4 c2:4 |", "organ": "!p m4/4 c3+e3+g3:4 |"}, bpm=44, label="half close")


def griefs():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render()
