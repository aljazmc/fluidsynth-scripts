from orchestra import Orchestra

# Handel, Messiah, Part I, No. 2. Comfort ye my people (accompanied
# recitative, tenor). A from-memory arrangement for General MIDI baroque
# orchestra, the tenor singing without words: the gentle E major strings with
# their soft repeated chords, the tenor's "Comfort ye" phrases and the closing
# recitative "The voice of him that crieth in the wilderness" follow Handel,
# the notes are approximate.
SEED = 1742

PARTS = ("tenor", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Larghetto e piano, 4/4
RITORNELLO = "m4/4 b4:3/2 c#5:1/2 b4:1 e5:1 | d#5:3/2 e5:1/2 f#5:2 | g#5:1 f#5:1/2 e5:1/2 d#5:1 c#5:1 | b4:4 |"
PULSE = "m4/4 " + " ".join(f"{c}:1/2 {c} {c} {c} {c} {c} {c} {c} |" for c in ("g#3+b3", "f#3+b3", "e3+g#3", "d#3+f#3"))
BASS = "m4/4 e3:4 | b2:4 | c#3:2 a2:2 | b2:4 |"
COMFORT = "m4/4 b4:2 r:1 b4:1/2 c#5:1/2 | b4:2 r:2 | b4:1 e5:1 d#5:1 c#5:1 | b4:3 r:1 |"
SPEAK = ("m4/4 r:1 g#4:1/2 g#4:1/2 b4:1 e5:1 | d#5:1 c#5:1/2 b4:1/2 a4:1 g#4:1 | "
         "f#4:1 a4:1 g#4:1/2 f#4:1/2 e4:1 | f#4:2 r:2 |")
SPEAK_BASS = "m4/4 e3:4 | b2:4 | c#3:2 b2:2 | b1:4 |"
# the closing secco recitative: a few chords, the voice declaiming
CRIETH = ("m4/4 r:1 b4:1/2 b4:1/2 b4:1 e5:1/2 b4:1/2 | g#4:1/2 g#4 a4 b4 c#5:1 r:1 | "
          "c#5:1/2 d#5:1/2 e5:1 b4:1/2 b4:1/2 a4:1/2 g#4:1/2 | f#4:1 b4:1 r:2 | "
          "r:1 d#5:1/2 c#5:1/2 b4:1 a4:1/2 g#4:1/2 | a4:1/2 b4:1/2 g#4:1 r:2 |")
CRIETH_CHORDS = "m4/4 e3+g#3+b3:4 | e3+a3+c#4:4 | f#3+a3+c#4:4 | f#3+b3+d#4:4 | b2+d#3+f#3+a3:4 | e3+g#3+b3:4 |"


def picture(orchestra):
    strings = {"violins 2": "!pp " + PULSE, "violas": ("!pp " + PULSE, -12), "cellos": "!pp " + BASS,
               "basses": ("!pp " + BASS, -12), "harpsichord": "!pp " + PULSE}
    orchestra.play({"violins": "!p " + RITORNELLO, **strings}, bpm=56, label="ritornello")
    orchestra.play({"tenor": "!mp " + COMFORT, **strings}, bpm=56, label="comfort ye")
    orchestra.play({"tenor": "!mp " + SPEAK, "violins 2": "!pp " + PULSE, "violas": ("!pp " + PULSE, -12),
                    "cellos": "!pp " + SPEAK_BASS, "basses": ("!pp " + SPEAK_BASS, -12)}, bpm=56)
    orchestra.play({"violins": "!p " + RITORNELLO, **strings}, bpm=56)
    orchestra.play({"tenor": "!mf " + COMFORT, **strings}, bpm=56, to=52)
    orchestra.play({"tenor": "!mf " + CRIETH, "harpsichord": "!mp " + CRIETH_CHORDS,
                    "cellos": "!mp m4/4 e3:4 | a2:4 | f#2:4 | b2:4 | b1:4 | e2:4 |"}, bpm=72, label="recitative")
    orchestra.play({"violins": "!mf m4/4 b4+e5:1 b4+d#5:1 b4+e5:2 |", "violas": "!mf m4/4 g#3+b3:1 f#3+b3:1 g#3+b3:2 |",
                    "cellos": "!mf m4/4 e3:1 b2:1 e2:2 |", "basses": "!mf m4/4 e2:1 b1:1 e1:2 |",
                    "harpsichord": "!mf m4/4 e3+g#3+b3:1 b2+d#3+f#3:1 e2+b2+e3+g#3:2 |"}, bpm=72, to=56, label="cadence")


def people():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
