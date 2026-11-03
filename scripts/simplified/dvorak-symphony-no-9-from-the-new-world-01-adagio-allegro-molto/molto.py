from orchestra import Orchestra

# Dvořák, Symphony No. 9 in E minor, Op. 95, "From the New World" (1893),
# I. Adagio - Allegro molto. A from-memory arrangement for General MIDI
# orchestra: the cellos' slow introduction and its sudden outburst, the horns'
# rising E minor arpeggio theme, the flute's G major tune with its spiritual
# flavour and the ringing coda follow Dvořák, the notes are approximate.
SEED = 1893

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba", "timpani",
         "violins", "violins 2", "violas", "cellos", "basses")

INTRO = "m4/4 e3:2 f#3:1 g3:1 | b3:3 a3:1 | g3:2 f#3:1 e3:1 | d#3:4 |"
INTRO_ANSWER = "m4/4 b4:2 a4:1 g4:1 | f#4:3 e4:1 | d#4:2 e4:1 f#4:1 | b3:4 |"
OUTBURST = "m4/4 e2+e3:1/4^ r:3/4 r:1 b1+b2:1/4^ r:3/4 r:1 | c2+c3:2^ b1+b2:2^ |"

# Allegro molto, 2/4
HORN = ("m2/4 e3:3/4 g3:1/4 b3:1 | b3:1/2 g3:1/2 e3:1 | e3:3/4 g3:1/4 b3:1 | d4:1 b3:1 | "
        "c4:3/4 b3:1/4 a3:1 | g3:1/2 f#3:1/2 e3:1 | f#3:1 d#3:1 | e3:2 |")
ANSWER = ("m2/4 r:1 b4:3/4 g4:1/4 | e5:3/4 d5:1/4 b4:1 | r:1 b4:3/4 g4:1/4 | e5:3/4 f#5:1/4 g5:1 | "
          "a5:3/4 g5:1/4 e5:1 | d5:1/2 b4:1/2 g4:1 | a4:1 f#4:1 | e4:2 |")
HORN_HARMONY = "m2/4 e2:2 | e2:2 | e2:2 | g2:2 | a2:2 | e2:2 | b1:2 | e2:2 |"
TUNE = ("m2/4 g4:1/2 g4:1/2 b4:1 | b4:1/2 g4:1/2 a4:1/2 b4:1/2 | d5:1 b4:1 | a4:2 | "
        "g4:1/2 g4:1/2 b4:1 | b4:1/2 g4:1/2 a4:1/2 b4:1/2 | a4:1 f#4:1 | g4:2 |")
TUNE_PAD = "m2/4 g3+b3+d4:2 | g3+b3+d4:2 | g3+b3+d4:2 | f#3+a3+d4:2 | g3+b3+d4:2 | e3+g3+b3:2 | d3+f#3+a3:2 | g3+b3+d4:2 |"
TUNE_BASS = "m2/4 g2:2 | g2:2 | g2:2 | d2:2 | g2:2 | e2:2 | d2:2 | g2:2 |"


def horn_theme(orchestra, dynamic, key=0, **kwargs):
    orchestra.play({"horns": f"!{dynamic} " + HORN, "clarinets": ("!p " + ANSWER, -12),
                    "oboes": ("!p " + ANSWER, 0), "cellos": "!pp " + HORN_HARMONY,
                    "basses": ("!pp " + HORN_HARMONY, -12),
                    "violas": "!pp m2/4 " + " ".join(["e3+b3:1/2' r:1/2 e3+b3:1/2' r:1/2 |"] * 8)},
                   shift=key, **kwargs)


