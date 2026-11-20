"""Tests for scripts/common.py. Run: python3 -m unittest discover tests"""
import importlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
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


if __name__ == "__main__":
    unittest.main()
