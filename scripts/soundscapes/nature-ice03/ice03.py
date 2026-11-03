import numpy as np

from common import RATE, fit, normalize

# Walking out on a cracking pond.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 40
# random seed: change it for another take of the same scene
SEED = 1720
# seconds of fade in and out
FADE = 2.0
# singing cracks (the laser-like pew) a second
SINGS = 0.5
# level (dB) of the singing
SING_LEVEL = -6
# (low, high) Hz the singing slides between
GLIDE = (400, 5000)
# sharp cracks a second
CRACKS = 0.6
# level (dB) of the cracks
CRACK_LEVEL = -4
# deep booms of the sheet a second
BOOMS = 0.05
# level (dB) of the booms
BOOM_LEVEL = -8
# (near, far) distance of the ice sounds, 0..1
DISTANCES = (0.0, 0.4)
# (seconds, length) of each glacier wall breaking off
CALVING = ()
# level (dB) of a cold wind, or None
WIND = None
# reverb length (seconds)
ECHO = 1.5
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


# --- the sound -------------------------------------------------------------------

def song(distance):
    """The "singing" of lake ice: a crack travelling through the sheet arrives
    as a laser-like "pew", the high frequencies first, then sliding down
    (the ice disperses the sound)."""
    low, high = GLIDE
    length = rng.uniform(0.15, 0.8) * (1 + distance)
    frames = round(length * RATE)
    t = np.arange(frames) / frames
    freq = high * rng.uniform(0.7, 1.0) * (low / high) ** (t ** 0.5)
    pew = tone(freq, (1, 0.3, 0.1)) * decay(frames, length) * np.minimum(1, t * 50)
    k = round(RATE * 0.003)
    tick = bandpass(rng.standard_normal(k) * decay(k, 0.003), 1500, None)
    return overlay(pew, 0.5 * tick)


def crack():
    """A sharp crack nearby: a burst of crackles."""
    out = np.zeros(round(RATE * 0.4))
    at = 0.0
    for _ in range(rng.integers(3, 12)):
        k = round(RATE * rng.uniform(0.002, 0.01))
        place(out, rng.standard_normal(k) * decay(k, k / RATE) * rng.uniform(0.3, 1.0), at)
        at += rng.exponential(0.02)
    return bandpass(out, 300, 10000)


def boom():
    """The deep, resonant boom of the whole sheet flexing."""
    length = rng.uniform(1.5, 4.0)
    frames = round(length * RATE)
    f0 = rng.uniform(50, 110)
    body = tone(glide(f0 * 1.3, f0, length), (1, 0.5, 0.25)) + 0.5 * bandpass(rng.standard_normal(frames), 30, 300)
    return body * decay(frames, length) * np.minimum(1, np.arange(frames) / (0.01 * RATE))


def calving(length):
    """A wall of a glacier breaking off: a long, crashing rumble."""
    frames = round(length * RATE)
    t = np.arange(frames) / RATE
    rumble = bandpass(noise(frames, 2, 1.8), 25, 1500)
    shape = np.minimum(1, t / 0.5) * np.exp(-t / (length / 3)) * wander(frames, 4, 0.5, 1.0)
    return rumble * shape[:, None]


def events(rate, make, spread, level):
    track = np.zeros((FRAMES, 2))
    for at in times(rate):
        distance = rng.uniform(*spread)
        sound = make(distance) if make is song else make()
        if distance > 0.4:
            sound = bandpass(sound, None, 9000 - 6000 * distance)
        place(track, pan(sound * (1 - 0.7 * distance) * rng.uniform(0.5, 1.0), rng.uniform(-1, 1)), at)
    return track * db(level)


def ice03():
    mix = events(SINGS, song, DISTANCES, SING_LEVEL)
    mix += events(CRACKS, crack, DISTANCES, CRACK_LEVEL)
    mix += events(BOOMS, boom, DISTANCES, BOOM_LEVEL)
    for at, length in CALVING:
        place(mix, calving(length) * db(-2), at)
    if WIND is not None:  # a cold wind over the open ice
        gust = wander(FRAMES, 1 / 9) ** 2
        mix += moving_lowpass(noise(FRAMES, 2, 1.6), 150 * (3000 / 150) ** gust) * gust[:, None] * db(WIND)
    return finish(reverb(mix, ECHO, WET), FADE)
