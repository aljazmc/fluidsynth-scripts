from orchestra import Orchestra

# Handel, Messiah, Part I, No. 14. There were shepherds abiding in the field
# (recitative, soprano) - And lo, the angel of the Lord came upon them
# (accompanied recitative). A from-memory arrangement for General MIDI baroque
# orchestra, the soprano singing without words: a plain C major recitative
# over the continuo, then the strings' shimmering broken chords in F as the
# angel appears, in Handel's manner; the notes are approximate.
SEED = 1754

PARTS = ("soprano", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

SHEPHERDS = ("m4/4 r:1 g4:1/2 g4:1/2 c5:1 g4:1/2 e4:1/2 | f4:1/2 g4:1/2 a4:1/2 g4:1/2 f4:1 e4:1 | "
             "r:1 c5:1/2 b4:1/2 a4:1 g4:1/2 f4:1/2 | e4:1 d4:1 c4:1 r:1 |")
SHEPHERDS_CHORDS = "m4/4 c3+e3+g3:4 | d3+f3+a3:2 g2+b2+d3:2 | f3+a3+c4:4 | g2+b2+d3+f3:2 c3+e3+g3:2 |"
SHEPHERDS_BASS = "m4/4 c3:4 | d3:2 g2:2 | f2:4 | g2:2 c2:2 |"
LO = ("m4/4 r:1 c5:1/2 c5:1/2 a4:1 f4:1/2 g4:1/2 | a4:1/2 bb4:1/2 c5:1 f4:1 r:1 | "
      "r:1 d5:1/2 c5:1/2 bb4:1 a4:1/2 g4:1/2 | a4:1 bb4:1/2 g4:1/2 f4:2 |")
SHIMMER = "m4/4 " + " ".join(f"{a}:1/4 {b} {c} {b} " * 4 + "|" for a, b, c in (
    ("f4", "a4", "c5"), ("f4", "a4", "c5"), ("g4", "bb4", "d5"), ("f4", "a4", "c5")))
LO_BASS = "m4/4 f2:4 | f2:4 | g2:2 c3:2 | f2:4 |"


def picture(orchestra):
    orchestra.play({"soprano": "!mp " + SHEPHERDS, "harpsichord": "!mp " + SHEPHERDS_CHORDS,
                    "cellos": "!mp " + SHEPHERDS_BASS, "basses": ("!p " + SHEPHERDS_BASS, -12)}, bpm=76, label="shepherds")
    orchestra.play({"soprano": "!mf " + LO, "violins": "!p " + SHIMMER, "violins 2": ("!p " + SHIMMER, -12),
                    "violas": "!pp m4/4 c4:4 | c4:4 | bb3:4 | a3:4 |", "cellos": "!p " + LO_BASS,
                    "basses": ("!p " + LO_BASS, -12)}, bpm=72, label="and lo, the angel")
    orchestra.play({"violins": "!p m4/4 f4+a4+c5:4 |", "violas": "!p m4/4 c4:4 |", "cellos": "!p m4/4 f2:4 |",
                    "harpsichord": "!p m4/4 f2+a2+c3:4 |"}, bpm=66, label="cadence")


def field():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
