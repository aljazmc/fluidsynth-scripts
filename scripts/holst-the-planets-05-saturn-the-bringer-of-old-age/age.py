from orchestra import Orchestra

# Holst, The Planets, V. Saturn, the Bringer of Old Age. A from-memory
# arrangement for General MIDI orchestra: the two chords swaying like a slow
# clock, the basses climbing beneath them, the trombones' procession, the
# clanging bells at the climax and the calm C major close follow Holst, the
# notes are approximate.
SEED = 1919

PARTS = ("flutes", "clarinets", "bassoons", "horns", "trombones", "tuba", "timpani", "harp",
         "bells", "organ", "violins", "violas", "cellos", "basses")

# Adagio, 4/4. Two chords, back and forth, a crotchet each.
CLOCK = "m4/4 " + " ".join(["e4+a4+b4:1 d4+g4+a4 e4+a4+b4 d4+g4+a4 |"] * 8)
CLIMB = "m4/4 r:4 | e2:4 | f#2:4 | g2:4 | a2:4 | b2:4 | c3:4 | d3:4 |"

PROCESSION = ("m4/4 e3:2 f#3:1 g3:1 | a3:3 g3:1 | f#3:2 e3:1 d3:1 | e3:4 | "
              "g3:2 a3:1 b3:1 | c4:3 b3:1 | a3:2 g3:1 f#3:1 | b2:4 |")
PROCESSION_CHORDS = ("m4/4 e3+b3:4 | d3+a3:4 | d3+a3:4 | e3+b3:4 | "
                     "e3+b3:4 | e3+c4:4 | d3+a3:4 | b2+f#3:4 |")

# the bells: two notes a fourth apart, swinging heavily
BELLS = "m4/4 " + " ".join(["e5:1 b4:1 e5:1 b4:1 |", "e5:1 a4:1 e5:1 a4:1 |"] * 4)
CLIMAX = ("m4/4 e4+g4+b4+e5:4 | c4+e4+a4+c5:4 | d4+f#4+a4+d5:4 | b3+d#4+f#4+b4:4 | "
          "c4+e4+g4+c5:4 | a3+c4+e4+a4:4 | b3+d#4+f#4+b4:4~ | b3+d#4+f#4+b4:4 |")
CLIMAX_BASS = "m4/4 e2:4 | a2:4 | d2:4 | b1:4 | c2:4 | a1:4 | b1:4~ | b1:4 |"

PEACE = "m4/4 c4+e4+g4:4 | b3+e4+g4:4 | a3+c4+e4:4 | g3+c4+e4:4~ | g3+c4+e4:4 |"
PEACE_BASS = "m4/4 c3:4 | e3:4 | a2:4 | c3:4~ | c3:4 |"


def picture(orchestra):
    orchestra.play({"flutes": "!pp " + CLOCK, "harp": ("!pp " + CLOCK, -12),
                    "basses": "!pp " + CLIMB + " !<p"}, bpm=50, label="clock")
    orchestra.play({"flutes": "!pp " + CLOCK, "clarinets": ("!pp " + CLOCK, -12),
                    "trombones": "!p " + PROCESSION + " !<mf", "violas": "!pp " + PROCESSION_CHORDS,
                    "cellos": ("!pp " + PROCESSION_CHORDS, -12), "basses": ("!pp " + CLIMB, 0)},
                   bpm=50, label="procession")
    orchestra.play({"flutes": "!p " + CLOCK + " !<f", "clarinets": ("!p " + CLOCK, -12),
                    "horns": "!mf " + PROCESSION + " !<f", "trombones": ("!mf " + PROCESSION, -12),
                    "violins": ("!mp " + PROCESSION, 12), "violas": "!p " + PROCESSION_CHORDS + " !<f",
                    "cellos": ("!p " + PROCESSION_CHORDS, -12), "tuba": ("!p " + CLIMB, -12),
                    "basses": "!mp " + CLIMB}, bpm=54, to=60, label="growing")

    # the bells: the old man's terror
    orchestra.play({"bells": "!ff " + BELLS, "organ": "!f " + CLIMAX, "horns": "!ff " + CLIMAX,
                    "trombones": ("!ff " + CLIMAX, -12), "tuba": "!ff " + CLIMAX_BASS,
                    "violins": ("!ff " + CLIMAX, 12), "violas": "!ff " + CLIMAX,
                    "cellos": ("!ff " + CLIMAX_BASS, 12), "basses": "!ff " + CLIMAX_BASS,
                    "timpani": "!f m4/4 " + " ".join(["e2:1 b1:1 e2:1 b1:1 |"] * 8)},
                   bpm=60, to=48, label="bells")
    orchestra.rest(1.0)

    # and then calm: C major, with harp and organ
    orchestra.play({"violins": ("!pp " + PEACE + " !>ppp", 12), "violas": "!pp " + PEACE + " !>ppp",
                    "cellos": "!pp " + PEACE_BASS + " !>ppp", "basses": ("!pp " + PEACE_BASS, -12),
                    "organ": ("!pp " + PEACE_BASS + " !>n", -12),
                    "harp": "!p m4/4 " + " ".join(["c3:1/2 g3 c4 e4 g4 e4 c4 g3 |"] * 3)
                    + " c3:1/2 g3 c4 e4 g4 c5 e5 g5 | c6:4 |",
                    "flutes": "!pp m4/4 r:4 | r:4 | e5:2 d5:2 | c5:4~ | c5:4 |"},
                   bpm=44, to=36, label="peace")


def age():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render(tail=7.0)
