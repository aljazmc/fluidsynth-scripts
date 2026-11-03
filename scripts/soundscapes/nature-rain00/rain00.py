import numpy as np

from common import RATE, fit, normalize

# A light drizzle on leaves.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 40
# random seed: change it for another take of the same scene
SEED = 606
# seconds of fade in and out
FADE = 2.0
# what the drops land on: "leaves", "grass", "window", "roof", "tent" or "puddle"
SURFACE = 'leaves'
# drops a second that can be heard one by one, at full strength
DROPS = 60
# level (dB) of those drops
DROP_LEVEL = -6
# level (dB) of the hiss of the countless farther drops
HISS = -30
# top frequency (Hz) of that hiss
BRIGHTNESS = 9000
# how the rain develops: "steady", "rising", "falling" or "passing"
SHAPE = 'steady'
# how much the rain swells and eases, 0..1
SWELL = 0.3
# level (dB) of the low wash of a downpour, or None
RUMBLE = None
# (drips a second, pitch Hz, level dB, position -1..1) of a dripping gutter or branch, or None
DRIPS = None
# level (dB) of the wind, or None
WIND = None
# amount of reverb
WET = 0.15

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

# --- rain ----------------------------------------------------------------------

def drop_sound(surface):
    """One raindrop landing on a surface, mono."""
    size = rng.uniform(0.2, 1.0)
    frames = max(8, round(RATE * 0.003 * (0.5 + size)))
    click = rng.standard_normal(frames) * decay(frames, frames / RATE)
    if surface == "leaves":  # a bright tick, sometimes a second one as it rolls off
        sound = bandpass(click, 1800, 12000)
        if rng.random() < 0.3:
            sound = overlay(sound, np.concatenate([np.zeros(round(RATE * rng.uniform(0.01, 0.05))), 0.5 * sound]))
    elif surface == "grass":  # soft and dull
        sound = 0.7 * bandpass(np.concatenate([click, np.zeros(frames)]), 500, 4000)
    elif surface == "window":  # a sharp tap and a faint ring of the glass
        ring = round(RATE * 0.03)
        sound = overlay(bandpass(click, 2500, None),
                        0.25 * tone(np.full(ring, rng.uniform(2500, 6000))) * decay(ring, 0.025))
    elif surface == "roof":  # a tin roof: a click and a short metallic ring
        ring = round(RATE * 0.12)
        f0 = rng.uniform(500, 1100)
        partials = sum(a * tone(np.full(ring, f0 * r)) for r, a in ((1, 1), (2.32, 0.6), (4.25, 0.4), (6.63, 0.25)))
        sound = overlay(bandpass(click, 800, 9000), 0.12 * partials * decay(ring, rng.uniform(0.04, 0.1)))
    elif surface == "tent":  # a dull drum of canvas
        thud = round(RATE * 0.04)
        sound = overlay(bandpass(click, 200, 2500),
                        0.5 * tone(np.full(thud, rng.uniform(150, 300))) * decay(thud, 0.03))
    elif surface == "puddle":  # a click, and often the rising "plink" of a bubble
        sound = bandpass(click, 800, 9000)
        if rng.random() < 0.5:
            length = rng.uniform(0.015, 0.05)
            f = rng.uniform(900, 3500) / (0.5 + size)
            plink = tone(glide(f, f * rng.uniform(1.3, 2.0), length)) * decay(round(length * RATE), length)
            sound = overlay(sound, 0.4 * plink)
    else:
        raise ValueError(f"unknown surface {surface!r}")
    return sound * (0.4 + size)


def rain_shape(shape, swell):
    """How hard it rains, 0..1, one value per frame."""
    t = np.arange(FRAMES) / FRAMES
    base = {"steady": np.ones(FRAMES), "rising": 0.15 + 0.85 * t, "falling": 1 - 0.85 * t,
            "passing": np.sin(np.pi * t) ** 1.5}[shape]
    return np.clip(base * (1 - swell + swell * wander(FRAMES, 1 / 8)), 0, 1)


def drops(rate, surface, level, width=1.0):
    """Individual drops, rate a second at full strength, spread across the stereo field."""
    track = np.zeros((FRAMES, 2))
    sounds = [drop_sound(surface) for _ in range(96)]
    for at in times(rate, level):
        sound = sounds[rng.integers(len(sounds))] * rng.lognormal(-1.2, 0.6)
        place(track, pan(sound, rng.uniform(-1, 1) * width), at)
    return track


def rain_hiss(level, brightness=8000):
    """The countless drops too far away to hear one by one."""
    hiss = bandpass(noise(FRAMES, 2, 0.7), 300, brightness)
    flutter = np.stack([wander(FRAMES, 20, 0.8, 1.0) for _ in range(2)], axis=1)
    return hiss * flutter * level[:, None]


def drips(rate, pitch, position):
    """A gutter or a branch dripping, at a steady-ish pace."""
    track = np.zeros((FRAMES, 2))
    at = rng.uniform(0, 1 / rate)
    while at < SECONDS:
        length = rng.uniform(0.04, 0.08)
        f = pitch * rng.uniform(0.9, 1.1)
        plop = tone(glide(f, f * 1.8, length), (1, 0.2)) * decay(round(length * RATE), length)
        place(track, pan(plop * rng.uniform(0.6, 1.0), position + rng.uniform(-0.05, 0.05)), at)
        at += max(0.05, rng.normal(1 / rate, 0.15 / rate))
    return track


def breeze(level):
    """A little wind moving through the rain."""
    gust = wander(FRAMES, 1 / 6) ** 2
    cutoff = 150 * (1500 / 150) ** gust
    return moving_lowpass(noise(FRAMES, 2, 1.6), cutoff) * (0.3 + 0.7 * gust)[:, None] * db(level)


def rain00():
    level = rain_shape(SHAPE, SWELL)
    mix = drops(DROPS, SURFACE, level) * db(DROP_LEVEL) + rain_hiss(level, BRIGHTNESS) * db(HISS)
    if RUMBLE is not None:  # the low wash of a heavy downpour
        mix += bandpass(noise(FRAMES, 2, 1.5), 30, 300) * level[:, None] * db(RUMBLE)
    if DRIPS is not None:
        rate, pitch, drip_level, position = DRIPS
        mix += drips(rate, pitch, position) * db(drip_level)
    if WIND is not None:
        mix += breeze(WIND)
    return finish(reverb(mix, 0.8, WET), FADE)
