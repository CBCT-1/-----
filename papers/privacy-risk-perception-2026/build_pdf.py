# -*- coding: utf-8 -*-
"""Typeset the Chinese translation as a print-quality PDF."""
import base64, os, re, mistune

SRC = 'translation.md'
md_text = open(SRC, encoding='utf-8').read()

renderer = mistune.create_markdown(plugins=['table'], escape=False)
html = renderer(md_text)

# --- pair each image with the caption paragraph that follows it -------------
html = re.sub(
    r'<p>\s*(<img[^>]*>)\s*</p>\s*<p>\s*(<strong>图\s*\d+.*?)</p>',
    r'<figure>\1<figcaption>\2</figcaption></figure>',
    html, flags=re.S)

# --- inline the figures so the HTML is self-contained ----------------------
def embed(m):
    path = m.group(1)
    with open(path, 'rb') as fh:
        b64 = base64.b64encode(fh.read()).decode()
    return 'src="data:image/png;base64,%s"' % b64

html = re.sub(r'src="([^"]+\.png)"', embed, html)

# --- split the title + metadata block out into a title header --------------
m = re.search(r'<h1>(.*?)</h1>', html, re.S)
title = m.group(1).strip()
html = html[:m.start()] + html[m.end():]

m = re.search(r'<blockquote>.*?</blockquote>', html, re.S)
meta = m.group(0)
html = html[:m.start()] + html[m.end():]
meta = meta.replace('<blockquote>', '<div class="meta">').replace('</blockquote>', '</div>')
html = html.lstrip()
html = re.sub(r'^<hr\s*/?>', '', html).lstrip()

CSS = """
@page { size: A4; margin: 19mm 18mm 17mm; }
* { box-sizing: border-box; }
body {
  font-family: "Noto Serif CJK SC", "Source Han Serif SC", serif;
  font-size: 10.5pt; line-height: 1.85; color: #16181d;
  text-align: justify; text-justify: inter-ideograph;
  margin: 0; -webkit-font-smoothing: antialiased;
}
.title {
  font-family: "Noto Sans CJK SC", sans-serif; font-weight: 700;
  font-size: 19pt; line-height: 1.45; color: #12233d;
  text-align: left; margin: 0 0 4pt; letter-spacing: .2px;
}
.rule { height: 2.5pt; background: linear-gradient(90deg,#1f4d8f 0%,#1f4d8f 34%,#c3cede 34%,#c3cede 100%);
        margin: 10pt 0 14pt; border-radius: 2pt; }
.meta {
  font-family: "Noto Sans CJK SC", sans-serif;
  background: #f5f7fa; border-left: 3pt solid #1f4d8f; border-radius: 2pt;
  padding: 10pt 13pt; margin: 0 0 20pt; font-size: 8.6pt; line-height: 1.72;
  color: #40474f; text-align: left;
}
.meta p { margin: 0 0 5pt; }
.meta p:last-child { margin-bottom: 0; }
.meta strong { color: #12233d; }
h2 {
  font-family: "Noto Sans CJK SC", sans-serif; font-size: 13.5pt; font-weight: 700;
  color: #12233d; margin: 19pt 0 9pt; padding-bottom: 4pt;
  border-bottom: 1pt solid #1f4d8f; break-after: avoid; text-align: left;
}
h3 {
  font-family: "Noto Sans CJK SC", sans-serif; font-size: 11.5pt; font-weight: 700;
  color: #1f4d8f; margin: 15pt 0 6pt; break-after: avoid; text-align: left;
}
h3::before { content: ""; display: inline-block; width: 3pt; height: 10pt;
  background: #1f4d8f; margin-right: 6pt; vertical-align: -1pt; border-radius: 1pt; }
p { margin: 0 0 8pt; orphans: 2; widows: 2; }
strong { color: #12233d; font-weight: 700; }
ol, ul { margin: 0 0 9pt; padding-left: 20pt; }
li { margin-bottom: 5pt; }
hr { border: none; border-top: .6pt solid #d8dde4; margin: 17pt 0; }
table {
  width: 100%; border-collapse: collapse; margin: 10pt 0 6pt;
  font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.2pt;
  line-height: 1.5; break-inside: avoid; text-align: center;
}
thead th {
  background: #eef2f7; color: #12233d; font-weight: 700; padding: 5pt 4pt;
  border-top: 1.1pt solid #12233d; border-bottom: .7pt solid #12233d;
}
tbody td { padding: 4.2pt 4pt; border-bottom: .35pt solid #e2e7ee; }
tbody tr:last-child td { border-bottom: 1.1pt solid #12233d; }
tbody td:first-child, thead th:first-child { text-align: left; }
figure { margin: 11pt 0 10pt; break-inside: avoid; text-align: center; }
figure img { max-width: 81%; height: auto; }
figcaption {
  font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.6pt; line-height: 1.65;
  color: #4a525c; text-align: left; margin: 6pt 8pt 0;
  padding-top: 5pt; border-top: .5pt solid #e2e7ee;
}
figcaption strong { color: #12233d; }
blockquote {
  background: #fdf9f0; border-left: 3pt solid #c8992a; border-radius: 2pt;
  margin: 12pt 0; padding: 9pt 13pt; font-size: 9.4pt; line-height: 1.75;
  color: #4a412c; break-inside: avoid;
}
blockquote p { margin: 0; }
blockquote strong { color: #7a5c10; }
code { font-family: "Noto Sans Mono CJK SC", monospace; font-size: 9pt;
  background: #f2f4f7; padding: 1pt 3pt; border-radius: 2pt; }
"""

doc = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>%s</title><style>%s</style></head><body>
<div class="title">%s</div><div class="rule"></div>%s
%s</body></html>""" % ('大学生隐私风险感知与隐私披露行为', CSS, title, meta, html)

open('translation.html', 'w', encoding='utf-8').write(doc)
print('html written:', len(doc), 'bytes')
