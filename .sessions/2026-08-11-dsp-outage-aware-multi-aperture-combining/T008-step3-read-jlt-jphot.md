# T008: Step 3 精读 JLT 2023 与 JPHOT 2020

> 2026-08-11 | assignee: fresh reader B | timebox: 15 minutes

## 目标

只精读并审计以下两篇合格全文，产出 estimator-changing competitor 与 phase-alignment neighbor 的结构化证据：

1. Liu et al., JLT 2023, DOI `10.1109/JLT.2023.3276637`；
2. Tu et al., IEEE Photonics Journal 2020, DOI `10.1109/JPHOT.2020.2977955`。

## 必读输入

- `stages/gw-read.md`
- `stages/glossary.md`
- `domain-comms.md`
- `D:/code/study/research-protocol/papers/doi/10.1109_jlt.2023.3276637/content.md`
- `papers/doi/10.1109_jphot.2020.2977955/content.md`
- 可审计既有 JLT note，但不得用 note 代替全文：
  - `D:/code/study/research-protocol/papers/_read_notes/10.1109_JLT.2023.3276637.md`

## 执行合同

- 先核标题；不匹配立即停止该篇并报告。
- 每篇至少覆盖 14 个标准字段：DOI、source path、read status、venue、year、贡献（至少两句）、方法概览、实验设置、baseline、结论、与本专题关系、具体实现、fit、code、validation。
- 每篇显式给 7 个结构段：state、action、reward/objective、model assumptions、network/algorithm、fit、problem extraction（M-C-A 与 glossary 四判据）。非 DRL 项写 `N/A`。
- 提取通信参数、每篇实验完备性（不超过 20 行）、逐项 evidence pointer（章节/表/图/全文行号）。
- 给每篇精确 `input -> trigger/action -> output`；重点说明 JLT 2N×2 CMA/RDE adaptive equalizer 在 raw signals 上处理 gain/phase/SOP/skew 的边界，以及 JPHOT 2020 phase alignment 的位置与输出。
- 给 JLT 2023 至少 1 个不超过 20 行的写作架构摘要。
- 只报告论文事实与候选问题证据；不得替主线判 Q# terminal，不设计算法，不搜索、不下载、不仿真。

## 唯一输出

只创建：`projects/thesis-fso/worker-logs/step-3-dsp-outage-read-l3-l4.md`。
不得修改 read-log、read notes、literature_notes、topic/session/master/registry。

## 完成回执

返回标题门、两篇字段完整性、最关键动作签名、证据路径、输出文件；若无法按时完整，明确缺项。
