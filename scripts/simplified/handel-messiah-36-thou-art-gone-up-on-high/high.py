from orchestra import Orchestra

# Handel, Messiah, Part II, No. 36. Thou art gone up on high (air, bass). A
# from-memory arrangement for General MIDI baroque orchestra, the bass
# singing without words: a stately D minor air in 3/4, its line climbing up
# "on high", with violins answering, in Handel's manner; the notes are
# approximate.
SEED = 1776

PARTS = ("bass voice", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro larghetto, 3/4
LINE = ("m3/4 d3:1 a3:1 d4:1 | c#4:3/2 d4:1/2 e4:1 | f4:1 e4:1/2 d4:1/2 c#4:1 | d4:3 | "
        "f3:1 bb3:1 d4:1 | e4:3/2 f4:1/2 g4:1 | a4:1 g4:1/2 f4:1/2 e4:1 | f4:2 r:1 | "
        "d4:1 bb3:1 g3:1 | e3:1 a3:1 c#4:1 | d4:1 a3:1 f3:1 | e3:3 | f3:1 g3:1 a3:1 | bb3:1 a3:1 g3:1 | f3:1 e3:1 a2:1 | d3:3 |")
BASS = ("m3/4 d3:3 | a2:3 | d3:1 g2:1 a2:1 | d2:3 | d3:3 | c3:3 | c3:2 c2:1 | f2:3 | "
        "g2:3 | a2:3 | d3:3 | a2:3 | d3:3 | g2:3 | a2:3 | d2:3 |")


def picture(orchestra):
    pad = {"violins 2": ("!pp " + BASS, 17), "violas": ("!pp " + BASS, 12), "cellos": "!p " + BASS,
           "basses": ("!p " + BASS, -12), "harpsichord": ("!p " + BASS, 12)}
    orchestra.play({"violins": ("!mf " + LINE, 12), **pad}, bpm=96, label="ritornello")
    orchestra.play({"bass voice": "!mf " + LINE, "violins": ("!p " + LINE, 24), **pad}, bpm=96, label="thou art gone up")
    orchestra.play({"violins": ("!mf " + LINE, 12), **pad}, bpm=96, to=80, label="ritornello")


def high():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
