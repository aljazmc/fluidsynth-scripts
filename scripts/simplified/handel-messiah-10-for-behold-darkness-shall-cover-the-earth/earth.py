from orchestra import Orchestra

# Handel, Messiah, Part I, No. 10. For behold, darkness shall cover the earth
# (accompanied recitative, bass). A from-memory arrangement for General MIDI
# baroque orchestra, the bass singing without words: murky B minor strings
# creeping in quavers, brightening to D major at "but the Lord shall arise
# upon thee", in Handel's manner; the notes are approximate.
SEED = 1750

PARTS = ("bass voice", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Larghetto, 4/4
CREEP = "m4/4 " + " ".join(f"{a}:1/2 {b} {a} {b} {c} {d} {c} {d} |" for a, b, c, d in (
    ("b3", "c#4", "d4", "c#4"), ("b3", "a#3", "b3", "c#4"), ("d4", "e4", "f#4", "e4"), ("d4", "c#4", "b3", "a#3")))
DARK = ("m4/4 r:2 f#3:1/2 f#3:1/2 b3:1 | f#3:1/2 f#3:1/2 d3:1 b2:1 r:1 | "
        "r:1 d3:1/2 e3:1/2 f#3:1 g3:1/2 f#3:1/2 | e3:2 f#3:2 |")
DARK_BASS = "m4/4 b2:4 | b2:4 | b2:4 | f#2:4 |"
ARISE = ("m4/4 r:1 a3:1/2 a3:1/2 d4:1 a3:1 | f#3:1/2 g3:1/2 a3:1 d3:2 | "
         "r:1 b3:1/2 a3:1/2 g3:1 f#3:1/2 e3:1/2 | a3:2 a2:2 | d3:4 |")
ARISE_CHORDS = "m4/4 d4+f#4+a4:4 | d4+f#4+a4:4 | g3+b3+d4:4 | e3+g3+a3+c#4:4 | d4+f#4+a4:4 |"
ARISE_BASS = "m4/4 d3:4 | d3:4 | g2:4 | a2:4 | d2:4 |"


def picture(orchestra):
    strings = {"violins": ("!p " + CREEP, 12), "violins 2": "!p " + CREEP, "violas": ("!pp " + CREEP, -12),
               "cellos": "!p " + DARK_BASS, "basses": ("!p " + DARK_BASS, -12)}
    orchestra.play(strings, bpm=60, label="darkness")
    orchestra.play({**strings, "bass voice": "!mp " + DARK}, bpm=60)
    orchestra.play({"bass voice": "!f " + ARISE, "violins": ("!mf " + ARISE_CHORDS, 12), "violins 2": "!mf " + ARISE_CHORDS,
                    "violas": ("!mf " + ARISE_CHORDS, -12), "cellos": "!mf " + ARISE_BASS, "basses": ("!mf " + ARISE_BASS, -12),
                    "harpsichord": "!mf " + ARISE_CHORDS}, bpm=66, to=56, label="the Lord shall arise")


def earth():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
