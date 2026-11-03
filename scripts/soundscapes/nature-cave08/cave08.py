import numpy as np

from common import RATE, fit, normalize

# A narrow passage, drips close by.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 40
# random seed: change it for another take of the same scene
SEED = 1523
# seconds of fade in and out
FADE = 2.0
# (seconds between drops, pitch Hz, position -1..1, level dB) of each drip point
DRIPS = ((1.6, 1500, -0.2, -4), (2.3, 1100, 0.2, -6))
# level (dB) of the cave's low hum
HUM = -32
# level (dB) of water running somewhere below, or None
STREAM = None
# level (dB) of air moving through the cave mouth, or None
DRAFT = None
# number of bat twitters
BATS = 0
# (delay seconds, gain) of each reflection off the walls
ECHOES = ((0.02, 0.4), (0.05, 0.25))
# reverb length (seconds)
ECHO = 1.0
# amount of reverb
WET = 0.3

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


# --- the sound -------------------------------------------------------------------

def drop(pitch):
    """A drop falling into a pool: a click and a rising "plink"."""
    length = rng.uniform(0.05, 0.12)
    frames = round(length * RATE)
    f = pitch * rng.uniform(0.95, 1.05)
    plink = tone(glide(f, f * rng.uniform(1.4, 2.0), length), (1, 0.15)) * decay(frames, length)
    k = round(RATE * 0.002)
    click = bandpass(rng.standard_normal(k) * decay(k, 0.002), 1500, 9000)
    return overlay(plink, 0.4 * click)


def drips(period, pitch, position, level):
    """One drip point in the cave, falling at its own slow, nearly steady pace."""
    track = np.zeros((FRAMES, 2))
    at = rng.uniform(0, period)
    while at < SECONDS:
        place(track, pan(drop(pitch) * rng.uniform(0.7, 1.0), position), at)
        at += max(0.1, rng.normal(period, period * 0.08))
    return track * db(level)


def echoes(audio):
    """Discrete reflections off the walls: delayed, darker copies."""
    out = audio.copy()
    for delay, gain in ECHOES:
        shift = round(delay * RATE)
        if shift < len(audio):
            reflected = bandpass(audio[:len(audio) - shift], None, 4000)
            out[shift:] += gain * reflected[:, ::-1]  # the reflection arrives from the other side
    return out


def bats(count):
    """Bats' social calls: quick, high sweeps in twittering bursts."""
    track = np.zeros((FRAMES, 2))
    for at in np.sort(rng.uniform(0, SECONDS - 1, count)):
        position = rng.uniform(-1, 1)
        for k in range(rng.integers(3, 9)):
            length = rng.uniform(0.008, 0.02)
            f = rng.uniform(9000, 14000)
            chirp = tone(glide(f, f * 0.6, length)) * bell(round(length * RATE), 0.2)
            place(track, pan(chirp * db(-26), position), at + k * rng.uniform(0.03, 0.07))
    return track


def cave08():
    mix = bandpass(noise(FRAMES, 2, 2.0), 20, 120) * db(HUM)  # the cave's own low hum
    for period, pitch, position, level in DRIPS:
        mix += drips(period, pitch, position, level)
    if STREAM is not None:  # water running somewhere below
        flow = bandpass(noise(FRAMES, 2, 1.0), 200, 2500) * wander(FRAMES, 3, 0.6, 1.0)[:, None]
        mix += bandpass(flow, None, 1500) * db(STREAM)
    if DRAFT is not None:  # air moving through the cave mouth
        gust = wander(FRAMES, 1 / 10) ** 2
        mix += moving_lowpass(noise(FRAMES, 2, 1.8), 60 * (600 / 60) ** gust) * gust[:, None] * db(DRAFT)
    if BATS:
        mix += bats(BATS)
    return finish(reverb(echoes(mix), ECHO, WET), FADE)
