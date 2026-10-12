#!/usr/bin/env python3
"""为《我是怎么来的》合成配乐：环境铺底和弦 + 拨弦旋律 + 打字、提示音效。

只用 numpy，不需要任何音频素材。音效时间点来自 film.html 导出的 cues.json，
所以画面里每敲出一个字、每打一个勾，都会有对应的声音。

用法：python3 music.py [cues.json] [输出.wav]
"""
import json
import sys
import wave

import numpy as np

SR = 48000
cues_path = sys.argv[1] if len(sys.argv) > 1 else 'cues.json'
out_path = sys.argv[2] if len(sys.argv) > 2 else 'build/music.wav'
spec = json.load(open(cues_path, encoding='utf-8'))
DUR = spec['duration']
N = int((DUR + 0.5) * SR)

bus = np.zeros((2, N))   # 干声
send = np.zeros((2, N))  # 送往混响的量
rng = np.random.default_rng(2021)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def add(sig, t0, rev=0.35, gain=1.0, pan=0.0):
    """把单声道或立体声片段混入总线，rev 为混响发送量。"""
    if sig.ndim == 1:
        th = (pan + 1) * np.pi / 4
        sig = np.stack([sig * np.cos(th), sig * np.sin(th)]) * np.sqrt(2)
    i0 = int(round(t0 * SR))
    if i0 < 0:
        sig, i0 = sig[:, -i0:], 0
    n = min(sig.shape[1], N - i0)
    if n <= 0:
        return
    bus[:, i0:i0 + n] += sig[:, :n] * gain
    send[:, i0:i0 + n] += sig[:, :n] * gain * rev


def env_asr(n, attack, release, hold_n):
    e = np.ones(n)
    na = min(n, max(1, int(attack * SR)))
    e[:na] = 0.5 - 0.5 * np.cos(np.pi * np.arange(na) / na)
    if hold_n < n:
        nr = n - hold_n
        e[hold_n:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(nr) / nr)
    return e


# ---------------- 乐器 ----------------
def pad(notes, t0, t1, amp, attack=1.8, release=2.6, bright=1.0):
    n = int((t1 - t0 + release) * SR)
    t = np.arange(n) / SR
    out = np.zeros((2, n))
    for m in notes:
        f = hz(m)
        for ch in range(2):
            s = np.zeros(n)
            for h, ha in ((1, 1.0), (2, 0.30 * bright), (3, 0.10 * bright), (4, 0.035 * bright)):
                if f * h > 8000:
                    continue
                for dc in (-7, 0, 7):
                    det = 2 ** ((dc + rng.uniform(-2, 2)) / 1200)
                    s += ha * np.sin(2 * np.pi * f * h * det * t + rng.uniform(0, 2 * np.pi))
            s *= (1 + 0.15 * np.sin(2 * np.pi * rng.uniform(0.06, 0.16) * t + rng.uniform(0, 6.28))) / 3
            out[ch] += s
    out *= env_asr(n, attack, release, int((t1 - t0) * SR)) * amp
    add(out, t0, rev=0.5)


def bass(m, t0, t1, amp):
    n = int((t1 - t0 + 2.5) * SR)
    t = np.arange(n) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t + 0.5) + 0.06 * np.sin(6 * np.pi * f * t)
    s *= env_asr(n, 1.4, 2.5, int((t1 - t0) * SR)) * amp
    add(s, t0, rev=0.15)


def pluck(m, t0, amp=0.13, decay=1.6, bell=False, rev=0.55, pan=None):
    f = hz(m)
    n = int(decay * 5 * SR)
    t = np.arange(n) / SR
    parts = ((1, 1.0, 1.0), (2.0, 0.35, 0.6), (3.01, 0.16, 0.4), (4.17, 0.07, 0.25), (5.43, 0.04, 0.18)) if bell else \
            ((1, 1.0, 1.0), (2, 0.42, 0.6), (3, 0.18, 0.42), (4, 0.09, 0.3), (5, 0.04, 0.22), (6, 0.02, 0.16))
    s = np.zeros(n)
    for h, ha, dk in parts:
        fh = f * h * (1 + 0.0002 * h * h)
        if fh > 15000:
            continue
        s += ha * np.sin(2 * np.pi * fh * t + rng.uniform(0, 6.28)) * np.exp(-t / (decay * dk))
    na = int(0.006 * SR)
    s[:na] *= np.linspace(0, 1, na)
    add(s * amp, t0, rev=rev, pan=rng.uniform(-0.35, 0.35) if pan is None else pan)


def click(t0, vol=1.0, bright=1.0):
    """键盘敲击：带一点“咔哒”的短噪声 + 低频轻击。"""
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    hp = np.concatenate([[0.0], np.diff(noise)]) * 0.5
    s = hp * np.exp(-t / 0.0028) * 0.55 * bright
    s += np.sin(2 * np.pi * rng.uniform(1900, 2600) * t) * np.exp(-t / 0.0018) * 0.25 * bright
    s += np.sin(2 * np.pi * rng.uniform(120, 160) * t) * np.exp(-t / 0.010) * 0.35
    add(s * rng.uniform(0.7, 1.0) * vol * 0.29, t0, rev=0.08, pan=rng.uniform(-0.12, 0.12))


