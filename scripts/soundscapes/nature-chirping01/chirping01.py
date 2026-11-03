import numpy as np

from common import RATE, Score, fit, normalize

# A dawn chorus in the woods.

# --- settings -------------------------------------------------------------------

# length of the soundscape
SECONDS = 45
# random seed: change it for another take of the same scene
SEED = 203
# seconds of fade in and out
FADE = 2.0
# FluidSynth channels of a distant flock (General MIDI Bird Tweet), or 0
FLOCK = 6
# level (dB) of the wind, or None
WIND = -30
# reverb length (seconds)
REVERB = 1.6
# amount of reverb
WET = 0.25
# (song, position -1..1, distance 0..1, mean seconds between songs, level dB) of each bird; songs are "sparrow", "warbler", "tit", "whistler", "cuckoo", "dove", "woodpecker", "blackbird", "finch"
BIRDS = (
    ('blackbird', -0.5, 0.3, 4.0, -6),
    ('finch', 0.6, 0.4, 5.0, -8),
    ('tit', -0.1, 0.3, 4.0, -8),
    ('warbler', 0.3, 0.5, 5.0, -9),
    ('sparrow', -0.8, 0.6, 3.0, -10),
    ('whistler', 0.9, 0.7, 7.0, -10),
    ('cuckoo', -0.3, 0.9, 12.0, -10),
)

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


# --- voices ------------------------------------------------------------------------

BIRD_TWEET = 123  # General MIDI program, zero-based


def sweep(f0, f1, duration, vibrato=0.0, vibrato_rate=0.0, harmonic=0.15):
    """A single chirp: an exponential glide from f0 to f1 under a smooth bell."""
    t = np.arange(round(duration * RATE)) / RATE
    freq = f0 * (f1 / f0) ** (t / duration)
    freq *= 1 + vibrato * np.sin(2 * np.pi * vibrato_rate * t)
    phase = 2 * np.pi * np.cumsum(freq) / RATE
    envelope = np.sin(np.pi * t / duration) ** 2
    return envelope * (np.sin(phase) + harmonic * np.sin(2 * phase))


def phrase(parts):
    """Join (gap seconds, sound) pairs into one mono phrase."""
    parts = list(parts)
    out = np.zeros(sum(round(gap * RATE) + len(s) for gap, s in parts) + 1)
    at = 0
    for gap, sound in parts:
        at += round(gap * RATE)
        out[at:at + len(sound)] += sound
        at += len(sound)
    return out


def sparrow():
    """Quick up-down chips."""
    parts = []
    for _ in range(rng.integers(3, 7)):
        low, high = rng.uniform(2500, 3200), rng.uniform(4200, 5200)
        parts.append((0.04, sweep(low, high, 0.035)))
        parts.append((0.0, sweep(high, low, 0.045)))
    return phrase(parts)


def warbler():
    """A fast trill of falling notes that speeds up and drops in pitch."""
    count = rng.integers(8, 16)
    top = rng.uniform(6000, 7000)
    return phrase((0.07 * (1 - 0.3 * i / count), sweep(top * (1 - 0.15 * i / count), 3800, 0.04))
                  for i in range(count))


def tit():
    """Two-note "tea-cher" call, repeated."""
    high, low = rng.uniform(5200, 5800), rng.uniform(3800, 4200)
    parts = []
    for _ in range(rng.integers(3, 5)):
        parts.append((0.08, sweep(high, high * 1.05, 0.11)))
        parts.append((0.03, sweep(low, low * 0.97, 0.13)))
    return phrase(parts)


def whistler():
    """A slow, rising whistle with a warbling vibrato."""
    start = rng.uniform(2000, 2400)
    return phrase([(0.0, sweep(start, start * 1.45, rng.uniform(0.5, 0.8), 0.02, 28, 0.05)),
                   (0.12, sweep(start * 1.3, start * 0.95, 0.25, 0.015, 28, 0.05))])


def cuckoo():
    """"Cu-coo", a falling third, a few times over."""
    high = rng.uniform(650, 760)
    parts = []
    for _ in range(rng.integers(2, 6)):
        parts.append((0.45, sweep(high, high * 0.99, 0.22, harmonic=0.05)))
        parts.append((0.1, sweep(high * 0.8, high * 0.78, 0.32, harmonic=0.05)))
    return phrase(parts)


