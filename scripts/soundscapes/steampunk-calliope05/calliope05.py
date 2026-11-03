import numpy as np

from common import RATE, Score, fit, normalize

# A brisk circus march.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 45
# random seed: change it for another take of the same scene
SEED = 5055
# seconds of fade in and out
FADE = 2.0
# beats a minute
TEMPO = 128
# MIDI note of the key's tonic (60 is middle C)
KEY = 70
# length of the tune in bars
BARS = 44
# True for three beats a bar (oom-pah-pah), False for two (a march)
WALTZ = False
# level (dB) of the steam
HISS = -26
# clicks of the valve rack a second
CLATTER = 6
# seconds at which a steam whistle blows, or None
WHISTLE_AT = None
# level (dB) of a fairground crowd, or None
CROWD = -20
# lowpass (Hz) for a calliope heard from across the fair, or None
DISTANCE = None
# reverb length (seconds)
ROOM = 1.2
# amount of reverb
WET = 0.25

# --- helpers (the same in every soundscape, copied in so this file stands alone)

FRAMES = round(SECONDS * RATE)
rng = np.random.default_rng(SEED)


def db(value):
    """Decibels to a gain factor."""
    return 10 ** (value / 20)


def pan(mono, position):
    """Equal-power pan of a mono sound; position -1 is hard left, +1 hard right."""
    angle = (np.clip(position, -1, 1) + 1) * np.pi / 4
    return np.stack((mono * np.cos(angle), mono * np.sin(angle)), axis=1)


def place(track, sound, seconds):
    """Mix a sound into a track (both mono or both stereo) at a time in seconds."""
    start = round(seconds * RATE)
    begin, end = max(start, 0), min(start + len(sound), len(track))
    if end > begin:
        track[begin:end] += sound[begin - start:end - start]


def overlay(*sounds):
    """Sum sounds of different lengths, all starting together."""
    out = np.zeros((max(len(s) for s in sounds),) + sounds[0].shape[1:])
    for sound in sounds:
        out[:len(sound)] += sound
    return out


def fast_size(frames):
    """The smallest FFT size from `frames` up made of factors 2, 3 and 5 (fast)."""
    best = 2 ** int(np.ceil(np.log2(max(frames, 1))))
    p5 = 1
    while p5 < best:
        p35 = p5
        while p35 < best:
            size = p35 * 2 ** max(0, int(np.ceil(np.log2(frames / p35))))
            best = min(best, size)
            p35 *= 3
        p5 *= 5
    return best


def response_filter(signal, response):
    """Zero-phase filter along time; response maps frequencies (Hz) to gains."""
    frames = len(signal)
    size = fast_size(frames)
    gain = response(np.fft.rfftfreq(size, 1 / RATE))
    if signal.ndim == 2:
        gain = gain[:, None]
    return np.fft.irfft(np.fft.rfft(signal, size, axis=0) * gain, n=size, axis=0)[:frames]


def bandpass(signal, low=None, high=None, order=2):
    """A Butterworth-shaped band: low and/or high cutoff in Hz, None for open."""
    def response(freqs):
        gain = np.ones_like(freqs)
        if high:
            gain /= np.sqrt(1 + (freqs / high) ** (2 * order))
        if low:
            gain /= np.sqrt(1 + (low / np.maximum(freqs, 1e-3)) ** (2 * order))
        return gain
    return response_filter(signal, response)


def resonance(signal, centre, width=0.5, gain_db=6.0):
    """Boost (or cut, with a negative gain) the band around centre Hz; width in octaves."""
    def response(freqs):
        octaves = np.log2(np.maximum(freqs, 1) / centre)
        return 1 + (db(gain_db) - 1) * np.exp(-0.5 * (octaves / width) ** 2)
    return response_filter(signal, response)


def noise(frames, channels=2, color=0.0):
    """Noise with a 1/f**color power spectrum (0 white, 1 pink, 2 brown) and an
    RMS of 1; one channel gives a 1-D array."""
    signal = rng.standard_normal((frames, channels))
    if color:
        signal = response_filter(signal, lambda f: np.maximum(f, 20.0) ** (-color / 2))
    signal /= np.sqrt(np.mean(signal ** 2))
    return signal[:, 0] if channels == 1 else signal


def wander(frames, rate, low=0.0, high=1.0):
    """A smooth random line between low and high, changing about `rate` times a second."""
    points = max(2, int(frames / RATE * rate) + 2)
    values = rng.uniform(low, high, points)
    x = np.linspace(0, points - 1.000001, frames)
    i = x.astype(int)
    s = (1 - np.cos(np.pi * (x - i))) / 2
    return values[i] + (values[i + 1] - values[i]) * s


