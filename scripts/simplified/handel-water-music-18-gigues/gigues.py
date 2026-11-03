from orchestra import Orchestra

# Handel, Water Music, Suite No. 3 in G major, HWV 350, 4. Gigues I & II
# (Country Dances). A from-memory arrangement for General MIDI baroque band:
# two lively jigs in 6/8, the second in G minor, and the first again to end
# the Water Music, for flute and strings, in Handel's manner; the notes are
# approximate.
SEED = 1734

PARTS = ("flutes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 6/8 (three crotchet beats)
FIRST = ("m6/8 g5:1 d5:1/2 b4:1 d5:1/2 | g5:1/2 a5 b5 a5:1 g5:1/2 | f#5:1 a5:1/2 d5:1 f#5:1/2 | a5:3/2 d5:3/2 | "
         "e5:1 c5:1/2 a4:1 c5:1/2 | d5:1 b4:1/2 g4:1 b4:1/2 | c5:1/2 b4 a4 d5:1 f#4:1/2 | g4:3 |")
FIRST_BASS = "m6/8 g2:3/2 g3:3/2 | g2:3/2 b2:3/2 | d3:3/2 d2:3/2 | d3:3/2 f#2:3/2 | " \
             "c3:3/2 a2:3/2 | b2:3/2 g2:3/2 | a2:3/2 d2:3/2 | g2:3 |"
SECOND = ("m6/8 g4:1 bb4:1/2 d5:1 g5:1/2 | f5:1 eb5:1/2 d5:1 c5:1/2 | bb4:1 c5:1/2 d5:1 bb4:1/2 | a4:3 | "
          "bb4:1 d5:1/2 g5:1 bb4:1/2 | c5:1 eb5:1/2 a4:1 c5:1/2 | bb4:1/2 a4 g4 a4:1 f#4:1/2 | g4:3 |")
SECOND_BASS = "m6/8 g2:3/2 g3:3/2 | bb2:3/2 a2:3/2 | g2:3/2 g3:3/2 | d3:3/2 d2:3/2 | " \
              "g2:3/2 g3:3/2 | eb2:3/2 f#2:3/2 | g2:3/2 d2:3/2 | g2:3 |"


def play(orchestra, melody, bass, dynamic, label, **kwargs):
    orchestra.play({"flutes": f"!{dynamic} " + melody, "violins": f"!{dynamic} " + melody,
                    "violins 2": (f"!{dynamic} " + melody, -12), "violas": (f"!{dynamic} " + bass, 16),
                    "cellos": f"!{dynamic} " + bass, "basses": (f"!{dynamic} " + bass, -12),
                    "bassoons": f"!{dynamic} " + bass, "harpsichord": (f"!{dynamic} " + bass, 12)},
                   bpm=160, label=label, **kwargs)


def picture(orchestra):
    for dynamic in ("mf", "mp"):
        play(orchestra, FIRST, FIRST_BASS, dynamic, "gigue I")
    for dynamic in ("mp", "p"):
        play(orchestra, SECOND, SECOND_BASS, dynamic, "gigue II")
    play(orchestra, FIRST, FIRST_BASS, "f", "gigue I again", to=136)


def gigues():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
