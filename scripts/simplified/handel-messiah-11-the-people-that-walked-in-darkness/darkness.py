from orchestra import Orchestra

# Handel, Messiah, Part I, No. 11. The people that walked in darkness (air,
# bass). A from-memory arrangement for General MIDI baroque orchestra, the
# bass singing without words: the strings and the voice groping together in
# bare unison through a winding, chromatic B minor line, the music itself
# "walking in darkness", follows Handel, the notes are approximate.
SEED = 1751

PARTS = ("bass voice", "harpsichord", "violins", "violins 2", "violas", "cellos", "basses")

# Larghetto, 4/4, all in unison
GROPE = ("m4/4 b2:1/2 c#3 d3 e3 f#3 g3 a#2 b2 | g3:1/2 f#3 e3 d3 c#3 d3 e3 c#3 | "
         "d3:1/2 e3 f#3 g3 a3 b3 c4 b3 | a#3:1/2 b3 c#4 a#3 b3:2 | "
         "e3:1/2 f#3 g3 a3 b3 c4 d#3 e3 | c4:1/2 b3 a3 g3 f#3 g3 a3 f#3 | "
         "g3:1/2 e3 c#3 a#2 b2 d3 f#3 f#2 | b2:4 |")
LIGHT = ("m4/4 d3:1/2 e3 f#3 g3 a3 b3 c#4 d4 | b3:1/2 a3 g3 f#3 e3 f#3 g3 e3 | "
         "f#3:1/2 g3 a3 b3 c#4 b3 a3 g3 | f#3:2 a3:2 | d3:4 |")


def unison(text, dynamic, voice=True):
    parts = {"violins": (f"!{dynamic} " + text, 24), "violins 2": (f"!{dynamic} " + text, 12),
             "violas": (f"!{dynamic} " + text, 12), "cellos": f"!{dynamic} " + text,
             "basses": (f"!{dynamic} " + text, -12)}
    if voice:
        parts["bass voice"] = f"!{dynamic} " + text
    return parts


def picture(orchestra):
    orchestra.play(unison(GROPE, "p", voice=False), bpm=64, label="ritornello")
    orchestra.play(unison(GROPE, "mp"), bpm=64, label="walked in darkness")
    orchestra.play({**unison(LIGHT, "mf"), "harpsichord": "!mf m4/4 d3+f#3+a3:4 | e3+g3+b3:4 | f#3+a3+c#4:4 | f#3+a3+c#4:4 | d3+f#3+a3:4 |"},
                   bpm=64, label="have seen a great light")
    orchestra.play(unison(GROPE, "mp"), bpm=64, to=56)


def darkness():
    orchestra = Orchestra(*PARTS, seed=SEED, reverb=90)
    picture(orchestra)
    return orchestra.render()
