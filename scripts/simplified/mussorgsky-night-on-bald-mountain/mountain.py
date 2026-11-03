from orchestra import Orchestra

# Mussorgsky, Night on Bald Mountain, in Rimsky-Korsakov's 1886 version (the
# one usually played; both men are long in the public domain). A from-memory
# arrangement for General MIDI orchestra: the whirling strings and the
# trombones' and tuba's hellish theme in D minor, the witches' sabbath growing
# wilder, the church bell at dawn that scatters the spirits and the quiet D
# major close with clarinet and flute follow the score, the notes are
# approximate.
SEED = 1867

PARTS = ("piccolo", "flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba",
         "timpani", "bells", "violins", "violas", "cellos", "basses", "percussion")

# Allegro feroce, 4/4
WHIRL = "m4/4 " + " ".join(["d5:1/4 c#5 d5 e5 f5 e5 d5 c#5 d5 e5 f5 g5 a5 g5 f5 e5 |",
                            "d5:1/4 c#5 d5 e5 f5 e5 d5 c#5 bb4 a4 g4 f4 e4 f4 g4 a4 |"] * 4)
CHERNOBOG = "m4/4 d3:1 d3:1/2 eb3:1/2 d3:1 c#3:1 | d3:2 a2:2 | bb2:1 a2:1 g2:1 f2:1 | e2:4 | " \
            "d3:1 d3:1/2 eb3:1/2 d3:1 c#3:1 | d3:2 f3:2 | e3:1 d3:1 c#3:1 bb2:1 | a2:4 |"
STABS = "m4/4 " + " ".join(["d4+f4+a4:1/2^ r:7/2 |", "r:4 |", "c#4+e4+g4+bb4:1/2^ r:7/2 |", "r:4 |"] * 2)

# the witches' dance: shrill staccato woodwinds over a stamping bass
DANCE = ("m4/4 a5:1/2' a5' bb5' a5' g5' f5' e5' d5' | c#5:1/2' d5' e5' f5' e5:1^ r:1 | "
         "a5:1/2' a5' bb5' a5' g5' f5' e5' f5' | d5:1^ a4:1^ d5:1^ r:1 |")
STAMP = "m4/4 " + " ".join(["d2:1^ a1:1 d2:1^ a1:1 |"] * 4)

# dawn: a church bell, then peace
DAWN = "m4/4 d5:2 e5:1 f#5:1 | a5:3 g5:1 | f#5:2 e5:1 d5:1 | e5:4 | f#5:2 a5:1 g5:1 | f#5:3 e5:1 | d5:2 c#5:1 e5:1 | d5:4 |"
DAWN_PAD = "m4/4 " + " ".join(f"{c}:4 |" for c in ("d4+f#4", "d4+f#4", "b3+d4", "a3+c#4", "d4+f#4", "b3+d4", "a3+e4", "a3+d4"))


def sabbath(orchestra, dynamic, **kwargs):
    orchestra.play({"violins": f"!{dynamic} " + WHIRL, "violas": (f"!{dynamic} " + WHIRL, -12),
                    "trombones": f"!{dynamic} " + CHERNOBOG, "tuba": (f"!{dynamic} " + CHERNOBOG, -12),
                    "bassoons": (f"!{dynamic} " + CHERNOBOG, -12), "cellos": f"!{dynamic} " + CHERNOBOG,
                    "basses": (f"!{dynamic} " + CHERNOBOG, -12), "horns": f"!{dynamic} " + STABS,
                    "timpani": f"!{dynamic} m4/4 " + " ".join(["d2:1/4 d2 d2 d2 d2:1 r:2 |", "a1:1/4 a1 a1 a1 a1:1 r:2 |"] * 4)},
                   **kwargs)


def picture(orchestra):
    sabbath(orchestra, "f", bpm=144, label="sabbath")
    sabbath(orchestra, "ff", bpm=144)
    orchestra.play({"piccolo": "!f " + DANCE, "flutes": "!f " + DANCE, "oboes": ("!f " + DANCE, -12),
                    "clarinets": ("!f " + DANCE, -12), "cellos": "!f " + STAMP, "basses": ("!f " + STAMP, -12),
                    "percussion": "!f m4/4 " + " ".join(["36:1 r:1 36:1 r:1 |"] * 4)}, bpm=152, label="dance")
    orchestra.play({"piccolo": "!ff " + DANCE, "violins": "!ff " + DANCE, "flutes": "!ff " + DANCE,
                    "trumpets": ("!f " + DANCE, -12), "cellos": "!ff " + STAMP, "basses": ("!ff " + STAMP, -12),
                    "tuba": ("!ff " + STAMP, 0), "percussion": "!ff m4/4 49:1 r:1 36:1 r:1 | 36:1 r:1 36:1 r:1 | 49:1 r:1 36:1 r:1 | 49+36:1 r:3 |"},
                   bpm=152)
    sabbath(orchestra, "fff", bpm=152, to=168, label="climax")
    orchestra.play({"trombones": "!fff m4/4 d3+f3+a3:4^ |", "tuba": "!fff m4/4 d2:4^ |", "horns": "!fff m4/4 d4+f4+a4:4^ |",
                    "violins": "!fff m4/4 " + " ".join(f"{n}:1/8" for n in ["d6", "c#6"] * 16) + " |",
                    "timpani": "!fff m4/4 " + " ".join(["d2:1/8"] * 32) + " |", "percussion": "!fff m4/4 49+36:4 |"},
                   bpm=60, gap=1.0, label="last fury")

    # the bell tolls six times and the spirits flee
    orchestra.play({"bells": "!f m4/4 " + " ".join(["d4:3 r:1 |"] * 6) + " !>p",
                    "violins": "!pp m4/4 " + " ".join(["d5+f#5:4 |"] * 6), "violas": "!pp m4/4 " + " ".join(["a3+d4:4 |"] * 6),
                    "basses": "!pp m4/4 " + " ".join(["d2:4 |"] * 6)}, bpm=60, label="bell")
    orchestra.play({"clarinets": "!p " + DAWN, "violins": "!pp " + DAWN_PAD, "violas": ("!pp " + DAWN_PAD, -12),
                    "cellos": "!pp m4/4 d3:4 | d3:4 | g2:4 | a2:4 | d3:4 | g2:4 | a2:4 | d3:4 |"}, bpm=60, label="dawn")
    orchestra.play({"flutes": ("!p " + DAWN, 12), "violins": "!pp " + DAWN_PAD, "violas": ("!pp " + DAWN_PAD, -12),
                    "cellos": "!pp m4/4 d3:4 | d3:4 | g2:4 | a2:4 | d3:4 | g2:4 | a2:4 | d3:4 |",
                    "basses": "!pp m4/4 d2:4 | d2:4 | g1:4 | a1:4 | d2:4 | g1:4 | a1:4 | d2:4 |"}, bpm=58, to=48)
    orchestra.play({"violins": "!pp m4/4 d5+f#5+a5:4~ | d5+f#5+a5:4 !>n |", "flutes": "!pp m4/4 r:2 a5:2 | d6:4 !>n |",
                    "violas": "!pp m4/4 d4:4~ | d4:4 !>n |", "basses": "!pp m4/4 d2:4~ | d2:4 !>n |"}, bpm=46)


def mountain():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render(tail=5.0)
