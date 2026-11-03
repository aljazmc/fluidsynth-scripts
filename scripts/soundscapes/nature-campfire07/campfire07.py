import numpy as np

from common import RATE, fit, normalize

# A bonfire on a windy beach.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 45
# random seed: change it for another take of the same scene
SEED = 108
# seconds of fade in and out
FADE = 2.0
# how much the fire flares and settles, 0..1
LIVELINESS = 0.6
# how far the fire dies down by the end, 0..1
DYING = 0.0
# level (dB) of the flames' roar
ROAR = -8
# top frequency (Hz) of the flames' roar
ROAR_CUTOFF = 800
# crackles a second
CRACKLES = 30
# level (dB) of the crackling
CRACKLE_LEVEL = -8
# share of crackles that are big pops, 0..1
POPS = 0.08
# level (dB) of steam from wet wood, or None
HISS = None
# seconds at which a log shifts
SETTLES = (18.0,)
# level (dB) of the wind, or None
WIND = -14
# level (dB) of crickets around the fire, or None
CRICKETS = None
# reverb length (seconds): open air is short, a stone hearth longer
ROOM = 0.5
# amount of reverb
WET = 0.05

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

WIDTH = 0.6  # how widely the crackles spread across the stereo field, 0..1


def crackle(big=False):
    """A crackle (a tiny burst of noise), or a pop of trapped sap."""
    length = rng.uniform(0.008, 0.03) if big else rng.uniform(0.001, 0.005)
    n = max(8, round(length * RATE))
    burst = rng.standard_normal(n) * decay(n, length)
    return bandpass(burst, 400, 6000) * 2 if big else bandpass(burst, 1200, 12000)


def crackles(level):
    """Crackling in clusters, as pockets of resin and moisture burst; level is
    how lively the fire is at each frame (0..1)."""
    track = np.zeros((FRAMES, 2))
    small = [crackle() for _ in range(64)]
    for at in times(CRACKLES / 4, level):  # cluster starts
        for _ in range(rng.integers(1, 8)):
            if rng.random() < POPS:
                sound = crackle(big=True)
            else:
                sound = small[rng.integers(len(small))]
            place(track, pan(sound * rng.lognormal(-0.5, 0.7), rng.uniform(-WIDTH, WIDTH)), at)
            at += rng.exponential(0.03)
    return track


def flames(level):
    """The soft roar of the flames, fluttering."""
    roar = bandpass(noise(FRAMES, 2, 2.0), 30, ROAR_CUTOFF)
    flutter = np.stack([wander(FRAMES, 8, 0.5, 1.0) for _ in range(2)], axis=1)
    return roar * flutter * level[:, None]


def hiss():
    """Steam escaping from wet wood, coming and going."""
    steam = bandpass(noise(FRAMES, 2), 2500, 7000)
    return steam * (np.clip(wander(FRAMES, 0.4, -0.5, 1.0), 0, 1) ** 2)[:, None]


def settle():
    """A log shifting: a dull thump, a flurry of crackles and the tinkle of embers."""
    n = round(RATE * 0.4)
    thump = bandpass(rng.standard_normal(n), None, 200, order=3) * bell(n, 0.1) * 0.6
    out = np.zeros((round(RATE * 2.0), 2))
    place(out, pan(thump, rng.uniform(-0.3, 0.3)), 0)
    for at in np.sort(rng.uniform(0.02, 1.5, 25)):
        place(out, pan(crackle(rng.random() < 0.2), rng.uniform(-0.5, 0.5)) * rng.uniform(0.3, 1), at)
    for at in np.sort(rng.uniform(0.1, 1.8, 6)):  # embers ringing as they fall
        k = round(RATE * 0.05)
        ping = tone(np.full(k, rng.uniform(3000, 6000))) * decay(k, 0.04) * 0.15
        place(out, pan(ping, rng.uniform(-0.5, 0.5)), at)
    return out


def crickets(level):
    """Crickets in the dark around the fire."""
    track = np.zeros((FRAMES, 2))
    for _ in range(6):
        k = round(RATE * 0.012)
        stroke = pan(tone(np.full(k, rng.uniform(4000, 5000))) * np.hanning(k), rng.uniform(-1, 1))
        interval, at = rng.uniform(0.35, 0.6), rng.uniform(0, 1)
        while at < SECONDS:
            for p in range(3):
                place(track, stroke, at + p * 0.03)
            at += interval * rng.uniform(0.95, 1.05)
    return bandpass(track, None, 7000) * db(level)


def campfire07():
    level = np.clip(1 - LIVELINESS + LIVELINESS * wander(FRAMES, 0.3), 0, 1) * np.linspace(1, 1 - DYING, FRAMES)
    mix = flames(level) * db(ROAR) + crackles(level) * db(CRACKLE_LEVEL)
    if HISS is not None:
        mix += hiss() * db(HISS)
    for at in SETTLES:
        place(mix, settle() * db(-6), at)
    if WIND is not None:
        gust = wander(FRAMES, 1 / 6) ** 2
        mix += moving_lowpass(noise(FRAMES, 2, 1.6), 120 * (2000 / 120) ** gust) * gust[:, None] * db(WIND)
    if CRICKETS is not None:
        mix += crickets(CRICKETS)
    return finish(reverb(mix, ROOM, WET), FADE)
