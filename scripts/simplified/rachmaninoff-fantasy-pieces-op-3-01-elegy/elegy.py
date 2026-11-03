from piano import Piece, pitch

# Rachmaninoff, Morceaux de fantaisie (Fantasy Pieces), Op. 3, No. 1, Élégie
# in E-flat minor. A from-memory piano arrangement: a grieving melody over
# wide, rolling left-hand arpeggios, a stormier middle and a return that sinks
# back into E-flat minor, in Rachmaninoff's manner; the notes are approximate.
SEED = 1893

MINOR = (0, 7, 15, 19)
MAJOR = (0, 7, 16, 19)
SEVENTH = (0, 7, 16, 22)


def roll(root, quality):
    """Eight quavers rolling up and back down over a low root."""
    r = pitch(root)
    a, b, c, d = (r + q for q in quality)
    return " ".join(f"{n}:1/2" for n in (a, b, c, d, c, b, c, b)) + " |"


GRIEF = (
    ("bb4:2 gb4:1 f4:1", "eb2", MINOR),
    ("eb4:3 f4:1", "ab1", MINOR),
    ("gb4:2 f4:1 eb4:1", "bb1", SEVENTH),
    ("d4:3 bb3:1", "bb1", SEVENTH),
    ("eb4:2 gb4:1 bb4:1", "eb2", MINOR),
    ("eb5:3 db5:1", "cb2", MAJOR),
    ("cb5:2 bb4:1 ab4:1", "ab1", MINOR),
    ("bb4:4", "bb1", SEVENTH),
)
STORM = (
    ("gb5:2 f5:1 eb5:1", "eb2", MINOR),
    ("db5:2 cb5:1 bb4:1", "gb1", MAJOR),
    ("ab4:2 cb5:1 eb5:1", "ab1", MINOR),
    ("gb5:3 f5:1", "db2", SEVENTH),
    ("f5:2 eb5:1 db5:1", "gb1", MAJOR),
    ("cb5:2 bb4:1 ab4:1", "cb2", MAJOR),
    ("bb4:2 a4:1 bb4:1", "f1", SEVENTH),
    ("bb4:4", "bb1", SEVENTH),
)
HOME = GRIEF[:7] + (("eb4:4", "eb2", MINOR),)


def play(piece, bars, dynamic, shift=0, **kwargs):
    piece.play((f"m4/4 !{dynamic} " + " ".join(f"{m} |" for m, _, _ in bars), shift),
               f"m4/4 !p " + " ".join(roll(r, q) for _, r, q in bars), pedal="bar", **kwargs)


def picture(piece):
    play(piece, GRIEF, "mp", bpm=72, label="grief")
    play(piece, GRIEF, "mf", shift=12, bpm=74)
    play(piece, STORM, "f", bpm=84, to=92, label="storm")
    play(piece, STORM, "ff", shift=0, bpm=92, to=72)
    play(piece, HOME, "mp", bpm=70, to=58, label="home")
    piece.play("m4/4 !pp gb3+bb3+eb4:4~ | gb3+bb3+eb4:4 |", "m4/4 !pp eb1+eb2:4~ | eb1+eb2:4 |",
               bpm=56, pedal=8)


def elegy():
    piece = Piece(SEED, reverb=80)
    picture(piece)
    return piece.render(tail=5.0)
