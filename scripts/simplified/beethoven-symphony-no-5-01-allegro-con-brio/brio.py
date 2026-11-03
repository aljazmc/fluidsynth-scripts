from orchestra import Orchestra

# Beethoven, Symphony No. 5 in C minor, Op. 67 (1808), I. Allegro con brio. A
# from-memory arrangement for General MIDI orchestra: the four-note motto and
# its fermatas, the motto passed up through the strings, the horn call into
# E-flat major, the lyrical second theme with the motto growling in the bass,
# the development's dying block chords, the oboe's little cadenza and the
# coda follow Beethoven, the details are approximate.
SEED = 1808

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "timpani",
         "violins", "violins 2", "violas", "cellos", "basses")

# 2/4, a minim to the bar
MOTTO = "m2/4 r:1/2 g4:1/2 g4 g4 | eb4:2~ | eb4:2 | r:1/2 f4:1/2 f4 f4 | d4:2~ | d4:2~ | d4:2 |"

# the motto handed from second violins to violas to first violins
STRETTO_V2 = "m2/4 r:1/2 g4:1/2 g4 g4 | eb4:2 | r:2 | r:2 | r:2 | r:2 | r:1/2 g4:1/2 g4 g4 | c5:2 |"
STRETTO_VA = "m2/4 r:2 | r:1/2 ab3:1/2 ab3 ab3 | g3:2 | r:2 | r:2 | r:1/2 d4:1/2 d4 d4 | b3:2 | r:2 |"
STRETTO_V1 = "m2/4 r:2 | r:2 | r:1/2 eb5:1/2 eb5 eb5 | c5:2 | r:1/2 f5:1/2 f5 f5 | d5:2 | r:2 | r:1/2 g5:1/2 g5 g5 |"
STRETTO_BASS = "m2/4 c3:2~ | c3:2 | c3:2~ | c3:2 | b2:2~ | b2:2 | g2:2~ | g2:2 |"


def hammer(chords):
    """The motto's rhythm on a series of chords: three quavers, then a minim."""
    return "m2/4 " + " ".join(f"r:1/2 {a}:1/2 {a} {a} | {b}:2 |" for a, b in chords)


CLIMB = (("g4+b4+d5+f5", "g4+b4+d5+f5"), ("g4+c5+eb5", "f4+ab4+d5"), ("eb4+g4+c5", "d4+g4+b4"),
         ("g4+b4+d5+f5", "g4+b4+d5+f5"))

HORN_CALL = "m2/4 r:1/2 bb3:1/2 bb3 bb3 | eb4:2 | f4:2 | bb3:2 |"
SECOND = ("m2/4 g4:1 ab4:1 | bb4:2 | eb5:1 d5:1 | c5:2 | bb4:1 ab4:1 | g4:1 f4:1 | g4:1 ab4:1 | bb4:2 | "
          "c5:1 d5:1 | eb5:2 | g5:1 f5:1 | eb5:2 | d5:1 c5:1 | bb4:1 ab4:1 | g4:1 f4:1 | eb4:2 |")
GROWL = "m2/4 " + " ".join(["r:1/2 bb2:1/2 bb2 bb2 | eb2:2 |"] * 8)
SECOND_CHORDS = "m2/4 " + " ".join(f"{c}:2 |" for c in (
    "eb4+g4", "eb4+g4", "f4+ab4", "eb4+ab4", "d4+f4", "eb4+g4", "d4+f4", "d4+f4",
    "eb4+ab4", "eb4+g4", "eb4+bb4", "eb4+g4", "f4+ab4", "d4+f4", "d4+ab4", "eb4+g4"))
CODETTA = hammer((("bb4+eb5+g5", "bb4+eb5+g5"), ("bb4+d5+f5+ab5", "bb4+d5+f5+ab5"),
                  ("bb4+eb5+g5", "bb4+eb5+g5"))) + " eb4+g4+bb4+eb5:1^ r:1 | eb4+g4+bb4+eb5:1^ r:1 |"

