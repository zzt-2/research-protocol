---
created: 2026-05-20
status: frozen
version: 1
---

# Research Contract — ris-phase-drl

## Hypothesis

在 N≥100 元素的 RIS 辅助 MU-MISO 系统中，标准 MLP-DRL（TD3/SAC/DDPG）退化为固定策略（avg ≈ Fixed ±1%）。一种**信道条件注意力网络**（Channel-Conditioned Attention Network, CCAN）通过逐元素注意力机制建模 RIS 元素间信道关联，使 TD3 能够学到信道自适应的相移策略，在 N=100、κ=10dB 场景下平均 sum rate 相对 MLP-DRL baseline 提升 ≥10%。

**假设来源**：
- baseline_report 实证：MLP-DRL avg=1291 ≈ Fixed avg=1292（-0.9%），确认 MLP 失效
- baseline_report 实证：PSO avg=1554 (+20% over Fixed)，确认信道自适应优化有价值
- 根因分析：obs_dim=2600→400 首层压缩比过大，MLP 无法从原始信道矩阵提取有效特征
- L013 (2026 IEEE) 负面证据：vanilla FCN 在 RIS 优化中随 N 增大失败

## Success Signal

CCAN+TD3 在 N=100、M=8、K=4、κ=10dB 场景下：
- **主指标**：跨 ≥3 seeds 的平均 sum rate ≥ 1.10 × MLP-TD3 平均 sum rate
- 即 CCAN avg ≥ 1419 bps/Hz（MLP-TD3 avg=1291, 1.10×=1420）
- **次指标**：CCAN avg ≥ PSO avg × 0.90（即 ≥1400 bps/Hz），证明 DRL 接近启发式上界

## Failure Signal

以下任一条件触发即为失败（独立定义，非 success 反面）：
1. CCAN+TD3 平均 sum rate < 1.05 × MLP-TD3 avg（<1356 bps/Hz），即 CCAN 无实质改进
2. CCAN 训练不收敛（loss 发散或 NaN，或 1000ep 内 avg 未超过 Fixed baseline）
3. CCAN 在 κ≤5dB 场景下仍 ≈ Fixed（说明改进仅来自特定信道条件，非架构优势）

## Baselines

- B1: TD3+MLP (来源: F3/AB-TD3) — 复现状态: **已复现** (baseline_report, avg=1291) — 交叉验证: 40% 田野调查出现率
- B2: SAC+MLP (来源: 领域共识) — 复现状态: **已复现** (baseline_report, avg=1292) — 交叉验证: 22% 田野调查出现率
- B3: DDPG+MLP (来源: L02) — 复现状态: **已复现** (baseline_report, avg=1293) — 交叉验证: 40% 田野调查出现率
- B4: PSO (来源: 启发式 baseline) — 复现状态: **已复现** (baseline_report, avg=1554) — 交叉验证: 1/8 竞品使用
- B5: Random — 复现状态: **已复现** (avg=430) — 下界
- B6: Fixed (θ=π) — 复现状态: **已复现** (avg=1292) — 非平凡固定策略（Rician LoS 对齐）

## Metrics

- M1: Average Sum Rate (bps/Hz) — 跨 episode 平均 sum rate — 越高越好 — **主指标**
- M2: Best Episode Sum Rate (bps/Hz) — 峰值性能 — 越高越好
- M3: Convergence Speed (episodes) — 达到最终 avg 95% 所需 episodes — 越低越好
- M4: 推理延迟 (ms/step) — 单步前向传播时间 — 越低越好

## Fairness Rules

1. **相同 RL 超参**：CCAN 和 B1-B3 使用相同的 lr=1e-3、γ=0.99、τ=1e-3、batch_size=256、buffer_size=1e5、grad_clip=1.0
2. **相同观测空间**：所有方法观测相同的 (Re(H1), Im(H1), Re(H2), Im(H2), cos(θ), sin(θ))。CCAN 通过内部注意力层处理，MLP baseline 通过展平 MLP 处理
3. **参数量对齐**：CCAN 总参数量 ≤ 2× MLP baseline 参数量。如超出需消融验证改进非来自容量
4. **相同训练预算**：相同 episode 数 × 相同 seeds × 相同评估 protocol（确定性评估，50 episodes，独立种子）
5. **不公平声明**：CCAN 使用注意力架构（更强的归纳偏置），这是核心创新点本身，不是不公平优势。消融实验 A3 验证此偏置的贡献

## Ablation Plan

| 编号 | 消融目标 | 预期影响方向 | 预期影响大小 |
|------|---------|-------------|-------------|
| A1 | w/o attention（用 per-element MLP 替代注意力） | 下降 | 中（~5-8%） |
| A2 | w/o parameter sharing（每个元素独立网络） | 下降 | 大（~10-15%，参数爆炸） |
| A3 | w/o channel encoder（原始 obs 直接进 policy MLP） | 下降 | 大（≈回到 MLP baseline） |

## Experiment List

