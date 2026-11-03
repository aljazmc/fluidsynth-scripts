from orchestra import Orchestra

# Handel, Messiah, Part III, No. 48. The trumpet shall sound (air, bass). A
# from-memory arrangement for General MIDI baroque orchestra, the bass
# singing without words: the D major Pomposo in 3/4 with its brilliant
# trumpet obbligato, the bass and trumpet calling to each other "and the dead
# shall be raised incorruptible", a quieter B minor middle "for this
# corruptible must put on incorruption", and the da capo, follow Handel; the
# notes are approximate.
SEED = 1788

PARTS = ("bass voice", "trumpets", "timpani", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Pomposo, ma non allegro, 3/4
CALL = ("m3/4 a4:1 d5:1 f#5:1 | a5:2 f#5:1 | d5:1/2 e5 f#5 g5 a5 f#5 | e5:2 a4:1 | "
        "d5:1 f#5:1 a5:1 | d6:2 a5:1 | b5:1/2 a5 g5 f#5 e5 d5 | d5:3 |")
VOICE = ("m3/4 a3:1 d4:1 f#4:1 | a4:2 f#4:1 | d4:1 a3:1 f#3:1 | e3:2 a3:1 | "
         "d4:1/4 e4 f#4 g4 a4:1 f#4:1 | b4:1 a4:1 g4:1 | f#4:1 e4:1 a3:1 | d3:3 |")
BASS = "m3/4 d3:3 | d3:3 | d3:3 | a2:3 | d3:3 | f#2:3 | g2:1 a2:1 a1:1 | d2:3 |"
PAD = "m3/4 f#3+a3:3 | f#3+a3:3 | f#3+a3:3 | e3+a3:3 | f#3+a3:3 | f#3+a3:3 | g3+b3:1 e3+a3:2 | f#3+a3:3 |"
DRUMS = "m3/4 d3:1 a2:1 a2:1 | d3:2 r:1 | d3:1 a2:1 d3:1 | a2:2 r:1 | d3:1 a2:1 a2:1 | d3:2 r:1 | a2:1 a2:1 a2:1 | d3:3 |"
# the middle section, B minor, no trumpet
CORRUPTIBLE = ("m3/4 f#3:1 b3:1 d4:1 | c#4:2 b3:1 | a#3:1 b3:1 c#4:1 | f#3:3 | "
               "d4:1 c#4:1 b3:1 | e4:2 d4:1 | c#4:1 b3:1 a#3:1 | b3:3 |")
CORRUPTIBLE_BASS = "m3/4 b2:3 | e2:3 | f#2:3 | f#2:3 | b2:3 | g2:3 | f#2:3 | b1:3 |"


def tutti(orchestra, label):
    orchestra.play({"trumpets": "!f " + CALL, "violins": "!f " + CALL, "violins 2": "!mf " + PAD,
                    "violas": ("!mf " + PAD, -12), "cellos": "!f " + BASS, "basses": ("!f " + BASS, -12),
                    "harpsichord": "!mf " + PAD, "timpani": "!f " + DRUMS}, bpm=96, label=label)


def picture(orchestra):
    tutti(orchestra, "trumpet ritornello")
    orchestra.play({"bass voice": "!f " + VOICE, "cellos": "!mf " + BASS, "basses": ("!mf " + BASS, -12),
                    "harpsichord": "!mf " + PAD, "violins 2": "!p " + PAD}, bpm=96, label="the trumpet shall sound")
    orchestra.play({"bass voice": "!f " + VOICE, "trumpets": "!f " + CALL, "cellos": "!f " + BASS,
                    "basses": ("!f " + BASS, -12), "harpsichord": "!mf " + PAD, "timpani": "!mf " + DRUMS},
                   bpm=96, label="and the dead shall be raised")
    tutti(orchestra, "ritornello")
    orchestra.play({"bass voice": "!mp " + CORRUPTIBLE, "cellos": "!p " + CORRUPTIBLE_BASS,
                    "basses": ("!p " + CORRUPTIBLE_BASS, -12), "violins 2": ("!pp " + CORRUPTIBLE_BASS, 19),
                    "harpsichord": ("!p " + CORRUPTIBLE_BASS, 12)}, bpm=88, label="for this corruptible")
    orchestra.play({"bass voice": "!f " + VOICE, "trumpets": "!f " + CALL, "cellos": "!f " + BASS,
                    "basses": ("!f " + BASS, -12), "harpsichord": "!mf " + PAD, "timpani": "!mf " + DRUMS},
                   bpm=96, label="da capo")
    tutti(orchestra, "ritornello")


def sound():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=95)
    picture(orchestra)
    return orchestra.render()
