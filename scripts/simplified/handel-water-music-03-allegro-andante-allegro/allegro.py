from orchestra import Orchestra

# Handel, Water Music, Suite No. 1 in F major, HWV 348, 3. Allegro - Andante -
# Allegro da capo. A from-memory arrangement for General MIDI baroque band:
# the famous horn calls tossed against the strings in F, a gentle D minor
# Andante for oboes and strings, and the Allegro again, in Handel's manner;
# the notes are approximate.
SEED = 1719

PARTS = ("oboes", "bassoons", "horns", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 3/4
STRINGS = ("m3/4 f5:1/2 e5 f5 g5 a5 f5 | c6:1 c5:1 r:1 | d5:1/2 c5 d5 e5 f5 d5 | g5:1 c5:1 r:1 | "
           "a5:1/2 g5 f5 e5 d5 c5 | bb4:1/2 a4 g4 a4 bb4 g4 | a4:1 g4:1 f4:1 | f4:3 |")
HORNS = ("m3/4 f4:1 a4:1/2 c5:1/2 f5:1 | c5:2 r:1 | c5:1 e5:1/2 g5:1/2 c6:1 | g5:2 r:1 | "
         "f5:1 c5:1 a4:1 | c5:1 g4:1 c5:1 | f4:1 c5:1 c4:1 | f4:3 |")
BASS = "m3/4 f2:1 a2:1 f2:1 | c3:1 c2:1 r:1 | bb2:1 g2:1 bb2:1 | c3:1 c2:1 r:1 | f2:1 a2:1 f2:1 | g2:1 e2:1 c2:1 | f2:1 c2:1 c2:1 | f2:3 |"
CHORDS = ("m3/4 f3+a3+c4:3 | e3+g3+c4:3 | g3+bb3+d4:3 | e3+g3+c4:3 | f3+a3+c4:3 | g3+bb3+c4:3 | "
          "f3+a3+c4:3/2 e3+g3+bb3:3/2 | f3+a3+c4:3 |")

# Andante, D minor, 3/4
ANDANTE = ("m3/4 d5:2 e5:1 | f5:3/2 e5:1/2 d5:1 | c#5:2 d5:1 | e5:3 | f5:2 g5:1 | a5:3/2 g5:1/2 f5:1 | "
           "e5:1 d5:1 c#5:1 | d5:3 |")
ANDANTE_BASS = "m3/4 d3:3 | bb2:3 | a2:3 | a2:3 | d3:3 | f2:3 | a2:3 | d2:3 |"
ANDANTE_CHORDS = "m3/4 d4+f4:3 | d4+f4:3 | c#4+e4:3 | c#4+e4:3 | d4+f4:3 | c4+f4:3 | c#4+e4:3 | d4+f4:3 |"


def allegro_section(orchestra):
    for dynamic in ("f", "f"):
        orchestra.play({"violins": f"!{dynamic} " + STRINGS, "violins 2": (f"!{dynamic} " + STRINGS, -12),
                        "oboes": f"!{dynamic} " + STRINGS, "violas": f"!{dynamic} " + CHORDS,
                        "cellos": f"!{dynamic} " + BASS, "basses": (f"!{dynamic} " + BASS, -12),
                        "bassoons": f"!{dynamic} " + BASS, "harpsichord": f"!{dynamic} " + CHORDS},
                       bpm=132, label="strings")
        orchestra.play({"horns": f"!{dynamic} " + HORNS, "cellos": f"!mf " + BASS, "basses": ("!mf " + BASS, -12),
                        "harpsichord": "!mf " + CHORDS}, bpm=132, label="horns answer")


def picture(orchestra):
    allegro_section(orchestra)
    for dynamic in ("p", "pp"):
        orchestra.play({"oboes": f"!{dynamic} " + ANDANTE, "violins": (f"!{dynamic} " + ANDANTE, 0),
                        "violas": f"!{dynamic} " + ANDANTE_CHORDS, "cellos": f"!{dynamic} " + ANDANTE_BASS,
                        "basses": (f"!{dynamic} " + ANDANTE_BASS, -12), "harpsichord": f"!{dynamic} " + ANDANTE_CHORDS},
                       bpm=72, label="andante")
    allegro_section(orchestra)
    orchestra.play({"horns": "!f m3/4 f4+c5:3 |", "violins": "!f m3/4 f5+a5:3 |", "oboes": "!f m3/4 c5+f5:3 |",
                    "cellos": "!f m3/4 f2:3 |", "basses": "!f m3/4 f1:3 |", "harpsichord": "!f m3/4 f2+c3+f3+a3:3 |"},
                   bpm=100, label="end")


def allegro():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
