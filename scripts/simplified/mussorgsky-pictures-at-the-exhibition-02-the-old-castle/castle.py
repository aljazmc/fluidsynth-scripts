from piano import Piece

# Mussorgsky, Pictures at an Exhibition, II. The Old Castle (Il vecchio
# castello), preceded by the second Promenade. A from-memory piano
# arrangement: key, meter, the drone and the troubadour's siciliano follow
# the original, the notes are approximate.
SEED = 1881

# Promenade II: Moderato comodo assai e con delicatezza, A-flat major. It turns
# towards E-flat, which becomes D-sharp, the dominant of the castle's G-sharp
# minor.
CHORUS = ("m5/4 g4+eb4+bb3:1 f4+d4+bb3 bb4+g4+d4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 | "
          "m6/4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 bb4+f4+d4 c5+g4+eb4 g4+eb4+bb3 f4+d4+bb3 |")
BASS = ("m5/4 eb3:1 bb2 g2 f2 bb2 | "
        "m6/4 f2:1 bb2 d3 c3 eb3 bb2 |")


def promenade(piece):
    piece.play("!p " + CHORUS, "!p " + BASS, bpm=84, shift=-2, pedal=1, label="promenade")
    piece.play("!mp " + CHORUS, "!mp " + BASS, bpm=84, shift=-2 + 5, pedal=1)
    piece.play("m4/4 !p g4+bb4+db5:2 g4+bb4+eb5:2 | !pp g4+bb4+db5+eb5:4 |",
               "m4/4 !p eb3+eb2:4~ | eb3+eb2:4 |", bpm=84, to=60, pedal="bar", gap=1.0)


# Andantino molto cantabile e con dolore, G-sharp minor, 6/8 (three quarter
# beats a bar). The left hand never leaves its G-sharp.
DRONE = "m6/8 " + " ".join(["g#1+g#2+d#3:3/2 g#2+d#3:1 g#2+d#3:1/2 |"] * 8)

SONG = ("m6/8 g#4:3/2 a#4:3/4 b4:1/4 a#4:1/2 | g#4:1 f#4:1/2 g#4:3/2 | "
        "b4:1 c#5:1/2 d#5:1 c#5:1/2 | b4:1 a#4:1/2 b4:3/2 | "
        "d#5:1 e5:1/2 d#5:1 c#5:1/2 | b4:1 c#5:1/2 a#4:3/2 | "
        "g#4:1 a#4:1/2 b4:1 a#4:1/2 | g#4:3 |")

ANSWER = ("m6/8 d#5:3/2 e5:3/4 d#5:1/4 c#5:1/2 | b4:1 c#5:1/2 d#5:3/2 | "
          "f#5:1 e5:1/2 d#5:1 c#5:1/2 | d#5:1 c#5:1/2 b4:3/2 | "
          "c#5:1 d#5:1/2 e5:1 d#5:1/2 | c#5:1 b4:1/2 a#4:3/2 | "
          "b4:1 a#4:1/2 g#4:1 f##4:1/2 | g#4:3 |")

# a second, inner voice that keeps the harmony moving over the drone
ALTO = ("m6/8 b3+d#4:3 | a#3+c#4:3 | g#3+e4:3 | d#4+f#4:3 | "
        "g#4:3 | d#4+f#4:3 | c#4+e4:3 | b3+d#4:3 |")
ALTO_ANSWER = ("m6/8 f#4+a#4:3 | g#4:3 | a#4:3/2 g#4:3/2 | f#4+a#4:3 | "
               "e4+g#4:3 | e4+f#4:3/2 d#4+f#4:3/2 | d#4:3/2 c#4:3/2 | b3+d#4:3 |")


def picture(piece):
    piece.play("m6/8 !pp " + " ".join(["g#1+g#2+d#3:3/2 g#2+d#3:1 g#2+d#3:1/2 |"] * 2),
               bpm=66, pedal="bar", label="drone alone")
    piece.play("!p " + SONG, "!pp " + ALTO, "!pp " + DRONE, bpm=66, pedal="bar", label="song")
    piece.play("!mp " + ANSWER, "!p " + ALTO_ANSWER, "!pp " + DRONE, bpm=66, pedal="bar")
    # the song moves to D-sharp minor, drone and all, then comes home
    piece.play(("!mf " + SONG, 7), ("!p " + ALTO, 7), ("!p " + DRONE, 7), bpm=66, pedal="bar")
    piece.play("!p " + SONG, "!pp " + ALTO, "!pp " + DRONE, bpm=66, pedal="bar")
    piece.play("!pp " + ANSWER, "!pp " + ALTO_ANSWER, "!ppp " + DRONE, bpm=66, to=56, pedal="bar")

    # coda: the troubadour's last phrase, fading over the drone
    piece.play("m6/8 !pp g#4:3/2 a#4:3/4 b4:1/4 a#4:1/2 | g#4:3 | r:3 | g#4+b4+d#5:3 |",
               "m6/8 !ppp " + " ".join(["g#1+g#2+d#3:3/2 g#2+d#3:1 g#2+d#3:1/2 |"] * 3)
               + " g#1+g#2+d#3:3 |",
               bpm=56, to=44, pedal="bar")


def castle():
    piece = Piece(SEED)
    promenade(piece)
    picture(piece)
    return piece.render(tail=5.0)
