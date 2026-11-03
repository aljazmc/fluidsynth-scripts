from orchestra import Orchestra

# Handel, Water Music, Suite No. 1 in F major, HWV 348, 5. Air. A
# from-memory arrangement for General MIDI baroque band: the graceful,
# stately Air in F, each half played twice, the second time softer, over
# harpsichord continuo, in Handel's manner; the tune is approximate.
SEED = 1721

PARTS = ("oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Andante, 4/4
A = ("m4/4 c5:1 f5:3/2 e5:1/4 f5:1/4 g5:1 | a5:3/2 g5:1/2 f5:1 e5:1 | d5:1 g5:3/2 f5:1/4 g5:1/4 a5:1 | "
     "g5:2 c5:2 | a5:1 bb5:1/2 a5:1/2 g5:1 f5:1 | e5:1 f5:1 g5:1 c5:1 | f5:1 e5:1/2 d5:1/2 c5:1 bb4:1 | a4:2 c5:2 |")
A_BASS = "m4/4 f2:2 a2:2 | f2:2 c3:2 | bb2:2 g2:2 | c3:2 c2:2 | f2:2 d2:2 | c2:2 e2:2 | f2:1 g2:1 c3:2 | f2:4 |"
B = ("m4/4 g5:1 c6:3/2 bb5:1/4 a5:1/4 g5:1 | f5:3/2 e5:1/2 d5:1 c5:1 | d5:1 bb5:3/2 a5:1/4 g5:1/4 f5:1 | "
     "e5:2 c5:2 | f5:1 a5:1/2 g5:1/2 f5:1 e5:1 | d5:1 g5:1 bb4:1 a4:1 | g4:1 c5:1/2 bb4:1/2 a4:1 g4:1 | f4:4 |")
B_BASS = "m4/4 c3:2 e2:2 | f2:2 a2:2 | bb2:2 d2:2 | c3:2 c2:2 | d2:2 a2:2 | bb2:2 c3:2 | c3:2 c2:2 | f2:4 |"


def chords(bass):
    triads = {"f": "a3+c4", "a": "c4+f4", "c": "e3+g3", "bb": "d3+f3", "g": "bb3+d4", "d": "f3+a3", "e": "g3+c4"}
    out = []
    for token in bass.split():
        if token[0] in "abcdefg":
            note, length = token.split(":")
            out.append(f"{note}+{triads[note.rstrip('0123456789')]}:{length}")
        else:
            out.append(token)
    return " ".join(out)


def half(orchestra, melody, bass, dynamic):
    orchestra.play({"violins": f"!{dynamic} " + melody, "oboes": (f"!{dynamic} " + melody, 0),
                    "violins 2": (f"!{dynamic} " + chords(bass), 12), "violas": (f"!{dynamic} " + chords(bass), 0),
                    "cellos": f"!{dynamic} " + bass, "basses": (f"!{dynamic} " + bass, -12),
                    "bassoons": ("!p " + bass, 0), "harpsichord": ("!p " + chords(bass), 12)}, bpm=76)


def picture(orchestra):
    for dynamic in ("mf", "p"):
        half(orchestra, A, A_BASS, dynamic)
    for dynamic in ("mf", "p"):
        half(orchestra, B, B_BASS, dynamic)


def air():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
