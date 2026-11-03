import importlib
import os
import struct
import subprocess
import sys
import tempfile

import numpy as np

scripts_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(scripts_dir)

RATE = 48000
CHANNELS = 2
SOUNDFONT = os.environ.get("SOUNDFONT", "/usr/share/sounds/sf2/FluidR3_GM.sf2")

TICKS_PER_BEAT = 480
TEMPO = 500000  # microseconds per beat, 120 bpm
TICKS_PER_SECOND = TICKS_PER_BEAT * 1000000 // TEMPO


# --- midi ------------------------------------------------------------------

def varlen(value):
    """MIDI variable-length quantity."""
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.append(0x80 | (value & 0x7F))
        value >>= 7
    return bytes(reversed(out))


def write_midi(path, events):
    """Write a format 0 MIDI file. Events are (seconds, status, data1, data2)
    tuples, e.g. (1.5, 0x90, 60, 100) is a note on, channel 0, at 1.5 s."""
    track = bytearray(b"\x00\xff\x51\x03" + TEMPO.to_bytes(3, "big"))
    now = 0
    # note offs before note ons at the same tick, so repeated notes retrigger
    for seconds, status, *data in sorted(events, key=lambda e: (e[0], (e[1] & 0xF0) != 0x80)):
        tick = round(seconds * TICKS_PER_SECOND)
        track += varlen(tick - now) + bytes([status, *data])
        now = tick
    track += b"\x00\xff\x2f\x00"

    with open(path, "wb") as f:
        f.write(b"MThd" + struct.pack(">IHHH", 6, 0, 1, TICKS_PER_BEAT))
        f.write(b"MTrk" + struct.pack(">I", len(track)) + track)


class Score:
    """Collects MIDI events in seconds and renders them through FluidSynth."""

    def __init__(self):
        self.events = []

    def program(self, channel, program, seconds=0.0):
        self.events.append((seconds, 0xC0 | channel, program))

    def control(self, channel, controller, value, seconds=0.0):
        self.events.append((seconds, 0xB0 | channel, controller, value))

    def note(self, seconds, duration, channel, pitch, velocity=100):
        self.events.append((seconds, 0x90 | channel, pitch, velocity))
        self.events.append((seconds + duration, 0x80 | channel, pitch, 0))

    def render(self, seconds, gain=0.5):
        """Render to a float32 array of shape (seconds * RATE, CHANNELS)."""
        if not os.path.isfile(SOUNDFONT):
            sys.exit(f"soundfont not found: {SOUNDFONT} (set SOUNDFONT)")

        with tempfile.TemporaryDirectory() as tmp:
            midi = os.path.join(tmp, "score.mid")
            raw = os.path.join(tmp, "score.raw")
            write_midi(midi, self.events)
            subprocess.run(
                ["fluidsynth", "-niq", "-g", str(gain), "-r", str(RATE),
                 "-T", "raw", "-O", "float", "-F", raw, SOUNDFONT, midi],
                check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL
            )
            audio = np.fromfile(raw, dtype=np.float32).reshape(-1, CHANNELS)

        return fit(audio, round(seconds * RATE))


# --- numpy helpers ---------------------------------------------------------

def fit(audio, frames):
    """Trim or zero-pad audio to exactly the given number of frames."""
    if len(audio) >= frames:
        return audio[:frames]
    return np.pad(audio, ((0, frames - len(audio)), (0, 0)))


def normalize(audio, peak_db=-1.0):
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    return audio * (10 ** (peak_db / 20) / peak)


# --- projects --------------------------------------------------------------

def load_project(target):
    """Render the project passed as the first argument and return its audio
    together with the output path (without extension) inside the root-level
    target directory.

    A project scripts/<theme>-<name>/ must provide <name>.py with a <name>()
    function returning a float array of shape (frames, CHANNELS) at RATE, e.g.
    scripts/nature-chirping00/chirping00.py:chirping00(). Projects can sit one
    folder deeper, e.g. simplified/handel-messiah-44-hallelujah; their output
    still goes straight into the target directory (see export_name).
    """
    args = sys.argv[1:]
    if not args:
        sys.exit("usage: python3 <script> <project>")

    project = args[0]
    project_dir = os.path.join(scripts_dir, project)
    if not os.path.isdir(project_dir):
        sys.exit(f"project not found: {project_dir}")

    name = project.rsplit("-", 1)[-1]
    sys.path.insert(0, project_dir)
    audio = getattr(importlib.import_module(name), name)()

    audio = np.asarray(audio, dtype=np.float32)
    if audio.ndim != 2 or audio.shape[1] != CHANNELS:
        sys.exit(f"{project} must return shape (frames, {CHANNELS}), got {audio.shape}")
    audio = np.clip(audio, -1.0, 1.0)

    target_dir = os.path.join(root_dir, target)
    os.makedirs(target_dir, exist_ok=True)

    return audio, os.path.join(target_dir, export_name(project))


def export_name(project):
    """Exports stay flat: simplified/foo is written as foo, any other
    subfolder keeps its name as a prefix (transcribed/foo -> transcribed-foo)
    so it cannot clash with the simplified version."""
    folder, _, name = project.rpartition("/")
    return name if folder in ("", "simplified") else folder.replace("/", "-") + "-" + name


def ffmpeg_export(audio, path, *args):
    """Encode float32 stereo audio with ffmpeg; args select codec/options."""
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-f", "f32le", "-ar", str(RATE), "-ac", str(CHANNELS), "-i", "pipe:0",
         *args, path],
        input=audio.astype("<f4").tobytes(), check=True
    )
