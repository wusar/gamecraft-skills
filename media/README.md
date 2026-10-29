# 项目介绍视频

路线：ImageGen 概念插画 + 确定性 Canvas 动效 + Windows Huihui 合成旁白 + 字幕 + FFmpeg。它是 AI 辅助讲解视频，画面不代表实机或视频模型生成结果。

成片作为 GitHub Release 附件，二进制不进入 Git 历史；概念图、分镜和渲染源码可修改重建。没有使用第三方研究视频的音画。

依赖：Node.js 20+、Playwright（可用 `PLAYWRIGHT_MODULE` 指向已有模块）、Chromium/Edge（`CHROME_PATH`）、Python 3.10+、FFmpeg（`FFMPEG_PATH`）。旁白脚本使用 Windows System.Speech；其他系统可准备相同分句 WAV。

```powershell
powershell -NoProfile -File media/make-narration.ps1
python media/prepare_timeline.py
node media/render.mjs
```

结果在 `media/output/`，默认拒绝覆盖最终 MP4。公开成片和验证范围见根目录 README。
