from orchestra import Orchestra

# Handel, Messiah, Part I, No. 20. He shall feed his flock (air, alto and
# soprano). A from-memory arrangement for General MIDI baroque orchestra,
# voices without words: the gentle 12/8 pastoral, first in F major for the
# alto, then a fourth higher in B-flat for the soprano, "Come unto him, all ye
# that labour", follows Handel; the tune is close, the rest approximate.
SEED = 1760

PARTS = ("alto", "soprano", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Larghetto, 12/8 (six crotchet beats)
FEED = ("m12/8 c5:3/2 a4:1/2 bb4:1 c5:3/2 f5:1/2 c5:1 | d5:3/2 c5:1/2 bb4:1 a4:3/2 g4:1/2 f4:1 | "
        "g4:3/2 a4:1/2 bb4:1 c5:3/2 bb4:1/2 a4:1 | g4:3 c4:3 | "
        "c5:3/2 a4:1/2 bb4:1 c5:3/2 f5:1/2 e5:1 | d5:3/2 e5:1/2 f5:1 c5:3/2 bb4:1/2 a4:1 | "
        "bb4:1 a4:1/2 g4:1 f4:1/2 a4:3/2 g4:1/2 f4:1 | f4:6 |")
BASS = "m12/8 f2:3 a2:3 | bb2:3 f2:3 | e2:3 f2:3 | c3:3 c2:3 | f2:3 a2:3 | bb2:3 a2:3 | bb2:3/2 c3:3/2 c2:3 | f2:6 |"
PAD = "m12/8 a3+c4:6 | bb3+d4:3 a3+c4:3 | g3+c4:3 a3+c4:3 | g3+bb3+e4:6 | a3+c4:6 | bb3+d4:3 a3+c4:3 | bb3+d4:3/2 g3+c4:3/2 g3+bb3:3 | a3+c4:6 |"


def phrase(orchestra, voice, dynamic, shift, label):
    orchestra.play({voice: f"!{dynamic} " + FEED, "violins 2": "!pp " + PAD, "violas": ("!pp " + PAD, -12),
                    "cellos": "!p " + BASS, "basses": ("!p " + BASS, -12), "harpsichord": ("!pp " + PAD, 0)},
                   bpm=80, shift=shift, label=label)


def picture(orchestra):
    orchestra.play({"violins": "!mp " + FEED, "violins 2": "!pp " + PAD, "violas": ("!pp " + PAD, -12),
                    "cellos": "!p " + BASS, "basses": ("!p " + BASS, -12), "harpsichord": "!pp " + PAD},
                   bpm=80, label="ritornello")
    phrase(orchestra, "alto", "mp", 0, "he shall feed his flock")
    phrase(orchestra, "soprano", "mp", 5, "come unto him")
    orchestra.play({"violins": "!p " + FEED, "violins 2": "!pp " + PAD, "violas": ("!pp " + PAD, -12),
                    "cellos": "!pp " + BASS, "basses": ("!pp " + BASS, -12), "harpsichord": "!pp " + PAD},
                   bpm=80, to=68, shift=5, label="ritornello")


def flock():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
