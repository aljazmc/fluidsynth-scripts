from piano import Piece, run, tremolo

# Mussorgsky, Pictures at an Exhibition, IX. The Hut on Hen's Legs, Baba Yaga
# (Избушка на курьих ножках. Баба-Яга). A from-memory piano arrangement:
# meter, tempi, the stamping octaves, the eerie Andante mosso and the run
# that leads straight into the Great Gate follow the original, the notes are
# approximate.
SEED = 1865

# Allegro con brio, feroce. 2/4. Octaves hurled across silence.
HURL = ("m2/4 c3+c2:1/2^ r:3/2 | r:2 | g2+g1:1/2^ r:3/2 | r:2 | "
        "c3+c2:1/2^ r:1/2 f#3+f#2:1/2^ r:1/2 | c3+c2:1/2^ r:1/2 f#3+f#2:1/2^ r:1/2 | "
        "c3+c2:1/2^ f#3+f#2^ c3+c2^ f#3+f#2^ | c3+c2:1^ r:1 |")

# the ride: staccato octaves in both hands, with the hut stamping below
RIDE = ("m2/4 c4+c3:1/2^' eb4+eb3' d4+d3' c4+c3' | g4+g3:1/2^' ab4+ab3' g4+g3' f#4+f#3' | "
        "g4+g3:1/2^' c5+c4' bb4+bb3' ab4+ab3' | g4+g3:1^ r:1 | "
        "ab4+ab3:1/2^' g4+g3' f4+f3' eb4+eb3' | d4+d3:1/2^' eb4+eb3' f4+f3' f#4+f#3' | "
        "g4+g3:1/2^' f#4+f#3' g4+g3' ab4+ab3' | g4+g3:1^ c4+c3:1^ |")
STAMP = "m2/4 " + " ".join(["c1+c2:1/2^ r:1/2 g1+g2:1/2 r:1/2 |"] * 3
                           + ["c1+c2:1/2^ r:3/2 |"]
                           + ["f1+f2:1/2^ r:1/2 c2:1/2 r:1/2 |", "g1+g2:1/2^ r:1/2 d2:1/2 r:1/2 |",
                              "g1+g2:1/2^ r:1/2 g1:1/2 r:1/2 |", "g1+g2:1^ c1+c2:1^ |"])

# Andante mosso: in the forest at night, a low tritone tremolo and a few
# creeping steps above it
CREEP = ("m2/4 r:2 | db4:1 c4:1 | r:2 | db4:1 c4:1 | r:2 | e4:1 eb4:1 | d4:2~ | d4:2 |")
MURMUR = "m2/4 " + " | ".join([tremolo("f#1+f#2", "c2+c3", 2)] * 8) + " |"


def picture(piece):
    piece.play("!fff " + HURL, bpm=150, pedal=None, label="hurl")
    for shift, dynamic in ((0, "ff"), (0, "f"), (5, "ff"), (0, "fff")):
        piece.play(f"!{dynamic} " + RIDE, f"!{dynamic} " + STAMP, bpm=150, shift=shift, label="ride")

    piece.rest(0.5)
    piece.play("!pp " + CREEP, "!pp " + MURMUR, bpm=80, pedal="bar", label="forest")
    piece.play("!p " + CREEP, "!p " + MURMUR + " !<f", bpm=80, shift=3, pedal="bar")
    piece.play("!pp " + CREEP + " !<mf", "!pp " + MURMUR + " !<ff", bpm=80, to=110, pedal="bar")

    # she comes back
    piece.play("!fff " + HURL, bpm=150)
    piece.play("!ff " + RIDE, "!ff " + STAMP, bpm=150)
    piece.play("!fff " + RIDE, "!fff " + STAMP, bpm=150, to=168)

    # up and up, straight into the gate: the run lands on the B-flat octaves
    piece.play("!f " + run("c3", "bb5", octave=True, marks="'") + " !<fff", bpm=168, label="run")
    piece.play("m2/4 !fff bb4+bb3+bb2:2^ |", "m2/4 !fff bb1+bb0:2^ |", bpm=168, pedal=2)


def legs():
    piece = Piece(SEED)
    picture(piece)
    return piece.render()
