from orchestra import Orchestra

# Beethoven, Symphony No. 5, IV. Allegro. A from-memory arrangement for
# General MIDI orchestra: the blazing C major march with piccolo, trombones
# and contrabassoon joining the orchestra for the first time, the second theme
# in triplets, the ghost of the scherzo, the return and the Presto coda with
# its endless final C major chords follow Beethoven, the notes are
# approximate.
SEED = 1805

PARTS = ("piccolo", "flutes", "oboes", "clarinets", "bassoons", "contrabassoon", "horns", "trumpets",
         "trombones", "timpani", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4 (alla breve)
MARCH = ("m4/4 c5:2 e5:2 | g5:4 | f5:1 e5:1 d5:1 c5:1 | d5:2 c5:1 b4:1 | "
         "c5:1 d5:1 e5:1 f5:1 | g5:2 a5:1 g5:1 | f5:1 e5:1 d5:1 g4:1 | c5:4 |")
MARCH_CHORDS = ("m4/4 e4+g4:2 g4+c5:2 | g4+c5+e5:4 | a4+c5:1 g4+c5 f4+b4 e4+g4 | f4+a4:2 e4+g4:1 d4+f4:1 | "
                "e4+g4:2 g4+c5:2 | c5+e5:2 c5+f5:1 c5+e5:1 | a4+c5:2 g4+b4:2 | e4+g4:4 |")
MARCH_BASS = "m4/4 c3:2 c3:2 | e3:4 | f3:1 c3:1 d3:1 c3:1 | g2:2 g2:2 | c3:2 a2:2 | e2:2 f2:2 | g2:2 g2:2 | c3:4 |"

TRIPLETS = ("m4/4 g5:1/3 f#5 g5 a5:1 g5:1/3 f#5 g5 b5:1 | d6:2 c6:1 b5:1 | a5:1/3 g#5 a5 b5:1 a5:1/3 g#5 a5 c6:1 | "
            "b5:2 a5:1 g5:1 | g5:1/3 f#5 g5 a5:1 g5:1/3 f#5 g5 e6:1 | d6:1 c6:1 b5:1 a5:1 | "
            "g5:1 b5:1 a5:1 f#5:1 | g5:4 |")
TRIPLET_BASS = "m4/4 g2:4 | g2:4 | d2:4 | g2:4 | c3:4 | d3:4 | d3:4 | g2:4 |"

GHOST = "m3/4 g4:1 g4 g4 | g4:3 | g4:1 g4 g4 | g4:3 | ab4:1 ab4 ab4 | g4:3 | f4:1 f4 f4 | eb4:3 |"


def march(orchestra, dynamic, **kwargs):
    orchestra.play({"violins": f"!{dynamic} " + MARCH, "flutes": (f"!{dynamic} " + MARCH, 12),
                    "piccolo": (f"!{dynamic} " + MARCH, 12), "oboes": f"!{dynamic} " + MARCH,
                    "clarinets": f"!{dynamic} " + MARCH_CHORDS, "trumpets": f"!{dynamic} " + MARCH,
                    "horns": f"!{dynamic} " + MARCH_CHORDS, "trombones": (f"!{dynamic} " + MARCH_CHORDS, -12),
                    "violins 2": f"!{dynamic} " + MARCH_CHORDS, "violas": (f"!{dynamic} " + MARCH_CHORDS, -12),
                    "cellos": f"!{dynamic} " + MARCH_BASS, "basses": (f"!{dynamic} " + MARCH_BASS, -12),
                    "bassoons": f"!{dynamic} " + MARCH_BASS, "contrabassoon": (f"!{dynamic} " + MARCH_BASS, -12),
                    "timpani": f"!{dynamic} m4/4 " + " ".join(["c3:1 r:1 g2:1 r:1 |"] * 8)}, **kwargs)


def picture(orchestra):
    march(orchestra, "ff", bpm=168, label="march")
    march(orchestra, "ff", bpm=168)
    orchestra.play({"violins": "!f " + TRIPLETS, "flutes": ("!f " + TRIPLETS, 0), "clarinets": ("!f " + TRIPLETS, -12),
                    "violas": "!mf m4/4 " + " ".join(["b3+d4:1/2 b3+d4 b3+d4 b3+d4 b3+d4 b3+d4 b3+d4 b3+d4 |"] * 8),
                    "cellos": "!f " + TRIPLET_BASS, "basses": ("!f " + TRIPLET_BASS, -12),
                    "horns": "!mf m4/4 " + " ".join(["g3+d4:4 |"] * 8)}, bpm=168, label="second theme")
    orchestra.play({"violins": ("!ff " + TRIPLETS, 0), "violins 2": ("!ff " + TRIPLETS, -12),
                    "oboes": ("!ff " + TRIPLETS, 0), "flutes": ("!ff " + TRIPLETS, 12),
                    "trumpets": "!ff m4/4 " + " ".join(["g4:1 r:1 g4:1 r:1 |"] * 8),
                    "cellos": "!ff " + TRIPLET_BASS, "basses": ("!ff " + TRIPLET_BASS, -12),
                    "trombones": "!f m4/4 " + " ".join(["g2+d3:4 |"] * 8), "timpani": "!ff m4/4 " + " ".join(["g2:1 r:3 |"] * 8)},
                   bpm=168)

    # the scherzo's ghost
    orchestra.play({"clarinets": "!pp " + GHOST, "oboes": ("!pp " + GHOST, 0),
                    "violins": "!pp m3/4 " + " ".join(["c4+eb4:1' r:2 |"] * 8),
                    "basses": "!pp m3/4 " + " ".join(["c2:1' r:2 |"] * 8)}, bpm=120, label="ghost")
    orchestra.play({"violins": "!pp m4/4 g4+b4+d5+f5:4 !<ff | g4+b4+d5+f5:4 |",
                    "violas": "!pp m4/4 g3+d4:4 !<ff | g3+d4:4 |", "basses": "!pp m4/4 g1:4 !<ff | g1:4 |",
                    "timpani": "!pp m4/4 g2:1/4 g2 g2 g2 g2 g2 g2 g2 g2 g2 g2 g2 g2 g2 g2 g2 !<ff | g2:4 |"},
                   bpm=120, to=168, label="return")
    march(orchestra, "fff", bpm=168, label="march again")

    # Presto
    presto = "m4/4 " + " ".join(["c5:1/2 e5 g5 e5 c5 e5 g5 c6 |", "b4:1/2 d5 g5 d5 b4 d5 g5 b5 |"] * 4)
    orchestra.play({"violins": "!ff " + presto, "violins 2": ("!ff " + presto, -12), "flutes": ("!ff " + presto, 12),
                    "piccolo": ("!ff " + presto, 12), "violas": ("!ff " + presto, -12),
                    "cellos": "!ff m4/4 " + " ".join(["c3:1 c3 c3 c3 |", "g2:1 g2 g2 g2 |"] * 4),
                    "basses": "!ff m4/4 " + " ".join(["c2:1 c2 c2 c2 |", "g1:1 g1 g1 g1 |"] * 4),
                    "trumpets": "!ff m4/4 " + " ".join(["c5:2 c5:2 |", "g4:2 g4:2 |"] * 4),
                    "horns": "!ff m4/4 " + " ".join(["c4+g4:4 |", "g3+d4:4 |"] * 4),
                    "timpani": "!ff m4/4 " + " ".join(["c3:1 c3 c3 c3 |", "g2:1 g2 g2 g2 |"] * 4)},
                   bpm=200, label="presto")
    end = "m4/4 " + " ".join(["X:1^ r:1 X:1^ r:1 |"] * 4) + " X:4^ | X:2^ r:2 | X:4^ |"
    voicing = {"violins": "c5+e5+g5+c6", "violins 2": "e4+c5", "violas": "g3+e4", "cellos": "c3", "basses": "c2",
               "flutes": "e6+g6", "piccolo": "c7", "oboes": "e5+c6", "clarinets": "g4+c5", "bassoons": "c3+c4",
               "contrabassoon": "c2", "horns": "c4+g4", "trumpets": "c5+e5", "trombones": "c3+g3+c4", "timpani": "c3"}
    orchestra.play({p: "!fff " + end.replace("X", v) for p, v in voicing.items()}, bpm=200, to=150, label="end")


def allegro():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
