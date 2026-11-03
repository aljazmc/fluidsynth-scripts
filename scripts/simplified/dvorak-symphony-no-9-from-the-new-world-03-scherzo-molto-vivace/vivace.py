from orchestra import Orchestra

# Dvořák, Symphony No. 9 "From the New World", III. Scherzo: Molto vivace. A
# from-memory arrangement for General MIDI orchestra: the drumming E minor
# scherzo tossed between the woodwinds, the gentler second strain, the C major
# trio's lilting dance and the coda in which the first movement's horn theme
# returns follow Dvořák, the notes are approximate.
SEED = 1895

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "timpani",
         "violins", "violins 2", "violas", "cellos", "basses", "percussion")

# Molto vivace, 3/4, one beat to the bar
DANCE = ("m3/4 b4:1 e5:1/2 b4:1/2 e5:1 | g5:1 f#5:1 e5:1 | d5:1 b4:1/2 d5:1/2 e5:1 | b4:3 | "
         "b4:1 e5:1/2 b4:1/2 e5:1 | g5:1 a5:1 b5:1 | a5:1 g5:1 f#5:1 | e5:3 |")
DRIVE = "m3/4 " + " ".join(f"{b}:1' {c}:1' {c}:1' |" for b, c in (
    ("e2", "e3+b3"), ("e2", "e3+b3"), ("b1", "d3+a3"), ("e2", "e3+b3"),
    ("e2", "e3+b3"), ("c2", "e3+g3"), ("b1", "d#3+a3"), ("e2", "e3+b3")))
DRUMS = "m3/4 " + " ".join(["e2:1 r:1 b1:1 |"] * 8)

GENTLE = ("m3/4 g4:2 a4:1 | b4:2 a4:1 | g4:1 f#4:1 e4:1 | d4:3 | g4:2 a4:1 | b4:2 d5:1 | c5:1 b4:1 a4:1 | g4:3 |")
GENTLE_BASS = "m3/4 " + " ".join(f"{b}:3 |" for b in ("g2", "g2", "c3", "d2", "g2", "g2", "d2", "g2"))

TRIO = ("m3/4 e5:2 d5:1 | c5:2 g4:1 | a4:1 b4:1 c5:1 | g4:3 | e5:2 f5:1 | g5:2 e5:1 | d5:1 c5:1 b4:1 | c5:3 |")
OOMPAH = "m3/4 " + " ".join(f"{b}:1' {c}:1' {c}:1' |" for b, c in (
    ("c2", "e3+g3"), ("c2", "e3+g3"), ("f2", "f3+a3"), ("c2", "e3+g3"),
    ("c2", "e3+g3"), ("c2", "e3+g3"), ("g1", "f3+g3"), ("c2", "e3+g3")))

HORN_RECALL = "m3/4 e3:3/2 g3:1/2 b3:1 | b3:1 g3:1 e3:1 | e3:3/2 g3:1/2 b3:1 | d4:3 |"


def scherzo(orchestra):
    orchestra.play({"flutes": "!f " + DANCE, "oboes": ("!f " + DANCE, -12), "violas": "!f " + DRIVE,
                    "cellos": "!f " + DRIVE, "basses": ("!f " + DRIVE, -12), "timpani": "!f " + DRUMS},
                   bpm=240, label="scherzo")
    orchestra.play({"violins": "!ff " + DANCE, "clarinets": ("!ff " + DANCE, -12), "flutes": ("!ff " + DANCE, 12),
                    "violins 2": ("!ff " + DANCE, -12), "violas": "!ff " + DRIVE, "cellos": "!ff " + DRIVE,
                    "basses": ("!ff " + DRIVE, -12), "horns": ("!f " + DRIVE, 12), "timpani": "!ff " + DRUMS,
                    "percussion": "!f m3/4 " + " ".join(["81:1 r:2 |"] * 8)}, bpm=240)
    orchestra.play({"oboes": "!p " + GENTLE, "flutes": ("!p " + GENTLE, 12), "violas": "!pp " + GENTLE_BASS.replace("2:", "3:"),
                    "cellos": "!pp " + GENTLE_BASS, "basses": ("!pp " + GENTLE_BASS, -12)}, bpm=216, label="gentle")
    orchestra.play({"violins": "!mf " + GENTLE, "clarinets": ("!mf " + GENTLE, -12), "cellos": "!p " + GENTLE_BASS,
                    "basses": ("!p " + GENTLE_BASS, -12)}, bpm=216, to=240)
    orchestra.play({"flutes": "!ff " + DANCE, "violins": "!ff " + DANCE, "oboes": "!ff " + DANCE,
                    "violins 2": ("!ff " + DANCE, -12), "violas": "!ff " + DRIVE, "cellos": "!ff " + DRIVE,
                    "basses": ("!ff " + DRIVE, -12), "trumpets": ("!f " + DANCE, -12), "timpani": "!ff " + DRUMS},
                   bpm=240)


def picture(orchestra):
    scherzo(orchestra)
    for dynamic in ("p", "mf"):
        orchestra.play({"flutes": f"!{dynamic} " + TRIO, "oboes": (f"!{dynamic} " + TRIO, -12),
                        "violins 2": "!p " + OOMPAH, "violas": "!p " + OOMPAH, "basses": ("!p " + OOMPAH, -12),
                        "percussion": "!p m3/4 " + " ".join(["81:1 r:2 |"] * 8)}, bpm=200, label="trio")
    orchestra.play({"violins": "!f " + TRIO, "clarinets": ("!f " + TRIO, -12), "horns": ("!mf " + OOMPAH, 12),
                    "violas": "!f " + OOMPAH, "cellos": "!f " + OOMPAH, "basses": ("!f " + OOMPAH, -12)},
                   bpm=200, to=240)
    scherzo(orchestra)
    # coda: the first movement's horn theme looms up
    orchestra.play({"horns": "!ff " + HORN_RECALL, "trombones": ("!f " + HORN_RECALL, -12),
                    "violins": "!f m3/4 " + " ".join(["e5:1/2 f#5 g5 f#5 e5 d#5 |"] * 4),
                    "cellos": "!f m3/4 e2:3 | e2:3 | e2:3 | g2:3 |", "basses": "!f m3/4 e1:3 | e1:3 | e1:3 | g1:3 |",
                    "timpani": "!f m3/4 " + " ".join(["e2:1 e2 e2 |"] * 4)}, bpm=200, label="coda")
    end = "m3/4 X:1^ r:2 | X:1^ r:2 | X:3^ |"
    voicing = {"violins": "e5+g5+b5", "violins 2": "b4", "violas": "e4", "cellos": "e3", "basses": "e2",
               "flutes": "e6", "oboes": "b5", "clarinets": "g4", "bassoons": "e2", "horns": "e4+b4",
               "trumpets": "e5", "trombones": "e3+b3", "timpani": "e2", "percussion": "49"}
    orchestra.play({p: "!fff " + end.replace("X", v) for p, v in voicing.items()}, bpm=200, to=150, label="end")


def vivace():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
