from piano import Piece, pitch

# Beethoven, Piano Sonata No. 14 "Moonlight", III. Presto agitato. A
# from-memory piano arrangement: the sonata form, the surging arpeggios that
# crash into two sforzando chords, the G-sharp minor second theme over a
# rushing accompaniment, the repeated-chord closing and the coda follow
# Beethoven, the details are approximate.
SEED = 1803

MINOR = (0, 3, 7)
MAJOR = (0, 4, 7)
SEVENTH = (0, 4, 7, 10)


def surge(root, quality, bass):
    """One bar: a sixteenth rest, eleven rising chord tones, two crashes."""
    base, notes = pitch(root), []
    for k in range(11):
        octave, degree = divmod(k, len(quality))
        notes.append(base + 12 * octave + quality[degree])
    crash = "+".join(str(n) for n in notes[-3:])
    rh = "r:1/4 " + " ".join(f"{n}:1/4" for n in notes) + f" {crash}:1/2^' {crash}:1/2^' |"
    b = pitch(bass)
    lh = " ".join(f"{b}+{b + 12}:1/2'" for _ in range(8)) + " |"
    return rh, lh


def surges(*bars):
    pairs = [surge(*bar) for bar in bars]
    return "m4/4 " + " ".join(r for r, _ in pairs), "m4/4 " + " ".join(l for _, l in pairs)


FIRST = (("c#3", MINOR, "c#2"), ("c#3", MINOR, "b1"), ("a2", MAJOR, "a1"), ("g#2", SEVENTH, "g#1"),
         ("c#3", MINOR, "c#2"), ("f#2", MINOR, "f#1"), ("g#2", SEVENTH, "g#1"), ("c#3", MINOR, "c#2"))


def alberti(low, high, middle):
    return f"{low}:1/4 {high} {middle} {high} " * 4 + "|"


# second theme, G-sharp minor, over rushing sixteenths
SECOND = ("m4/4 d#5:3 d#5:1 | e5:2 d#5:1 c#5:1 | b4:2 a#4:2 | g#4:4 | "
          "d#5:3 d#5:1 | e5:2 f#5:1 e5:1 | d#5:2 c#5:1 a#4:1 | g#4:4 |")
SECOND_LH = "m4/4 " + " ".join(alberti(*c) for c in (
    ("g#2", "d#3", "b2"), ("c#3", "g#3", "e3"), ("d#2", "a#2", "f##2"), ("g#2", "d#3", "b2"),
    ("g#2", "d#3", "b2"), ("c#3", "g#3", "e3"), ("d#2", "a#2", "f##2"), ("g#2", "d#3", "b2")))

# closing: hammered chords
HAMMER = "m4/4 " + " ".join(f"{c}:1/2^ {c}:1/2 {c}:1/2 {c}:1/2 {c}:2^ |" for c in (
    "g#3+b3+d#4+g#4", "d#4+f##4+a#4+d#5", "g#3+b3+d#4+g#4", "d#4+f##4+a#4+d#5"))
HAMMER_LH = "m4/4 " + " ".join(f"{b}:1/2 {b} {b} {b} {b}:2 |" for b in ("g#1+g#2", "d#2+d#3", "g#1+g#2", "d#2+d#3"))


def exposition(piece):
    rh, lh = surges(*FIRST)
    piece.play("!p " + rh + " !<f", "!p " + lh + " !<f", bpm=160, pedal=None, label="first theme")
    piece.play("!f " + SECOND, "!p " + SECOND_LH, bpm=160, label="second theme")
    piece.play("!ff " + HAMMER, "!ff " + HAMMER_LH, bpm=160, label="closing")


def picture(piece):
    exposition(piece)
    # development: the surges wander through F-sharp minor and back
    rh, lh = surges(("f#2", MINOR, "f#1"), ("f#2", MINOR, "e1"), ("d2", MAJOR, "d1"), ("c#2", SEVENTH, "c#1"),
                    ("f#2", MINOR, "f#1"), ("g#2", SEVENTH, "g#1"), ("g#2", SEVENTH, "g#1"), ("g#2", SEVENTH, "g#1"))
    piece.play("!mf " + rh + " !<ff", "!mf " + lh + " !<ff", bpm=160, label="development")
    piece.play("!ff " + SECOND, "!mf " + SECOND_LH, bpm=160, shift=-2, label="second theme, F-sharp minor")
    # recapitulation
    rh, lh = surges(*FIRST)
    piece.play("!p " + rh + " !<ff", "!p " + lh + " !<ff", bpm=160, label="recapitulation")
    piece.play("!f " + SECOND, "!p " + SECOND_LH, bpm=160, shift=-7, label="second theme, C-sharp minor")
    piece.play("!ff " + HAMMER, "!ff " + HAMMER_LH, bpm=160, shift=-7)
    # coda
    rh, lh = surges(("c#3", MINOR, "c#2"), ("f#2", MINOR, "f#1"), ("g#2", SEVENTH, "g#1"), ("c#3", MINOR, "c#2"))
    piece.play("!ff " + rh, "!ff " + lh, bpm=160, label="coda")
    piece.play("!f m4/4 " + " ".join(f"{n}:1/4" for n in range(pitch("c#6"), pitch("c#3") - 1, -1)
                                     if n % 12 in (1, 4, 8)) + " r:1 |", bpm=160, pedal=4)
    piece.play("m4/4 !ff c#3+g#3+c#4+e4:1^ r:1 c#3+g#3+c#4+e4:1^ r:1 | c#2+c#3+g#3+c#4:4^ |",
               "m4/4 !ff c#1+c#2:1^ r:1 c#1+c#2:1^ r:1 | c#1+c#2:4^ |", bpm=160, to=120, pedal=4)


def agitato():
    piece = Piece(SEED)
    picture(piece)
    return piece.render()
