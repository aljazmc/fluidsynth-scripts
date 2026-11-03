from piano import Piece

# Mussorgsky, Pictures at an Exhibition, III. Children Quarrelling at Play in
# the Tuileries (Tuileries. Dispute d'enfants après jeux), preceded by the
# third Promenade. A from-memory piano arrangement: key, meter, tempo and the
# teasing figure follow the original, the notes are approximate.
SEED = 1839

# Promenade III: Moderato non tanto, pesamente. B major.
CHORUS = ("m5/4 g4+eb4+bb3:1 f4+d4+bb3 bb4+g4+d4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 | "
          "m6/4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 bb4+f4+d4 c5+g4+eb4 g4+eb4+bb3 f4+d4+bb3 |")
BASS = ("m5/4 eb3+eb2:1 bb2+bb1 g2+g1 f2+f1 bb2+bb1 | "
        "m6/4 f2+f1:1 bb2+bb1 d3+d2 c3+c2 eb3+eb2 bb2+bb1 |")


def promenade(piece):
    piece.play("!mf " + CHORUS, "!mf " + BASS, bpm=88, shift=1, pedal=1, label="promenade")
    piece.play("!f " + CHORUS, "!f " + BASS, bpm=88, to=70, shift=1, pedal=1)
    piece.play("m4/4 !mf b4+f#4+d#4+b3:4 |", "m4/4 !mf b2+b1:4 |", bpm=70, pedal=4, gap=0.8)


# Allegretto non troppo, capriccioso. B major, 4/4. "Nyah-nyah" thirds, a
# quick twist of sixteenths, and a light, staccato left hand.
TEASE = ("m4/4 f#5:1/2 d#5 f#5 d#5 e5:1/4 f#5 e5 d#5 c#5:1/2 b4 | "
         "d#5:1/2 c#5 d#5 c#5 b4:1/4 c#5 b4 a#4 g#4:1/2 f#4 | "
         "f#5:1/2 d#5 f#5 d#5 g#5:1/4 a#5 g#5 f#5 e5:1/2 d#5 | "
         "c#5:1/2 e5 d#5 c#5 b4:2 |")
SKIP = ("m4/4 b2:1/2' d#3+f#3' b2' d#3+f#3' f#2' e3+a#3' b2' d#3+f#3' | "
        "g#2' d#3+b3' g#2' d#3+b3' c#3' e3+a#3' f#2' e3+a#3' | "
        "b2' d#3+f#3' b2' d#3+f#3' e2' g#3+b3' e2' g#3+b3' | "
        "f#2' e3+a#3' f#2' e3+a#3' b2:1' b1+b2:1' |")

# a sulking, cantabile middle in E major and G-sharp minor
SULK = ("m4/4 b4:1 c#5:1/2 b4:1/2 g#4:2 | a#4:1 b4:1/2 a#4:1/2 f#4:2 | "
        "g#4:1 a#4:1/2 b4:1/2 c#5:1 d#5:1 | c#5:2 b4:1 a#4:1 |")
SULK_BASS = ("m4/4 e2+b2+e3:4 | f#2+c#3+a#3:4 | e2+b2+g#3:2 c#2+g#2+e3:2 | f#2+c#3+a#3:4 |")
SULK_ALTO = ("m4/4 g#4:2 e4:2 | f#4:2 c#4:2 | e4:2 g#4:2 | e4:2 d#4:1 c#4:1 |")


def picture(piece):
    piece.play("!mf " + TEASE, "!mp " + SKIP, bpm=126, label="tease")
    piece.play("!p " + TEASE, "!p " + SKIP, bpm=126)
    piece.play("!p " + SULK, "!pp " + SULK_ALTO, "!pp " + SULK_BASS, bpm=104, pedal="bar",
               label="sulk")
    piece.play("!mp " + SULK, "!p " + SULK_ALTO, "!p " + SULK_BASS, bpm=104, to=92, shift=-4,
               pedal="bar")
    piece.play("!mf " + TEASE, "!mp " + SKIP, bpm=126, label="tease again")
    piece.play("!f " + TEASE, "!mf " + SKIP, bpm=126, to=112)
    # the children run off laughing
    piece.play("m4/4 !mf b4:1/4 d#5 f#5 b5:1/4' r:1 b4+d#5+f#5+b5:1' r:1 |",
               "m4/4 !mf r:2 b1+b2:1' r:1 |", bpm=112)


def tuileries():
    piece = Piece(SEED)
    promenade(piece)
    picture(piece)
    return piece.render()
