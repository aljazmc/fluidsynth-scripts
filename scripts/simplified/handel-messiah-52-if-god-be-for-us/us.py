from orchestra import Orchestra

# Handel, Messiah, Part III, No. 52. If God be for us, who can be against us?
# (air, soprano). A from-memory arrangement for General MIDI baroque
# orchestra, the soprano singing without words: a calm, trusting G minor
# Larghetto in 3/4 with a solo violin line weaving around the voice, in
# Handel's manner; the notes are approximate.
SEED = 1792

PARTS = ("soprano", "solo violin", "harpsichord", "violins 2", "violas", "cellos", "basses")

# Larghetto, 3/4
LINE = ("m3/4 d5:1 g5:1 f#5:1 | g5:3/2 a5:1/2 bb5:1 | a5:1 g5:1 f#5:1 | g5:2 d5:1 | "
        "eb5:1 d5:1 c5:1 | bb4:3/2 c5:1/2 d5:1 | c5:1 bb4:1 a4:1 | bb4:2 d5:1 | "
        "eb5:1 c5:1 a4:1 | d5:1 bb4:1 g4:1 | c5:1 bb4:1 a4:1 | g4:3 |")
VIOLIN = ("m3/4 bb5:1/2 a5 g5 a5 bb5 c6 | d6:1/2 c6 bb5 a5 g5 f#5 | g5:1/2 a5 bb5 a5 g5 f#5 | g5:3 | "
          "c6:1/2 bb5 a5 g5 f5 eb5 | d5:1/2 eb5 f5 g5 f5 eb5 | eb5:1/2 d5 c5 d5 eb5 c5 | d5:3 | "
          "c5:1/2 eb5 g5 eb5 c5 a4 | bb4:1/2 d5 g5 d5 bb4 g4 | a4:1/2 c5 eb5 c5 f#4 a4 | g4:3 |")
BASS = "m3/4 g2:3 | g2:3 | d3:3 | g2:3 | c3:3 | g2:3 | f2:3 | bb2:3 | c3:3 | g2:3 | d3:3 | g2:3 |"
PAD = "m3/4 bb3+d4:3 | bb3+d4:3 | a3+c4:3 | bb3+d4:3 | c4+eb4:3 | bb3+d4:3 | a3+c4:3 | bb3+d4:3 | c4+eb4:3 | bb3+d4:3 | a3+c4:3 | bb3+d4:3 |"


def picture(orchestra):
    strings = {"violins 2": "!pp " + PAD, "violas": ("!pp " + PAD, -12), "cellos": "!p " + BASS,
               "basses": ("!p " + BASS, -12), "harpsichord": "!pp " + PAD}
    orchestra.play({"solo violin": "!mp " + VIOLIN, **strings}, bpm=72, label="ritornello")
    orchestra.play({"soprano": "!mp " + LINE, "solo violin": "!p " + VIOLIN, **strings}, bpm=72, label="if God be for us")
    orchestra.play({"soprano": "!mp " + LINE, "solo violin": "!p " + VIOLIN, **strings}, bpm=72, to=62)
    orchestra.play({"solo violin": "!p " + VIOLIN, **strings}, bpm=66, to=56, label="ritornello")


def us():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
