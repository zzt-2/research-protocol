# Handoff: Ch2 切换 Size Generalization 质量审计

> 来源: S001 | 交接目标: 对 Ch2 做全面质量审计，输出问题清单+修复建议
> 文件名: H002-ch2-handoff.md

## 已完成边界

- S003 三章审查已完成，Ch2 判定：核心 WARN(GNN+0.8%)、top-K 定位 WARN、竞品 PASS(附条件)
- 全部实验 E1-E9 + 消融 A1-A5 完成，素材包 6 文件 ~95KB 就绪
- 待决项：是否补 N=30-40 拐点数据（可跳过，Limitations 中承认）

## 不要做什么

- 不要写论文正文
- 不要跑新实验（除非审计发现必须补做且用户同意）
- 不要修改已有实验数据
- 不要在主对话做大量文件阅读——全部委托子 agent

## 必读

1. `.sessions/chapter-quality-audit/topic-index.md`（专题总控）
2. `.sessions/thesis-structure-research/S003-three-chapter-audit.md`（前置审查结论）
3. `projects/leo-ntn-handover-drl/paper_materials/`（6 文件，素材包）
4. `projects/leo-ntn-handover-drl/contract.md`（Contract v2 frozen）
5. `projects/leo-ntn-handover-drl/decision_log.md`（D001-D032）
6. `projects/leo-ntn-handover-drl/literature_notes.md`（6 篇精读）
7. `projects/leo-ntn-handover-drl/baseline_report.md`（4 个 baseline 详情）

## Ch2 核心信息摘要

### 核心声称（4条）
1. top-K 候选压缩(K=6)将 396 维动作空间降至 6，B2 阻塞率从 25%→0%，决定性改进
2. 同规模 100UE 下 GNN 优于 MLP：reward +34%，阻塞率 -58%
3. Size generalization：20UE 训练 GNN→100UE 正 reward(35,699)，MLP 崩溃(-9,710)
4. 参数效率：GNN 25,858 参数 vs B2 DDQN ~712K（25x 压缩）

### 实验清单
- ✅ E1-E3: 20/50/100 UE 基线对比
- ✅ E4-E5: Size gen 20→50 / 20→100 UE
- ✅ E6-E7: 50/100 UE cap=10 鲁棒性
- ✅ E8-E9: B2/B1 baseline
- ✅ A1-A5: 消融全部完成（top-K/GNN消息/T=2/等）

### 指标
M1 Total episode reward, M2 Mean blocking rate, M3 Total handover count, M4 Jain's fairness index

### Baseline
B1(HHS启发式)✅, B2(Dueling DDQN flat 396-action)✅, B3(PPO)✅, B4(Random)✅, C6(flat MLP+top-K)✅

### 竞品
Lee 2025(GNN切换，无DRL), Eydian 2025(二部图匹配), Chou(Dueling DDQN无GNN), Kim 2022 BGNN(二部图GNN波束赋形), ARTHF(Fan 2025, self-attention+Dueling Rainbow)

### 已知风险
1. GNN 绝对性能贡献仅 +0.8%（at 15UE），叙事需谨慎定位
2. 50UE 同规模 GNN 仍不如 MLP(+4.9%)，缺 N=30-40 拐点数据
3. top-K 贡献远超 GNN——需避免"top-K 做了 99% 工作"印象
4. 最后文献检索 2026-05-09（距今 13 天）
5. 单 seed 评估，无统计检验
6. GNN 迁移(35,699)优于 MLP 同规模训练(33,843)——杀手论点未被充分挖掘

### 独特挑战：GNN 贡献叙事
GNN 的核心价值不在绝对性能增量，而在：
- 结构泛化能力（20→100UE 正 reward vs MLP 崩溃）
- 参数效率（25x 压缩）
- 与 MLP 同规模训练对比胜出（迁移 > 同规模训练）

审计需特别验证这个叙事逻辑是否站得住，是否有更强竞品做了类似叙事。

## 审计执行计划

### Phase 1: 文献新鲜度 & 新颖性（2 个子 agent 并行）

