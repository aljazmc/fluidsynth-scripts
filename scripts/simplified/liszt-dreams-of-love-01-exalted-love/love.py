from piano import Piece, pitch, run

# Liszt, Liebesträume (Dreams of Love), S. 541, No. 1 in A-flat major, "Hohe
# Liebe" (Exalted Love). A from-memory piano arrangement: a slow song in the
# middle of the piano inside murmuring broken chords, swelling to a fervent
# climax and fading on a long A-flat chord, in Liszt's manner; the notes are
# approximate.
SEED = 1845

TRIAD = (0, 4, 7)
MINOR = (0, 3, 7)
SEVENTH = (0, 4, 10)


def murmur(root, quality):
    """Sixteen semiquavers: root, then the chord rocking above it."""
    r = pitch(root)
    t, f = r + 12 + quality[1], r + 12 + quality[2]
    return " ".join(f"{n}:1/4" for n in (r, f, t + 12, f) * 4) + " |"


SONG = (
    ("eb4:2 ab4:1 c5:1", "ab1", TRIAD),
    ("c5:3 bb4:1", "eb2", SEVENTH),
    ("bb4:2 db5:1 bb4:1", "eb2", SEVENTH),
    ("ab4:4", "ab1", TRIAD),
    ("ab4:2 c5:1 f5:1", "f1", MINOR),
    ("eb5:3 db5:1", "db2", TRIAD),
    ("c5:2 bb4:1 g4:1", "eb2", SEVENTH),
    ("ab4:4", "ab1", TRIAD),
)
FERVOUR = (
    ("c5:2 eb5:1 ab5:1", "ab1", TRIAD),
    ("ab5:3 g5:1", "c2", MINOR),
    ("f5:2 ab5:1 db6:1", "db2", TRIAD),
    ("c6:3 bb5:1", "ab1", TRIAD),
    ("ab5:2 g5:1 f5:1", "bb1", SEVENTH),
    ("eb5:3 c5:1", "eb2", SEVENTH),
    ("db5:2 c5:1 bb4:1", "eb2", SEVENTH),
    ("ab4:4", "ab1", TRIAD),
)


def play(piece, bars, dynamic, shift=0, **kwargs):
    piece.play((f"m4/4 !{dynamic} " + " ".join(f"{m} |" for m, _, _ in bars), shift),
               "m4/4 !pp " + " ".join(murmur(r, q) for _, r, q in bars), pedal="bar", **kwargs)


def picture(piece):
    play(piece, SONG, "p", bpm=56, label="song")
    play(piece, SONG, "mp", shift=12, bpm=58, label="song, higher")
    play(piece, FERVOUR, "f", bpm=62, to=56, label="fervour")
    piece.play("!mf " + run("ab6", "eb5", step="1/6") + " !>p", bpm=56, to=48, pedal=4, label="cadenza")
    play(piece, SONG, "p", bpm=52, to=46, label="song, last time")
    piece.play("m4/4 !pp eb4+ab4+c5:4~ | eb4+ab4+c5:4 |", "m4/4 !pp ab1+eb2+ab2:4~ | ab1+eb2+ab2:4 |",
               bpm=46, pedal=8)


def love():
    piece = Piece(SEED, reverb=80)
    picture(piece)
    return piece.render(tail=5.0)
