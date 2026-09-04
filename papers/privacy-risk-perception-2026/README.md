# 大学生隐私风险感知与隐私披露行为（2026）

- `Huang-et-al-2026-fpsyg-1891374.pdf` — 英文原文 PDF
- `中文译本.docx` — **Word 版（14 页，A4，插图内嵌）**，可直接编辑批注
- `中文译本.pdf` — 排版好的 PDF 版（16 页，A4，插图内嵌），只读阅读用这个
- `中文译本.html` — 同一份内容的单文件网页版（图片已 base64 内嵌，可离线打开）
- `中文译本.md` — Markdown 源文，便于二次编辑
- `figs/` — 图 1–4 的中文重绘版（PNG + SVG）及生成脚本 `redraw_figures.py`
- `build_pdf.py` / `topdf.py` — 由 Markdown 生成 HTML 再输出 PDF 的构建脚本
- `build_docx.js` / `fix_pbdr.py` — 由 Markdown 生成 Word 的构建脚本

## 重新生成 PDF

```
python3 build_pdf.py   # Markdown -> 带样式的自包含 HTML
python3 topdf.py       # HTML -> PDF（A4，含页码）
```

依赖：`mistune`、`playwright`，以及 `fonts-noto-cjk` / `fonts-noto-cjk-extra` 字体。

## 重新生成 Word

```
node build_docx.js     # Markdown -> docx（正文宋体、标题黑体）
python3 fix_pbdr.py    # 修正 docx-js 输出的 w:pBdr 子元素顺序，否则 Word/LibreOffice 打不开
```

依赖：`npm install docx`。

## 出处

Huang S, Yuan L, Yang Y, Li J, Chen Y, Liu Y, Zhang S and Liu P (2026).
Privacy risk perception and privacy disclosure behavior among college students:
the mediating role of online social anxiety and the moderating role of privacy cynicism.
*Frontiers in Psychology* 17:1891374. doi: 10.3389/fpsyg.2026.1891374

原文链接：https://doi.org/10.3389/fpsyg.2026.1891374

## 许可

© 2026 Huang, Yuan, Yang, Li, Chen, Liu, Zhang and Liu.
原文为依据 Creative Commons 署名许可（CC BY 4.0）发布的开放获取论文。
本目录下的 PDF、中文译本与重绘插图依该许可存放与分发，署名归原作者所有。
插图为依据原文图片重绘的中文版：图形结构、数据点与统计标注均与原图一致，仅将图内英文标签译为中文。
译本仅供阅读参考，如与原文有出入，以英文原文为准。
