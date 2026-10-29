# 生产参考：3D 原型、资产与验收

来源：最初 7 条及追加 4 条 B站视频的全长音轨转写与每条 12 帧抽查，分析日期 2026-10-29。以下为简短转述；本机未复现作者工程。

## 证据分层

| 层级 | 含义 | 用法 |
|---|---|---|
| 视频说法 | 口播/字幕主张 | 只能作为假设 |
| 作者演示 | 视频里出现的运行画面 | 说明“可能做到”，非保证 |
| 本机测试 | 自己跑过的构建与日志 | 可作为验收依据 |
| 已发布游戏 | 有发布包与外部反馈 | 证明交付状态，具体行为仍需验证 |

写作与汇报时显式标注层级，不用作者演示替代本机测试。

## 原型路线

- 先做可玩小样，再扩规模。龙战案例先在 Three.js 做出可玩版再迁 Godot（[BV16jjj6WEkc 02:17](https://www.bilibili.com/video/BV16jjj6WEkc/?t=137)）。这是该作者经验，不代表所有项目都要双引擎。
- 浏览器方案（如 Three.js）可承担低成本玩法验证或成品交付；需要原生交付时再单独评估迁移成本。
- 迁移时重新选插件：水面、天空、特效等要按目标引擎重新适配（[06:26](https://www.bilibili.com/video/BV16jjj6WEkc/?t=386)、[07:48](https://www.bilibili.com/video/BV16jjj6WEkc/?t=468)）。

## 工程节奏（UE 跑酷案例）

- 先建 Git，阶段可用即存检查点（[BV1cCEi6sEU5 04:50](https://www.bilibili.com/video/BV1cCEi6sEU5/?t=290)）。
- 从第三人称模板角色起步，按顺序加无限路径、移动、障碍、金币、结算（[05:33](https://www.bilibili.com/video/BV1cCEi6sEU5/?t=333)）。
- 运行、截图、检查场景；用明确命名和参考图识别资产（[06:43](https://www.bilibili.com/video/BV1cCEi6sEU5/?t=403)）。
- 作者最后仍有误判死亡、桥面接缝、障碍穿模、金币重叠等问题（[14:18](https://www.bilibili.com/video/BV1cCEi6sEU5/?t=858)）。说明“做完流程”不等于“品质完成”，验收要覆盖边界输入。

## 模板与成套资产

- 48 小时 Roguelike 作者明确使用购入模板与现成植被水面资产（[BV1cpjF6jEGV 07:16](https://www.bilibili.com/video/BV1cpjF6jEGV/?t=436)）。加速来自模板和成套资产，不来自单纯模型能力。
- 场景拆成可组合小部件，统一视觉方向（[02:54](https://www.bilibili.com/video/BV1cpjF6jEGV/?t=174)）。
- Blender 内调旋转、导出、绑定后仍需手工修权重（[05:38](https://www.bilibili.com/video/BV1cpjF6jEGV/?t=338)）。
- 进引擎前统一缩放、旋转、轴心（[10:53](https://www.bilibili.com/video/BV1cpjF6jEGV/?t=653)）；作者自称结果是可玩原型（[18:53](https://www.bilibili.com/video/BV1cpjF6jEGV/?t=1133)）。

## 资产规格清单

- 单位：米或厘米，导出与导入一致。
- 轴向：前进轴(+X/+Y/+Z)、上轴，导入设置中的轴转换要记录。
- 骨架：人形或通用绑定，骨骼命名、根骨骼、是否混合控制骨。
- 动画：动作名、是否循环、根运动有无、帧率、事件/通知名称。
- 材质：贴图尺寸、PBR 通道、是否需要重烘焙。
- 碰撞：哪一层、近似形状、是否需要手动碰撞。
先锁定会影响当前玩法的规格；导入后在试玩场验证，简单占位不必先写完整资产手册。

## 追加视频的具体教训

- 脚本控制位移时检查动画是否也含平移；作者使用 In Place 避免二者叠加（[BV1aaez6WED9 02:29](https://www.bilibili.com/video/BV1aaez6WED9/?t=149)）。采用 root motion 的设计不能一律关闭。若攻击判定依赖骨架、体型与武器，提前用接近正式规格的角色测试（[01:16](https://www.bilibili.com/video/BV1aaez6WED9/?t=76)）。
- Unity 现场教程记录脚本编译后 MCP 连接断开（[BV1gP7Q6VEZy 14:12](https://www.bilibili.com/video/BV1gP7Q6VEZy/?t=852)）。重连后先读取实际编辑器状态，再判断上一次修改是否完成，避免盲目重发。该问题属于当时的插件和环境，不代表所有版本。

## 角色与动画

- HUD 先做可点击 HTML 原型定规格，再接入引擎（[BV1C5ab6MEU1 01:00](https://www.bilibili.com/video/BV1C5ab6MEU1/?t=60)）。
- 建单位测试场，快速切角色和预览动作（[06:15](https://www.bilibili.com/video/BV1C5ab6MEU1/?t=375)）。
- 复用已有动作与动捕片段，再适配武器与比例（[09:23](https://www.bilibili.com/video/BV1C5ab6MEU1/?t=563)）。
- 用可保存的姿势截图做反馈，减少“再转一点”式猜测（[22:00](https://www.bilibili.com/video/BV1C5ab6MEU1/?t=1320)）。
- 作者承认部分生成过程未录，效果与耗时为个人经验，不能证明某模型稳定更优。

## 问题定位方法

- 过曝/光照错误：先复现、截图，逐项关闭效果定位，不用模糊要求（[BV16jjj6WEkc 03:56](https://www.bilibili.com/video/BV16jjj6WEkc/?t=236)）。
- 绑定异常（翅膀不自然、角随翅膀动）：导入 GLB 后仍会出现，需在试玩场逐骨检查（[06:26](https://www.bilibili.com/video/BV16jjj6WEkc/?t=386)）。

## 长期维护（2D 复盘，工程经验可复用）

- 内置类型名冲突会让工具测试与引擎运行结果不一致；把检查意见标 TODO 后集中处理（[BV1bFk7BvEuL 05:34](https://www.bilibili.com/video/BV1bFk7BvEuL/?t=334)、[07:34](https://www.bilibili.com/video/BV1bFk7BvEuL/?t=454)）。该建议限于具体冲突，不扩大为“禁止所有 class_name”。
- 保留有效场景清单，分小模块并持久记录验收；提交时可能仍有失败测试与误跳旧场景（[BV1k16YBwE2V 03:29](https://www.bilibili.com/video/BV1k16YBwE2V/?t=209)、[06:19](https://www.bilibili.com/video/BV1k16YBwE2V/?t=379)、[08:18](https://www.bilibili.com/video/BV1k16YBwE2V/?t=498)）。作者对颜色问题的解释未在本机复现，不写成引擎定律。
- 通用系统与独有玩法分离，便于复用（[BV1xBrDB9E42 02:33](https://www.bilibili.com/video/BV1xBrDB9E42/?t=153)）。
- 以上三条为 2D 项目，只作工程经验参考，不作 3D 产能证据。

## 验收清单

- 实际启动构建或 PIE，注入输入，收截图与日志。
- 记录构建号/提交哈希/环境版本快照。
- 边界输入（快速切换、重叠、边缘碰撞）单独测。
- 未解决项进入待办并写进交付说明。
