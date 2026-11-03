import re

from piano import Piece
from score import BAR_NUMBERS, LEFT, ORDER, RIGHT

# Beethoven, Bagatelle No. 25 in A minor, WoO 59, "Für Elise" (1810), simplified.

SEED = 1810

# (first bar, crotchet bpm, crotchet bpm at the end or None, dynamic or None)
# at "Poco moto" in 3/8; a passage starts again wherever its first bar comes
# round in the repeats. Every start falls where the pedal is up.
SECTIONS = (
    (0, 66, None, None),     # A, pp as written
    (9, 66, None, "p"),      # the answering phrase
    (23, 66, None, "p"),     # F major episode
    (30, 66, 62, "mp"),      # the demisemiquaver run, easing into the return
    (38, 66, None, "pp"),    # A
    (59, 66, None, "mf"),    # over the drumming A
    (77, 66, 54, None),      # arpeggios, pp as written, and the chromatic fall
    (82, 66, None, "pp"),    # A
    (100, 66, 56, None),     # the last phrase
)
DYNAMIC = re.compile(r"![<>]?(ppp|pp|p|mp|mf|fff|ff|f)\b")
STARTS = {first: (bpm, to, dynamic) for first, bpm, to, dynamic in SECTIONS}


def passages():
    """(settings, [written bar indices]) in playing order."""
    out = []
    for k in ORDER:
        number = BAR_NUMBERS[k]
        starts_here = number in STARTS and (not out or BAR_NUMBERS[out[-1][1][-1]] != number)
        if starts_here or not out:
            out.append((STARTS.get(number, SECTIONS[0][1:]), []))
        out[-1][1].append(k)
    return out


def picture(piece):
    current = "pp"  # the dynamic in force; the braille writes it in the right hand, for both
    for (bpm, to, dynamic), bars in passages():
        right = " ".join(RIGHT[k] for k in bars)
        written = DYNAMIC.findall(right)
        if dynamic is None:  # the one written at the start, else the one in force
            opens = DYNAMIC.match(RIGHT[bars[0]].split()[1])
            dynamic = opens.group(1) if opens else current
        current = written[-1] if written else dynamic
        right = f"!{dynamic} " + right
        left = f"!{dynamic} " + " ".join(LEFT[k] for k in bars)
        label = f"bars {BAR_NUMBERS[bars[0]]}-{BAR_NUMBERS[bars[-1]]}"
        piece.play(right, left, bpm=bpm, to=to, label=label)


def elise():
    piece = Piece(SEED)
    picture(piece)
    return piece.render()
