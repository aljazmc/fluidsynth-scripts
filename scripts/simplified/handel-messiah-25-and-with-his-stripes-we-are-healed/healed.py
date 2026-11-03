from orchestra import Orchestra

# Handel, Messiah, Part II, No. 25. And with his stripes we are healed
# (chorus). A from-memory arrangement for General MIDI baroque orchestra, the
# choir singing without words: a strict F minor fugue in long notes, its
# subject leaping through a diminished fourth, entering voice by voice over
# the continuo, in Handel's manner; the notes are approximate.
SEED = 1765

PARTS = ("choir", "oboes", "bassoons", "harpsichord", "organ", "violins", "violins 2", "violas", "cellos", "basses")

# Alla breve, moderato: four crotchets, slow minims
SUBJECT = "m4/4 f4:2 db5:2 | e4:3 f4:1 | g4:1 ab4:1 bb4:1 g4:1 | c5:2 r:2 |"
ANSWER = "m4/4 c5:2 ab5:2 | b4:3 c5:1 | d5:1 eb5:1 f5:1 d5:1 | g5:2 r:2 |"
COUNTER = "m4/4 ab4:2 bb4:2 | g4:2 ab4:2 | bb4:2 c5:2 | c5:1 bb4:1 ab4:2 |"


def picture(orchestra):
    plan = [("alto", (ANSWER, -12)), ("soprano", (ANSWER, 0)), ("tenor", (SUBJECT, -12)), ("bass", (SUBJECT, -24))]
    strings = {"soprano": "violins", "alto": "violins 2", "tenor": "violas", "bass": "cellos"}
    voices = [(SUBJECT, 0)]
    orchestra.play({"choir": [("!mf " + SUBJECT, 0)], "violins 2": "!mf " + SUBJECT, "organ": ("!p " + SUBJECT, -12)},
                   bpm=88, label="alto subject")
    for name, (line, shift) in plan[1:]:
        voices = [(COUNTER, s) for _, s in voices] + [(line, shift)]
        parts = {"choir": [("!mf " + text, s) for text, s in voices],
                 strings[name]: ("!mf " + line, shift), "harpsichord": ("!p " + COUNTER, -12)}
        if name == "bass":
            parts["basses"] = ("!mf " + line, shift - 12)
            parts["bassoons"] = ("!mf " + line, shift)
        orchestra.play(parts, bpm=88, label=f"{name} entry")
    orchestra.play({"choir": [("!f " + ANSWER, 0), ("!f " + SUBJECT, 0), ("!f " + COUNTER, -12), ("!f " + SUBJECT, -24)],
                    "violins": "!f " + ANSWER, "oboes": "!f " + ANSWER, "violins 2": "!f " + SUBJECT,
                    "violas": ("!f " + COUNTER, -12), "cellos": ("!f " + SUBJECT, -24), "basses": ("!f " + SUBJECT, -36),
                    "organ": ("!mf " + SUBJECT, -24)}, bpm=88, to=72, label="stretto")
    orchestra.play({"choir": ["!f m4/4 c5:4 | c5:4 |", "!f m4/4 ab4:4 | g4:4 |", "!f m4/4 f4:4 | e4:4 |", "!f m4/4 db3:4 | c3:4 |"],
                    "violins": "!f m4/4 c5:4 | c5:4 |", "violas": "!f m4/4 f4:4 | e4:4 |", "cellos": "!f m4/4 db3:4 | c3:4 |",
                    "basses": "!f m4/4 db2:4 | c2:4 |", "organ": "!mf m4/4 db3+f3+ab3:4 | c3+e3+g3:4 |"},
                   bpm=72, to=56, label="half close")


def healed():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render()
