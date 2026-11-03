from orchestra import Orchestra

# Handel, Messiah, Part III, No. 49. Then shall be brought to pass the saying
# that is written (recitative, alto). A from-memory arrangement for General
# MIDI baroque orchestra, the alto singing without words over harpsichord and
# cello: a few bars of secco recitative ending in E-flat for the duet, in
# Handel's manner; the notes are approximate.
SEED = 1789

PARTS = ("alto", "harpsichord", "cellos", "basses")

LINE = ("m4/4 r:1 bb4:1/2 bb4:1/2 g4:1 eb4:1/2 f4:1/2 | g4:1/2 ab4:1/2 bb4:1 eb4:1 r:1 | "
        "r:1 c5:1/2 bb4:1/2 ab4:1 g4:1/2 f4:1/2 | g4:1/2 eb4:1/2 f4:1 eb4:2 |")
CHORDS = "m4/4 eb3+g3+bb3:4 | eb3+g3+bb3:4 | ab2+c3+eb3:4 | bb2+d3+f3:2 eb3+g3+bb3:2 |"
BASS = "m4/4 eb3:4 | g2:4 | ab2:4 | bb2:2 eb2:2 |"


def picture(orchestra):
    orchestra.play({"alto": "!mp " + LINE, "harpsichord": "!mp " + CHORDS, "cellos": "!mp " + BASS,
                    "basses": ("!p " + BASS, -12)}, bpm=80, label="recitative")


def saying():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
