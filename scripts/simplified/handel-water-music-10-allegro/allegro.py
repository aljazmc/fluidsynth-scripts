from orchestra import Orchestra

# Handel, Water Music, Suite No. 2 in D major, HWV 349, 1. Allegro. A
# from-memory arrangement for General MIDI baroque band: the ceremonial D
# major opening of the suite, trumpets and horns trading fanfares with the
# strings and oboes over timpani and continuo, in Handel's manner; the notes
# are approximate.
SEED = 1726

PARTS = ("oboes", "bassoons", "horns", "trumpets", "timpani", "harpsichord",
         "violins", "violins 2", "violas", "cellos", "basses")

# 4/4
FANFARE = "m4/4 d5:1 d5:1/2 d5:1/2 a4:1 d5:1 | f#5:1 f#5:1/2 f#5:1/2 d5:1 f#5:1 | a5:1 f#5:1 d5:1 a4:1 | d5:2 r:2 |"
ANSWER = ("m4/4 d5:1/2 e5 f#5 g5 a5 g5 f#5 e5 | f#5:1/2 g5 a5 b5 a5 g5 f#5 e5 | "
          "d5:1/2 f#5 e5 d5 c#5 e5 a4 c#5 | d5:2 r:2 |")
BASS = "m4/4 d2:1 d3:1 d2:1 d3:1 | d2:1 d3:1 d2:1 d3:1 | d2:1 f#2:1 a2:1 a1:1 | d2:2 r:2 |"
DRUMS = "m4/4 d2:1 d2:1/2 d2:1/2 a1:1 d2:1 | d2:1 d2:1/2 d2:1/2 a1:1 d2:1 | d2:1 a1:1 d2:1 a1:1 | d2:2 r:2 |"


def picture(orchestra):
    for dynamic in ("f", "mf", "f"):
        orchestra.play({"trumpets": f"!{dynamic} " + FANFARE, "horns": (f"!{dynamic} " + FANFARE, -12),
                        "timpani": f"!{dynamic} " + DRUMS, "cellos": f"!{dynamic} " + BASS,
                        "basses": (f"!{dynamic} " + BASS, -12), "harpsichord": (f"!{dynamic} " + BASS, 12)},
                       bpm=112, label="fanfare")
        orchestra.play({"violins": f"!{dynamic} " + ANSWER, "oboes": f"!{dynamic} " + ANSWER,
                        "violins 2": (f"!{dynamic} " + ANSWER, -12), "violas": (f"!{dynamic} " + BASS, 19),
                        "cellos": f"!{dynamic} " + BASS, "basses": (f"!{dynamic} " + BASS, -12),
                        "bassoons": f"!{dynamic} " + BASS, "harpsichord": (f"!{dynamic} " + BASS, 12)},
                       bpm=112, label="answer")
    end = "m4/4 X:1^ r:1 X:2^ |"
    voicing = {"trumpets": "d5+f#5", "horns": "d4+a4", "timpani": "d2", "violins": "d5+a5", "violins 2": "f#4",
               "violas": "a3", "oboes": "a4+d5", "cellos": "d3", "basses": "d2", "bassoons": "d2",
               "harpsichord": "d2+a2+d3+f#3"}
    orchestra.play({p: "!f " + end.replace("X", v) for p, v in voicing.items()}, bpm=96, label="end")


def allegro():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
