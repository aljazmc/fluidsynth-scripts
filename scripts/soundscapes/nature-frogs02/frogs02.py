import numpy as np

from common import RATE, fit, normalize

# A tree frog chorus.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 45
# random seed: change it for another take of the same scene
SEED = 507
# seconds of fade in and out
FADE = 2.0
# (species, count, level dB, distance 0..1) of each group; species are "peeper", "bullfrog", "treefrog", "toad" and "greenfrog"
CHORUS = (('treefrog', 10, -8, 0.5),)
# level (dB) of water lapping at the bank
WATER = -36
# amount of reverb
WET = 0.2

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


# --- the calls -----------------------------------------------------------------------
# each returns the calls of one frog over the whole piece, as (seconds, mono sound)

def formant(f0, centre, width=0.6, count=30):
    """Harmonic amplitudes of a buzz on f0, shaped by a resonance at centre Hz."""
    return tuple(float(np.exp(-0.5 * (np.log2((k + 1) * f0 / centre) / width) ** 2)) for k in range(count))


def peeper():
    """Spring peeper: a clear, rising "peep", repeated in long bouts."""
    calls, at = [], rng.uniform(0, 3)
    f0 = rng.uniform(2500, 2950)
    while at < SECONDS:
        for _ in range(rng.integers(10, 40)):
            length = rng.uniform(0.12, 0.18)
            peep = tone(glide(f0, f0 * 1.15, length), (1, 0.1))
            calls.append((at, peep * bell(len(peep), 0.7)))
            at += rng.uniform(0.5, 1.2)
        at += rng.uniform(2, 8)
    return calls


def bullfrog():
    """Bullfrog: a deep "jug-o-rum", a few in a row, then a long silence."""
    calls, at = [], rng.uniform(0, 8)
    f0 = rng.uniform(90, 130)
    while at < SECONDS:
        for _ in range(rng.integers(3, 7)):
            length = rng.uniform(0.5, 0.9)
            frames = round(length * RATE)
            buzz = tone(glide(f0 * 1.05, f0 * 0.95, length), formant(f0, 260, 0.7))
            buzz += 0.3 * tone(np.full(frames, f0), formant(f0, 1000, 0.4))
            lumps = bell(frames, 0.3) * (0.6 + 0.4 * np.sin(np.pi * 2 * np.arange(frames) / frames) ** 2)
            calls.append((at, buzz * lumps))
            at += length + rng.uniform(0.3, 0.6)
        at += rng.uniform(8, 25)
    return calls


def treefrog():
    """Tree frog: a two-part "rib-bit", a buzz of clicks shaped by the throat."""
    calls, at = [], rng.uniform(0, 3)
    f0, centre = rng.uniform(150, 250), rng.uniform(1400, 2400)
    while at < SECONDS:
        for _ in range(rng.integers(4, 16)):
            syllables = []
            for length in (rng.uniform(0.05, 0.07), rng.uniform(0.08, 0.11)):
                buzz = tone(np.full(round(length * RATE), f0), formant(f0, centre, 0.5))
                syllables += [buzz * bell(len(buzz), 0.2), np.zeros(round(RATE * 0.05))]
            calls.append((at, np.concatenate(syllables)))
            at += rng.uniform(0.6, 1.5)
        at += rng.uniform(3, 10)
    return calls


def toad():
    """American toad: a long, sweet trill of quick pulses."""
    calls, at = [], rng.uniform(0, 6)
    f0, rate = rng.uniform(1500, 2000), rng.uniform(30, 40)
    while at < SECONDS:
        length = rng.uniform(3, 12)
        frames = round(length * RATE)
        t = np.arange(frames) / RATE
        trill = tone(np.full(frames, f0), (1, 0.15)) * np.sin(np.pi * rate * t) ** 6
        calls.append((at, trill * bell(frames, 0.1)))
        at += length + rng.uniform(5, 20)
    return calls


def greenfrog():
    """Green frog: a single loose-banjo "gunk", now and then."""
    calls, at = [], rng.uniform(0, 5)
    f0 = rng.uniform(200, 380)
    while at < SECONDS:
        frames = round(RATE * 0.15)
        pluck = tone(np.full(frames, f0), (1, 0.6, 0.4, 0.25, 0.15)) * decay(frames, 0.12)
        calls.append((at, pluck))
        if rng.random() < 0.3:
            calls.append((at + 0.25, 0.7 * pluck))
        at += rng.uniform(1.5, 8)
    return calls


SPECIES = {"peeper": peeper, "bullfrog": bullfrog, "treefrog": treefrog, "toad": toad, "greenfrog": greenfrog}


def frogs02():
    mix = np.zeros((FRAMES, 2))
    for species, count, level, distance in CHORUS:
        for _ in range(count):
            position = rng.uniform(-1, 1)
            far = np.clip(distance + rng.uniform(-0.15, 0.15), 0, 1)
            gain = db(level) * (1 - 0.7 * far) * rng.uniform(0.7, 1.0)
            for at, sound in SPECIES[species]():
                if far > 0.4:
                    sound = bandpass(sound, None, 8000 - 6000 * far)
                place(mix, pan(sound * gain, position), at)
    # the water: a slow lapping at the bank
    mix += bandpass(noise(FRAMES, 2, 1.5), 40, 600) * wander(FRAMES, 0.5, 0.4, 1.0)[:, None] * db(WATER)
    return finish(reverb(mix, 1.6, WET), FADE)
