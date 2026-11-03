from orchestra import Orchestra

# Handel, Water Music, Suite No. 1 in F major, HWV 348, 9. (Allegro
# moderato). A from-memory arrangement for General MIDI baroque band: the
# suite's closing movement, a broad, cheerful piece in F for the whole band
# with horns, in Handel's manner; the notes are approximate.
SEED = 1725

PARTS = ("oboes", "bassoons", "horns", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 4/4
TUNE = ("m4/4 f5:1 a5:1/2 g5:1/2 f5:1 c5:1 | d5:1 f5:1/2 e5:1/2 d5:1 bb4:1 | c5:1/2 d5 e5 f5 g5:1 c5:1 | "
        "a5:1/2 g5 f5 e5 f5:2 | bb5:1 a5:1/2 g5:1/2 a5:1 f5:1 | g5:1 f5:1/2 e5:1/2 f5:1 d5:1 | "
        "c5:1/2 f5 e5 d5 c5:1 e5:1 | f5:4 |")
BASS = "m4/4 f2:1 f3:1 a2:1 f2:1 | bb2:1 bb1:1 g2:1 bb2:1 | c3:1 bb2:1 a2:1 c3:1 | f2:1 c2:1 f2:2 | " \
       "d3:1 d2:1 f2:1 d2:1 | e2:1 c2:1 a2:1 bb2:1 | c3:1 a2:1 c3:1 c2:1 | f2:4 |"
HORNS = "m4/4 f4+c5:2 f4+c5:2 | f4+bb4:2 f4+bb4:2 | c4+g4:2 c4+g4:2 | f4+c5:4 | f4+a4:2 f4+a4:2 | c4+g4:2 f4+c5:2 | c4+g4:2 c4+g4:2 | f4+c5:4 |"


def picture(orchestra):
    for dynamic, horns in (("f", True), ("mf", False), ("f", True)):
        parts = {"violins": f"!{dynamic} " + TUNE, "oboes": f"!{dynamic} " + TUNE,
                 "violins 2": (f"!{dynamic} " + TUNE, -12), "violas": (f"!{dynamic} " + BASS, 19),
                 "cellos": f"!{dynamic} " + BASS, "basses": (f"!{dynamic} " + BASS, -12),
                 "bassoons": f"!{dynamic} " + BASS, "harpsichord": (f"!{dynamic} " + BASS, 12)}
        if horns:
            parts["horns"] = f"!{dynamic} " + HORNS
        orchestra.play(parts, bpm=104, to=88 if dynamic == "f" and not horns else None)
    orchestra.play({"horns": "!f m4/4 f4+c5:4 |", "violins": "!f m4/4 f5+a5:4 |", "oboes": "!f m4/4 c5+f5:4 |",
                    "cellos": "!f m4/4 f2:4 |", "basses": "!f m4/4 f1:4 |", "harpsichord": "!f m4/4 f2+c3+f3+a3:4 |"},
                   bpm=80, label="end")


def moderato():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
