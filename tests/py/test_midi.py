"""The MIDI files that common.write_midi() writes, read back with a small
parser of the Standard MIDI File format. Run: python3 -m unittest discover tests/py"""
import importlib
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
common = importlib.import_module("common")


def read_varlen(data, at):
    value = 0
    while True:
        byte = data[at]
        at += 1
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            return value, at


def read_midi(path):
    """(format, tracks, division, [(tick, event bytes)]) of a one-track file.
    Running status is not expected, as write_midi() never uses it."""
    data = Path(path).read_bytes()
    assert data[:4] == b"MThd", "no MThd chunk"
    length, fmt, tracks, division = struct.unpack(">IHHH", data[4:14])
    assert length == 6, f"MThd length {length}"
    assert data[14:18] == b"MTrk", "no MTrk chunk"
    (size,) = struct.unpack(">I", data[18:22])
    track = data[22:]
    assert len(track) == size, f"MTrk says {size} bytes, has {len(track)}"

    events, at, tick = [], 0, 0
    while at < len(track):
        delta, at = read_varlen(track, at)
        tick += delta
        status = track[at]
        if status == 0xFF:  # meta event: type, length, data
            length, start = read_varlen(track, at + 2)
            end = start + length
        elif status & 0xF0 in (0xC0, 0xD0):  # program change, channel pressure
            end = at + 2
        else:
            assert status & 0x80, f"running status at byte {at}"
            end = at + 3
        events.append((tick, track[at:end]))
        at = end
    return fmt, tracks, division, events


class WriteMidiTest(unittest.TestCase):

    def write(self, events):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.mid"
            common.write_midi(path, events)
            return read_midi(path)

    def test_writes_a_valid_format_0_file(self):
        fmt, tracks, division, events = self.write([(0.0, 0x90, 60, 100), (1.0, 0x80, 60, 0)])
        self.assertEqual((fmt, tracks, division), (0, 1, common.TICKS_PER_BEAT))
        # starts with the tempo, ends with end of track
        self.assertEqual(events[0], (0, b"\xff\x51\x03" + common.TEMPO.to_bytes(3, "big")))
        self.assertEqual(events[-1][1], b"\xff\x2f\x00")

    def test_places_events_at_their_seconds(self):
        seconds = [0.0, 0.5, 1.25, 2.0, 61.0]
        _, _, _, events = self.write([(s, 0x90, 60 + i, 100) for i, s in enumerate(seconds)])
        notes = [(tick, data) for tick, data in events if data[0] == 0x90]
        self.assertEqual([tick for tick, _ in notes],
                         [round(s * common.TICKS_PER_SECOND) for s in seconds])
        self.assertEqual([data[1] for _, data in notes], [60, 61, 62, 63, 64])

    def test_sorts_events_by_time(self):
        _, _, _, events = self.write([(2.0, 0x90, 62, 90), (1.0, 0x90, 61, 90), (0.0, 0x90, 60, 90)])
        self.assertEqual([data[1] for _, data in events if data[0] == 0x90], [60, 61, 62])

    def test_note_off_comes_before_note_on_at_the_same_time(self):
        # a repeated note must stop before it starts again, or it doesn't sound
        _, _, _, events = self.write([(1.0, 0x90, 60, 100), (1.0, 0x80, 60, 0), (0.0, 0x90, 60, 100)])
        at_one_second = [data[0] for tick, data in events
                         if tick == common.TICKS_PER_SECOND and data[0] != 0xFF]
        self.assertEqual(at_one_second, [0x80, 0x90])

    def test_keeps_channels_and_two_byte_messages(self):
        _, _, _, events = self.write([(0.0, 0xC5, 40), (0.1, 0xB5, 7, 100), (0.2, 0x95, 70, 80)])
        self.assertEqual([data for _, data in events[1:-1]],
                         [b"\xc5\x28", b"\xb5\x07\x64", b"\x95\x46\x50"])

    def test_writes_long_pieces(self):
        # delta times beyond one byte of variable-length number
        _, _, _, events = self.write([(0.0, 0x90, 60, 100), (600.0, 0x80, 60, 0)])
        self.assertEqual(events[-2][0], 600 * common.TICKS_PER_SECOND)


class ScoreTest(unittest.TestCase):

    def test_note_adds_a_note_on_and_off(self):
        score = common.Score()
        score.note(1.5, 0.5, 3, 64, 90)
        self.assertEqual(sorted(score.events), [(1.5, 0x93, 64, 90), (2.0, 0x83, 64, 0)])

    def test_program_and_control_go_to_their_channel(self):
        score = common.Score()
        score.program(9, 0)
        score.control(2, 64, 127, seconds=3.0)
        self.assertEqual(score.events, [(0.0, 0xC9, 0), (3.0, 0xB2, 64, 127)])


if __name__ == "__main__":
    unittest.main()
