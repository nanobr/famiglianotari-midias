"""Trilha original: valsa romântica italiana (bandolim em tremolo + acordeão musette + baixo)."""
import numpy as np, wave, sys

SR = 44100
BPM = 108
BEAT = 60 / BPM
BAR = 3 * BEAT
out_path = sys.argv[1]

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def pluck(freq, dur, amp=0.3, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for k in range(1, 14):
        f = freq * k
        if f > 12000: break
        decay = 2.2 + 1.6 * k / bright
        s += (1 / k ** 1.1) * np.sin(2 * np.pi * f * t) * np.exp(-decay * t)
    att = np.minimum(1, t / 0.003)
    return amp * s * att

def mandolin(freq, dur, amp, tremolo):
    n = int(dur * SR); s = np.zeros(n)
    if not tremolo:
        for det in (1.0, 1.0025):
            s += pluck(freq * det, dur, amp * 0.55, bright=1.4)
        return s
    step = 1 / 11.0  # ~11 palhetadas/s
    i = 0; t0 = 0.0
    while t0 < dur - 0.02:
        a = amp * (0.75 if i % 2 else 0.6) * (0.9 + 0.1 * np.random.rand())
        p = pluck(freq * (1.0 if i % 2 else 1.0025), min(0.5, dur - t0), a, bright=1.4)
        st = int(t0 * SR); s[st:st + len(p)] += p[:n - st]
        t0 += step; i += 1
    return s

def accordion(freqs, dur, amp):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    vib = 1 + 0.003 * np.sin(2 * np.pi * 5.2 * t)
    for f0 in freqs:
        for det in (0.9965, 1.0, 1.0035):  # musette
            ph = 2 * np.pi * f0 * det * np.cumsum(vib) / SR
            for k in range(1, 7):
                s += (0.6 ** k) * np.sin(k * ph)
    env = np.minimum(1, t / 0.06) * np.minimum(1, (dur - t) / 0.08)
    return amp * s * env / max(1, len(freqs))

CH = {  # (baixo, acorde médio)
    'D': (50, [62, 66, 69]), 'Bm': (47, [62, 66, 71]), 'G': (43, [62, 67, 71]),
    'A': (45, [61, 64, 69]), 'Em': (40, [59, 64, 67]), 'A7': (45, [61, 64, 67]),
}
# melodia: lista de (midi, batidas, tremolo)
A_prog = ['D', 'D', 'Bm', 'Bm', 'G', 'A', 'D', 'A']
A_mel = [(78,2,0),(81,1,0), (86,3,1), (83,2,0),(81,1,0), (78,3,1),
         (79,1,0),(83,1,0),(86,1,0), (85,2,0),(83,1,0), (81,3,1), (76,1,0),(78,1,0),(79,1,0)]
B_prog = ['G', 'G', 'D', 'D', 'Em', 'A', 'D', 'A7']
B_mel = [(83,2,0),(79,1,0), (86,3,1), (81,2,0),(78,1,0), (74,3,1),
         (76,1,0),(79,1,0),(83,1,0), (81,1,0),(79,1,0),(76,1,0), (78,3,1), (81,1,0),(79,1,0),(76,1,0)]
C_prog = ['G', 'A', 'Bm', 'G', 'A', 'D']
C_mel = [(83,2,0),(86,1,0), (85,3,1), (86,2,0),(83,1,0), (79,1,0),(83,1,0),(81,1,0),
         (76,1,0),(78,1,0),(79,1,0), (86,6,1)]
prog = A_prog + B_prog + A_prog + C_prog          # 30 compassos
mel = A_mel + B_mel + A_mel + C_mel

total = len(prog) * BAR + 2.5
N = int(total * SR)
mix = np.zeros(N)
def add(sig, t):
    st = int(t * SR); e = min(N, st + len(sig)); mix[st:e] += sig[:e - st]

np.random.seed(7)
last = len(prog) - 1
for b, ch in enumerate(prog):
    t = b * BAR
    bass, chord = CH[ch]
    final = b == last
    add(pluck(hz(bass), BAR * (2 if final else 1), 0.55, bright=0.6), t)
    if final:
        add(accordion([hz(m) for m in chord], BAR * 2.2, 0.16), t)
    else:
        for k in (1, 2):  # "tum-pá-pá"
            add(accordion([hz(m) for m in chord], BEAT * 0.8, 0.13), t + k * BEAT)
t = 0
for m, beats, trem in mel:
    d = beats * BEAT
    add(mandolin(hz(m), d + 0.25, 0.34, trem), t)
    t += d

# reverb simples
ir_n = int(1.6 * SR); ir_t = np.arange(ir_n) / SR
ir = np.random.randn(ir_n) * np.exp(-3.8 * ir_t); ir[0] = 0
wet = np.fft.irfft(np.fft.rfft(mix, N + ir_n) * np.fft.rfft(ir, N + ir_n))[:N]
y = mix + 0.018 * wet
# fade-out final
fo = int(2.5 * SR); y[-fo:] *= np.linspace(1, 0, fo)
y = y / np.max(np.abs(y)) * 0.89
stereo = np.stack([y, np.roll(y, 220) * 0.97], axis=1)
with wave.open(out_path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())
print(f"{total:.2f}s")
