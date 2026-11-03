import numpy as np

from common import RATE, fit, normalize

# An eagle owl on a rocky crag.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 50
# random seed: change it for another take of the same scene
SEED = 1316
# seconds of fade in and out
FADE = 2.0
# (species, position -1..1, distance 0..1, mean seconds between calls, level dB) of each owl; species are "tawny", "barn", "eagle", "horned" and "screech"
OWLS = (('eagle', 0.0, 0.5, 6, -4),)
# level (dB) of the low hum of the night air
NIGHT = -28
# level (dB) of the wind, or None
WIND = -26
# level (dB) of a few distant crickets, or None
CRICKETS = None
# reverb length (seconds): a canyon echoes long
ECHO = 3.0
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


# --- the calls -----------------------------------------------------------------------

def hoot(f0, length, wobble=0.0, harmonics=(1, 0.12, 0.03), fall=0.92):
    """One hoot: a soft, falling tone, maybe wavering."""
    frames = round(length * RATE)
    freq = glide(f0 * 1.04, f0 * fall, length) * (1 + 0.04 * np.sin(2 * np.pi * wobble * np.arange(frames) / RATE))
    breath = bandpass(rng.standard_normal(frames), f0 * 0.8, f0 * 2.5) * 0.08
    return (tone(freq, harmonics) + breath) * bell(frames, 0.25)


def silence(seconds):
    return np.zeros(round(seconds * RATE))


def tawny():
    """Tawny owl: a long "hoo", a pause, then a wavering "hoo-oo-oo-oo";
    or the female's sharp "ke-wick"."""
    if rng.random() < 0.3:
        frames = round(RATE * 0.35)
        f = glide(1300, 2000, 0.35)
        call = tone(f, (1, 0.6, 0.4, 0.25)) * bell(frames, 0.3)
        return bandpass(call * (1 + 0.5 * np.sign(np.sin(2 * np.pi * 70 * np.arange(frames) / RATE))), 600, 6000)
    f0 = rng.uniform(370, 430)
    return np.concatenate([hoot(f0, 0.5), silence(rng.uniform(1.5, 3.0)), hoot(f0, 0.15), silence(0.2),
                           hoot(f0 * 1.02, 1.1, wobble=9)])


def barn():
    """Barn owl: a long, harsh screech of noise."""
    length = rng.uniform(1.0, 2.0)
    frames = round(length * RATE)
    rasp = bandpass(rng.standard_normal(frames), 2000, 7000) * (0.6 + 0.4 * np.sin(2 * np.pi * rng.uniform(60, 90) * np.arange(frames) / RATE))
    shriek = tone(glide(rng.uniform(2600, 3200), rng.uniform(2200, 2600), length), (1, 0.4, 0.2)) * 0.3
    return (rasp + shriek) * bell(frames, 0.15)


def eagle():
    """Eagle owl: a deep "oo-hu", far-carrying."""
    f0 = rng.uniform(280, 330)
    return np.concatenate([hoot(f0, 0.25, harmonics=(1, 0.2, 0.05), fall=0.85), silence(0.12),
                           hoot(f0 * 0.9, 0.35, harmonics=(1, 0.2, 0.05), fall=0.8)])


def horned():
    """Great horned owl: "hoo, h'hoo — hoo — hoo", in a steady rhythm."""
    f0 = rng.uniform(250, 300)
    parts = []
    for length, gap in ((0.3, 0.2), (0.12, 0.05), (0.35, 0.5), (0.4, 0.5), (0.45, 0)):
        parts += [hoot(f0, length, harmonics=(1, 0.15, 0.04)), silence(gap)]
    return np.concatenate(parts)


def screech():
    """Eastern screech owl: a descending, trembling whinny."""
    length = rng.uniform(1.2, 2.0)
    frames = round(length * RATE)
    t = np.arange(frames) / RATE
    freq = glide(rng.uniform(900, 1050), rng.uniform(550, 650), length)
    tremble = 0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(12, 18) * t)
    return tone(freq, (1, 0.2, 0.05)) * tremble * bell(frames, 0.2)


SPECIES = {"tawny": tawny, "barn": barn, "eagle": eagle, "horned": horned, "screech": screech}


def crickets(level):
    """A few crickets far off."""
    track = np.zeros((FRAMES, 2))
    for _ in range(5):
        k = round(RATE * 0.012)
        stroke = pan(tone(np.full(k, rng.uniform(3800, 4800))) * np.hanning(k), rng.uniform(-1, 1))
        interval, at = rng.uniform(0.4, 0.7), rng.uniform(0, 1)
        while at < SECONDS:
            for p in range(3):
                place(track, stroke, at + p * 0.03)
            at += interval * rng.uniform(0.95, 1.05)
    return bandpass(track, None, 5000) * db(level)


def owls03():
    mix = bandpass(noise(FRAMES, 2, 1.8), 30, 400) * db(NIGHT)
    for species, position, distance, every, level in OWLS:
        at = rng.uniform(0.5, every)
        gain = db(level) * (1 - 0.6 * distance)
        while at < SECONDS - 2:
            call = SPECIES[species]()
            if distance > 0.3:
                call = bandpass(call, None, 7000 - 5000 * distance)
            place(mix, pan(call * gain, position + rng.uniform(-0.05, 0.05)), at)
            at += len(call) / RATE + every * rng.uniform(0.6, 1.4)
    if WIND is not None:
        gust = wander(FRAMES, 1 / 8) ** 2
        mix += moving_lowpass(noise(FRAMES, 2, 1.6), 100 * (1500 / 100) ** gust) * gust[:, None] * db(WIND)
    if CRICKETS is not None:
        mix += crickets(CRICKETS)
    return finish(reverb(mix, ECHO, WET), FADE)
