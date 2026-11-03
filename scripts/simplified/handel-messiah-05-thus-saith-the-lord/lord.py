from orchestra import Orchestra

# Handel, Messiah, Part I, No. 5. Thus saith the Lord (accompanied recitative,
# bass). A from-memory arrangement for General MIDI baroque orchestra, the
# bass singing without words: the strings' jagged dotted D minor figures, the
# bass's long, shuddering run on "I will shake" and the calmer close "the
# desire of all nations shall come" follow Handel, the notes are approximate.
SEED = 1745

PARTS = ("bass voice", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 4/4
DOTTED = "m4/4 r:1 d5:3/4 d5:1/4 a4:3/4 a4:1/4 f4:3/4 f4:1/4 | d4:1 r:1 a4:3/4 a4:1/4 e4:3/4 e4:1/4 |"
DOTTED_LOW = "m4/4 r:1 f4:3/4 f4:1/4 d4:3/4 d4:1/4 a3:3/4 a3:1/4 | f3:1 r:1 c#4:3/4 c#4:1/4 a3:3/4 a3:1/4 |"
DOTTED_BASS = "m4/4 d3:1 r:3 | d2:1 r:1 a2:2 |"
THUS = ("m4/4 r:2 a3:1/2 a3:1/2 d4:1 | a3:1/2 a3:1/2 f3:1 d3:1 r:1 | "
        "r:1 d4:1/2 c4:1/2 bb3:1 a3:1/2 g3:1/2 | a3:2 r:2 |")
SHAKE = ("m4/4 r:1 a3:1/2 a3:1/2 d4:1/4 e4 f4 e4 d4 c#4 b3 c#4 | d4:1/4 e4 f4 g4 a4 g4 f4 e4 f4 e4 d4 c#4 d4 c4 bb3 a3 | "
         "bb3:1/4 c4 d4 c4 bb3 a3 g3 a3 bb3 a3 g3 f3 e3 f3 g3 e3 | f3:1/4 g3 a3 g3 f3 e3 d3 e3 f3:1 r:1 | "
         "r:1 a3:1/2 a3:1/2 d4:1 c#4:1 | d4:2 r:2 |")
SHAKE_STRINGS = "m4/4 " + " ".join(f"{c}:1/4 " * 16 + "|" for c in ("d4+f4", "d4+f4", "d4+g4", "c4+f4", "c#4+e4", "d4+f4"))
SHAKE_BASS = "m4/4 d3:4 | d3:4 | g2:4 | a2:4 | a2:4 | d2:4 |"
DESIRE = ("m4/4 r:1 f3:1/2 f3:1/2 bb3:1 bb3:1/2 a3:1/2 | g3:1 g3:1/2 f3:1/2 e3:1 r:1 | "
          "r:1 a3:1/2 a3:1/2 c#4:1 d4:1/2 a3:1/2 | f3:1/2 g3:1/2 a3:1 d3:2 |")
DESIRE_CHORDS = "m4/4 bb2+d3+f3:4 | c3+e3+g3:4 | a2+c#3+e3:4 | d3+f3+a3:2 a2+c#3+e3:1 d3+f3+a3:1 |"


def picture(orchestra):
    orchestra.play({"violins": "!f " + DOTTED, "violins 2": "!f " + DOTTED_LOW, "violas": ("!f " + DOTTED_LOW, -12),
                    "cellos": "!f " + DOTTED_BASS, "basses": ("!f " + DOTTED_BASS, -12)}, bpm=72, label="strings")
    orchestra.play({"bass voice": "!f " + THUS, "harpsichord": "!mf m4/4 d3+f3+a3:4 | d3+f3+a3:4 | g2+bb2+d3:4 | a2+c#3+e3:4 |",
                    "cellos": "!mf m4/4 d3:4 | d3:4 | g2:4 | a2:4 |"}, bpm=72, label="thus saith")
    orchestra.play({"violins": "!f " + DOTTED, "violins 2": "!f " + DOTTED_LOW, "violas": ("!f " + DOTTED_LOW, -12),
                    "cellos": "!f " + DOTTED_BASS, "basses": ("!f " + DOTTED_BASS, -12)}, bpm=72)
    orchestra.play({"bass voice": "!f " + SHAKE, "violins": ("!mf " + SHAKE_STRINGS, 12), "violas": "!mf " + SHAKE_STRINGS,
                    "cellos": "!mf " + SHAKE_BASS, "basses": ("!mf " + SHAKE_BASS, -12)}, bpm=72, label="I will shake")
    orchestra.play({"bass voice": "!mf " + DESIRE, "harpsichord": "!mp " + DESIRE_CHORDS,
                    "violins 2": ("!p " + DESIRE_CHORDS, 12), "violas": ("!p " + DESIRE_CHORDS, 0),
                    "cellos": "!mp m4/4 bb2:4 | c3:4 | a2:4 | d3:2 a2:1 d2:1 |"}, bpm=66, to=56, label="the desire")


def lord():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
