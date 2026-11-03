from piano import Piece

# Rachmaninoff, Morceaux de fantaisie (Fantasy Pieces), Op. 3, No. 3, Mélodie
# in E major. A from-memory piano arrangement: a long singing tune in the
# tenor, framed by soft repeated chords above and a slow bass below, rising to
# a warm climax and settling in E major, in Rachmaninoff's manner; the notes
# are approximate.
SEED = 1894

# Adagio sostenuto, 4/4. (tenor tune, repeated chord above, bass)
SONG = (
    ("g#3:2 a3:1 b3:1", "g#4+b4+e5", "e2"),
    ("c#4:3 b3:1", "a4+c#5+e5", "a1"),
    ("a3:2 g#3:1 f#3:1", "a4+b4+d#5", "b1"),
    ("g#3:4", "g#4+b4+e5", "e2"),
    ("b3:2 c#4:1 d#4:1", "g#4+b4+e5", "g#1"),
    ("e4:3 d#4:1", "a4+c#5+e5", "c#2"),
    ("c#4:2 b3:1 a3:1", "f#4+a4+d#5", "f#1"),
    ("b3:4", "f#4+a4+d#5", "b1"),
)
CLIMAX = (
    ("e4:2 f#4:1 g#4:1", "g#4+b4+e5", "c#2"),
    ("a4:3 g#4:1", "a4+c#5+f#5", "f#1"),
    ("f#4:2 e4:1 d#4:1", "a4+b4+d#5", "b1"),
    ("e4:4", "g#4+b4+e5", "e2"),
    ("c#4:2 d#4:1 e4:1", "a4+c#5+e5", "a1"),
    ("f#4:3 e4:1", "a4+b4+d#5", "b1"),
    ("d#4:2 c#4:1 b3:1", "a4+b4+d#5", "b1"),
    ("e4:4", "g#4+b4+e5", "e2"),
)


def play(piece, bars, dynamic, **kwargs):
    piece.play(f"m4/4 !{dynamic} " + " ".join(f"{t} |" for t, _, _ in bars),
               "m4/4 !pp " + " ".join(f"{c}:1/2 {c} {c} {c} {c} {c} {c} {c} |" for _, c, _ in bars),
               "m4/4 !p " + " ".join(f"{b}+{b[:-1]}{int(b[-1]) + 1}:4 |" for _, _, b in bars),
               pedal="bar", **kwargs)


def picture(piece):
    play(piece, SONG, "mp", bpm=54, label="song")
    play(piece, SONG[:4] + CLIMAX[:4], "mf", bpm=56, label="rising")
    play(piece, CLIMAX, "f", bpm=58, to=52, label="climax")
    play(piece, SONG, "p", bpm=52, to=44, label="settling")
    piece.play("m4/4 !pp e3+g#3+b3+e4:4~ | e3+g#3+b3+e4:4 |", "m4/4 !pp e1+e2:4~ | e1+e2:4 |", bpm=44, pedal=8)


def melody():
    piece = Piece(SEED, reverb=80)
    picture(piece)
    return piece.render(tail=5.0)
