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


# --- mastering -------------------------------------------------------------

# every project is mastered to this integrated loudness (LUFS) and true peak
# (dBTP), so it plays well on small speakers such as a laptop's
LOUDNESS = -16.0
TRUE_PEAK = -1.0
# the limiter aims below TRUE_PEAK: meters oversample in different ways, and
# lossy encoders add a little to peaks
LIMIT = TRUE_PEAK - 1.0

# K-weighting of ITU-R BS.1770 at 48 kHz: a high shelf, then a high-pass
K_WEIGHTING = (
    ((1.53512485958697, -2.69169618940638, 1.19839281085285),
     (1.0, -1.69065929318241, 0.73248077421585)),
    ((1.0, -2.0, 1.0),
     (1.0, -1.99004745483398, 0.99007225036621)),
)


def loudness(audio):
    """Integrated loudness (LUFS) of ITU-R BS.1770 with the gating of EBU
    R128: 400 ms blocks every 100 ms, an absolute gate at -70 LUFS and a
    relative one 10 LU below. Returns -inf for silence."""
    if RATE != 48000:
        raise ValueError("K_WEIGHTING is for 48 kHz")
    audio = np.asarray(audio, dtype=np.float64)
    frames = len(audio)
    # filter in the frequency domain, padded so the filters' tails don't wrap
    n = 1 << int(np.ceil(np.log2(frames + RATE)))
    z = np.exp(-1j * np.pi * np.arange(n // 2 + 1) / (n // 2))
    response = np.ones(n // 2 + 1, dtype=complex)
    for b, a in K_WEIGHTING:
        response *= np.polyval(b[::-1], z) / np.polyval(a[::-1], z)
    weighted = np.fft.irfft(np.fft.rfft(audio, n, axis=0) * response[:, None], n, axis=0)
    power = np.concatenate(([0.0], np.cumsum(np.sum(weighted[:frames] ** 2, axis=1))))

    block, step = round(0.4 * RATE), round(0.1 * RATE)
    starts = np.arange(0, frames - block + 1, step)
    if len(starts) == 0:
        return -np.inf
    blocks = (power[starts + block] - power[starts]) / block
    with np.errstate(divide="ignore"):
        levels = -0.691 + 10 * np.log10(blocks)
    gated = blocks[levels > -70]
    if len(gated) == 0:
        return -np.inf
    relative = -0.691 + 10 * np.log10(np.mean(gated)) - 10
    gated = blocks[(levels > -70) & (levels > relative)]
    return -0.691 + 10 * np.log10(np.mean(gated))


def true_peaks(audio):
    """The peak of each frame over both channels, 4 times oversampled, so the
    peaks between the samples count too (as in ITU-R BS.1770)."""
    audio = np.asarray(audio, dtype=np.float64)
    taps = np.arange(-12, 12)
    peaks = np.max(np.abs(audio), axis=1)
    for phase in (0.25, 0.5, 0.75):
        t = taps + phase
        fir = np.sinc(t) * np.kaiser(len(t), 8.0)
        for channel in audio.T:
            # value between frame i and i+1, at i + phase
            between = np.convolve(channel, fir[::-1], mode="full")[12:12 + len(channel)]
            peaks = np.maximum(peaks, np.abs(between))
    return peaks


def limit(audio, ceiling_db=LIMIT, attack=0.005, release_db=200.0, block=64):
    """Look-ahead true-peak limiter: ramps the gain down ahead of a peak, 6 dB
    every `attack` seconds, so nothing goes above `ceiling_db` (dBTP), and
    back up at `release_db` dB a second."""
    ceiling = 10 ** (ceiling_db / 20)
    peaks = true_peaks(audio)
    if np.max(peaks) <= ceiling:
        return audio
    need = np.minimum(1.0, ceiling / np.maximum(peaks, 1e-12))
    blocks = -(-len(need) // block)
    need = np.pad(need, (0, blocks * block - len(need)), constant_values=1.0)
    gain = 20 * np.log10(need.reshape(blocks, block).min(axis=1))
    # each block also takes its neighbours' gain, so interpolating between
    # the block centres never lets a peak through
    gain = np.minimum(gain, np.minimum(np.roll(gain, 1), np.roll(gain, -1)))

    # ramp down before a peak (look-ahead) and back up after it
    seconds = block / RATE
    down = 6.0 * seconds / attack
    up = release_db * seconds
    gain = gain.tolist()
    for i in range(len(gain) - 2, -1, -1):
        gain[i] = min(gain[i], gain[i + 1] + down)
    for i in range(1, len(gain)):
        gain[i] = min(gain[i], gain[i - 1] + up)

    centres = np.arange(blocks) * block + (block - 1) / 2
    curve = np.interp(np.arange(len(audio)), centres, 10 ** (np.array(gain) / 20))
    return audio * curve[:, None]


def master(audio):
    """Bring audio to LOUDNESS, then limit its true peak to LIMIT. Limiting
    takes some loudness away, so it makes up for it and limits again."""
    audio = np.asarray(audio, dtype=np.float64)
    level = loudness(audio)
    if not np.isfinite(level):
        return audio.astype(np.float32)
    gain = LOUDNESS - level
    for _ in range(3):
        mastered = limit(audio * 10 ** (gain / 20))
        missing = LOUDNESS - loudness(mastered)
        if missing < 0.2:
            break
        gain += missing
    return mastered.astype(np.float32)


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
    audio = np.clip(master(audio), -1.0, 1.0)

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
