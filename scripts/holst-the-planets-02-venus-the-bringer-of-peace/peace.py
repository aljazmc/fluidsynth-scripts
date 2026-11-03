from orchestra import Orchestra

# Holst, The Planets, II. Venus, the Bringer of Peace. A from-memory
# arrangement for General MIDI orchestra: the rising horn call, the woodwinds'
# answering chords, the solo violin, harp and celesta in E-flat follow Holst,
# the notes are approximate.
SEED = 1915

PARTS = ("flutes", "oboes", "clarinets", "horns", "harp", "celesta", "solo violin",
         "violins", "violins 2", "violas", "cellos", "basses")

# Adagio, 4/4
HORN = "m4/4 eb4:2 f4:1 g4:1 | bb4:3 g4:1 | ab4:2 g4:1 f4:1 | eb4:4 |"
ANSWER = ("m4/4 g5+bb5+eb6:2 gb5+bb5+db6:2 | f5+ab5+db6:2 f5+a5+c6:2 | "
          "eb5+g5+bb5:2 eb5+gb5+bb5:2 | d5+f5+bb5:4 |")
ANSWER_LOW = "m4/4 eb4+g4:2 eb4+gb4:2 | db4+f4:2 c4+f4:2 | bb3+eb4:2 bb3+eb4:2 | bb3+d4:4 |"

SONG = ("m4/4 bb5:2 c6:1 d6:1 | eb6:3 d6:1 | c6:1 bb5:1 ab5:1 g5:1 | f5:2 g5:2 | "
        "ab5:2 bb5:1 c6:1 | bb5:3 g5:1 | f5:2 eb5:1 f5:1 | eb5:4 |")
PAD = "m4/4 g3+bb3:4 | g3+bb3:4 | ab3+c4:4 | f3+bb3:4 | ab3+c4:4 | g3+bb3:4 | f3+ab3:4 | g3+bb3:4 |"
ROOTS = "m4/4 eb3:4 | eb3:4 | ab2:4 | bb2:4 | ab2:4 | eb3:4 | bb2:4 | eb3:4 |"
CHORDS = (("eb3", "bb3", "eb4", "g4"), ("eb3", "bb3", "eb4", "g4"), ("ab2", "eb3", "ab3", "c4"),
          ("bb2", "f3", "bb3", "d4"), ("ab2", "eb3", "ab3", "c4"), ("eb3", "bb3", "eb4", "g4"),
          ("bb2", "f3", "ab3", "d4"), ("eb3", "bb3", "eb4", "g4"))


def harp(chords):
    """Rising and falling quavers through each bar's chord."""
    bars = []
    for a, b, c, d in chords:
        bars.append(f"{a}:1/2 {b} {c} {d} {c} {b} {c} {d} |")
    return "m4/4 " + " ".join(bars)


def sparkle(chords):
    """Celesta glints on the top of each chord (play it two octaves up)."""
    return "m4/4 " + " ".join(f"r:1 {c}+{d}:1/2 r:3/2 {d}:1/2 r:1/2 |" for _, _, c, d in chords)


def picture(orchestra):
    orchestra.play({"horns": "!p " + HORN}, bpm=54, label="horn")
    orchestra.play({"flutes": "!pp " + ANSWER, "oboes": ("!pp " + ANSWER, -12),
                    "clarinets": "!pp " + ANSWER_LOW}, bpm=54, label="answer")
    orchestra.play({"horns": ("!p " + HORN, 5), "violas": "!pp " + ANSWER_LOW,
                    "harp": "!pp " + harp(CHORDS[:4])}, bpm=54)
    orchestra.play({"flutes": "!pp " + ANSWER, "clarinets": ("!pp " + ANSWER, -12),
                    "celesta": ("!pp " + sparkle(CHORDS[:4]), 24)}, bpm=54, to=50, gap=0.5)

    # the solo violin over harp and strings
    orchestra.play({"solo violin": "!p " + SONG + " !<mp", "violins 2": "!pp " + PAD,
                    "violas": ("!pp " + PAD, -12), "cellos": "!pp " + ROOTS, "basses": ("!pp " + ROOTS, -12),
                    "harp": "!p " + harp(CHORDS)}, bpm=56, label="violin")
    orchestra.play({"violins": "!mp " + SONG + " !<mf", "flutes": ("!p " + SONG, 0),
                    "violins 2": "!p " + PAD, "violas": ("!p " + PAD, -12), "cellos": "!p " + ROOTS,
                    "basses": ("!p " + ROOTS, -12), "harp": "!p " + harp(CHORDS),
                    "horns": ("!p " + PAD, 0)}, bpm=56, label="strings")

    # the horn call once more, and the peace settles
    orchestra.play({"horns": "!p " + HORN, "violins 2": "!pp m4/4 g3+bb3:4 | g3+bb3:4 | ab3+c4:4 | g3+bb3:4 |",
                    "cellos": "!pp m4/4 eb3:4 | eb3:4 | ab2:4 | eb3:4 |"}, bpm=54, label="horn again")
    orchestra.play({"flutes": "!pp " + ANSWER, "oboes": ("!pp " + ANSWER, -12),
                    "clarinets": "!pp " + ANSWER_LOW, "celesta": ("!pp " + sparkle(CHORDS[:4]), 24),
                    "harp": "!pp " + harp(CHORDS[:4])}, bpm=52, to=46)
    final = "m4/4 X:4~ | X:4 |"
    orchestra.play({
        "violins": "!pp " + final.replace("X", "g5+bb5+eb6") + " !>n",
        "violins 2": "!pp " + final.replace("X", "eb5+g5") + " !>n",
        "violas": "!pp " + final.replace("X", "bb3+eb4") + " !>n",
        "cellos": "!pp " + final.replace("X", "eb3") + " !>n",
        "basses": "!pp " + final.replace("X", "eb2") + " !>n",
        "harp": "!pp m4/4 eb3:1/2 bb3 eb4 g4 bb4 eb5 g5 bb5 | eb6:4 |",
        "celesta": "!pp m4/4 r:4 | g6+bb6+eb7:4 |",
    }, bpm=46, to=40, label="end")


def peace():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render(tail=6.0)