# development: the block chords answering between winds and strings, dying away
BLOCKS_WINDS = "m2/4 " + " ".join(f"{c}:2 | r:2 |" for c in ("f4+ab4+c5", "e4+g4+bb4+db5", "f4+ab4+c5", "f#4+a4+c5+eb5"))
BLOCKS_STRINGS = "m2/4 " + " ".join(f"r:2 | {c}:2 |" for c in ("e4+g4+bb4+db5", "f4+ab4+c5", "f#4+a4+c5+eb5", "g4+b4+d5"))

OBOE_CADENZA = "g5:1 f5:1/2 eb5:1/2 d5:1/2 c5:1/2 b4:1/2 c5:1/2 d5:2"


def unison(text, dynamic):
    return {"violins": f"!{dynamic} " + text, "violins 2": f"!{dynamic} " + text,
            "violas": (f"!{dynamic} " + text, -12), "cellos": (f"!{dynamic} " + text, -12),
            "basses": (f"!{dynamic} " + text, -24), "clarinets": f"!{dynamic} " + text}


def exposition(orchestra, key=0, second_key=0):
    orchestra.play(unison(MOTTO, "ff"), bpm=216, shift=key, label="motto")
    orchestra.play({"violins 2": "!p " + STRETTO_V2 + " !<f", "violas": "!p " + STRETTO_VA + " !<f",
                    "violins": "!p " + STRETTO_V1 + " !<f", "cellos": "!p " + STRETTO_BASS + " !<f",
                    "basses": ("!p " + STRETTO_BASS, -12)}, bpm=216, shift=key, label="stretto")
    climb = hammer(CLIMB)
    orchestra.play({"violins": ("!ff " + climb, 12), "violins 2": "!ff " + climb, "flutes": ("!ff " + climb, 12),
                    "oboes": "!ff " + climb, "horns": ("!ff " + climb, -12), "trumpets": "!ff " + climb,
                    "violas": ("!ff " + climb, -12), "cellos": "!ff m2/4 " + " ".join(["g2:1/2 g2 g2 g2 | g2:2 |"] * 4),
                    "basses": "!ff m2/4 " + " ".join(["g1:1/2 g1 g1 g1 | g1:2 |"] * 4),
                    "timpani": "!ff m2/4 " + " ".join(["r:1/2 g2:1/2 g2 g2 | g2:2 |"] * 4)},
                   bpm=216, shift=key, gap=0.2, label="climb")
    orchestra.play({"horns": "!ff " + HORN_CALL}, bpm=216, shift=second_key, label="horn call")
    orchestra.play({"violins": "!p " + SECOND, "clarinets": ("!p " + SECOND, 0),
                    "violas": "!pp " + SECOND_CHORDS, "violins 2": "!pp " + SECOND_CHORDS,
                    "cellos": "!p " + GROWL, "basses": ("!p " + GROWL, -12)},
                   bpm=216, shift=second_key, label="second theme")
    orchestra.play({"violins": ("!ff " + CODETTA, 0), "violins 2": ("!ff " + CODETTA, -12),
                    "flutes": ("!ff " + CODETTA, 12), "oboes": "!ff " + CODETTA,
                    "clarinets": "!ff " + CODETTA, "horns": ("!ff " + CODETTA, -12),
                    "trumpets": "!ff " + CODETTA, "violas": ("!ff " + CODETTA, -12),
                    "cellos": ("!ff " + CODETTA, -24), "basses": ("!ff " + CODETTA, -36),
                    "timpani": "!ff m2/4 r:2 | eb2:2 | r:2 | bb1:2 | r:2 | eb2:2 | eb2:1^ r:1 | eb2:1^ r:1 |"},
                   bpm=216, shift=second_key, gap=0.3, label="codetta")


