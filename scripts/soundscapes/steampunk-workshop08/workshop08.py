import numpy as np

from common import RATE, fit, normalize

# A cavernous railway workshop.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 50
# random seed: change it for another take of the same scene
SEED = 4957
# seconds of fade in and out
FADE = 2.0
# ratchet bursts a second
RATCHETS = 0.15
# filing a second
FILES = 0.05
# runs of hammer taps a second
TAPS = 0.2
# springs boinging a second
SPRINGS = 0.0
# level (dB) of a belt-driven lathe, or None
LATHE = -10
# (seconds it starts to heat, seconds until it whistles) of a kettle, or None
KETTLE = None
# whether a clock ticks
CLOCK = False
# reverb length (seconds)
ROOM = 2.5
# amount of reverb
WET = 0.4

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


# --- the sound -------------------------------------------------------------------

def ratchet():
    """A ratchet wrench: a burst of clicks."""
    out = np.zeros(round(RATE * 1.0))
    pawl = clank(rng.uniform(1800, 2600), 0.025)
    for k in range(rng.integers(6, 16)):
        place(out, pawl * rng.uniform(0.7, 1.0), k * rng.uniform(0.04, 0.06))
    return out


def rasp():
    """A file drawn across brass: strokes of scraping noise."""
    out = np.zeros(round(RATE * 4))
    at = 0.0
    for _ in range(rng.integers(3, 8)):
        n = round(RATE * rng.uniform(0.3, 0.5))
        stroke = bandpass(rng.standard_normal(n), 2000, 9000) * (0.5 + 0.5 * np.sin(2 * np.pi * 120 * np.arange(n) / RATE) ** 2)
        place(out, stroke * bell(n, 0.3) * 0.5, at)
        at += n / RATE + rng.uniform(0.15, 0.3)
    return out


def taps():
    """A small hammer tapping a brass fitting."""
    out = np.zeros(round(RATE * 3))
    f0 = rng.uniform(1500, 3000)
    for k in range(rng.integers(3, 10)):
        place(out, clank(f0, 0.3) * rng.uniform(0.5, 1.0), k * rng.uniform(0.2, 0.35))
    return out


def spring():
    """A spring released: a wobbling "boing"."""
    length = rng.uniform(0.4, 0.9)
    n = round(length * RATE)
    t = np.arange(n) / RATE
    f = rng.uniform(150, 400) * (1 + 0.3 * np.sin(2 * np.pi * rng.uniform(8, 14) * t) * np.exp(-t * 4))
    return tone(f, (1, 0.6, 0.4, 0.3)) * decay(n, length) * 0.5


def lathe(level):
    """A belt-driven lathe: the whine of the spindle, the hum of the belt, the tool chattering."""
    t = np.arange(FRAMES) / RATE
    spindle = tone(np.full(FRAMES, rng.uniform(180, 260)), (1, 0.5, 0.3, 0.2)) * 0.3
    belt = bandpass(noise(FRAMES, 1, 1.0), 60, 1200) * 0.5
    cutting = bandpass(noise(FRAMES, 1), 1500, 8000) * np.clip(wander(FRAMES, 0.4, -0.5, 1.0), 0, 1) ** 2
    return pan(spindle + belt + cutting, 0.5) * db(level)


def workshop08():
    mix = bandpass(noise(FRAMES, 2, 1.8), 30, 400) * db(-32)  # the room
    for make, rate, level in ((ratchet, RATCHETS, -8), (rasp, FILES, -10), (taps, TAPS, -10), (spring, SPRINGS, -10)):
        for at in times(rate):
            place(mix, pan(make() * db(level), rng.uniform(-0.8, 0.8)), at)
    if LATHE is not None:
        mix += lathe(LATHE)
    if KETTLE is not None:  # the kettle on the stove, coming to the boil and whistling
        at, length = KETTLE
        n = round(length * RATE)
        rising = bandpass(rng.standard_normal(n), 500, 5000) * np.linspace(0, 1, n) ** 2 * 0.3
        place(mix, pan(rising, -0.6), at)
        place(mix, pan(whistle(rng.uniform(1400, 1800), 4.0, (1.0, 1.01)) * 0.6, -0.6), at + length)
    if CLOCK:
        for at in np.arange(0, SECONDS, 0.5):
            place(mix, pan(clank(2400 if int(at * 2) % 2 else 2000, 0.04) * db(-26), 0.8), at)
    return finish(reverb(mix, ROOM, WET), FADE)
