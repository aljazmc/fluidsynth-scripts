"""An orchestra for the notation in piano.py: each part gets its own General
MIDI instrument on its own channel.

Sustained instruments (strings, winds, brass, organ, choir) take their
dynamics from MIDI expression (CC11), sampled along the part's first voice, so
hairpins swell and fade through held notes. Struck and plucked instruments
take their dynamics from note velocity, like the piano.

The "percussion" part plays General MIDI drum numbers on channel 10, e.g.
36 bass drum, 38 snare, 49 crash cymbal, 52 china cymbal (a passable gong).
"""
from fractions import Fraction

import numpy as np

from common import RATE, Score, normalize
from piano import DYNAMICS, Voice, tempo_map

PERCUSSION_CHANNEL = 9
MELODIC_CHANNELS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15)

# name: (General MIDI program, zero-based; pan -1..1; sustained; volume)
INSTRUMENTS = {
    "piccolo": (72, 0.15, True, 88),
    "flutes": (73, -0.1, True, 100),
    "oboes": (68, 0.1, True, 96),
    "cor anglais": (69, 0.15, True, 96),
    "clarinets": (71, -0.2, True, 100),
    "bassoons": (70, 0.25, True, 100),
    "horns": (60, -0.45, True, 108),
    "trumpets": (56, 0.3, True, 100),
    "trombones": (57, 0.45, True, 104),
    "tuba": (58, 0.5, True, 104),
    "timpani": (47, 0.0, False, 112),
    "harp": (46, -0.65, False, 110),
    "celesta": (8, -0.5, False, 105),
    "glockenspiel": (9, -0.3, False, 90),
    "xylophone": (13, 0.3, False, 95),
    "bells": (14, 0.35, False, 100),
    "organ": (19, 0.0, True, 92),
    "choir": (52, 0.0, True, 105),
    "solo violin": (40, -0.4, True, 100),
    "violins": (48, -0.6, True, 112),
    "violins 2": (48, -0.3, True, 106),
    "violas": (48, 0.2, True, 102),
    "cellos": (48, 0.45, True, 106),
    "basses": (43, 0.6, True, 106),
    "pizzicato": (45, -0.2, False, 110),
    "percussion": (None, 0.0, False, 112),
}


def expression(level):
    """Map a dynamic level to CC11, matching the velocity curve's range."""
    return int(np.clip(round(level * 127 / DYNAMICS["fff"]), 0, 127))


class Orchestra:
    def __init__(self, *names, seed=0, reverb=95, humanize=1.0):
        melodic = [n for n in names if n != "percussion"]
        if len(melodic) > len(MELODIC_CHANNELS):
            raise ValueError(f"at most {len(MELODIC_CHANNELS)} melodic parts, got {len(melodic)}")

        self.score = Score()
        self.seconds = 0.0
        self.rng = np.random.default_rng(seed)
        self.humanize = humanize
        self.channels = dict(zip(melodic, MELODIC_CHANNELS))
        if "percussion" in names:
            self.channels["percussion"] = PERCUSSION_CHANNEL

        for part, channel in self.channels.items():
            program, pan, _, volume = INSTRUMENTS[part]
            if program is not None:
                self.score.program(channel, program)
            self.score.control(channel, 7, volume)
            self.score.control(channel, 10, round(64 + 63 * pan))
            self.score.control(channel, 91, reverb)
            self.score.control(channel, 11, expression(DYNAMICS["mf"]))

    def play(self, parts, bpm, to=None, meter=None, shift=0, gap=0.0, label="section"):
        """Play {part: voice or [voices]} together from where the last section
        ended. A voice is a notation string or a (string, semitones) pair."""
        parsed = {}
        for part, voices in parts.items():
            if part not in self.channels:
                raise ValueError(f"{label}: {part!r} is not in this orchestra")
            if isinstance(voices, (str, tuple)):
                voices = [voices]
            parsed[part] = []
            for i, voice in enumerate(voices):
                text, own = (voice, 0) if isinstance(voice, str) else voice
                total = 0 if part == "percussion" else shift + own
                parsed[part].append(Voice(text, meter, total, f"{label}, {part} {i + 1}"))

        length = max(v.length for voices in parsed.values() for v in voices)
        clock = tempo_map(bpm, to, length)
        start = self.seconds

        for part, voices in parsed.items():
            channel = self.channels[part]
            sustained = INSTRUMENTS[part][2]

            if sustained:
                last, beat = None, Fraction(0)
                while beat <= length:
                    value = expression(voices[0].velocity(beat))
                    if value != last:
                        self.score.control(channel, 11, value, start + clock(beat))
                        last = value
                    beat += Fraction(1, 4)

            for voice in voices:
                for beat, notated, p, accent, staccato in voice.notes:
                    on, off = clock(beat), clock(beat + notated)
                    held = (off - on) * (0.5 if staccato else 0.98 if sustained else 0.96)
                    if sustained:
                        velocity = 84 + 0.3 * (voice.velocity(beat) - DYNAMICS["mf"])
                    else:
                        velocity = voice.velocity(beat)
                    velocity += 16 * accent + self.rng.normal(0, 3 * self.humanize)
                    jitter = self.rng.normal(0, 0.006 * self.humanize)
                    self.score.note(max(0.0, start + on + jitter), max(0.03, held), channel,
                                    int(np.clip(p, 0, 127)), int(np.clip(velocity, 1, 127)))

        self.seconds = start + clock(length) + gap

    def rest(self, seconds):
        self.seconds += seconds

    def render(self, tail=5.0, gain=0.4):
        audio = self.score.render(self.seconds + tail, gain)
        fade = np.minimum(1, (len(audio) - 1 - np.arange(len(audio))) / (1.0 * RATE))
        return normalize(audio * fade[:, None])
