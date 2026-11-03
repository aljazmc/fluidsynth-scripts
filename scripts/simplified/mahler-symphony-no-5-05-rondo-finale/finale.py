from orchestra import Orchestra

# Mahler, Symphony No. 5, Part III, 5. Rondo-Finale. Allegro. A from-memory
# arrangement for General MIDI orchestra: the horn's opening call, the
# bassoon's and oboe's chirpy fragments, the busy fugal strings, the
# Adagietto's tune sped up, and the second movement's brass chorale returning
# in triumph to end in D major follow Mahler, the notes are approximate.
SEED = 1906

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba", "timpani",
         "harp", "violins", "violins 2", "violas", "cellos", "basses", "percussion")

# Allegro, 2/2 (four crotchets)
CALL = "m4/4 a3:4~ | a3:2 r:2 |"
CHIRP = "m4/4 d4:1/2 e4 f#4 g4 a4:1 r:1 | b3:1/2 c#4 d4 e4 f#4:1 r:1 |"
FUGUE = ("m4/4 d4:1/2 e4 f#4 g4 a4 b4 a4 g4 | f#4:1/2 g4 a4 f#4 d4:1 r:1 | "
         "a4:1/2 b4 c#5 d5 e5 f#5 e5 d5 | c#5:1/2 d5 e5 c#5 a4:1 r:1 |")
SPED = ("m4/4 a4:2 bb4:1/2 c5:1/2 d5:1 | c5:1 bb4:1/2 a4:1/2 g4:2 | g4:2 a4:1/2 bb4:1/2 c5:1 | "
        "bb4:1 a4:1/2 g4:1/2 f4:2 |")
CHORALE = ("m4/4 d4+f#4+a4+d5:2 e4+g4+b4+e5:2 | f#4+a4+d5+f#5:4 | g4+b4+d5+g5:2 f#4+a4+d5+f#5:2 | "
           "e4+a4+c#5+e5:4 | d4+g4+b4+d5:2 e4+a4+c#5+e5:2 | f#4+a4+d5+f#5:2 g4+b4+e5+g5:2 | "
           "a4+d5+f#5+a5:4~ | a4+d5+f#5+a5:4 |")
CHORALE_BASS = "m4/4 d2:2 e2:2 | d2:4 | g1:2 d2:2 | a1:4 | b1:2 a1:2 | d2:2 e2:2 | d2:4~ | d2:4 |"


def fugue(orchestra, dynamic, **kwargs):
    entries = [("cellos", -12), ("violas", 0), ("violins 2", 7), ("violins", 12)]
    for i in range(len(entries)):
        parts = {p: (f"!{dynamic} " + FUGUE, s) for p, s in entries[:i + 1]}
        parts["basses"] = (f"!{dynamic} m4/4 d2:2 a1:2 | d2:4 | a1:2 e2:2 | a1:4 |", 0)
        if i >= 2:
            parts["bassoons"] = (f"!{dynamic} " + FUGUE, -12)
        orchestra.play(parts, **kwargs)


