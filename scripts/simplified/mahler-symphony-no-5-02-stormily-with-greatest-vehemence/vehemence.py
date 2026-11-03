from orchestra import Orchestra

# Mahler, Symphony No. 5, Part I, 2. Stürmisch bewegt, mit größter Vehemenz
# (Stormily, with greatest vehemence). A from-memory arrangement for General
# MIDI orchestra: the basses' furious upward lunges, the shrieking woodwinds,
# the slow lament that recalls the funeral march, the brass chorale in D major
# that blazes up and collapses, and the ghostly close follow Mahler, the notes
# are approximate.
SEED = 1903

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba", "timpani",
         "harp", "violins", "violins 2", "violas", "cellos", "basses", "percussion")

# Stürmisch bewegt, 2/2 (four crotchets)
LUNGE = "m4/4 " + " ".join(["a1:1/4 b1 c2 d2 e2 f2 g#2 a2 c3:1^ r:1 |", "r:4 |"] * 2)
SHRIEK = "m4/4 r:2 f6:1^ e6:1 | d6:1/2 c6 b5 a5 g#5:2 | r:2 a6:1^ g#6:1 | f6:1/2 e6 d6 c6 b5:2 |"
STAB = "m4/4 r:2 a3+c4+f4:1^ r:1 | r:4 | r:2 g#3+b3+e4:1^ r:1 | r:4 |"
FURY = ("m4/4 e5:1 f5:1/2 e5:1/2 d5:1 c5:1 | b4:3/2 c5:1/2 d5:2 | f5:1 e5:1/2 d5:1/2 c5:1 b4:1 | a4:4 | "
        "c6:1 b5:1/2 a5:1/2 g#5:1 a5:1 | f5:3/2 e5:1/2 d5:2 | c5:1 b4:1 a4:1 g#4:1 | a4:4 |")
FURY_BASS = "m4/4 " + " ".join(f"{b}:1/2 {b} {b} {b} {b} {b} {b} {b} |" for b in
                               ("a1", "d2", "e2", "a1", "a1", "d2", "e2", "a1"))

# Bedeutend langsamer: the cellos lament, remembering the funeral march
LAMENT = "m4/4 f3:2 e3:1 d3:1 | c3:3 db3:1 | eb3:2 db3:1 c3:1 | f2:4 | ab3:2 g3:1 f3:1 | e3:3 f3:1 | g3:2 c3:2 | f3:4 |"
LAMENT_PAD = "m4/4 " + " ".join(f"{c}:4 |" for c in ("ab3+c4", "ab3+c4", "g3+bb3", "ab3+c4", "ab3+c4", "bb3+c4", "bb3+e4", "ab3+c4"))

CHORALE = ("m4/4 d4+f#4+a4+d5:2 e4+g4+b4+e5:2 | f#4+a4+d5+f#5:4 | g4+b4+d5+g5:2 f#4+a4+d5+f#5:2 | "
           "e4+a4+c#5+e5:4 | d4+g4+b4+d5:2 e4+a4+c#5+e5:2 | f#4+a4+d5+f#5:2 g4+b4+e5+g5:2 | "
           "a4+d5+f#5+a5:4~ | a4+d5+f#5+a5:4 |")
CHORALE_BASS = "m4/4 d2:2 e2:2 | d2:4 | g1:2 d2:2 | a1:4 | b1:2 a1:2 | d2:2 e2:2 | d2:4~ | d2:4 |"


