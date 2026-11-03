from orchestra import Orchestra

# Holst, The Planets, IV. Jupiter, the Bringer of Jollity. A from-memory
# arrangement for General MIDI orchestra: the scurrying strings and the
# syncopated horn tune, a stamping 3/4 dance, the broad Andante maestoso hymn
# in E-flat (the tune later sung as "Thaxted") and the brilliant close follow
# Holst, the notes are approximate.
SEED = 1918

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba",
         "timpani", "glockenspiel", "violins", "violins 2", "violas", "cellos", "percussion")

# Allegro giocoso, 2/4
SCURRY = "m2/4 " + " ".join(["c5:1/4 d5 e5 d5 c5 d5 e5 g5 |", "a5:1/4 g5 e5 d5 c5 d5 e5 c5 |"] * 4)
HORN_TUNE = ("m2/4 r:1/2 g4:1/2 a4:1/2 c5:1/2 | d5:1 c5:1/2 a4:1/2 | c5:1/2 g4:1/2 a4:1 | g4:2 | "
             "r:1/2 e4:1/2 g4:1/2 a4:1/2 | c5:1 d5:1/2 e5:1/2 | d5:1/2 c5:1/2 a4:1/2 d5:1/2 | c5:2 |")
BOUNCE = "m2/4 " + " ".join((["c3:1/2' g2' c3' g2' |"] * 3 + ["g2:1/2' d3' g2' d3' |"]) * 2)

# a stamping dance in 3/4
DANCE = ("m3/4 e5:1/2 f5:1/2 g5:1 c6:1 | b5:1/2 a5:1/2 g5:1 e5:1 | "
         "f5:1/2 g5:1/2 a5:1 f5:1 | e5:1/2 d5:1/2 c5:2 |")
DANCE_BASS = "m3/4 c3:1' g2' g2' | c3' g2' g2' | f2' c3' c3' | g2' c3:2' |"
TAMBOURINE = "m3/4 " + " ".join(["54:1 54:1/2 54:1/2 54:1 |"] * 4)

# Andante maestoso, 3/4: the hymn, here in C and played in E-flat
HYMN = ("m3/4 e4:1/2 g4:1/2 | a4:3/2 c5:1/2 b4:1/2 g4:1/2 | c5:1/2 d5:1/2 c5:1 b4:1 | "
        "a4:1/2 b4:1/2 a4:1 g4:1 | e4:2 e4:1/2 g4:1/2 | a4:3/2 c5:1/2 b4:1/2 g4:1/2 | "
        "c5:1/2 d5:1/2 e5:1 e5:1 | e5:1 d5:1/2 c5:1/2 d5:1 | c5:3 |")
HYMN_INNER = ("m3/4 r:1 | f3+a3:3 | e3+g3:3 | e3+a3:3 | e3+g3:3 | f3+a3:3 | "
              "e3+g3:3 | d3+g3:3 | e3+g3:3 |")
HYMN_BASS = "m3/4 r:1 | f2:3 | c3:3 | a2:3 | c3:3 | f2:3 | c3:3 | g2:3 | c3:3 |"


def picture(orchestra):
    # the strings set off, the horns join in
    orchestra.play({"violins": "!f " + SCURRY, "violins 2": ("!f " + SCURRY, -12),
                    "violas": "!mf " + BOUNCE, "cellos": "!mf " + BOUNCE}, bpm=132, label="scurry")
    orchestra.play({"violins": "!f " + SCURRY, "violins 2": ("!f " + SCURRY, -12),
                    "horns": "!f " + HORN_TUNE, "violas": "!mf " + BOUNCE, "cellos": "!f " + BOUNCE,
                    "tuba": ("!mf " + BOUNCE, -12)}, bpm=132, label="horn tune")
    orchestra.play({"violins": "!ff " + SCURRY, "flutes": ("!f " + SCURRY, 12),
                    "trumpets": "!ff " + HORN_TUNE, "horns": ("!ff " + HORN_TUNE, -12),
                    "trombones": "!f " + BOUNCE, "cellos": "!ff " + BOUNCE, "tuba": ("!f " + BOUNCE, -12),
                    "timpani": "!f " + BOUNCE, "glockenspiel": ("!mf " + HORN_TUNE, 12)},
                   bpm=132, label="tutti")

    # the dance
    for dynamic, shift in (("f", 0), ("ff", 5)):
        orchestra.play({"violins": f"!{dynamic} " + DANCE, "oboes": f"!{dynamic} " + DANCE,
                        "clarinets": (f"!{dynamic} " + DANCE, -12), "horns": (f"!{dynamic} " + DANCE, -12),
                        "cellos": f"!{dynamic} " + DANCE_BASS, "bassoons": f"!{dynamic} " + DANCE_BASS,
                        "tuba": (f"!{dynamic} " + DANCE_BASS, -12), "percussion": "!mf " + TAMBOURINE},
                       bpm=152, shift=shift, label="dance")

    # the hymn, first in the strings and horns, then the whole orchestra
    orchestra.play({"violins": "!mf " + HYMN, "violins 2": ("!mf " + HYMN, -12),
                    "horns": ("!mp " + HYMN, -12), "violas": "!mp " + HYMN_INNER,
                    "cellos": "!mp " + HYMN_BASS}, bpm=72, shift=3, label="hymn")
    orchestra.play({"violins": ("!f " + HYMN + " !<ff", 12), "violins 2": "!f " + HYMN,
                    "flutes": ("!f " + HYMN, 12), "oboes": "!f " + HYMN, "clarinets": "!f " + HYMN,
                    "trumpets": "!f " + HYMN + " !<ff", "horns": ("!f " + HYMN_INNER, 12),
                    "trombones": "!f " + HYMN_INNER, "violas": "!f " + HYMN_INNER,
                    "cellos": "!f " + HYMN_BASS, "bassoons": "!f " + HYMN_BASS,
                    "tuba": ("!f " + HYMN_BASS, -12), "timpani": "!mf " + HYMN_BASS},
                   bpm=68, to=60, shift=3, label="hymn, tutti")

    # back to the start, and a brilliant end
    orchestra.play({"violins": "!ff " + SCURRY, "violins 2": ("!ff " + SCURRY, -12),
                    "flutes": ("!f " + SCURRY, 12), "trumpets": "!ff " + HORN_TUNE,
                    "horns": ("!ff " + HORN_TUNE, -12), "trombones": "!ff " + BOUNCE,
                    "cellos": "!ff " + BOUNCE, "tuba": ("!ff " + BOUNCE, -12), "timpani": "!ff " + BOUNCE,
                    "percussion": "!f m2/4 " + " ".join(["54:1/2 54 54 54 |"] * 8)},
                   bpm=132, to=144, label="return")
    end = "m2/4 X:1/2^ r:1/2 X:1/2^ r:1/2 | X:2^ |"
    chord = {"trumpets": "c5+e5+g5", "horns": "e4+g4+c5", "trombones": "c3+g3+c4", "tuba": "c2",
             "violins": "c6+e6+g6", "violins 2": "c5+g5", "violas": "e4+c5", "cellos": "c3+g3",
             "flutes": "c6+g6", "oboes": "e5+c6", "clarinets": "g4+c5", "bassoons": "c2+c3",
             "timpani": "c2", "glockenspiel": "c6+g6", "percussion": "49+36"}
    orchestra.play({part: "!fff " + end.replace("X", notes) for part, notes in chord.items()},
                   bpm=132, to=100, label="end")


def jollity():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
