import numpy as np

from common import RATE, Score, fit, normalize

# A morning meadow: wind in the leaves, a handful of synthesized birds singing
# around the listener, and a distant flock played by FluidSynth's General MIDI
# "Bird Tweet" patch.
SECONDS = 30
FRAMES = SECONDS * RATE
SEED = 2026

FADE = 2.0  # seconds of fade in/out
REVERB = 1.2  # seconds of reverb tail

BIRD_TWEET = 123  # General MIDI program, zero-based
FLOCK_CHANNELS = 6

rng = np.random.default_rng(SEED)


def db(value):
    return 10 ** (value / 20)


def pan(mono, position):
    """Equal-power pan; position -1 is hard left, +1 hard right."""
    angle = (position + 1) * np.pi / 4
    return np.stack((mono * np.cos(angle), mono * np.sin(angle)), axis=1)


def place(track, sound, seconds):
    start = round(seconds * RATE)
    end = min(start + len(sound), len(track))
    if end > start:
        track[start:end] += sound[:end - start]


def lowpass(mono, cutoff):
    """Windowed-sinc FIR, enough to push a bird back into the distance."""
    taps = 63
    n = np.arange(taps) - taps // 2
    kernel = np.sinc(2 * cutoff / RATE * n) * np.hamming(taps)
    return np.convolve(mono, kernel / kernel.sum(), mode="same")


def colored_noise(frames, channels, exponent):
    """Noise with a 1/f**exponent power spectrum (1 is pink, 2 is brown)."""
    spectrum = np.fft.rfft(rng.standard_normal((channels, frames)))
    freqs = np.fft.rfftfreq(frames, 1 / RATE)
    freqs[0] = freqs[1]
    noise = np.fft.irfft(spectrum / freqs ** (exponent / 2), n=frames).T
    return noise / np.max(np.abs(noise))


# --- voices ----------------------------------------------------------------

def sweep(f0, f1, duration, vibrato=0.0, vibrato_rate=0.0, harmonic=0.15):
    """A single chirp: exponential glide from f0 to f1 under a smooth bell."""
    t = np.arange(round(duration * RATE)) / RATE
    freq = f0 * (f1 / f0) ** (t / duration)
    freq *= 1 + vibrato * np.sin(2 * np.pi * vibrato_rate * t)
    phase = 2 * np.pi * np.cumsum(freq) / RATE
    envelope = np.sin(np.pi * t / duration) ** 2
    return envelope * (np.sin(phase) + harmonic * np.sin(2 * phase))


def phrase(parts):
    """Join (gap seconds, sound) pairs into one mono phrase."""
    parts = list(parts)
    out = np.zeros(round(sum(gap * RATE + len(s) for gap, s in parts)) + 1)
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
    return phrase(
        (0.07 * (1 - 0.3 * i / count), sweep(top * (1 - 0.15 * i / count), 3800, 0.04))
        for i in range(count)
    )


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
    return phrase([
        (0.0, sweep(start, start * 1.45, rng.uniform(0.5, 0.8), 0.02, 28, 0.05)),
        (0.12, sweep(start * 1.3, start * 0.95, 0.25, 0.015, 28, 0.05)),
    ])


# (song, position, distance in 0..1, mean seconds between phrases, level dB)
BIRDS = (
    (sparrow, -0.6, 0.2, 3.0, -6),
    (sparrow, 0.7, 0.7, 4.5, -10),
    (warbler, 0.3, 0.4, 6.0, -8),
    (tit, -0.2, 0.3, 5.0, -7),
    (tit, 0.9, 0.9, 7.0, -12),
    (whistler, -0.9, 0.6, 8.0, -9),
)


def songbirds():
    track = np.zeros((FRAMES, 2))
    for song, position, distance, interval, level in BIRDS:
        at = rng.uniform(0, interval)
        while at < SECONDS:
            sound = song()
            if distance > 0.5:
                sound = lowpass(sound, 9000 - 6000 * distance)
            gain = db(level) * (1 - 0.6 * distance)
            place(track, pan(sound * gain, position), at)
            at += len(sound) / RATE + rng.exponential(interval)
    return track


def flock():
    """Distant tweets from FluidSynth, spread across channels panned apart."""
    score = Score()
    for channel in range(FLOCK_CHANNELS):
        score.program(channel, BIRD_TWEET)
        score.control(channel, 7, 70)  # volume
        score.control(channel, 10, round(np.interp(channel, (0, FLOCK_CHANNELS - 1), (10, 117))))
        score.control(channel, 91, 100)  # reverb send

        at = rng.uniform(0, 4)
        while at < SECONDS - 1:
            for _ in range(rng.integers(1, 4)):
                score.note(at, rng.uniform(0.15, 0.6), channel,
                           int(rng.integers(72, 97)), int(rng.integers(40, 80)))
                at += rng.uniform(0.1, 0.3)
            at += rng.exponential(3.5)
    return score.render(SECONDS)


def wind():
    """Brownish noise for leaves, swelling in slow gusts."""
    leaves = colored_noise(FRAMES, 2, 1.6)
    t = np.arange(FRAMES) / RATE
    gusts = 0.6 + 0.4 * np.sin(2 * np.pi * t / 11) * np.sin(2 * np.pi * t / 4.3 + 1)
    return leaves * gusts[:, None] * db(-26)


def reverb(audio, wet=0.18):
    """Convolve with an exponentially decaying noise burst (FFT based)."""
    t = np.arange(round(REVERB * RATE)) / RATE
    impulse = rng.standard_normal((len(t), 2)) * np.exp(-6.9 * t / REVERB)[:, None]
    impulse /= np.sqrt(np.sum(impulse ** 2, axis=0))
    size = len(audio) + len(impulse) - 1
    tail = np.fft.irfft(np.fft.rfft(audio, size, axis=0) * np.fft.rfft(impulse, size, axis=0),
                        size, axis=0)
    return audio + wet * fit(tail, len(audio))


def chirping00():
    mix = songbirds() + 2.5 * flock()
    mix = reverb(mix) + wind()

    fade = np.minimum(1, np.minimum(np.arange(FRAMES), FRAMES - 1 - np.arange(FRAMES)) / (FADE * RATE))
    return normalize(mix * fade[:, None])
