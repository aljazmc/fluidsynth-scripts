from piano import MAJOR, Piece, scale

# Mussorgsky, Pictures at an Exhibition, VII. The Market at Limoges, the
# Great News (Limoges. Le marché. La grande nouvelle), preceded by the fifth
# Promenade. A from-memory piano arrangement: key, meter, tempo, the
# chattering repeated notes and the headlong ending follow the original, the
# notes are approximate.
SEED = 1867

# Promenade V: Allegro giusto, nel modo russico, poco sostenuto. B-flat major.
CHORUS = ("m5/4 g4+eb4+bb3:1 f4+d4+bb3 bb4+g4+d4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 | "
          "m6/4 c5+a4+f4:1/2 f5+c5+a4 d5+bb4+f4:1 bb4+f4+d4 c5+g4+eb4 g4+eb4+bb3 f4+d4+bb3 |")
BASS = ("m5/4 eb3+eb2:1 bb2+bb1 g2+g1 f2+f1 bb2+bb1 | "
        "m6/4 f2+f1:1 bb2+bb1 d3+d2 c3+c2 eb3+eb2 bb2+bb1 |")


def promenade(piece):
    piece.play("!f " + CHORUS, "!f " + BASS, bpm=100, pedal=1, label="promenade")
    piece.play("!mf " + CHORUS, "!mf " + BASS, bpm=100, shift=5, pedal=1)
    piece.play("!f " + CHORUS, "!f " + BASS, ("!f " + BASS, -12), bpm=100, to=80, pedal=1)
    piece.play("m4/4 !f bb4+f4+d4+bb3:4 |", "m4/4 !f bb2+bb1:4 |", bpm=80, pedal=4, gap=0.8)


# Allegretto vivo, sempre scherzando. E-flat major, 4/4. Market women
# quarrelling: repeated notes, sudden accents, never a pause for breath.
CHATTER = ("m4/4 eb5:1/4' eb5' eb5' f5' g5:1/2' eb5' bb4:1/4' c5' bb4' ab4' g4:1/2' bb4' | "
           "ab4:1/4' ab4' ab4' bb4' c5:1/2' ab4' f4:1/4' g4' ab4' bb4' c5:1/2' r:1/2 | "
           "g5:1/4' g5' g5' ab5' bb5:1/2' g5' eb5:1/4' f5' eb5' d5' c5:1/2' d5' | "
           "eb5:1/4' g5' f5' d5' eb5:1/2' bb4' eb5:1' r:1 |")
STALLS = ("m4/4 eb3:1/2' bb3' g3' bb3' eb3' bb3' g3' bb3' | "
          "ab2' eb3' c3' eb3' f2' c3' ab2' c3' | "
          "eb3' bb3' g3' bb3' eb3' bb3' g3' bb3' | "
          "bb2' f3' ab3' f3' eb3:1' eb2:1' |")

# the big news, passed on in accented thirds, in C minor
NEWS = ("m4/4 c5+eb5:1/4' c5+eb5' c5+eb5' d5+f5' eb5+g5:1/2^ r:1/2 "
        "g5+bb5:1/4' f5+ab5' eb5+g5' d5+f5' c5+eb5:1/2' r:1/2 | "
        "b4+d5:1/4' b4+d5' c5+eb5' d5+f5' g4+b4+d5:1/2^ r:1/2 "
        "g4+b4+d5:1/2^ g4+b4+d5^ g4+b4+d5:1^ |")
NEWS_BASS = ("m4/4 c3:1/2' g3' eb3' g3' c3' g3' eb3' g3' | "
             "g2' d3' b2' d3' g2:1^ g1+g2:1^ |")


def picture(piece):
    piece.play("!mf " + CHATTER, "!mp " + STALLS, bpm=138, label="chatter")
    piece.play("!f " + CHATTER, "!mf " + STALLS, bpm=138, shift=5)
    piece.play("!f " + NEWS, "!mf " + NEWS_BASS, bpm=138, label="news")
    piece.play("!f " + NEWS, "!f " + NEWS_BASS, bpm=138, shift=2)
    piece.play("!ff " + NEWS + " !<fff", "!ff " + NEWS_BASS, bpm=138, shift=4)
    piece.play("!p " + CHATTER + " !<ff", "!p " + STALLS + " !<f", bpm=138, label="chatter again")
    piece.play("!ff " + CHATTER, "!f " + STALLS, ("!f " + STALLS, -12), bpm=138, to=152)

    # everyone rushes off: a headlong run down two octaves and a slam
    rush = "!ff " + scale("eb6", -14, MAJOR, step="1/4", marks="'") + " !>f"
    piece.play(rush, ("!ff " + scale("eb5", -14, MAJOR, step="1/4", marks="'"), 0), bpm=152, label="rush")
    piece.play("m4/4 !ff eb3+g3+bb3+eb4:1^ r:1 eb2+eb3:2^ |",
               "m4/4 !ff eb1+eb2:1^ r:1 eb1+bb1:2^ |", bpm=152, pedal=4)


def limoges():
    piece = Piece(SEED)
    promenade(piece)
    picture(piece)
    return piece.render()