def boom(t0, amp=0.28):
    n = int(4.0 * SR)
    t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(34 + 60 * np.exp(-t / 0.35)) / SR
    s = np.sin(ph) * np.exp(-t / 1.1) + 0.3 * np.sin(2 * ph) * np.exp(-t / 0.4)
    na = int(0.008 * SR)
    s[:na] *= np.linspace(0, 1, na)
    add(s * amp, t0, rev=0.3)


def whoosh(tp, amp=0.05, dur=1.8):
    """转场的气流声，在 tp 附近达到最响。"""
    n = int(dur * SR)
    x = np.arange(n) / n
    env = np.where(x < 0.7, (x / 0.7) ** 2, 0.5 + 0.5 * np.cos(np.pi * (x - 0.7) / 0.3))
    fr = np.fft.rfftfreq(n, 1 / SR)
    shape = np.exp(-((np.log2(fr + 1) - np.log2(900)) / 1.3) ** 2)
    out = np.stack([np.fft.irfft(np.fft.rfft(rng.standard_normal(n)) * shape, n) for _ in range(2)])
    out *= env * amp / (np.max(np.abs(out)) + 1e-9)
    add(out, tp - 0.7 * dur, rev=0.4)


# ---------------- 和弦进行（与画面分场对齐） ----------------
CH = {
    'intro':    [62, 69, 76],
    'Dmaj9':    [50, 57, 61, 64, 66],
    'D':        [50, 57, 62, 66, 69],
    'Bm9':      [47, 54, 57, 61, 62],
    'Gmaj7#11': [43, 50, 54, 59, 61],
    'Gmaj9':    [43, 50, 54, 57, 59],
    'Em9':      [52, 59, 62, 66, 67],
    'Asus4':    [45, 52, 57, 62, 64],
    'F#m7':     [42, 49, 52, 57, 61],
    'D/F#':     [42, 50, 57, 62, 66],
    'A/C#':     [49, 52, 57, 61, 64],
}
SCHED = [  # (开始, 结束, 和弦, 音量)
    (3.5, 9.4, 'intro', 0.020),
    (9.0, 15.0, 'Dmaj9', 0.050), (15.0, 21.5, 'Bm9', 0.044), (21.5, 28.0, 'Gmaj7#11', 0.044),
    (28.0, 34.0, 'Em9', 0.044), (34.0, 40.0, 'Asus4', 0.046),
    (40.0, 46.0, 'Dmaj9', 0.042), (46.0, 52.0, 'F#m7', 0.040),
    (52.0, 57.0, 'Bm9', 0.040), (57.0, 62.0, 'Gmaj7#11', 0.040),
    (62.0, 66.5, 'Em9', 0.038), (66.5, 70.5, 'Asus4', 0.038), (70.5, 75.0, 'Dmaj9', 0.040),
    (75.0, 79.5, 'Gmaj7#11', 0.040), (79.5, 84.0, 'Bm9', 0.040), (84.0, 88.0, 'Em9', 0.040),
    (88.0, 93.0, 'F#m7', 0.040), (93.0, 98.0, 'Asus4', 0.042),
    (98.0, 100.8, 'D', 0.046), (100.8, 104.5, 'A/C#', 0.048), (104.5, 108.2, 'Bm9', 0.048),
    (108.2, 111.9, 'Gmaj7#11', 0.050), (111.9, 113.75, 'D/F#', 0.052), (113.75, 115.6, 'Em9', 0.052),
    (115.6, 118.0, 'Asus4', 0.050),
    (118.0, 124.0, 'Bm9', 0.034), (124.0, 131.0, 'Gmaj7#11', 0.036),
    (131.0, 134.5, 'Gmaj9', 0.044), (134.5, 137.5, 'D/F#', 0.046), (137.5, 140.0, 'Em9', 0.048),
    (140.0, 142.5, 'Asus4', 0.048), (142.5, 151.5, 'Dmaj9', 0.046),
]


def chord_at(t):
    cur = SCHED[1][2]
    for t0, t1, name, _ in SCHED:
        if t0 <= t < t1:
            cur = name
    return CH[cur]


for t0, t1, name, amp in SCHED:
    pad(CH[name], t0, t1, amp, attack=3.0 if name == 'intro' else 1.8)
    if name != 'intro':
        low = CH[name][0]
        bass(low - 12 if low - 12 >= 33 else low, t0, t1, amp * 2.2)

# 片名：一个琶音和几个点缀音
for i, m in enumerate([62, 69, 78]):
    pluck(m, 9.3 + i * 0.07, amp=0.11)