| 编号 | 实验名 | 类型 | 优先级 |
|------|--------|------|--------|
| E1 | CCAN+TD3 vs B1-B6（N=100, κ=10dB） | 核心 | P0 |
| E2 | CCAN+SAC / CCAN+DDPG（架构迁移性） | 对比 | P1 |
| E3 | N ∈ {64, 100, 200} 规模扩展 | 鲁棒 | P1 |
| E4 | κ ∈ {3, 5, 10} dB 信道复杂度 | 鲁棒 | P1 |
| E5 | K ∈ {2, 4, 8} 用户数扩展 | 鲁棒 | P2 |
| E6 | Ablation A1 (w/o attention) | 消融 | P1 |
| E7 | Ablation A2 (w/o parameter sharing) | 消融 | P1 |
| E8 | Ablation A3 (w/o channel encoder) | 消融 | P1 |

## Simulation Config

### 信道模型
- Rician 衰落（ULA LoS + CN(0,1) NLoS），块衰落（每 episode 独立生成）
- 直连链路阻断（Hd=0）
- 路径损耗模型：PL = PL₀(d/d₀)^{-α}

### 核心参数
- N（RIS 元素数）：{64, 100, 200}
- M（BS 天线数）：8
- K（用户数）：{2, 4, 8}
- κ（Rician 因子）：{3, 5, 10} dB
- Episode 长度：50 步（块衰落，信道不变）

### DL 架构（CCAN）
- Channel Encoder：per-element attention, d_model=64, n_heads=4
- Phase Decoder：shared MLP (128→N)，输入 (channel_embed, cos θ, sin θ)
- RL 算法：TD3（hidden=(400,300) for critic）
- Actor 参数量：≤ 2× MLP Actor（~1M params 上限）

### 训练配置
- Episodes：2000（early stopping: 100-ep avg 变化 <1%）
- Seeds：≥3（seed 0,1,2）
- Optimizer：Adam, lr=1e-3
- Buffer：1e5 transitions
- Batch：256
- γ=0.99, τ=1e-3, grad_clip=1.0

### 评估条件
- 确定性评估（无探索噪声），50 episodes，独立种子
- 报告：avg ± std, best, 收敛速度

## Parameter Provenance

| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| N | {64,100,200} | L06:100, F3:32-64 | |
| M | 8 | L02:8, F3:8-12 | |
| K | {2,4,8} | L02:4, F3:8-12 | |
| κ | {3,5,10} dB | [设计选择: 覆盖弱/中/强 LoS 场景，B3 风险对冲] | |
| Hd | 0（阻断）| F3:§II-A | |
| T | 50 步 | [设计选择: MVE v3 验证通过，多步块衰落防 MDP 退化] | |
| P_t | 30 dBm | [设计选择: 微基站典型值; L06=25dBm(室内), F3=30dBW(空中), L05扫描含30dBm] | |
| σ² | -94 dBm | [计算: kT₀B+NF = -174+70+10 = -94 dBm, 参考 L06:Section IV] | |
| f_c | 2.4 GHz | L05:Section IV | |
| B | 10 MHz | L05:Section IV | |
| PL₀ | -30 dB | L02:Section IV | |
| d₀ | 1 m | L02:Section IV | |
| α₁ | 2.2 | L02:Section IV | |
| α₂ | 2.8 | F4:Table (beta=2.8) | |
| d_BS-RIS | 50 m | [设计选择: L02坐标推导≈104m, L06室内≤6m; 取50m为城市微基站合理距离] | |
| d_RIS-UE | 10 m | [设计选择: L06室内3-5m, L02室外≈55m; 取10m为RIS近距离覆盖] | |
| lr | 1e-3 | F3:1e-3 | |
| γ | 0.99 | F3:0.99 | |
| τ | 1e-3 | F3:1e-3 | |
| batch_size | 256 | [设计选择: 标准 DRL 默认值] | |
| buffer_size | 1e5 | F3:1e5 | |
| seeds | ≥3 | [设计选择: 统计规范性] | 超越全部竞品(0/8) |

[ASSUMPTION] 已全部消除：0/22。α₂ 升级为 F4 来源，其余 3 个为设计选择（附文献交叉引用）。

## 声称-证据映射表

| Claim | Type | Planned Experiment | Expected Evidence |
|-------|------|-------------------|-------------------|
| C1: CCAN+TD3 在 N=100 时 avg sum rate ≥1.10× MLP-TD3 | bounded | E1 | 表：各方法 avg±std, 配对 t 检验 p<0.05 |
| C2: 信道自适应是 CCAN 改进的来源（非参数量） | bounded | E6,E8 | 消融表：w/o encoder ≈ baseline |
| C3: CCAN 跨 RL 算法有效 | bounded | E2 | 表：CCAN+SAC/DDPG > MLP+SAC/DDPG |
| C4: CCAN 在不同信道条件下有效 | bounded | E4 | 图：avg rate vs κ 曲线 |
| C5: CCAN 随 N 扩展保持优势 | bounded | E3 | 图：avg rate vs N 曲线 |
