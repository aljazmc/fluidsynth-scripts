"""Tests for scripts/common.py. Run: python3 -m unittest discover tests/py"""
import importlib
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
common = importlib.import_module("common")


class VarlenTest(unittest.TestCase):

    def test_matches_the_midi_specification(self):
        # examples from the Standard MIDI File specification
        examples = {
            0x00000000: b"\x00",
            0x00000040: b"\x40",
            0x0000007F: b"\x7f",
            0x00000080: b"\x81\x00",
            0x00002000: b"\xc0\x00",
            0x00003FFF: b"\xff\x7f",
            0x00004000: b"\x81\x80\x00",
            0x00100000: b"\xc0\x80\x00",
            0x0FFFFFFF: b"\xff\xff\xff\x7f",
        }
        for value, encoded in examples.items():
            with self.subTest(value=hex(value)):
                self.assertEqual(common.varlen(value), encoded)


def tone(frequency, dbfs, seconds=5.0):
    """A sine in both channels, at RATE."""
    t = np.arange(round(seconds * common.RATE)) / common.RATE
    mono = 10 ** (dbfs / 20) * np.sin(2 * np.pi * frequency * t)
    return np.column_stack((mono, mono))


def db(value):
    return 20 * np.log10(value)


class LoudnessTest(unittest.TestCase):

    def test_reads_a_tone_at_its_level(self):
        # ITU-R BS.1770: a 1 kHz sine at 0 dBFS in one channel reads -3.01
        # LUFS, so in both channels it reads 0, and at -20 dBFS it reads -20
        self.assertAlmostEqual(common.loudness(tone(1000, -20)), -20.0, delta=0.1)

    def test_weights_bass_less(self):
        # K-weighting takes about 3.6 dB off at 60 Hz
        self.assertAlmostEqual(common.loudness(tone(60, -20)), -23.6, delta=0.2)

    def test_reads_silence_as_minus_infinity(self):
        self.assertEqual(common.loudness(np.zeros((common.RATE * 2, 2))), -np.inf)


class MasterTest(unittest.TestCase):

    def test_true_peaks_find_the_peaks_between_samples(self):
        # a sine at a quarter of the rate, sampled 45 degrees off its peaks
        n = np.arange(common.RATE)
        mono = np.sin(np.pi / 2 * n + np.pi / 4)
        audio = np.column_stack((mono, mono))
        self.assertAlmostEqual(np.max(np.abs(audio)), 0.707, delta=0.001)
        self.assertGreater(np.max(common.true_peaks(audio)), 0.97)

    def test_limit_keeps_peaks_below_the_ceiling(self):
        audio = tone(1000, -20)
        audio[common.RATE:common.RATE + 50] = 1.0  # a click
        limited = common.limit(audio)
        self.assertLessEqual(db(np.max(common.true_peaks(limited))), common.LIMIT + 0.01)
        # away from the click the tone is untouched
        self.assertTrue(np.allclose(limited[3 * common.RATE:], audio[3 * common.RATE:]))

    def test_limit_leaves_quiet_audio_alone(self):
        audio = tone(1000, -20)
        self.assertIs(common.limit(audio), audio)

    def test_master_brings_quiet_and_loud_audio_to_the_target(self):
        for dbfs in (-40, -6):
            with self.subTest(dbfs=dbfs):
                mastered = common.master(tone(1000, dbfs))
                self.assertAlmostEqual(common.loudness(mastered), common.LOUDNESS, delta=0.2)
                self.assertLessEqual(db(np.max(common.true_peaks(mastered))), common.LIMIT + 0.01)

    def test_master_limits_peaky_audio(self):
        audio = tone(1000, -40)
        audio[::common.RATE // 4] = 1.0  # clicks four times a second
        mastered = common.master(audio)
        self.assertLessEqual(db(np.max(common.true_peaks(mastered))), common.LIMIT + 0.01)
        self.assertGreater(common.loudness(mastered), common.LOUDNESS - 2)


if __name__ == "__main__":
    unittest.main()
