import numpy as np

from common import RATE, fit, normalize

# A heavy forge, slow and huge.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 50
# random seed: change it for another take of the same scene
SEED = 3641
# seconds of fade in and out
FADE = 2.0
# level (dB) of the plant's machine drone
DRONE = -8
# mains frequency (Hz)
MAINS = 50
# seconds between strokes of the hydraulic press, or 0 for none
PRESS_PERIOD = 6.0
# robot arms
ARMS = 0
# conveyor clacks a second, or 0
CONVEYOR = 0
# welding arcs a second
WELDS = 0.1
# (seconds between, level dB) of a warning tone, or None
ALARM = None
# reverb length (seconds): a big hall rings long
ROOM = 3.0
# amount of reverb
WET = 0.45

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

def servo(length):
    """A robot arm moving: servo whine gliding up as it speeds, down as it stops."""
    frames = round(length * RATE)
    t = np.arange(frames) / frames
    f = rng.uniform(300, 900)
    speed = np.sin(np.pi * t) ** 0.7
    whine = tone(f * (0.6 + 0.8 * speed), (1, 0.5, 0.3, 0.15))
    gears = bandpass(rng.standard_normal(frames), 1500, 7000) * 0.2
    return (whine * 0.3 + gears) * speed


def press():
    """A hydraulic press: the hiss of the stroke and a heavy, metallic slam."""
    out = np.zeros((round(RATE * 1.5), 2))
    n = round(RATE * 0.4)
    hiss = bandpass(rng.standard_normal(n), 1500, 9000) * bell(n, 0.7) * 0.4
    place(out, pan(hiss, 0.0), 0)
    k = round(RATE * 0.8)
    slam = (bandpass(rng.standard_normal(k), 30, 2000) * decay(k, 0.25)
            + sum(a * tone(np.full(k, f)) for f, a in ((110, 1), (247, 0.6), (523, 0.3))) * decay(k, 0.5) * 0.4)
    place(out, pan(slam, 0.0), 0.4)
    return out


def clack():
    """A conveyor link passing over the roller."""
    k = round(RATE * 0.03)
    return bandpass(rng.standard_normal(k) * decay(k, 0.015), 400, 5000)


def weld():
    """An arc welder: a buzzing, sizzling crackle."""
    length = rng.uniform(0.5, 3.0)
    frames = round(length * RATE)
    sizzle = bandpass(rng.standard_normal(frames), 1500, 12000) * (rng.random(frames) < 0.2)
    buzz = tone(np.full(frames, 2 * MAINS), (1, 0.6, 0.4, 0.3)) * 0.2
    return (sizzle + buzz) * bell(frames, 0.05)


def factory05():
    # the plant: a big, steady machine drone
    mix = bandpass(noise(FRAMES, 2, 1.6), 30, 1200) * db(DRONE)
    mix += pan(tone(np.full(FRAMES, 2 * MAINS), (1, 0.5, 0.3, 0.2)), 0.0) * db(DRONE - 8)
    if PRESS_PERIOD:
        at = rng.uniform(0, PRESS_PERIOD)
        position = rng.uniform(-0.5, 0.5)
        while at < SECONDS - 1.5:
            sound = press()
            place(mix, np.stack((sound[:, 0] * (1 - position) / 2 * 2, sound[:, 1] * (1 + position) / 2 * 2), 1) * db(-6), at)
            at += PRESS_PERIOD
    for _ in range(ARMS):
        position, at = rng.uniform(-1, 1), rng.uniform(0, 3)
        while at < SECONDS - 3:
            length = rng.uniform(0.6, 2.5)
            place(mix, pan(servo(length) * db(-10), position), at)
            at += length + rng.uniform(0.3, 2.0)
    if CONVEYOR:
        position = rng.uniform(-0.8, 0.8)
        for at in np.arange(0, SECONDS, 1 / CONVEYOR):
            place(mix, pan(clack() * db(-16) * rng.uniform(0.8, 1.0), position), at)
    for at in times(WELDS):
        place(mix, pan(weld() * db(-14), rng.uniform(-1, 1)), at)
    if ALARM is not None:  # a warning tone, on and off
        period, level = ALARM
        for at in np.arange(rng.uniform(0, period), SECONDS - 1, period):
            n = round(RATE * 0.4)
            place(mix, pan(tone(np.full(n, 960), (1, 0, 0.3)) * bell(n, 0.05) * db(level), 0.6), at)
    return finish(reverb(mix, ROOM, WET), FADE)
