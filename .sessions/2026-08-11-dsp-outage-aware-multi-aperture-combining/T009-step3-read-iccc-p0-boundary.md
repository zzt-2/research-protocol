# T009: Step 3 精读 ICCC 2022 并核 2019 P0 边界

> 2026-08-11 | assignee: fresh reader C | timebox: 15 minutes

## 目标

精读 ICCC 2022 reliability MRC，并只用既有 metadata/abstract/receipt 审计 2019 P0 的可断言边界。P0 不是第六篇全文，不得推断其 exact action。

## 必读输入

- `stages/gw-read.md`
- `stages/glossary.md`
- `domain-comms.md`
- `papers/doi/10.1109_iccc56324.2022.10065885/content.md`
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/R001-step1-synthesis.md`
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/step1-provenance-receipt.md`
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/step1-candidate-collision-matrix.md`
- `search-archive/2026-08-11/step2-p0-oa-title.json`

## 执行合同

- 先核 ICCC 标题；不匹配立即停止并报告。
- ICCC 至少覆盖 14 个标准字段：DOI、source path、read status、venue、year、贡献（至少两句）、方法概览、实验设置、baseline、结论、与本专题关系、具体实现、fit、code、validation。
- 显式给 7 个结构段：state、action、reward/objective、model assumptions、network/algorithm、fit、problem extraction（M-C-A 与 glossary 四判据）。非 DRL 项写 `N/A`。
- 提取通信参数、实验完备性（不超过 20 行）、逐项 evidence pointer（章节/表/图/全文行号）。
- 给 ICCC 精确 `input -> trigger/action -> output`，重点分辨 pilot/LS/MMSE estimation quality 是否真正驱动权重，还是仅分析传统 MRC under estimation error。
- 对 2019 只形成三栏：可由 title/abstract 断言、不可断言、若 Q# 存活则 Step3.5 必须补的债；不得称 fulltext read，不得给 exact collision verdict。
- 不替主线判 Q# terminal，不设计算法，不搜索、不下载、不仿真。

## 唯一输出

只创建：`projects/thesis-fso/worker-logs/step-3-dsp-outage-read-l5-p0-boundary.md`。
不得修改 read-log、read notes、literature_notes、topic/session/master/registry。

## 完成回执

返回标题门、字段完整性、ICCC 动作签名、2019 可断言边界、证据路径、输出文件；若无法按时完整，明确缺项。
