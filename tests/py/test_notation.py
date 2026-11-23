"""The text notation of piano.py, and the arrangements written in it.
Run: python3 -m unittest discover tests/py

The arrangements are played with FluidSynth swapped for a recorder of the
MIDI events, so they run in seconds and need neither FluidSynth nor a
soundfont: every bar must fill its meter, and every event must be valid MIDI.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

ARRANGEMENTS = sorted(p.parent for p in (SCRIPTS / "simplified").glob("*/piano.py"))


def piano_modules():
    """Each distinct piano.py, imported under its own name, as the
    arrangements carry their own copies."""
    modules, seen = [], set()
    for folder in ARRANGEMENTS:
        path = folder / "piano.py"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in seen:
            continue
        seen.add(digest)
        spec = importlib.util.spec_from_file_location(f"piano_{len(modules)}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules.append((folder.name, module))
    return modules


PIANOS = piano_modules()


class NotationTest(unittest.TestCase):

    def each(self):
        for project, piano in PIANOS:
            yield project, piano

    def test_pitch_names(self):
        for project, piano in self.each():
            with self.subTest(piano=project):
                names = {"c4": 60, "a4": 69, "eb4": 63, "f#3": 54, "b#3": 60,
                         "cbb4": 58, "c-1": 0, "g9": 127, "60": 60}
                for text, midi in names.items():
                    self.assertEqual(piano.pitch(text), midi, text)
                for midi in range(128):
                    self.assertEqual(piano.pitch(piano.name(midi)), midi)
                with self.assertRaises(ValueError):
                    piano.pitch("h4")

    def test_durations_are_sticky(self):
        for project, piano in self.each():
            with self.subTest(piano=project):
                voice = piano.Voice("c4:1/2 d4 e4:1 f4 r:2 g4")
                beats = [(n[0], n[1]) for n in voice.notes]
                half, one = Fraction(1, 2), Fraction(1)
                self.assertEqual(beats, [(0, half), (half, half), (1, one), (2, one), (5, 2)])
                self.assertEqual(voice.length, 7)

    def test_chords_marks_and_rests(self):
        for project, piano in self.each():
            with self.subTest(piano=project):
                voice = piano.Voice("c4+e4+g4:2 r:1 a4:1^ b4'")
                self.assertEqual([n[2] for n in voice.notes], [60, 64, 67, 69, 71])
                self.assertEqual([n[0] for n in voice.notes], [0, 0, 0, 3, 4])
                self.assertEqual([(n[3], n[4]) for n in voice.notes][-2:], [(True, False), (False, True)])

    def test_ties_join_notes_of_the_same_pitch(self):
        for project, piano in self.each():
            with self.subTest(piano=project):
                voice = piano.Voice("c4:1~ c4:1/2 d4:1~ e4:1")
                self.assertEqual([(n[2], n[1]) for n in voice.notes],
                                 [(60, Fraction(3, 2)), (62, 1), (64, 1)])

    def test_bars_must_fill_the_meter(self):
        for project, piano in self.each():
            with self.subTest(piano=project):
                piano.Voice("m3/4 c4:1 d4 e4 | f4 g4 a4 |")
                piano.Voice("m3/4 c4:1 | d4 e4 f4 |")  # a pickup
                with self.assertRaises(ValueError):
                    piano.Voice("m3/4 c4:1 d4 e4 | f4 g4 |")
                with self.assertRaises(ValueError):
                    piano.Voice("m4/4 c4:1 d4 e4 f4 | g4 a4 b4 c5 d5 |")

    def test_bad_tokens_fail_with_the_bar(self):
        for project, piano in self.each():
            with self.subTest(piano=project):
                with self.assertRaisesRegex(ValueError, "bar 2"):
                    piano.Voice("c4:1 | c4:1:2 |")

    def test_dynamics_and_hairpins(self):
        for project, piano in self.each():
            with self.subTest(piano=project):
                voice = piano.Voice("!p c4:1 d4 e4 !<f f4")
                p, f = piano.DYNAMICS["p"], piano.DYNAMICS["f"]
                self.assertEqual(voice.velocity(0), p)
                self.assertAlmostEqual(voice.velocity(Fraction(3, 2)), p + (f - p) / 2)
                self.assertEqual(voice.velocity(3), f)
                self.assertEqual(piano.Voice("c4").velocity(0), piano.DYNAMICS["mf"])

    def test_tempo(self):
        for project, piano in self.each():
            with self.subTest(piano=project):
                steady = piano.tempo_map(120, None, 8)
                self.assertAlmostEqual(steady(4), 2.0)
                # a ritardando from 120 to 60 takes longer than 120 and less than 60
                rit = piano.tempo_map(120, 60, 8)
                self.assertTrue(4.0 < rit(8) < 8.0)
                times = [rit(beat) for beat in range(9)]
                self.assertEqual(times, sorted(times))


# Runs one arrangement in its own process (the arrangements share module
# names) with Score.render recording the events instead of calling FluidSynth.
RECORD = """
import json, sys
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
import numpy as np
import common
recorded = []
def render(self, seconds, gain=0.5):
    recorded.append({"seconds": seconds, "events": self.events})
    return np.zeros((common.RATE, common.CHANNELS), dtype=np.float32)
common.Score.render = render
name = sys.argv[2].rsplit("-", 1)[-1]
getattr(__import__(name), name)()
json.dump(recorded, sys.stdout)
"""


class ArrangementTest(unittest.TestCase):
    """Every arrangement parses and plays valid MIDI."""

    def test_arrangements_play_valid_midi(self):
        self.assertTrue(ARRANGEMENTS)
        for folder in ARRANGEMENTS:
            with self.subTest(project=folder.name):
                result = subprocess.run(
                    [sys.executable, "-c", RECORD, str(SCRIPTS), str(folder)],
                    capture_output=True, text=True, cwd=ROOT
                )
                # a bar that doesn't fill its meter fails here, with its number
                self.assertEqual(result.returncode, 0, result.stderr[-2000:])
                for render in json.loads(result.stdout):
                    self.check(render["seconds"], render["events"])

    def check(self, seconds, events):
        sounding = {}
        notes = 0
        for event in events:
            at, status, *data = event
            kind, channel = status & 0xF0, status & 0x0F
            where = f"{event} at {at:.2f} s"
            self.assertTrue(0 <= at <= seconds, f"outside 0..{seconds:.1f} s: {where}")
            self.assertIn(kind, (0x80, 0x90, 0xB0, 0xC0), where)
            self.assertEqual(len(data), 1 if kind == 0xC0 else 2, where)
            for value in data:
                self.assertIsInstance(value, int, where)
                self.assertTrue(0 <= value <= 127, where)
            if kind == 0x90:
                # velocity 0 would be a note off
                self.assertGreater(data[1], 0, where)
                key = (channel, data[0])
                sounding[key] = sounding.get(key, 0) + 1
                notes += 1
            elif kind == 0x80:
                key = (channel, data[0])
                sounding[key] = sounding.get(key, 0) - 1
        self.assertGreater(notes, 100, "hardly any notes")
        unbalanced = {key: count for key, count in sounding.items() if count}
        self.assertEqual(unbalanced, {}, "(channel, pitch): note ons minus note offs")


if __name__ == "__main__":
    unittest.main()
