from orchestra import Orchestra

# Holst, The Planets (1914-16), I. Mars, the Bringer of War. A from-memory
# arrangement for General MIDI orchestra: the 5/4 col legno ostinato on G,
# the slow chromatic climb above it, the brass hammering in the ostinato's
# rhythm, a march theme in the middle and the crushing close follow Holst, the
# notes are approximate.
SEED = 1914

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba",
         "timpani", "harp", "violins", "violins 2", "violas", "cellos", "basses", "percussion")


def ostinato(note, bars=1):
    """Holst's 5/4 rhythm: a triplet, two crotchets, two quavers, a crotchet."""
    bar = f"{note}:1/3' {note}' {note}' {note}:1' {note}' {note}:1/2' {note}' {note}:1' |"
    return "m5/4 " + " ".join([bar] * bars)


# a slow climb that never quite settles
CLIMB = "m5/4 g3:5~ | g3:5 | d4:5~ | d4:5 | db4:5 | c4:3 db4:1 d4:1 | eb4:5~ | eb4:5 |"

# the march in the middle, for horns and trombones in the tenor register
MARCH = ("m5/4 c4:2 d4:1 eb4:1 f4:1 | g4:3 f4:1 eb4:1 | d4:2 eb4:1 f4:1 d4:1 | c4:5 | "
         "eb4:2 f4:1 g4:1 ab4:1 | bb4:3 ab4:1 g4:1 | f4:2 g4:1 ab4:1 f4:1 | g4:5 |")
MARCH_CHORDS = ("m5/4 c3+g3:5 | c3+g3:5 | g2+d3:5 | c3+g3:5 | "
                "ab2+eb3:5 | eb3+bb3:5 | f2+c3:5 | g2+d3:5 |")
SNARE = "m5/4 " + " ".join(["38:1/3 38 38 38:1 38:1 38:1/2 38 38:1 |"] * 8)


