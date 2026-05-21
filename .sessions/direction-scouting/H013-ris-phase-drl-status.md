# Handoff: RIS Phase DRL 项目状态

> 来源: S003 | 交接目标: 评估 ris-phase-drl 是否可复活，或转向相关方向
> 文件名: H013-ris-phase-drl-status.md

## 已完成边界

**项目已归档**（D022）。完整走过的阶段：GW Step 1-7 → Contract → Execute Step 1-2 → 归档。

### 核心结论：不可行

CCAN+TD3 四轮验证 + CCAN+SAC 两轮验证，**avg 全部停在 Fixed(θ=π) 水平**（<1.5% 改善），确认 off-policy RL 在 Rician LoS 主导场景下无法学到信道自适应策略。

### 走过的完整路径

```
GW Step 1-3: 8 篇精读，空白确认（最直接竞品已撤稿）
GW Step 4a: 五维度 Go（MVE 三轮迭代才通过）
GW Step 5: Baseline 选定（DDPG+SAC+PSO+Random+Fixed）
GW Step 6: 仿真器设计（多步块衰落 + 直连阻断 + ZF 预编码）
GW Step 7: Baseline 训练 — MLP DRL ≈ Fixed，但 PSO > Fixed +20%
Contract: CCAN+TD3，核心假设 avg ≥ 1.10× MLP-TD3
Execute Round 1: CCAN+TD3 early stop → avg=1301（Fixed 水平）
Execute Round 2: CCAN+TD3 no early stop → avg=1275-1315 震荡（Fixed 水平）
Execute Round 3: CCANCritic + TD3 → 与 Round 1 完全相同
Execute Round 4: CCAN+SAC → avg=1273（-1.5% vs Fixed）
归档
```

### 关键数据

| 方法 | avg sum rate | vs Fixed(1292) | best |
|------|-------------|----------------|------|
| Fixed(θ=0) | 0 | -100% | 0 |
| Fixed(θ=π) | 1292 | baseline | — |
| Random | ~12 | -99% | — |
| PSO | 1554 | +20.2% | — |
| MLP-TD3 | 1281 | -0.9% | — |
| MLP-SAC | 1273 | -1.5% | — |
| MLP-DDPG | 1284 | -0.6% | — |
| **CCAN+TD3 (early stop)** | **1301** | **+0.7%** | **1576** |
| **CCAN+TD3 (no early stop)** | **~1290** | **~0%** | **1670** |
| **CCAN+SAC** | **1273** | **-1.5%** | **1610** |

**关键信号**：CCAN best=1670 远超 PSO=1554，说明架构容量足够。但 RL 训练无法稳定输出好策略——Critic 瓶颈假设也被推翻（CCANCritic 结果相同）。

## 不要做什么

### 已排除的修复方向

1. **换 Critic 架构** — 已尝试 CCANCritic，结果完全相同。问题不在 Critic。
2. **换 off-policy 算法** — TD3 和 SAC 都试了，同样的 Fixed 吸引子。
3. **调超参** — 四轮用了不同配置（early stop / no early stop / 不同 critic），改善 <1%。
4. **加熵正则化** — SAC 的熵正则化没有帮助逃离 Fixed 吸引子。

### 根本原因分析

问题不是算法或架构，而是**问题本身的物理特性**：

1. **Rician LoS 主导 (κ=10dB)**：信道能量 90%+ 集中在 LoS 分量。最优相移接近 Fixed(θ=π)（抵消 LoS 相位），NLoS 分量提供的自适应空间极小。
2. **Fixed 是强吸引子**：任何接近 Fixed 的策略都获得高 reward，RL 探索噪声 0.1 std 偶然发现好策略（best=1670）但频率极低。
3. **Replay buffer 稀释**：好策略样本被大量 Fixed 水平样本稀释，Actor update 取 mean Q 信号太弱。

### 如果想复活，唯一可能的方向

1. **换信道模型**：去掉 Rician LoS 主导，用 Rayleigh 或低 κ。但这改变了论文定位（"大规模 RIS"场景下 LoS 是常态）。
2. **换场景为卫星-RIS**：卫星地面链路有更强的多径和动态性，可能打破 Fixed 吸引子。但这需要重新设计整个仿真器。
3. **用 on-policy RL (PPO)**：没有 off-policy 的 replay buffer 稀释问题。但 PPO 样本效率低，100 维连续动作空间可能不收敛。
4. **改问题定义**：不优化 sum rate，优化 fairness 或边缘用户 rate。这些目标下 Fixed 可能不是好的基准策略。

**但说实话，复活概率不高。** 根本原因是 100 维连续相移空间 + LoS 主导 = 最优策略接近 Fixed，这是物理特性决定的。

## 如果要转向卫星-RIS 方向

之前在 S003 讨论中提到过：把 ris-phase-drl 的方法（TD3/SAC 处理高维连续动作）迁移到卫星场景。

**优势**：
- 方法已验证（CCAN 架构容量足够，best=1670）
- 卫星地面链路有多径、多普勒、阴影效应，信道动态性更强
- "RIS 辅助 LEO 卫星通信"是卫星通信子方向

**风险**：
- 如果卫星信道也有 LoS 主导（大概率），同样的问题会复现
- 需要重新搭仿真器（卫星信道模型 vs 地面 Rician 模型）
- 需要重新做 GW 的文献检索

**建议**：如果想走这个方向，先做快速 MVE——用卫星信道模型（如 3GPP TR 38.811）跑 100ep，看 TD3 是否能 > Fixed。如果不能，说明问题不在场景而在方法。

## 必读

1. `projects/ris-phase-drl/decision_log.md` — D001-D022 完整决策链
2. `projects/ris-phase-drl/contract.md` — Contract 冻结内容（CCAN+TD3 方案）
3. `projects/ris-phase-drl/baseline_report.md` — Baseline 训练结果
4. `projects/ris-phase-drl/data-flow.md` — 数据流设计
5. `projects/ris-phase-drl/simulator-design.md` — 仿真器设计规格
6. `projects/ris-phase-drl/experiment_completeness_checklist.md` — 实验完备性检查

## 下一轮

### 选项 A：确认归档，投入其他方向

- 更新 projects-overview.md 标记归档
- 全力投入 EOS 任务调度或其他方向

### 选项 B：尝试卫星-RIS 变体

1. 先做快速 MVE：卫星信道模型 + TD3，看 avg 是否能稳定超过 Fixed
2. 如果 MVE 通过 → 修改仿真器，重新走 Contract
3. 如果 MVE 不通过 → 确认归档

### 选项 C：完全转向

- 不碰 RIS，用这个对话做方向搜索或其他项目
- 参见 H012-satellite-direction-search.md
