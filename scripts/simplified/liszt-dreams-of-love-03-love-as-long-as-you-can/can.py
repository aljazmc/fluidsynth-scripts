from piano import Piece, pitch, run

# Liszt, Liebesträume (Dreams of Love), S. 541 (1850), No. 3 in A-flat major,
# "O lieb, so lang du lieben kannst" (Love as long as you can). A from-memory
# piano arrangement: the 6/4 nocturne with its tenor melody inside rippling
# arpeggios, the two cadenzas, the impassioned climax and the return high in
# the right hand follow Liszt, the notes are approximate.
SEED = 1850

TRIAD = (0, 4, 7, 12)
MINOR = (0, 3, 7, 12)
SEVENTH = (0, 4, 7, 10)


def ripple(root, quality):
    """Twelve quavers rising and falling through the chord from a low root."""
    r, t, f, x = (pitch(root) + q for q in quality)
    notes = (r, f, r + 12, t + 12, f + 12, x + 12, f + 12, t + 12, r + 12, f, t + 12, f + 12)
    return " ".join(f"{n}:1/2" for n in notes) + " |"


# (melody bar, root of the harmony, quality)
THEME = (
    ("c5:3 c5:1 bb4:1 ab4:1", "ab1", TRIAD),
    ("eb5:4 db5:1 c5:1", "eb2", SEVENTH),
    ("c5:3 bb4:1 ab4:1 g4:1", "eb2", SEVENTH),
    ("ab4:4 r:2", "ab1", TRIAD),
    ("c5:3 c5:1 db5:1 eb5:1", "ab1", TRIAD),
    ("f5:4 eb5:1 db5:1", "db2", TRIAD),
    ("c5:2 bb4:1 ab4:2 g4:1", "eb2", SEVENTH),
    ("ab4:6", "ab1", TRIAD),
)
# the climb to the climax, through F minor and C-flat major
CLIMB = (
    ("ab4:3 c5:1 f5:1 ab5:1", "f1", MINOR),
    ("g5:4 f5:1 eb5:1", "c2", SEVENTH),
    ("eb5:3 gb5:1 bb5:1 cb6:1", "cb2", TRIAD),
    ("bb5:4 ab5:1 gb5:1", "gb1", SEVENTH),
    ("gb5:3 eb5:1 db5:1 cb5:1", "cb2", TRIAD),
    ("bb4:4 c5:1 db5:1", "bb1", SEVENTH),
    ("eb5:3 db5:1 c5:1 bb4:1", "eb2", SEVENTH),
    ("ab4:6", "ab1", TRIAD),
)


def section(bars, dynamic, shift=0):
    melody = f"m6/4 !{dynamic} " + " ".join(f"{m} |" for m, _, _ in bars)
    waves = f"m6/4 !{'p' if dynamic in ('p', 'mp') else 'mp'} " + " ".join(ripple(r, q) for _, r, q in bars)
    return (melody, shift), waves


def picture(piece):
    piece.play(*section(THEME, "p"), bpm=78, pedal="bar", label="theme")
    piece.play("!mp " + run("eb6", "c5", step="1/6") + " " + run("c5", "ab4", step="1/4") + " !>p",
               bpm=78, to=60, pedal=8, label="first cadenza")
    piece.play(*section(THEME, "mf", 0), bpm=80, pedal="bar", label="theme again")
    piece.play(*section(CLIMB, "f"), bpm=84, to=76, pedal="bar", label="climb")
    piece.play("!ff " + run("cb7", "bb4", step="1/8") + " !>mp", bpm=76, to=56, pedal=8, label="second cadenza")
    melody, waves = section(THEME, "mf")
    piece.play((melody[0], 12), waves, bpm=74, pedal="bar", label="return, high")
    # coda: the last phrase, dying away
    piece.play("m6/4 !p c5:3 bb4:1 ab4:1 g4:1 | ab4:6 | r:6 | ab4+c5+eb5+ab5:6 |",
               "m6/4 !pp " + ripple("eb2", SEVENTH) + " " + ripple("ab1", TRIAD) + " "
               + ripple("db2", TRIAD) + " ab1+eb2+ab2:6 |",
               bpm=70, to=50, pedal="bar", label="coda")


def can():
    piece = Piece(SEED, reverb=80)
    picture(piece)
    return piece.render(tail=5.0)
