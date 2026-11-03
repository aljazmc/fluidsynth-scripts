from orchestra import Orchestra

# Holst, The Planets, VII. Neptune, the Mystic. A from-memory arrangement for
# General MIDI orchestra: the quiet 5/4, the flutes circling between E minor
# and G-sharp minor, harps and celesta, and the wordless women's chorus
# swaying between two chords until it fades into nothing follow Holst, the
# notes are approximate.
SEED = 1921

PARTS = ("flutes", "oboes", "clarinets", "harp", "celesta", "choir",
         "violins", "violins 2", "violas", "cellos", "basses")

# Andante, 5/4, pianissimo throughout
CIRCLE = "m5/4 " + " ".join(["e5:1/2 b4 g4 b4 e5 b4 g4 b4 e5 b4 |",
                             "d#5:1/2 b4 g#4 b4 d#5 b4 g#4 b4 d#5 b4 |"] * 4)
HAZE = "m5/4 " + " ".join(["e3+b3:5 |", "g#2+d#3:5 |"] * 4)
GLINT = "m5/4 " + " ".join(["r:3 b5:1/2 r:3/2 |", "r:2 d#6:1/2 r:5/2 |"] * 4)
HARP = "m5/4 " + " ".join(["e2:1/2 b2 e3 g3 b3 e4 b3 g3 e3 b2 |",
                           "g#1:1/2 d#2 g#2 b2 d#3 g#3 d#3 b2 g#2 d#2 |"] * 4)

# the chorus: two chords, endlessly
VOICES = "m5/4 " + " ".join(["e4+g4+b4:5 |", "d#4+g#4+b4:5 |"] * 4)
VOICES_HIGH = "m5/4 " + " ".join(["g4+b4+e5:5 |", "g#4+b4+d#5:5 |"] * 4)
STRINGS = "m5/4 " + " ".join(["e3+b3+g4:5 |", "g#2+d#3+b3:5 |"] * 4)


def picture(orchestra):
    orchestra.play({"flutes": "!pp " + CIRCLE, "clarinets": "!ppp " + HAZE}, bpm=66, label="circling")
    orchestra.play({"flutes": "!pp " + CIRCLE, "oboes": ("!ppp " + HAZE, 12),
                    "harp": "!pp " + HARP, "celesta": "!pp " + GLINT, "violas": "!ppp " + HAZE,
                    "cellos": ("!ppp " + HAZE, -12)}, bpm=66, label="harps")
    orchestra.play({"violins": "!ppp " + STRINGS + " !<pp", "violins 2": ("!ppp " + STRINGS, -12),
                    "celesta": ("!pp " + CIRCLE, 12), "harp": "!pp " + HARP,
                    "basses": ("!ppp " + HAZE, -12)}, bpm=66, label="strings")

    # the voices enter, the orchestra falls away beneath them
    orchestra.play({"choir": "!ppp " + VOICES + " !<pp", "flutes": "!pp " + CIRCLE + " !>ppp",
                    "harp": "!pp " + HARP + " !>ppp", "violins": "!ppp " + STRINGS + " !>n",
                    "celesta": "!pp " + GLINT}, bpm=66, label="voices")
    orchestra.play({"choir": ["!pp " + VOICES, "!pp " + VOICES_HIGH], "celesta": "!ppp " + GLINT,
                    "flutes": "!ppp " + CIRCLE + " !>n"}, bpm=66)
    # the voices alone, repeating until they are lost in the distance
    orchestra.play({"choir": ["!pp " + VOICES + " " + VOICES[5:] + " !>n",
                              "!pp " + VOICES_HIGH + " " + VOICES_HIGH[5:] + " !>n"]},
                   bpm=66, to=56, label="lost in the distance")


def mystic():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render(tail=4.0)
