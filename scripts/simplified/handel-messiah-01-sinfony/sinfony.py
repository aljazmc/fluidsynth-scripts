from orchestra import Orchestra

# Handel, Messiah (1741), Part I, No. 1. Sinfony (Overture). A from-memory
# arrangement for General MIDI baroque orchestra: the French overture in E
# minor, a grave dotted opening played twice and a terse fugal Allegro
# moderato, follows Handel's design; the notes are approximate.
SEED = 1741

PARTS = ("oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

GRAVE = ("m4/4 e5:3/2 b4:1/2 g4:3/2 e4:1/2 | c5:3/2 b4:1/2 a4:3/2 g4:1/2 | f#4:3/2 a4:1/2 d#5:3/2 f#5:1/2 | b4:4 | "
         "g5:3/2 e5:1/2 b4:3/2 g4:1/2 | a4:3/2 c5:1/2 f#5:3/2 a5:1/2 | g5:3/2 f#5:1/2 e5:3/2 d#5:1/2 | e5:4 |")
GRAVE_INNER = ("m4/4 g4+b4:2 e4+g4:2 | e4+a4:2 c4+e4:2 | d#4+f#4:2 f#4+b4:2 | d#4+f#4:4 | "
               "e4+g4:2 e4+g4:2 | e4+a4:2 d#4+f#4:2 | e4+b4:2 c4+a4:2 | e4+g4:4 |")
GRAVE_BASS = "m4/4 e3:2 e2:2 | a2:2 c3:2 | b2:2 b1:2 | b2:4 | e3:2 g2:2 | c3:2 b2:2 | e2:2 b1:2 | e2:4 |"

SUBJECT = "m4/4 b4:1 e5:1/2 f#5:1/2 g5:1 f#5:1/2 e5:1/2 | d#5:1 e5:1 r:1/2 b4:1/2 c5:1/2 a4:1/2 |"
ANSWER = "m4/4 f#4:1 b4:1/2 c#5:1/2 d5:1 c#5:1/2 b4:1/2 | a#4:1 b4:1 r:1/2 f#4:1/2 g4:1/2 e4:1/2 |"
EPISODE = ("m4/4 g4:1/2 a4 b4 c5 d5 c5 b4 a4 | b4:1/2 c5 d5 e5 f#5 e5 d#5 c#5 | "
           "d#5:1/2 e5 f#5 g5 a5 g5 f#5 e5 | d#5:2 b4:2 |")
EPISODE_BASS = "m4/4 e3:1 c3:1 a2:1 d3:1 | g2:1 e2:1 a2:1 a#2:1 | b2:1 g2:1 c3:1 a2:1 | b2:2 b1:2 |"


def picture(orchestra):
    for dynamic in ("f", "mf"):
        orchestra.play({"violins": f"!{dynamic} " + GRAVE, "oboes": f"!{dynamic} " + GRAVE,
                        "violins 2": f"!{dynamic} " + GRAVE_INNER, "violas": (f"!{dynamic} " + GRAVE_INNER, -12),
                        "cellos": f"!{dynamic} " + GRAVE_BASS, "basses": (f"!{dynamic} " + GRAVE_BASS, -12),
                        "bassoons": f"!{dynamic} " + GRAVE_BASS, "harpsichord": (f"!{dynamic} " + GRAVE_INNER, -12)},
                       bpm=54, label="grave")
    orchestra.play({"violins": "!f " + SUBJECT}, bpm=104, label="fugue")
    orchestra.play({"violins 2": "!f " + ANSWER, "violins": "!mf m4/4 g5:1 a5:1 b5:1 a5:1 | g5:1 f#5:1 e5:2 |"}, bpm=104)
    orchestra.play({"violas": ("!f " + SUBJECT, -12), "violins": "!mf m4/4 e5:1 f#5:1 g5:1 f#5:1 | b4:1 e5:1 e5:2 |",
                    "violins 2": "!mf m4/4 b4:1 c5:1 b4:1 a4:1 | f#4:1 g4:1 g4:2 |"}, bpm=104)
    orchestra.play({"cellos": ("!f " + ANSWER, -24), "basses": ("!f " + ANSWER, -36), "bassoons": ("!f " + ANSWER, -24),
                    "violins": "!mf m4/4 d5:1 e5:1 f#5:1 e5:1 | c#5:1 d5:1 d5:2 |",
                    "violins 2": "!mf m4/4 a4:1 g4:1 a4:1 g4:1 | e4:1 f#4:1 f#4:2 |", "violas": "!mf m4/4 f#4:2 d4:2 | e4:2 d4:2 |",
                    "harpsichord": "!mf m4/4 b2+d3+f#3:2 g2+b2+d3:2 | a#2+c#3+e3:2 b2+d3+f#3:2 |"}, bpm=104)
    orchestra.play({"violins": "!f " + EPISODE, "oboes": "!f " + EPISODE, "violins 2": ("!f " + EPISODE, -4),
                    "violas": ("!f " + EPISODE_BASS, 12), "cellos": "!f " + EPISODE_BASS,
                    "basses": ("!f " + EPISODE_BASS, -12), "bassoons": "!f " + EPISODE_BASS,
                    "harpsichord": ("!f " + EPISODE_BASS, 12)}, bpm=104, label="episode")
    orchestra.play({"violins": "!f " + SUBJECT, "oboes": "!f " + SUBJECT, "violins 2": ("!f " + ANSWER, -7),
                    "cellos": ("!f " + SUBJECT, -24), "basses": ("!f " + SUBJECT, -36), "violas": ("!f " + ANSWER, -12)},
                   bpm=104, to=80)
    orchestra.play({"violins": "!f m4/4 b4+e5:2 b4+d#5:2 | b4+e5:4 |", "violins 2": "!f m4/4 g4:2 f#4:2 | g4:4 |",
                    "violas": "!f m4/4 e4:2 b3:2 | b3:4 |", "cellos": "!f m4/4 c3:2 b2:2 | e2:4 |",
                    "basses": "!f m4/4 c2:2 b1:2 | e1:4 |", "oboes": "!f m4/4 e5:2 d#5:2 | e5:4 |",
                    "harpsichord": "!f m4/4 c3+e3+g3:2 b2+d#3+f#3:2 | e2+b2+e3+g3:4 |"}, bpm=72, to=56, label="end")


def sinfony():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
