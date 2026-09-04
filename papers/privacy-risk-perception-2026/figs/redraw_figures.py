# -*- coding: utf-8 -*-
"""Redraw the four figures of Huang et al. (2026) with Chinese labels.
Source: Front. Psychol. 17:1891374, CC BY 4.0 — adaptation permitted with attribution."""
import os
F = 'Noto Sans CJK SC, WenQuanYi Zen Hei, sans-serif'
os.makedirs('figs', exist_ok=True)

HEAD = '''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{F}">
<rect width="{w}" height="{h}" fill="#ffffff"/>
<defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#111"/></marker>
</defs>
'''

def box(x, y, w, h, lines, fs=21):
    s = '<rect x="%d" y="%d" width="%d" height="%d" fill="#fff" stroke="#111" stroke-width="2.5"/>' % (x, y, w, h)
    cy = y + h / 2 - (len(lines) - 1) * fs * 0.62
    for i, t in enumerate(lines):
        s += '<text x="%d" y="%.1f" font-size="%d" text-anchor="middle" fill="#111">%s</text>' % (
            x + w / 2, cy + i * fs * 1.24 + fs * 0.36, fs, t)
    return s

def arrow(x1, y1, x2, y2, wid=2.5):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#111" stroke-width="%s" marker-end="url(#ah)"/>' % (x1, y1, x2, y2, wid)

def lab(x, y, t, fs=20, anchor='middle', fill='#111', rot=None, weight='normal'):
    r = ' transform="rotate(%s %s %s)"' % (rot, x, y) if rot else ''
    return '<text x="%.1f" y="%.1f" font-size="%d" text-anchor="%s" fill="%s" font-weight="%s"%s>%s</text>' % (
        x, y, fs, anchor, fill, weight, r, t)

# ---------------- Figure 1: hypothesized research model ----------------
w, h = 920, 610
s = HEAD.format(w=w, h=h, F=F)
s += box(340, 24, 240, 66, ['网络社交焦虑'])
s += box(20, 334, 224, 84, ['隐私风险感知'])
s += box(676, 334, 224, 84, ['隐私披露行为'])
s += box(350, 508, 224, 66, ['隐私犬儒主义'])
s += arrow(218, 334, 346, 94)            # PRP -> OSA
s += arrow(574, 94, 698, 334)            # OSA -> PDB
s += arrow(244, 376, 672, 376)           # PRP -> PDB (direct)
s += arrow(392, 508, 288, 218)           # cynicism -> a path
s += arrow(462, 508, 462, 386)           # cynicism -> c' path
s += arrow(532, 508, 634, 218)           # cynicism -> b path
open('figs/fig1_zh.svg', 'w').write(s + '</svg>')

# ---------------- Figure 2: mediation model with estimates ----------------
w, h = 940, 600
s = HEAD.format(w=w, h=h, F=F)
s += box(248, 14, 150, 54, ['评价焦虑'], fs=19)
s += box(418, 14, 150, 54, ['互动焦虑'], fs=19)
s += box(588, 14, 150, 54, ['隐私担忧'], fs=19)
s += '<ellipse cx="480" cy="182" rx="146" ry="64" fill="#fff" stroke="#111" stroke-width="2.5"/>'
s += lab(480, 190, '网络社交焦虑', fs=22)
s += box(24, 440, 214, 84, ['隐私风险感知'])
s += box(702, 440, 214, 84, ['隐私披露行为'])
s += arrow(400, 132, 336, 72)
s += arrow(480, 118, 480, 72)
s += arrow(560, 132, 654, 72)
s += arrow(190, 440, 372, 228)
s += arrow(588, 228, 750, 440)
s += arrow(238, 482, 698, 482)
s += lab(316, 140, '0.94<tspan font-size="13" baseline-shift="super">a</tspan>')
s += lab(516, 104, '0.89<tspan font-size="13" baseline-shift="super">a</tspan>')
s += lab(654, 128, '0.86<tspan font-size="13" baseline-shift="super">a</tspan>')
s += lab(224, 344, '0.28<tspan font-size="13" baseline-shift="super">a</tspan>', rot=-49)
s += lab(716, 344, '0.14<tspan font-size="13" baseline-shift="super">a</tspan>', rot=53)
s += lab(468, 466, '0.35<tspan font-size="13" baseline-shift="super">a</tspan>')
s += lab(24, 578, '注：a 表示 p &lt; 0.001；图中为标准化路径系数。', fs=16, anchor='start', fill='#555')
open('figs/fig2_zh.svg', 'w').write(s + '</svg>')

