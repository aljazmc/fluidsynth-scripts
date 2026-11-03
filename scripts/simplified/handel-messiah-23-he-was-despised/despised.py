from orchestra import Orchestra

# Handel, Messiah, Part II, No. 23. He was despised (air, alto). A
# from-memory arrangement for General MIDI baroque orchestra, the alto
# singing without words: the long, sorrowful E-flat major Largo with its
# sighing pauses, the agitated C minor middle "He gave his back to the
# smiters" over jabbing dotted strings, and the return, follow Handel, the
# notes are approximate.
SEED = 1763

PARTS = ("alto", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Largo, 4/4
DESPISED = ("m4/4 bb4:2 r:1 bb4:1/2 bb4:1/2 | eb5:2 r:1 bb4:1 | c5:1 bb4:1/2 ab4:1/2 g4:1 f4:1 | g4:2 r:2 | "
            "g4:1 ab4:1 bb4:1 eb5:1 | d5:1 c5:1 bb4:1 ab4:1 | g4:3/2 f4:1/2 f4:1 eb4:1 | eb4:4 |")
BASS = "m4/4 eb3:2 g2:2 | c3:2 g2:2 | ab2:2 bb2:2 | eb2:4 | eb3:2 c3:2 | f2:2 bb2:2 | bb2:2 bb1:2 | eb2:4 |"
PAD = "m4/4 g3+bb3:4 | g3+c4:4 | ab3+c4:2 f3+bb3:2 | g3+bb3:4 | g3+bb3:2 g3+c4:2 | f3+ab3:2 f3+bb3:2 | eb3+bb3:2 d3+ab3:2 | g3+bb3:4 |"

SMITERS = ("m4/4 g4:3/4 g4:1/4 c5:3/4 c5:1/4 g4:3/4 g4:1/4 eb4:3/4 eb4:1/4 | "
           "ab4:3/4 ab4:1/4 f4:3/4 f4:1/4 d4:2 | "
           "g4:3/4 g4:1/4 eb5:3/4 eb5:1/4 d5:3/4 d5:1/4 c5:3/4 c5:1/4 | b4:2 r:2 |")
JABS = "m4/4 " + " ".join(f"r:1/4 {c}:1/4 " * 8 + "|" for c in ("eb4+g4", "f4+ab4", "eb4+g4", "d4+f4"))
JABS_BASS = "m4/4 c3:4 | f2:2 g2:2 | c3:2 f#2:2 | g2:4 |"


def picture(orchestra):
    pad = {"violins 2": "!pp " + PAD, "violas": ("!pp " + PAD, -12), "cellos": "!p " + BASS,
           "basses": ("!p " + BASS, -12), "harpsichord": "!pp " + PAD}
    orchestra.play({"violins": "!p " + DESPISED, **pad}, bpm=46, label="ritornello")
    orchestra.play({"alto": "!mp " + DESPISED, **pad}, bpm=46, label="he was despised")
    orchestra.play({"alto": "!mf " + SMITERS, "violins": ("!f " + JABS, 12), "violins 2": "!f " + JABS,
                    "cellos": "!f " + JABS_BASS, "basses": ("!f " + JABS_BASS, -12)}, bpm=72, label="smiters")
    orchestra.play({"alto": "!mf " + SMITERS, "violins": ("!f " + JABS, 12), "violins 2": "!f " + JABS,
                    "cellos": "!f " + JABS_BASS, "basses": ("!f " + JABS_BASS, -12)}, bpm=72, to=56)
    orchestra.play({"alto": "!p " + DESPISED, **pad}, bpm=44, to=40, label="da capo")


def despised():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render()
