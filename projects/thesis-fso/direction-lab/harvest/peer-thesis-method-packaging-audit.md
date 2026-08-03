# 同行硕士论文方法包装审计

> 2026-08-03 | owner: `.sessions/2026-07-09-thesis-writing` / S018 / D025
> 用途：区分旧调研的真实证据深度，并为本轮统一的“方法章→增量→recipe→内部映射”抽取建立基线。

## 1. 旧调研实际覆盖

| 批次 | 旧口径 | 可复核的读取深度 | 审计结论 |
|---|---:|---|---|
| thesis-structure-research | 34 篇全文分析 | 留存 5 篇目录级记录和 4 篇独立结构分析；最初 5 篇任务字段是章间衔接、共享元素和独立性，不是方法动作 | 不能按“34 篇方法章全文精读”使用；其余 25 篇缺少可审计记录 |
| 2026-05-31 thesis-writing-prep | 无统一篇数 | 主要使用题名、摘要和综述层证据；个别全文未取得或仍待下载 | 适合写作结构/措辞校准，不是方法包装逆向工程 |
| 2026-06-17 method-redirection | 首轮 21 篇，二轮 11 篇，合计常被表述为 32 篇 | 深度混合：部分 CPE、张岱、唐承茂进入方法细节；二轮只明确第一批 5 篇精读；原始子 agent 记录未独立归档 | 不能按“32 篇均精读两个方法章”使用 |

证据：`.sessions/_archive/thesis-structure-research/H001-deep-read.md:9-14`、`.sessions/_archive/thesis-structure-research/topic-index.md:10-20,55`、`.sessions/2026-05-31-thesis-writing-prep/S005-innovation-restructure.md:28-33`、`.sessions/2026-05-31-thesis-writing-prep/R004-survey-signal-processing-framing.md:207-220,280-288`、`.sessions/2026-06-17-thesis-method-redirection/R001-survey-peer-master-theses.md:5,21-29,41-74,141-157,179-187,256-280,762-765`。

## 2. 七个问题的事实回答

1. **看了多少篇、读到多深**：可复核的是 5 篇目录精读、4 篇独立结构分析，以及后续混合深度的 21+11 篇候选；不能把三个口径相加后称为统一方法章精读。
2. **全文还是摘要/目录**：三者都有，但没有统一深度。结构研究主要读目录，写作准备主要读摘要/题名，方法重定向只有一部分进入具体方法章。
3. **是否拆出 baseline→method delta**：早期没有；后期对 4b#1 拆出了 `唐承茂静态 B=27/D=38 → 自适应交织`，并附 FPGA 控制增量。
4. **是否映射到本项目资产**：仅对单个交织候选映射到 FPGA、开环与硬件约束；没有建立同行 recipe 到当前 Ch3/Ch4/Ch5 资产的逐章映射。
5. **是否形成可执行 recipe**：形成过 4b#1 的单候选 Groundwork 合同，含 baseline、delta、上界门和 MVE PASS 标准；但没有形成可迁移的包装 recipe library。
6. **为何没产出可用方法**：直接原因是静态 `B=27` 已全程足够，自适应交织的 BER 增益上界为 0 dB，时延指标又无硕论先例；流程原因是先从“交织方法”反推问题，跳过 GW Step 3 的 M-C-A 问题发现链。
7. **哪些旧结论仍有效**：算法+FPGA 验证是常见硕士形态、小幅 dB 增益可以构成硕士工作量、唐承茂静态交织参数可作为失败史 baseline；“34 篇均全文深析”“32 篇均精读方法章”、仅从题名得到的方法内核、Le 2021 的 GG 模型断言均应拒绝或降级。

执行合同证据：`.sessions/2026-06-17-thesis-method-redirection/decisions.md:211-244`、`.sessions/2026-06-17-thesis-method-redirection/handoffs/H004-groundwork-entry-4b1-adaptive-interleaving.md:9-15,31-40`。失败证据：`.sessions/2026-06-19-4b1-adaptive-interleaving-groundwork/S001-groundwork-feasibility-fr21-kill.md:20,35-55`。问题链纠偏：`.sessions/2026-06-20-problem-driven-redirection/R001-six-kill-commonality-and-gw-step3-correction.md:14-23,29-57`。

## 3. Root-cause table

| 表象 | 已验证根因 | 后果 | 本轮纠正 |
|---|---|---|---|
| 看了很多却没有 recipe | 旧任务目标是结构、写作校准或选方向，不是逐篇抽取方法动作 | 输出停在分类、排名或章节标题 | 每篇固定抽取两个方法章的 baseline→actual delta |
| “34/32 篇”显得覆盖很深 | 统计口径混合，部分原始记录缺失 | 无法逐篇复核读取深度 | 只计有学位元数据、全文路径、章节范围和 delta 的样本 |
| 候选一度可执行但很快 Kill | 先定方法再反推问题，物理天花板后置暴露 | 单候选合同无法转化为可用方法 | recipe 只能提供包装形态，不能替代 M-C-A 与上界门 |
| 外部调研无法迁移到当前论文 | 只对单候选做约束映射，没有逐章内部资产表 | Ch3/Ch4/Ch5 没有现成方法合同 | 将真实 recipe 映射到内核的 action、baseline、证据和最小缺口 |
| 普通硕士粒度仍不清楚 | 旧记录常用“创新强/弱”评价，没有统一记录公式、流程、实验和消融规模 | 容易把硕士方法误按顶刊标准淘汰 | 本轮用统一 14 字段模板重读真实硕士论文 |

## 4. 保留与拒绝

| 旧结论 | 证据等级 | 处置 |
|---|---|---|
| 算法+FPGA 验证是常见硕士组织形态 | 全文聚合 | 保留为写作形态证据，不等同于本项目已有新方法 |
| 4b#1 可与唐承茂静态交织比较 | 全文 delta | 保留为失败路线的完整 baseline 记录 |
| 4b#1 有有效 BER 增量 | 上界与实测反证 | 拒绝；不得复活 |
| 34 篇均完成全文方法分析 | 无完整审计链 | 拒绝 |
| 32 篇均精读核心方法章 | 混合深度 | 拒绝 |
| Le 2021 已证明特定 GG-LCR/AFD 上游模型 | 摘要推断且 DOI/模型存疑 | 拒绝/未证实 |

## 5. 最小结论

旧工作失败的准确表述是：**证据深度不均、任务目标错位、没有统一 baseline→delta→recipe→内部映射单元，并在唯一可执行候选上先定方法后找问题**；不是“完全没有全文阅读”。本轮只有带逐篇章节范围和真实动作差异的样本才能进入 recipe library。