for t, m in ((11.6, 76), (12.3, 78), (13.2, 81)):
    pluck(m, t, amp=0.07)

# 阅读：越来越密的星点
t = 29.0
while t < 39.0:
    tones = chord_at(t)
    pluck(tones[rng.integers(1, len(tones))] + 24, t, amp=rng.uniform(0.025, 0.05) * (0.6 + 0.4 * (t - 29) / 10), decay=0.9, rev=0.7)
    t += rng.uniform(0.22, 0.42) * (1.2 - 0.5 * (t - 29) / 10)

# 神经网络：像计算一样规律跳动的琶音
t, i = 53.0, 0
while t < 61.2:
    tones = chord_at(t)
    pluck(tones[i % len(tones)] + 12 + 12 * ((i // len(tones)) % 2), t, amp=0.035, decay=0.7, rev=0.45)
    t += 0.3
    i += 1

# 时间线：轻轻推进的八分音符
t, i = 100.8, 0
while t < 116.5:
    tones = chord_at(t)
    pluck(tones[(i * 2) % len(tones)] + 12, t, amp=0.026, decay=0.8, rev=0.5)
    t += 0.4625
    i += 1

# 可解释性：几声空灵的钟音
for t, m in ((119.5, 71), (121.3, 78), (123.9, 85), (126.5, 81), (129.0, 78)):
    pluck(m, t, amp=0.06, bell=True, decay=2.2, rev=0.8)

# 尾声旋律
for t, m in ((131.6, 78), (133.6, 76), (136.6, 74), (137.6, 76), (139.2, 81), (139.5, 86)):
    pluck(m, t, amp=0.10, decay=2.0)

# ---------------- 画面音效 ----------------
NODE_MELODY = [74, 76, 78, 81, 83, 85, 86]
for c in spec['cues']:
    kind, t = c['type'], c['t']
    if kind == 'type':
        click(t, vol=c.get('vol', 1.0), bright=0.6 + 0.4 * c.get('vol', 1.0))
    elif kind == 'boom':
        boom(t)
    elif kind == 'ding':
        for m in c['notes']:
            pluck(m, t, amp=0.10 * c.get('vol', 1.0), bell=True, decay=1.8, rev=0.6)
    elif kind == 'pluck':
        for i, m in enumerate(c['notes']):
            pluck(m, t + i * c.get('arp', 0.0), amp=0.10, decay=1.8)
    elif kind == 'tick':
        click(t, vol=0.6)
        for m in c['notes']:
            pluck(m + 12, t, amp=0.07, decay=0.9)
    elif kind == 'click':
        click(t, vol=0.8, bright=1.3)
        click(t + 0.08, vol=0.5, bright=1.3)
    elif kind == 'node':
        k = c['k']
        if k < len(NODE_MELODY):
            pluck(NODE_MELODY[k], t, amp=0.12, decay=1.8)
        else:
            for i, m in enumerate([74, 78, 81, 86, 90]):
                pluck(m, t + i * 0.06, amp=0.09, bell=i > 2, decay=2.4)
    elif kind == 'whoosh':
        whoosh(t)


# ---------------- 混响与母带 ----------------
def reverb(x, rt60=3.4, pre=0.025):
    n = int(rt60 * 1.2 * SR)
    t = np.arange(n) / SR
    nfft = 1 << (x.shape[1] + n - 1).bit_length()
    fr = np.fft.rfftfreq(nfft, 1 / SR)
    lp = 1 / (1 + (fr / 3800) ** 2)
    out = np.zeros_like(x)
    ip = int(pre * SR)
    for ch in range(2):
        ir = rng.standard_normal(n) * np.exp(-6.91 * t / rt60)
        IR = np.fft.rfft(ir, nfft) * lp
        IR[0] = 0
        IR /= np.sqrt(np.sum(np.abs(np.fft.irfft(IR, nfft)) ** 2))
        y = np.fft.irfft(np.fft.rfft(x[ch], nfft) * IR, nfft)
        out[ch, ip:] = y[:x.shape[1] - ip]
    return out


mix = bus + 0.6 * reverb(send)
fade_in = int(0.2 * SR)
mix[:, :fade_in] *= np.linspace(0, 1, fade_in)
f0, f1 = int(150.5 * SR), int(DUR * SR)
mix[:, f0:f1] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(f1 - f0) / (f1 - f0))
mix[:, f1:] = 0

rms = np.sqrt(np.mean(mix[:, int(9 * SR):int(150 * SR)] ** 2))
mix *= 10 ** (-17.5 / 20) / rms
peak_before = np.max(np.abs(mix))
mix = np.tanh(mix / 0.9) * 0.9   # 软限幅
pcm = (np.clip(mix, -1, 1) * 32767).astype('<i2').T.copy()
with wave.open(out_path, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f'{out_path}: {pcm.shape[0] / SR:.1f}s，限幅前峰值 {20 * np.log10(peak_before):.1f} dBFS')
