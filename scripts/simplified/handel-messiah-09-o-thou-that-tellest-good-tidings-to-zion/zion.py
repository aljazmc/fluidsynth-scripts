from orchestra import Orchestra

# Handel, Messiah, Part I, No. 9. O thou that tellest good tidings to Zion
# (air, alto, and chorus). A from-memory arrangement for General MIDI baroque
# orchestra, voices without words: the swinging D major 6/8 air for alto with
# violins, then the chorus taking up the tune, follow Handel, the notes are
# approximate.
SEED = 1749

PARTS = ("alto", "choir", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Andante, 6/8 (three crotchet beats)
TUNE = ("m6/8 a4:1 f#4:1/2 d4:1 a4:1/2 | b4:1 a4:1/2 g4:1 f#4:1/2 | e4:1 a4:1/2 c#5:1 e5:1/2 | d5:3/2 a4:3/2 | "
        "b4:1 d5:1/2 g5:1 b4:1/2 | a4:1 f#4:1/2 d5:1 f#4:1/2 | e4:1 g4:1/2 f#4:1 e4:1/2 | d4:3 |")
BASS = "m6/8 d3:3/2 f#2:3/2 | g2:3/2 a2:3/2 | a2:3/2 c#3:3/2 | d3:3/2 f#2:3/2 | g2:3/2 e2:3/2 | f#2:3/2 d2:3/2 | a2:3/2 a1:3/2 | d2:3 |"
CHORDS = "m6/8 f#3+a3:3 | g3+b3:3/2 a3+c#4:3/2 | a3+c#4:3 | f#3+a3:3 | g3+b3:3 | f#3+a3:3 | g3+c#4:3/2 e3+g3:3/2 | f#3+a3:3 |"
ALTO_C = "m6/8 f#4:1 d4:1/2 a3:1 f#4:1/2 | g4:1 f#4:1/2 e4:1 d4:1/2 | c#4:1 e4:1/2 a4:1 c#4:1/2 | a4:3/2 f#4:3/2 | " \
         "g4:1 b4:1/2 d5:1 g4:1/2 | f#4:1 d4:1/2 a4:1 d4:1/2 | c#4:1 e4:1/2 d4:1 c#4:1/2 | a3:3 |"
TENOR_C = "m6/8 d4:3/2 a3:3/2 | d4:3/2 c#4:3/2 | a3:3 | a3:3 | d4:3 | d4:3/2 a3:3/2 | a3:3/2 g3:3/2 | f#3:3 |"


def picture(orchestra):
    orchestra.play({"violins": "!mf " + TUNE, "violins 2": ("!mf " + TUNE, -12), "violas": "!p " + CHORDS,
                    "cellos": "!mf " + BASS, "basses": ("!mf " + BASS, -12), "harpsichord": "!p " + CHORDS},
                   bpm=112, label="ritornello")
    for dynamic in ("mf", "mf"):
        orchestra.play({"alto": f"!{dynamic} " + TUNE, "violins": ("!p " + TUNE, 12), "violas": "!p " + CHORDS,
                        "cellos": "!p " + BASS, "basses": ("!p " + BASS, -12), "harpsichord": "!p " + CHORDS},
                       bpm=112, label="alto")
    orchestra.play({"violins": "!mf " + TUNE, "violins 2": ("!mf " + TUNE, -12), "cellos": "!mf " + BASS,
                    "basses": ("!mf " + BASS, -12), "harpsichord": "!p " + CHORDS}, bpm=112)
    orchestra.play({"choir": [("!f " + TUNE, 12), "!f " + ALTO_C, "!f " + TENOR_C, ("!f " + BASS, 0)],
                    "violins": ("!f " + TUNE, 12), "violins 2": "!f " + ALTO_C, "violas": "!f " + TENOR_C,
                    "cellos": "!f " + BASS, "basses": ("!f " + BASS, -12), "harpsichord": "!mf " + CHORDS},
                   bpm=112, label="chorus")
    orchestra.play({"violins": "!f " + TUNE, "violins 2": ("!f " + TUNE, -12), "violas": "!mf " + CHORDS,
                    "cellos": "!f " + BASS, "basses": ("!f " + BASS, -12), "harpsichord": "!mf " + CHORDS},
                   bpm=112, to=92, label="ritornello")


def zion():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