def picture(orchestra):
    orchestra.play({"horns": "!p " + CALL, "basses": "!pp m4/4 a1:4~ | a1:2 r:2 |"}, bpm=132, label="call")
    orchestra.play({"bassoons": "!mp " + CHIRP, "oboes": ("!mp " + CHIRP, 12)}, bpm=132, gap=0.3, label="chirps")
    orchestra.play({"clarinets": ("!mp " + CHIRP, 12), "horns": ("!p " + CHIRP, 0)}, bpm=132, gap=0.3)
    fugue(orchestra, "mf", bpm=144, label="fugue")
    orchestra.play({"violins": "!mf " + SPED, "flutes": ("!mf " + SPED, 12), "violas": "!p m4/4 f3+a3:4 | e3+g3:4 | e3+g3:4 | f3+a3:4 |",
                    "cellos": "!p m4/4 f2:4 | c3:4 | c3:4 | f2:4 |", "harp": "!p m4/4 f2:1/2 c3 f3 a3 c4 a3 f3 c3 | c2:1/2 g2 c3 e3 g3 e3 c3 g2 | c2:1/2 g2 c3 e3 g3 e3 c3 g2 | f2:1/2 c3 f3 a3 c4 a3 f3 c3 |"},
                   bpm=144, label="adagietto, sped up")
    fugue(orchestra, "f", bpm=144, label="fugue again")
    orchestra.play({"violins": "!f " + SPED, "oboes": ("!f " + SPED, 12), "violins 2": ("!f " + SPED, -12),
                    "horns": "!f m4/4 f3+c4:4 | e3+c4:4 | e3+c4:4 | f3+c4:4 |", "cellos": "!f m4/4 f2:4 | c3:4 | c3:4 | f2:4 |"},
                   bpm=144, shift=2)
    fugue(orchestra, "ff", bpm=152, label="fugue, wilder")

    # the chorale, at last in triumph
    orchestra.play({"trumpets": "!fff " + CHORALE, "horns": ("!fff " + CHORALE, -12), "trombones": ("!fff " + CHORALE, -12),
                    "tuba": "!fff " + CHORALE_BASS, "violins": ("!ff m4/4 " + " ".join(["d5:1/4 e5 f#5 a5 d6 a5 f#5 e5 d5 e5 f#5 a5 d6 a5 f#5 e5 |"] * 8), 0),
                    "violins 2": "!ff " + CHORALE, "violas": ("!ff " + CHORALE, -12), "cellos": ("!ff " + CHORALE_BASS, 12),
                    "basses": "!fff " + CHORALE_BASS, "flutes": ("!ff " + CHORALE, 12), "oboes": "!ff " + CHORALE,
                    "clarinets": "!ff " + CHORALE, "harp": "!f m4/4 " + " ".join(["d3:1/4 a3 d4 f#4 a4 d5 f#5 a5 d6 a5 f#5 d5 a4 f#4 d4 a3 |"] * 8),
                    "timpani": "!fff m4/4 " + " ".join(["d2:1 a1:1 d2:1 a1:1 |"] * 8),
                    "percussion": "!ff m4/4 49:4 | r:4 | 49:4 | r:4 | 49:4 | r:4 | 49:4 | 49+36:4 |"},
                   bpm=76, to=66, label="chorale")
    # the dash to the end
    dash = "m4/4 " + " ".join(["d5:1/4 e5 f#5 g5 a5 b5 c#6 d6 a5 f#5 d5 a4 f#4 a4 d5 f#5 |"] * 2)
    orchestra.play({"violins": "!ff " + dash, "flutes": ("!ff " + dash, 12), "violins 2": ("!ff " + dash, -12),
                    "cellos": "!ff m4/4 d3:1 a2 d3 a2 | d3:1 a2 d3 a2 |", "basses": "!ff m4/4 d2:1 a1 d2 a1 | d2:1 a1 d2 a1 |",
                    "trumpets": "!ff m4/4 d5:2 a4:2 | d5:2 f#5:2 |", "timpani": "!ff m4/4 d2:1 a1 d2 a1 | d2:1 a1 d2 a1 |"},
                   bpm=168, to=184, label="dash")
    end = "m4/4 X:1^ r:1 X:1^ r:1 | X:1^ r:3 |"
    voicing = {"violins": "d5+f#5+a5+d6", "violins 2": "a4+d5", "violas": "f#4", "cellos": "d3", "basses": "d2",
               "flutes": "d6+f#6", "oboes": "a5", "clarinets": "f#4+a4", "bassoons": "d2+d3", "horns": "d4+f#4+a4",
               "trumpets": "d5+a5", "trombones": "d3+a3", "tuba": "d2", "timpani": "d2", "harp": "d2+a2+d3",
               "percussion": "49+36"}
    orchestra.play({p: "!fff " + end.replace("X", v) for p, v in voicing.items()}, bpm=184, label="end")


def finale():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
