from orchestra import Orchestra

# Handel, Water Music, Suite No. 1 in F major, HWV 348, 6. Minuet. A
# from-memory arrangement for General MIDI baroque band: a courtly minuet in F
# with horns, a contrasting trio for strings in D minor and the minuet again,
# in Handel's manner; the notes are approximate.
SEED = 1722

PARTS = ("oboes", "bassoons", "horns", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 3/4
MINUET = ("m3/4 c5:1 f5:1 a5:1 | g5:2 f5:1 | e5:1 g5:1 c6:1 | bb5:2 a5:1 | "
          "a5:1 f5:1 d5:1 | g5:1 e5:1 c5:1 | f5:1 e5:1 g5:1 | f5:3 |")
MINUET_BASS = "m3/4 f2:3 | c3:3 | c3:3 | c2:3 | d2:3 | c2:3 | c2:3 | f2:3 |"
MINUET_HORNS = "m3/4 f4+c5:3 | c4+g4:3 | c4+g4:3 | c4+g4:3 | f4+c5:3 | c4+g4:3 | c4+g4:3 | f4+c5:3 |"
TRIO = ("m3/4 a4:1 d5:1 f5:1 | e5:2 d5:1 | c#5:1 e5:1 a5:1 | g5:2 f5:1 | "
        "f5:1 d5:1 bb4:1 | g4:1 bb4:1 e5:1 | d5:1 c#5:1 e5:1 | d5:3 |")
TRIO_BASS = "m3/4 d3:3 | bb2:3 | a2:3 | a2:3 | bb2:3 | g2:3 | a2:3 | d2:3 |"


def play(orchestra, melody, bass, dynamic, horns=None):
    parts = {"violins": f"!{dynamic} " + melody, "oboes": f"!{dynamic} " + melody,
             "violins 2": (f"!{dynamic} " + melody, -12), "violas": (f"!{dynamic} " + bass, 19),
             "cellos": f"!{dynamic} " + bass, "basses": (f"!{dynamic} " + bass, -12),
             "harpsichord": (f"!{dynamic} " + bass, 12)}
    if horns:
        parts["horns"] = f"!{dynamic} " + horns
        parts["bassoons"] = f"!{dynamic} " + bass
    orchestra.play(parts, bpm=126)


def picture(orchestra):
    for dynamic in ("f", "mf"):
        play(orchestra, MINUET, MINUET_BASS, dynamic, MINUET_HORNS)
    for dynamic in ("p", "pp"):
        play(orchestra, TRIO, TRIO_BASS, dynamic)
    play(orchestra, MINUET, MINUET_BASS, "f", MINUET_HORNS)


def minuet():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