def picture(orchestra):
    exposition(orchestra, key=0, second_key=0)

    # development
    orchestra.play({**unison(MOTTO, "ff"), "horns": "!ff " + MOTTO}, bpm=216, shift=5, label="development")
    orchestra.play({"violins 2": "!f " + STRETTO_V2, "violas": "!f " + STRETTO_VA, "violins": "!f " + STRETTO_V1,
                    "cellos": "!f " + STRETTO_BASS, "basses": ("!f " + STRETTO_BASS, -12),
                    "bassoons": ("!f " + STRETTO_BASS, 0)}, bpm=216, shift=5)
    orchestra.play({"flutes": "!f " + BLOCKS_WINDS + " !>pp", "oboes": ("!f " + BLOCKS_WINDS, -12),
                    "clarinets": ("!f " + BLOCKS_WINDS, -12), "violins": "!f " + BLOCKS_STRINGS + " !>pp",
                    "violins 2": ("!f " + BLOCKS_STRINGS, -12), "violas": ("!f " + BLOCKS_STRINGS, -12)},
                   bpm=216, to=180, label="blocks")
    orchestra.play({"flutes": "!pp " + BLOCKS_WINDS, "violins": "!pp " + BLOCKS_STRINGS},
                   bpm=180, gap=0.2)

    # recapitulation, with the oboe's lament where the first fermata was
    orchestra.play(unison(MOTTO[:MOTTO.index("| r:1/2 f4")] + "|", "fff"), bpm=216, label="recapitulation")
    orchestra.play({"oboes": "!p " + OBOE_CADENZA}, bpm=60, to=40, gap=0.3, label="oboe")
    orchestra.play({"violins 2": "!p " + STRETTO_V2 + " !<f", "violas": "!p " + STRETTO_VA + " !<f",
                    "violins": "!p " + STRETTO_V1 + " !<f", "cellos": "!p " + STRETTO_BASS + " !<f",
                    "basses": ("!p " + STRETTO_BASS, -12)}, bpm=216)
    orchestra.play({"horns": "!ff " + HORN_CALL, "bassoons": "!ff " + HORN_CALL}, bpm=216, shift=-3)
    orchestra.play({"violins": "!p " + SECOND, "flutes": ("!p " + SECOND, 0), "violas": "!pp " + SECOND_CHORDS,
                    "violins 2": "!pp " + SECOND_CHORDS, "cellos": "!p " + GROWL, "basses": ("!p " + GROWL, -12)},
                   bpm=216, shift=-3, label="second theme in C")

    # coda: the motto, hammered, and the last chords in C minor
    orchestra.play({**unison(MOTTO, "fff"), "horns": "!fff " + MOTTO, "trumpets": "!fff " + MOTTO,
                    "timpani": "!fff m2/4 r:1/2 g2:1/2 g2 g2 | c2:2~ | c2:2 | r:1/2 g2:1/2 g2 g2 | g2:2~ | g2:2~ | g2:2 |"},
                   bpm=216, label="coda")
    end = "m2/4 r:1/2 X:1/2^ X X | Y:2^ | r:1/2 X:1/2^ X X | Y:2^ | Y:1^ r:1 | Y:1^ r:1 | Y:2^ |"
    voicing = {"violins": ("g4+b4+d5", "g4+c5+eb5"), "violins 2": ("d4+f4", "eb4+g4"),
               "violas": ("b3", "c4"), "cellos": ("g2", "c3"), "basses": ("g1", "c2"),
               "flutes": ("d5+f5", "eb5+g5"), "oboes": ("b4+d5", "c5+eb5"), "clarinets": ("d4+f4", "eb4+g4"),
               "bassoons": ("g2+g3", "c3+c4"), "horns": ("g3+d4", "c4+g4"), "trumpets": ("g4", "c5"),
               "timpani": ("g2", "c2")}
    orchestra.play({p: "!fff " + end.replace("X", a).replace("Y", b) for p, (a, b) in voicing.items()},
                   bpm=216, to=160, label="end")


def brio():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
