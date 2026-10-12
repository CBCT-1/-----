#!/usr/bin/env bash
# 一键生成《我是怎么来的》：逐帧渲染 → 合成配乐 → 编码成 MP4
set -euo pipefail
cd "$(dirname "$0")"
[ -d node_modules/@fontsource ] || npm install --ignore-scripts --no-audit --no-fund
rm -rf frames && mkdir -p build
node render.cjs --workers "${WORKERS:-4}"
python3 music.py cues.json build/music.wav
ffmpeg -y -v warning -framerate 30 -i frames/f%05d.jpg -i build/music.wav \
  -c:v libx264 -preset slow -crf 23 -tune animation -pix_fmt yuv420p \
  -c:a aac -b:a 160k -movflags +faststart -shortest how-i-came-to-be.mp4
ffmpeg -y -v warning -i build/music.wav -c:a aac -b:a 160k music.m4a
echo "完成：how-i-came-to-be.mp4"
