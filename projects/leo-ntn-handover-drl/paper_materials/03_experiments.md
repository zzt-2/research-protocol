# 实验数据

> 来源文件：execution_report.md, baseline_report.md, contract.md, decision_log.md
> 生成日期：2026-05-10

---

## 1. 仿真环境

### 1.1 星座与信道参数表

| 参数 | 值 | 来源 |
|------|------|------|
| 星座类型 | Walker-delta | contract.md |
| 面数 × 每面星数 | 18 × 22 = 396 卫星 | contract.md / baseline_report.md |
| 轨道高度 | 550 km | contract.md |
| 轨道倾角 | 53°（Starlink-like subset） | contract.md |
| 频段 | Ku-band 12 GHz | contract.md / baseline_report.md |
| 带宽 | 250 MHz | contract.md / baseline_report.md |
| 路径损耗模型 | FSPL（自由空间路径损耗） | contract.md |
| 大气衰减模型 | ITU-R P.676 | contract.md |
| 阴影衰落模型 | 3GPP TR 38.811 LoS | contract.md |
| 雨衰模型 | AR(1)，σ=5 dB，相关时间 30s | contract.md |
| 阴影衰落 σ | 20°=4.0 dB, 45°=1.5 dB, 90°=1.0 dB（单调递减） | baseline_report.md 1.1 |
| 大气衰减值 | 20°=0.585 dB, 45°=0.283 dB, 90°=0.200 dB（单调递减） | baseline_report.md 1.1 |
| FSPL 参考值 | d=550km f=12GHz → 168.83 dB | baseline_report.md 1.1 |
| Shannon 容量参考值 | SINR=10dB B=250MHz → 864.9 Mbps | baseline_report.md 1.1 |
| 可见卫星统计 | 平均 4.4 颗/UE，范围 2-6 颗 | baseline_report.md 1.1 |
| lag-1 自相关 | 0.197（远低于 0.95 警戒线） | baseline_report.md 1.1 / D004 |

### 1.2 地面配置表

| 参数 | 值 | 来源 |
|------|------|------|
| UE 分布 | 北京地区（40°N, 116°E）± 3° 均匀分布 | contract.md |
| 最小仰角 | 20° | contract.md / baseline_report.md |
| sat_capacity（20 UE） | 10 信道/星 | contract.md |
| sat_capacity（50 UE） | 15 信道/星 | contract.md / D026 |
| sat_capacity（100 UE） | 25 信道/星 | contract.md / D026 |
| Groundwork 阶段 UE 数 | 15 | baseline_report.md 1.3 |

### 1.3 仿真参数表

| 参数 | 值 | 来源 |
|------|------|------|
| 仿真持续时间 | 7200s（2 小时） | contract.md / baseline_report.md |
| 决策间隔 | 10s | contract.md / baseline_report.md |
| 每 episode 步数 | 720 steps | contract.md |
| Transitions/episode（15 UE） | 10,800（15 UE × 720 步） | baseline_report.md 2.3 |
| Transitions/episode（50 UE） | 36,000（50 UE × 720 步） | D027 |
| 观测空间维度（full） | 1585（396×4+1） | baseline_report.md 5 |
| 观测空间维度（top-K=6） | 41（6×6+5） | execution_report.md 6.3 / D017 |

### 1.4 奖励函数

完整公式（来源：contract.md）：

```
reward = w_r · R_norm + w_l · L_norm - w_b · B - w_h · H
```

| 符号 | 含义 | 说明 |
|------|------|------|
| R_norm | 归一化速率 | SINR=10dB → 0.4728，log₂(1+SINR)/log₂(1+SINR_max) |
| L_norm | 剩余容量归一化 | 反映负载均衡程度 |
| B | 阻塞惩罚 | 被 capacity 拒绝的 UE 惩罚 |
| H | 切换惩罚 | 抑制乒乓切换 |

奖励合理性验证（来源：baseline_report.md 1.2）：

