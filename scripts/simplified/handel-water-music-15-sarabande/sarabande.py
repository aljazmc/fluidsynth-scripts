from orchestra import Orchestra

# Handel, Water Music, Suite No. 3 in G major, HWV 350, 1. Sarabande. A
# from-memory arrangement for General MIDI baroque band: the quiet, intimate
# suite for flute and strings opens with a grave sarabande in E minor, its
# stress on the second beat, in Handel's manner; the notes are approximate.
SEED = 1731

PARTS = ("flutes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 3/4, the weight on beat two
A = ("m3/4 b4:1 e5:3/2 d#5:1/2 | e5:1 g5:3/2 f#5:1/2 | e5:1 c5:3/2 b4:1/2 | b4:3 | "
     "g5:1 b5:3/2 a5:1/2 | g5:1 f#5:3/2 e5:1/2 | d#5:1 e5:3/2 f#5:1/2 | b4:3 |")
A_BASS = "m3/4 e3:3 | e3:3 | a2:3 | b2:3 | e3:3 | a2:3 | b2:3 | e2:3 |"
B = ("m3/4 d5:1 g5:3/2 f#5:1/2 | e5:1 a5:3/2 g5:1/2 | f#5:1 d5:3/2 c5:1/2 | b4:3 | "
     "c5:1 e5:3/2 d5:1/2 | b4:1 g5:3/2 f#5:1/2 | e5:1 d#5:3/2 e5:1/2 | e5:3 |")
B_BASS = "m3/4 g2:3 | c3:3 | d3:3 | g2:3 | a2:3 | g2:3 | b2:3 | e2:3 |"


def half(orchestra, melody, bass, dynamic):
    orchestra.play({"flutes": f"!{dynamic} " + melody, "violins": (f"!{dynamic} " + melody, 0),
                    "violins 2": ("!p " + bass, 19), "violas": ("!p " + bass, 12), "cellos": "!p " + bass,
                    "basses": ("!p " + bass, -12), "harpsichord": ("!p " + bass, 12)}, bpm=60)


def picture(orchestra):
    for dynamic in ("mp", "p"):
        half(orchestra, A, A_BASS, dynamic)
    for dynamic in ("mp", "p"):
        half(orchestra, B, B_BASS, dynamic)


def sarabande():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
