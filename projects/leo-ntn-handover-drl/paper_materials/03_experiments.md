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
| ε 衰减 eps_decay | 40 | — |
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

来源：contract.md S4, D022

| 指标 | GNN (E4-20) | MLP (C6-20) | gap | 来源 |
|------|------------|------------|-----|------|
| Reward gap | — | — | **+0.3%** | contract.md S4 |

评估配置：3 seeds，50 episodes 训练（20 UE 档位），3 seeds 评估。

结论：GNN 与 MLP 在 20 UE 下性能接近（gap +0.3%），符合文献预期——GNN 优势在 N>20-30 时才显现（Lee 2023, Shen 2019）。

---

## 7. Level 2: 同规模扩展

### 7.1 50 UE (cap=15)

| 指标 | GNN (E4-50-c15) | MLP (C6-50-c15) | gap | 来源 |
|------|----------------|----------------|-----|------|
| Reward | — | — | MLP 略优 +4.9% | contract.md F1 |

评估配置：3 seeds，100 episodes 训练（50+ UE 档位），3 seeds 评估。

来源：contract.md F1 注明"MLP 略优 +4.9%，但在 size gen 场景 GNN +61.5%"。

### 7.2 100 UE (cap=25)

| 指标 | GNN (E4-100-c25) | MLP (C6-100-c25) | gap | 来源 |
|------|-----------------|-----------------|-----|------|
| Reward | 45,313 | 33,843 | **+34%** | D028 |
| 阻塞率 | 8.56% | 20.6% | **-58%** | D028 |

评估配置：3 seeds，100 episodes 训练，3 seeds 评估。来源：decision_log D028。

---

## 8. Level 3: Size Generalization

> 迁移条件：模型参数完全冻结，仅环境改变（UE 数量和 sat_capacity）。来源：contract.md Fairness Rules

### 8.1 20→50 UE 迁移

| 指标 | GNN 迁移 | MLP 迁移 | gap | 来源 |
|------|---------|---------|-----|------|
| Reward gap | — | — | **GNN +61.5%** | contract.md S2 / D029 |

来源：contract.md S2 阈值 ≥15%，实测 +61.5%。

### 8.2 20→100 UE 迁移

| 指标 | GNN 迁移 | MLP 迁移 | gap | 来源 |
|------|---------|---------|-----|------|
| GNN 迁移 reward | 35,699（正 reward） | — | — | contract.md S3 / D029 |
| MLP 迁移 reward | — | -9,710（完全崩溃） | — | D029 |
| MLP 迁移阻塞率 | — | 71.5% | — | D029 |
| GNN vs MLP gap | — | — | **+467%** | contract.md A5 / D029 |

来源：decision_log D029, contract.md A5。

### 8.3 50→100 UE 迁移

源文件中未记录此实验数据。contract.md 实验列表中 E1-E9 未包含 50→100 迁移实验。

### 8.4 迁移条件说明

- 模型参数完全冻结，仅环境改变（来源：contract.md Fairness Rules）
- GNN 的 permutation equivariance 使参数在 UE 数量变化时保持语义
- MLP 固定维度输入无法泛化（来源：D029）

---

## 9. 消融实验全表

来源：contract.md "Ablation Plan"

| 编号 | 消融目标 | 预期影响方向 | 实际结果 | 结论 | 来源 |
|------|---------|-------------|---------|------|------|
| A1 | top-K 压缩（B2→C6） | reward 大幅提升 | ✓ B2 25% → C6 0% 阻塞 | top-K 压缩是决定性改进（396→6 动作空间，reward 4866→9857） | contract.md / D022 |
| A2 | GNN 消息传递（C6→E4） | reward 小幅提升 | ✓ +0.8% at 15 UE（+77 reward over C6） | GNN 有效但增量有限，真正决定性改进来自 top-K | D022 |
| A3 | GNN 深度 T=2 vs T=1 | reward 下降 | ✓ -1.8% | T=2 消息传递是最关键 GNN 组件 | contract.md / D022 |
| A4 | orbit_phase 编码 | reward 轻微下降 | ✓ -0.4% | orbit_phase 有轻微正面贡献 | contract.md |
| A5 | size generalization（20UE→100UE） | GNN 保持，MLP 崩溃 | ✓ GNN reward 35,699，MLP reward -9,710，gap +467% | size generalization 是 GNN 决定性优势 | contract.md / D029 |

注：A1-A5 为 contract.md 记录的已完成消融。方案 A 的消融（A1 flat FC vs LA-DDQN）见 execution_report.md，属于方案 A 体系，非方案 C 消融。

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

来源：contract.md "Success Signal"

| 条件 | 指标 | 阈值 | 实测 | 是否满足 |
|------|------|------|------|---------|
| S1: 同规模 100 UE | GNN vs MLP reward gap | ≥15% | **+34%** | ✓ |
| S2: Size generalization 50 UE | GNN 迁移 reward gap | ≥15% | **+61.5%** | ✓ |
| S3: Size generalization 100 UE | GNN 迁移保持正 reward | 正值 | **35,699** | ✓ |
| S4: 20 UE 基线 | GNN ≈ MLP | gap <5% | **+0.3%** | ✓ |

### 12.2 失败信号 (F1-F3)

来源：contract.md "Failure Signal"

| 条件 | 触发条件 | 状态 | 说明 |
|------|---------|------|------|
| F1: 50 UE 同规模 | GNN vs MLP gap <5% | **未触发** | MLP 略优 +4.9%，但在 size gen 场景 GNN +61.5% |
| F2: Size gen 无差异 | GNN 迁移 ≈ MLP 迁移 | **未触发** | GNN +467% at 100 UE |
| F3: 训练不稳定 | GNN 无法收敛 | **未触发** | 100 UE 训练 loss 稳定下降 |

---

## 13. 数据一致性检查

以下是 decision_log 与 contract.md 之间可能存在不一致的数字：

### 13.1 D022 vs S4: GNN 增量数值

| 记录位置 | 描述 | 数值 |
|---------|------|------|
| D022 | GNN 在 top-K 基础上仅 +0.8%（+77 reward over C6） | +0.8% at 15 UE |
| contract.md S4 | 20 UE 基线 GNN ≈ MLP | gap +0.3% at 20 UE |

**说明**：D022 报告 +0.8% 对应 15 UE（Groundwork 阶段 UE 数量），contract.md S4 报告 +0.3% 对应 20 UE（Contract 调整后的 UE 数量）。UE 数量不同，数值差异合理。

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
