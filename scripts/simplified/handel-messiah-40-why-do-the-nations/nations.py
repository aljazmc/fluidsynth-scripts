from orchestra import Orchestra

# Handel, Messiah, Part II, No. 40. Why do the nations so furiously rage
# together (air, bass). A from-memory arrangement for General MIDI baroque
# orchestra, the bass singing without words: the strings' furious repeated
# semiquavers in C major and the bass's raging runs follow Handel, the notes
# are approximate.
SEED = 1780

PARTS = ("bass voice", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
RAGE = "m4/4 " + " ".join(f"{c}:1/4 " * 16 + "|" for c in ("c5", "e5", "g5", "c5", "f5", "g5", "g4", "c5"))
RAGE_INNER = "m4/4 " + " ".join(f"{c}:1/4 " * 16 + "|" for c in ("e4+g4", "g4+c5", "e4+c5", "e4+g4", "a4+c5", "g4+b4", "f4+b4", "e4+g4"))
BASS = "m4/4 " + " ".join(f"{c}:1/2 " * 8 + "|" for c in ("c3", "c3", "c3", "a2", "f2", "g2", "g2", "c3"))
WHY = ("m4/4 c3:1 c3:1/2 c3:1/2 g3:1 g3:1 | c4:1/4 b3 a3 g3 f3 e3 d3 c3 g3:2 | "
       "e3:1 e3:1/2 e3:1/2 a3:1 a3:1 | f3:1/4 g3 a3 b3 c4 b3 a3 g3 a3:2 | "
       "f3:1/4 g3 a3 bb3 a3 g3 f3 e3 f3:1 d3:1 | g3:1/4 a3 b3 c4 b3 a3 g3 f3 e3:1 c3:1 | "
       "f3:1 d3:1 g3:1 g2:1 | c3:4 |")


def picture(orchestra):
    strings = {"violins": "!f " + RAGE, "violins 2": "!f " + RAGE_INNER, "violas": ("!mf " + RAGE_INNER, -12),
               "cellos": "!f " + BASS, "basses": ("!f " + BASS, -12), "harpsichord": ("!mf " + BASS, 12)}
    orchestra.play(strings, bpm=128, label="ritornello")
    orchestra.play({**strings, "bass voice": "!f " + WHY, "violins": "!mf " + RAGE, "violins 2": "!mf " + RAGE_INNER},
                   bpm=128, label="why do the nations")
    orchestra.play({**strings, "bass voice": ("!f " + WHY, 7), "violins": ("!mf " + RAGE, 7),
                    "violins 2": ("!mf " + RAGE_INNER, 7), "cellos": ("!f " + BASS, 7), "basses": ("!f " + BASS, -5)},
                   bpm=128, label="in G")
    orchestra.play({**strings, "bass voice": "!f " + WHY, "violins": "!mf " + RAGE, "violins 2": "!mf " + RAGE_INNER},
                   bpm=128)
    orchestra.play(strings, bpm=128, to=112, label="ritornello")


def nations():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
