"""A small text notation for piano music, played by FluidSynth's General MIDI
grand piano through common.Score.

A voice is a string of whitespace separated tokens:

    c4  eb4:1/2  f#3+a3+d4:1.5   note or chord (+), ":" duration in quarter beats
    60:1/4                       a MIDI note number works as a pitch too
    r:2                          rest
    <note>~                      tie into the next note of the same pitch
    <note>'                      staccato
    <note>^                      accent
    !mf  !<ff  !>n               dynamic (n is niente); < and > ramp from the previous one
    m3/4                         meter, checked at every bar line
    |                            bar line (the first bar may be a pickup)
    *                            pedal change

Durations are sticky: a note without ":" reuses the previous duration.
"""
import re
from fractions import Fraction

import numpy as np

from common import RATE, Score, normalize

PIANO = 0  # General MIDI program, zero-based
CHANNELS = (0, 1, 2, 3, 4, 5, 6, 7)  # one per voice, so voices never cut each other off

LETTERS = dict(c=0, d=2, e=4, f=5, g=7, a=9, b=11)
# GM pianos fall off steeply below ~40; n (niente) is for fading to nothing
DYNAMICS = dict(n=1, ppp=34, pp=44, p=54, mp=64, mf=75, f=88, ff=102, fff=116)

PITCH = re.compile(r"([a-g])([#b]*)(-?\d)$")
NOTE = re.compile(r"([^:'^~]+)(?::([\d./]+))?([\'^~]*)$")


def pitch(name):
    if name.isdigit():
        return int(name)
    match = PITCH.match(name)
    if not match:
        raise ValueError(f"bad pitch: {name}")
    letter, accidentals, octave = match.groups()
    return 12 * (int(octave) + 1) + LETTERS[letter] + accidentals.count("#") - accidentals.count("b")


