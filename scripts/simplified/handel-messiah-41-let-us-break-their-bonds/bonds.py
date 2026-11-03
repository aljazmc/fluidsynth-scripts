from orchestra import Orchestra

# Handel, Messiah, Part II, No. 41. Let us break their bonds asunder (chorus).
# A from-memory arrangement for General MIDI baroque orchestra, the choir
# singing without words: the defiant C major chorus, its snapping staccato
# "let us break their bonds asunder" set against the long, tied "and cast
# away their yokes from us", in Handel's manner; the notes are approximate.
SEED = 1781

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro e staccato, 4/4
BREAK = "m4/4 g4:1/2' c5' c5' e5' d5:1/2' g4' g4' b4' | c5:1/2' e5' d5' c5' b4:1' g4:1' |"
CAST = "m4/4 c5:4~ | c5:2 b4:2 | a4:4~ | a4:2 g4:2 |"
CAST_LOW = "m4/4 e4:4~ | e4:2 d4:2 | c4:4~ | c4:2 b3:2 |"


def picture(orchestra):
    entries = [(0, "violins"), (-5, "violins 2"), (-12, "violas"), (-24, "cellos")]
    for i, (shift, strings) in enumerate(entries):
        parts = {"choir": [("!f " + BREAK, s) for s, _ in entries[:i + 1]], strings: ("!f " + BREAK, shift),
                 "harpsichord": "!mf m4/4 c3+e3+g3:2 g2+b2+d3:2 | c3+e3+g3:2 g2+b2+d3:2 |"}
        if i == 3:
            parts["basses"] = ("!f " + BREAK, -36)
            parts["bassoons"] = ("!f " + BREAK, -24)
        orchestra.play(parts, bpm=116, label="let us break their bonds")
    for dynamic in ("f", "ff"):
        orchestra.play({"choir": [("!" + dynamic + " " + CAST, 0), "!" + dynamic + " " + CAST_LOW,
                                  ("!" + dynamic + " " + BREAK + " " + BREAK[5:], -12), ("!" + dynamic + " " + BREAK + " " + BREAK[5:], -24)],
                        "violins": "!" + dynamic + " " + CAST, "oboes": "!" + dynamic + " " + CAST,
                        "violins 2": "!" + dynamic + " " + CAST_LOW, "violas": ("!" + dynamic + " " + BREAK + " " + BREAK[5:], -12),
                        "cellos": ("!" + dynamic + " " + BREAK + " " + BREAK[5:], -24),
                        "basses": ("!" + dynamic + " " + BREAK + " " + BREAK[5:], -36)}, bpm=116, label="and cast away")
    orchestra.play({"choir": ["!ff m4/4 c5:1^ r:1 c5:2^ |", "!ff m4/4 g4:1^ r:1 g4:2^ |", "!ff m4/4 e4:1^ r:1 e4:2^ |",
                              "!ff m4/4 c3:1^ r:1 c3:2^ |"], "violins": "!ff m4/4 c5+e5:1^ r:1 c5+e5:2^ |",
                    "violas": "!ff m4/4 g4:1^ r:1 g4:2^ |", "cellos": "!ff m4/4 c3:1^ r:1 c3:2^ |",
                    "basses": "!ff m4/4 c2:1^ r:1 c2:2^ |", "harpsichord": "!ff m4/4 c3+e3+g3:1^ r:1 c3+e3+g3:2^ |"},
                   bpm=116, to=90, label="end")


def bonds():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
