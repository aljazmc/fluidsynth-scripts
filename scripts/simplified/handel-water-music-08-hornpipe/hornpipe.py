from orchestra import Orchestra

# Handel, Water Music, Suite No. 1 in F major, HWV 348, 8. Hornpipe. A
# from-memory arrangement for General MIDI baroque band: a jaunty hornpipe in
# F in triple time with syncopated cross-rhythms, strings answered by oboes,
# in Handel's manner; the notes are approximate.
SEED = 1724

PARTS = ("oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 3/2 (six crotchets)
TUNE = ("m3/2 f5:1 c5:1 a4:1 c5:2 f5:1 | e5:1 c5:1 g4:1 c5:2 e5:1 | f5:1 a5:1 g5:1 f5:1 e5:1 d5:1 | c5:6 | "
        "d5:1 bb4:1 g4:1 bb4:2 d5:1 | c5:1 a4:1 f4:1 a4:2 c5:1 | bb4:1 d5:1 c5:1 bb4:1 a4:1 g4:1 | f4:6 |")
BASS = "m3/2 f2:3 a2:3 | c3:3 e2:3 | f2:3 bb2:3 | c3:3 c2:3 | bb2:3 g2:3 | f2:3 a2:3 | bb2:3 c3:3 | f2:6 |"


def picture(orchestra):
    for melody_part, dynamic in (("violins", "f"), ("oboes", "mf"), ("violins", "f")):
        parts = {melody_part: f"!{dynamic} " + TUNE, "violins 2": (f"!{dynamic} " + TUNE, -12),
                 "violas": (f"!{dynamic} " + BASS, 16), "cellos": f"!{dynamic} " + BASS,
                 "basses": (f"!{dynamic} " + BASS, -12), "harpsichord": (f"!{dynamic} " + BASS, 12)}
        if melody_part == "oboes":
            parts["bassoons"] = f"!{dynamic} " + BASS
        orchestra.play(parts, bpm=168, label=melody_part)


def hornpipe():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
