import numpy as np

from common import RATE, fit, normalize

# A busy hub, trains coming and going.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 55
# random seed: change it for another take of the same scene
SEED = 3739
# seconds of fade in and out
FADE = 2.0
# level (dB) of the station's ventilation
VENTS = -18
# level (dB) of travellers waiting, or None
CROWD = -14
# (seconds, kind) of each train; kinds are "arrive", "depart" and "pass"
TRAINS = ((1.0, 'arrive'), (15.0, 'pass'), (24.0, 'depart'), (38.0, 'arrive'))
# seconds at which an announcement plays
ANNOUNCEMENTS = (10.0, 33.0)
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


# --- the sound -------------------------------------------------------------------

def train(kind):
    """A maglev train: arriving (a rising hum and rush, a falling brake
    whine), departing (the reverse), or passing through at speed."""
    length = {"arrive": 12, "depart": 10, "pass": 6}[kind]
    frames = round(length * RATE)
    t = np.arange(frames) / frames
    if kind == "arrive":
        speed = np.clip(1 - t * 1.15, 0, 1) ** 0.8
        near = np.minimum(1, t * 4)
    elif kind == "depart":
        speed = np.clip(t * 1.2 - 0.1, 0, 1) ** 1.2
        near = np.minimum(1, (1 - t) * 3)
    else:
        speed = np.ones(frames)
        near = np.exp(-((t - 0.5) / 0.15) ** 2)
    hum = tone(60 + 500 * speed, (1, 0.5, 0.3, 0.2, 0.1)) * 0.3
    whine = tone(800 + 2200 * speed, (1, 0.3)) * 0.1
    rush = bandpass(noise(frames, 1, 1.0), 100, 8000) * speed
    sound = (hum + whine + rush) * near
    if kind == "pass":  # it crosses the platform from one side to the other
        angle = (np.clip(1 - 2 * t, -1, 1) + 1) * np.pi / 4
        return np.stack((sound * np.cos(angle), sound * np.sin(angle)), axis=1)
    out = pan(sound, rng.uniform(-0.3, 0.3))
    # the doors: a soft chime and a pneumatic hiss, while it stands
    door = (0.88 if kind == "arrive" else 0.05) * length
    for k, f in enumerate((880, 1109, 1319)):
        n = round(RATE * 0.35)
        place(out, pan(tone(np.full(n, f), (1, 0.2)) * decay(n, 0.35) * 0.15, 0.0), door + k * 0.25)
    n = round(RATE * 0.8)
    place(out, pan(bandpass(rng.standard_normal(n), 1500, 8000) * bell(n, 0.1) * 0.15, 0.0), door + 0.9)
    return out


def announcement():
    """A station announcement's chime: three notes, then a synthetic voice-like drone."""
    out = []
    for f in rng.choice([523, 659, 784, 1047], 3):
        n = round(RATE * 0.3)
        out.append(tone(np.full(n, f), (1, 0.3)) * decay(n, 0.3))
    n = round(RATE * rng.uniform(2, 4))
    voice = moving_lowpass(rng.standard_normal(n), wander(n, 8, 500, 2000), bands=8)
    out.append(bandpass(voice, 300, 3000) * np.clip(wander(n, 6, -0.3, 1), 0, 1) * 0.5)
    return np.concatenate(out)


def maglev02():
    mix = bandpass(noise(FRAMES, 2, 1.6), 30, 600) * db(VENTS)  # ventilation
    if CROWD is not None:  # travellers waiting: a murmur
        murmur = sum(pan(bandpass(moving_lowpass(noise(FRAMES, 1, 1.0), wander(FRAMES, 5, 400, 1600), bands=8), 150, 3000)
                         * np.clip(wander(FRAMES, 3, -0.5, 1.0), 0, 1), rng.uniform(-1, 1)) for _ in range(6))
        mix += murmur * db(CROWD)
    for at, kind in TRAINS:
        place(mix, train(kind) * db(-2), at)
    for at in ANNOUNCEMENTS:
        place(mix, pan(announcement() * db(-12), 0.2), at)
    return finish(reverb(mix, ROOM, WET), FADE)
