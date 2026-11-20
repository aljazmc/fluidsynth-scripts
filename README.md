# fluidsynth-scripts

Python scripts that make music and soundscapes with FluidSynth and NumPy,
and a shell script that encodes them with FFmpeg into WAV, FLAC, MP3, Opus
and about fifteen other audio formats. Each piece is a self-contained
project in `scripts/` with AI-generated code.

## Requirements

- Python 3 with [NumPy](https://numpy.org/)
- FluidSynth, with `fluidsynth` on the `PATH`
- A General MIDI soundfont, by default
  `/usr/share/sounds/sf2/FluidR3_GM.sf2` (on Debian and Ubuntu, the
  `fluid-soundfont-gm` package); set `SOUNDFONT` to use another one
- FFmpeg, with `ffmpeg` on the `PATH`, built with the encoders of the
  formats you want (`libmp3lame`, `libvorbis`, `libopus`, …)

## Usage

```sh
./project.sh <project> <format>          # build one format
./project.sh <project> all               # build every format
./project.sh all <format>                # build every project
./project.sh <group> all <format>        # build every project of a group
./project.sh <project> <format> clean    # remove one output
./project.sh <project> clean             # remove all outputs of a project
./project.sh clean                       # remove build/ and npy/
```

For example:

```sh
./project.sh simplified/beethoven-fur-elise mp3
./project.sh soundscapes all flac
SOUNDFONT=/usr/share/sounds/sf2/TimGM6mb.sf2 ./project.sh simplified/beethoven-fur-elise wav
```

A project is named by its path inside `scripts/`, and a group is a folder
of projects, such as `simplified` or `soundscapes`. Outputs stay flat:
`simplified/<name>` goes to `build/<name>.<format>`, and other groups keep
their name as a prefix, e.g. `soundscapes/nature-rain00` goes to
`build/soundscapes-nature-rain00.<format>`. Existing outputs are skipped,
so clean them to rebuild. Run `./project.sh` from the repository root.
Without arguments, it prints the usage with every format and group and
the first ten projects; `ls scripts/*/` lists them all.

### Formats

`aac ac3 aiff alac au caf dts eac3 flac m4a mka mp2 mp3 ogg opus tta w64
wav wma wv npy`

All audio is rendered as 48 kHz stereo floats and encoded by FFmpeg:

- **PCM**: `wav` and `au` (16-bit), `aiff`, `caf` and `w64` (24-bit).
- **Lossless compressed**: `flac` (24-bit), `mka` (FLAC in Matroska),
  `alac` (written as `build/<name>-alac.m4a`, so it doesn't clash with
  `m4a`), `tta` and `wv`.
- **Lossy**: `aac` and `m4a` (AAC), `ac3`, `dts`, `eac3`, `mp2`, `mp3`,
  `ogg` (Vorbis), `opus` and `wma`.
- **`npy`** saves the raw float32 array of shape `(frames, 2)` to
  `npy/<name>.npy`, to load it with `numpy.load()` and process it further.

## How it works

```
project.sh ──> python3 scripts/export<format>.py <project>
                                    │
                                    ▼
                             scripts/common.py
                                    │ load_project()
                                    ▼
    scripts/<project>/<name>.py: <name>() -> float array (frames, 2)
       │ Score: MIDI events ──> fluidsynth -F raw ──> NumPy
       │ and/or NumPy synthesis, mixing, reverb
                                    │ ffmpeg_export()
                                    ▼
                  ffmpeg -f f32le -i pipe:0 -c:a <codec> ...
```

- `project.sh` checks the arguments and runs `scripts/export<format>.py`
  (or `scripts/savenpy.py`) with the project as its argument.
- `scripts/common.py` imports the project, calls its function, checks the
  shape of the audio and clips it to ±1. It also holds the shared tools:
  `Score`, which collects notes and controller changes in seconds, writes
  them as a MIDI file and renders it offline with FluidSynth through the
  soundfont, and `fit()` and `normalize()` for NumPy audio.
- Each `scripts/export<format>.py` pipes the audio into FFmpeg with the
  codec and quality settings of one format.

## Projects

A project is a folder holding `<name>.py` with a function `<name>()`,
where `<name>` is the part of the folder name after its last hyphen. It
returns a float array of shape `(frames, 2)` at 48 kHz. A project needs
nothing outside its folder, apart from `scripts/common.py`.

### Simplified

Simplified arrangements of classical music in the public domain, played
by FluidSynth's General MIDI instruments:

```
scripts/simplified/beethoven-fur-elise/
├── elise.py   # elise(): tempi, dynamics and the order of the passages
├── piano.py   # a small text notation for piano music, played through Score
└── score.py   # the music, one notation string per bar
```

| Project | Played by |
|---|---|
| beethoven-fur-elise | piano |
| holst-the-planets-01-mars-the-bringer-of-war | orchestra |
| holst-the-planets-02-venus-the-bringer-of-peace | orchestra |
| holst-the-planets-03-mercury-the-winged-messenger | orchestra |
| holst-the-planets-04-jupiter-the-bringer-of-jollity | orchestra |
| holst-the-planets-05-saturn-the-bringer-of-old-age | orchestra |
| holst-the-planets-06-uranus-the-magician | orchestra |
| holst-the-planets-07-neptune-the-mystic | orchestra |

The notation (see the docstring of `piano.py`) writes notes, chords,
rests, ties, staccato, accents, dynamics with hairpins, meters and pedal
changes as text, e.g. `!mf c4 eb4:1/2 f#3+a3+d4:1.5 |`. The scores were
transcribed bar by bar from braille music. `orchestra.py` gives each part
its own General MIDI instrument, channel and pan; sustained instruments
follow the dynamics through MIDI expression (CC11), struck and plucked
ones through note velocity.

### Soundscapes

Fifty ambient scenes in three themes, each in ten takes (`00` to `09`),
named `soundscapes/<theme>-<scene><take>`:

| Theme | Scenes |
|---|---|
| cyberpunk | club, drones, factory, maglev, neon, reactor, servers, streets, terminal, traffic |
| nature | bamboo, bees, campfire, cave, chirping, cicadas, crickets, dunes, frogs, geese, geyser, hail, ice, jungle, loons, owls, rain, rockfall, savanna, seals, stags, stream, thunderstorm, volcano, waterfall, waves, whales, whitewater, wind, wolves |
| steampunk | airship, automaton, boiler, calliope, clockwork, engine, foundry, locomotive, telegraph, workshop |

Each soundscape is a single file that starts with its settings: length,
random seed, fades, levels, and the position, distance and timing of each
sound source. Most are synthesized with NumPy alone (noise, filters,
oscillators, panning and reverb); `chirping`, `waves` and `calliope` also
play General MIDI instruments through `Score`. Change the `SEED` for
another take of the same scene.

## Tests

```sh
bash tests/test_project.sh             # project.sh
python3 -m unittest discover tests     # the Python scripts
```

The tests need only bash and Python's standard library, and none of them
runs the application or writes outputs. `tests/test_project.sh` checks
that `project.sh` rejects bad arguments with its usage and exit code 1.
`tests/test_common.py` checks `varlen()`, the MIDI variable-length
numbers, against the examples in the Standard MIDI File specification.

To lint the code with [ShellCheck](https://www.shellcheck.net/) and
[Ruff](https://docs.astral.sh/ruff/):

```sh
shellcheck project.sh tests/*.sh
ruff check .
```

## Gallery

`simplified/beethoven-fur-elise`, exported with
`./project.sh simplified/beethoven-fur-elise mp3` and the FluidR3_GM
soundfont. Click the waveform to listen:

[![beethoven-fur-elise](gallery/beethoven-fur-elise.png)](gallery/beethoven-fur-elise.mp3)

▶ [beethoven-fur-elise.mp3](gallery/beethoven-fur-elise.mp3) (2:56)

## License

The scripts are licensed under the MIT license, see [LICENSE](LICENSE).
The files in `gallery/` were made with them and are under the same
license. The music they arrange (Beethoven, Holst) is in the public
domain.

The scripts drive software and use sounds that are not part of this
repository and have licenses of their own:

- [FluidSynth](https://github.com/FluidSynth/fluidsynth/blob/master/LICENSE)
  is licensed under the GNU Lesser General Public License, version 2.1
  or later. The scripts only run it as a separate program.
- Soundfonts: the default
  [FluidR3_GM](https://packages.debian.org/stable/fluid-soundfont-gm)
  soundfont by Frank Wen is licensed under the MIT license. Other
  soundfonts have their own licenses, e.g. TimGM6mb is under the GNU GPL,
  version 2; check the license of the soundfont you use before you
  publish what you render with it.
- [NumPy](https://numpy.org/doc/stable/license.html) is licensed under
  the BSD 3-Clause license.
- [FFmpeg](https://ffmpeg.org/legal.html) is licensed under the GNU LGPL,
  version 2.1 or later, or the GNU GPL, version 2 or later, depending on
  how it was built.