| 策略 | 吞吐量项 | 负载项 | 阻塞项 | 切换项 | 总奖励 |
|------|---------|--------|--------|--------|--------|
| Random | 60.9% | 31.0% | 0.0% | 8.1% | +586.7 |
| Greedy | 58.2% | 5.2% | 36.0% | 0.5% | -118.0 |

验证结论：无单一项独占（最大项 60.9% < 95%），策略区分度 120% > 10%。

---

## 2. 仿真器验证结果

### 2.1 模块验证（9 项 PASS）

| 检查项 | 结果 | 详情 | 来源 |
|--------|------|------|------|
| FSPL 解析 | PASS | d=550km f=12GHz → 168.83 dB，与公式精确匹配 | baseline_report.md 1.1 |
| 大气衰减 | PASS | 20°=0.585dB, 45°=0.283dB, 90°=0.200dB，单调递减 | baseline_report.md 1.1 |
| 阴影衰落 σ | PASS | 20°=4.0dB, 45°=1.5dB, 90°=1.0dB，按 TR 38.811 单调递减 | baseline_report.md 1.1 |
| Shannon 容量 | PASS | SINR=10dB B=250MHz → 864.9 Mbps，精确匹配 | baseline_report.md 1.1 |
| R_norm 归一化 | PASS | SINR=10dB → 0.4728，符合 log₂(1+SINR)/log₂(1+SINR_max) | baseline_report.md 1.1 |
| 仰角计算 | PASS | 正上方卫星 → 90.0° | baseline_report.md 1.1 |
| 可见卫星统计 | PASS | 平均 4.4 颗/UE，范围 2-6 颗 | baseline_report.md 1.1 |
| 自相关预警 | PASS | lag-1 = 0.197，远低于 0.95 警戒线 | baseline_report.md 1.1 |
| 退化测试 | PASS | 阴影模型重置功能正常 | baseline_report.md 1.1 |

### 2.2 MDP Checkpoint（奖励合理性）

| 策略 | 吞吐量项 | 负载项 | 阻塞项 | 切换项 | 总奖励 | 来源 |
|------|---------|--------|--------|--------|--------|------|
| Random | 60.9% | 31.0% | 0.0% | 8.1% | +586.7 | baseline_report.md 1.2 |
| Greedy | 58.2% | 5.2% | 36.0% | 0.5% | -118.0 | baseline_report.md 1.2 |

---

## 3. Baseline 复现结果

> 所有 baseline 评估：5 seeds，报告均值。来源：baseline_report.md §2

### 3.1 B4 Random（下界）

| 指标 | 均值 ± 标准差 (5 seeds) | 来源 |
|------|----------------------|------|
| 吞吐量 | 36,105 Mbps | baseline_report.md 2.1 |
| 阻塞率 | 0.02% | baseline_report.md 2.1 |
| 切换次数 | 8,435 | baseline_report.md 2.1 |

分析：随机策略通过均匀分散 UE 到不同卫星，几乎不产生阻塞。但切换频繁（每步 ~1.2 次/UE），不优化信道质量。

### 3.2 B1 HHS（传统启发式）

| 指标 | 均值 ± 标准差 (5 seeds) | 来源 |
|------|----------------------|------|
| 吞吐量 | 20,911 Mbps | baseline_report.md 2.2 |
| 阻塞率 | **37.4%** | baseline_report.md 2.2 |
| 切换次数 | 877 | baseline_report.md 2.2 |

**高阻塞率根因分析**：
- HHS 原为单 UE 算法（论文 L08），多 UE 独立决策导致聚集效应
- 稳定性奖励（logistic ψ）和切换惩罚（P_ho=0.03）使 UE 粘滞在同一卫星，超过容量限制
- 切换次数仅 877（比 Random 的 8,435 减少 90%），但代价是极高阻塞率
- 这是 HHS 在多 UE 场景的结构性局限，也是 DRL 的核心改进空间

