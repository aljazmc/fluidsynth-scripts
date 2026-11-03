from orchestra import Orchestra

# Handel, Messiah, Part I, No. 13. Pifa (Pastoral Symphony). A from-memory
# arrangement for General MIDI baroque orchestra: the shepherds' bagpipe
# music, a lilting C major siciliano in 12/8 for violins in thirds over a
# drone, follows Handel's design; the notes are approximate.
SEED = 1753

PARTS = ("harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Larghetto e mezzo piano, 12/8 (six crotchet beats)
TUNE = ("m12/8 e5:3/2 f5:1/2 e5:1 d5:3/2 e5:1/2 c5:1 | g5:3/2 a5:1/2 g5:1 f5:3/2 e5:1/2 d5:1 | "
        "e5:3/2 f5:1/2 e5:1 d5:1 c5:1/2 b4:1 c5:1/2 | d5:3 g4:3 | "
        "e5:3/2 f5:1/2 e5:1 d5:3/2 e5:1/2 c5:1 | a5:3/2 b5:1/2 a5:1 g5:3/2 f5:1/2 e5:1 | "
        "f5:1 e5:1/2 d5:1 c5:1/2 b4:1 c5:1/2 d5:3/2 | c5:6 |")
THIRDS = ("m12/8 c5:3/2 d5:1/2 c5:1 b4:3/2 c5:1/2 a4:1 | e5:3/2 f5:1/2 e5:1 d5:3/2 c5:1/2 b4:1 | "
          "c5:3/2 d5:1/2 c5:1 b4:1 a4:1/2 g4:1 a4:1/2 | b4:3 g4:3 | "
          "c5:3/2 d5:1/2 c5:1 b4:3/2 c5:1/2 a4:1 | f5:3/2 g5:1/2 f5:1 e5:3/2 d5:1/2 c5:1 | "
          "d5:1 c5:1/2 b4:1 a4:1/2 g4:1 a4:1/2 b4:3/2 | e4:6 |")
DRONE = "m12/8 " + " ".join(f"{c}:6 |" for c in ("c3+g3", "c3+g3", "c3+g3", "g2+d3", "c3+g3", "f2+c3", "g2+d3", "c3+g3"))


def picture(orchestra):
    for dynamic in ("mp", "p"):
        orchestra.play({"violins": f"!{dynamic} " + TUNE, "violins 2": f"!{dynamic} " + THIRDS,
                        "violas": ("!pp " + DRONE, 12), "cellos": "!pp " + DRONE, "basses": ("!pp " + DRONE, -12),
                        "harpsichord": ("!pp " + DRONE, 12)}, bpm=84, to=76 if dynamic == "p" else None)


def pifa():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
