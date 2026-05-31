---
created: 2026-05-19
status: frozen
version: 1
---

# Research Contract

## Hypothesis

In SFC-constrained VNE scenarios (sfc_ratio=0.6) on medium-to-large substrate networks (≥50 nodes), matching-style cross-graph attention combined with SFC dependency chain position encoding and explicit edge feature encoding improves R2C by ≥5% over PPO-DualGAT+ (the strongest GNN baseline), with the advantage robust across ≥3 medium-to-large substrate topologies and ≥3 random seeds.

**Scope 限定**: 假设范围限定为 ≥50 节点网络。GEANT (23节点) 作为小规模补充验证，不纳入门控。依据: B3 失败模式 — 小规模场景复杂组件退化（ntn-handover: 15 UE 时 GNN 仅 +0.8%）。

**GW 初步证据**: MatchingGAT 30ep (R2C=0.790) vs DualGAT+ 30ep (R2C=0.756), 单 seed 提升 +4.5%。消融确认三组件各有贡献。

## Success Signal

1. **R2C 主指标**: Mean R2C improvement ≥5% over PPO-DualGAT+ across medium-to-large topologies (WX100, BRAIN, WX500, ≥3 seeds each)
2. **AC 辅助指标**: Mean AC ≥0.95 across all topologies
3. **消融完备性**: Each of the three core components (cross-graph attention, SFC PE, edge features) contributes ≥1.5% R2C in ablation (30ep, ≥3 seeds)

## Failure Signal

1. **边际改进**: Mean R2C improvement <3% over PPO-DualGAT+ across topologies — 核心方法无法提供有意义提升
2. **拓扑特异**: R2C improvement <2% over PPO-DualGAT+ on any medium-to-large topology (BRAIN/WX500) — 优势依赖特定拓扑结构
3. **组件无贡献**: No single ablation component contributes >2% R2C — 方法创新无实证支撑

注: 3-5% R2C 改善区间为"边际"区域，需通过收敛速度、消融深度、SFC 信息价值等辅助证据补充论证。

注: GEANT (23节点) 作为小规模补充验证，**不纳入 success/failure signal 门控**。GEANT 结果单独报告，预期优势可能缩小（B3: 小规模场景 GNN 消息传递范围有限）。若 GEANT 上 DualGAT+ ≈ MatchingGAT，视为"方法在中大规模网络上的优势不适用于极小网络"，非假设失败。

## Baselines

- B1: **GRC Rank** (来源: Gong 2014, Virne内置 `grc_rank`) — 复现状态: ✅ 已复现(GW Step 7, R2C=0.543, AC=0.836) — 交叉验证: 被 L01/L02/L04/L09 共4篇使用, 领域共识启发式
- B2: **PPO-DualGAT+** (来源: Virne L01, `ppo_dual_gat+`) — 复现状态: ✅ 已复现(GW Step 7, 30ep, R2C=0.756, AC=0.912) — 交叉验证: Virne基准最优架构, WX100 RAC=78.1%
- B3: **PG-MLP** (来源: Virne L01, `pg_mlp`) — 复现状态: ✅ 已复现(GW Step 7, 30ep, R2C=0.599, AC=0.908) — 交叉验证: GNN vs MLP消融标配
- B4: **CONAL** (来源: L12, Virne内置 `conal`) — 复现状态: 待复现 — 交叉验证: 约束感知VNE代表(CMDP for VNE) — 优先级 P1
- B5: **PPO-DualGCN** (来源: Virne L01, `ppo_dual_gcn`) — 复现状态: 待复现 — 交叉验证: GNN架构变体(GCN vs GAT) — 优先级 P2

注: B1-B3 为 P0 必做。B4/B5 优先级较低，若训练时间紧张可仅保留 B1-B3。

## Metrics

- M1: **R2C** (Revenue-to-Cost Ratio) — 成功嵌入VNR总收益/总成本 — 越高越好 [主指标]
- M2: **AC** (Acceptance Rate) — 成功嵌入VNR数/总VNR数 — 越高越好
- M3: **收敛速度** — 达到最终R2C 95%所需epoch数 — 越小越好

