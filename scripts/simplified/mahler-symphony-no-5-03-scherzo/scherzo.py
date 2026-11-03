from orchestra import Orchestra

# Mahler, Symphony No. 5, Part II, 3. Scherzo. Kräftig, nicht zu schnell. A
# from-memory arrangement for General MIDI orchestra: the solo horn's call,
# the robust D major ländler, the swaying waltz, the plucked pizzicato
# section, the horn answering its own distant echo and the headlong close
# follow Mahler, the notes are approximate.
SEED = 1904

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "timpani",
         "harp", "violins", "violins 2", "violas", "cellos", "basses", "pizzicato", "percussion")

# 3/4
HORN_CALL = "m3/4 a3:1 d4:1/2 e4:1/2 f#4:1 | a4:2 f#4:1 | d4:1 e4:1/2 f#4:1/2 g4:1 | a4:3 |"
LANDLER = ("m3/4 d5:1/2 e5:1/2 f#5:1 a5:1 | f#5:1 d5:1 a4:1 | b4:1/2 c#5:1/2 d5:1 g5:1 | e5:3 | "
           "e5:1/2 f#5:1/2 g5:1 b5:1 | a5:1 f#5:1 d5:1 | e5:1 c#5:1/2 d5:1/2 e5:1 | d5:3 |")
STOMP = "m3/4 " + " ".join(f"{b}:1' {c}:1' {c}:1' |" for b, c in (
    ("d2", "f#3+a3+d4"), ("d2", "f#3+a3+d4"), ("g1", "g3+b3+d4"), ("a1", "g3+a3+c#4"),
    ("a1", "g3+a3+c#4"), ("d2", "f#3+a3+d4"), ("a1", "g3+a3+c#4"), ("d2", "f#3+a3+d4")))
WALTZ = ("m3/4 f#5:2 e5:1 | d5:2 a4:1 | b4:1 d5:1 g5:1 | f#5:2 e5:1 | e5:2 d5:1 | c#5:2 a4:1 | "
         "b4:1 c#5:1 d5:1 | d5:3 |")
PLUCK = ("m3/4 a4:1/2 r:1/2 d5:1/2 r:1/2 f#5:1/2 r:1/2 | e5:1/2 r:1/2 c#5:1/2 r:1/2 a4:1/2 r:1/2 | "
         "b4:1/2 r:1/2 g4:1/2 r:1/2 d5:1/2 r:1/2 | a4:1/2 r:5/2 |")


def landler(orchestra, dynamic, **kwargs):
    orchestra.play({"violins": f"!{dynamic} " + LANDLER, "clarinets": (f"!{dynamic} " + LANDLER, -12),
                    "violas": f"!{dynamic} " + STOMP, "cellos": f"!{dynamic} " + STOMP,
                    "basses": (f"!{dynamic} " + STOMP, -12), "horns": (f"!{dynamic} " + LANDLER, -12),
                    "timpani": f"!{dynamic} m3/4 " + " ".join(["d2:1 r:2 |", "a1:1 r:2 |"] * 4)}, **kwargs)


def picture(orchestra):
    orchestra.play({"horns": "!f " + HORN_CALL}, bpm=150, gap=0.3, label="horn call")
    landler(orchestra, "f", bpm=150, label="ländler")
    landler(orchestra, "ff", bpm=150)
    orchestra.play({"violins": "!p " + WALTZ, "flutes": ("!p " + WALTZ, 12), "harp": "!pp " + STOMP,
                    "violas": "!pp " + STOMP, "basses": ("!pp " + STOMP, -12)}, bpm=138, label="waltz")
    orchestra.play({"violins": "!mf " + WALTZ, "oboes": ("!mp " + WALTZ, 0), "violins 2": ("!mp " + WALTZ, -12),
                    "violas": "!p " + STOMP, "cellos": "!p " + STOMP, "basses": ("!p " + STOMP, -12)},
                   bpm=138, to=150)
    orchestra.play({"pizzicato": "!mf " + PLUCK + " " + PLUCK[5:], "harp": ("!p " + PLUCK + " " + PLUCK[5:], -12),
                    "clarinets": "!p m3/4 r:3 | r:3 | r:3 | r:3 | d5:3 | c#5:3 | b4:3 | a4:3 |"},
                   bpm=150, label="pizzicato")
    # the horn and its echo across the hills
    orchestra.play({"horns": "!f " + HORN_CALL, "basses": "!pp m3/4 d2:3 | d2:3 | g1:3 | a1:3 |"}, bpm=120, gap=0.4,
                   label="horn")
    orchestra.play({"horns": ("!pp " + HORN_CALL, 0)}, bpm=120, gap=0.6, label="echo")
    landler(orchestra, "ff", bpm=150, label="ländler again")
    orchestra.play({"violins": "!ff " + WALTZ, "flutes": ("!ff " + WALTZ, 12), "trumpets": ("!f " + WALTZ, -12),
                    "violas": "!ff " + STOMP, "cellos": "!ff " + STOMP, "basses": ("!ff " + STOMP, -12),
                    "trombones": ("!f " + STOMP, -12)}, bpm=150, to=176)
    end = "m3/4 X:1^ r:1 X:1^ | X:3^ |"
    voicing = {"violins": "d5+f#5+a5", "violins 2": "a4", "violas": "f#4", "cellos": "d3", "basses": "d2",
               "flutes": "d6", "oboes": "a5", "clarinets": "f#4", "bassoons": "d2", "horns": "d4+a4",
               "trumpets": "d5", "trombones": "d3+a3", "timpani": "d2", "harp": "d2+a2+d3", "percussion": "49+36"}
    orchestra.play({p: "!fff " + end.replace("X", v) for p, v in voicing.items()}, bpm=176, label="end")


def scherzo():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
