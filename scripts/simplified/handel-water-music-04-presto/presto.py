from orchestra import Orchestra

# Handel, Water Music, Suite No. 1 in F major, HWV 348, 4. Presto. A
# from-memory arrangement for General MIDI baroque band: a brisk binary dance
# in F for oboes, horns and strings over harpsichord continuo, each half
# repeated, in Handel's manner; the notes are approximate.
SEED = 1720

PARTS = ("oboes", "bassoons", "horns", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Presto, 3/8 (one and a half crotchet beats)
A = ("m3/8 c5:1/2 f5 a5 | g5:1/2 e5 c5 | f5:1/2 a5 c6 | bb5:1/2 g5 e5 | a5:1/2 f5 c5 | d5:1/2 bb4 g4 | "
     "c5:1/2 e5 g5 | c5:3/2 |")
A_BASS = "m3/8 f2:3/2 | c3:3/2 | f2:3/2 | c3:3/2 | f2:3/2 | bb2:3/2 | c3:3/2 | c2:3/2 |"
B = ("m3/8 g5:1/2 e5 c5 | a5:1/2 f5 c5 | bb5:1/2 g5 d5 | c6:1/2 a5 f5 | d5:1/2 bb4 g4 | c5:1/2 a4 f4 | "
     "g4:1/2 c5 e5 | f5:3/2 |")
B_BASS = "m3/8 c3:3/2 | f2:3/2 | g2:3/2 | a2:3/2 | bb2:3/2 | f2:3/2 | c3:3/2 | f2:3/2 |"


def half(orchestra, melody, bass, dynamic):
    chords = bass.replace("2:", "3:")
    orchestra.play({"violins": f"!{dynamic} " + melody, "oboes": f"!{dynamic} " + melody,
                    "violins 2": (f"!{dynamic} " + melody, -12), "horns": (f"!{dynamic} " + chords, 12),
                    "violas": (f"!{dynamic} " + chords, 7), "cellos": f"!{dynamic} " + bass,
                    "basses": (f"!{dynamic} " + bass, -12), "bassoons": f"!{dynamic} " + bass,
                    "harpsichord": (f"!{dynamic} " + chords, 12)}, bpm=168)


def picture(orchestra):
    for dynamic in ("f", "mf"):
        half(orchestra, A, A_BASS, dynamic)
    for dynamic in ("f", "mf"):
        half(orchestra, B, B_BASS, dynamic)
    orchestra.play({"violins": "!f m3/8 f5:3/2 |", "horns": "!f m3/8 f4+c5:3/2 |", "cellos": "!f m3/8 f2:3/2 |",
                    "basses": "!f m3/8 f1:3/2 |", "harpsichord": "!f m3/8 f2+c3+f3+a3:3/2 |"}, bpm=120, label="end")


def presto():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
