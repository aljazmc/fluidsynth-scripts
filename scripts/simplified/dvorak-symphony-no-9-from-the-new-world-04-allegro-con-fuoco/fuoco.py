from orchestra import Orchestra

# Dvořák, Symphony No. 9 "From the New World", IV. Allegro con fuoco. A
# from-memory arrangement for General MIDI orchestra: the strings' grinding
# half-step that speeds up like a train, the horns' and trumpets' great E minor
# theme, the clarinet's tender second theme, the recollections of the Largo
# and the scherzo, and the blazing E major close whose last chord fades away
# follow Dvořák, the notes are approximate.
SEED = 1896

PARTS = ("flutes", "oboes", "cor anglais", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba",
         "timpani", "violins", "violins 2", "violas", "cellos", "basses", "percussion")

GRIND = "m4/4 " + " ".join(["e2+e3:1/2 f2+f3:1/2 e2+e3:1/2 f2+f3:1/2 e2+e3:1/2 f2+f3:1/2 e2+e3:1/2 f2+f3:1/2 |"] * 2) \
    + " " + " ".join(["e2+e3:1/4 f2+f3 e2+e3 f2+f3 e2+e3 f2+f3 e2+e3 f2+f3 e2+e3 f2+f3 e2+e3 f2+f3 e2+e3 f2+f3 e2+e3 f2+f3 |"] * 2)

THEME = ("m4/4 e4:2 f#4:1/2 g4:1/2 f#4:1 | e4:2 b3:2 | e4:2 f#4:1/2 g4:1/2 a4:1 | g4:2 f#4:2 | "
         "e4:2 f#4:1/2 g4:1/2 f#4:1 | e4:2 d4:1 c4:1 | b3:1 c4:1 d4:1 f#4:1 | e4:4 |")
THEME_BASS = "m4/4 e2:4 | e2:2 g2:2 | c2:4 | b1:4 | e2:4 | e2:2 a1:2 | b1:4 | e2:4 |"
SAWING = "m4/4 " + " ".join(["e4:1/3 f#4 g4 e4 f#4 g4 e4 f#4 g4 e4 f#4 g4 |"] * 8)

SECOND = "m4/4 b4:3 a4:1 | g4:2 a4:2 | b4:3 d5:1 | a4:4 | g4:3 f#4:1 | e4:2 f#4:2 | g4:2 a4:1 f#4:1 | g4:4 |"
SECOND_PAD = "m4/4 " + " ".join(f"{c}:4 |" for c in ("g3+d4", "e3+c4", "g3+d4", "f#3+d4", "e3+b3", "c3+e3", "d3+c4", "g3+b3"))

LARGO = "m4/4 f4:3/2 ab4:1/2 ab4:2 | f4:3/2 eb4:1/2 db4:2 |"


def train(orchestra):
    orchestra.play({"violins": ("!p " + GRIND + " !<ff", 24), "violins 2": ("!p " + GRIND + " !<ff", 12),
                    "violas": ("!p " + GRIND + " !<ff", 12), "cellos": "!p " + GRIND + " !<ff",
                    "basses": ("!p " + GRIND + " !<ff", -12)}, bpm=100, to=144, label="the train")
    orchestra.play({"violins": "!ff m4/4 e5+g5+b5:1/2^ r:1/2 e5+g5+b5:1/2^ r:1/2 e5+g5+b5:1^ r:1 |",
                    "violas": "!ff m4/4 e4+b4:1/2^ r:1/2 e4+b4:1/2^ r:1/2 e4+b4:1^ r:1 |",
                    "basses": "!ff m4/4 e2:1/2^ r:1/2 e2:1/2^ r:1/2 e2:1^ r:1 |",
                    "timpani": "!ff m4/4 e2:1/2^ r:1/2 e2:1/2^ r:1/2 e2:1^ r:1 |"}, bpm=144)


