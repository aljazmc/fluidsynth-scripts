from orchestra import Orchestra

# Handel, Messiah, Part II, No. 43. Thou shalt break them with a rod of iron
# (air, tenor). A from-memory arrangement for General MIDI baroque orchestra,
# the tenor singing without words: the A minor air in 3/4 whose violins leap
# about jaggedly, "dashing them in pieces like a potter's vessel", in
# Handel's manner; the notes are approximate.
SEED = 1783

PARTS = ("tenor", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Andante, 3/4
DASH = ("m3/4 a4:1/2 e5 c5 a5 e5 c5 | b4:1/2 e5 g#4 b5 e5 g#4 | c5:1/2 a5 e5 c6 a5 e5 | d5:1/2 f5 b4 g#5 e5 b4 | "
        "c5:1/2 e5 a4 c6 a5 e5 | d5:1/2 f5 d5 b5 g#5 e5 | c5:1/2 a5 b4 g#5 e5 g#4 | a4:3 |")
LINE = ("m3/4 a3:1 c4:1 e4:1 | e4:3/2 d4:1/2 b3:1 | c4:1 e4:1 a4:1 | g#4:2 e4:1 | "
        "a4:1 e4:1 c4:1 | d4:1 f4:1 b3:1 | c4:1 b3:1 g#3:1 | a3:3 |")
BASS = "m3/4 a2:3 | e2:3 | a2:3 | e2:3 | a2:3 | d2:2 e2:1 | a1:1 e2:1 e1:1 | a1:3 |"


def picture(orchestra):
    orchestra.play({"violins": "!f " + DASH, "violins 2": ("!mf " + DASH, -12), "violas": ("!mf " + BASS, 12),
                    "cellos": "!f " + BASS, "basses": ("!f " + BASS, -12), "harpsichord": ("!mf " + BASS, 12)},
                   bpm=104, label="ritornello")
    for shift in (0, 7, 0):
        orchestra.play({"tenor": ("!f " + LINE, shift), "violins": ("!mf " + DASH, shift), "violas": ("!p " + BASS, 12 + shift),
                        "cellos": ("!mf " + BASS, shift), "basses": ("!mf " + BASS, shift - 12),
                        "harpsichord": ("!mf " + BASS, 12 + shift)}, bpm=104, label="thou shalt break them")
    orchestra.play({"violins": "!f " + DASH, "violins 2": ("!mf " + DASH, -12), "cellos": "!f " + BASS,
                    "basses": ("!f " + BASS, -12), "harpsichord": ("!mf " + BASS, 12)}, bpm=104, to=88, label="ritornello")


def them():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
