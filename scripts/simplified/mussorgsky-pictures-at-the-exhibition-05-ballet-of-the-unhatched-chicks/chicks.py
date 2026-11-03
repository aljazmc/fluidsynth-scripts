from piano import Piece, trill

# Mussorgsky, Pictures at an Exhibition, V. Ballet of the Unhatched Chicks
# (Балет невылупившихся птенцов), preceded by the fourth Promenade. A
# from-memory piano arrangement: keys, meter, tempo, the grace-note chirps
# and the trilling trio follow the original, the notes are approximate.
SEED = 1870

# Promenade IV: Tranquillo, D minor. The theme turned inward.
CHORUS = ("m5/4 e4+c4+a3:1 d4+a3+f3 g4+d4+bb3 a4+e4+c#4:1/2 d5+a4+f4 bb4+g4+d4:1 | "
          "m6/4 a4+f4+d4:1/2 d5+a4+f4 bb4+g4+d4:1 g4+eb4+bb3 a4+e4+c#4 e4+c#4+a3 d4+a3+f3 |")
BASS = ("m5/4 a2+a1:1 d2+d1 g2+g1 a2+a1 g2+g1 | "
        "m6/4 f2+f1:1 g2+g1 eb2+eb1 a2+a1 a1+a2 d2+d1 |")


def promenade(piece):
    piece.play("!p " + CHORUS, "!pp " + BASS, bpm=72, pedal=1, label="promenade")
    piece.play("!pp " + CHORUS, "!pp " + BASS, bpm=72, to=60, shift=-5, pedal=1)
    piece.play("m4/4 !pp a4+e4+c#4:4 | d4+a3+f3:4 |", "m4/4 !pp a2+a1:4 | d2+d1:4 |",
               bpm=60, to=50, pedal="bar", gap=1.0)
    # a first peep from the shells
    piece.play("m2/4 !pp a5:1/4 bb5 a5 bb5 a5:1 |", bpm=60, gap=0.6)


# Scherzino. Vivo leggiero. F major, 2/4. Each chirp is a grace note snapped
# onto a staccato chord.
def chirp(grace, chord):
    return f"{grace}:1/16 {chord}:3/16' r:1/4"


def bar(*chirps):
    return " ".join(chirp(*c) for c in chirps) + " |"


PECK = "m2/4 " + " ".join((
    bar(("g5", "f5+a5"), ("g5", "f5+a5"), ("bb5", "a5+c6"), ("g5", "f5+a5")),
    bar(("a5", "g5+bb5"), ("a5", "g5+bb5"), ("f5", "e5+g5"), ("f5", "e5+g5")),
    bar(("g5", "f5+a5"), ("bb5", "a5+c6"), ("d6", "c6+e6"), ("bb5", "a5+c6")),
    "a5+f5+c6:1/4' g5+e5+bb5:1/4' f5+a5:1/2' r:1 |",
))
HOP = ("m2/4 f3+a3:1/4' r:1/4 c4' r:1/4 f3+a3' r:1/4 c4' r:1/4 | "
       "e3+bb3' r:1/4 c4' r:1/4 e3+bb3' r:1/4 c4' r:1/4 | "
       "f3+a3' r:1/4 c4' r:1/4 f3+a3' r:1/4 c4' r:1/4 | "
       "c3+c4:1/2' c3+bb3' f3+a3:1/2' r:1/2 |")

# Trio, B-flat major: the right hand trills on, the left hand pecks below.
TRILL = "m2/4 " + " | ".join([trill("d6", "eb6", 2)] * 3 + [trill("c6", "d6", 2)]) + " |"
PECK_LOW = "m2/4 " + " ".join((
    bar(("c4", "bb3+d4"), ("c4", "bb3+d4"), ("g4", "f4+a4"), ("g4", "f4+a4")),
    bar(("c4", "bb3+d4"), ("c4", "bb3+d4"), ("bb4", "a4+c5"), ("g4", "f4+a4")),
    bar(("f4", "eb4+g4"), ("f4", "eb4+g4"), ("d4", "c4+eb4"), ("d4", "c4+eb4")),
    "d4+f4:1/4' c4+eb4' bb3+d4:1/2' r:1 |",
))


def picture(piece):
    for dynamic in ("p", "pp"):
        piece.play(f"!{dynamic} " + PECK, f"!{dynamic} " + HOP, bpm=138, label="chirps")
    for dynamic in ("p", "mp"):
        piece.play(f"!{dynamic} " + TRILL, f"!{dynamic} " + PECK_LOW, bpm=138, label="trio")
    for dynamic in ("p", "mp"):
        piece.play(f"!{dynamic} " + PECK, f"!{dynamic} " + HOP, bpm=138, label="da capo")
    # coda: two last hops and they are gone
    piece.play("m2/4 !mp " + bar(("g5", "f5+a5"), ("bb5", "a5+c6"), ("d6", "c6+f6"), ("g6", "f6+a6"))
               + " f5+a5+c6+f6:1/4' r:7/4 |",
               "m2/4 !p f3+a3:1/4' r:1/4 c4' r:1/4 f3+a3' r:1/4 c4' r:1/4 | f2+f3:1/4' r:7/4 |",
               bpm=138)


def chicks():
    piece = Piece(SEED)
    promenade(piece)
    picture(piece)
    return piece.render()