def theme(orchestra, dynamic, key=0, **kwargs):
    orchestra.play({"horns": f"!{dynamic} " + THEME, "trumpets": f"!{dynamic} " + THEME,
                    "trombones": (f"!{dynamic} " + THEME_BASS, 12), "tuba": f"!{dynamic} " + THEME_BASS,
                    "violins": f"!{dynamic} " + SAWING, "violins 2": (f"!{dynamic} " + SAWING, -12),
                    "violas": (f"!{dynamic} " + SAWING, -12), "cellos": f"!{dynamic} " + THEME_BASS,
                    "basses": (f"!{dynamic} " + THEME_BASS, -12),
                    "timpani": f"!{dynamic} m4/4 " + " ".join(["e2:1 r:1 b1:1 r:1 |"] * 8),
                    "percussion": f"!{dynamic} m4/4 49:4 | r:4 | r:4 | r:4 | 49:4 | r:4 | r:4 | r:4 |"},
                   shift=key, **kwargs)


def picture(orchestra):
    train(orchestra)
    theme(orchestra, "ff", bpm=144, label="theme")
    orchestra.play({"violins": ("!ff " + THEME, 12), "violins 2": "!ff " + THEME, "flutes": ("!f " + THEME, 12),
                    "oboes": ("!f " + THEME, 12), "violas": "!f " + SAWING, "cellos": "!ff " + THEME_BASS,
                    "basses": ("!ff " + THEME_BASS, -12), "horns": ("!f " + THEME_BASS, 24)}, bpm=144)

    orchestra.play({"clarinets": "!p " + SECOND, "violins 2": "!pp " + SECOND_PAD, "violas": ("!pp " + SECOND_PAD, -12),
                    "cellos": "!pp m4/4 g2:4 | c2:4 | g2:4 | d2:4 | e2:4 | a1:4 | d2:4 | g2:4 |"},
                   bpm=132, label="clarinet")
    orchestra.play({"violins": "!mf " + SECOND, "flutes": ("!mf " + SECOND, 12), "violins 2": "!p " + SECOND_PAD,
                    "violas": ("!p " + SECOND_PAD, -12),
                    "cellos": "!p m4/4 g2:4 | c2:4 | g2:4 | d2:4 | e2:4 | a1:4 | d2:4 | g2:4 |"}, bpm=132)

    # development: the theme fragmented, the Largo remembered
    theme(orchestra, "f", key=-4, bpm=144, label="development")
    orchestra.play({"cor anglais": "!mf " + LARGO, "violas": "!p m4/4 ab3+db4:4 | ab3+db4:4 |",
                    "cellos": "!p m4/4 db3:4 | db3:4 |"}, bpm=96, label="largo remembered")
    theme(orchestra, "ff", key=3, bpm=144)

    # recapitulation and the E major coda
    theme(orchestra, "ff", bpm=144, label="recapitulation")
    orchestra.play({"clarinets": "!p " + SECOND, "violins 2": "!pp " + SECOND_PAD, "violas": ("!pp " + SECOND_PAD, -12)},
                   bpm=132, shift=-3)
    major = THEME.replace("g4", "g#4").replace("c4", "c#4")
    orchestra.play({"horns": "!fff " + major, "trumpets": "!fff " + major, "trombones": ("!fff " + major, -12),
                    "violins": ("!fff " + major, 12), "violins 2": "!fff " + major, "flutes": ("!fff " + major, 12),
                    "oboes": ("!ff " + major, 12), "violas": "!ff " + SAWING.replace("g4", "g#4"),
                    "cellos": "!fff " + THEME_BASS, "basses": ("!fff " + THEME_BASS, -12),
                    "tuba": "!fff " + THEME_BASS, "timpani": "!fff m4/4 " + " ".join(["e2:1/4 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 |"] * 8)},
                   bpm=132, to=100, label="E major")
    # the last chord: held, and fading away
    voicing = {"violins": "e5+g#5+b5", "violins 2": "b4+e5", "violas": "g#4", "cellos": "e3", "basses": "e2",
               "flutes": "e6+g#6", "oboes": "b5+e6", "clarinets": "g#4+b4", "bassoons": "e2+b2", "horns": "e4+g#4+b4",
               "trumpets": "e5", "trombones": "e3+b3", "tuba": "e2", "timpani": "e2"}
    orchestra.play({p: f"!fff m4/4 {v}:4~ | {v}:4~ | {v}:4 !>n |" for p, v in voicing.items()},
                   bpm=60, label="last chord")


def fuoco():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render(tail=5.0)
