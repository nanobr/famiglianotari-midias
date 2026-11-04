import numpy as np, wave

SR = 44100
rng = np.random.default_rng(7)


def env(n, attack=0.005, decay=8.0):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-decay * t)


def pop():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = 500 + 1400 * (t / t[-1]) ** 0.6
    ph = 2 * np.pi * np.cumsum(f) / SR
    return 0.55 * np.sin(ph) * env(n, 0.002, 30)


def tick():
    n = int(0.018 * SR)
    t = np.arange(n) / SR
    return 0.10 * np.sin(2 * np.pi * 1900 * t) * env(n, 0.001, 260)


def drip():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    f = 1400 - 900 * (t / t[-1])
    ph = 2 * np.pi * np.cumsum(f) / SR
    return 0.35 * np.sin(ph) * env(n, 0.002, 18)


def boing():
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    f = 180 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-4 * t) + 140 * np.exp(-6 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return 0.6 * np.sin(ph) * env(n, 0.003, 4.5)


def whoosh():
    n = int(0.45 * SR)
    noise = rng.standard_normal(n)
    # crude band-pass sweep via moving average of different widths
    out = np.zeros(n)
    for k in (3, 6, 12):
        out += np.convolve(noise, np.ones(k) / k, mode="same")
    t = np.arange(n) / SR
    shape = np.sin(np.pi * t / t[-1]) ** 2
    return 0.12 * out * shape


def pluck(freq, dur, amp=0.18):
    n = int(dur * SR)
    p = int(SR / freq)
    buf = rng.uniform(-1, 1, p)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.996 * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return amp * out


def music(total):
    # gentle ukulele-ish loop: C - Am - F - G, one chord per 2 beats at 120 bpm
    notes = {"C": [261.6, 329.6, 392.0, 523.3], "Am": [220.0, 261.6, 329.6, 440.0],
             "F": [174.6, 220.0, 261.6, 349.2], "G": [196.0, 246.9, 293.7, 392.0]}
    prog = ["C", "Am", "F", "G"]
    beat = 0.5
    out = np.zeros(int(total * SR) + SR)
    t, i = 0.0, 0
    while t < total:
        chord = notes[prog[(i // 4) % 4]]
        f = chord[[0, 2, 1, 3][i % 4]]
        s = pluck(f, 0.9, 0.11)
        a = int(t * SR)
        out[a:a + len(s)] += s[: len(out) - a]
        t += beat / 2
        i += 1
    return out[: int(total * SR)]


def make_audio(ep, path):
    durs = [d for _, d in ep.SCENES]
    total = sum(durs)
    mix = music(total) * 0.8
    fx = {"pop": pop(), "drip": drip(), "boing": boing(), "whoosh": whoosh()}
    tk = tick()
    base = 0.0
    for d, cues in zip(durs, ep.CUES):
        for at, kind, length in cues:
            if kind == "type":
                for k in np.arange(0, length, 0.07):
                    a = int((base + at + k) * SR)
                    mix[a:a + len(tk)] += tk[: len(mix) - a]
            else:
                s = fx[kind]
                a = int((base + at) * SR)
                mix[a:a + len(s)] += s[: len(mix) - a]
        base += d
    # fade out last 0.8 s
    n = int(0.8 * SR)
    mix[-n:] *= np.linspace(1, 0, n)
    mix = mix / max(1.0, np.abs(mix).max() / 0.9)
    data = (mix * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


