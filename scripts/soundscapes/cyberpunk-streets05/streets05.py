import numpy as np

from common import RATE, fit, normalize

# A downpour on a deserted boulevard.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 50
# random seed: change it for another take of the same scene
SEED = 3237
# seconds of fade in and out
FADE = 2.0
# level (dB) of the far traffic roar
TRAFFIC = -16
# hover cars passing, a second
PASSES = 0.15
# level (dB) of the hover cars
PASS_LEVEL = -6
# number of distant sirens
SIRENS = 1
# number of advertising jingles
CHIMES = 1
# level (dB) of people passing and talking, or None
CROWD = None
# level (dB) of rain on metal and asphalt, or None
RAIN = -10
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

def hovercar():
    """A hover car passing: an electric whine bending down as it goes by
    (Doppler), a rush of air, crossing from one side to the other."""
    length = rng.uniform(2.0, 5.0)
    frames = round(length * RATE)
    t = np.arange(frames) / frames
    f = rng.uniform(300, 1200)
    doppler = 1 + 0.06 * np.tanh(4 * (0.5 - t))
    whine = tone(f * doppler, (1, 0.5, 0.2, 0.1)) + 0.5 * tone(f * 1.5 * doppler, (1, 0.3))
    rush = bandpass(rng.standard_normal(frames), 200, 6000)
    near = np.exp(-((t - 0.5) / 0.18) ** 2)
    sound = (0.4 * whine + rush) * near
    start = rng.choice([-1, 1])
    angle = (np.clip(start * (1 - 2 * t), -1, 1) + 1) * np.pi / 4
    return np.stack((sound * np.cos(angle), sound * np.sin(angle)), axis=1)


def siren():
    """A far siren: a synthetic wail sweeping up and down."""
    length = rng.uniform(4, 9)
    frames = round(length * RATE)
    t = np.arange(frames) / RATE
    rate = rng.uniform(0.3, 1.2)
    f = rng.uniform(600, 900) * (1 + 0.35 * np.sin(2 * np.pi * rate * t))
    return bandpass(tone(f, (1, 0.5, 0.3, 0.2)), None, 2500) * bell(frames, 0.4)


def chime():
    """An advertising screen's jingle: a few bright synthetic notes."""
    root = rng.uniform(500, 900)
    parts = []
    for step in rng.choice([0, 3, 5, 7, 10, 12], rng.integers(3, 6)):
        n = round(RATE * 0.15)
        parts.append(tone(np.full(n, root * 2 ** (step / 12)), (1, 0.3, 0.1)) * decay(n, 0.15))
    return np.concatenate(parts)


def crowd(level):
    """People passing and talking: babble, without words, in shifting vowels."""
    out = np.zeros((FRAMES, 2))
    for _ in range(6):
        voice = noise(FRAMES, 1, 1.0)
        vowel = wander(FRAMES, 6, 400, 1800)
        voice = moving_lowpass(voice, vowel, bands=8) * np.clip(wander(FRAMES, 4, -0.5, 1.0), 0, 1)
        out += pan(bandpass(voice, 150, 3500), rng.uniform(-1, 1))
    return out * db(level)


def streets05():
    mix = bandpass(noise(FRAMES, 2, 1.8), 25, 800) * wander(FRAMES, 0.2, 0.7, 1.0)[:, None] * db(TRAFFIC)
    for at in times(PASSES):
        place(mix, hovercar() * db(PASS_LEVEL) * rng.uniform(0.4, 1.0), at)
    for at in np.sort(rng.uniform(0, SECONDS - 4, SIRENS)):
        place(mix, pan(siren() * db(-16), rng.uniform(-1, 1)), at)
    for at in np.sort(rng.uniform(0, SECONDS - 2, CHIMES)):
        place(mix, pan(chime() * db(-18), rng.uniform(-1, 1)), at)
    if CROWD is not None:
        mix += crowd(CROWD)
    if RAIN is not None:  # rain on metal and wet asphalt
        mix += bandpass(noise(FRAMES, 2, 0.7), 400, 9000) * db(RAIN)
        for at in times(150):
            k = round(RATE * 0.04)
            ping = tone(np.full(k, rng.uniform(1500, 4000))) * decay(k, 0.03) * 0.3
            place(mix, pan(ping * db(RAIN + 6), rng.uniform(-1, 1)), at)
    return finish(reverb(mix, 2.0, WET), FADE)