def picture(orchestra):
    # the ostinato alone, then the climb above it
    orchestra.play({
        "violas": "!pp " + ostinato("g3", 2), "cellos": "!pp " + ostinato("g2", 2),
        "harp": "!pp " + ostinato("g2", 2), "timpani": "!pp " + ostinato("g2", 2),
    }, bpm=160, label="ostinato")
    orchestra.play({
        "violas": "!pp " + ostinato("g3", 8) + " !<mf", "cellos": "!pp " + ostinato("g2", 8) + " !<mf",
        "harp": "!pp " + ostinato("g2", 8) + " !<mf", "timpani": "!pp " + ostinato("g2", 8) + " !<mf",
        "bassoons": "!p " + CLIMB + " !<mf", "horns": "!p " + CLIMB + " !<mf",
    }, bpm=160, label="climb")
    orchestra.play({
        "violas": "!mf " + ostinato("g3", 8) + " !<f", "cellos": "!mf " + ostinato("g2", 8) + " !<f",
        "basses": "!mf " + ostinato("g2", 8) + " !<f", "timpani": "!mf " + ostinato("g2", 8) + " !<f",
        "horns": ("!mf " + CLIMB + " !<f", 5), "violins": ("!mf " + CLIMB + " !<f", 17),
        "trombones": ("!mf " + CLIMB + " !<f", -7), "clarinets": ("!mf " + CLIMB + " !<f", 5),
    }, bpm=160, label="climb higher")

    # the brass take up the ostinato's rhythm on clashing chords
    blows = ostinato("db5+f5", 2) + " " + ostinato("eb5+g5", 2)[5:] + " " \
        + ostinato("d5+f#5", 2)[5:] + " " + ostinato("c5+e5", 2)[5:]
    blows_low = ostinato("db4+ab4", 2) + " " + ostinato("eb4+bb4", 2)[5:] + " " \
        + ostinato("d4+a4", 2)[5:] + " " + ostinato("c4+g4", 2)[5:]
    orchestra.play({
        "trumpets": "!f " + blows + " !<ff", "trombones": "!f " + blows_low + " !<ff",
        "horns": ("!f " + blows_low + " !<ff", 12),
        "violins": "!f " + ostinato("g4", 8), "violins 2": "!f " + ostinato("g3", 8),
        "violas": "!f " + ostinato("g3", 8), "cellos": "!f " + ostinato("g2", 8),
        "basses": "!f " + ostinato("g2", 8), "timpani": "!f " + ostinato("g2", 8) + " !<ff",
        "tuba": "!f " + ostinato("g1", 8),
    }, bpm=160, label="brass blows")

    # the march
    orchestra.play({
        "horns": "!f " + MARCH, "trombones": ("!mf " + MARCH, -12), "bassoons": ("!mf " + MARCH, -12),
        "violas": "!mp " + MARCH_CHORDS, "cellos": "!mp " + MARCH_CHORDS,
        "basses": ("!mp " + MARCH_CHORDS, -12), "percussion": "!mp " + SNARE,
    }, bpm=144, label="march")
    orchestra.play({
        "trumpets": "!f " + MARCH, "horns": ("!f " + MARCH, -12), "violins": ("!f " + MARCH, 12),
        "trombones": ("!f " + MARCH, -12), "tuba": ("!f " + MARCH_CHORDS, -12),
        "violas": "!f " + MARCH_CHORDS, "cellos": "!f " + MARCH_CHORDS, "basses": ("!f " + MARCH_CHORDS, -12),
        "percussion": "!f " + SNARE + " !<ff", "timpani": "!f " + ostinato("c3", 8),
    }, bpm=144, to=160, label="march, tutti")

    # the ostinato returns under everything
    orchestra.play({
        "trumpets": ("!ff " + CLIMB, 12), "horns": ("!ff " + CLIMB, 5), "trombones": "!ff " + CLIMB,
        "flutes": ("!ff " + CLIMB, 24), "oboes": ("!ff " + CLIMB, 17), "clarinets": ("!ff " + CLIMB, 12),
        "violins": ("!ff " + CLIMB, 12), "violins 2": "!ff " + ostinato("g4", 8),
        "violas": "!ff " + ostinato("g3", 8), "cellos": "!ff " + ostinato("g2", 8),
        "basses": "!ff " + ostinato("g2", 8), "timpani": "!ff " + ostinato("g2", 8) + " !<fff",
        "tuba": "!ff " + ostinato("g1", 8), "bassoons": "!ff " + ostinato("g2", 8),
    }, bpm=160, label="return")

    # crushing close: a clash hammered in the ostinato's rhythm, then C
    clash = ostinato("c4+db4+f4+ab4", 2)
    orchestra.play({
        "trumpets": ("!fff " + clash, 12), "horns": "!fff " + clash, "trombones": ("!fff " + clash, -12),
        "violins": ("!fff " + clash, 12), "violas": "!fff " + clash, "cellos": ("!fff " + clash, -12),
        "basses": "!fff " + ostinato("c2", 2), "tuba": "!fff " + ostinato("c2", 2),
        "timpani": "!fff " + ostinato("c2", 2), "percussion": "!fff " + ostinato("36", 2),
    }, bpm=160, to=120, label="clash")
    end = "m4/4 X:1^ r:1 X:1^ r:1 | X:4^ |"
    chord = {"trumpets": "c5+e5+g5", "horns": "c4+e4+g4", "trombones": "c3+g3+c4", "tuba": "c2",
             "violins": "c5+g5+c6", "violins 2": "e4+c5", "violas": "g3+c4", "cellos": "c3+g3",
             "basses": "c2", "flutes": "c6+g6", "oboes": "e5+c6", "clarinets": "g4+c5",
             "bassoons": "c2+c3", "timpani": "c2", "percussion": "36+49"}
    orchestra.play({part: "!fff " + end.replace("X", notes) for part, notes in chord.items()},
                   bpm=80, to=56, label="end")


def war():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