**Agent 1A — 最新文献检索**
- 关键词组合：GNN + handover / beam selection + LEO / NTN + size generalization / scalability
- 执行：`bash tools/search` 做 4-6 组检索，时间 2026-01 至今
- 特别关注：Lee 2025 是否有更新版本或跟进工作
- 输出：新论文列表 + 重叠度判定

**Agent 1B — 已有竞品深化核查**
- 输入：读 `literature_notes.md` + `novelty_search.md`（如有）
- 任务：
  1. 验证"四要素组合无完全先例"的新颖性结论
  2. 每个竞品的技术细节 vs 我们的核心声称
  3. Lee 2025 需精确技术区分论证
- 输出：竞品-差异化矩阵

### Phase 2: 实验完备性对标（2 个子 agent 并行）

**Agent 2A — 领域 Top 论文实验清单提取**
- 精读 2-3 篇：Lee 2025(ICT Express), Kim 2022 BGNN(TWC), ARTHF(Fan 2025)
- 提取维度同 H001（baseline/消融/统计/可视化/指标/泛化设计）
- 特别关注：切换论文的标准实验设计是什么？

**Agent 2B — 我们的实验覆盖度自检**
- 读 Ch2 contract.md + paper_materials/ 全部 6 文件
- 按 2A 的 checklist 逐项对比
- 特别关注：
  - 消融是否充分论证 top-K vs GNN 各自贡献？
  - Size gen 实验设计是否严格（训练集/测试集独立性）？
  - 是否需要更多 UE 数量的过渡点？

### Phase 3: 指标完整性 + 数据自洽性（2 个子 agent 并行）

**Agent 3A — 指标完整性**
- 切换领域标准指标：阻塞率、掉话率、切换次数、ping-pong率、吞吐量、公平性、时延
- 我们报了哪些？缺哪些？能补吗？

**Agent 3B — 数据自洽性验证**
- 重点检查：
  1. 15UE vs 20UE 的 GNN 增量数字(+0.8% vs +0.3%)是否在论文中标注对应 UE 数
  2. 消融编号 A1-A5 以 contract.md 方案 C 为准，与 execution_report 方案 A 是否混淆
  3. E4-50 首次运行失败(reward -4857)是否已被最终结果覆盖
  4. paper_materials/01_research_context.md 第8节 10 项待补充标记

### Phase 4: 汇总与输出

同 H001 Phase 4 格式，审计报告写入 `.sessions/chapter-quality-audit/S003-ch2-audit.md`。

额外输出：**GNN 贡献叙事论证方案**——如何在论文中定位 GNN 贡献而不被 top-K 掩盖。

## 接口变更

无

## 失败数据附录

无

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| N=30-40 拐点 | 实验完备性 | 未做 | 审计判定 CRITICAL 则补做（~2h GPU）|
| 单 seed 评估 | 统计严谨性 | 所有实验 | 审计判定需要则补跑 |
| sat_capacity 调整 | 公平性 | 已在 decision_log 记录 | 论文正文需说明 |
| 消融编号混淆 | 数据一致性 | 方案 A/C 共存 | 论文统一为方案 C 编号 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 |
|--------|----------|---------|
| 新颖性 | 四要素组合无完全先例仍成立 | Contract S0 |
| 实验覆盖 | 切换领域 top 论文实验维度 80%+ | Contract S5 |
| 指标完整 | 切换领域标准指标 90%+ 报告 | domain-comms.md |
| 数据自洽 | 0 矛盾 | 框架通用要求 |
| GNN 叙事 | 贡献定位不被 top-K 掩盖 | S003 审查建议 |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证 S003 中 Ch2 的审查结论（核心 WARN、竞品 PASS 附条件）
- [ ] 已确认消融编号以 contract.md 方案 C 为准
- [ ] 已检查必读文件中至少 3 个存在且可读

## 下一轮

1. 新对话读取本交接文档 + topic-index
2. 按 Phase 1→2→3→4 顺序执行
3. 审计报告写入 S003，问题清单更新到本交接文档
4. 完成后更新 topic-index 进展线索