# ---------------- Figures 3 & 4: simple slope plots ----------------
def slope_plot(fname, ytitle, yticks, ylo, yhi, blue, red, ylab_dx=0):
    w, h = 980, 580
    X0, X1, Y0, Y1 = 132, 648, 44, 444        # plot frame
    xl, xr = 232, 582                          # the two x positions
    sy = lambda v: Y1 - (v - ylo) / (yhi - ylo) * (Y1 - Y0)
    s = HEAD.format(w=w, h=h, F=F)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#8a8a8a" stroke-width="2"/>' % (X0, Y0, X0, Y1)
    for v in yticks:
        y = sy(v)
        s += '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#8a8a8a" stroke-width="2"/>' % (X0 - 9, y, X0, y)
        s += lab(X0 - 16, y + 7, ('%g' % v).replace('-', '−'), fs=19, anchor='end', fill='#333')
    if ylo < 0 < yhi:
        s += '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#c9c9c9" stroke-width="2"/>' % (X0, sy(0), X1, sy(0))
        base = sy(0) + 30
    else:
        s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#8a8a8a" stroke-width="2"/>' % (X0, Y1, X1, Y1)
        base = Y1 + 34
    for (col, dash, pts, mark) in ((('#2f6fb5'), '16,10', blue, 'd'), (('#b5382f'), '5,9', red, 's')):
        s += '<polyline points="%.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="5" stroke-dasharray="%s"/>' % (
            xl, sy(pts[0]), xr, sy(pts[1]), col, dash)
        for (px, pv) in ((xl, pts[0]), (xr, pts[1])):
            if mark == 'd':
                s += '<path d="M %.1f %.1f l 11 8 l -11 8 l -11 -8 z" fill="%s"/>' % (px, sy(pv) - 8, col)
            else:
                s += '<rect x="%.1f" y="%.1f" width="15" height="15" fill="%s"/>' % (px - 7.5, sy(pv) - 7.5, col)
    s += lab(xl, base, '低（M−1SD）', fs=21)
    s += lab(xr, base, '高（M+1SD）', fs=21)
    s += lab((xl + xr) / 2, h - 26, '隐私风险感知', fs=23)
    s += lab(40 + ylab_dx, (Y0 + Y1) / 2, ytitle, fs=23, rot=-90)
    s += '<line x1="678" y1="250" x2="742" y2="250" stroke="#2f6fb5" stroke-width="5" stroke-dasharray="16,10"/>'
    s += '<path d="M 710 242 l 11 8 l -11 8 l -11 -8 z" fill="#2f6fb5"/>'
    s += lab(752, 258, '低隐私犬儒主义', fs=19, anchor='start')
    s += '<line x1="678" y1="298" x2="742" y2="298" stroke="#b5382f" stroke-width="5" stroke-dasharray="5,9"/>'
    s += '<rect x="702.5" y="290.5" width="15" height="15" fill="#b5382f"/>'
    s += lab(752, 306, '高隐私犬儒主义', fs=19, anchor='start')
    open(fname, 'w').write(s + '</svg>')

slope_plot('figs/fig3_zh.svg', '隐私披露行为', [0, 1, 2, 3, 4, 5, 6], 0, 6, (3.20, 5.65), (2.82, 4.83))
slope_plot('figs/fig4_zh.svg', '网络社交焦虑', [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8], -1, 0.8,
           (0.27, 0.60), (-0.34, -0.86))
print('svg written')
