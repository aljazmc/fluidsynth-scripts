from orchestra import Orchestra

# Handel, Messiah, Part II, No. 37. The Lord gave the word (chorus). A
# from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: the tenors and basses' proclamation "The Lord gave
# the word" answered by the whole choir's busy, running "great was the
# company of the preachers" in B-flat major, in Handel's manner; the notes
# are approximate.
SEED = 1777

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Andante allegro, 4/4
WORD = "m4/4 bb3:1 f3:1 d4:1 bb3:1 | f4:2 r:2 |"
COMPANY = {"s": "m4/4 f5:1/4 eb5 d5 c5 d5 eb5 f5 d5 bb4:1 f5:1 | g5:1/4 f5 eb5 d5 eb5 f5 g5 eb5 c5:1 g5:1 | "
                "f5:1/2 eb5 d5 c5 bb4:1 a4:1 | bb4:2 r:2 |",
           "a": "m4/4 d5:1 d5:1 d5:1 d5:1 | eb5:1 eb5:1 eb5:1 eb5:1 | d5:1 bb4:1 bb4:1 a4:1 | bb4:2 r:2 |",
           "t": "m4/4 bb3:1/4 c4 d4 eb4 f4 eb4 d4 c4 d4:1 bb3:1 | c4:1/4 d4 eb4 f4 g4 f4 eb4 d4 eb4:1 c4:1 | "
                "f4:1 f4:1 f4:1 eb4:1 | d4:2 r:2 |",
           "b": "m4/4 bb2:1 bb2:1 bb2:1 bb2:1 | eb3:1 eb3:1 c3:1 c3:1 | d3:1 eb3:1 f3:1 f2:1 | bb2:2 r:2 |"}


def picture(orchestra):
    for _ in range(2):
        orchestra.play({"choir": [("!f " + WORD, 12), "!f " + WORD], "violas": ("!f " + WORD, 12), "cellos": "!f " + WORD,
                        "basses": ("!f " + WORD, -12), "bassoons": "!f " + WORD,
                        "harpsichord": "!mf m4/4 bb2+d3+f3:4 | f2+a2+c3:2 r:2 |"}, bpm=104, label="the Lord gave the word")
        orchestra.play({"choir": [f"!f " + COMPANY[v] for v in "satb"], "violins": "!f " + COMPANY["s"],
                        "oboes": "!f " + COMPANY["s"], "violins 2": "!f " + COMPANY["a"], "violas": "!f " + COMPANY["t"],
                        "cellos": "!f " + COMPANY["b"], "basses": ("!f " + COMPANY["b"], -12),
                        "bassoons": "!f " + COMPANY["b"], "harpsichord": "!mf " + COMPANY["b"]},
                       bpm=104, label="great was the company")
    orchestra.play({"choir": [f"!ff " + COMPANY[v] for v in "satb"], "violins": "!ff " + COMPANY["s"],
                    "oboes": "!ff " + COMPANY["s"], "violins 2": "!ff " + COMPANY["a"], "violas": "!ff " + COMPANY["t"],
                    "cellos": "!ff " + COMPANY["b"], "basses": ("!ff " + COMPANY["b"], -12),
                    "bassoons": "!ff " + COMPANY["b"], "harpsichord": "!f " + COMPANY["b"]}, bpm=104, to=84)


def word():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
