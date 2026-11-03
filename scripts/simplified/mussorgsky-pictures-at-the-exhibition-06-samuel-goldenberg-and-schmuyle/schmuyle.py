from piano import Piece

# Mussorgsky, Pictures at an Exhibition, VI. Samuel Goldenberg and Schmuÿle
# ("Samuel" Goldenberg und "Schmuÿle"), two Jews, one rich, one poor. A
# from-memory piano arrangement: key, meter, tempo, the two characters and
# their final confrontation follow the original, the notes are approximate.
SEED = 1868

# Andante. Grave-energico. B-flat minor, 4/4. Goldenberg speaks in heavy
# octaves, in a scale with an augmented second (D-flat to E).
GOLDENBERG = ("m4/4 bb3:1 c4:1/3 db4 c4 bb3:1/2 c4:1/2 db4:1 | "
              "e4:3/4 f4:1/4 gb4:1/2 f4:1/2 e4:1/3 f4 e4 db4:1 | "
              "c4:1/2 db4:1/2 e4:1/4 db4 c4 bb3 c4:1 a3:1 | bb3:4 | "
              "f4:1 gb4:1/3 f4 e4 f4:1/2 gb4:1/2 a4:1 | "
              "bb4:3/4 a4:1/4 gb4:1/2 f4:1/2 e4:1/3 f4 e4 db4:1 | "
              "c4:1/2 db4:1/2 e4:1/4 db4 c4 bb3 c4:1 a3:1 | bb3:4 |")


# Andantino. Schmuÿle whines: high, fast repeated notes, one pitch per beat,
# each beat starting with a flick from the note above.
def whine(*pitches):
    beats = []
    for p in pitches:
        if p == "|":
            beats.append("|")
        else:
            upper, note = p.split("/")
            beats.append(f"{upper}:1/6 {note} {note} {note} {note} {note}")
    return "m4/4 " + " ".join(beats)


SCHMUYLE = whine("eb5/db5", "eb5/db5", "db5/c5", "eb5/db5", "|",
                 "f5/eb5", "eb5/db5", "db5/c5", "c5/bb4", "|",
                 "eb5/db5", "eb5/db5", "db5/c5", "eb5/db5", "|",
                 "gb5/f5", "f5/eb5", "eb5/db5", "db5/c5", "|")
SCHMUYLE_BASS = ("m4/4 bb2+f3+db4:2 gb2+db3+bb3:2 | f2+c3+a3:2 bb2+f3+db4:2 | "
                 "bb2+f3+db4:2 gb2+db3+bb3:2 | eb2+bb2+gb3:2 f2+c3+a3:2 |")


def picture(piece):
    piece.play("!ff " + GOLDENBERG, ("!ff " + GOLDENBERG, -12), bpm=56, label="goldenberg")
    piece.rest(0.6)
    piece.play("!p " + SCHMUYLE, "!pp " + SCHMUYLE_BASS, bpm=60, pedal=2, label="schmuyle")
    piece.play("!mp " + SCHMUYLE + " !<mf", "!p " + SCHMUYLE_BASS, bpm=60, pedal=2)

    # both at once: Goldenberg below, Schmuÿle whining on above him
    piece.play("!f " + SCHMUYLE + " " + SCHMUYLE[5:] + " !<ff",
               ("!ff " + GOLDENBERG, -12), ("!ff " + GOLDENBERG, -24),
               bpm=56, label="together")

    # Schmuÿle's last plea, and Goldenberg's dismissal
    piece.play("m4/4 !p db5:1 c5:1/2 bb4:1/2 c5:1 a4:1 | !pp bb4:4 |",
               "m4/4 !pp gb2+db3+bb3:2 f2+c3+a3:2 | bb1+f2+db3:4 |",
               bpm=48, to=40, pedal=2, gap=0.8, label="plea")
    piece.play("m4/4 !ff bb2+bb1:1/2^ c3+c2:1/4 db3+db2 c3+c2:1 bb2+bb1:2^ | "
               "r:1 bb1+bb0:3^ |", bpm=56, pedal=4)


def schmuyle():
    piece = Piece(SEED)
    picture(piece)
    return piece.render()
