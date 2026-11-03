from piano import Piece, run

# Rachmaninoff, Morceaux de fantaisie (Fantasy Pieces), Op. 3, No. 4,
# Polichinelle (Punchinello) in F-sharp minor. A from-memory piano
# arrangement: the jester's leaping chords flung across the keyboard, the
# fast glittering main section, a wistful middle and the furious return, in
# Rachmaninoff's manner; the notes are approximate.
SEED = 1895

# Allegro vivace, 4/4
LEAPS = ("m4/4 f#2+f#3:1/2^ r:1/2 c#5+f#5+a5:1/2^ r:1/2 f#2+f#3:1/2^ r:1/2 a5+c#6+f#6:1/2^ r:1/2 | "
         "e#2+e#3:1/2^ r:1/2 c#5+e#5+g#5:1/2^ r:1/2 c#2+c#3:1/2^ r:1/2 g#5+c#6+e#6:1/2^ r:1/2 |")
JIG = ("m4/4 f#5:1/4 a5 c#6 a5 g#5 b5 d6 b5 a5 c#6 f#6 c#6 e#5 g#5 c#6 g#5 | "
       "f#5:1/4 a5 c#6 a5 b5 d6 f#6 d6 c#6 e6 g6 e6 c#6 a5 f#5 c#5 | "
       "d5:1/4 f#5 b5 f#5 c#5 e#5 g#5 e#5 b4 d5 f#5 d5 a4 c#5 f#5 c#5 | "
       "g#4:1/4 b4 e#5 b4 c#5 e#5 g#5 c#6 f#5:1/2' r:3/2 |")
JIG_LH = ("m4/4 f#2:1/2' c#3+a3' f#2' c#3+a3' f#2' c#3+b3' f#2' c#3+a3' | "
          "f#2' c#3+a3' b1' d3+f#3' a1' c#3+e3' a1' c#3+f#3' | "
          "b1' d3+f#3' c#2' e#3+g#3' d2' f#3+b3' f#2' c#3+a3' | "
          "c#2' g#2+e#3' c#2' g#2+e#3' f#1+f#2:1' r:1 |")

# a wistful, singing middle in D major
WISTFUL = ("m4/4 f#4:2 e4:1 d4:1 | a4:3 g4:1 | f#4:2 e4:1 c#4:1 | d4:4 | "
           "b4:2 a4:1 g4:1 | f#4:3 e4:1 | d4:2 c#4:1 e4:1 | d4:4 |")
WISTFUL_LH = ("m4/4 d2:1/2 a2 d3 f#3 a3 f#3 d3 a2 | d2:1/2 a2 d3 f#3 a3 f#3 d3 a2 | "
              "a1:1/2 e2 a2 c#3 e3 c#3 a2 e2 | d2:1/2 a2 d3 f#3 a3 f#3 d3 a2 | "
              "g1:1/2 d2 g2 b2 d3 b2 g2 d2 | d2:1/2 a2 d3 f#3 a3 f#3 d3 a2 | "
              "a1:1/2 e2 a2 c#3 e3 c#3 a2 e2 | d2:1/2 a2 d3 f#3 a3 f#3 d3 a2 |")


def picture(piece):
    piece.play("!ff " + LEAPS + " " + LEAPS[5:], bpm=152, pedal=1, label="leaps")
    piece.play("!mf " + JIG, "!mf " + JIG_LH, bpm=152, label="jig")
    piece.play("!f " + JIG, "!f " + JIG_LH, bpm=152)
    piece.play("!ff " + LEAPS, bpm=152, pedal=1, gap=0.4)
    piece.play("!p " + WISTFUL, "!pp " + WISTFUL_LH, bpm=80, pedal=2, label="wistful")
    piece.play("!mp " + WISTFUL, "!p " + WISTFUL_LH, bpm=80, to=72, shift=12, pedal=2)
    piece.play("!ff " + LEAPS + " " + LEAPS[5:], bpm=152, pedal=1, label="return")
    piece.play("!f " + JIG, "!f " + JIG_LH, bpm=152)
    piece.play("!ff " + JIG + " !<fff", "!ff " + JIG_LH, bpm=152, to=168)
    piece.play("!fff " + run("f#6", "f#3", step="1/8", octave=True)
               + " f#2+c#3+f#3+a3+c#4+f#4:2^", bpm=168, pedal=4, label="end")


def punchinello():
    piece = Piece(SEED)
    picture(piece)
    return piece.render()
