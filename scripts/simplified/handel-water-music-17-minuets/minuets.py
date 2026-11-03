from orchestra import Orchestra

# Handel, Water Music, Suite No. 3 in G major, HWV 350, 3. Minuets I & II. A
# from-memory arrangement for General MIDI baroque band: a gracious G major
# minuet for flute and strings, a darker second minuet in G minor, and the
# first again, in Handel's manner; the notes are approximate.
SEED = 1733

PARTS = ("flutes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 3/4
FIRST = ("m3/4 d5:1 g5:1 b5:1 | a5:1 f#5:1 d5:1 | e5:1 g5:1 c6:1 | b5:2 a5:1 | "
         "g5:1 e5:1 c5:1 | d5:1 b4:1 g4:1 | a4:1 d5:1 f#4:1 | g4:3 |")
FIRST_BASS = "m3/4 g2:3 | d3:3 | c3:3 | g2:3 | c3:3 | b2:3 | d3:3 | g2:3 |"
SECOND = ("m3/4 g4:1 bb4:1 d5:1 | eb5:2 d5:1 | c5:1 a4:1 f#4:1 | g4:3 | "
          "bb4:1 d5:1 g5:1 | f5:1 eb5:1 d5:1 | c5:1 bb4:1 a4:1 | g4:3 |")
SECOND_BASS = "m3/4 g2:3 | c3:3 | d3:3 | g2:3 | g2:3 | bb2:3 | d3:3 | g2:3 |"


def play(orchestra, melody, bass, dynamic, label):
    orchestra.play({"flutes": f"!{dynamic} " + melody, "violins": f"!{dynamic} " + melody,
                    "violins 2": (f"!{dynamic} " + melody, -12), "violas": (f"!{dynamic} " + bass, 16),
                    "cellos": f"!{dynamic} " + bass, "basses": (f"!{dynamic} " + bass, -12),
                    "harpsichord": (f"!{dynamic} " + bass, 12)}, bpm=120, label=label)


def picture(orchestra):
    for dynamic in ("mf", "mp"):
        play(orchestra, FIRST, FIRST_BASS, dynamic, "minuet I")
    for dynamic in ("mp", "p"):
        play(orchestra, SECOND, SECOND_BASS, dynamic, "minuet II")
    play(orchestra, FIRST, FIRST_BASS, "mf", "minuet I again")


def minuets():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
