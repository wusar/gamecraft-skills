---
name: gamecraft-research
description: 从开发视频、官方文档和原仓库提炼可追溯的游戏制作经验；适用于学习工作流、比较工具及把经验更新成 skill，可选 DeepSeek Search/Fetch。
---

# 从资料到可执行经验

先定义本次需要回答的决策和缺少的证据，复用项目已有资料。只搜索公开任务词，不把私人聊天、日志或凭据发给检索服务。已有目标引擎和平台时据此收窄；缺失但不影响检索时先给合理默认。

## 检索

1. 本机成果与缓存 → 官方文档和 GitHub 原仓库 → 制作视频和复盘。GitHub 读 README、相关源码、Issues 和 Releases；不按星数直接认定质量。
2. 优先有真实操作、运行画面、失败分析及可用工程的视频。记录原作者；译配、转载、同一系列不能算多个独立验证。
3. 需要 DeepSeek 时读 [接入说明](references/deepseek.md)。提供方不可用就换现有搜索工具，保留限制。模型给出的流畅答案不能代替网页正文。

## 视频分析

遵守来源访问条件。优先复用已有字幕或可合法获取的音轨；需要浏览器时先核验已有会话，不导出 Cookie。没有访问就记录为候选，不能写“已看完”。

对实际取得的音频按短块转写并缓存，抽查关键画面。记录覆盖范围、音轨/字幕/视觉各自状态及 ASR 不确定术语；重复文本、静音段幻觉和模型名称需单独核对。视觉复杂的动作需看动态片段，截图不能证明碰撞与手感正确。

使用 [经验卡模板](references/evidence.md) 记录：**结论 → 来源与时间点 → 适用条件 → 如何验收 → 已知失败 → 证据等级**。

## 提炼与落地

- 保留改变开发决定的非显然经验，合并同义项，明确代价及例外。不要把作者一次成功变成“永远”“必须”。
- 将搜索发现、读过正文、作者演示、本机测试和公开交付分开标注。测试了某组件不能自动证明整条管线可用。
- 进入游戏任务时只加载相应的少量经验。更新 skill 后用真实场景试用，再修正有证据的问题。
- 开源只发布原创提炼、短摘与原链接，不镜像第三方完整视频、音频、字幕或私有资料。

## 附带检索工具

Python 3.10+，仅标准库；密钥仅从 `DEEPSEEK_API_KEY` 环境变量读取。

```sh
python scripts/research.py search 'Godot scene testing site:github.com' --count 5 --dry-run
python scripts/research.py search 'Unity MCP debugging site:github.com' --count 5
python scripts/research.py fetch 'https://docs.godotengine.org/en/stable/'
```

脚本路径相对于本 skill 目录。默认写本地 `.cache/gamecraft-research`；没有 Key 时先检查有效缓存，缓存复用不需要凭据，新的联网请求才需要 Key。搜索结果只是发现线索。`--out` 可保存新 JSON；`--refresh` 明确请求重新联网。遇失败不自动重试计费请求。费用与模型支持以当前官方正文为准，不承诺永久免费。