def dove():
    """A collared dove's "coo-COO-coo": soft, low and hollow."""
    base = rng.uniform(430, 520)
    return phrase([(0.0, sweep(base, base * 1.05, 0.35, 0.01, 6, 0.25)),
                   (0.08, sweep(base * 1.1, base * 1.02, 0.6, 0.01, 6, 0.25)),
                   (0.12, sweep(base, base * 0.95, 0.45, 0.01, 6, 0.25))])


def woodpecker():
    """Drumming on a dead branch: quick knocks, fading."""
    count = rng.integers(14, 26)
    rate = rng.uniform(15, 22)
    centre = rng.uniform(900, 1800)
    parts = []
    for i in range(count):
        n = round(RATE * 0.012)
        knock = resonance(bandpass(rng.standard_normal(n) * decay(n, 0.01), 300, 4000), centre, 0.4, 12)
        parts.append((1 / rate - n / RATE if i else 0.0, knock * (1 - 0.5 * i / count) * 0.6))
    return phrase(parts)


def blackbird():
    """A mellow, wandering song of fluted notes, each phrase different."""
    parts = []
    note = rng.uniform(1600, 2600)
    for _ in range(rng.integers(4, 9)):
        note = np.clip(note * 2 ** (rng.integers(-4, 5) / 12), 1400, 3200)
        length = rng.uniform(0.08, 0.3)
        parts.append((rng.uniform(0.02, 0.08), sweep(note, note * rng.uniform(0.9, 1.15), length, 0.01, 22, 0.1)))
    return phrase(parts)


def finch():
    """A chaffinch: a falling run that speeds up, then a quick flourish."""
    count = rng.integers(8, 14)
    top = rng.uniform(5500, 6500)
    parts = [(0.09 * (1 - 0.5 * i / count), sweep(top * 0.97 ** i, top * 0.97 ** i * 0.85, 0.05))
             for i in range(count)]
    parts.append((0.03, sweep(3500, 6000, 0.08)))
    parts.append((0.0, sweep(6000, 3000, 0.12)))
    return phrase(parts)


SONGS = {"sparrow": sparrow, "warbler": warbler, "tit": tit, "whistler": whistler, "cuckoo": cuckoo,
         "dove": dove, "woodpecker": woodpecker, "blackbird": blackbird, "finch": finch}


def songbirds():
    track = np.zeros((FRAMES, 2))
    for song, position, distance, interval, level in BIRDS:
        at = rng.uniform(0, interval)
        while at < SECONDS:
            sound = SONGS[song]()
            if distance > 0.5:
                sound = bandpass(sound, None, 9000 - 6000 * distance)
            gain = db(level) * (1 - 0.6 * distance)
            place(track, pan(sound * gain, position), at)
            at += len(sound) / RATE + rng.exponential(interval)
    return track


def flock():
    """Distant tweets from FluidSynth, spread across channels panned apart."""
    score = Score()
    for channel in range(FLOCK):
        score.program(channel, BIRD_TWEET)
        score.control(channel, 7, 70)  # volume
        score.control(channel, 10, round(np.interp(channel, (0, max(FLOCK - 1, 1)), (10, 117))))
        score.control(channel, 91, 100)  # reverb send
        at = rng.uniform(0, 4)
        while at < SECONDS - 1:
            for _ in range(rng.integers(1, 4)):
                score.note(at, rng.uniform(0.15, 0.6), channel, int(rng.integers(72, 97)), int(rng.integers(40, 80)))
                at += rng.uniform(0.1, 0.3)
            at += rng.exponential(3.5)
    return score.render(SECONDS)


def wind():
    """Brownish noise for leaves, swelling in slow gusts."""
    t = np.arange(FRAMES) / RATE
    gusts = 0.6 + 0.4 * np.sin(2 * np.pi * t / 11) * np.sin(2 * np.pi * t / 4.3 + 1)
    return noise(FRAMES, 2, 1.6) * gusts[:, None] * db(WIND) * 0.25


def chirping01():
    mix = songbirds()
    if FLOCK:
        mix += 2.5 * flock()
    mix = reverb(mix, REVERB, WET)
    if WIND is not None:
        mix += wind()
    return finish(mix, FADE)