def name(midi):
    """MIDI number to a sharp spelled pitch name, e.g. 61 -> c#4."""
    return ("c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b")[midi % 12] + str(midi // 12 - 1)


def bar_length(meter):
    return Fraction(meter) * 4


class Voice:
    """One parsed voice: notes, dynamics and pedal marks, in quarter beats."""

    def __init__(self, text, meter=None, shift=0, label="voice"):
        self.notes = []  # [beat, length, pitch, accent, staccato]
        self.dynamics = []  # (beat, velocity, ramp)
        self.pedals = []
        self.bars = []

        beat, duration, bar_start, bar = Fraction(0), Fraction(1), Fraction(0), 1
        meter = bar_length(meter) if meter else None
        tied = {}

        for token in text.split():
            if token == "|":
                filled = beat - bar_start
                if meter and filled != meter and not (bar == 1 and filled < meter):
                    raise ValueError(f"{label}, bar {bar}: {filled} beats, meter wants {meter}")
                self.bars.append(beat)
                bar_start, bar = beat, bar + 1
            elif token == "*":
                self.pedals.append(beat)
            elif token.startswith("m") and "/" in token:
                meter = bar_length(token[1:])
            elif token.startswith("!"):
                ramp = token[1] in "<>"
                self.dynamics.append((beat, DYNAMICS[token[1 + ramp:]], ramp))
            else:
                match = NOTE.match(token)
                if not match:
                    raise ValueError(f"{label}, bar {bar}: bad token {token!r}")
                body, length, marks = match.groups()
                if length:
                    duration = Fraction(length)
                still_tied = {}
                if body != "r":
                    for p in (pitch(part) + shift for part in body.split("+")):
                        if p in tied:
                            note = tied[p]
                            note[1] = beat + duration - note[0]
                        else:
                            note = [beat, duration, p, "^" in marks, "'" in marks]
                            self.notes.append(note)
                        if "~" in marks:
                            still_tied[p] = note
                tied = still_tied
                beat += duration

        self.length = beat

    def velocity(self, beat):
        points = self.dynamics or [(Fraction(0), DYNAMICS["mf"], False)]
        since, level = Fraction(0), points[0][1]
        for at, value, ramp in points:
            if at > beat:
                if ramp and at > since:
                    return level + (value - level) * float((beat - since) / (at - since))
                return level
            since, level = at, value
        return level


def tempo_map(bpm, to, length):
    """Seconds at a beat, with the tempo gliding linearly from bpm to `to`."""
    a, b, total = float(bpm), float(to or bpm), float(length)

    def seconds(beat):
        x = float(beat)
        if a == b or total == 0:
            return 60 * x / a
        k = (b - a) / total
        return 60 / k * np.log((a + k * x) / a)

    return seconds


class Piece:
    """Plays sections of voices one after another and renders the result."""

    def __init__(self, seed=0, reverb=70, humanize=1.0):
        self.score = Score()
        self.seconds = 0.0
        self.rng = np.random.default_rng(seed)
        self.humanize = humanize
        for channel in CHANNELS:
            self.score.program(channel, PIANO)
            self.score.control(channel, 7, 110)  # volume
            self.score.control(channel, 10, 64)  # pan
            self.score.control(channel, 91, reverb)  # reverb send

    def pedal(self, seconds, down):
        for channel in CHANNELS:
            self.score.control(channel, 64, 127 if down else 0, seconds)

    def play(self, *voices, bpm, to=None, meter=None, pedal=None, shift=0, gap=0.0, label="section"):
        """Play voices together starting where the previous section ended.

        A voice is a notation string or a (string, semitones) pair. pedal is
        None, "bar" (change at every bar line) or a number of beats; "*" tokens
        add changes anywhere. to glides the tempo from bpm over the section.
        """
        parsed = []
        for i, voice in enumerate(voices):
            text, own = (voice, 0) if isinstance(voice, str) else voice
            parsed.append(Voice(text, meter, shift + own, f"{label}, voice {i + 1}"))

        length = max(v.length for v in parsed)
        clock = tempo_map(bpm, to, length)
        start = self.seconds

        for channel, voice in zip(CHANNELS, parsed):
            for beat, notated, p, accent, staccato in voice.notes:
                on, off = clock(beat), clock(beat + notated)
                held = (off - on) * (0.45 if staccato else 0.96)
                velocity = voice.velocity(beat) + 14 * accent + self.rng.normal(0, 3 * self.humanize)
                jitter = self.rng.normal(0, 0.005 * self.humanize)
                self.score.note(max(0.0, start + on + jitter), max(0.03, held), channel,
                                int(np.clip(p, 21, 108)), int(np.clip(velocity, 1, 127)))

        changes = {beat for v in parsed for beat in v.pedals}
        if pedal == "bar":
            changes |= set(parsed[0].bars)
        elif pedal:
            changes |= {Fraction(i) * Fraction(pedal) for i in range(int(length / Fraction(pedal)) + 1)}
        if changes or pedal:
            changes.add(Fraction(0))
            for beat in sorted(c for c in changes if c < length):
                self.pedal(start + clock(beat), False)
                self.pedal(start + clock(beat) + 0.04, True)
            self.pedal(start + clock(length), False)

        self.seconds = start + clock(length) + gap

    def rest(self, seconds):
        self.seconds += seconds

    def render(self, tail=4.0, gain=0.6):
        audio = self.score.render(self.seconds + tail, gain)
        fade = np.minimum(1, (len(audio) - 1 - np.arange(len(audio))) / (0.5 * RATE))
        return normalize(audio * fade[:, None])


# --- texture helpers -------------------------------------------------------

def trill(a, b, beats, step="1/8"):
    """Alternate two pitches for the given number of beats."""
    count = int(Fraction(beats) / Fraction(step))
    return " ".join(f"{(a, b)[i % 2]}:{step}" for i in range(count))


def tremolo(chord_a, chord_b, beats, step="1/4"):
    return trill(chord_a, chord_b, beats, step)


def run(start, end, step="1/4", octave=False, marks=""):
    """Chromatic run from one pitch to another, optionally in octaves."""
    a, b = pitch(start), pitch(end)
    direction = 1 if b >= a else -1
    notes = range(a, b + direction, direction)
    return " ".join(f"{n}+{n - 12}:{step}{marks}" if octave else f"{n}:{step}{marks}" for n in notes)


def scale(start, steps, degrees, first=0, step="1/2", marks=""):
    """Walk `steps` scale steps (negative goes down) from start, which is
    degree `first` of a scale given as semitone offsets, e.g. MAJOR."""
    base = pitch(start) - degrees[first]
    out = []
    for i in range(abs(steps) + 1):
        octave, degree = divmod(first + (i if steps >= 0 else -i), len(degrees))
        out.append(f"{base + 12 * octave + degrees[degree]}:{step}{marks}")
    return " ".join(out)


MAJOR = (0, 2, 4, 5, 7, 9, 11)
MINOR = (0, 2, 3, 5, 7, 8, 10)
