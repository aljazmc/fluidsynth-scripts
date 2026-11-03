from orchestra import Orchestra

# Beethoven, Symphony No. 5, II. Andante con moto. A from-memory arrangement
# for General MIDI orchestra: the double variations in A-flat major, the
# violas' and cellos' gentle theme, the second theme on clarinets and bassoons
# that bursts into C major with trumpets and drums, the theme varied in faster
# notes and the quiet close follow Beethoven, the notes are approximate.
SEED = 1807

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "trumpets", "timpani",
         "violins", "violins 2", "violas", "cellos", "basses")

# 3/8, a semiquaver is a quarter of a beat
THEME = ("m3/8 eb3:3/8 ab3:1/8 | c4:3/4 bb3:1/4 ab3:1/4 bb3:1/4 | c4:1/2 eb4:1/2 db4:1/2 | "
         "c4:3/4 bb3:1/4 ab3:1/4 g3:1/4 | ab3:1 r:1/4 eb3:1/4 | ab3:3/4 c4:1/4 eb4:1/4 ab4:1/4 | "
         "g4:1/2 f4:1/2 eb4:1/2 | db4:3/4 c4:1/4 bb3:1/4 db4:1/4 | c4:1 r:1/2 |")
THEME_BASS = ("m3/8 r:1/2 | ab2:3/2 | ab2:1/2 c3:1/2 bb2:1/2 | eb2:3/2 | ab2:1 r:1/2 | "
              "ab2:3/2 | eb2:3/2 | eb2:3/2 | ab2:1 r:1/2 |")
# the theme in semiquavers: each note broken into a little turn
FAST = ("m3/8 eb3:1/4 ab3:1/4 | c4:1/4 db4 c4 bb3 ab3 bb3 | c4:1/4 db4 eb4 f4 eb4 db4 | "
        "c4:1/4 db4 c4 bb3 ab3 g3 | ab3:1/4 bb3 ab3 g3 ab3 eb3 | ab3:1/4 bb3 c4 db4 eb4 ab4 | "
        "g4:1/4 ab4 f4 g4 eb4 f4 | db4:1/4 eb4 c4 db4 bb3 db4 | c4:1 r:1/2 |")

SECOND = ("m3/8 ab4:3/8 c5:1/8 eb5:1/2 db5:1/2 | c5:3/4 bb4:1/4 c5:1/2 | ab4:3/8 c5:1/8 eb5:1/2 ab5:1/2 | "
          "g5:3/2 |")
FANFARE = ("m3/8 g4:3/8 c5:1/8 e5:1/2 d5:1/2 | c5:3/4 b4:1/4 c5:1/2 | g5:3/8 e5:1/8 c5:1/2 g4:1/2 | c5:3/2 |")
FANFARE_BASS = "m3/8 c3:3/2 | g2:3/2 | c3:3/2 | c2+c3:3/2 |"
FANFARE_DRUMS = "m3/8 c3:1/2 r:1 | g2:1/2 r:1 | c3:1/2 g2:1/2 c3:1/2 | c3:1/2 r:1 |"


def theme(orchestra, dynamic, fast=False, minor=False, **kwargs):
    line = FAST if fast else THEME
    if minor:
        line = line.replace("c4", "cb4").replace("c3", "cb3")
    orchestra.play({"violas": f"!{dynamic} " + line, "cellos": f"!{dynamic} " + line,
                    "basses": (f"!{dynamic} " + THEME_BASS, -12), "violins 2": (f"!pp " + THEME_BASS, 12),
                    "bassoons": ("!pp " + THEME_BASS, 0)}, **kwargs)


def second(orchestra, dynamic):
    orchestra.play({"clarinets": f"!{dynamic} " + SECOND, "bassoons": (f"!{dynamic} " + SECOND, -12),
                    "violins": "!pp m3/8 ab3+c4:3/2 | eb3+g3:3/2 | ab3+c4:3/2 | g3+b3:3/2 |"},
                   bpm=50, label="second theme")
    orchestra.play({"trumpets": "!ff " + FANFARE, "horns": ("!ff " + FANFARE, -12),
                    "violins": ("!ff " + FANFARE, 12), "flutes": ("!ff " + FANFARE, 12),
                    "oboes": "!ff " + FANFARE, "cellos": "!ff " + FANFARE_BASS,
                    "basses": ("!ff " + FANFARE_BASS, -12), "timpani": "!ff " + FANFARE_DRUMS},
                   bpm=50, gap=0.4, label="C major")


def picture(orchestra):
    theme(orchestra, "p", bpm=50, label="theme")
    second(orchestra, "p")
    theme(orchestra, "p", fast=True, bpm=50, label="variation")
    second(orchestra, "mp")
    theme(orchestra, "p", fast=True, minor=True, bpm=48, label="minor variation")
    orchestra.play({"violins": ("!ff " + THEME, 12), "flutes": ("!ff " + THEME, 24),
                    "oboes": ("!f " + THEME, 12), "violas": "!ff " + THEME, "cellos": "!ff " + THEME,
                    "basses": ("!ff " + THEME_BASS, -12), "horns": ("!f " + THEME_BASS, 12),
                    "trumpets": ("!f m3/8 r:1/2 | ab4:3/2 | ab4:3/2 | eb4:3/2 | ab4:1 r:1/2 | ab4:3/2 | eb4:3/2 | eb4:3/2 | ab4:1 r:1/2 |", 0),
                    "timpani": "!f m3/8 r:1/2 | ab2:3/2 | ab2:3/2 | eb2:3/2 | ab2:1 r:1/2 | ab2:3/2 | eb2:3/2 | eb2:3/2 | ab2:1 r:1/2 |"},
                   bpm=52, label="tutti")
    # coda: più moto on the bassoon, then the last chords
    orchestra.play({"bassoons": "!p " + FAST, "violins": ("!pp " + THEME_BASS, 24)}, bpm=60, to=50, label="coda")
    orchestra.play({"violins": "!p " + THEME[:THEME.index("| ab3:3/4")] + "|",
                    "violas": ("!pp " + THEME_BASS[:THEME_BASS.index("| ab2:3/2 | eb2:3/2 | eb2")] + "|", 12),
                    "cellos": ("!pp " + THEME_BASS[:THEME_BASS.index("| ab2:3/2 | eb2:3/2 | eb2")] + "|", 0)},
                   bpm=48, to=40)
    end = "m3/8 X:1/2^ r:1 | X:3/2^ |"
    voicing = {"violins": "ab4+c5+eb5", "violins 2": "eb4+ab4", "violas": "c4", "cellos": "ab2", "basses": "ab1",
               "flutes": "ab5", "oboes": "c5+eb5", "clarinets": "ab4", "bassoons": "ab2+eb3", "horns": "eb4+ab4",
               "trumpets": "eb4", "timpani": "ab2"}
    orchestra.play({p: "!ff " + end.replace("X", v) for p, v in voicing.items()}, bpm=48, label="end")


def moto():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render()