def moving_lowpass(signal, cutoff, bands=12, low=40.0, high=18000.0):
    """A lowpass whose cutoff (Hz, one value per frame) moves: the signal is
    split into bands, each faded in and out as the cutoff passes it."""
    frames = len(signal)
    size = fast_size(frames)
    spectrum = np.fft.rfft(signal, size, axis=0)
    freqs = np.fft.rfftfreq(size, 1 / RATE)
    edges = np.concatenate(([0.0], np.geomspace(low, high, bands - 1), [RATE]))
    out = np.zeros_like(signal)
    for k in range(bands):
        mask = (freqs >= edges[k]) & (freqs < edges[k + 1])
        part = np.fft.irfft(spectrum * (mask[:, None] if signal.ndim == 2 else mask), n=size, axis=0)[:frames]
        centre = np.sqrt(max(edges[k], 20.0) * min(edges[k + 1], 20000.0))
        weight = 1 / np.sqrt(1 + (centre / np.maximum(cutoff, 1.0)) ** 4)
        out += part * (weight[:, None] if signal.ndim == 2 else weight)
    return out


def decay(frames, seconds):
    """An exponential decay falling 60 dB over `seconds`."""
    return np.exp(-6.9 * np.arange(frames) / RATE / seconds)


def glide(f0, f1, seconds):
    """Frequencies gliding exponentially from f0 to f1, one per frame."""
    frames = max(1, round(seconds * RATE))
    return f0 * (f1 / f0) ** (np.arange(frames) / max(frames - 1, 1))


def tone(freq, harmonics=(1.0,)):
    """A tone following freq (Hz, one value per frame), with harmonic amplitudes."""
    phase = 2 * np.pi * np.cumsum(freq) / RATE + rng.uniform(0, 2 * np.pi)
    return sum(a * np.sin((k + 1) * phase) for k, a in enumerate(harmonics) if a)


def bell(frames, attack=0.5):
    """A smooth envelope rising for `attack` of its length, then falling."""
    t = np.linspace(0, 1, frames)
    up = np.sin(np.pi / 2 * np.minimum(t / attack, 1)) ** 2 if attack > 0 else np.ones(frames)
    down = np.cos(np.pi / 2 * np.clip((t - attack) / (1 - attack), 0, 1)) ** 2 if attack < 1 else np.ones(frames)
    return up * down


def times(rate, level=None, start=0.0, end=None):
    """Event times (s) of a random process with `rate` events a second, thinned
    by a per-frame level curve in 0..1."""
    end = SECONDS if end is None else end
    count = rng.poisson(max(rate, 0) * max(end - start, 0))
    at = np.sort(rng.uniform(start, end, count))
    if level is not None:
        at = at[rng.random(len(at)) < level[np.minimum((at * RATE).astype(int), len(level) - 1)]]
    return at


def reverb(audio, seconds=1.2, wet=0.2):
    """Convolve with an exponentially decaying noise burst (FFT based)."""
    t = np.arange(round(seconds * RATE)) / RATE
    impulse = rng.standard_normal((len(t), 2)) * np.exp(-6.9 * t / seconds)[:, None]
    impulse /= np.sqrt(np.sum(impulse ** 2, axis=0))
    size = fast_size(len(audio) + len(impulse) - 1)
    tail = np.fft.irfft(np.fft.rfft(audio, size, axis=0) * np.fft.rfft(impulse, size, axis=0), size, axis=0)
    return audio + wet * fit(tail, len(audio))


def finish(mix, fade=2.0, crest=20.0):
    """Fade in and out, round off the rare peaks more than `crest` dB above the
    average level (a lone crackle or drop would otherwise set the volume of the
    whole piece), then normalize."""
    frames = len(mix)
    ramp = np.minimum(1, np.minimum(np.arange(frames), frames - 1 - np.arange(frames)) / (fade * RATE))
    mix = mix * ramp[:, None]
    ceiling = np.sqrt(np.mean(mix ** 2)) * db(crest)
    if ceiling > 0:
        mix = ceiling * np.tanh(mix / ceiling)
    return normalize(mix)

# --- steam and brass (the same in every steampunk soundscape) ------------------------

def hiss(length, low=1500, high=10000, attack=0.02):
    """A jet of steam: a bright hiss, quick to start, dying away."""
    n = max(8, round(length * RATE))
    jet = bandpass(rng.standard_normal(n), low, high)
    return jet * np.minimum(1, np.arange(n) / (attack * RATE)) * decay(n, length)


