from orchestra import Orchestra

# Handel, Messiah, Part I, No. 6. But who may abide the day of his coming
# (air, alto). A from-memory arrangement for General MIDI baroque orchestra,
# the alto singing without words: the gentle D minor Larghetto in 3/8 twice
# interrupted by the Prestissimo "for he is like a refiner's fire" with its
# furious string tremolos follows Handel, the notes are approximate.
SEED = 1746

PARTS = ("alto", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Larghetto, 3/8 (one and a half crotchet beats)
ABIDE = ("m3/8 d4:1/2 f4:1/2 a4:1/2 | a4:1 g4:1/4 f4:1/4 | e4:1/2 g4:1/2 bb4:1/2 | bb4:1 a4:1/2 | "
         "d5:3/4 c5:1/4 bb4:1/2 | a4:1/2 g4:1/2 f4:1/2 | e4:3/4 f4:1/4 g4:1/2 | f4:1 e4:1/2 | d4:3/2 |")
ABIDE_BASS = "m3/8 d3:3/2 | d3:3/2 | c#3:3/2 | c#3:3/2 | bb2:3/2 | f2:3/2 | g2:3/2 | a2:3/2 | d2:3/2 |"
ABIDE_STRINGS = "m3/8 f3+a3:3/2 | f3+a3:3/2 | e3+g3:3/2 | e3+g3:3/2 | d3+f3:3/2 | c3+f3:3/2 | bb2+e3:3/2 | c#3+e3:3/2 | d3+f3:3/2 |"

# Prestissimo, 4/4
FIRE = ("m4/4 a4:1 a4:1/2 a4:1/2 d5:1 a4:1 | f4:1/4 g4 a4 bb4 a4 g4 f4 e4 d4:2 | "
        "bb4:1 bb4:1/2 bb4:1/2 e5:1 bb4:1 | a4:1/4 bb4 c5 d5 c5 bb4 a4 g4 a4:2 | "
        "d5:1/4 c5 bb4 a4 g4 f4 e4 d4 c#4:1 a4:1 | d4:4 |")
FIRE_TREMOLO = "m4/4 " + " ".join(f"{c}:1/4 " * 16 + "|" for c in ("d4+f4+a4", "d4+f4+a4", "e4+g4+bb4", "f4+a4+c5", "e4+g4+a4", "d4+f4+a4"))
FIRE_BASS = "m4/4 " + " ".join(f"{b}:1/2 " * 8 + "|" for b in ("d3", "d3", "c#3", "f2", "a2", "d2"))


def larghetto(orchestra, dynamic):
    orchestra.play({"alto": f"!{dynamic} " + ABIDE, "violins": ("!pp " + ABIDE, 12), "violins 2": "!pp " + ABIDE_STRINGS,
                    "violas": ("!pp " + ABIDE_STRINGS, 0), "cellos": "!p " + ABIDE_BASS, "basses": ("!p " + ABIDE_BASS, -12),
                    "harpsichord": "!p " + ABIDE_STRINGS}, bpm=60, label="larghetto")


def prestissimo(orchestra):
    orchestra.play({"alto": "!f " + FIRE, "violins": ("!f " + FIRE_TREMOLO, 12), "violins 2": "!f " + FIRE_TREMOLO,
                    "violas": ("!f " + FIRE_TREMOLO, -12), "cellos": "!f " + FIRE_BASS, "basses": ("!f " + FIRE_BASS, -12),
                    "harpsichord": "!f " + FIRE_BASS}, bpm=168, label="refiner's fire")


def picture(orchestra):
    orchestra.play({"violins": "!p " + ABIDE, "violins 2": "!pp " + ABIDE_STRINGS, "cellos": "!p " + ABIDE_BASS,
                    "basses": ("!p " + ABIDE_BASS, -12)}, bpm=60, label="ritornello")
    larghetto(orchestra, "mp")
    prestissimo(orchestra)
    larghetto(orchestra, "mp")
    prestissimo(orchestra)
    orchestra.play({"violins": "!f " + FIRE_TREMOLO.split("|")[0] + "|", "violas": "!f m4/4 d4+f4:4 |",
                    "cellos": "!f m4/4 d3:4 |", "basses": "!f m4/4 d2:4 |"}, bpm=168, to=100, label="end")


def abide():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
