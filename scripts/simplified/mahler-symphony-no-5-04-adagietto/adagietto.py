from orchestra import Orchestra

# Mahler, Symphony No. 5, Part III, 4. Adagietto. Sehr langsam. A from-memory
# arrangement for General MIDI orchestra: strings and harp alone, the long
# F major song in the violins, the yearning middle and the swelling return
# follow Mahler; the melody's opening is close, the rest approximate.
SEED = 1905

PARTS = ("harp", "violins", "violins 2", "violas", "cellos", "basses")

# Sehr langsam, 4/4
SONG = ("m4/4 r:3 a4:1 | a4:3 bb4:1/2 c5:1/2 | d5:3 c5:1 | c5:2 bb4:1 a4:1 | "
        "g4:3 a4:1/2 bb4:1/2 | bb4:2 a4:1 g4:1 | f4:3 e4:1 | f4:4 |")
SONG_HARMONY = ("f", "f", "bb", "f", "g", "c", "c", "f")
YEARN = ("m4/4 r:3 c5:1 | f5:3 e5:1/2 d5:1/2 | c5:3 bb4:1 | a4:2 g4:1 f4:1 | "
         "db5:3 c5:1/2 bb4:1/2 | ab4:3 g4:1 | g4:2 a4:1 bb4:1 | c5:4 |")
YEARN_HARMONY = ("f", "f", "f", "f", "bbm", "f", "c", "c")
CHORDS = {"f": ("f2", "c3+f3+a3"), "bb": ("bb1", "d3+f3+bb3"), "g": ("g2", "bb2+d3+g3"),
          "c": ("c2", "e3+g3+bb3"), "bbm": ("bb1", "db3+f3+bb3")}


def harp(harmony):
    out = []
    for name in harmony:
        root, chord = CHORDS[name]
        notes = [root] + chord.split("+")
        out.append(" ".join(f"{n}:1/2" for n in notes + notes[::-1]) + " |")
    return "m4/4 " + " ".join(out)


def pad(harmony):
    return "m4/4 " + " ".join(f"{CHORDS[n][1]}:4 |" for n in harmony)


def bass(harmony):
    return "m4/4 " + " ".join(f"{CHORDS[n][0]}:4 |" for n in harmony)


def phrase(orchestra, song, harmony, dynamic, **kwargs):
    orchestra.play({"violins": f"!{dynamic} " + song, "violins 2": ("!pp " + pad(harmony), 12),
                    "violas": "!pp " + pad(harmony), "cellos": ("!pp " + bass(harmony), 12),
                    "basses": "!pp " + bass(harmony), "harp": "!p " + harp(harmony)}, **kwargs)


def picture(orchestra):
    orchestra.play({"harp": "!pp " + harp(("f", "f")), "violas": "!ppp " + pad(("f", "f"))}, bpm=50, label="harp")
    phrase(orchestra, SONG, SONG_HARMONY, "p", bpm=50, label="song")
    phrase(orchestra, SONG + " !<mf", SONG_HARMONY, "p", bpm=52, label="song again")
    phrase(orchestra, YEARN + " !<f", YEARN_HARMONY, "mp", bpm=54, to=58, label="yearning")
    orchestra.play({"violins": ("!f " + YEARN, 12), "violins 2": "!f " + YEARN, "violas": "!mf " + pad(YEARN_HARMONY),
                    "cellos": ("!mf " + YEARN, -12), "basses": "!mf " + bass(YEARN_HARMONY),
                    "harp": "!mf " + harp(YEARN_HARMONY)}, bpm=56, to=46, label="climax")
    phrase(orchestra, SONG, SONG_HARMONY, "p", bpm=48, to=40, label="return")
    orchestra.play({"violins": "!pp m4/4 f4+a4+c5:4~ | f4+a4+c5:4 !>n |", "violas": "!pp m4/4 c4:4~ | c4:4 !>n |",
                    "cellos": "!pp m4/4 f2:4~ | f2:4 !>n |", "basses": "!pp m4/4 f1:4~ | f1:4 !>n |",
                    "harp": "!pp m4/4 f2:1/2 c3 f3 a3 c4 f4 a4 c5 | f5:4 |"}, bpm=40)


def adagietto():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=110)
    picture(orchestra)
    return orchestra.render(tail=6.0)
