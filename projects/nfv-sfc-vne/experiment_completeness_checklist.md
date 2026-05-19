### 实验完备性自检清单

> Contract Step 5 产出 | 2026-05-19

#### Tier 1: 必做（门控条件）

| # | 维度 | 要求 | 状态 | 说明 |
|---|------|------|------|------|
| T1-1 | 多 seed + error bar | ≥3 seeds, mean±std | ✅ pass | 3 seeds (0,1,2)，报告 mean±std |
| T1-2 | Baseline 来源声明 | 每个 baseline 标注实现来源 | ✅ pass | B1-B5 全部 Virne 内置，来源已在 contract.md Baselines 节声明 |
| T1-3 | Baseline 公平调参 | 声明调参预算/方式 | ✅ pass | 所有 DRL solver 共享 Virne learning.yaml 默认超参，不单独调参。声明于 contract.md Fairness Rules #2 |
| T1-4 | 逐模块消融 | 逐一移除/替换，非参数扫描 | ✅ pass | A1(w/o SFC PE), A2(w/o Cross-Attn), A3(w/o Edge Attr)，使用零化/替换，非参数扫描 |
| T1-5 | 信道模型溯源 | 参数引用标准 | ☐ NA | VNE 非无线通信，不涉及信道模型。替换检查: 拓扑参数溯源 → [来源: L01 §Exp]，已声明 |
| T1-6 | 声称 scope 控制 | bounded 限定词 | ✅ pass | C1-C4 全部 bounded（4种拓扑、3 seeds、WX100），无 universal 声称 |

**Tier 1 结果**: 5 pass + 1 NA → **通过**

#### Tier 2: 应做

| # | 维度 | 要求 | 状态 | 说明 |
|---|------|------|------|------|
| T2-1 | 统计显著性检验 | 配对 t / Wilcoxon, 报告 p | ✅ pass | 3 seeds 配对 t-test，报告 p-value |
| T2-2 | Alt-explanation 排除 | 排除至少 1 个替代解释 | ✅ pass | 消融排除"仅靠模型容量提升"的替代解释（A1-A3 各组件贡献不同） |
| T2-3 | 声称-证据审计 | 每个 claim 有对应实验 | ✅ pass | C1→E1+E2, C2→E3, C3→E2, C4→E4，已映射于 contract.md 声称-证据映射 |
| T2-4 | 跨拓扑验证 | ≥2 种拓扑配置 | ✅ pass | 4 种拓扑: WX100 + GEANT + BRAIN + WX500 |
| T2-5 | 复杂度报告 | 推理延迟或理论 O() | ✅ pass | E5: 参数量 + 推理延迟对比 |

**Tier 2 结果**: 5 pass → **通过**

#### Tier 3: 加分

| # | 维度 | 要求 | 状态 | 说明 |
|---|------|------|------|------|
| T3-1 | Red-teaming | 自找漏洞并讨论 | ✅ plan | E6: SFC ratio 灵敏度分析（0.3/0.6/0.9），讨论方法在不同 SFC 密度下的行为 |
| T3-2 | 真实数据验证 | 与实测/公开数据对比 | ✅ pass | GEANT/BRAIN 为真实网络拓扑，非纯随机图 |
| T3-3 | 因果分析 | causal probing / 机制分析 | ✅ pass | 消融实验 A1-A3 提供组件级因果分析 |
| T3-4 | 最优解对比 | DP/理论下界 | ☐ NA | VNE 是 NP-hard，大规模无精确解。小规模(≤15节点)可做 ILP 对比但 Virne 不内置 |
| T3-5 | 极端条件测试 | 边界场景 stress test | ☐ plan | 可测试高 SFC ratio (0.9) + 大 VNR (size≥8) 的极端场景 |

---

## 压力测试 5 问

### Q1: 结构性优势

MatchingGAT vs GRC（最简 baseline）的结构性优势:

