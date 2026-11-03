from orchestra import Orchestra

# Wagner, Siegfried Idyll (1870), the birthday serenade for Cosima played on
# the stairs at Tribschen. A from-memory arrangement for General MIDI chamber
# orchestra: the tender E major string theme (later the love music of
# Siegfried Act III), the oboe's old lullaby "Schlaf, Kindchen, schlafe", the
# woodbird's call on the flute, Siegfried's horn and the calm, trilling close
# follow Wagner, the notes are approximate.
SEED = 1870

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets",
         "violins", "violins 2", "violas", "cellos", "basses")

# Ruhig bewegt, 4/4
THEME = ("m4/4 r:2 b4:1 c#5:1 | b4:2 g#4:1 a4:1 | b4:3 e5:1 | d#5:2 c#5:1 b4:1 | "
         "a4:3 g#4:1 | f#4:2 g#4:1 a4:1 | g#4:2 f#4:1 e4:1 | e4:4 |")
THEME_PAD = "m4/4 " + " ".join(f"{c}:4 |" for c in (
    "g#3+b3", "g#3+b3", "g#3+b3+e4", "f#3+a3+b3", "f#3+a3+c#4", "f#3+a3+d#4", "e3+g#3+b3", "e3+g#3+b3"))
THEME_BASS = "m4/4 e3:4 | e3:4 | e3:4 | b2:4 | f#2:4 | b2:4 | b2:4 | e2:4 |"

LULLABY = "m4/4 b4:1 b4:1 g#4:2 | b4:1 b4:1 g#4:2 | a4:1 g#4:1 f#4:1 e4:1 | f#4:4 | " \
          "g#4:1 g#4:1 e4:2 | g#4:1 g#4:1 e4:2 | f#4:1 e4:1 d#4:1 f#4:1 | e4:4 |"
LULLABY_PAD = "m4/4 " + " ".join(f"{c}:1/2 {c} {c} {c} {c} {c} {c} {c} |" for c in (
    "e3+b3", "e3+b3", "e3+a3", "d#3+b3", "e3+b3", "e3+b3", "d#3+a3", "e3+g#3"))

WOODBIRD = "m4/4 e6:1/4 c#6 b5:1/2 r:1 e6:1/4 c#6 b5:1/2 r:1 | g#5:1/4 a5 b5 c#6 e6:1 r:2 |"
HORN_CALL = "m4/4 e4:1/2 g#4:1/2 b4:1 e5:2 | d#5:1/2 c#5:1/2 b4:1 g#4:2 | e4:1/2 g#4:1/2 b4:1 e5:1 f#5:1 | g#5:4 |"


def theme(orchestra, dynamic, lead="violins", shift=0, **kwargs):
    orchestra.play({lead: f"!{dynamic} " + THEME, "violins 2": "!pp " + THEME_PAD, "violas": ("!pp " + THEME_PAD, 0),
                    "cellos": "!pp " + THEME_BASS, "basses": ("!pp " + THEME_BASS, -12)}, shift=shift, **kwargs)


def picture(orchestra):
    theme(orchestra, "p", bpm=60, label="theme")
    orchestra.play({"cellos": "!mp " + THEME, "violins": ("!pp " + THEME_PAD, 12), "violas": "!pp " + THEME_PAD,
                    "basses": ("!pp " + THEME_BASS, -12)}, shift=-12, bpm=60, label="theme in the cellos")
    orchestra.play({"oboes": "!p " + LULLABY, "violins 2": "!pp " + LULLABY_PAD, "violas": ("!pp " + LULLABY_PAD, 0),
                    "basses": "!pp m4/4 e2:4 | e2:4 | a1:4 | b1:4 | e2:4 | e2:4 | b1:4 | e2:4 |"},
                   bpm=66, label="lullaby")
    orchestra.play({"clarinets": "!mp " + LULLABY, "violins": ("!p " + THEME, 12), "violas": ("!pp " + LULLABY_PAD, 0),
                    "cellos": "!pp m4/4 e3:4 | e3:4 | a2:4 | b2:4 | e3:4 | e3:4 | b2:4 | e3:4 |"},
                   bpm=66)
    orchestra.play({"flutes": "!mp " + WOODBIRD, "violins 2": "!pp m4/4 g#4+b4:4 | g#4+b4:4 |",
                    "violas": "!pp m4/4 e4:4 | e4:4 |"}, bpm=72, label="woodbird")
    orchestra.play({"horns": "!mf " + HORN_CALL, "violins": "!p m4/4 " + " ".join(["e5:1/2 g#5 b5 g#5 e5 g#5 b5 g#5 |"] * 4),
                    "cellos": "!p m4/4 e3:4 | b2:4 | e3:4 | e3:4 |", "basses": "!p m4/4 e2:4 | b1:4 | e2:4 | e2:4 |"},
                   bpm=80, label="horn")
    orchestra.play({"violins": "!f " + THEME, "flutes": ("!mf " + THEME, 12), "trumpets": ("!mf " + HORN_CALL, 0),
                    "horns": ("!f " + THEME_PAD, 12), "violins 2": "!mf " + THEME_PAD, "violas": "!mf " + THEME_PAD,
                    "cellos": "!f " + THEME_BASS, "basses": ("!f " + THEME_BASS, -12),
                    "bassoons": ("!mf " + THEME_BASS, -12)}, bpm=72, to=64, label="climax")
    theme(orchestra, "p", bpm=60, label="return")
    orchestra.play({"oboes": "!pp m4/4 b4:1 b4:1 g#4:2 | f#4:2 e4:2 |", "violins": "!pp m4/4 " + " ".join(["g#5:1/8 a5"] * 16) + " | e5:4 |",
                    "violas": "!pp m4/4 b3+e4:4 | b3+e4:4 |", "basses": "!pp m4/4 e2:4 | e2:4 |"}, bpm=56, label="trills")
    orchestra.play({"violins": "!pp m4/4 g#4+b4+e5:4~ | g#4+b4+e5:4 !>n |", "violas": "!pp m4/4 e4:4~ | e4:4 !>n |",
                    "horns": "!pp m4/4 e4:4~ | e4:4 !>n |", "basses": "!pp m4/4 e2:4~ | e2:4 !>n |"}, bpm=48)


def idyll():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=105)
    picture(orchestra)
    return orchestra.render(tail=6.0)