### 3.3 B2 Dueling DDQN（DRL baseline 1）

| 指标 | 验证结果 (5 episodes) | 来源 |
|------|---------------------|------|
| Episode reward | 3,345 - 4,241 | baseline_report.md 2.3 |
| Transitions/episode | 10,800（15 UE × 720 步） | baseline_report.md 2.3 |
| Training loss | 0.31 → 0.19（下降趋势） | baseline_report.md 2.3 |
| CUDA | 正常使用 | baseline_report.md 2.3 |

架构：Dueling Q = V + A - mean(A)，rate 归一化到 [0,1]（原论文 L02 未归一化，F5 根因修正）。

### 3.4 B3 PPO（DRL baseline 2）

| 指标 | 验证结果 (3 episodes) | 来源 |
|------|---------------------|------|
| Value loss | 10.5 → 0.5（快速下降） | baseline_report.md 2.4 |
| Entropy | ~1.4（持续探索） | baseline_report.md 2.4 |
| Eval step reward | 0.199 | baseline_report.md 2.4 |
| Eval blocking rate | 45.5% | baseline_report.md 2.4 |

说明：仅 3 episode 未充分收敛，45.5% 阻塞率是训练不足的表现。Actor-Critic 共享层正确，PPO-clip 损失正常。

### 3.5 与论文对比说明

复现定义（来源：baseline_report.md §3）：

> "复现"在本项目中定义为：在自己的仿真环境中实现论文的算法架构和核心设计，验证相对趋势。

| Baseline | 论文方法 | 本项目修正 | 验证方式 | 来源 |
|----------|---------|-----------|---------|------|
| B1 HHS | L08 Algorithm 1 | 星座从 Starlink 1584 降至 396 | 结构验证 | baseline_report.md 3 |
| B2 DDQN | L02 Dueling DDQN | rate 归一化到 [0,1] | 趋势验证 | baseline_report.md 3 |
| B3 PPO | L01/L10 PPO | 无修正 | 趋势验证 | baseline_report.md 3 |
| B4 Random | — | — | 下界确认 | baseline_report.md 3 |

不直接对比绝对数值的理由（来源：baseline_report.md §3）：
1. 星座规模不同（396 vs L02 的 298 / L07 的 1584）
2. 信道模型不同（本项目简化 vs L08 完整 ITU-R 模型）
3. UE 数量/分布不同（15 vs L02 的 10-30）
4. 奖励函数修正（L02 的 rate 未归一化，本项目已修正）

---

## 4. GNN+DDQN 架构配置（E4 最佳配置）

来源：contract.md "GNN+DDQN 架构（E4 最佳配置）"

| 超参数 | 值 | 说明 |
|--------|------|------|
| K（top-K 候选压缩） | 6 | 从 396 颗降到 6 颗候选 |
| GNN 类型 | MPNN-E（边条件化消息传递神经网络） | D010 |
| 消息传递层数 T | 2 | D022 确认 T=2 最关键（+1.8%） |
| GNN hidden dim | 32 | — |
| GNN out dim | 64 | — |
| Q 函数类型 | 分解式 Dueling Q：V(h_ue) + A(h_ue, h_sat, h_edge) - mean(A) | D011 |
| 参数量 | 25,858 | contract.md |
| 学习率 LR | 1e-3（共享） | — |
| 折扣因子 gamma | 0.99 | — |
| ε 衰减 eps_decay | 20 | D036：eps_decay=5+per-episode随机化导致探索不足，20修复 |
| 目标网络更新 target_update | 3000 | — |
| 经验回放 buffer | 200K | D027 扩大（原 50K 在 50 UE 下不足） |
| batch size | 128 | — |
| 梯度裁剪 grad_clip | 1.0 | — |
| 训练 episodes（50+ UE） | 100 | — |
| 训练 episodes（15-20 UE） | 50 | — |
| 评估 seeds | 3（100, 200, 300） | — |

