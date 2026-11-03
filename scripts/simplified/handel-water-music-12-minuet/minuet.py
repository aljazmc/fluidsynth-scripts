from orchestra import Orchestra

# Handel, Water Music, Suite No. 2 in D major, HWV 349, 3. Minuet. A
# from-memory arrangement for General MIDI baroque band: a stately D major
# minuet with trumpets and drums, each half repeated, in Handel's manner; the
# notes are approximate.
SEED = 1728

PARTS = ("oboes", "bassoons", "horns", "trumpets", "timpani", "harpsichord",
         "violins", "violins 2", "violas", "cellos", "basses")

# 3/4
A = "m3/4 d5:1 f#5:1 a5:1 | g5:1 e5:1 c#5:1 | d5:1 a4:1 f#5:1 | e5:3 | f#5:1 d5:1 a5:1 | b5:1 g5:1 e5:1 | a5:1 g5:1 f#5:1 | e5:3 |"
A_BASS = "m3/4 d3:3 | a2:3 | d3:3 | a2:3 | d3:3 | g2:3 | a2:3 | a1:3 |"
B = "m3/4 e5:1 a5:1 c#6:1 | d6:1 a5:1 f#5:1 | g5:1 b5:1 g5:1 | f#5:1 a5:1 d5:1 | e5:1 g5:1 b4:1 | a4:1 f#5:1 d5:1 | e5:2 c#5:1 | d5:3 |"
B_BASS = "m3/4 a2:3 | d3:3 | g2:3 | d3:3 | g2:3 | f#2:3 | a2:3 | d2:3 |"


def half(orchestra, melody, bass, dynamic):
    orchestra.play({"violins": f"!{dynamic} " + melody, "oboes": f"!{dynamic} " + melody,
                    "trumpets": f"!{dynamic} " + melody, "violins 2": (f"!{dynamic} " + melody, -12),
                    "horns": (f"!{dynamic} " + bass, 19), "violas": (f"!{dynamic} " + bass, 16),
                    "cellos": f"!{dynamic} " + bass, "basses": (f"!{dynamic} " + bass, -12),
                    "bassoons": f"!{dynamic} " + bass, "harpsichord": (f"!{dynamic} " + bass, 12),
                    "timpani": f"!{dynamic} m3/4 " + " ".join(["d2:1 r:1 a1:1 |"] * 8)}, bpm=120)


def picture(orchestra):
    for dynamic in ("f", "mf"):
        half(orchestra, A, A_BASS, dynamic)
    for dynamic in ("f", "mf"):
        half(orchestra, B, B_BASS, dynamic)


def minuet():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
