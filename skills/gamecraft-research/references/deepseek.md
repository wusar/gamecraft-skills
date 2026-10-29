# DeepSeek 接入：搜索、抓取与模型分工

核验日期：2026-10-29。当前原始资料：[Search & Fetch](https://api-docs.deepseek.com/guides/search/)、[Search schema](https://api-docs.deepseek.com/api/search/)、[Fetch schema](https://api-docs.deepseek.com/api/fetch/)、[Responses 兼容性](https://api-docs.deepseek.com/guides/responses_api/)。实际使用前刷新会变化的限制和计费。

独立 API：`POST https://api.deepseek.com/v1/tools/search` 接收 query、count、need_content；Fetch 为 `/v1/tools/fetch`，接收 url。它们与模型调用分开，使用同一 DeepSeek API Key。query 为 1–128 字符，count 为 1–50；Fetch 目标 URL 不得包含账号密码。

搜索可用 `site:`、引号、排除词和日期约束。先用少量结果收敛到原始来源，再抓取需要核验的页面；不要把排名或 authority 分值当事实验证。

模型的作用：规划检索、提炼经验、检查矛盾。搜索服务的作用：提供真实网页和原链接。可以把独立 Search/Fetch 结果交给 Flash，也可使用宿主已有联网工具；Flash 本身的文本回答不证明联网成功。Responses 文档本次列内置 `web_search` 支持 V4 Pro、Flash 忽略该工具；不能把内置工具兼容性与独立 Search API 混为一谈。

公开 API 请求会消耗服务额度，计费可能变化。缓存命中不重新发送，空结果保留为空，鉴权或限流错误不自动切换付费模型。模型 Token、搜索次数与订阅用量分开记录；没有实际账单数据不声称具体节省。

本项目首次验证：4 次 Search HTTP 200 且有结果；后续 Fetch 和 CLI 的状态见 `docs/validation.md`。仅这一小样本，不代表长期可用性或搜索质量基准。