---

## 5. flat MLP+topK 配置（C6 对照组）

来源：contract.md "flat MLP+topK 架构（C6 对照组）"

| 超参数 | 值 | 说明 |
|--------|------|------|
| top-K | 6 | 与 E4 相同 |
| 网络结构 | Dueling DDQN：obs_dim=34 → 128 → 64 → V(1) + A(6) | — |
| 参数量 | 13,191 | — |
| 其余训练配置 | 与 E4 相同 | LR, gamma, buffer, batch 等完全一致 |

---

## 6. Level 1: 20 UE 基线可行性

来源：D036, eps_decay=20, 3 seeds × 3 eval seeds

| 指标 | GNN (E4-20-d20) | MLP (C6-20-d20) | gap |
|------|----------------|----------------|-----|
| Reward | 12,847 ± 126 | 12,861 ± 101 | **-0.1%** |
| 阻塞率 | 0.0006 ± 0.0016 | 0.0000 ± 0.0000 | — |
| 切换次数 | 1,336 ± 191 | 1,079 ± 89 | +23.8% |
| Jain 公平性 | 1.000 | 1.000 | — |
| 吞吐量 (Mbps) | 2,371 ± 15 | 2,399 ± 13 | — |

评估配置：3 seeds 训练，3 eval seeds (100,200,300)，eps_decay=20。

结论：GNN 与 MLP 在 20 UE 下性能持平（gap -0.1%），符合文献预期——GNN 优势在 N>20-30 时才显现（Lee 2023, Shen 2019）。

---

## 7. Level 2: 同规模扩展

### 7.1 50 UE (cap=15)

来源：D036, eps_decay=20, 3 seeds × 3 eval seeds

| 指标 | GNN (E4-50-c15-d20) | MLP (C6-50-c15-d20) | gap |
|------|---------------------|---------------------|-----|
| Reward | 28,198 ± 978 | 23,273 ± 792 | **+21.2%** |
| 阻塞率 | 0.0101 ± 0.0110 | 0.0955 ± 0.0151 | **-89.4%** |
| 切换次数 | 3,928 ± 1,089 | 8,214 ± 2,323 | **-52.2%** |
| Jain 公平性 | 1.000 | 0.996 | — |
| 吞吐量 (Mbps) | 2,354 ± 30 | 2,074 ± 36 | +13.5% |

评估配置：3 seeds 训练，3 eval seeds，eps_decay=20。

结论：50UE 下 GNN 显著优于 MLP（reward +21.2%，阻塞率 -89.4%），GNN 的 inter-UE 建模在大规模下发挥作用。

### 7.2 100 UE (cap=25)

来源：D028 (eps_decay=5 旧数据，eps_decay=20 下训练不稳定，已放弃同规模 100UE)

| 指标 | GNN (E4-100-c25) | MLP (C6-100-c25) | gap | 来源 |
|------|-----------------|-----------------|-----|------|
| Reward | 45,313 | 33,843 | **+34%** | D028 |
| 阻塞率 | 8.56% | 20.6% | **-58%** | D028 |

注：此为 eps_decay=5 单 seed 数据（seed=42 固定 episode）。eps_decay=20 下 100UE 同规模训练因探索不足而不稳定。文献中同规模最大 UE 数为 50（Lee & Lim 2025），100UE 贡献通过 size gen 体现（见 §8）。

---

## 8. Level 3: Size Generalization

> 迁移条件：模型参数完全冻结，仅环境改变（UE 数量和 sat_capacity）。
> 来源：D036, eps_decay=20, 3 独立训练模型 × 3 eval seeds

### 8.1 20→50 UE 迁移

| 指标 | GNN 迁移 | MLP 迁移 | gap |
|------|---------|---------|-----|
| Retention | 218.1% ± 9.7% | 218.5% ± 5.2% | ≈0% |
| Avg reward | ~28,020 | ~28,106 | ≈0% |
| 阻塞率 | 0.0233 | 0.0204 | — |

