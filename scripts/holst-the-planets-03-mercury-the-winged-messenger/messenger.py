from orchestra import Orchestra

# Holst, The Planets, III. Mercury, the Winged Messenger. A from-memory
# arrangement for General MIDI orchestra: the 6/8 Vivace, the flickering
# figures in two keys at once (B-flat and E), the little tune for solo violin
# and celesta and the vanishing end follow Holst, the notes are approximate.
SEED = 1916

PARTS = ("flutes", "oboes", "clarinets", "bassoons", "horns", "celesta", "glockenspiel", "harp",
         "solo violin", "violins", "violins 2", "violas", "cellos", "pizzicato")

# Vivace, 6/8 (three crotchet beats a bar). B-flat bars answered by E bars.
FLICK_B = "bb4:1/2' d5' f5' bb5' f5' d5' |"
FLICK_E = "e5:1/2' g#5' b5' e6' b5' g#5' |"
REST = "r:3 |"


def flicker(bars, first):
    """Alternate bars of figures with rests, starting on figures if first."""
    return "m6/8 " + " ".join((FLICK_B if i % 4 < 2 else FLICK_E) if (i % 2 == 0) == first else REST
                              for i in range(bars))


PLUCK = "m6/8 " + " ".join(["bb2:1/2' r:5/2 |", "e2:1/2' r:5/2 |"] * 4)

TUNE = ("m6/8 e5:1 f#5:1/2 g#5:1 e5:1/2 | b5:3/2 g#5:3/2 | a5:1 g#5:1/2 f#5:1 e5:1/2 | f#5:3 | "
        "e5:1 f#5:1/2 g#5:1 b5:1/2 | c#6:3/2 b5:3/2 | a5:1 g#5:1/2 f#5:1 g#5:1/2 | e5:3 |")
TUNE_CHORDS = ("m6/8 g#3+b3+e4:3 | g#3+b3+e4:3 | a3+c#4+e4:3 | a3+b3+d#4:3 | "
               "g#3+b3+e4:3 | a3+c#4+e4:3 | f#3+a3+d#4:3 | g#3+b3+e4:3 |")
TUNE_BASS = "m6/8 e2:1/2' r:5/2 | e2:1/2' r:5/2 | a2:1/2' r:5/2 | b2:1/2' r:5/2 | e2:1/2' r:5/2 | a2:1/2' r:5/2 | b2:1/2' r:5/2 | e2:1/2' r:5/2 |"


def picture(orchestra):
    for dynamic in ("p", "mp"):
        orchestra.play({"flutes": f"!{dynamic} " + flicker(8, True),
                        "clarinets": f"!{dynamic} " + flicker(8, False),
                        "pizzicato": "!p " + PLUCK}, bpm=200, label="flicker")
    orchestra.play({"celesta": "!mp " + flicker(8, True), "oboes": "!mp " + flicker(8, False),
                    "violins": ("!p " + flicker(8, False), 12), "pizzicato": "!mp " + PLUCK},
                   bpm=200)

    # the tune: solo violin, then celesta and glockenspiel a tritone away
    orchestra.play({"solo violin": "!mp " + TUNE, "violas": "!pp " + TUNE_CHORDS,
                    "pizzicato": "!p " + TUNE_BASS, "harp": ("!pp " + TUNE_BASS, 12)},
                   bpm=200, label="tune")
    orchestra.play({"celesta": ("!mf " + TUNE, -6), "glockenspiel": ("!p " + TUNE, 6),
                    "violins 2": ("!pp " + TUNE_CHORDS, -6), "pizzicato": ("!p " + TUNE_BASS, -6),
                    "flutes": "!pp " + flicker(8, True)}, bpm=200)
    orchestra.play({"violins": ("!mf " + TUNE, 12), "flutes": ("!mf " + TUNE, 12),
                    "horns": ("!p " + TUNE_CHORDS, 0), "cellos": ("!p " + TUNE_CHORDS, -12),
                    "pizzicato": "!mf " + TUNE_BASS, "harp": ("!p " + TUNE_BASS, 12),
                    "bassoons": ("!p " + TUNE_BASS, 0)}, bpm=200, label="tune, tutti")

    # the figures come back, rise, and are gone
    orchestra.play({"flutes": "!mf " + flicker(8, True) + " !<f",
                    "clarinets": "!mf " + flicker(8, False) + " !<f",
                    "celesta": ("!mf " + flicker(8, False), 12), "pizzicato": "!mf " + PLUCK,
                    "violins": ("!mf " + flicker(8, True), 12)}, bpm=200, label="return")
    orchestra.play({"flutes": "!p " + flicker(4, True) + " !>pp", "celesta": ("!p " + flicker(4, False), 12),
                    "pizzicato": "!pp m6/8 bb2:1/2' r:5/2 | e2:1/2' r:5/2 | bb2:1/2' r:5/2 | e2:1/2' r:5/2 |"},
                   bpm=200)
    orchestra.play({"celesta": "!pp m6/8 bb5:1/2' d6' f6' bb6:1/2' r:1 | e6:1/2' r:5/2 |",
                    "flutes": "!pp m6/8 r:3 | e6:1/2' r:5/2 |",
                    "harp": "!pp m6/8 r:3 | e3+b3:1/2 r:5/2 |"}, bpm=200, label="gone")


def messenger():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render(tail=4.0)
