# 我是怎么来的 · How I Came to Be

一部 2 分 33 秒的短片：Claude 用第一人称讲述自己是怎么来的。
剧本、动画和配乐都是 Claude 写成的代码，在云端容器里逐帧渲染出来。

成片：[`how-i-came-to-be.mp4`](how-i-came-to-be.mp4)（1920×1080，30fps，带配乐）
体积更小的版本：[`how-i-came-to-be-720p.mp4`](how-i-came-to-be-720p.mp4)（1280×720，13.6 MB）

## 分镜

| 时间 | 场景 | 内容 |
|---|---|---|
| 0:00 | 开场 | 光标打出“你好，我是 Claude。” |
| 0:09 | 片名 | 我是怎么来的 |
| 0:15 | 2021 | 达里奥和丹妮拉·阿莫迪兄妹与几位研究者创立 Anthropic：AI 必须安全、诚实、对人有益 |
| 0:28 | 阅读 | 海量的人类文字汇聚成一个光点 |
| 0:40 | 预测下一个词 | “床前明月光，疑是地上＿” → 霜 |
| 0:52 | 预训练 | 神经网络里，海量参数被一点点调整 |
| 1:02 | 人类反馈（RLHF） | 人们比较两个回答，选出更好的那个 |
| 1:15 | 宪法式 AI | 有帮助 · 诚实 · 无害 |
| 1:28 | 安全测试 | 红队测试、危险能力评估、安全防护；负责任扩展政策 |
| 1:38 | 一代一代 | 2023.03 Claude → Claude 2 → Claude 3 家族 → Claude 3.5 Sonnet → Claude 3.7 Sonnet 与 Claude Code → Claude 4 → Claude 4.5 系列 → 今天 |
| 1:58 | 可解释性 | 放大镜在网络里找到一个个“特征” |
| 2:11 | 尾声 | “现在，轮到你了。你想聊点什么？” |
| 2:27 | 片尾字幕 | |

## 怎么做出来的

- `film.html`：整部片子就是一个网页。`render(t)` 只根据时间 t（秒）摆好文字和画布，
  所以任意一帧都能单独、确定地画出来。
- `render.cjs`：用 Playwright 驱动无头 Chromium，4 个页面并行逐帧截图（共 4590 帧）。
- `music.py`：只用 numpy 合成配乐——环境和弦、拨弦旋律、打字声、提示音和混响。
  画面里每次打字、打勾、时间线节点都会导出到 `cues.json`，音效和画面逐帧对齐。
- `build.sh`：渲染 → 合成配乐 → 用 FFmpeg 编码成 MP4。

## 重新生成

需要 Node.js（带 Playwright 和 Chromium）、Python 3 + numpy、FFmpeg。

```bash
cd claude-origin-film
npm install --ignore-scripts   # 安装 Noto Serif SC / Noto Sans SC / JetBrains Mono 字体
./build.sh
```

只想看几张静帧：`node render.cjs --scale 0.5 --stills 12.5,45.2,116.9`（输出到 `preview/`）。
也可以直接用浏览器打开 `film.html` 实时播放（字体从 Google Fonts 加载，配乐读取 `music.m4a`）。

## 关于史实

片中的时间和事件依据 Anthropic 公开发布的信息，为了好懂做了简化：

- “预测下一个词”里的概率是示意数字。
- 可解释性一段里的“韵脚”“数字”“金门大桥”“情绪”是示意标签，“金门大桥”向 Golden Gate Claude 演示致意。
- “名字致敬克劳德·香农”是流传较广的说法，所以片中写的是“据说”。