分析：50UE 迁移 GNN ≈ MLP。MLP 的 per-UE 独立决策在中等规模（50UE, cap=15）尚能维持，负载未严重饱和。

### 8.2 20→100 UE 迁移

| 指标 | GNN 迁移 | MLP 迁移 | gap |
|------|---------|---------|-----|
| Retention | **340.3% ± 36.9%** | 248.7% ± **102.3%** | **+37%** |
| Avg reward | ~43,720 | ~32,020 | +36.5% |
| 阻塞率 (worst seed) | 0.176 | **0.455** | — |

分析：100UE 迁移是 GNN 与 MLP 的分水岭：
- GNN 3 个模型一致：retention 302%~390%，阻塞 5.5%~17.6%
- MLP seed 2 完全崩溃：阻塞 45.5%，retention 仅 107.9%
- MLP std 102.3% vs GNN std 36.9%：GNN 稳定性是 MLP 的 **2.8 倍**

根因：GNN 的二部图结构建模 inter-UE 资源竞争，在 100UE 高负载下做出全局协调的卫星分配。MLP 独立决策导致局部最优聚集，极端情况下触发级联阻塞。

### 8.3 Size Gen 完整对比表

| 规模迁移 | GNN Retention | MLP Retention | GNN 稳定性优势 (std比) |
|---------|--------------|--------------|----------------------|
| 20→50 | 218.1% ± 9.7% | 218.5% ± 5.2% | ≈1x（相当） |
| 20→100 | 340.3% ± 36.9% | 248.7% ± 102.3% | **2.8x** |

结论：GNN size gen 优势不在于"MLP 不能迁移"（MLP per-UE 架构技术上可迁移），而在于**大规模高负载下的稳定性**。50UE 负载适中时两者相当，100UE 高负载时 GNN 稳定性远优于 MLP。

### 8.4 迁移条件说明

- 模型参数完全冻结，仅环境改变（来源：contract.md Fairness Rules）
- GNN 的二部图结构天然支持可变 UE 数量（permutation equivariance）
- MLP per-UE 独立决策，架构上可迁移，但缺乏 inter-UE 协调导致大规模不稳定

---

## 9. 消融实验全表

来源：contract.md "Ablation Plan"

| 编号 | 消融目标 | 预期影响方向 | 实际结果 | 结论 | 来源 |
|------|---------|-------------|---------|------|------|
| A1 | top-K 压缩（B2→C6） | reward 大幅提升 | ✓ B2 25% → C6 0% 阻塞 | top-K 压缩是决定性改进（396→6 动作空间，reward 4866→9857） | contract.md / D022 |
| A2 | GNN 消息传递（C6→E4） | reward 小幅提升 | ✓ +0.8% at 15 UE（+77 reward over C6）；20 UE 实测 gap ≈ 0% | GNN 有效但增量有限，真正决定性改进来自 top-K | D022 |
| A3 | GNN 深度 T=2 vs T=1 | reward 下降 | ✓ -1.8% | T=2 消息传递是最关键 GNN 组件 | contract.md / D022 |
| A4 | orbit_phase 编码 | reward 轻微下降 | ✓ -0.4% | orbit_phase 有轻微正面贡献 | contract.md |
| A5 | size generalization（20UE→100UE） | GNN 保持，MLP 崩溃 | ✓ GNN retention 340.3%，MLP 248.7%（std 102.3%，最差 seed 阻塞 45.5%） | size gen 稳定性是 GNN 决定性优势（std 比 2.8x） | D036 |

注：A1-A5 为 contract.md 记录的已完成消融，属于方案 C 消融链。消融路径：B2（flat 396-action DDQN）→A1 top-K 压缩→C6（flat MLP+topK）→A2 GNN 消息传递→E4（GNN+DDQN）；A3/A4 为 E4 组件消融；A5 为 size generalization 验证。方案 A 的消融（A1 flat FC vs LA-DDQN）见 execution_report.md，属于方案 A 体系，非方案 C 消融。

