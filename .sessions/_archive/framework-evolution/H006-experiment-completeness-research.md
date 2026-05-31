# [H006] 实验完备性缺口调研

> 来源: S006 | 交接目标: 多角度调研后确定框架增强方案
> 文件名: H006-experiment-completeness-research.md

## 背景

框架目前只有纵向主线（GW→Contract→Execute），缺少"审稿人视角"的横向覆盖机制。从 leo-congestion-routing 漏洞审计（session 1840cd63）发现 6 项修复全部是事后补救，框架在设计阶段无拦截。

核心问题：研究者（和 AI）都不知道"论文实验部分该做到什么程度才算完备"，只能拍脑袋，导致事后大量返工。

已写入 S006（`.sessions/framework-evolution/S006-experiment-completeness.md`）。

## 必读

1. `.sessions/framework-evolution/S006-experiment-completeness.md` — 完整诊断
2. `.sessions/framework-evolution/topic-index.md` — 框架演进全局状态
3. `stages/gw-read.md` — 现有精读流程（含写作架构提取，了解现有能力边界）
4. `stages/contract.md` — Contract 阶段流程（对标检查可能加在这里）
5. `templates.md` — 文档模板（了解现有提取模板结构）

## 调研任务（大量子 agent 并行）

### 第一批：方法论调研（web search，不依赖论文库）

每个角度派多个子 agent，确保覆盖充分。子 agent 必须返回结构化摘要（≤500 词），不能灌原文。

#### A. ML 顶会论文检查表

- NeurIPS/ICML/ICLR 的 paper checklist 具体内容
- 审稿人被要求检查哪些实验维度
- 这些检查表是怎么设计的、涵盖什么

#### B. 目标期刊审稿标准

- IEEE TWC / TCOM / JSAC 的 reviewer guidelines
- IEEE 审稿人实际被要求评估什么
- 有没有实验完备性相关的标准

#### C. 学术论证方法论

- Toulmin argumentation model 在学术写作中的应用
- claim-evidence mapping 方法
- 其他学术写作方法论中关于"证据充分性"的部分
- 最好找具体的教程或论文

#### D. 论文拒稿原因分析

- ML/DL 论文常见拒稿原因，特别是实验相关的
- "incomplete evaluation" "insufficient experiments" "missing baselines" 等常见拒稿理由
- 最好找博主/审稿人分享的经验文章

#### E. 实验设计最佳实践

- "what makes a good ML paper experiment section"
- 实验可复现性 checklist
- 是否存在系统性的"实验完备性框架"

### 第二批：竞品论文实证分析（读已有 content.md）

从已有论文库中选 10-20 篇精读过的论文，系统提取实验完备性维度。

**提取维度**（每篇论文都要提取）：

1. **指标清单**：报了哪些指标，主指标和辅助指标分别是什么
2. **统计检验**：用什么检验、几组种子、怎么报告（p-value/CI/error bar/表格/文字）
3. **Baseline 矩阵**：几个 baseline、什么类型（经典/DL/启发式/消融）、是否声明实现来源
4. **消融实验**：消融了什么、怎么消融（零向量 vs 删除 vs 替换）、几个实验
5. **鲁棒性/泛化**：测了哪些条件变化（规模/噪声/参数/场景/极端条件）
6. **声称-证据对应**：结论中的每个声称对应哪个实验/表/图
7. **参数展示**：参数怎么展示（集中表格 vs 散落）、是否标注出处
8. **可视化类型**：什么类型的图、几张、什么范式
9. **对比公平性**：是否声明了公平对比条件（相同数据/相同超参搜索/相同训练预算）

**产出要求**：
- 每篇论文提取为结构化 JSON 或 markdown 表格
- 最终汇总为"领域实验完备性矩阵"：每项维度在 N 篇论文中的出现频率
- 标注哪些是"领域标准"（≥70% 论文做了）、哪些是"加分项"（30-70%）、哪些是"罕见但有力的"

### 子 agent 调度建议

- 第一批 5 个角度，每个角度 1-3 个子 agent（看搜索结果量），约 9-15 个
- 第二批论文分析，按 3-5 篇/agent 分批，约 4-6 个
- 总计约 13-21 个子 agent，分 2-3 批执行
- 每批结果汇总后再决定下一批是否需要调整

**注意**：子 agent 时间上限 15 分钟（900s）。单次搜索 + 摘要控制在 500 词以内。

## 调研完成后的产出

1. **"实验完备性提取"模板**：加在 gw-read.md 的提取模板中，和现有"写作架构提取"并列
2. **"对标检查"步骤设计**：加在 Contract 哪一步、具体检查什么、输出什么
3. **"声称-证据映射"的最终形态**：基于调研确定具体格式
4. **框架文件修改方案**：列出需要改的文件和具体改动

产出写入 R001（`.sessions/framework-evolution/R001-experiment-completeness-research.md`）。

## 不要做什么

- 不要在主对话直接 webSearch/webReader（会撑爆上下文）
- 不要只搜 1-2 条就下结论，每个角度至少搜 3 组不同关键词
- 不要把调研结果写成散文，必须是结构化的表格/JSON
- 不要在此对话中实施框架改动——调研完后写方案，另开对话实施
