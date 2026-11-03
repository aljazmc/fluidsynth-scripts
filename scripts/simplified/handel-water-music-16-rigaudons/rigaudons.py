from orchestra import Orchestra

# Handel, Water Music, Suite No. 3 in G major, HWV 350, 2. Rigaudons I & II. A
# from-memory arrangement for General MIDI baroque band: a perky G major
# rigaudon, a second in G minor, and the first again, for flute and strings,
# in Handel's manner; the notes are approximate.
SEED = 1732

PARTS = ("flutes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 2/2 (four crotchets)
FIRST = ("m4/4 g5:1 d5:1 b4:1 g4:1 | c5:1 e5:1 d5:2 | b4:1 g5:1 f#5:1 e5:1 | d5:2 r:2 | "
         "e5:1 c5:1 a4:1 c5:1 | d5:1 b4:1 g4:1 b4:1 | a4:1 d5:1 c5:1 a4:1 | g4:2 r:2 |")
FIRST_BASS = "m4/4 g2:2 g3:2 | c3:2 b2:2 | g2:2 d3:2 | d2:2 r:2 | c3:2 a2:2 | b2:2 g2:2 | d3:2 d2:2 | g2:2 r:2 |"
SECOND = ("m4/4 g4:1 bb4:1 d5:1 g5:1 | f5:1 eb5:1 d5:2 | c5:1 eb5:1 g5:1 c5:1 | bb4:2 r:2 | "
          "a4:1 c5:1 f5:1 a4:1 | bb4:1 d5:1 g5:1 bb4:1 | a4:1 g4:1 f#4:1 a4:1 | g4:2 r:2 |")
SECOND_BASS = "m4/4 g2:2 g3:2 | bb2:2 bb2:2 | c3:2 eb2:2 | bb2:2 r:2 | f2:2 f3:2 | g2:2 g3:2 | d3:2 d2:2 | g2:2 r:2 |"


def play(orchestra, melody, bass, dynamic, label):
    orchestra.play({"flutes": f"!{dynamic} " + melody, "violins": f"!{dynamic} " + melody,
                    "violins 2": (f"!{dynamic} " + melody, -12), "violas": (f"!{dynamic} " + bass, 16),
                    "cellos": f"!{dynamic} " + bass, "basses": (f"!{dynamic} " + bass, -12),
                    "bassoons": f"!{dynamic} " + bass, "harpsichord": (f"!{dynamic} " + bass, 12)},
                   bpm=144, label=label)


def picture(orchestra):
    for dynamic in ("mf", "mp"):
        play(orchestra, FIRST, FIRST_BASS, dynamic, "rigaudon I")
    for dynamic in ("mp", "p"):
        play(orchestra, SECOND, SECOND_BASS, dynamic, "rigaudon II")
    play(orchestra, FIRST, FIRST_BASS, "mf", "rigaudon I again")


def rigaudons():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