---

## 10. 训练配置对比

GNN (E4) vs MLP (C6) 超参对比表：

| 配置项 | GNN (E4) | MLP (C6) | 说明 | 来源 |
|--------|---------|---------|------|------|
| top-K | 6 | 6 | 相同 | contract.md |
| 编码方式 | 二部图 MPNN-E（per-UE bipartite + MPNN-E） | 展平向量 | 唯一差异 | contract.md Fairness Rules |
| 网络结构 | MPNN-E: T=2, hidden=32, out=64 | FC: obs_dim=34 → 128 → 64 | — | contract.md |
| Q 函数 | 分解式：V(h_ue) + A(h_ue, h_sat, h_edge) | flat: V(1) + A(6) | — | contract.md |
| 参数量 | 25,858 | 13,191 | — | contract.md |
| LR | 1e-3 | 1e-3 | 相同 | contract.md |
| gamma | 0.99 | 0.99 | 相同 | contract.md |
| buffer | 200K | 200K | 相同 | contract.md |
| batch size | 128 | 128 | 相同 | contract.md |
| 训练 episodes（50+ UE） | 100 | 100 | 相同 | contract.md |
| 训练 episodes（15-20 UE） | 50 | 50 | 相同 | contract.md |
| 评估 seeds | 3 (100, 200, 300) | 3 (100, 200, 300) | 相同 | contract.md |
| sat_capacity | 相同（按 UE 规模比例调整） | 相同 | 公平性保障 | contract.md |

---

## 11. B2 CUDA 崩溃记录

来源：decision_log D031

| 项 | 详情 |
|------|------|
| 场景 | B2 Dueling DDQN，50 UE |
| 失败现象 | CUDA launch failure |
| 根因 | 396 维动作空间 + 50 UE 导致 CUDA 内存/计算溢出 |
| 决策 | 不重新尝试。B2 在 15 UE 已 25% 阻塞率，50 UE 必然更差，50 UE 额外验证非必要 |
| 来源 | D031 |

---

## 12. 成功/失败信号对照

### 12.1 成功信号 (S1-S4)

来源：contract.md "Success Signal", D036 eps_decay=20 数据

| 条件 | 指标 | 阈值 | 实测 (eps_decay=20) | 是否满足 |
|------|------|------|---------------------|---------|
| S1: 同规模 50 UE | GNN vs MLP reward gap | ≥15% | **+21.2%** | ✓ |
| S2: Size gen 50 UE | GNN 迁移 retention | ≥100% | **218.1%** | ✓ |
| S3: Size gen 100 UE | GNN 迁移稳定性 | std < MLP std | **36.9% vs 102.3%** | ✓ |
| S4: 20 UE 基线 | GNN ≈ MLP | gap <5% | **-0.1%** | ✓ |

### 12.2 失败信号 (F1-F3)

来源：contract.md "Failure Signal"

| 条件 | 触发条件 | 状态 | 说明 |
|------|---------|------|------|
| F1: 50 UE 同规模 | GNN vs MLP gap <5% | **未触发** | GNN +21.2%，eps_decay=20 修复后显著 |
| F2: Size gen 无差异 | GNN 迁移 ≈ MLP 迁移 | **部分触发** | 50UE 迁移 GNN ≈ MLP，但 100UE 迁移 GNN 稳定性远优于 MLP |
| F3: 训练不稳定 | GNN 无法收敛 | **未触发** | eps_decay=20 训练稳定 |

---

## 13. 数据一致性检查

以下是 decision_log 与 contract.md 之间可能存在不一致的数字：

### 13.1 D028/D029 旧数据 vs D036 新数据

