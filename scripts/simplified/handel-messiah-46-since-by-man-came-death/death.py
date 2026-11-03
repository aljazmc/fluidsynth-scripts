from orchestra import Orchestra

# Handel, Messiah, Part III, No. 46. Since by man came death (chorus). A
# from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: the hushed, unaccompanied A minor Grave "Since by man
# came death" and "For as in Adam all die" twice broken by the orchestra's
# bright C major Allegro "by man came also the resurrection of the dead",
# "even so in Christ shall all be made alive", follows Handel; the notes are
# approximate.
SEED = 1786

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

GRAVE = {"s": "m4/4 e5:2 e5:1 d5:1 | c5:2 b4:2 | c5:1 d5:1 b4:1 c5:1 | b4:4 |",
         "a": "m4/4 c5:2 b4:1 b4:1 | a4:2 g#4:2 | a4:1 a4:1 g#4:1 a4:1 | g#4:4 |",
         "t": "m4/4 a4:2 g#4:1 f4:1 | e4:2 e4:2 | e4:1 f4:1 e4:1 e4:1 | e4:4 |",
         "b": "m4/4 a3:2 e3:1 d3:1 | e3:2 e2:2 | a2:1 d3:1 e3:1 a2:1 | e3:4 |"}
ALLEGRO = {"s": "m4/4 c5:1 e5:1/2 d5:1/2 c5:1 g5:1 | e5:1/4 f5 g5 f5 e5 d5 c5 b4 c5:1 d5:1 | e5:1 d5:1 c5:2 |",
           "a": "m4/4 g4:1 g4:1/2 g4:1/2 g4:1 g4:1 | g4:1 a4:1 g4:1 g4:1 | g4:1 g4:1 e4:2 |",
           "t": "m4/4 e4:1 c4:1/2 d4:1/2 e4:1 d4:1 | c4:1 c4:1 e4:1 d4:1 | c4:1 b3:1 g3:2 |",
           "b": "m4/4 c3:1 c3:1/2 b2:1/2 c3:1 b2:1 | c3:1 a2:1 e2:1 f2:1 | g2:1 g2:1 c2:2 |"}


def grave(orchestra, shift, label):
    orchestra.play({"choir": [f"!pp " + GRAVE[v] for v in "satb"]}, bpm=44, shift=shift, gap=0.4, label=label)


def allegro(orchestra, label):
    orchestra.play({"choir": [f"!f " + ALLEGRO[v] for v in "satb"], "violins": "!f " + ALLEGRO["s"],
                    "oboes": "!f " + ALLEGRO["s"], "violins 2": "!f " + ALLEGRO["a"], "violas": "!f " + ALLEGRO["t"],
                    "cellos": "!f " + ALLEGRO["b"], "basses": ("!f " + ALLEGRO["b"], -12),
                    "bassoons": "!f " + ALLEGRO["b"], "harpsichord": "!f " + ALLEGRO["b"]},
                   bpm=112, gap=0.3, label=label)


def picture(orchestra):
    grave(orchestra, 0, "since by man came death")
    allegro(orchestra, "by man came also the resurrection")
    grave(orchestra, -2, "for as in Adam all die")
    allegro(orchestra, "even so in Christ shall all be made alive")
    allegro(orchestra, "shall all be made alive")


def death():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=105)
    picture(orchestra)
    return orchestra.render()
