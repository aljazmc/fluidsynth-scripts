import numpy as np

from common import RATE, fit, normalize

# Two humpbacks, one near, one far.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 60
# random seed: change it for another take of the same scene
SEED = 1819
# seconds of fade in and out
FADE = 2.0
# (species, position -1..1, distance 0..1, level dB) of each animal; species are "humpback", "orca" and "dolphin"
SINGERS = (('humpback', -0.5, 0.2, -2), ('humpback', 0.7, 0.8, -6))
# level (dB) of the sea's low wash, heard from below
SEA = -24
# level (dB) of the crackle of snapping shrimp on a reef, or None
SHRIMP = None
# reverb length (seconds): sound carries far under water
ECHO = 5.0
# amount of reverb
WET = 0.55

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


# --- the voices ------------------------------------------------------------------------

def unit(kind, base):
    """One unit of a humpback's song, mono."""
    if kind == "moan":  # long, low, slowly gliding
        length = rng.uniform(1.5, 3.5)
        freq = glide(base, base * rng.uniform(0.7, 1.4), length)
        harmonics = (1, 0.5, 0.3, 0.15, 0.08)
    elif kind == "whoop":  # a rising sweep
        length = rng.uniform(0.6, 1.2)
        freq = glide(base, base * rng.uniform(2.5, 4.0), length)
        harmonics = (1, 0.4, 0.2)
    elif kind == "cry":  # high and plaintive
        length = rng.uniform(0.8, 1.8)
        freq = glide(base * 4, base * rng.uniform(3, 5), length)
        harmonics = (1, 0.6, 0.4, 0.3)
    else:  # grunt: low pulses
        length = rng.uniform(0.3, 0.7)
        frames = round(length * RATE)
        pulses = np.sin(np.pi * rng.uniform(15, 30) * np.arange(frames) / RATE) ** 8
        return tone(np.full(frames, base * 0.6), (1, 0.6, 0.4, 0.3, 0.2)) * pulses * bell(frames, 0.2)
    frames = len(freq)
    freq = freq * (1 + 0.01 * np.sin(2 * np.pi * rng.uniform(3, 6) * np.arange(frames) / RATE))
    return tone(freq, harmonics) * bell(frames, rng.uniform(0.2, 0.5))


def humpback():
    """A humpback's song: a phrase of units, repeated with small changes (a
    theme), then a new theme; [(seconds, sound)] over the piece."""
    calls, at = [], rng.uniform(0, 5)
    base = rng.uniform(120, 250)
    while at < SECONDS:
        theme = [(rng.choice(["moan", "whoop", "cry", "grunt"], p=[0.4, 0.25, 0.2, 0.15]), base * 2 ** rng.uniform(-0.5, 0.5))
                 for _ in range(rng.integers(3, 6))]
        for _ in range(rng.integers(2, 4)):
            for kind, pitch in theme:
                sound = unit(kind, pitch * rng.uniform(0.97, 1.03))
                calls.append((at, sound))
                at += len(sound) / RATE + rng.uniform(0.3, 1.2)
        at += rng.uniform(2, 6)
    return calls


def orca():
    """Orca calls: pulsed, nasal tones with sudden jumps, and click trains."""
    calls, at = [], rng.uniform(0, 3)
    while at < SECONDS:
        if rng.random() < 0.7:
            length = rng.uniform(0.6, 1.5)
            frames = round(length * RATE)
            f = rng.uniform(800, 1800)
            freq = np.where(np.arange(frames) < frames * rng.uniform(0.3, 0.7), f, f * rng.uniform(1.3, 1.8))
            pulsed = 0.6 + 0.4 * np.sin(2 * np.pi * rng.uniform(200, 400) * np.arange(frames) / RATE)
            calls.append((at, tone(freq, (1, 0.7, 0.5, 0.3)) * pulsed * bell(frames, 0.2)))
            at += length + rng.uniform(1, 5)
        else:
            calls.append((at, clicks(rng.integers(10, 40), rng.uniform(5, 15))))
            at += rng.uniform(2, 5)
    return calls


def dolphin():
    """Dolphins: high whistles sweeping up and down, and clicks."""
    calls, at = [], rng.uniform(0, 2)
    while at < SECONDS:
        if rng.random() < 0.6:
            length = rng.uniform(0.4, 1.2)
            frames = round(length * RATE)
            t = np.arange(frames) / RATE
            freq = rng.uniform(7000, 11000) * (1 + 0.3 * np.sin(2 * np.pi * rng.uniform(1, 3) * t + rng.uniform(0, 6)))
            calls.append((at, tone(freq, (1, 0.2)) * bell(frames, 0.2)))
            at += length + rng.uniform(0.3, 2)
        else:
            calls.append((at, clicks(rng.integers(20, 80), rng.uniform(20, 60))))
            at += rng.uniform(1, 3)
    return calls


def clicks(count, rate):
    """An echolocation click train, mono."""
    out = np.zeros(round(RATE * (count / rate + 0.05)))
    for k in range(count):
        n = round(RATE * 0.0008)
        place(out, bandpass(rng.standard_normal(n), 2000, None) * np.hanning(n), k / rate * rng.uniform(0.95, 1.05))
    return out


SPECIES = {"humpback": humpback, "orca": orca, "dolphin": dolphin}


def whales01():
    # the sea itself, heard from below: a low wash, the surface far above
    mix = bandpass(noise(FRAMES, 2, 1.6), 20, 600) * wander(FRAMES, 0.2, 0.6, 1.0)[:, None] * db(SEA)
    if SHRIMP is not None:  # snapping shrimp: a constant crackle over a reef
        snaps = np.zeros((FRAMES, 2))
        for at in times(400):
            k = round(RATE * 0.001)
            place(snaps, pan(rng.standard_normal(k) * rng.lognormal(-1, 0.6), rng.uniform(-1, 1)), at)
        mix += bandpass(snaps, 2000, None) * db(SHRIMP)
    for species, position, distance, level in SINGERS:
        gain = db(level) * (1 - 0.6 * distance)
        for at, sound in SPECIES[species]():
            sound = bandpass(sound, None, 9000 - 6000 * distance) if distance > 0.3 else sound
            place(mix, pan(sound * gain, position + rng.uniform(-0.1, 0.1)), at)
    return finish(reverb(mix, ECHO, WET), FADE)