## Fairness Rules

1. **环境一致**: 所有 solver 使用相同 Virne 仿真环境、相同 VNR 生成种子序列、相同奖励函数 (fixed_intermediate, intermediate=0.1)
2. **训练一致**: 所有 DRL solver 使用 PPO，共享 Virne learning.yaml 超参数（lr=0.001, gamma=0.99, eps_clip=0.2, gae_lambda=0.98, entropy_coef=0.01），仅架构不同
3. **预算一致**: 所有 DRL solver 训练相同 epoch 数（30ep），使用相同 500 VNRs/epoch
4. **评估一致**: 相同评估集（Virne built-in eval）
5. **消融规范**: 消融使用零化（非删除），保持输入维度一致
6. **约束一致**: SFC 约束由环境通过 action masking 强制执行，所有 solver 面对相同约束
7. **SFC 信息不对称声明** [显式声明]: MatchingGAT 额外编码 VNF 类型 + SFC 链位置信息，其他 baseline 不接收 SFC 特征输入。这是核心方法贡献（主动利用 SFC 结构做更优决策），非信息泄露。消融 A1 量化此信息增量。

## Ablation Plan

| 编号 | 消融目标 | 预期影响方向 | 预期影响大小 | 实现方式 |
|------|---------|-------------|-------------|---------|
| A1 | w/o SFC PE | R2C 下降 | 小 (GW 10ep: -1.8%) | 零化 VNF type + chain position embeddings |
| A2 | w/o Cross-Attn | R2C 下降 | 中 (GW 10ep: -2.2%) | 替换为简单 addition (p_emb + v_emb) |
| A3 | w/o Edge Attr | R2C 下降 | 大 (GW 10ep: -4.4%) | 零化 edge attributes (bw, delay) |

GW 初步结果排序: 边特征 > 跨图注意力 > SFC 位置编码。Execute 阶段需用 30ep + ≥3 seeds 严格验证。注意 GW 消融仅 10ep vs Full 30ep，可能低估组件贡献。

## Experiment List

| 编号 | 实验名 | 类型 | 优先级 | 描述 |
|------|--------|------|--------|------|
| E1 | 主对比实验 | 核心 | P0 | MatchingGAT vs B1-B5, WX100, 30ep, 3 seeds |
| E2 | 跨拓扑泛化 | 对比 | P0 | MatchingGAT vs B1-B3, BRAIN/WX500 (主) + GEANT (补充), 30ep, 3 seeds |
| E3 | 消融实验 | 消融 | P0 | A1-A3, WX100, 30ep, 3 seeds |
| E4 | 收敛分析 | 对比 | P1 | 训练曲线, MatchingGAT vs DualGAT+ vs MLP, 单 seed |
| E5 | 推理复杂度 | 对比 | P2 | 参数量 + 推理延迟对比 |
| E6 | SFC ratio 灵敏度 | 鲁棒 | P3 | sfc_ratio ∈ {0.3, 0.6, 0.9}, MatchingGAT vs DualGAT+, WX100, 单 seed, 30ep |

## 已知风险与缓解

| 风险 | 严重度 | 缓解措施 | 状态 |
|------|--------|---------|------|
| **R1: GEANT 小规模退化** — 23 节点 GNN 消息传递范围不足，cross-attn 优势可能消失 | 高 | 假设 scope 限定 ≥50 节点，GEANT 不纳入门控；Execute 开头跑 GEANT 5ep 快速验证确认趋势 | 已在假设/signal/claim 中反映 |
| **R2: 消融 30ep vs 10ep 差异** — GW 消融仅 10ep，30ep 结果可能变化 | 中 | E3 严格 30ep 同条件消融；若差异大则记录并分析原因 | E3 已锁定 |
| **R3: 单训练拓扑泛化** — 仅 WX100 训练，BRAIN/WX500 推理性能未知 | 中 | Virne L01 已验证跨拓扑可行；E2 显式验证 | E2 已锁定 |
| **R4: SFC ratio 敏感性** — sfc_ratio=0.6 下有效，其他值未知 | 低 | E6 灵敏度实验作为 Tier 3 red-teaming | E6 已加入 |
| **R5: CONAL baseline 竞争力** — B4 单篇方法，可能意外强势 | 低 | 标记 P1 优先级；若 CONAL 强则调整叙事为"matching vs constraint-aware 两种路径" | B4 优先级 P1 |

