# Voice — Research Direction Lab 完整体系设计

> 用户原话档案，按日期。执行提示词与旧对话报告不冒充用户自然原话。

## 2026-07-20

- "感觉，是skill的能力和代码的能力混了？代码只做比较轻量的控制以及那些碎片步骤。流程尽可能靠skill？这设计思路是不是不对" → D001
- "是。以及，我之前的那些原话，里面有很多我在乎的东西，得考虑到" → D001, D002
- ".sessions\\2026-07-17-direction-lab-governance-pilot\\voice.md 你也看看" → D002
- "以及，之前对于skill的设计也做了不少，但每次都说不完善然后就给我写进了普通的文档。我感觉，咱们这次最好先一次把整个体系都规划好？" → D001
- "认可" → D003
- "继续。顺便推演一下使用？" → D005, D007

## 2026-07-20（Task 9 shadow 授权提示词）

> 来源：执行提示词（粘贴文本，非对话原话，按 voice-quote.md §"执行提示词"规则标 [转述:执行提示词]）
> 注：本段是用户授权 Task 9 shadow 的执行提示词关键约束，非自然对话原话；不冒充用户自然原话。

[转述:执行提示词] "你现在获得明确授权，执行 Research Direction Lab 的 Task 9 live shadow；若 Task 9 独立终验 PASS，则继续执行 Task 10 cutover 和最小化 AGENTS.md 路由固化。不要开 Goal。不要等待我逐步确认，在授权边界内持续推进，直到得到 PASS、明确 FAIL/PARTIAL，或所有合法路径都耗尽。" → D008
[转述:执行提示词] "不要在主 worktree 或旧 p03/unified-batch-runner dirty worktree 上执行。" → D008
[转述:执行提示词] "地基证书必须先于科学批跑。" → D008（Foundation Certificate 强制）
[转述:执行提示词] "性能数字只能留在 shadow/sandbox artifact，不能进入正式论文材料" → D008
[转述:执行提示词] "存在合法替代工作时不得因单个 blocker 停止" → D008（自动续跑）
[转述:执行提示词] "只有涉及战略性范围扩张、不可逆改动或所有合法路径耗尽时才请求用户" → D008（escalation 边界）
[转述:执行提示词] "每完成一个科学 batch 都必须产生 harvest" → D008
[转述:执行提示词] "STATUS 必须始终保持一页可读入口" → D008
[转述:执行提示词] "Task 9 和 Task 10 分别独立复核。实现 agent 不得自审自验。" → D008
[转述:执行提示词] "必须解决 AGENTS.md 当前'stages/groundwork 是唯一合法研究路径'与 Direction Lab 的表面冲突。" → D008
[转述:执行提示词] "整个对话只在收尾时提交一次；不要 push。" → D008