def tutti_theme(orchestra, dynamic, key=0, **kwargs):
    orchestra.play({"violins": (f"!{dynamic} " + HORN, 12), "violins 2": (f"!{dynamic} " + HORN, 0),
                    "horns": f"!{dynamic} " + HORN, "trumpets": (f"!{dynamic} " + HORN, 12),
                    "flutes": (f"!{dynamic} " + ANSWER, 12), "oboes": f"!{dynamic} " + ANSWER,
                    "trombones": (f"!{dynamic} " + HORN_HARMONY, 12), "tuba": f"!{dynamic} " + HORN_HARMONY,
                    "cellos": (f"!{dynamic} " + HORN, -12), "basses": (f"!{dynamic} " + HORN_HARMONY, -12),
                    "timpani": f"!{dynamic} m2/4 " + " ".join(["e2:1/2 r:1/2 b1:1/2 r:1/2 |"] * 8)},
                   shift=key, **kwargs)


def flute_tune(orchestra, dynamic, key=0, **kwargs):
    orchestra.play({"flutes": f"!{dynamic} " + TUNE, "violins 2": "!pp " + TUNE_PAD, "violas": ("!pp " + TUNE_PAD, -12),
                    "cellos": "!pp " + TUNE_BASS, "basses": ("!pp " + TUNE_BASS, -12)}, shift=key, **kwargs)
    orchestra.play({"violins": f"!mf " + TUNE, "flutes": (f"!mf " + TUNE, 12), "violins 2": "!p " + TUNE_PAD,
                    "violas": ("!p " + TUNE_PAD, -12), "cellos": "!p " + TUNE_BASS, "basses": ("!p " + TUNE_BASS, -12),
                    "horns": ("!p " + TUNE_PAD, 0)}, shift=key, **kwargs)


def picture(orchestra):
    orchestra.play({"cellos": "!p " + INTRO, "basses": ("!pp " + INTRO, -12)}, bpm=60, label="introduction")
    orchestra.play({"flutes": "!pp " + INTRO_ANSWER, "oboes": ("!pp " + INTRO_ANSWER, -12),
                    "violas": "!pp m4/4 e3+g3:4 | d#3+f#3:4 | e3+g3:4 | f#3+a3:4 |"}, bpm=60, gap=0.4)
    orchestra.play({"violins": ("!ff " + OUTBURST, 24),
                    "violas": ("!ff " + OUTBURST, 12), "cellos": ("!ff " + OUTBURST, 0), "basses": ("!ff " + OUTBURST, -12),
                    "timpani": "!ff m4/4 e2:1/4^ r:3/4 r:1 b1:1/4^ r:3/4 r:1 | " + " ".join(["b1:1/8 e2"] * 16) + " |",
                    "horns": "!ff m4/4 r:4 | c4+e4:2 b3+d#4:2 |"}, bpm=60, to=100, gap=0.4, label="outburst")

    horn_theme(orchestra, "f", bpm=152, label="horn theme")
    tutti_theme(orchestra, "ff", bpm=152, label="tutti")
    flute_tune(orchestra, "p", key=0, bpm=144, label="flute tune")

    # development: the horn theme in other keys, growing
    horn_theme(orchestra, "f", key=-3, bpm=152, label="development")
    horn_theme(orchestra, "ff", key=1, bpm=152)
    tutti_theme(orchestra, "ff", key=-2, bpm=152)

    # recapitulation and coda
    horn_theme(orchestra, "f", bpm=152, label="recapitulation")
    flute_tune(orchestra, "p", key=1, bpm=144)
    tutti_theme(orchestra, "fff", bpm=152, to=160, label="coda")
    end = "m2/4 X:1^ r:1 | X:1^ r:1 | X:2^~ | X:2^ |"
    voicing = {"violins": "e5+g5+b5", "violins 2": "b4+e5", "violas": "g3+e4", "cellos": "e3", "basses": "e2",
               "flutes": "e6+g6", "oboes": "b5+e6", "clarinets": "g4+b4", "bassoons": "e2+b2", "horns": "e4+b4",
               "trumpets": "e5", "trombones": "e3+b3", "tuba": "e2", "timpani": "e2"}
    orchestra.play({p: "!fff " + end.replace("X", v) for p, v in voicing.items()}, bpm=160, to=100, label="end")


def molto():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