## Simulation Config

### 网络拓扑

| 参数 | 值 | 来源 |
|------|-----|------|
| 主拓扑 | Waxman(100, α=0.5, β=0.2) | [来源: L01 §Exp] |
| 泛化拓扑-1 | GEANT (23节点, 真实拓扑) | [来源: L01 §Exp] |
| 泛化拓扑-2 | BRAIN (161节点, 真实拓扑) | [来源: L01 §Exp] |
| 泛化拓扑-3 | WX500 (500节点, Waxman) | [来源: L01 §Exp] |
| Substrate node CPU | U[50,100] | [来源: L01 §Exp] |
| Substrate link BW | U[50,100] | [来源: L01 §Exp] |

### VNR 生成

| 参数 | 值 | 来源 |
|------|-----|------|
| VNR 规模 | U[2,10] 节点 | [来源: L01 §Exp] |
| 连接概率 | p=0.5 (Erdos-Renyi) | [来源: L01 §Exp] |
| VNR node CPU demand | U[0,20] | [来源: L01 §Exp] |
| VNR link BW demand | U[0,50] | [来源: L01 §Exp] |
| VNR/epoch | 500 | [来源: L01 §Exp] |

### SFC 约束

| 参数 | 值 | 来源 |
|------|-----|------|
| SFC ratio | 0.6 | [设计选择: 中等密度, 确保足够SFC约束样本] |
| VNF type 数量 | 5 | [设计选择: 适度的VNF功能多样性] |
| SFC 拓扑模型 | random graph + SFC 叠加层 | [设计选择: 保持VNE拓扑复杂度, D013] |

### 训练配置

| 参数 | 值 | 来源 |
|------|-----|------|
| 算法 | PPO | [来源: L01, PPO效率最优] |
| Training epochs | 30 | [设计选择: GW验证30ep充分收敛] |
| Learning rate (actor/critic) | 0.001 | [来源: L01 Virne learning.yaml] |
| Gamma | 0.99 | [来源: L01 Virne learning.yaml] |
| GAE lambda | 0.98 | [来源: L01 Virne learning.yaml] |
| Clip ratio | 0.2 | [来源: L01 Virne learning.yaml] |
| Entropy coef | 0.01 | [来源: L01 Virne learning.yaml] |
| Critic loss coef | 0.5 | [来源: L01 Virne learning.yaml] |
| Batch size | 128 | [来源: L01 Virne learning.yaml] |
| Target steps | 256 | [来源: L01 Virne learning.yaml] |
| Repeat times | 10 | [来源: L01 Virne learning.yaml] |
| Max grad norm | 0.5 | [来源: L01 Virne learning.yaml] |
| Embedding dim | 128 | [来源: L01 Virne learning.yaml] |
| Hidden dim | 128 | [来源: L01 Virne learning.yaml] |
| GNN layers | 3 | [来源: L01 Virne learning.yaml] |

### 奖励函数

| 参数 | 值 | 来源 |
|------|-----|------|
| 类型 | fixed_intermediate | [来源: L01, fixed=0.1效果最好, D014] |
| 成功奖励 | R2C(episode) | [来源: L01] |
| 中间步骤奖励 | 0.1 | [来源: L01 §Exp] |
| 失败惩罚 | -0.1 | [来源: L01 §Exp] |

### 评估协议

| 参数 | 值 | 来源 |
|------|-----|------|
| Random seeds | 3 (0, 1, 2) | [设计选择: ≥3种子统计可靠性] |
| 评估方式 | Virne built-in eval | [来源: L01] |
| 硬件 | NVIDIA RTX 4070 Laptop GPU | [设计选择] |

## 数据集设计

### 参数空间

本项目使用 Virne 仿真器在线生成 VNR 实例，不使用静态数据集。

