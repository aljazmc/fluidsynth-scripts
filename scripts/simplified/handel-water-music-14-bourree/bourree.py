from orchestra import Orchestra

# Handel, Water Music, Suite No. 2 in D major, HWV 349, 5. Bourrée. A
# from-memory arrangement for General MIDI baroque band: a quick, bustling
# bourrée in D that closes the suite, played first by strings, then oboes,
# then the full band with trumpets and drums, in Handel's manner; the notes
# are approximate.
SEED = 1730

PARTS = ("oboes", "bassoons", "horns", "trumpets", "timpani", "harpsichord",
         "violins", "violins 2", "violas", "cellos", "basses")

# 2/2 (four crotchets)
TUNE = ("m4/4 d5:1 f#5:1/2 e5:1/2 d5:1 a5:1 | g5:1 f#5:1/2 e5:1/2 f#5:1 d5:1 | e5:1 a5:1 c#5:1 e5:1 | "
        "d5:2 a4:2 | f#5:1 a5:1/2 g5:1/2 f#5:1 d5:1 | b5:1 a5:1/2 g5:1/2 f#5:1 e5:1 | d5:1 f#5:1 e5:1 c#5:1 | d5:4 |")
BASS = "m4/4 d3:2 f#2:2 | g2:2 d2:2 | a2:2 a1:2 | d2:2 d3:2 | d3:2 b2:2 | g2:2 a2:2 | b2:1 g2:1 a2:2 | d2:4 |"


def picture(orchestra):
    for stage, dynamic in (("strings", "mf"), ("oboes", "mf"), ("tutti", "f")):
        parts = {"cellos": f"!{dynamic} " + BASS, "basses": (f"!{dynamic} " + BASS, -12),
                 "violas": (f"!{dynamic} " + BASS, 16), "harpsichord": (f"!{dynamic} " + BASS, 12)}
        if stage in ("strings", "tutti"):
            parts["violins"] = f"!{dynamic} " + TUNE
            parts["violins 2"] = (f"!{dynamic} " + TUNE, -12)
        if stage in ("oboes", "tutti"):
            parts["oboes"] = f"!{dynamic} " + TUNE
            parts["bassoons"] = f"!{dynamic} " + BASS
        if stage == "tutti":
            parts["trumpets"] = f"!{dynamic} " + TUNE
            parts["horns"] = (f"!{dynamic} " + BASS, 19)
            parts["timpani"] = f"!{dynamic} m4/4 " + " ".join(["d2:1 a1:1 d2:1 a1:1 |"] * 8)
        orchestra.play(parts, bpm=152, label=stage)


def bourree():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
