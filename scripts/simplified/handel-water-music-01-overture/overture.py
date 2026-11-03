from orchestra import Orchestra

# Handel, Water Music (1717), Suite No. 1 in F major, HWV 348, 1. Overture
# (Largo - Allegro). A from-memory arrangement for General MIDI baroque band:
# the French overture's slow dotted opening and the lively fugal Allegro with
# oboes and violins over harpsichord continuo follow Handel's design, the
# notes are approximate.
SEED = 1717

PARTS = ("oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Largo, 4/4: dotted rhythms
LARGO = ("m4/4 f4+a4+c5:3/2 c5:1/2 a4:3/2 f4:1/2 | bb4:3/2 a4:1/2 g4:3/2 c5:1/2 | "
         "a4:3/2 bb4:1/2 c5:3/2 d5:1/2 | e4+g4+c5:4 |")
LARGO_BASS = "m4/4 f2:2 f2:2 | g2:2 c2:2 | f2:2 a2:2 | c2:4 |"
LARGO_CHORDS = "m4/4 f3+a3+c4:2 f3+a3+c4:2 | g3+bb3+d4:2 e3+g3+c4:2 | f3+a3+c4:2 f3+a3+c4:2 | e3+g3+c4:4 |"

# Allegro: a fugue subject in quavers, answered at the fifth
SUBJECT = "m4/4 c5:1/2 f5 e5 f5 c5 a4 f4 a4 | bb4:1/2 d5 c5 bb4 a4:1 r:1 |"
ANSWER = "m4/4 g4:1/2 c5 b4 c5 g4 e4 c4 e4 | f4:1/2 a4 g4 f4 e4:1 r:1 |"
EPISODE = ("m4/4 a4:1/2 bb4 c5 d5 c5 bb4 a4 g4 | f4:1/2 g4 a4 bb4 a4 g4 f4 e4 | "
           "d4:1/2 e4 f4 g4 f4 e4 d4 c4 | f4:2 r:2 |")
EPISODE_BASS = "m4/4 f2:1 f3:1 e3:1 c3:1 | d3:1 bb2:1 c3:1 c2:1 | bb2:1 g2:1 c3:1 c2:1 | f2:2 r:2 |"


def picture(orchestra):
    for dynamic in ("f", "mf"):
        orchestra.play({"violins": f"!{dynamic} " + LARGO, "oboes": f"!{dynamic} " + LARGO,
                        "violins 2": (f"!{dynamic} " + LARGO_CHORDS, 12), "violas": f"!{dynamic} " + LARGO_CHORDS,
                        "cellos": f"!{dynamic} " + LARGO_BASS, "basses": (f"!{dynamic} " + LARGO_BASS, -12),
                        "bassoons": f"!{dynamic} " + LARGO_BASS, "harpsichord": f"!{dynamic} " + LARGO_CHORDS},
                       bpm=56, label="largo")

    orchestra.play({"violins": "!f " + SUBJECT, "harpsichord": "!mf m4/4 f3+a3+c4:2 f3+a3+c4:2 | bb2+d3+f3:2 f3+a3+c4:2 |"},
                   bpm=112, label="allegro")
    orchestra.play({"violins 2": "!f " + ANSWER, "violins": "!mf m4/4 a4:1 c5:1 a4:1 c5:1 | d5:1 bb4:1 c5:2 |",
                    "harpsichord": "!mf m4/4 c3+e3+g3:2 c3+e3+g3:2 | f2+a2+c3:2 c3+e3+g3:2 |"}, bpm=112)
    orchestra.play({"violas": ("!f " + SUBJECT, -12), "cellos": ("!f " + ANSWER, -12), "basses": ("!f " + ANSWER, -24),
                    "violins": "!mf m4/4 f5:1 e5:1 f5:1 c5:1 | d5:1 g5:1 e5:2 |",
                    "violins 2": "!mf m4/4 a4:1 g4:1 a4:1 a4:1 | bb4:1 bb4:1 g4:2 |"}, bpm=112)
    for dynamic in ("f", "f"):
        orchestra.play({"violins": f"!{dynamic} " + EPISODE, "oboes": f"!{dynamic} " + EPISODE,
                        "violins 2": (f"!{dynamic} " + EPISODE, -5), "cellos": f"!{dynamic} " + EPISODE_BASS,
                        "basses": (f"!{dynamic} " + EPISODE_BASS, -12), "bassoons": f"!{dynamic} " + EPISODE_BASS,
                        "harpsichord": f"!{dynamic} m4/4 f3+a3+c4:2 c3+e3+g3:2 | bb2+d3+f3:2 c3+e3+g3:2 | g2+bb2+d3:2 c3+e3+g3:2 | f3+a3+c4:2 r:2 |"},
                       bpm=112, label="episode")
    orchestra.play({"violins": "!f " + SUBJECT, "oboes": "!f " + SUBJECT, "violins 2": ("!f " + ANSWER, 0),
                    "cellos": ("!f " + SUBJECT, -24), "basses": ("!f " + SUBJECT, -36), "bassoons": ("!f " + SUBJECT, -24),
                    "harpsichord": "!f m4/4 f3+a3+c4:2 c3+e3+g3:2 | bb2+d3+f3:2 c3+e3+g3:2 |"}, bpm=112, to=96)
    orchestra.play({"violins": "!f m4/4 c5+f5:4 |", "oboes": "!f m4/4 a4+c5:4 |", "violas": "!f m4/4 f4:4 |",
                    "cellos": "!f m4/4 f2:4 |", "basses": "!f m4/4 f1:4 |", "harpsichord": "!f m4/4 f2+c3+f3+a3+c4:4 |"},
                   bpm=80, label="end")


def overture():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
