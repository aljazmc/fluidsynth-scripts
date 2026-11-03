from orchestra import Orchestra

# Mahler, Symphony No. 5 (1902), Part I, 1. Trauermarsch (Funeral March). In
# gemessenem Schritt. Streng. Wie ein Kondukt. A from-memory arrangement for
# General MIDI orchestra: the lone trumpet's triplet call, the orchestra's
# crash, the grieving C-sharp minor march, the wild B-flat minor trio and the
# trumpet call fading into a last pizzicato follow Mahler, the notes are
# approximate.
SEED = 1902

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba", "timpani",
         "harp", "violins", "violins 2", "violas", "cellos", "basses", "percussion")

CALL = ("m4/4 c#5:1/3 c#5 c#5 | c#5:3 c#5:1/3 c#5 c#5 | c#5:3 c#5:1/3 c#5 c#5 | "
        "c#5:1 e5:1 g#5:1 c#6:1 | b5:2 a5:1 g#5:1 | f#5:2 e5:1 d#5:1 | e5:2 c#5:2 | c#5:4 |")
CRASH = "m4/4 X:1^ r:1 X:1^ r:1 | X:4^ |"
CRASH_VOICING = {"trumpets": "c#5+e5+g#5", "horns": "c#4+e4+g#4", "trombones": "c#3+g#3+c#4", "tuba": "c#2",
                 "violins": "c#5+e5+g#5", "violins 2": "g#4", "violas": "e4", "cellos": "c#3", "basses": "c#2",
                 "flutes": "c#6+e6", "oboes": "g#5", "clarinets": "e5", "bassoons": "c#2+c#3",
                 "timpani": "c#2", "percussion": "49+36"}

MARCH = ("m4/4 c#5:3/2 b4:1/2 a4:1 g#4:1 | f#4:3/2 g#4:1/2 a4:2 | g#4:3/2 f#4:1/2 e4:1 d#4:1 | c#4:4 | "
         "e5:3/2 d#5:1/2 c#5:1 b4:1 | a4:3/2 b4:1/2 c#5:2 | b4:3/2 a4:1/2 g#4:1 f#4:1 | g#4:4 |")
TREAD = "m4/4 " + " ".join(f"{b}:3/2 {f}:1/2 {b}:2 |" for b, f in (
    ("c#2", "g#1"), ("f#2", "c#2"), ("g#1", "d#2"), ("c#2", "g#1"),
    ("a1", "e2"), ("f#2", "c#2"), ("g#1", "d#2"), ("c#2", "g#1")))
MARCH_PAD = "m4/4 " + " ".join(f"{c}:4 |" for c in (
    "e3+g#3", "f#3+a3", "d#3+f#3+b#3", "e3+g#3", "e3+a3+c#4", "f#3+a3+c#4", "d#3+f#3+b#3", "e3+g#3+b#3"))

# Plötzlich schneller. Leidenschaftlich. Wild.
WILD = "m4/4 " + " ".join(f"{a}:1/4 {b} {c} {d} " * 4 + "|" for a, b, c, d in (
    ("bb4", "c5", "db5", "f5"), ("gb5", "f5", "db5", "c5"), ("bb4", "db5", "f5", "bb5"), ("a5", "gb5", "f5", "eb5"),
    ("db5", "f5", "bb5", "db6"), ("c6", "bb5", "a5", "gb5"), ("f5", "eb5", "db5", "c5"), ("bb4", "a4", "bb4", "f4")))
SHRIEK = "m4/4 bb5:2 db6:2 | c6:2 a5:2 | bb5:2 f6:2 | e6:4 | db6:2 bb5:2 | gb5:2 f5:2 | e5:2 f5:2 | bb4:4 |"
WILD_BASS = "m4/4 " + " ".join(f"{b}:1/2 {b} {b} {b} {b} {b} {b} {b} |" for b in
                               ("bb1", "gb1", "bb1", "f1", "bb1", "gb1", "f1", "bb1"))


def crash(orchestra, dynamic):
    orchestra.play({p: f"!{dynamic} " + CRASH.replace("X", v) for p, v in CRASH_VOICING.items()}, bpm=72, gap=0.3)


def procession(orchestra, dynamic, **kwargs):
    orchestra.play({"violins": f"!{dynamic} " + MARCH, "violins 2": (f"!{dynamic} " + MARCH, -12),
                    "violas": f"!{dynamic} " + MARCH_PAD, "cellos": f"!{dynamic} " + TREAD,
                    "basses": (f"!{dynamic} " + TREAD, -12), "clarinets": ("!p " + MARCH_PAD, 12),
                    "harp": f"!{dynamic} " + TREAD, "percussion": "!p m4/4 " + " ".join(["36:1 r:3 |"] * 8)}, **kwargs)


def picture(orchestra):
    orchestra.play({"trumpets": "!f " + CALL}, bpm=72, label="trumpet call")
    crash(orchestra, "fff")
    procession(orchestra, "p", bpm=66, label="march")
    procession(orchestra, "mf", bpm=66)
    orchestra.play({"trumpets": "!ff " + CALL, "horns": ("!f " + MARCH_PAD, 12), "cellos": "!f " + TREAD,
                    "basses": ("!f " + TREAD, -12), "timpani": "!f m4/4 " + " ".join(["c#2:1/3 c#2 c#2 c#2:3 |"] * 8)},
                   bpm=72, label="call again")
    crash(orchestra, "fff")

    # the trio: sudden, passionate, wild
    orchestra.play({"violins": "!ff " + WILD, "violins 2": ("!ff " + WILD, -12), "trumpets": "!ff " + SHRIEK,
                    "horns": ("!f " + SHRIEK, -12), "violas": ("!f " + WILD_BASS, 24), "cellos": ("!ff " + WILD_BASS, 12),
                    "basses": "!ff " + WILD_BASS, "trombones": ("!f " + WILD_BASS, 12),
                    "timpani": ("!ff " + WILD_BASS, 12)},
                   bpm=120, label="trio")
    orchestra.play({"violins": "!fff " + WILD, "flutes": ("!ff " + SHRIEK, 12), "oboes": "!ff " + SHRIEK,
                    "trumpets": "!fff " + SHRIEK, "violas": ("!ff " + WILD_BASS, 24), "cellos": ("!ff " + WILD_BASS, 12),
                    "basses": "!fff " + WILD_BASS, "percussion": "!ff m4/4 49:4 | r:4 | 49:4 | r:4 | 49:4 | r:4 | 49:4 | 52:4 |"},
                   bpm=120, to=72, label="trio climax")

    procession(orchestra, "p", bpm=66, label="march returns")
    # the call, far away, and the end
    orchestra.play({"trumpets": "!p " + CALL[:CALL.index("| c#5:1 e5")] + "|",
                    "basses": "!pp m4/4 r:1 | c#2:4 | c#2:4 |"}, bpm=66, label="distant call")
    orchestra.play({"flutes": "!pp m4/4 c#6:1/3 c#6 c#6 | c#6:4 |", "basses": "!pp m4/4 r:1 | c#2:4 |"},
                   bpm=60, to=50, gap=0.6)
    orchestra.play({"basses": "!f m4/4 c#2:1/2' r:7/2 |", "cellos": "!f m4/4 c#3:1/2' r:7/2 |"}, bpm=50, label="pizzicato")


def march():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
