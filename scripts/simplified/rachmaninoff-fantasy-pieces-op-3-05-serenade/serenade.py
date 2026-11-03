from piano import Piece

# Rachmaninoff, Morceaux de fantaisie (Fantasy Pieces), Op. 3, No. 5,
# Sérénade in B-flat minor. A from-memory piano arrangement: a Spanish-tinged
# serenade in the tempo of a minuet, the left hand strumming like a guitar,
# the tune ornamented with grace notes, a brighter middle in D-flat major, in
# Rachmaninoff's manner; the notes are approximate.
SEED = 1896

# Tempo di minuetto, 3/4. The left hand: bass, then two strummed chords.
def strum(bass, chord):
    return f"{bass}:1' {chord}:1/2' {chord}:1/2' {chord}:1' |"


TUNE = ("m3/4 f5:1 gb5:1/4 f5:1/4 e5:1/4 f5:1/4 db5:1 | bb4:2 c5:1 | db5:1 c5:1/2 bb4:1/2 a4:1 | bb4:3 | "
        "db5:1 eb5:1/4 db5:1/4 c5:1/4 db5:1/4 bb4:1 | gb5:2 f5:1 | e5:1 f5:1/2 db5:1/2 c5:1 | bb4:3 |")
TUNE_LH = "m3/4 " + " ".join(strum(b, c) for b, c in (
    ("bb1", "f3+bb3+db4"), ("gb1", "gb3+bb3+db4"), ("f1", "f3+a3+c4"), ("bb1", "f3+bb3+db4"),
    ("bb1", "f3+bb3+db4"), ("eb2", "gb3+bb3+eb4"), ("f1", "f3+a3+eb4"), ("bb1", "f3+bb3+db4")))

BRIGHT = ("m3/4 ab4:1 db5:1 f5:1 | eb5:2 db5:1 | c5:1 eb5:1 ab5:1 | gb5:2 f5:1 | "
          "eb5:1 db5:1 c5:1 | db5:1 f5:1 bb5:1 | ab5:1 gb5:1/2 f5:1/2 eb5:1 | db5:3 |")
BRIGHT_LH = "m3/4 " + " ".join(strum(b, c) for b, c in (
    ("db2", "f3+ab3+db4"), ("ab1", "gb3+ab3+c4"), ("ab1", "gb3+ab3+c4"), ("db2", "f3+ab3+db4"),
    ("ab1", "gb3+ab3+c4"), ("bb1", "f3+bb3+db4"), ("ab1", "gb3+ab3+c4"), ("db2", "f3+ab3+db4")))


def picture(piece):
    piece.play("m3/4 !p " + " ".join([strum("bb1", "f3+bb3+db4")] * 2), bpm=120, label="guitar")
    piece.play("!mp " + TUNE, "!p " + TUNE_LH, bpm=120, label="tune")
    piece.play("!mf " + TUNE, "!mp " + TUNE_LH, bpm=120, shift=0)
    piece.play("!mp " + BRIGHT, "!p " + BRIGHT_LH, bpm=116, label="bright")
    piece.play("!f " + BRIGHT, "!mf " + BRIGHT_LH, bpm=116, to=108)
    piece.play(("!mp " + TUNE, 12), "!p " + TUNE_LH, bpm=120, label="tune, high")
    piece.play("!p " + TUNE + " !>pp", "!pp " + TUNE_LH + " !>pp", bpm=116, to=100)
    piece.play("m3/4 !pp r:1 f3+bb3+db4:1/2' r:3/2 | bb1+f2+bb2:3 |", bpm=100, pedal=3)


def serenade():
    piece = Piece(SEED)
    picture(piece)
    return piece.render()
