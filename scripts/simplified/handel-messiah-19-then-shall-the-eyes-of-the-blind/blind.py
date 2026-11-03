from orchestra import Orchestra

# Handel, Messiah, Part I, No. 19. Then shall the eyes of the blind be opened
# (recitative, alto). A from-memory arrangement for General MIDI baroque
# orchestra, the alto singing without words over harpsichord and cello: a
# short secco recitative ending in F major, ready for "He shall feed his
# flock", in Handel's manner; the notes are approximate.
SEED = 1759

PARTS = ("alto", "harpsichord", "cellos", "basses")

LINE = ("m4/4 r:1 c5:1/2 c5:1/2 a4:1 f4:1/2 g4:1/2 | a4:1/2 a4:1/2 bb4:1/2 c5:1/2 f4:1 r:1 | "
        "r:1 d5:1/2 d5:1/2 bb4:1 g4:1/2 a4:1/2 | bb4:1/2 c5:1/2 d5:1 g4:1 r:1 | "
        "r:1 e5:1/2 c5:1/2 g4:1 bb4:1/2 a4:1/2 | g4:1/2 a4:1/2 f4:1 r:2 |")
CHORDS = "m4/4 f3+a3+c4:4 | f3+a3+c4:4 | g3+bb3+d4:4 | g3+bb3+d4:4 | c3+e3+g3+bb3:4 | f3+a3+c4:4 |"
BASS = "m4/4 f2:4 | a2:4 | bb2:4 | g2:4 | c3:4 | f2:4 |"


def picture(orchestra):
    orchestra.play({"alto": "!mp " + LINE, "harpsichord": "!mp " + CHORDS, "cellos": "!mp " + BASS,
                    "basses": ("!p " + BASS, -12)}, bpm=76, label="recitative")
    orchestra.play({"harpsichord": "!mp m4/4 c3+e3+g3+bb3:1 f2+a2+c3+f3:1 r:2 |", "cellos": "!mp m4/4 c3:1 f2:1 r:2 |"},
                   bpm=76, label="cadence")


def blind():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