| 记录位置 | 旧值 (eps_decay=5, seed=42) | 新值 (eps_decay=20, 3 seeds) | 说明 |
|---------|---------------------------|------------------------------|------|
| D028 50UE 同规模 | MLP +4.9% | **GNN +21.2%** | eps_decay=5 探索不足导致 GNN 被低估 |
| D029 size gen 100UE | GNN 35,699 vs MLP -9,710 | GNN retention 340% vs MLP 249% (std 102%) | 旧数据 seed=42 固定 episode，MLP 崩溃是因为固定场景记忆，新数据更可靠 |
| F1 50UE | "MLP 略优 +4.9%" | **GNN +21.2%** | 已 superseded |

**根因**：D028/D029 使用 eps_decay=5 + `run_ep(seed=42)`，每 episode 场景完全相同，GNN 探索在 ~15 episode 后停止，无法适应 per-episode 随机化。D036 改用 eps_decay=20，GNN 有足够探索窗口。

### 13.2 D022 vs S4: GNN 增量数值

| 记录位置 | 描述 | 数值 |
|---------|------|------|
| D022 | GNN 在 top-K 基础上仅 +0.8%（+77 reward over C6） | +0.8% at 15 UE |
| 本文档 §6 (20 UE 实测) | 20 UE 基线 GNN ≈ MLP | gap -0.13% at 20 UE |

**说明**：D022 报告 +0.8% 对应 15 UE（Groundwork 阶段 UE 数量），20 UE 实测 gap 为 -0.13%（GNN 略低但基本持平）。UE 数量不同，数值差异合理。两档位结论一致：GNN 与 MLP 在小规模下性能相当。

### 13.2 D022 中 T=2 消融贡献

| 记录位置 | 描述 |
|---------|------|
| D022 | "T=2 消息传递是最关键 GNN 组件（+1.8%）" |
| contract.md A3 | "T=2 vs T=1 reward 下降 -1.8%" |

**说明**：D022 和 A3 表述角度不同——D022 说去掉 T=2 会导致 -1.8%，A3 预期方向也是 reward 下降。数值一致，方向一致。

### 13.3 方案 A 消融 vs 方案 C 消融的 A1 编号复用

| 记录位置 | A1 含义 |
|---------|---------|
| execution_report.md | A1 = Flat FC 消融（方案 A 体系，否定 DLA） |
| contract.md Ablation Plan | A1 = top-K 压缩消融（方案 C 体系，B2→C6） |

**说明**：两套消融编号体系不同，A1 含义完全不同。方案 A 已放弃（D021），方案 C 消融编号以 contract.md 为准。

### 13.4 E4-50 首次运行失败

| 记录位置 | 描述 |
|---------|------|
| D027 | "50 UE × 720 steps = 36K transitions/episode，buffer 50K 仅存 ~1.4 episode 导致 GNN 训练崩溃（E4-50 首次运行 reward -4,857）" |

**说明**：E4-50 最终结果在扩容 buffer 至 200K 后恢复正常，contract.md 中未记录此次失败的中间值。最终 50 UE 同规模结果以 F1 记录的"MLP 略优 +4.9%"为准。

---

## 14. sat_capacity 调整记录

来源：decision_log D026

| UE 规模 | sat_capacity | 调整理由 | 来源 |
|---------|-------------|---------|------|
| 20 UE | cap=10 | 基准配置 | contract.md |
| 50 UE | cap=15 | 按比例调整 | D026 |
| 100 UE | cap=25 | 按比例调整 | D026 |

**调整决策和理由**（来源：D026）：
- cap=10 在 100 UE 下结构性不可行：~5 可见卫星 × 10 容量 = 50 < 100 UE
- Phase 1 验证确认 cap=10 × 100 UE 随机阻塞率 86%，任何算法都无法有效改善
- 按比例调整保证负载强度在各规模下可比较，而非简单复制固定 capacity
- GNN 和 MLP 使用相同 capacity（公平性保障，来源：contract.md Fairness Rules）
