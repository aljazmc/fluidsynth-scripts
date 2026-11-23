"""Loudness and frequency tests: every project should sound right on typical
laptop speakers. Run: python3 -m unittest discover tests

The checks on the projects render them, which takes a while, so they only run
with RENDER set: RENDER=all for every project, or a pattern such as
RENDER='soundscapes/cyberpunk-*' (fnmatch, on the path inside scripts/).
JOBS sets how many render at once (default: the number of CPUs). They need
FluidSynth, a soundfont, NumPy and FFmpeg, like project.sh.

The checks on the meter itself run always, if FFmpeg is installed.
"""
import fnmatch
import math
import os
import re
import shutil
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
RATE = 48000
CHANNELS = 2

# --- what typical laptop speakers can play --------------------------------------

# Small drivers roll off steeply below about 150 Hz and above about 16 kHz; what
# is left is what a laptop plays.
LAPTOP_LOW = 150
LAPTOP_HIGH = 16000
# Integrated loudness (LUFS): loud enough to hear well at full volume on small
# speakers, near what streaming services play at (-14 to -16), not so loud
# that the speakers distort.
LOUDNESS_MIN = -20.0
LOUDNESS_MAX = -12.0
# True peak (dBTP): headroom for the speakers' own processing and for lossy
# encoding
PEAK_MAX = -1.0
# Loudness range (LU): the soft passages must stay above the noise of a room
# and of the fan
RANGE_MAX = 15.0
# How much quieter (LU) a project sounds once the laptop has dropped the bass
# below LAPTOP_LOW: more means it is mostly made of sound a laptop can't play.
BASS_LOSS_MAX = 6.0
# How much quieter (LU) once the laptop has dropped what lies above
# LAPTOP_HIGH: more means hiss or energy above what it can play.
TREBLE_LOSS_MAX = 0.5

# 24 dB per octave, like the roll-off of a small driver in a closed box
BASS_FILTER = f"highpass=f={LAPTOP_LOW},highpass=f={LAPTOP_LOW}"
TREBLE_FILTER = f"lowpass=f={LAPTOP_HIGH},lowpass=f={LAPTOP_HIGH}"


# --- measuring --------------------------------------------------------------------

def ebur128(audio, filters=""):
    """Measure raw float32 stereo audio at RATE with FFmpeg's EBU R128 meter,
    after the given FFmpeg audio filters. Returns integrated loudness (LUFS),
    loudness range (LU) and true peak (dBTP)."""
    chain = (filters + "," if filters else "") + "ebur128=peak=true:framelog=quiet"
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(RATE),
         "-ac", str(CHANNELS), "-i", "pipe:0", "-af", chain, "-f", "null", "-"],
        input=audio, capture_output=True, check=True
    )
    summary = result.stderr.decode().rsplit("Summary:", 1)[-1]

    def value(label):
        match = re.search(rf"{label}:\s+(-?inf|-?[\d.]+)", summary)
        if not match:
            raise ValueError(f"no {label} in the output of ebur128:\n{summary}")
        return float(match.group(1))

    return value("I"), value("LRA"), value("Peak")


def measure(audio):
    """Everything the checks need, as a dict."""
    loudness, loudness_range, peak = ebur128(audio)
    bass_cut = ebur128(audio, BASS_FILTER)[0]
    treble_cut = ebur128(audio, TREBLE_FILTER)[0]
    return {
        "loudness": loudness,
        "range": loudness_range,
        "peak": peak,
        "bass_loss": loudness - bass_cut,
        "treble_loss": loudness - treble_cut,
    }


def problems(m):
    """The checks a measurement fails, as readable lines."""
    found = []
    if not LOUDNESS_MIN <= m["loudness"] <= LOUDNESS_MAX:
        found.append(f"loudness {m['loudness']:.1f} LUFS, expected "
                     f"{LOUDNESS_MIN:.0f} to {LOUDNESS_MAX:.0f}")
    if m["peak"] > PEAK_MAX:
        found.append(f"true peak {m['peak']:.1f} dBTP, expected at most {PEAK_MAX:.0f}")
    if m["range"] > RANGE_MAX:
        found.append(f"loudness range {m['range']:.1f} LU, expected at most {RANGE_MAX:.0f}")
    if m["bass_loss"] > BASS_LOSS_MAX:
        found.append(f"{m['bass_loss']:.1f} LU quieter without the bass below "
                     f"{LAPTOP_LOW} Hz, expected at most {BASS_LOSS_MAX:.0f}")
    if m["treble_loss"] > TREBLE_LOSS_MAX:
        found.append(f"{m['treble_loss']:.1f} LU quieter without what lies above "
                     f"{LAPTOP_HIGH} Hz, expected at most {TREBLE_LOSS_MAX}")
    return found


