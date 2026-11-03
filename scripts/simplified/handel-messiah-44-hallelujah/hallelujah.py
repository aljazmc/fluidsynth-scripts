from orchestra import Orchestra

# Handel, Messiah, Part II, No. 44. Hallelujah (chorus). A from-memory
# arrangement for General MIDI baroque orchestra, the choir singing without
# words: the D major "Hallelujah" shouts, the unison "For the Lord God
# omnipotent reigneth", the hushed "The kingdom of this world", the fugal
# "And he shall reign for ever and ever", the sopranos climbing on "King of
# Kings and Lord of Lords" over the others' "for ever, Hallelujah", and the
# great pause before the last Hallelujah follow Handel; the main motifs are
# close, the rest approximate.
SEED = 1784

PARTS = ("choir", "oboes", "bassoons", "trumpets", "timpani", "harpsichord", "organ",
         "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
H = {"s": "m4/4 d5:1 a4:3/4 b4:1/4 a4:1 r:1 | d5:1 a4:3/4 b4:1/4 a4:1 r:1 | "
          "a4:1/2 b4:1/4 a4:1/4 d5:1/2 e5:1/4 d5:1/4 f#5:1/2 g5:1/4 f#5:1/4 e5:1 | d5:2 r:2 |",
     "a": "m4/4 a4:1 f#4:3/4 g4:1/4 f#4:1 r:1 | a4:1 f#4:3/4 g4:1/4 f#4:1 r:1 | "
          "f#4:1/2 g4:1/4 f#4:1/4 a4:1/2 a4:1/4 a4:1/4 a4:1/2 b4:1/4 a4:1/4 a4:1 | a4:2 r:2 |",
     "t": "m4/4 f#4:1 d4:3/4 d4:1/4 d4:1 r:1 | f#4:1 d4:3/4 d4:1/4 d4:1 r:1 | "
          "d4:1/2 d4:1/4 d4:1/4 f#4:1/2 e4:1/4 f#4:1/4 d4:1/2 d4:1/4 d4:1/4 c#4:1 | d4:2 r:2 |",
     "b": "m4/4 d3:1 d3:3/4 g2:1/4 d3:1 r:1 | d3:1 d3:3/4 g2:1/4 d3:1 r:1 | "
          "d3:1/2 g2:1/4 d3:1/4 f#2:1/2 c#3:1/4 d3:1/4 b2:1/2 g2:1/4 a2:1/4 a2:1 | d2:2 r:2 |",
     "timpani": "m4/4 d3:1 a2:1 d3:1 r:1 | d3:1 a2:1 d3:1 r:1 | d3:1 a2:1 d3:1 a2:1 | d3:2 r:2 |"}
OMNIPOTENT = "m4/4 a4:1 a4:1/2 a4:1/2 a4:1 a4:1/2 a4:1/2 | d5:3/2 c#5:1/2 b4:1 a4:1 |"
SHOUT = {"s": "m4/4 d5:1 a4:3/4 b4:1/4 a4:1 r:1 | d5:1 a4:3/4 b4:1/4 a4:1 r:1 |",
         "a": "m4/4 a4:1 f#4:3/4 g4:1/4 f#4:1 r:1 | a4:1 f#4:3/4 g4:1/4 f#4:1 r:1 |",
         "t": "m4/4 f#4:1 d4:3/4 d4:1/4 d4:1 r:1 | f#4:1 d4:3/4 d4:1/4 d4:1 r:1 |",
         "b": "m4/4 d3:1 d3:3/4 g2:1/4 d3:1 r:1 | d3:1 d3:3/4 g2:1/4 d3:1 r:1 |",
         "timpani": "m4/4 d3:1 a2:1 d3:1 r:1 | d3:1 a2:1 d3:1 r:1 |"}
KINGDOM = {"s": "m4/4 a4:2 b4:1 a4:1 | g4:2 f#4:2 | e4:1 f#4:1 g4:1 e4:1 | f#4:2 e4:2 |",
           "a": "m4/4 f#4:2 g4:1 f#4:1 | e4:2 d4:2 | c#4:1 d4:1 e4:1 c#4:1 | d4:2 c#4:2 |",
           "t": "m4/4 d4:2 d4:1 d4:1 | b3:2 a3:2 | a3:2 a3:2 | a3:2 a3:2 |",
           "b": "m4/4 d3:2 g2:1 d3:1 | e2:2 f#2:2 | a2:2 c#3:2 | d3:2 a2:2 |"}
REIGN = "m4/4 a3:1 a3:1/2 a3:1/2 d4:1 c#4:1 | b3:1/2 c#4:1/2 d4:1 e4:1 f#4:1 | e4:1/2 d4:1/2 c#4:1 d4:2 |"
FOREVER = "m4/4 r:2 a4:1 a4:1 | d5:1 a4:3/4 b4:1/4 a4:1 r:1 |"


def chorus(orchestra, voices, dynamic, label, **kwargs):
    orchestra.play({"choir": [f"!{dynamic} " + voices[v] for v in "satb"], "violins": f"!{dynamic} " + voices["s"],
                    "oboes": f"!{dynamic} " + voices["s"], "violins 2": f"!{dynamic} " + voices["a"],
                    "violas": f"!{dynamic} " + voices["t"], "cellos": f"!{dynamic} " + voices["b"],
                    "basses": (f"!{dynamic} " + voices["b"], -12), "bassoons": f"!{dynamic} " + voices["b"],
                    "trumpets": f"!{dynamic} " + voices["s"], "organ": (f"!mf " + voices["t"], 0),
                    **({"timpani": f"!{dynamic} " + voices["timpani"]} if "timpani" in voices else {})},
                   label=label, **kwargs)


def unison(orchestra, text, dynamic, label):
    orchestra.play({"choir": [(f"!{dynamic} " + text, 0), (f"!{dynamic} " + text, 0), (f"!{dynamic} " + text, -12),
                              (f"!{dynamic} " + text, -24)], "violins": f"!{dynamic} " + text,
                    "violins 2": (f"!{dynamic} " + text, -12), "violas": (f"!{dynamic} " + text, -12),
                    "cellos": (f"!{dynamic} " + text, -24), "basses": (f"!{dynamic} " + text, -36)}, bpm=100, label=label)


def picture(orchestra):
    orchestra.play({"violins": "!f " + SHOUT["s"], "violins 2": "!f " + SHOUT["a"], "violas": "!f " + SHOUT["t"],
                    "cellos": "!f " + SHOUT["b"], "basses": ("!f " + SHOUT["b"], -12)}, bpm=100, label="introduction")
    chorus(orchestra, H, "f", "hallelujah", bpm=100)
    for _ in range(2):
        unison(orchestra, OMNIPOTENT, "f", "for the Lord God omnipotent reigneth")
        chorus(orchestra, SHOUT, "ff", "hallelujah", bpm=100)
    chorus(orchestra, KINGDOM, "p", "the kingdom of this world", bpm=96)
    # and he shall reign: a fugato from the basses up
    for i, (shift, part) in enumerate(((-12, "cellos"), (0, "violas"), (5, "violins 2"), (12, "violins"))):
        parts = {"choir": [("!f " + REIGN, s) for s, _ in ((-12, 0), (0, 0), (5, 0), (12, 0))[:i + 1]],
                 part: ("!f " + REIGN, shift), "harpsichord": "!mf m4/4 d3+f#3+a3:4 | g2+b2+d3:4 | a2+c#3+e3:2 d3+f#3+a3:2 |"}
        if i == 0:
            parts["basses"] = ("!f " + REIGN, -24)
        orchestra.play(parts, bpm=100, label="and he shall reign")
    # King of Kings: the sopranos climb on long notes, the others answer
    for top in ("d5", "e5", "f#5", "g5", "a5"):
        king = f"m4/4 {top}:4 | {top}:4 |"
        orchestra.play({"choir": ["!ff " + king, "!f " + FOREVER, ("!f " + FOREVER, -12), ("!f " + FOREVER, -24)],
                        "violins": "!ff " + king, "trumpets": "!ff " + king, "oboes": "!ff " + king,
                        "violins 2": "!f " + FOREVER, "violas": ("!f " + FOREVER, -12), "cellos": ("!f " + FOREVER, -24),
                        "basses": ("!f " + FOREVER, -36), "timpani": "!f m4/4 d3:1 a2:1 d3:1 a2:1 | d3:1 a2:1 d3:1 r:1 |"},
                       bpm=100, label=f"King of Kings on {top}")
    chorus(orchestra, H, "ff", "hallelujah", bpm=100)
    chorus(orchestra, SHOUT, "ff", "hallelujah", bpm=100, gap=1.2)
    # the great pause, then the last Hallelujah, Adagio
    final = {"s": "m4/4 d5:2 e5:2 | d5:4 |", "a": "m4/4 a4:2 a4:2 | a4:4 |", "t": "m4/4 f#4:2 g4:2 | f#4:4 |",
             "b": "m4/4 d3:2 a2:2 | d2:4 |", "timpani": "m4/4 d3:2 a2:2 | d3:4 |"}
    chorus(orchestra, final, "fff", "Adagio", bpm=48, to=40)


def hallelujah():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=100)
    picture(orchestra)
    return orchestra.render()