def storm(orchestra, dynamic, **kwargs):
    orchestra.play({"cellos": f"!{dynamic} " + LUNGE, "basses": (f"!{dynamic} " + LUNGE, 0),
                    "bassoons": (f"!{dynamic} " + LUNGE, 12), "flutes": f"!{dynamic} " + SHRIEK,
                    "oboes": (f"!{dynamic} " + SHRIEK, -12), "clarinets": (f"!{dynamic} " + SHRIEK, -12),
                    "trombones": (f"!{dynamic} " + STAB, -12), "horns": f"!{dynamic} " + STAB,
                    "timpani": f"!{dynamic} m4/4 r:2 a2:1^ r:1 | r:4 | r:2 e2:1^ r:1 | r:4 |"}, **kwargs)
    orchestra.play({"violins": f"!{dynamic} " + FURY, "violins 2": (f"!{dynamic} " + FURY, -12),
                    "violas": (f"!{dynamic} " + FURY_BASS, 24), "cellos": (f"!{dynamic} " + FURY_BASS, 12),
                    "basses": f"!{dynamic} " + FURY_BASS, "trumpets": (f"!{dynamic} " + FURY, 0),
                    "timpani": (f"!{dynamic} " + FURY_BASS, 12)}, **kwargs)


def picture(orchestra):
    storm(orchestra, "ff", bpm=152, label="storm")
    storm(orchestra, "fff", bpm=152)
    orchestra.play({"cellos": "!p " + LAMENT, "violas": "!pp " + LAMENT_PAD,
                    "basses": "!pp m4/4 f1:4 | f1:4 | c2:4 | f1:4 | f1:4 | c2:4 | c2:4 | f1:4 |",
                    "timpani": "!pp m4/4 " + " ".join(["f2:1/3 f2 f2 f2:3 |"] * 8)}, bpm=60, label="lament")
    orchestra.play({"violins": ("!mp " + LAMENT, 24), "cellos": "!mp " + LAMENT, "violas": "!p " + LAMENT_PAD,
                    "clarinets": ("!p " + LAMENT_PAD, 12)}, bpm=60, to=80)
    storm(orchestra, "ff", bpm=152, shift=-2, label="storm again")

    # the chorale breaks through in D major, then collapses
    orchestra.play({"trumpets": ("!ff " + CHORALE, 0), "horns": ("!ff " + CHORALE, -12),
                    "trombones": ("!ff " + CHORALE, -12), "tuba": "!ff " + CHORALE_BASS,
                    "violins": ("!ff m4/4 " + " ".join(["d5:1/4 e5 f#5 a5 d6 a5 f#5 e5 d5 e5 f#5 a5 d6 a5 f#5 e5 |"] * 8), 0),
                    "violins 2": ("!ff " + CHORALE, 0), "violas": ("!f " + CHORALE, -12),
                    "cellos": ("!ff " + CHORALE_BASS, 12), "basses": "!ff " + CHORALE_BASS,
                    "harp": "!f m4/4 " + " ".join(["d3:1/4 a3 d4 f#4 a4 d5 f#5 a5 d6 a5 f#5 d5 a4 f#4 d4 a3 |"] * 8),
                    "timpani": "!ff m4/4 " + " ".join(["d2:1 a1:1 d2:1 a1:1 |"] * 8),
                    "percussion": "!ff m4/4 49:4 | r:4 | r:4 | r:4 | 49:4 | r:4 | 49:4 | r:4 |"},
                   bpm=72, to=60, label="chorale")
    orchestra.play({"trombones": "!ff m4/4 a2+c3+f3:4 !>p | g#2+b2+e3:4 |",
                    "timpani": "!f m4/4 a1:1/4 a1 a1 a1 a1 a1 a1 a1 a1 a1 a1 a1 a1 a1 a1 a1 !>pp | a1:4 |",
                    "basses": "!f m4/4 a1:4 !>pp | a1:4 |", "percussion": "!f m4/4 52:4 | r:4 |"},
                   bpm=60, gap=0.5, label="collapse")
    # a ghostly close
    orchestra.play({"flutes": "!pp m4/4 e6:1/2 d6 c6 b5 a5:2 | r:4 |", "harp": "!pp m4/4 r:4 | a1:1 r:3 |",
                    "timpani": "!pp m4/4 r:4 | a1:1 r:3 |", "basses": "!pp m4/4 a1:4~ | a1:1 r:3 |"},
                   bpm=60, to=48)


def vehemence():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
