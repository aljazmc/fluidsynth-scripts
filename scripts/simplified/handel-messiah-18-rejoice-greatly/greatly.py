from orchestra import Orchestra

# Handel, Messiah, Part I, No. 18. Rejoice greatly, O daughter of Zion (air,
# soprano). A from-memory arrangement for General MIDI baroque orchestra, the
# soprano singing without words: the bright B-flat major Allegro with long
# coloratura runs on "rejoice", the gentler G minor middle "He is the
# righteous Saviour" and the da capo follow Handel, the notes are
# approximate.
SEED = 1758

PARTS = ("soprano", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Allegro, 4/4
RITORNELLO = ("m4/4 bb4:1/2 d5 f5 bb5 f5:1 d5:1 | eb5:1/4 f5 g5 f5 eb5 d5 c5 bb4 f5:2 | "
              "g5:1/4 a5 bb5 a5 g5 f5 eb5 d5 c5:1/4 d5 eb5 d5 c5 bb4 a4 g4 | f4:2 r:2 |")
BASS = "m4/4 bb2:1 d3:1 bb2:1 bb1:1 | c3:1 a2:1 bb2:1 d3:1 | eb3:1 c3:1 f3:1 f2:1 | bb2:2 r:2 |"
REJOICE = ("m4/4 f5:2 bb4:2 | r:1 d5:1/2 eb5:1/2 f5:1 bb5:1 | "
           "f5:1/4 g5 a5 bb5 a5 g5 f5 eb5 d5 eb5 f5 g5 f5 eb5 d5 c5 | "
           "bb4:1/4 c5 d5 eb5 d5 c5 bb4 a4 bb4:1 r:1 | "
           "d5:1/4 eb5 f5 g5 f5 eb5 d5 c5 eb5 f5 g5 a5 g5 f5 eb5 d5 | c5:2 f4:2 | "
           "bb4:1 c5:1/2 d5:1/2 c5:1 a4:1 | bb4:4 |")
REJOICE_BASS = "m4/4 bb2:4 | bb2:4 | bb2:2 f2:2 | bb2:4 | bb2:2 g2:2 | f2:4 | g2:1 eb2:1 f2:2 | bb1:4 |"
SAVIOUR = ("m4/4 d5:2 g5:1 f5:1 | eb5:2 d5:1 c5:1 | bb4:1 a4:1 g4:1 bb4:1 | a4:3 r:1 | "
           "c5:2 f5:1 eb5:1 | d5:2 c5:1 bb4:1 | a4:1 bb4:1 c5:1 a4:1 | g4:4 |")
SAVIOUR_BASS = "m4/4 g2:4 | c3:4 | g2:2 g2:2 | d3:4 | a2:4 | bb2:4 | c3:2 d3:2 | g2:4 |"


def chords(bass):
    triads = {"bb": "+d3+f3", "d": "+f3+a3", "c": "+eb3+g3", "eb": "+g3+bb3", "f": "+a2+c3", "g": "+bb2+d3", "a": "+c3+e3"}
    out = []
    for token in bass.split():
        if token[0] in "abcdefg":
            note, length = token.split(":")
            out.append(note + triads[note.rstrip("0123456789")] + ":" + length)
        else:
            out.append(token)
    return " ".join(out)


def picture(orchestra):
    def ritornello(dynamic):
        orchestra.play({"violins": f"!{dynamic} " + RITORNELLO, "violins 2": (f"!{dynamic} " + RITORNELLO, -12),
                        "violas": ("!mf " + BASS, 12), "cellos": f"!{dynamic} " + BASS, "basses": (f"!{dynamic} " + BASS, -12),
                        "harpsichord": "!mf " + chords(BASS)}, bpm=120, label="ritornello")

    def rejoice():
        orchestra.play({"soprano": "!f " + REJOICE, "violins": ("!p " + REJOICE_BASS, 24), "violas": ("!p " + REJOICE_BASS, 12),
                        "cellos": "!p " + REJOICE_BASS, "basses": ("!p " + REJOICE_BASS, -12),
                        "harpsichord": "!p " + chords(REJOICE_BASS)}, bpm=120, label="rejoice")

    ritornello("f")
    rejoice()
    ritornello("f")
    orchestra.play({"soprano": "!mp " + SAVIOUR, "violins": ("!pp " + SAVIOUR_BASS, 24), "violas": ("!pp " + SAVIOUR_BASS, 12),
                    "cellos": "!pp " + SAVIOUR_BASS, "basses": ("!pp " + SAVIOUR_BASS, -12),
                    "harpsichord": "!pp " + chords(SAVIOUR_BASS)}, bpm=88, label="righteous saviour")
    rejoice()
    ritornello("f")


def greatly():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
