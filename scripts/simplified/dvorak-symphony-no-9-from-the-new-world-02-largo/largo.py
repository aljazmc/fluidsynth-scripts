from orchestra import Orchestra

# Dvořák, Symphony No. 9 "From the New World", II. Largo. A from-memory
# arrangement for General MIDI orchestra: the brass and woodwind chords that
# lead from E major into D-flat, the cor anglais singing the famous tune over
# muted strings, the restless C-sharp minor middle, and the tune's return,
# broken by silences, follow Dvořák; the tune is close, the rest approximate.
SEED = 1894

PARTS = ("flutes", "oboes", "cor anglais", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba",
         "timpani", "violins", "violins 2", "violas", "cellos", "basses")

CHORALE = "m4/4 X:2 Y:2 | Z:4 |"
CHORDS = (("e3+g#3+b3+e4", "f3+bb3+db4+f4", "f3+ab3+db4+f4"),
          ("e3+a3+c#4+e4", "f3+ab3+db4+f4", "eb3+ab3+c4+eb4"),
          ("db3+f3+ab3+db4", "eb3+gb3+bb3+eb4", "db3+f3+ab3+db4"))

GOING_HOME = ("m4/4 f4:3/2 ab4:1/2 ab4:2 | f4:3/2 eb4:1/2 db4:2 | eb4:1 f4:1 ab4:1 f4:1 | eb4:4 | "
              "f4:3/2 ab4:1/2 ab4:2 | f4:3/2 eb4:1/2 db4:2 | eb4:1 f4:1 eb4:1 db4:1 | db4:4 |")
STRINGS = ("m4/4 ab3+db4:4 | ab3+db4:4 | ab3+c4+eb4:4 | ab3+c4+eb4:4 | ab3+db4:4 | gb3+bb3+db4:4 | "
           "gb3+ab3+c4:4 | f3+ab3+db4:4 |")
BASS = "m4/4 db3:4 | db3:4 | ab2:4 | ab2:4 | db3:4 | gb2:4 | ab2:4 | db3:4 |"

# Un poco più mosso, C-sharp minor: flutes and oboes over a trembling pulse
MIDDLE = ("m4/4 g#4:2 b4:1 a4:1 | g#4:3 f#4:1 | e4:2 f#4:1 g#4:1 | c#4:4 | "
          "c#5:2 b4:1 a4:1 | g#4:3 f#4:1 | a4:2 g#4:1 f#4:1 | g#4:4 |")
PULSE = "m4/4 " + " ".join(f"{c}:1/2' {c}' {c}' {c}' {c}' {c}' {c}' {c}' |" for c in (
    "c#3+e3", "c#3+e3", "c#3+e3", "c#3+e3", "a2+e3", "c#3+e3", "d#3+f#3", "c#3+e3"))


def chorale(orchestra, dynamic, **kwargs):
    for x, y, z in CHORDS:
        text = CHORALE.replace("X", x).replace("Y", y).replace("Z", z)
        orchestra.play({"horns": f"!{dynamic} " + text, "trombones": (f"!{dynamic} " + text, -12),
                        "clarinets": (f"!{dynamic} " + text, 12), "bassoons": (f"!{dynamic} " + text, -12),
                        "tuba": (f"!{dynamic} m4/4 {x.split('+')[0]}:2 {y.split('+')[0]}:2 | {z.split('+')[0]}:4 |", -12)},
                       **kwargs)


def picture(orchestra):
    chorale(orchestra, "p", bpm=44, label="chorale")
    orchestra.play({"cor anglais": "!p " + GOING_HOME, "violins 2": "!pp " + STRINGS, "violas": ("!pp " + STRINGS, -12),
                    "cellos": "!pp " + BASS, "basses": ("!pp " + BASS, -12)}, bpm=46, label="cor anglais")
    orchestra.play({"cor anglais": "!mp " + GOING_HOME, "clarinets": ("!p " + GOING_HOME, -12),
                    "violins": ("!pp " + STRINGS, 12), "violins 2": "!pp " + STRINGS, "violas": ("!pp " + STRINGS, -12),
                    "cellos": "!pp " + BASS, "basses": ("!pp " + BASS, -12)}, bpm=46)
    chorale(orchestra, "pp", bpm=44)

    orchestra.play({"flutes": "!p " + MIDDLE, "oboes": ("!p " + MIDDLE, -12), "violins 2": "!pp " + PULSE,
                    "violas": "!pp " + PULSE, "basses": "!pp m4/4 c#2:4 | c#2:4 | c#2:4 | c#2:4 | a1:4 | c#2:4 | g#1:4 | c#2:4 |"},
                   bpm=52, label="C-sharp minor")
    orchestra.play({"clarinets": "!mp " + MIDDLE, "violins": ("!mp " + MIDDLE, 12), "violins 2": "!p " + PULSE,
                    "violas": "!p " + PULSE, "cellos": ("!p " + MIDDLE, -12),
                    "basses": "!p m4/4 c#2:4 | c#2:4 | c#2:4 | c#2:4 | a1:4 | c#2:4 | g#1:4 | c#2:4 |"},
                   bpm=52)
    # a brief, bright storm, the trombones recalling the first movement
    orchestra.play({"trombones": "!ff m4/4 e3:3/2 g3:1/2 b3:2 | b3:1 g3:1 e3:2 |",
                    "trumpets": "!ff m4/4 e5:3/2 g5:1/2 b5:2 | b5:1 g5:1 e5:2 |",
                    "violins": "!ff m4/4 " + " | ".join([" ".join(f"{n}:1/4" for n in ("e5", "f#5", "g5", "a5") * 4)] * 2) + " |",
                    "cellos": "!ff m4/4 e2:4 | e2:4 |", "basses": "!ff m4/4 e1:4 | e1:4 |",
                    "timpani": "!ff m4/4 e2:1/4 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 | e2:4 |"},
                   bpm=60, to=44, gap=0.6, label="storm")

    # the tune returns, faltering, broken by silences
    orchestra.play({"cor anglais": "!p " + GOING_HOME[:GOING_HOME.index("| f4:3/2 ab4:1/2 ab4:2 | f4:3/2 eb4:1/2 db4:2 | eb4:1 f4:1 eb4")] + "|",
                    "violins 2": "!pp " + STRINGS[:STRINGS.index("| ab3+db4:4 | gb3")] + "|",
                    "cellos": "!pp m4/4 db3:4 | db3:4 | ab2:4 | ab2:4 |"}, bpm=44, label="return")
    for phrase in ("m4/4 f4:3/2 ab4:1/2 ab4:2 | m2/4 r:2 |", "m4/4 f4:3/2 eb4:1/2 db4:2 | m2/4 r:2 |"):
        orchestra.play({"violins": "!pp " + phrase, "violins 2": ("!ppp " + phrase, -12)}, bpm=42)
    orchestra.play({"cor anglais": "!pp m4/4 eb4:1 f4:1 eb4:1 db4:1 | db4:4 |",
                    "violas": "!ppp m4/4 gb3+ab3+c4:4 | f3+ab3+db4:4 |", "cellos": "!ppp m4/4 ab2:4 | db3:4 |"},
                   bpm=42, to=36)
    chorale(orchestra, "pp", bpm=40, to=34)
    orchestra.play({"basses": "!pp m4/4 db2+ab2:4~ | db2+ab2:4 !>n |", "violas": "!ppp m4/4 f3+ab3+db4:4~ | f3+ab3+db4:4 !>n |"},
                   bpm=34)


def largo():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render(tail=6.0)