1. **VNE 本质是图匹配问题**: 节点映射需要同时考虑 VNR 和 substrate 的拓扑结构。GRC 仅按 substrate 节点 capacity 排序（纯局部特征），无法考虑 VNR-Substrate 的结构匹配关系。MatchingGAT 的跨图注意力直接编码 "哪个 substrate 节点最匹配当前 VNR 节点"。
2. **SFC 依赖链约束**: GRC 不感知 SFC 结构，仅通过 action masking 被动遵守。MatchingGAT 通过 VNF type + chain position embedding 主动利用 SFC 信息。
3. **全局协调**: GNN 通过消息传递聚合邻域信息，实现全局资源感知。GRC 是纯贪心，无法考虑已映射节点对后续映射的影响。

**不是简单"DL 替代传统方法"**: DL（GNN+attention）的图结构建模能力直接匹配 VNE 的图匹配本质。

### Q2: 边际结果

若 R2C 改善仅 3-5%（边际区间）:
- **消融深度支撑**: A1-A3 量化各组件贡献，即使整体改善边际，组件分析仍有方法论价值
- **框架贡献**: SFC-Virne 扩展 + MatchingGAT 实现为社区提供可复用工具
- **新颖性独立于性能**: SFC 依赖链 + matching-style GNN 的组合本身是首次尝试
- **失败兜底**: 若性能边际，可重新定位为"SFC 约束 VNE 的首个 matching-style GNN 框架 + 消融分析"

### Q3: 信号独立性

- Success #1 (R2C ≥5%) vs Failure #1 (R2C <3%): **不同阈值**，3-5% 为边际区（独立判断区域）
- Failure #2 (拓扑特异 <2%): **评估维度不同**（per-topology vs overall mean）
- Failure #3 (无组件贡献 >2%): **分析层面不同**（组件级 vs 方法级）

Failure signal 不是 success 的简单否定，捕获了不同的失败模式。

### Q4: Baseline 共识性

| Baseline | 使用论文数 | 代码状态 | 共识性 |
|----------|-----------|---------|--------|
| B1 GRC | 4篇 (L01,L02,L04,L09) | Virne内置 | ✅ 领域共识 |
| B2 PPO-DualGAT+ | 1篇 (L01) 但为 benchmark SOTA | Virne内置 | ✅ Virne 基准最优 |
| B3 PG-MLP | 1篇 (L01) 但为标准消融 | Virne内置 | ✅ GNN vs MLP 标配 |
| B4 CONAL | 1篇 (L12) | Virne内置 | ⚠️ 单篇方法，但代表约束感知 VNE 方向。标记 P1 |
| B5 PPO-DualGCN | 1篇 (L01) | Virne内置 | ✅ 架构变体消融 |

B1-B3 共识性强。B4 需额外论证（已通过 "约束感知 VNE 代表" 定位）。B5 标准架构消融。

### Q5: 反模式排查

| # | 反模式 | 检查内容 | 状态 |
|---|--------|---------|------|
| 1 | 信息泄露 | 处理组和对照组状态维度相同？消融用零化非删除？ | ✅ SFC 信息不对称已显式声明(Fairness Rules #7)，消融用零化保持维度一致。Action masking 对所有 solver 相同 |
| 2 | 仿真过于简化 | 仿真器包含目标方法擅长处理的信号？流量足以差异化？ | ✅ VNR 需求 U[0,20] vs substrate U[50,100] 产生资源竞争。SFC 约束增加映射复杂度。GEANT/BRAIN 为真实拓扑 |
| 3 | 确定性+DL强行优越 | GNN 优势来源明确？低流量退化预案？ | ✅ 优势来源 = 跨图匹配注意力(VNE 是图匹配问题) + SFC 位置编码(SFC 是新增约束维度)。低竞争时所有方法表现相似是预期行为 |
| 4 | 跨实验数据不一致 | 所有实验共用同一组拓扑和流量矩阵？ | ✅ 同拓扑同 seed 生成相同 VNR 序列，所有 solver 在相同实例上评估。不同拓扑为不同实验（by design） |

**反模式排查结果**: 全部 pass，无致命风险信号。

---

## 总结

- Tier 1: 5 pass + 1 NA → **通过**
- Tier 2: 5 pass → **通过**
- 压力测试 5 问: 无致命风险
- 反模式 4 项: 全部 pass
- **Contract 可进入 Step 6 冻结**
