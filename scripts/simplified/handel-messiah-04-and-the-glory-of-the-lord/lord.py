from orchestra import Orchestra

# Handel, Messiah, Part I, No. 4. And the glory of the Lord (chorus). A
# from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: the dancing A major 3/4, the altos starting "And the
# glory", the running "shall be revealed", the long-note "for the mouth of
# the Lord hath spoken it" and the grand final pause and cadence follow
# Handel, the notes are approximate.
SEED = 1744

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 3/4
INTRO = ("m3/4 a4:1 c#5:1/2 b4:1/2 a4:1 | e5:2 e4:1 | f#4:1/2 g#4 a4 b4 c#5 d5 | e5:2 r:1 |")
INTRO_BASS = "m3/4 a2:1 a3:1 a2:1 | c#3:2 a2:1 | d3:2 b2:1 | e2:2 r:1 |"
GLORY_S = "m3/4 a4:1 c#5:1 c#5:1 | b4:1/2 a4:1/2 g#4:1 r:1 | a4:1 c#5:1 d5:1 | e5:2 d5:1 | c#5:3 |"
GLORY = "m3/4 e4:1 a4:1 a4:1 | g#4:1/2 f#4:1/2 e4:1 r:1 | e4:1 a4:1 b4:1 | c#5:2 b4:1 | a4:3 |"
GLORY_T = "m3/4 c#4:1 e4:1 e4:1 | e4:1/2 d4:1/2 b3:1 r:1 | c#4:1 e4:1 f#4:1 | e4:3 | e4:3 |"
GLORY_B = "m3/4 a2:1 a2:1 a2:1 | e3:1 e2:1 r:1 | a2:1 a2:1 d3:1 | e3:2 e2:1 | a2:3 |"
REVEALED_S = ("m3/4 e5:2 f#5:1/2 e5:1/2 | d5:1/2 e5 f#5 g#5 a5 b5 | c#6:1/2 b5 a5 g#5 f#5 e5 | "
              "d5:1/2 c#5 b4 c#5 d5 b4 | a4:3 |")
REVEALED_A = "m3/4 c#4:2 d4:1 | b3:3 | e4:3 | f#4:2 e4:1 | e4:3 |"
REVEALED_T = ("m3/4 e4:2 f#4:1/2 e4:1/2 | d4:1/2 e4 f#4 g#4 a4 b4 | c#5:1/2 b4 a4 g#4 f#4 e4 | "
              "d4:1/2 c#4 b3 c#4 d4 b3 | a3:3 |")
REVEALED_B = "m3/4 a2:2 d3:1 | b2:3 | a2:3 | b2:2 e2:1 | a2:3 |"
FLESH = "m3/4 c#5:1 c#5:1 b4:1 | a4:1 a4:1 g#4:1 | a4:2 b4:1 | e4:3 |"
MOUTH = "m3/4 a3:3 | a3:3 | a3:3 | b3:3 | c#4:3 | b3:3 |"


def satb(s, a, t, b, dynamic):
    return {"choir": [f"!{dynamic} " + s, f"!{dynamic} " + a, f"!{dynamic} " + t, f"!{dynamic} " + b],
            "violins": f"!{dynamic} " + s, "violins 2": f"!{dynamic} " + a, "violas": f"!{dynamic} " + t,
            "cellos": f"!{dynamic} " + b, "basses": (f"!{dynamic} " + b, -12), "harpsichord": f"!mf " + b,
            "oboes": f"!{dynamic} " + s, "bassoons": f"!{dynamic} " + b}


def picture(orchestra):
    orchestra.play({"violins": "!f " + INTRO, "oboes": "!f " + INTRO, "violins 2": ("!f " + INTRO, -12),
                    "cellos": "!f " + INTRO_BASS, "basses": ("!f " + INTRO_BASS, -12), "harpsichord": "!f " + INTRO_BASS},
                   bpm=144, label="introduction")
    orchestra.play({"choir": "!f " + GLORY, "violins 2": "!f " + GLORY,
                    "cellos": "!mf m3/4 a2:3 | e2:3 | a2:3 | e2:3 | a2:3 |"}, bpm=144, label="altos")
    orchestra.play(satb(GLORY_S, GLORY, GLORY_T, GLORY_B, "f"), bpm=144, label="tutti")
    orchestra.play(satb(REVEALED_S, REVEALED_A, REVEALED_T, REVEALED_B, "f"), bpm=144, label="revealed")
    orchestra.play(satb(FLESH, "m3/4 e4:1 e4:1 e4:1 | e4:1 f#4:1 e4:1 | e4:2 d4:1 | c#4:3 |",
                        "m3/4 a3:1 a3:1 g#3:1 | a3:1 d4:1 b3:1 | c#4:2 b3:1 | a3:3 |",
                        "m3/4 a2:1 a2:1 e2:1 | f#2:1 d2:1 e2:1 | c#2:1 d2:1 e2:1 | a1:3 |", "f"),
               bpm=144, label="all flesh")
    orchestra.play(satb("m3/4 e5:2 c#5:1 | d5:2 b4:1 | c#5:1 b4:1 a4:1 | g#4:1 a4:1 b4:1 | a4:2 g#4:1 | a4:3 |",
                        "m3/4 c#5:2 a4:1 | b4:2 g#4:1 | a4:1 g#4:1 f#4:1 | e4:3 | e4:2 e4:1 | e4:3 |",
                        "m3/4 a3:2 e4:1 | f#4:2 e4:1 | e4:3 | b3:3 | c#4:2 b3:1 | c#4:3 |",
                        MOUTH, "ff"), bpm=144, label="the mouth of the Lord")
    orchestra.play(satb(INTRO, "m3/4 c#4:3 | e4:3 | d4:3 | e4:3 |", "m3/4 a3:3 | a3:3 | a3:3 | g#3:3 |", INTRO_BASS, "f"),
                   bpm=144)
    # the famous pause, then the broad Adagio close
    orchestra.play(satb("m3/4 a4:1 e5:1 r:1 |", "m3/4 c#4:1 c#5:1 r:1 |", "m3/4 e3:1 a4:1 r:1 |", "m3/4 a2:1 a3:1 r:1 |", "ff"),
                   bpm=144, gap=1.0)
    orchestra.play(satb("m3/4 a4:3 | a4:3 |", "m3/4 f#4:3 | e4:3 |", "m3/4 d4:3 | c#4:3 |", "m3/4 d3:3 | a2:3 |", "ff"),
                   bpm=60, to=48, label="adagio")


def lord():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
