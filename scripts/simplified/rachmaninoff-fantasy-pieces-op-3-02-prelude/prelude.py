from piano import Piece, pitch

# Rachmaninoff, Morceaux de fantaisie (Fantasy Pieces), Op. 3 (1892), No. 2,
# Prelude in C-sharp minor. A from-memory piano arrangement: the three
# hammered octaves A, G-sharp, C-sharp, the quiet chorale built on them, the
# Agitato with its falling triplets, the return on four staves fff and the
# hushed coda follow Rachmaninoff, the chords are approximate.
SEED = 1892

BELL = "m4/4 a2+a3:1^ g#2+g#3:1^ c#2+c#3:2^ |"
BELL_LH = "m4/4 a1+a2:1^ g#1+g#2:1^ c#1+c#2:2^ |"

# Lento: a bass octave on the beat, chords answering on beats two to four
CHORALE = ("m4/4 r:1 c#4+e4+a4:1 c#4+e4+g#4:1 g#3+c#4+e4:1 | r:1 c#4+e4+a4:1 c#4+e4+g#4:1 g#3+c#4+e4:1 | "
           "r:1 b3+d4+g#4:1 b3+d4+f#4:1 f#3+b3+d4:1 | r:1 a3+c#4+f#4:1 a3+c#4+e4:1 e3+a3+c#4:1 | "
           "r:1 a3+d4+f#4:1 a3+d4+e4:1 f#3+a3+d4:1 | r:1 g#3+c#4+e4:1 g#3+b3+e4:1 e3+g#3+b3:1 | "
           "r:1 a3+c#4+f#4:1 g#3+b#3+f#4:1 g#3+b#3+d#4:1 | r:1 g#3+c#4+e4:3 |")
CHORALE_LH = ("m4/4 c#2+c#3:4 | b1+b2:4 | e2+e3:4 | f#1+f#2:4 | d2+d3:4 | e1+e2:4 | g#1+g#2:4 | c#2+c#3:4 |")


def falling(start):
    """A bar of triplet quavers sliding down in pairs from a starting pitch."""
    p = pitch(start)
    notes = []
    for beat in range(4):
        top = p - 2 * beat
        notes += [top, top - 1, top - 4]
    return " ".join(f"{n}:1/3" for n in notes) + " |"


AGITATO = "m4/4 " + " ".join(falling(s) for s in ("e5", "e5", "f#5", "f#5", "g#5", "a5", "b5", "c#6"))
AGITATO_LH = ("m4/4 c#3+e3:1 c#3+e3 c#3+f#3 c#3+e3 | c#3+e3:1 c#3+e3 c#3+f#3 c#3+e3 | "
              "d3+f#3:1 d3+f#3 d3+g#3 d3+f#3 | d3+f#3:1 d3+f#3 d3+g#3 d3+f#3 | "
              "e3+g#3:1 e3+a3 f#3+a3 f#3+b3 | f#3+a3:1 f#3+b3 g#3+b3 g#3+c#4 | "
              "g#3+b#3:1 g#3+b#3 g#3+d#4 g#3+d#4 | g#2+g#3:1 g#2+g#3 g#2+g#3 g#2+g#3 |")


def picture(piece):
    piece.play("!fff " + BELL, "!fff " + BELL_LH, bpm=50, pedal=4, gap=0.6, label="bell")
    piece.play("!pp " + CHORALE, "!pp " + CHORALE_LH, bpm=52, pedal="bar", label="chorale")
    piece.play("!p " + AGITATO + " !<ff", "!p " + AGITATO_LH + " !<ff", bpm=112, to=124, pedal=2,
               label="agitato")
    piece.play("!ff " + AGITATO + " !<fff", "!ff " + AGITATO_LH, bpm=124, to=96, pedal=2)
    piece.play("!fff " + BELL, "!fff " + BELL_LH, bpm=48, pedal=4, label="bell again")
    # the return: the chorale doubled into four staves, fff
    piece.play(("!fff " + CHORALE, 12), "!fff " + CHORALE, ("!fff " + CHORALE_LH, -12), "!ff " + CHORALE_LH,
               bpm=48, to=44, pedal="bar", label="four staves")
    # coda: the bell, softly, and the last chord
    piece.play("!pp " + BELL + " m4/4 r:1 g#3+c#4+e4:3 | r:1 g#3+c#4+e4+g#4:3 |",
               "!pp " + BELL_LH + " m4/4 c#2+c#3:4 | c#1+c#2:4 |", bpm=44, to=36, pedal="bar", label="coda")


def prelude():
    piece = Piece(SEED, reverb=80)
    picture(piece)
    return piece.render(tail=6.0)
