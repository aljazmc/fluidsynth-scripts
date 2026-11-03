from piano import Piece

# Mussorgsky, Pictures at an Exhibition, IV. Cattle (Bydło), a Polish ox
# cart. A from-memory piano arrangement: key, meter, the relentless left hand
# and the piano original's ff start dying away to ppp follow Mussorgsky, the
# tune is approximate.
SEED = 1873

# Sempre moderato, pesante. G-sharp minor, 2/4.
TUNE = ("m2/4 g#4:1 a#4:1/2 b4:1/2 | c#5:1 d#5:1 | c#5:1/2 b4 a#4 b4 | c#5:2 | "
        "d#5:1 e5:1/2 d#5:1/2 | c#5:1 b4:1/2 a#4:1/2 | b4:1/2 a#4 g#4 a#4 | g#4:2 |")
THIRDS = ("m2/4 d#4:2 | e4:1 f#4:1 | e4:2 | e4+g#4:2 | "
          "g#4+b4:2 | e4+g#4:1 d#4+f#4:1 | d#4:2 | b3+d#4:2 |")

# one heavy chord per eighth, one harmony per bar
ROOTS = ("g#1+d#2+g#2", "e1+b1+e2", "e1+b1+e2", "c#2+g#2+c#3",
         "b1+f#2+b2", "f#1+c#2+f#2", "g#1+d#2+g#2", "g#1+d#2+g#2")


def wheels(roots=ROOTS):
    return "m2/4 " + " ".join(f"{c}:1/2^ {c} {c} {c} |" for c in roots)


def picture(piece):
    piece.play("!ff " + wheels(ROOTS[:2]), bpm=64, label="the cart")
    piece.play("!ff " + TUNE, "!f " + THIRDS, "!ff " + wheels(), bpm=64, pedal="bar", label="tune")
    piece.play("!ff " + TUNE, "!f " + THIRDS, ("!ff " + TUNE, -12), "!ff " + wheels(),
               bpm=64, pedal="bar")

    # the climb: the tune in D-sharp minor, thicker and louder
    piece.play(("!ff " + TUNE, 7), ("!ff " + THIRDS, 7), ("!ff " + TUNE, -5), ("!fff " + wheels(), 7),
               bpm=64, pedal="bar", label="climb")
    piece.play(("!ff " + TUNE, 0), ("!f " + THIRDS, 0), ("!ff " + TUNE, -12), "!ff " + wheels(),
               bpm=64, pedal="bar")

    # the cart rolls away
    piece.play("!f " + TUNE + " !>p", "!mf " + THIRDS + " !>pp", "!f " + wheels() + " !>p",
               bpm=64, to=60, pedal="bar", label="away")
    piece.play("m2/4 !p g#4:1 a#4:1/2 b4:1/2 | a#4:2 | g#4:2 | r:2 |",
               "!p " + wheels(ROOTS[:4]) + " !>pp", bpm=60, to=56)
    piece.play("!pp " + wheels(("g#1+d#2+g#2",) * 6) + " !>ppp",
               bpm=56, to=48)
    piece.play("m2/4 !ppp g#1+d#2+g#2:2 |", bpm=48, pedal=2)


def cattle():
    piece = Piece(SEED)
    picture(piece)
    return piece.render()
