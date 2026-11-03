from orchestra import Orchestra

# Handel, Messiah, Part III, No. 50. O death, where is thy sting? (duet, alto
# and tenor). A from-memory arrangement for General MIDI baroque orchestra,
# the singers without words: a lively E-flat major duet over continuo, alto
# and tenor imitating each other, in Handel's manner; the notes are
# approximate.
SEED = 1790

PARTS = ("alto", "tenor", "harpsichord", "cellos", "basses")

# Andante, 4/4
STING = "m4/4 bb4:1 eb5:1/2 d5:1/2 eb5:1 bb4:1 | c5:1/2 bb4:1/2 ab4:1/2 g4:1/2 f4:1 r:1 |"
GRAVE = "m4/4 g4:1 ab4:1/2 bb4:1/2 eb4:1 f4:1 | g4:1/2 f4:1/2 eb4:1/2 d4:1/2 eb4:1 r:1 |"
BASS = "m4/4 eb3:1 g2:1 c3:1 g2:1 | ab2:1 bb2:1 bb1:1 r:1 |"
BASS2 = "m4/4 eb3:1 c3:1 ab2:1 ab2:1 | bb2:1 bb2:1 eb2:1 r:1 |"


CHORDS = {"eb3": "eb3+g3+bb3", "g2": "g2+bb2+eb3", "c3": "c3+eb3+g3", "ab2": "ab2+c3+eb3",
          "bb2": "bb2+d3+f3", "bb1": "bb1+f2+bb2", "eb2": "eb2+bb2+eb3"}


def continuo(bass, dynamic="mp"):
    """Cellos and basses on the bass line, the harpsichord filling in chords."""
    tokens = []
    for token in bass.split():
        note, _, length = token.partition(":")
        tokens.append(f"{CHORDS[note]}:{length}" if note in CHORDS else token)
    chords = " ".join(tokens)
    return {"cellos": f"!{dynamic} " + bass, "basses": (f"!{dynamic} " + bass, -12), "harpsichord": f"!{dynamic} " + chords}


def picture(orchestra):
    orchestra.play({"alto": "!mf " + STING, **continuo(BASS)}, bpm=92, label="alto")
    orchestra.play({"tenor": ("!mf " + STING, -12), "alto": "!mp " + GRAVE, **continuo(BASS)}, bpm=92, label="tenor answers")
    orchestra.play({"alto": ("!mf " + STING, 5), "tenor": ("!mp " + GRAVE, -7), **continuo(BASS2)}, bpm=92, label="O grave")
    orchestra.play({"tenor": ("!mf " + STING, -7), "alto": ("!mp " + GRAVE, 5), **continuo(BASS2)}, bpm=92)
    orchestra.play({"alto": "!mf " + STING, "tenor": ("!mf " + GRAVE, -12), **continuo(BASS)}, bpm=92)
    orchestra.play({"alto": "!mf " + GRAVE, "tenor": ("!mf " + STING, -12), **continuo(BASS2)}, bpm=92, to=80)


def sting():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render(tail=3.0)
