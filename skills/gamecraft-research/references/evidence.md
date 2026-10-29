# 经验卡

```json
{
  "id": "asset-animation-contract",
  "claim": "为同一角色确定一个位移拥有者，避免脚本移动与动画根位移叠加",
  "source_ids": ["video-character-import"],
  "timestamp_seconds": 0,
  "evidence_level": "author_demonstration",
  "applies_when": "角色移动由脚本控制，动画也包含平移",
  "verify": "播放移动动作并检查实际位移、脚滑与碰撞，确认脚本或 root motion 中只有一方负责移动",
  "limits": "使用 root motion 的设计不应一律改为 In Place",
  "local_test": null
}
```

时间点必须来自实际转写/画面核对，不能照此模板的 0 秒造一个证据。来源应包含标题、作者、原作者/转载关系、URL、发布日期、核验日期、版本及访问状态。

等级：`discovered`（只搜到）、`retrieved`（取得正文或媒体）、`author_demonstration`（作者展示）、`local_test`（本机真实任务通过）、`shipped`（可用交付）。等级说明对象和范围，不能只靠整数升级。实现与教学演示使用不同标签。

同一个问题可有相互矛盾的经验；保留引擎版本、镜头、设备、素材和测试方法，按条件选择，不用“多数视频都说”抹平差异。
