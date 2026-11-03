from piano import Piece

# Mussorgsky, Pictures at an Exhibition, X. The Bogatyr Gate (in the ancient
# capital, Kyiv), better known as The Great Gate of Kiev. A from-memory piano
# arrangement: key, meter, the hymn in great chords, the soft chorale, the
# bells with the Promenade above them and the grandioso close follow the
# original, the notes are approximate.
SEED = 1874

# Allegro alla breve. Maestoso. Con grandezza. E-flat major.
HYMN = ("m4/4 eb5+bb4+g4+eb4:2 f5+d5+bb4+f4:2 | bb4+g4+d4+bb3:2 c5+ab4+eb4+c4:2 | "
        "f5+c5+ab4+f4:2 d5+bb4+f4+d4:2 | eb5+bb4+g4+eb4:4 | "
        "g5+eb5+bb4+g4:2 f5+d5+bb4+f4:2 | eb5+c5+ab4+eb4:2 c5+ab4+eb4+c4:2 | "
        "bb4+f4+d4+bb3:2 d5+bb4+f4+d4:2 | eb5+bb4+g4+eb4:4 |")
ROOTS = (("eb2+eb3", "bb1+bb2"), ("g1+g2", "ab1+ab2"), ("f1+f2", "bb1+bb2"), ("eb1+eb2", "eb1+eb2"),
         ("eb2+eb3", "d2+d3"), ("c2+c3", "ab1+ab2"), ("bb1+bb2", "bb1+bb2"), ("eb1+eb2", "eb1+eb2"))
PILLARS = "m4/4 " + " ".join(f"{a}:2 {b}:2 |" for a, b in ROOTS)
POUNDING = "m4/4 " + " ".join(f"{a}:1/2^ {a} {a} {a} {b}:1/2^ {b} {b} {b} |" for a, b in ROOTS)

# Senza espressione: a soft, plain chorale in E-flat minor, like monks singing
CHORALE = ("m4/4 eb4+bb3+gb3:2 eb4+bb3+gb3:1 db4+bb3+f3:1 | eb4+cb4+gb3:2 f4+db4+ab3:2 | "
           "gb4+eb4+bb3:1 f4+db4+bb3:1 eb4+cb4+gb3:1 db4+bb3+f3:1 | eb4+bb3+gb3:4 |")
CHORALE_BASS = ("m4/4 eb2+eb3:3 bb1+bb2:1 | cb2+cb3:2 db2+db3:2 | "
                "gb2:1 bb2:1 cb3:1 bb2:1 | eb2+bb2:4 |")

# the bells ring and the Promenade walks in above them
CHORUS = ("m5/4 g4+eb4+bb3:1 f4+d4+bb3 bb4+g4+d4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 | "
          "m6/4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 bb4+f4+d4 c5+g4+eb4 g4+eb4+bb3 f4+d4+bb3 |")
BELLS = ("m5/4 eb2+bb2:1 ab1+eb2 eb2+bb2 ab1+eb2 eb2+bb2 | "
         "m6/4 ab1+eb2:1 eb2+bb2 ab1+eb2 eb2+bb2 ab1+eb2 eb2+bb2 |")
CHIMES = ("m5/4 bb5+eb6:1/2' r:1/2 g5+c6:1/2' r:1/2 bb5+eb6:1/2' r:1/2 g5+c6:1/2' r:1/2 bb5+eb6:1/2' r:1/2 | "
          "m6/4 g5+c6:1/2' r:1/2 bb5+eb6:1/2' r:1/2 g5+c6:1/2' r:1/2 "
          "bb5+eb6:1/2' r:1/2 g5+c6:1/2' r:1/2 bb5+eb6:1/2' r:1/2 |")


def picture(piece):
    piece.play("!ff " + HYMN, "!ff " + PILLARS, bpm=104, pedal=2, label="hymn")
    piece.rest(0.4)
    piece.play("!pp " + CHORALE, "!pp " + CHORALE_BASS, bpm=88, pedal="bar", label="chorale")
    piece.play("!ff " + HYMN, "!ff " + POUNDING, ("!f " + PILLARS, -12), bpm=104, pedal=2,
               label="hymn, pounding")
    piece.rest(0.4)
    piece.play("!pp " + CHORALE, "!pp " + CHORALE_BASS, bpm=88, shift=5, pedal="bar")

    # the bells, growing; the Promenade sings through them in E-flat
    for dynamic in ("mp", "mf", "f"):
        piece.play(f"!{dynamic} " + CHORUS, f"!{dynamic} " + BELLS, f"!{dynamic} " + CHIMES,
                   bpm=96, shift=5, pedal=1, label="bells")
    piece.play("!f " + CHORUS + " !<ff", "!f " + BELLS + " !<ff", "!f " + CHIMES,
               bpm=96, to=84, shift=5, pedal=1)

    # Meno mosso, sempre maestoso: the hymn in full, then the last chords
    piece.play("!ff " + HYMN, ("!ff " + HYMN, 12), "!ff " + POUNDING, ("!ff " + PILLARS, -12),
               bpm=84, pedal=2, label="grandioso")
    piece.play("!fff " + HYMN, ("!fff " + HYMN, 12), "!fff " + POUNDING, ("!fff " + PILLARS, -12),
               bpm=84, to=60, pedal=2)
    piece.play("m4/4 !fff eb5+bb4+g4+eb4:4~ | eb5+bb4+g4+eb4:4 |",
               "m4/4 !fff eb6+bb5+g5+eb5:4~ | eb6+bb5+g5+eb5:4 |",
               "m4/4 !fff eb2+eb3:1 eb2+eb3 bb1+bb2 bb1+bb2 | eb1+eb2:4 |",
               bpm=60, to=48, pedal=8)


def kyiv():
    piece = Piece(SEED)
    picture(piece)
    return piece.render(tail=6.0)
