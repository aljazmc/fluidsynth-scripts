from orchestra import Orchestra

# Handel, Messiah, Part I, No. 3. Ev'ry valley shall be exalted (air, tenor).
# A from-memory arrangement for General MIDI baroque orchestra, the tenor
# singing without words: the bright E major ritornello, the tenor's long
# runs on "exalted", the wavering "crooked" and the level "plain" follow
# Handel, the notes are approximate.
SEED = 1743

PARTS = ("tenor", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Andante, 4/4
RITORNELLO = ("m4/4 e5:1/2 b4 g#4 b4 e5:1 f#5:1/2 g#5:1/2 | a5:1/2 g#5 f#5 e5 d#5:1 b4:1 | "
              "e5:1/4 f#5 g#5 a5 b5:1 a5:1/4 g#5 f#5 e5 d#5:1 | e5:4 |")
RIT_BASS = "m4/4 e3:1 g#2:1 e2:1 e3:1 | c#3:1 a2:1 b2:1 b1:1 | c#3:1 a2:1 b2:1 b1:1 | e2:4 |"
EVERY = ("m4/4 b3:3/2 b3:1/2 e4:1 b3:1 | g#4:3/2 g#4:1/2 b4:2 | "
         "b4:1/4 c#5 d#5 e5 d#5 c#5 b4 a4 g#4 a4 b4 c#5 b4 a4 g#4 f#4 | "
         "g#4:1/4 a4 b4 c#5 b4 a4 g#4 f#4 e4:1 r:1 | "
         "e4:1 f#4:1/2 e4:1/2 d#4:1 c#4:1/2 d#4:1/2 | e4:2 b3:2 | "
         "c#4:1 e4:1 a4:1 g#4:1 | f#4:3 r:1 |")
EVERY_BASS = "m4/4 e3:4 | e3:2 g#2:2 | b2:2 b1:2 | e2:2 e3:2 | a2:2 b2:2 | c#3:2 g#2:2 | a2:2 b2:2 | b1:4 |"
CROOKED = ("m4/4 b4:1 a4:1/2 g#4:1/2 a4:1/2 g#4:1/2 f#4:1/2 g#4:1/2 | f#4:2 r:2 | "
           "e4:1/2 e4:1/2 a4:3 | g#4:4 | "
           "b4:1/4 c#5 d#5 e5 f#5 e5 d#5 c#5 b4 a4 g#4 f#4 e4:1 | f#4:2 d#4:2 | e4:4 |")
CROOKED_BASS = "m4/4 b2:2 e3:2 | b2:4 | c#3:2 a2:2 | e2:4 | e3:2 a2:2 | b2:2 b1:2 | e2:4 |"


def chords(bass):
    return bass.replace("e3:", "e3+g#3+b3:").replace("b2:", "b2+d#3+f#3:").replace("a2:", "a2+c#3+e3:")


def picture(orchestra):
    for dynamic in ("f", "mf"):
        orchestra.play({"violins": f"!{dynamic} " + RITORNELLO, "violins 2": (f"!{dynamic} " + RITORNELLO, -12),
                        "violas": (f"!{dynamic} " + RIT_BASS, 12), "cellos": f"!{dynamic} " + RIT_BASS,
                        "basses": (f"!{dynamic} " + RIT_BASS, -12), "harpsichord": (f"!p " + chords(RIT_BASS), 0)},
                       bpm=92, label="ritornello")
        orchestra.play({"tenor": "!mf " + EVERY, "violins": ("!p " + EVERY, 12), "cellos": "!p " + EVERY_BASS,
                        "basses": ("!p " + EVERY_BASS, -12), "harpsichord": "!p " + chords(EVERY_BASS),
                        "violas": ("!pp " + EVERY_BASS, 12)}, bpm=92, label="every valley")
        orchestra.play({"tenor": "!mf " + CROOKED, "cellos": "!p " + CROOKED_BASS, "basses": ("!p " + CROOKED_BASS, -12),
                        "harpsichord": "!p " + chords(CROOKED_BASS), "violins 2": ("!pp " + CROOKED_BASS, 19)},
                       bpm=92, label="crooked straight")
    orchestra.play({"violins": "!f " + RITORNELLO, "violins 2": ("!f " + RITORNELLO, -12), "violas": ("!f " + RIT_BASS, 12),
                    "cellos": "!f " + RIT_BASS, "basses": ("!f " + RIT_BASS, -12), "harpsichord": "!mf " + chords(RIT_BASS)},
                   bpm=92, to=76, label="ritornello")


def exalted():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
