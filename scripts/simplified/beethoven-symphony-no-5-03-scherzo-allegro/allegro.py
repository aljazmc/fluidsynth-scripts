from orchestra import Orchestra

# Beethoven, Symphony No. 5, III. Allegro (Scherzo). A from-memory
# arrangement for General MIDI orchestra: the cellos' and basses' creeping
# arpeggio, the horns' hammering G in the motto's rhythm, the C major trio's
# scrambling fugato, the ghostly pianissimo return and the timpani's long
# transition that rises without a break into the finale follow Beethoven, the
# notes are approximate.
SEED = 1806

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "timpani",
         "violins", "violins 2", "violas", "cellos", "basses")

# 3/4, one beat to the bar
CREEP = "m3/4 r:2 g2:1 | c3:1 eb3:1 g3:1 | c4:2 bb3:1 | ab3:1 g3:1 f#3:1 | g3:3~ | g3:3 |"
ANSWER = "m3/4 r:2 g2:1 | c3:1 eb3:1 g3:1 | c4:2 bb3:1 | ab3:1 bb3:1 b3:1 | c4:3~ | c4:3 |"
HAMMER = "m3/4 g4:1 g4 g4 | g4:3 | g4:1 g4 g4 | g4:3 | ab4:1 ab4 ab4 | g4:3 | f4:1 f4 f4 | eb4:3 |"
HAMMER_CHORDS = "m3/4 c4+eb4:3 | c4+eb4:3 | c4+eb4:3 | b3+d4:3 | c4+f4:3 | c4+eb4:3 | b3+d4:3 | c4+eb4:3 |"
HAMMER_BASS = "m3/4 c3:3 | c3:3 | c3:3 | g2:3 | f2:3 | c3:3 | g2:3 | c3:3 |"

# Trio: C major, a fugato that starts in the basses
FUGUE = "m3/4 c3:1/2 d3 e3 f3 g3 a3 | b3:1/2 c4 b3 a3 g3 f3 | e3:1/2 f3 g3 e3 c3:1 | g3:1 g2:1 r:1 |"
REST4 = "m3/4 r:3 | r:3 | r:3 | r:3 |"


def scherzo(orchestra, ghost=False):
    level = "pp" if ghost else "p"
    loud = "p" if ghost else "ff"
    orchestra.play({"cellos": f"!{level} " + CREEP, "basses": (f"!{level} " + CREEP, -12)},
                   bpm=264, label="creep")
    orchestra.play({"cellos": f"!{level} " + ANSWER, "basses": (f"!{level} " + ANSWER, -12),
                    "violas": (f"!{level} " + ANSWER, 12), "violins 2": "!pp m3/4 r:3 | r:3 | r:3 | r:3 | eb4:3~ | eb4:3 |"},
                   bpm=264)
    orchestra.play({"horns": f"!{loud} " + HAMMER, "violins": (f"!{loud} " + HAMMER_CHORDS, 12),
                    "violins 2": f"!{loud} " + HAMMER_CHORDS, "violas": f"!{loud} " + HAMMER_CHORDS,
                    "cellos": f"!{loud} " + HAMMER_BASS, "basses": (f"!{loud} " + HAMMER_BASS, -12),
                    **({} if ghost else {"trumpets": "!f " + HAMMER, "timpani": "!f " + HAMMER_BASS.replace("3:", "2:").replace("f2", "g2")})},
                   bpm=264, label="hammer")


def trio(orchestra):
    voices = [("basses", -12), ("cellos", 0), ("violas", 7), ("violins 2", 12), ("violins", 19)]
    for i, (part, shift) in enumerate(voices):
        parts = {}
        for j, (other, s) in enumerate(voices[:i + 1]):
            parts[other] = ("!f " + FUGUE, s) if j == i else ("!mf " + FUGUE, s)
        if i >= 2:
            parts["bassoons"] = ("!f " + FUGUE, -12)
        orchestra.play(parts, bpm=264, label="trio")
    orchestra.play({"violins": ("!ff " + FUGUE, 19), "violins 2": ("!ff " + FUGUE, 12), "violas": ("!ff " + FUGUE, 7),
                    "cellos": "!ff " + FUGUE, "basses": ("!ff " + FUGUE, -12), "flutes": ("!f " + FUGUE, 24),
                    "oboes": ("!f " + FUGUE, 19), "horns": "!f m3/4 c4+g4:3 | g3+d4:3 | c4+g4:3 | g3+d4:3 |"},
                   bpm=264)


def picture(orchestra):
    scherzo(orchestra)
    scherzo(orchestra)
    trio(orchestra)
    scherzo(orchestra, ghost=True)

    # the transition: a drum ticking on C under a held chord, then the climb
    orchestra.play({"timpani": "!pp m3/4 " + " ".join(["c3:1 c3 c3 |"] * 12),
                    "violins 2": "!pp m3/4 " + " ".join(["ab3+c4:3 |"] * 12),
                    "violas": "!pp m3/4 " + " ".join(["ab3:3 |"] * 12),
                    "basses": "!pp m3/4 " + " ".join(["ab1:3 |"] * 12)},
                   bpm=264, label="drum")
    orchestra.play({"timpani": "!pp m3/4 " + " ".join(["c3:1 c3 c3 |"] * 8) + " !<ff",
                    "violins": "!pp m3/4 g4:3 | ab4:3 | b4:3 | c5:3 | d5:3 | eb5:3 | f5:3 | g5:3 | !<ff",
                    "violins 2": "!pp m3/4 " + " ".join(["g3+d4:3 |"] * 8) + " !<ff",
                    "violas": "!pp m3/4 " + " ".join(["b3+f4:3 |"] * 8) + " !<ff",
                    "cellos": "!pp m3/4 " + " ".join(["g2:3 |"] * 8) + " !<ff",
                    "basses": "!pp m3/4 " + " ".join(["g1:3 |"] * 8) + " !<ff",
                    "horns": "!pp m3/4 " + " ".join(["g3+d4:3 |"] * 8) + " !<ff",
                    "bassoons": "!pp m3/4 " + " ".join(["g2+f3:3 |"] * 8) + " !<ff"},
                   bpm=264, label="climb")
    voicing = {"violins": "g4+b4+d5+f5", "violins 2": "g3+d4", "violas": "b3+f4", "cellos": "g2", "basses": "g1",
               "horns": "g3+d4", "trumpets": "g4", "bassoons": "g2+f3", "oboes": "b4+f5", "clarinets": "d4+f4",
               "flutes": "d5+g5", "timpani": "g2"}
    orchestra.play({p: f"!ff m3/4 {v}:3~ | {v}:3 |" for p, v in voicing.items()}, bpm=264, label="into the finale")


def allegro():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
