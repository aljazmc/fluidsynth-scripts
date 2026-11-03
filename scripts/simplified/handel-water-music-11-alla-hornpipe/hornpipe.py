from orchestra import Orchestra

# Handel, Water Music, Suite No. 2 in D major, HWV 349, 2. Alla Hornpipe. A
# from-memory arrangement for General MIDI baroque band: the famous festive
# hornpipe in D, its bold opening tossed between trumpets and strings, a
# quieter B minor middle without the brass, and the opening section again,
# in Handel's manner; the tune is close, the rest approximate.
SEED = 1727

PARTS = ("oboes", "bassoons", "horns", "trumpets", "timpani", "harpsichord",
         "violins", "violins 2", "violas", "cellos", "basses")

# 3/2 (six crotchets)
TUNE = ("m3/2 d5:2 a4:1 d5:1 f#5:1 d5:1 | a5:2 f#5:1 a5:1 d6:2 | c#6:1 b5:1 a5:1 g5:1 f#5:1 e5:1 | "
        "f#5:1 e5:1 d5:2 a4:2 | d5:2 a4:1 d5:1 f#5:1 d5:1 | a5:2 f#5:1 a5:1 d6:2 | "
        "b5:1 a5:1 g5:1 f#5:1 e5:1 d5:1 | e5:4 a4:2 |")
TUNE_END = ("m3/2 a5:2 g5:1 f#5:1 e5:1 d5:1 | g5:2 f#5:1 e5:1 d5:1 c#5:1 | d5:1 f#5:1 e5:2 a4:2 | d5:6 |")
BASS = "m3/2 d3:2 d2:2 d3:2 | f#2:2 d2:2 f#2:2 | a2:2 a1:2 a2:2 | d2:2 d3:2 f#2:2 | " \
       "d3:2 d2:2 d3:2 | f#2:2 d2:2 f#2:2 | g2:2 a2:2 b2:2 | a2:4 a1:2 |"
BASS_END = "m3/2 f#2:2 d2:2 f#2:2 | e2:2 a2:2 a1:2 | b1:2 a1:2 a2:2 | d2:6 |"

# the middle, in B minor, strings and oboes only
MIDDLE = ("m3/2 b4:2 f#4:1 b4:1 d5:1 b4:1 | f#5:2 d5:1 f#5:1 b5:2 | a5:1 g5:1 f#5:1 e5:1 d5:1 c#5:1 | "
          "d5:2 c#5:2 b4:2 | g5:2 e5:1 g5:1 b5:1 g5:1 | f#5:2 d5:1 f#5:1 a5:2 | g5:1 f#5:1 e5:1 d5:1 c#5:1 b4:1 | "
          "c#5:4 f#4:2 |")
MIDDLE_BASS = "m3/2 b2:2 b1:2 b2:2 | d3:2 b2:2 d3:2 | f#2:2 f#3:2 f#2:2 | b2:2 f#2:2 b1:2 | " \
              "e2:2 e3:2 e2:2 | d2:2 d3:2 d2:2 | e2:2 f#2:2 g2:2 | f#2:4 f#1:2 |"


def bright(orchestra, dynamic):
    parts = {"violins": f"!{dynamic} " + TUNE + " " + TUNE_END[5:], "oboes": f"!{dynamic} " + TUNE + " " + TUNE_END[5:],
             "trumpets": f"!{dynamic} " + TUNE + " " + TUNE_END[5:],
             "violins 2": (f"!{dynamic} " + TUNE + " " + TUNE_END[5:], -12),
             "horns": (f"!{dynamic} " + BASS + " " + BASS_END[5:], 24),
             "violas": (f"!{dynamic} " + BASS + " " + BASS_END[5:], 16),
             "cellos": f"!{dynamic} " + BASS + " " + BASS_END[5:],
             "basses": (f"!{dynamic} " + BASS + " " + BASS_END[5:], -12),
             "bassoons": f"!{dynamic} " + BASS + " " + BASS_END[5:],
             "harpsichord": (f"!{dynamic} " + BASS + " " + BASS_END[5:], 12),
             "timpani": f"!{dynamic} m3/2 " + " ".join(["d2:2 r:2 a1:2 |"] * 12)}
    orchestra.play(parts, bpm=176, label="hornpipe")


def picture(orchestra):
    bright(orchestra, "f")
    orchestra.play({"violins": "!mp " + MIDDLE, "oboes": "!mp " + MIDDLE, "violins 2": ("!p " + MIDDLE, -12),
                    "violas": ("!p " + MIDDLE_BASS, 16), "cellos": "!p " + MIDDLE_BASS,
                    "basses": ("!p " + MIDDLE_BASS, -12), "harpsichord": ("!p " + MIDDLE_BASS, 12)},
                   bpm=176, label="middle")
    bright(orchestra, "f")


def hornpipe():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
