from piano import Piece, run, trill

# Mussorgsky, Pictures at an Exhibition (1874), I. The Gnome (Gnomus),
# preceded by the first Promenade. A piano arrangement written from memory:
# the Promenade tune, keys, meters, tempi and the shape of each section
# follow the original, the inner details are an approximation, not an urtext
# transcription.
SEED = 1874

# Promenade: Allegro giusto, nel modo russico, senza allegrezza, ma poco
# sostenuto. B-flat major, alternating 5/4 and 6/4 bars.
SOLO = ("m5/4 g4+g3:1 f4+f3 bb4+bb3 c5+c4:1/2 f5+f4 d5+d4:1 | "
        "m6/4 c5+c4:1/2 f5+f4 d5+d4:1 bb4+bb3 c5+c4 g4+g3 f4+f3 |")
CHORUS = ("m5/4 g4+eb4+bb3:1 f4+d4+bb3 bb4+g4+d4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 | "
          "m6/4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 bb4+f4+d4 c5+g4+eb4 g4+eb4+bb3 f4+d4+bb3 |")
BASS = ("m5/4 eb3+eb2:1 bb2+bb1 g2+g1 f2+f1 bb2+bb1 | "
        "m6/4 f2+f1:1 bb2+bb1 d3+d2 c3+c2 eb3+eb2 bb2+bb1 |")


def promenade(piece):
    piece.play("!f " + SOLO, bpm=96, label="promenade solo")
    piece.play("!f " + CHORUS, "!f " + BASS, bpm=96, pedal=1, label="promenade chorus")
    piece.play("!mf " + SOLO, bpm=96, shift=5, label="promenade solo in E-flat")
    piece.play("!mf " + CHORUS, "!mf " + BASS, bpm=96, shift=5, pedal=1)
    piece.play("!f " + CHORUS, "!f " + BASS, ("!f " + BASS, -12), bpm=96, pedal=1)
    piece.play("!ff " + CHORUS, "!ff " + BASS, ("!ff " + BASS, -12), bpm=96, to=72, pedal=1)
    piece.play("m3/4 !f bb4+f4+d4+bb3:3 |", "m3/4 !f bb2+bb1:3 |", bpm=72, pedal=3, gap=1.2)


# Gnomus: Sempre vivo, E-flat minor, 3/4. A lurching figure in octaves,
# broken off by silences, then a heavier, groaning answer.
LURCH = ("m3/4 eb3+eb2:1/4 f3+f2 gb3+gb2 ab3+ab2 bb3+bb2:1/2' r:1/2 cb4+cb3:1^ | "
         "bb3+bb2:2 r:1 |")
STAGGER = ("m3/4 gb3+gb2:1/2 f3+f2 eb3+eb2 d3+d2 eb3+eb2:1 | "
           "cb3+cb2:1^ bb2+bb1:1^ r:1 |")

# Poco meno mosso, pesante: soft chords over a sliding bass, with a sigh.
GROAN = ("m3/4 bb4+eb5+gb5:1 bb4+d5+f5 bb4+eb5+gb5 | cb5+eb5+ab5:2 bb4+d5+f5:1 | "
         "bb4+eb5+gb5:1 a4+eb5+gb5 ab4+d5+f5 | g4+db5+e5:3 |")
GROAN_BASS = ("m3/4 eb2+eb3:3~ | eb2+eb3:3 | cb2+cb3:3 | bb1+bb2:3 |")

STOMP = "m3/4 " + " ".join(["eb2+eb1:1/2^ eb2+eb1:1/2 bb2+bb1:1/2 eb2+eb1 bb1+bb0 eb2+eb1 |"] * 4)
STABS = ("m3/4 a3+c4+eb4+gb4:1^ r:2 | c4+eb4+gb4+a4:1^ r:2 | "
         "eb4+gb4+a4+c5:1^ r:2 | gb4+a4+c5+eb5:1^ r:1 cb5+eb5+gb5:1^ |")


def picture(piece):
    # A: two lurches and a stagger, broken by silences
    for dynamic in ("ff", "f"):
        piece.play(f"!{dynamic} " + LURCH, bpm=168, gap=0.5, label="lurch")
        piece.play(f"!{dynamic} " + LURCH, bpm=168, shift=-12, gap=0.3)
        piece.play(f"!{dynamic} " + STAGGER, bpm=168, gap=0.8, label="stagger")

    # B: pesante
    piece.play("!p " + GROAN, "!p " + GROAN_BASS, bpm=72, pedal="bar", gap=0.5, label="groan")
    piece.play("!pp " + GROAN, "!pp " + GROAN_BASS, bpm=72, to=60, shift=-5, pedal="bar", gap=1.0)

    # A again
    piece.play("!f " + LURCH, bpm=168, gap=0.4)
    piece.play("!ff " + STAGGER, bpm=168, gap=0.6)

    # C: the gnome trembling, a trill over a slowly sinking bass
    shiver = "m3/4 !pp " + " | ".join(trill("eb5", "fb5", 3) for _ in range(4)) + " !<f |"
    sink = "m3/4 !pp cb3+cb2:3 | bb2+bb1:3 | a2+a1:3 | ab2+ab1:3 !<f |"
    piece.play(shiver, sink, bpm=96, pedal="bar", label="trembling")
    shiver_low = "m3/4 !p " + " | ".join(trill("bb4", "cb5", 3) for _ in range(4)) + " !<ff |"
    sink_low = "m3/4 !p g2+g1:3 | gb2+gb1:3 | f2+f1:3 | e2+e1:3 !<ff |"
    piece.play(shiver_low, sink_low, bpm=104, pedal="bar")

    # D: stamping in the bass, diminished chords thrown at it, accelerating
    piece.play("!f " + STABS, "!f " + STOMP, bpm=120, to=160, label="stomp")
    piece.play("!ff " + STABS, "!ff " + STOMP, bpm=160, to=184, shift=1)

    # Coda: Vivo. A chromatic dash in octaves, a fall, two blows.
    dash = "!f " + run("eb3", "d5", octave=True) + " !<ff"
    fall = "!ff " + run("eb5", "e3", octave=True)
    piece.play(dash, bpm=184, label="dash")
    piece.play(fall, bpm=184)
    piece.play("m3/4 !ff eb4+gb4+bb4+eb5:1^ r:1/2 eb4+gb4+bb4+eb5:1/2^ r:1 | r:3 |",
               "m3/4 !ff eb2+eb1:1^ r:1/2 eb2+eb1:1/2^ r:1 | eb1+bb1+eb2:3^ |",
               bpm=184, pedal=3)


def gnome():
    piece = Piece(SEED)
    promenade(piece)
    picture(piece)
    return piece.render()
