from orchestra import Orchestra

# Handel, Water Music, Suite No. 1 in F major, HWV 348, 2. Adagio e staccato.
# A from-memory arrangement for General MIDI baroque band: a plaintive D minor
# oboe solo over detached string chords and harpsichord, in Handel's manner;
# the notes are approximate.
SEED = 1718

PARTS = ("oboes", "bassoons", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# 3/4
SOLO = ("m3/4 a4:2 d5:1 | c#5:3/2 b4:1/2 a4:1 | f5:2 e5:1 | d5:3 | "
        "bb4:2 g5:1 | f5:3/2 e5:1/2 d5:1 | e5:1 c#5:1 a4:1 | d5:3 | "
        "f5:2 a5:1 | g5:3/2 f5:1/2 e5:1 | d5:1 c5:1 bb4:1 | a4:3 | "
        "d5:2 bb4:1 | g4:3/2 a4:1/2 bb4:1 | a4:1 g4:1 e4:1 | d4:3 |")
HARMONY = ("d", "a", "d", "d", "g", "d", "a", "d", "d", "c", "g", "a", "bb", "g", "a", "d")
CHORDS = {"d": ("d2", "d3+f3+a3"), "a": ("a1", "c#3+e3+a3"), "g": ("g1", "bb2+d3+g3"),
          "c": ("c2", "c3+e3+g3"), "bb": ("bb1", "bb2+d3+f3")}


def picture(orchestra):
    strings = "m3/4 " + " ".join(f"{CHORDS[h][1]}:1' {CHORDS[h][1]}' {CHORDS[h][1]}' |" for h in HARMONY)
    bass = "m3/4 " + " ".join(f"{CHORDS[h][0]}:1' {CHORDS[h][0]}' {CHORDS[h][0]}' |" for h in HARMONY)
    harpsichord = "m3/4 " + " ".join(f"{CHORDS[h][0]}+{CHORDS[h][1]}:3 |" for h in HARMONY)
    for dynamic in ("mp", "p"):
        orchestra.play({"oboes": f"!{dynamic} " + SOLO, "violins 2": ("!p " + strings, 12), "violas": "!p " + strings,
                        "cellos": ("!p " + bass, 12), "basses": "!p " + bass, "harpsichord": "!p " + harpsichord},
                       bpm=56, to=50 if dynamic == "p" else None, label="adagio")
    orchestra.play({"oboes": "!p m3/4 a4:3 |", "violas": "!p m3/4 c#4+e4+a4:3 |", "cellos": "!p m3/4 a2:3 |",
                    "basses": "!p m3/4 a1:3 |", "harpsichord": "!p m3/4 a1+c#3+e3+a3:3 |"}, bpm=44, label="half close")


def staccato():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=80)
    picture(orchestra)
    return orchestra.render()
