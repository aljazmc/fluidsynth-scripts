from orchestra import Orchestra

# Handel, Water Music, Suite No. 2 in D major, HWV 349, 4. Lentement. A
# from-memory arrangement for General MIDI baroque band: a slow, dignified
# dance in triple time, its long notes and gentle dotted rhythms shared by
# strings, oboes and horns, in Handel's manner; the notes are approximate.
SEED = 1729

PARTS = ("oboes", "bassoons", "horns", "trumpets", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 3/2 (six crotchets)
A = ("m3/2 f#5:2 e5:3/2 d5:1/2 d5:2 | a5:3 g5:1 f#5:2 | e5:2 d5:3/2 c#5:1/2 d5:2 | "
     "c#5:4 a4:2 | d5:2 f#5:3/2 e5:1/2 d5:2 | b5:3 a5:1 g5:2 | f#5:2 e5:3/2 d5:1/2 e5:2 | d5:6 |")
A_BASS = "m3/2 d3:6 | f#2:6 | g2:4 f#2:2 | a2:4 a1:2 | b2:6 | g2:6 | a2:4 a1:2 | d2:6 |"
HORNS = "m3/2 d4+a4:6 | d4+a4:6 | d4+a4:6 | e4+a4:6 | d4+a4:6 | d4+g4:6 | e4+a4:6 | d4+a4:6 |"


def picture(orchestra):
    for dynamic, extra in (("mf", {}), ("p", {"horns": "!p " + HORNS}), ("mf", {"horns": "!mf " + HORNS})):
        orchestra.play({"violins": f"!{dynamic} " + A, "oboes": f"!{dynamic} " + A,
                        "violins 2": (f"!{dynamic} " + A, -12), "violas": (f"!{dynamic} " + A_BASS, 16),
                        "cellos": f"!{dynamic} " + A_BASS, "basses": (f"!{dynamic} " + A_BASS, -12),
                        "bassoons": f"!{dynamic} " + A_BASS, "harpsichord": (f"!{dynamic} " + A_BASS, 12), **extra},
                       bpm=84, to=72 if dynamic == "mf" and extra else None)


def lentement():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
