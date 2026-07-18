# [S001] Ch2 LEO 切换 DRL 竞品 + 方法论终审

> 2026-05-25 | Phase 1 对话1 | 完成
> 2026-05-25 续接: 1a-1d 全部完成

## 目标

确认 Ch2 (LEO NTN Handover DRL) 无未引竞品，实验设计符合子领域通行标准。

## 记录

### 已知竞品（已有 literature_notes / novelty_search 记录）

| 论文 | 要素覆盖 | 威胁等级 |
|------|---------|---------|
| Lee & Lim 2025 (ICT Express) | GNN + 二部图 + LEO 切换 | 低-中（最直接竞争者） |
| Chou 2026 (arXiv:2605.02416) | Dueling DDQN + 多目标切换 | 低-中 |
| ARTHF / Fan 2025 (MDPI) | Self-attention + Rainbow + 负载 | 中 |
| Eydian 2025 (OJCOMS) | 加权二部图匹配 + 切换 | 低 |
| Kim 2022 (TWC, BGNN) | 二部图 GNN + 波束赋形 | 低-中 |
| L018 / JSAC 2024 | EMODRL 多目标切换 | 已引 |
| L016 / TMC 2025 | Transformer + D3QN + AoI | 已引 |
| L004 / arXiv 2026 | 自适应奖励 + 切换困境 | 已引 |
| L029 / arXiv 2026 | Dueling DDQN 切换 | 已引 |

### 本轮检索结果

#### 1a: LEO handover DRL 竞品检索

- 6 轮检索，~210 条结果，去重 ~180 篇
- **6 篇新候选**（均低-中威胁）：

| 论文 | 重叠要素 | 威胁 | 备注 |
|------|---------|------|------|
| Graph RL-Based Handover Strategy (2024) | Graph RL + Handover | 低-中 | 非二部图GNN，无size gen |
| Multi-Layer Graph-Based ISL Group Handover (2025) | Graph + Handover | 低 | 无DRL，组切换 |
| Message Passing-Based Assignment for Handover (2025) | Message passing + Handover | 低-中 | 偏传统优化 |
| Two-Stage GNN-Based Scalable Access (2025) | GNN + scalable | 低-中 | 接入选择非切换 |
| QoS-aware Handover Multi-agent DRL (Liang 2024, APCC) | Multi-agent DRL + Handover | 低 | 无GNN/二部图 |
| PER-DDQN Load Balancing Handover (2025) | DDQN + Handover | 低 | 纯DRL |

- **核心确认：无任何论文同时使用 GNN + DRL 做卫星切换**

#### 1b: 二部图 DRL 先例检索

- 4 轮检索，~120 条结果
- **关键发现：二部图 + DRL 在无线资源分配中已有先例**

| 论文 | 二部图建模 | RL 算法 | 场景 | 与 Ch2 关系 |
|------|-----------|---------|------|------------|
| **Xie 2023** (IEEE WCSP) | 用户-HAP 在线二部匹配 | RL + GNN编码器 + 多头注意力 | HAP 接入控制 | **最接近先例**：二部图+GNN+RL |
| **Yin 2022** (Mobile Info Systems) | 卫星-BS 二部图 | DDQN (PSDDQN) | 卫星-地面站关联 | 先例：二部图+DDQN 卫星场景 |
| Yu & Tang 2024 | CU-DU 加权二部图 | DRL + KM | D2D 链路匹配 | 部分先例 |
| Jamshidiha 2025 | 二部 K-NN 干扰图 | DRL + STGNN | 功率分配 | 部分先例 |

- **新颖性需限定范围**：二部图+RL 不新颖（Xie 2023, Yin 2022），但 UE-卫星二部图+GNN消息传递+Dueling DDQN 用于 LEO 切换仍无先例

#### 1c: 方法论 checklist

精读 L029, L018, L004, Lee & Lim 2025, ARTHF 五篇论文：

| 维度 | 通行标准 | Ch2 做法 | 合规 |
|------|---------|---------|------|
| Seed 数 | 1-10不等，多数未报告 | 3 seeds (100,200,300) | ✓（下限，L004同等） |
| 统计报告 | 均值必须，std加分 | mean ± std | ✓（超越多数） |
| 统计检验 | 零论文做 | 无 | ✓（符合） |
| 主要指标 | 吞吐量+阻塞率+切换频率 三指标 | 吞吐量+阻塞率+切换次数+公平性 | ✓（超越） |
| Baseline 数 | 3-8个 | 3传统+DRL对比 | ✓ |
| Baseline 公平性 | 同环境同参数 | 同环境同参数 | ✓ |
| 消融实验 | 0-2组（非强制） | 5组(A1-A5) | ✓（超越） |
| 评估方式 | 训练后固定策略 | 训练后固定策略 | ✓ |

#### 1d: 综合合规报告

**竞品覆盖结论**：
- Ch2 竞品覆盖**基本完整**
- 新发现 6 篇论文威胁等级均为低-中，建议在 related work 提及 1-2 篇（Two-Stage GNN-Based Scalable Access、Graph RL-Based Handover Strategy）
- **核心新颖性未被推翻**：GNN + DRL + 卫星切换 仍无先例

**新颖性范围修正**：
- ~~"首次将二部图与 DRL 结合"~~ → 应改为"本研究将 UE-卫星二部图 GNN 与 Dueling DDQN 结合用于 LEO 切换决策"
- 必须引用 Xie 2023 和 Yin 2022 作为二部图+RL 在相近场景中的先例
- Kim 2022 BGNN 也应引用（二部图 GNN + 跨规模可扩展，非 RL 但技术路线相近）

**方法论合规结论**：
- Ch2 实验方法论**符合或超越**子领域通行标准
- 主要风险不在方法论合规性，在 GNN 增量贡献论证策略
- 结合 S003 结论：应补充 bootstrap 95% CI + Welch's t-test（零计算成本）

**风险矩阵**：

| 风险 | 等级 | 建议 |
|------|------|------|
| GNN 小规模增量小(+0.8%) | 中 | 侧重 size gen (A5) 作为决定性优势 |
| 3 seeds 为下限 | 低 | 引用 L004 同等做法 + 补 CI |
| 无 L029 方法作为 baseline | 中 | 讨论 Ch2 vs L029 方法论差异 |
| 二部图+RL 先例需引用 | 低 | 引 Xie 2023 + Yin 2022 |

## 决策引用

- 无新决策（本轮为确认性检索，未改变方向）

## 范围确认

- 本轮在 scope boundary 内：是（Phase 1 对话1）

## 后续

- 将合规报告要点更新到 topic-index 不变量/结论段
- 对话 5 需执行：Ch2 数据溯源 + 旧数据清除 + 统计补充(CI/t-test)
- Ch2 paper-materials 新颖性措辞修正（引用 Xie 2023 + Yin 2022）
