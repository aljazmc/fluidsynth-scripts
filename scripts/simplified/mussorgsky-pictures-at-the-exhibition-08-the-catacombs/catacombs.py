from piano import Piece, tremolo

# Mussorgsky, Pictures at an Exhibition, VIII. The Catacombs, a Roman Tomb
# (Catacombae. Sepulcrum romanum) and With the Dead in a Dead Language (Cum
# mortuis in lingua mortua). A from-memory piano arrangement: key, tempi, the
# alternating ff/pp chords with their fermatas and the Promenade in B minor
# under a high tremolo follow the original, the chords are approximate.
SEED = 1866

# Catacombae. Largo, B minor, 3/4. Single chords held into the dark, loud and
# soft by turns. (right hand, left hand, dynamic, fermata seconds)
VAULT = (
    ("b3+b4", "b1+b2", "ff", 1.6),
    ("d4+f#4+b4", "b2", "p", 1.0),
    ("d4+g4+b4", "g1+g2", "ff", 1.4),
    ("c#4+e4+g4+a#4", "a#1+a#2", "p", 1.0),
    ("c#4+f#4+a#4", "f#1+f#2", "ff", 1.8),
    ("d4+f#4+b4", "b1+b2", "pp", 1.2),
    ("c4+e4+g4+c5", "c2+c3", "ff", 1.6),
    ("c#4+e4+a#4", "f#1+f#2", "p", 1.2),
    ("d4+g4+b4", "e1+e2", "ff", 1.4),
    ("c#4+e#4+g#4+b4", "c#2+c#3", "pp", 1.0),
    ("c#4+f#4+a#4", "f#1+f#2", "f", 1.6),
    ("b3+d4+f#4+b4", "b1+b2+f#2", "ppp", 2.5),
)

# Cum mortuis in lingua mortua. Andante non troppo, con lamento. The
# Promenade, in B minor, in the middle of the piano; above it an F-sharp
# tremolo that never stops.
CHORUS = ("m5/4 g4+d4+b3:1 f#4+d4+b3 b4+f#4+d4 c#5+a#4+f#4:1/2 f#5+c#5+a#4 d5+b4+f#4:1 | "
          "m6/4 c#5+a#4+f#4:1/2 f#5+c#5+a#4 d5+b4+f#4:1 b4+f#4+d4 c#5+g4+e4 g4+e4+b3 f#4+d4+b3 |")
BASS = ("m5/4 e2+e3:1 b1+b2 b1+b2 f#1+f#2 b1+b2 | "
        "m6/4 f#1+f#2:1 b1+b2 d2+d3 a#1+a#2 e2+e3 b1+b2 |")
SHIMMER = ("m5/4 " + tremolo("f#5", "f#6", 5) + " | m6/4 " + tremolo("f#5", "f#6", 6) + " |")


def picture(piece):
    for right, left, dynamic, fermata in VAULT:
        # the fermata holds the chord on, then a short breath before the next
        beats = 3 + round(fermata * 48 / 60 * 4) / 4
        piece.play(f"!{dynamic} {right}:{beats}", f"!{dynamic} {left}:{beats}",
                   bpm=48, pedal=beats, gap=0.25, label="catacombae")

    piece.rest(1.0)
    piece.play("!p " + CHORUS, "!p " + BASS, "!pp " + SHIMMER, bpm=60, pedal=1, label="cum mortuis")
    piece.play("!mp " + CHORUS, "!p " + BASS, "!p " + SHIMMER, bpm=60, shift=5, pedal=1)
    piece.play("!p " + CHORUS, "!pp " + BASS, "!pp " + SHIMMER, bpm=60, to=52, pedal=1)

    # the dead answer in B major
    piece.play("m4/4 !pp b3+d#4+f#4+b4:4~ | b3+d#4+f#4+b4:4 |",
               "m4/4 !ppp b1+b2:4~ | b1+b2:4 |",
               "m4/4 !pp " + tremolo("f#5", "f#6", 4) + " | " + tremolo("f#5", "f#6", 4) + " !>ppp |",
               bpm=52, to=44, pedal=8)


def catacombs():
    piece = Piece(SEED)
    picture(piece)
    return piece.render(tail=6.0)