# --- rendering --------------------------------------------------------------------

RENDER = """
import sys
sys.path.insert(0, sys.argv[1])
sys.argv = sys.argv[1:]
from common import load_project
audio, _ = load_project("build")
sys.stdout.buffer.write(audio.astype("<f4").tobytes())
"""


def projects():
    """Projects as paths inside scripts/, like project.sh lists them."""
    found = []
    for script in SCRIPTS.glob("**/*.py"):
        folder = script.parent
        if folder != SCRIPTS and script.stem == folder.name.rsplit("-", 1)[-1]:
            found.append(folder.relative_to(SCRIPTS).as_posix())
    return sorted(found)


def render(project):
    """Render a project to raw float32 stereo, in its own Python process, as
    projects in different folders share module names (piano, score, ...)."""
    return subprocess.run(
        [sys.executable, "-c", RENDER, str(SCRIPTS), project],
        capture_output=True, check=True, cwd=ROOT
    ).stdout


# --- tests ------------------------------------------------------------------------

def tone(frequency, dbfs, seconds=10.0):
    """A sine in both channels, as raw float32 stereo."""
    import array
    amplitude = 10 ** (dbfs / 20)
    samples = array.array("f")
    for n in range(round(seconds * RATE)):
        value = amplitude * math.sin(2 * math.pi * frequency * n / RATE)
        samples.extend((value, value))
    if sys.byteorder != "little":
        samples.byteswap()
    return samples.tobytes()


@unittest.skipUnless(shutil.which("ffmpeg"), "needs ffmpeg")
class MeterTest(unittest.TestCase):
    """The meter reads known signals as the standard says."""

    def test_reads_a_tone_at_its_level(self):
        # ITU-R BS.1770: a 1 kHz sine at 0 dBFS in one channel reads -3.01
        # LUFS, so in both channels it reads 0, and at -20 dBFS it reads -20
        loudness, loudness_range, peak = ebur128(tone(1000, -20))
        self.assertAlmostEqual(loudness, -20.0, delta=0.2)
        self.assertAlmostEqual(peak, -20.0, delta=0.2)
        self.assertLess(loudness_range, 1.0)

    def test_a_tone_a_laptop_plays_passes(self):
        m = measure(tone(1000, -15))
        self.assertEqual(problems(m), [])

    def test_a_bass_tone_fails_on_the_bass(self):
        m = measure(tone(60, -15))
        self.assertGreater(m["bass_loss"], BASS_LOSS_MAX)
        self.assertTrue(any("bass" in line for line in problems(m)))

    def test_a_high_tone_fails_on_the_treble(self):
        m = measure(tone(19000, -15))
        self.assertGreater(m["treble_loss"], TREBLE_LOSS_MAX)

    def test_a_quiet_tone_fails_on_the_loudness(self):
        m = measure(tone(1000, -30))
        self.assertTrue(any("loudness" in line for line in problems(m)))

    def test_a_loud_tone_fails_on_the_peak(self):
        m = measure(tone(1000, -0.5))
        self.assertTrue(any("true peak" in line for line in problems(m)))


def selected():
    pattern = os.environ.get("RENDER", "")
    if pattern == "all":
        pattern = "*"
    return [p for p in projects() if pattern and fnmatch.fnmatch(p, pattern)]


@unittest.skipUnless(os.environ.get("RENDER"), "set RENDER to render the projects")
class ProjectTest(unittest.TestCase):
    """Every project selected by RENDER suits typical laptop speakers."""

    def test_projects_suit_laptop_speakers(self):
        chosen = selected()
        self.assertTrue(chosen, f"no project matches RENDER={os.environ['RENDER']}")

        def check(project):
            try:
                return project, problems(measure(render(project)))
            except subprocess.CalledProcessError as error:
                return project, [f"failed: {error.stderr.decode().strip()[-500:]}"]

        jobs = int(os.environ.get("JOBS", os.cpu_count() or 1))
        with ThreadPoolExecutor(jobs) as pool:
            for project, found in pool.map(check, chosen):
                with self.subTest(project=project):
                    self.assertEqual(found, [], "\n" + "\n".join(found))


if __name__ == "__main__":
    unittest.main()