| 参数 | 取值范围 | 文献溯源 | 备注 |
|------|---------|---------|------|
| Substrate 规模 | 23-500 节点 | [来源: L01 §Exp] | 4种拓扑 |
| VNR 规模 | 2-10 节点 | [来源: L01 §Exp] | U[2,10] |
| VNR 连接概率 | 0.5 | [来源: L01 §Exp] | Erdos-Renyi |
| SFC ratio | 0.6 | [设计选择] | 主实验 |
| VNF type 数 | 5 | [设计选择] | |

### 数据规模与划分

- 训练: 30 epochs × 500 VNRs/epoch = 15000 VNRs（在线生成，种子控制可复现）
- 评估: Virne built-in evaluation（训练后固定评估集）
- 无静态划分（在线生成 + 种子控制保证可复现性）

## Parameter Provenance

> Step 3 验证完成 (2026-05-19)。所有参数已溯源，无 [ASSUMPTION] 标记。

| 参数 | 值 | 来源 |
|------|-----|------|
| Substrate node CPU | U[50,100] | [来源: L01 §Exp] Virne 默认 |
| Substrate link BW | U[50,100] | [来源: L01 §Exp] Virne 默认 |
| VNR node CPU | U[0,20] | [来源: L01 §Exp] Virne 默认 |
| VNR link BW | U[0,50] | [来源: L01 §Exp] Virne 默认 |
| VNR size | U[2,10] | [来源: L01 §Exp] Virne 默认 |
| VNR p | 0.5 | [来源: L01 §Exp] Virne 默认 |
| sfc_ratio | 0.6 | [设计选择: 0.6 确保平均 VNR 含 ~3.6 个 SFC VNF，约束有意义但不压倒 VNE 复杂度。0.3 过弱(SFC 无显著差异)，1.0 退化为纯链(GNN 优势消失，B3 模式)] |
| num_vnf_types | 5 | [设计选择: ETSI NFV 常见 VNF 类型 5-10 种，取下限中值，足够区分 VNF 功能差异又不引入过多噪声] |
| Training epochs | 30 | [设计选择: GW 验证 DualGAT+ epoch10 收敛(R2C 0.74 平台期)，MatchingGAT epoch5 收敛(R2C 0.777)，30ep 提供 3-6x 余量。Virne 默认 50ep，30ep 为训练时间(~2h/seed)与收敛保证的平衡] |
| PPO lr | 0.001 | [来源: L01 Virne learning.yaml] |
| PPO gamma | 0.99 | [来源: L01 Virne learning.yaml] |
| PPO eps_clip | 0.2 | [来源: L01 Virne learning.yaml] |
| PPO gae_lambda | 0.98 | [来源: L01 Virne learning.yaml] |
| Embedding dim | 128 | [来源: L01 Virne learning.yaml] |
| GNN layers | 3 | [来源: L01 Virne learning.yaml] |
| Seeds | 3 (0,1,2) | [设计选择: DRL 文献统计报告最低要求，3 seeds 可报告 mean±std] |
| VNRs/epoch | 500 | [来源: L01 §Exp] Virne 默认 |

## 声称-证据映射

| Claim | Type | Planned Experiment | Expected Evidence |
|-------|------|-------------------|-------------------|
| C1: MatchingGAT R2C ≥5% 优于 PPO-DualGAT+ | bounded (中大规模拓扑: WX100/BRAIN/WX500, 3 seeds) | E1 主对比 + E2 跨拓扑 | Table 1: WX100性能对比, Table 2: 跨拓扑对比 |
| C2: 三组件各贡献 ≥1.5% R2C | bounded (WX100, 30ep, 3 seeds) | E3 消融 | Table 3: 消融实验表 |
| C3: 优势跨中大规模拓扑鲁棒 | bounded (WX100/BRAIN/WX500) | E2 跨拓扑泛化 | Table 2: 3种中大规模拓扑R2C/AC对比 |
| C4: 收敛更快 | bounded (WX100) | E4 收敛分析 | Fig: 训练曲线对比 |
