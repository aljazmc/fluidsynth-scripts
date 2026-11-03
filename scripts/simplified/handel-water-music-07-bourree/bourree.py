from orchestra import Orchestra

# Handel, Water Music, Suite No. 1 in F major, HWV 348, 7. Bourrée. A
# from-memory arrangement for General MIDI baroque band: a short, springy
# bourrée in F starting on the upbeat, played through by strings, then
# oboes, then everyone, in Handel's manner; the notes are approximate.
SEED = 1723

PARTS = ("oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 2/2 (four crotchets), upbeat start
TUNE = ("m4/4 c5:1 | f5:1 e5:1/2 d5:1/2 c5:1 a4:1 | bb4:1 g4:1 c5:1 c5:1 | d5:1 c5:1/2 bb4:1/2 a4:1 f5:1 | "
        "e5:1 d5:1/2 c5:1/2 c5:1 c5:1 | f5:1 e5:1/2 d5:1/2 c5:1 a5:1 | g5:1 f5:1/2 e5:1/2 d5:1 bb5:1 | "
        "a5:1 g5:1/2 f5:1/2 g5:1 e5:1 | f5:4 |")
BASS = "m4/4 r:1 | f2:2 f3:2 | e3:2 e2:2 | bb2:2 f2:2 | c3:2 c2:2 | a2:2 f2:2 | bb2:2 g2:2 | c3:2 c2:2 | f2:4 |"


def picture(orchestra):
    for lead, dynamic in (("violins", "f"), ("oboes", "mf"), ("both", "f")):
        parts = {"cellos": f"!{dynamic} " + BASS, "basses": (f"!{dynamic} " + BASS, -12),
                 "violas": (f"!{dynamic} " + BASS, 19), "harpsichord": (f"!{dynamic} " + BASS, 12)}
        if lead in ("violins", "both"):
            parts["violins"] = f"!{dynamic} " + TUNE
            parts["violins 2"] = (f"!{dynamic} " + TUNE, -12)
        if lead in ("oboes", "both"):
            parts["oboes"] = f"!{dynamic} " + TUNE
            parts["bassoons"] = f"!{dynamic} " + BASS
        orchestra.play(parts, bpm=152, label=lead)


def bourree():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