def clank(f0, length=0.4, ratios=(1, 2.76, 5.40, 8.93)):
    """Struck metal: a click and a ring of inharmonic partials (a bar or plate)."""
    n = round(length * RATE)
    ring = sum(tone(np.full(n, f0 * r)) * decay(n, length / (1 + 0.6 * k)) / (1 + k)
               for k, r in enumerate(ratios))
    k = round(RATE * 0.003)
    click = bandpass(rng.standard_normal(k) * decay(k, 0.003), 800, None)
    return overlay(0.5 * ring, click)


def thud(length=0.3, cutoff=200):
    """A heavy, dull blow."""
    n = round(length * RATE)
    return bandpass(rng.standard_normal(n), 20, cutoff, order=3) * decay(n, length) * np.minimum(1, np.arange(n) / 40)


def whistle(f, length, pipes=(1.0, 1.26, 1.5)):
    """A steam whistle: a few pipes sounding a chord, breathy, with a swell."""
    n = round(length * RATE)
    t = np.arange(n) / RATE
    sound = sum(tone(np.full(n, f * r) * (1 + 0.004 * np.sin(2 * np.pi * 5 * t)), (1, 0.3, 0.1)) for r in pipes)
    breath = bandpass(rng.standard_normal(n), f * 0.8, f * 4) * 0.4
    swell = np.minimum(1, t / 0.15) * np.minimum(1, (length - t) / 0.3)
    return (sound / len(pipes) + breath) * swell


# --- the music ---------------------------------------------------------------------

CALLIOPE = 82  # General MIDI "Lead 3 (calliope)", zero-based
MAJOR = (0, 2, 4, 5, 7, 9, 11)


def tune():
    """A new tune each time (from the seed): a melody wandering by steps
    over the chords of the key, with an oom-pah (or oom-pah-pah) bass."""
    beats = 3 if WALTZ else 2
    beat = 60 / TEMPO
    progression = (0, 3, 4, 0, 5, 3, 4, 0)  # chord roots, as scale degrees
    melody, bass = [], []
    degree = 7
    for bar in range(BARS):
        root = progression[bar % len(progression)]
        chord = {root % 7, (root + 2) % 7, (root + 4) % 7}
        at = bar * beats * beat
        for k in range(beats):
            for half in range(2):
                if rng.random() < 0.35 and half:
                    continue  # a longer note
                degree += rng.choice([-2, -1, -1, 1, 1, 2])
                degree = int(np.clip(degree, 4, 14))
                if k == 0 and half == 0 and degree % 7 not in chord:
                    degree += 1 if (degree + 1) % 7 in chord else -1
                length = beat / 2 if half or rng.random() < 0.5 else beat
                melody.append((at + k * beat + half * beat / 2, length * 0.9, degree))
        bass.append((at, beat * 0.8, root - 7))
        for k in range(1, beats):
            bass.append((at + k * beat, beat * 0.5, root - 7 + 2 + (k % 2) * 2))
    return melody, bass


def midi(degree):
    octave, step = divmod(degree, 7)
    return KEY + 12 * octave + MAJOR[step]


def music():
    score = Score()
    for channel, (volume, pan_) in enumerate(((110, 54), (90, 74))):
        score.program(channel, CALLIOPE)
        score.control(channel, 7, volume)
        score.control(channel, 10, pan_)
        score.control(channel, 91, 40)
    melody, bass = tune()
    start = 2.0
    for at, length, degree in melody:
        score.note(start + at, length, 0, midi(degree), int(rng.integers(90, 115)))
    for at, length, degree in bass:
        score.note(start + at, length, 1, midi(degree), int(rng.integers(75, 95)))
    return score.render(SECONDS), start + max(at + length for at, length, _ in melody)


def calliope05():
    audio, end = music()
    mix = audio * 3
    # the steam that sounds the pipes, and the clatter of the valve rack
    mix += bandpass(noise(FRAMES, 2), 1500, 9000) * db(HISS)
    for at in times(CLATTER):
        if at < end:
            place(mix, pan(clank(rng.uniform(1500, 3000), 0.03) * db(-26), rng.uniform(-0.5, 0.5)), at)
    if WHISTLE_AT is not None:
        place(mix, pan(whistle(rng.uniform(500, 700), 2.0) * db(-6), 0.3), WHISTLE_AT)
    if CROWD is not None:  # a fair around it: a murmur of people
        murmur = sum(pan(bandpass(moving_lowpass(noise(FRAMES, 1, 1.0), wander(FRAMES, 5, 400, 1600), bands=8), 150, 3000)
                         * np.clip(wander(FRAMES, 3, -0.5, 1.0), 0, 1), rng.uniform(-1, 1)) for _ in range(5))
        mix += murmur * db(CROWD)
    if DISTANCE:
        mix = bandpass(mix, None, DISTANCE)
    return finish(reverb(mix, ROOM, WET), FADE)
