from piano import Piece

# Beethoven, Piano Sonata No. 14 in C-sharp minor, Op. 27 No. 2, "Moonlight"
# (1801), I. Adagio sostenuto. A from-memory piano arrangement: the unbroken
# triplets, the octave bass, the dotted melody on G-sharp, the turn to E major
# and E minor, the long dominant pedal and the coda with the melody in the bass
# follow Beethoven, the harmonies are approximate.
SEED = 1801

# Si deve suonare tutto questo pezzo delicatissimamente e senza sordino.
CM = ("g#3", "c#4", "e4")
CM_B = ("g#3", "c#4", "e4")
A = ("a3", "c#4", "e4")
D = ("a3", "d4", "f#4")
FM = ("a3", "c#4", "f#4")
G7 = ("g#3", "c4", "f#4")
G7B = ("f#3", "c4", "d#4")
E = ("g#3", "b3", "e4")
B7 = ("f#3", "b3", "d#4")
EM = ("g3", "b3", "e4")
C = ("g3", "c4", "e4")
B7M = ("f#3", "a3", "d#4")

# (first half, second half, bass, melody) for each 4/4 bar
BARS = (
    (CM, CM, "c#2+c#3:4", "r:4"),
    (CM_B, CM_B, "b1+b2:4", "r:4"),
    (A, D, "a1+a2:2 f#1+f#2:2", "r:4"),
    (G7, G7B, "g#1+g#2:4", "r:4"),
    (CM, CM, "c#2+c#3:4", "r:3 g#4:3/4 g#4:1/4"),
    (CM, FM, "c#2+c#3:2 a1+a2:2", "g#4:3 g#4:3/4 g#4:1/4"),
    (FM, G7, "f#1+f#2:2 g#1+g#2:2", "a4:2 g#4:2"),
    (CM, CM, "c#2+c#3:4", "g#4:4"),
    (E, E, "e1+e2:4", "b4:3 b4:3/4 b4:1/4"),
    (E, B7, "e1+e2:2 b1+b2:2", "b4:3 b4:3/4 b4:1/4"),
    (FM, B7, "a1+a2:2 b1+b2:2", "c#5:2 b4:2"),
    (E, E, "e1+e2:4", "b4:4"),
    (EM, EM, "e1+e2:4", "b4:3 b4:3/4 b4:1/4"),
    (C, B7M, "c2+c3:2 b1+b2:2", "c5:2 b4:2"),
    (EM, EM, "g1+g2:4", "b4:4"),
    (B7M, B7, "b1+b2:4", "r:4"),
    # the long dominant pedal on G-sharp, the triplets rising and falling
    (G7, CM, "g#1+g#2:4", "r:4"),
    (("c4", "f#4", "g#4"), ("c#4", "e4", "g#4"), "g#1+g#2:4", "r:4"),
    (("f#4", "g#4", "c5"), ("e4", "g#4", "c#5"), "g#1+g#2:4", "r:4"),
    (G7, G7B, "g#1+g#2:4", "r:4"),
    # the melody returns
    (CM, CM, "c#2+c#3:4", "r:3 g#4:3/4 g#4:1/4"),
    (CM, FM, "c#2+c#3:2 a1+a2:2", "g#4:3 g#4:3/4 g#4:1/4"),
    (FM, G7, "f#1+f#2:2 g#1+g#2:2", "a4:2 g#4:2"),
    (CM, CM, "c#2+c#3:4", "g#4:4"),
)
# coda: the melody sinks into the bass
CODA = (
    (CM, CM, "c#2:3 g#1:3/4 g#1:1/4", "r:4"),
    (G7, G7, "g#1:3 g#1:3/4 g#1:1/4", "r:4"),
    (CM, CM, "c#2:3 g#1:3/4 g#1:1/4", "r:4"),
    (G7, CM, "g#1:2 c#2:2", "r:4"),
    (("c#3", "e3", "g#3"), ("c#3", "e3", "g#3"), "c#2+c#3:4", "r:4"),
)


def triplets(first, second):
    return " ".join(f"{n}:1/3" for chord in (first, first, second, second) for n in chord) + " |"


def play(piece, bars, dynamic, **kwargs):
    piece.play(f"m4/4 !{dynamic} " + " ".join(triplets(a, b) for a, b, _, _ in bars),
               f"m4/4 !{dynamic} " + " ".join(f"{bass} |" for _, _, bass, _ in bars),
               f"m4/4 !p " + " ".join(f"{tune} |" for _, _, _, tune in bars),
               pedal=2, **kwargs)


def picture(piece):
    play(piece, BARS[:16], "pp", bpm=54, label="melody")
    play(piece, BARS[16:20], "pp", bpm=54, label="pedal point")
    play(piece, BARS[20:], "pp", bpm=54, label="return")
    play(piece, CODA, "pp", bpm=52, to=44, label="coda")
    piece.play("m4/4 !pp c#2+c#3+g#3+c#4+e4:4~ | c#2+c#3+g#3+c#4+e4:4 |", bpm=44, pedal=8)


def sostenuto():
    piece = Piece(SEED, reverb=80)
    picture(piece)
    return piece.render(tail=5.0)
