from piano import Piece, pitch

# Liszt, Liebesträume (Dreams of Love), S. 541, No. 2 in E major, "Seliger
# Tod" (Blessed Death). A from-memory piano arrangement: a hushed, rapt song
# in E major over gently pulsing chords, a passionate outburst in the middle
# and a calm, transfigured close, in Liszt's manner; the notes are
# approximate.
SEED = 1846

TRIAD = (0, 4, 7)
MINOR = (0, 3, 7)
SEVENTH = (0, 4, 10)


def pulse(root, quality):
    """Bass on the beat, the chord repeated in quavers above (6/8: three beats)."""
    r = pitch(root)
    chord = "+".join(str(r + 12 + q) for q in quality)
    return f"{r}:1/2 {chord}:1/2 {chord}:1/2 {r + 7}:1/2 {chord}:1/2 {chord}:1/2 |"


HYMN = (
    ("b4:3/2 g#4:1/2 a4:1/2 b4:1/2", "e2", TRIAD),
    ("c#5:1 b4:1/2 a4:3/2", "a1", TRIAD),
    ("g#4:1 f#4:1/2 g#4:1 a4:1/2", "b1", SEVENTH),
    ("b4:3", "e2", TRIAD),
    ("e5:3/2 d#5:1/2 c#5:1/2 b4:1/2", "c#2", MINOR),
    ("a4:1 c#5:1/2 b4:3/2", "f#1", MINOR),
    ("g#4:1 a4:1/2 f#4:1 d#4:1/2", "b1", SEVENTH),
    ("e4:3", "e2", TRIAD),
)
OUTBURST = (
    ("g5:3/2 f#5:1/2 e5:1/2 d5:1/2", "c2", TRIAD),
    ("c5:1 e5:1/2 g5:3/2", "a1", MINOR),
    ("f#5:1 e5:1/2 d#5:1 c5:1/2", "b1", SEVENTH),
    ("b4:3", "e2", MINOR),
    ("a5:3/2 g5:1/2 f#5:1/2 e5:1/2", "c2", TRIAD),
    ("d#5:1 f#5:1/2 a5:3/2", "b1", SEVENTH),
    ("g#5:1 f#5:1/2 e5:1 d#5:1/2", "b1", SEVENTH),
    ("e5:3", "e2", TRIAD),
)


def play(piece, bars, dynamic, shift=0, **kwargs):
    piece.play((f"m6/8 !{dynamic} " + " ".join(f"{m} |" for m, _, _ in bars), shift),
               f"m6/8 !pp " + " ".join(pulse(r, q) for _, r, q in bars), pedal="bar", **kwargs)


def picture(piece):
    play(piece, HYMN, "p", bpm=84, label="hymn")
    play(piece, HYMN, "mp", shift=12, bpm=86, label="hymn, higher")
    play(piece, OUTBURST, "f", bpm=96, to=88, label="outburst")
    play(piece, HYMN, "pp", bpm=80, to=66, label="transfigured")
    piece.play("m6/8 !pp g#4+b4+e5:3~ | g#4+b4+e5:3 |", "m6/8 !ppp e1+b1+e2:3~ | e1+b1+e2:3 |",
               bpm=60, pedal=6)


def death():
    piece = Piece(SEED, reverb=80)
    picture(piece)
    return piece.render(tail=5.0)
