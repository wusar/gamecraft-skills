# 相关开源方案

查询日期：2026-10-29。以下仅核对原仓库 README 与 GitHub 元数据；未安装或执行，没有将 README 的效果、成本和性能说法作为独立实测。提交快照与当时许可证记录在[来源登记](../research/sources.json)，后续使用应重新核对版本和依赖。

| 项目 | README 描述的用途 | 可借鉴之处 | 本项目的取舍 |
|---|---|---|---|
| [MihirSahu14/playbench](https://github.com/MihirSahu14/playbench) | 用机器人运行真实构建、收集试玩日志并迭代平衡 | 把运行证据和交付门槛放进循环 | 作为后续自动试玩候选，尚未核对具体引擎接入，未引入依赖 |
| [g0dam/video-studio-skills](https://github.com/g0dam/video-studio-skills) | 从审美方向、故事、资产设定到分镜、渲染包和 QA | 阶段产物持久化及连续性约束 | 可用于较长介绍片的规划；它本身不代表已接通视频生成后端 |
| [RandomNest/aivideo-production-skills](https://github.com/RandomNest/aivideo-production-skills) | 面向不同模型的视频制作产物、镜头规划与质量检查 | 角色/世界状态连续性、预算与返修记录 | 作为模型生成镜头的参考，当前介绍片仍使用已验证的代码动效路线 |

三者查询时均标注 MIT。这里只发布原创摘要与原链接，未复制其技能指令，也未据此宣称它们优于其他方案。
