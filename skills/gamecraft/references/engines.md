# 引擎与工具选型参考

来源快照日期 2026-10-29。以下版本与工具状态是当日来源记录，不是实时最新事实；使用前按官方文档与本地实测复核。

## 选型方法

- 由交付目标决定：浏览器成品/低成本验证可考虑 Three.js 类方案；需要原生编辑器、成熟模板与成套资产的 3D 项目，在 UE、Unity、Godot 中按可跑通模板选。
- 不以单个演示视频判断引擎优劣，也不听“最好”“3A”类宣传语。
- 视频案例中三个 3D 项目来自同一原作者（Stefan 3D AI）的转载/译配，不构成多来源独立证据。

## Godot

- 龙战案例：Three.js 原型后迁 Godot（[BV16jjj6WEkc 02:17](https://www.bilibili.com/video/BV16jjj6WEkc/?t=137)）。迁移后需重选水面、天空、特效插件，阴影问题未解决（[07:48](https://www.bilibili.com/video/BV16jjj6WEkc/?t=468)）。
- 内置类型命名冲突、场景误跳转等工程问题见 production.md 的 2D 复盘；属具体冲突，不是普遍规则。

## Unity

- 角色/动画案例：先 HUD HTML 原型，再建单位试玩场，复用动作片段（[BV1C5ab6MEU1 01:00](https://www.bilibili.com/video/BV1C5ab6MEU1/?t=60)、[06:15](https://www.bilibili.com/video/BV1C5ab6MEU1/?t=375)）。
- 效果与耗时为个人经验，不作为引擎或模型对比结论。

## Unreal Engine

- 跑酷教程使用 UE 5.7 指南（[BV1cCEi6sEU5](https://www.bilibili.com/video/BV1cCEi6sEU5/)）。UE 5.7 的步骤、端口、安装法不能盲目套到 UE 5.8。
- Epic 官方 Unreal MCP 文档（[dev.epicgames.com](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor)）标记 Experimental：可驱动编辑器、检查对象、跑自动测试，但功能和 API 仍可能变化。本技能记录来源时未安装或握手，实际接入需本机验证。
- 社区方案（均为独立项目，非 Epic 官方，未在本机安装；许可证落地前单独核实）：
  - VibeUE：主推 UE 5.8 原生 MCP 扩展，[原仓库 5-8 分支](https://github.com/kevinpbuckley/VibeUE/tree/5-8)。
  - Unreal Engine Skills：[仓库](https://github.com/kevinpbuckley/unreal-engine-skills)，目标 UE 5.8，README 强调按本机引擎源码交叉核验。
  - UnrealClaude：[仓库](https://github.com/Natfii/UnrealClaude)，声明 UE 5.7，并提示蓝图编辑有问题；不能认定对 5.8 无条件兼容。
- 规划方法可借鉴 Superpowers（[仓库](https://github.com/obra/superpowers)）的上下文检查、分解与验收，但不要照搬长串提问。

## 浏览器与 Web

- Three.js 适合可玩验证或浏览器成品；迁移到引擎时重新评估插件与性能。
- 龙战案例还使用 Neural4D 赞助；不采用其宣传语作为质量结论。

## 资产与插件来源

- 优先引擎自带模板、官方示例、可核实许可证的社区模板。
- 记录每个模板/资产的来源、版本、许可证与获取方式；不代购、不代下载未授权内容。
- AI 生成资产（模型、贴图、动画）进入项目前走 production.md 的规格与试玩场检查。

## 版本记录模板

```
日期：2026-10-29
引擎与版本：<名称 版本号>
来源类型：官方文档 / GitHub 仓库 / 视频演示 / 本机安装
是否本机验证：是/否
已知限制：
```

版本结论一律写成当日快照，不用作实时最新依据。
