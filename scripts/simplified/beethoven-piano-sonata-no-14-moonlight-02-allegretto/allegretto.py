from piano import Piece

# Beethoven, Piano Sonata No. 14 "Moonlight", II. Allegretto. A from-memory
# piano arrangement: the D-flat major minuet in 3/4, its trio with the
# off-beat sforzando chords over a held bass, and the minuet da capo follow
# Beethoven, the notes are approximate.
SEED = 1802

MINUET_A = ("m3/4 f4+ab4:2 db4+f4:1 | c4+eb4:2 bb3+db4:1 | ab3+c4:1 bb3+db4:1 c4+eb4:1 | db4+f4:2 r:1 | "
            "f4+ab4:2 db4+f4:1 | eb4+gb4:2 c4+eb4:1 | db4+f4:1 c4+eb4:1 ab3+c4:1 | ab3+db4:2 r:1 |")
MINUET_A_LH = ("m3/4 db3:1' f3+ab3' f3+ab3' | ab2' eb3+gb3' eb3+gb3' | ab2' eb3+gb3' eb3+gb3' | "
               "db3' f3+ab3' f3+ab3' | db3' f3+ab3' f3+ab3' | ab2' eb3+gb3' eb3+gb3' | "
               "db3' f3+ab3' ab2' | db3' ab2' db2' |")
MINUET_B = ("m3/4 eb4+ab4:2 c4+eb4:1 | db4+f4:2 bb3+db4:1 | c4+eb4:1 db4+f4:1 eb4+g4:1 | ab4+c5:2 r:1 | "
            "c5+eb5:2 ab4+c5:1 | bb4+db5:2 g4+bb4:1 | ab4+c5:1 g4+bb4:1 eb4+g4:1 | eb4+ab4:2 r:1 |")
MINUET_B_LH = ("m3/4 ab2:1' eb3+c4' eb3+c4' | bb2' db3+f3' db3+f3' | eb3' g3+db4' g3+db4' | ab2' eb3+c4' eb3+c4' | "
               "ab2' eb3+c4' eb3+c4' | eb2' g3+db4' g3+db4' | eb3' g3+db4' eb2' | ab2' eb2' ab1' |")

# Trio: chords struck on the second beat and held over, a D-flat drone below
TRIO_HARMONY = ("db4+f4+ab4", "db4+f4+ab4", "c4+eb4+gb4+ab4", "c4+eb4+gb4+ab4",
                "c4+eb4+gb4+ab4", "c4+eb4+gb4+ab4", "db4+f4+ab4", "db4+f4+ab4")
TRIO = "m3/4 " + " ".join(f"r:1 {c}:2^ |" for c in TRIO_HARMONY)
TRIO_LH = "m3/4 " + " ".join(["db2+db3:3 |"] * 4 + ["ab1+ab2:3 |"] * 2 + ["db2+db3:3 |"] * 2)


def minuet(piece, dynamic):
    piece.play(f"!{dynamic} " + MINUET_A, f"!{dynamic} " + MINUET_A_LH, bpm=150, label="minuet")
    piece.play(f"!{dynamic} " + MINUET_B, f"!{dynamic} " + MINUET_B_LH, bpm=150)
    piece.play(f"!{dynamic} " + MINUET_A, f"!{dynamic} " + MINUET_A_LH, bpm=150, to=138)


def picture(piece):
    minuet(piece, "p")
    for dynamic in ("f", "p", "f"):
        piece.play(f"!{dynamic} " + TRIO, f"!{dynamic} " + TRIO_LH, bpm=146, pedal="bar", label="trio")
    minuet(piece, "p")
    piece.play("m3/4 !p ab3+db4+f4:2 r:1 | db3+ab3+db4+f4:3 |", "m3/4 !p db2:2 r:1 | db1+db2:3 |",
               bpm=138, to=120, pedal=3)


def allegretto():
    piece = Piece(SEED)
    picture(piece)
    return piece.render()
