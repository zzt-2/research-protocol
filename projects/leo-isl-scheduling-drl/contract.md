---
created: 2026-05-15
status: frozen
version: 1
---

# Research Contract — LEO ISL Scheduling via GNN-DRL

## Hypothesis

在 N_LCT=3 终端约束的 LEO 巨型星座中，基于 GAT-PPO 的拓扑感知 ISL 调度方法通过学习边级选择策略（对每条候选 ISL 独立评分并选 top-K），相比固定贪心基线能将网络吞吐量从 17.09% 提升到 ≥25%，同时将切换率控制在 0.5 以下。

**核心创新点**（文献空白确认）：
1. 首个用 GNN 编码星座拓扑结构做 ISL 调度的 DRL 方法（vs 现有 4 篇 DRL 全用 FC 网络）
2. 首个支持逐链路独立评分的细粒度动作空间（vs 现有方法 8/16 选项粗粒度）
3. 在 N_LCT 终端约束下系统评估（vs 现有工作假设无限 ISL 或固定 4 条）

## Success Signal

**定量阈值**：在 Starlink Phase I（24×66=1584 星）全规模、N_LCT=3、demand=10Gbps 场景下：
- M1（吞吐量）≥ 25%（固定贪心 17.09%，相对提升 ≥46%）
- 同时 M3（切换率）≤ 0.5（稳定性约束）
- 消融实验 A1（GNN→FC）证明拓扑编码贡献 ≥3 个百分点 M1 提升

**评估条件**：5 个随机种子取均值，标准差 < 2 个百分点

## Failure Signal

独立于 success 定义：
1. **DRL 优势不显著**：M1 < 19%（相对提升 <11%，不足以支撑"GNN-DRL 必要性"结论）
2. **GNN 无结构性贡献**：消融 A1 中 FC 替代 GNN 后 M1 差距 < 1 个百分点（拓扑编码无效）
3. **训练不稳定**：5 个种子中 ≥2 个发散或 M1 < 固定贪心

任一条件触发即为 failure。

## Baselines

- B1: +Grid/Fixed (来源: L01 §III-A, L09 §II-B) — 复现状态: ✅ 已复现 — 交叉验证: 被 5 篇论文使用 (L01, L03, L05, L09, L12)
- B2: Wang TCOM MADRL (来源: L09, IEEE TCOM 2024) — 复现状态: ✅ 已实现 — 交叉验证: 最直接 DRL 竞品，720 星验证

B1 为领域共识（所有论文共同基准），B2 为最接近的 DRL 竞品。

## Metrics

- M1: 吞吐量 — 成功路由流量占总需求的比例 — 越高越好（主指标）
- M2: 端到端时延 — 路由路径传播延迟均值 (ms) — 越低越好
- M3: 切换率 — 每步 ISL 变更数 / 总活跃 ISL 数 — 越低越好
- M4: 阻塞率 — 未成功路由流量占比 — 越低越好
- M5: 公平性 — Jain 公平指数 (flow-level throughput) — 越高越好

## Fairness Rules

- 统一路由算法：所有方法使用相同 Dijkstra 最短路径路由器 [D006]
- 统一信道模型：Gaussian beam + Rayleigh jitter (L01 参数)
- 统一星座参数：Starlink Phase I (24×66=1584, 550km, 53°)
- 统一流量模型：GHS-POP 100 GS 重力模型, demand=10Gbps/flow
- 统一评估指标和 episode 配置：50 步 × τ=10s
- 差异仅在 ISL 调度策略（固定拓扑 / DQN / GNN-DRL）
- 所有实验使用相同随机种子和拓扑快照（反模式 4 防护）

## Ablation Plan

| 编号 | 消融目标 | 预期影响方向 | 预期影响大小 |
|------|---------|-------------|-------------|
| A1 | GNN→FC（移除拓扑编码，3层MLP替换GATv2） | M1 下降 | 大（≥3pp） |
| A2 | 细粒度→粗粒度动作（top-3评分改为8选1固定候选集） | M1 下降 | 中（1-3pp） |
| A3 | 移除切换惩罚（奖励函数去掉 w₂·M3 项） | M3 升高，M1 可能微升或不变 | 中 |
| A4 | 无参数共享（每卫星独立网络） | 训练不稳定或收敛变慢 | 中 |

## Experiment List

| 编号 | 实验名 | 类型 | 优先级 |
|------|--------|------|--------|
| E01 | 核心方法 vs B1/B2 全规模对比 | 核心/对比 | P0 |
| E02 | 消融 A1: GNN→FC | 消融 | P0 |
| E03 | 消融 A2: 细粒度→粗粒度动作 | 消融 | P1 |
| E04 | 消融 A3: 无切换惩罚 | 消融 | P1 |
| E05 | 参数鲁棒性: demand×N_GS×Z_MAX | 鲁棒 | P1 |
| E06 | 规模泛化: 24×20 训练→24×66 推理 | 鲁棒 | P2 |

## Simulation Config

### 星座参数
- 星座: Starlink Phase I, 24 轨道面 × 66 星/面 = 1584 颗卫星
- 轨道高度: 550 km
- 轨道倾角: 53°
- 轨道面间隔 RAAN: 360°/24 = 15°

### ISL 信道模型
- 类型: 激光 ISL (LISL)
- 模型: Gaussian beam + Rayleigh 指向抖动
- 波长: λ = 1.55 μm
- 发射功率: P₀ = 20 W
- 带宽: B = 1 GHz
- 接收孔径: A = 0.01 m²
- 响应度: Ψ = 0.5 A/W
- 噪声电流: σ_N = 3×10⁻⁷ A
- 指向抖动: σ_J = 10 μrad (Rayleigh)
- 中断概率: ε = 0.001
- FOR 半角: θ = 60°

### ISL 约束
- 终端数: N_LCT = 3（每卫星最多同时 3 条 ISL）
- 最大距离: Z_MAX = 3000 km
- 同轨 ISL: 永久保持（环形），不占用 N_LCT 配额

### 流量模型
- 地面站: N_GS = 100, GHS-POP 重力模型分布
- 需求: base_demand = 10 Gbps/flow
- 源-目的对: 从地面站集合中随机采样
- 路由: 单路径 Dijkstra（传播延迟 + 1ms/hop 边权）

### Episode 配置
- 决策间隔: τ = 10 s
- Episode 长度: 50 步 (500 s ≈ 1/12 轨道周期)
- 轨道推进: 二体力学，每步更新卫星位置

### DL 架构
- GNN: GATv2, 4 heads, 64-dim, 3 层
- Actor: edge_decoder MLP (64→32→1) + Gumbel top-K selection
- Critic: global avg pool → MLP (64→32→1)
- 算法: PPO (clip=0.2, GAE λ=0.95, γ=0.99)
- 优化器: Adam, lr=3e-4
- 训练: 500 episodes, early stopping (50 ep patience)

### 奖励函数
- r_t = w₁ · R_tput − w₂ · C_switch − w₃ · C_setup
- R_tput = delivered/total_demand ∈ [0,1]（吞吐量）
- C_switch = n_changed/n_active_prev ∈ [0,1]（切换率惩罚）
- C_setup = total_setup_delay/max_possible ∈ [0,1]（建链延迟惩罚，反映 L04 setup delay）
- 权重: w₁=1.0, w₂=0.3, w₃=0.2 (D008)
- 范围: [-0.5, 1.0]
- M5(公平性)仅作为评估指标，不参与奖励（避免多目标训练不稳定）

### 评估条件
- 5 个随机种子，取均值 ± 标准差
- 评估 episodes: 20 (取最后 10 步均值)
- 显著性: 配对 t 检验, p < 0.05

## Parameter Provenance

### 星座参数
| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| N_planes | 24 | [来源: Starlink FCC filing, L04 §V] | Phase I v2 |
| S_per_plane | 66 | [来源: Starlink FCC filing, L04 §V] | Phase I v2 |
| altitude | 550 km | [来源: L01 实验设置, L04 §V] | |
| inclination | 53° | [来源: L04 §V] | |
| RAAN 间隔 | 15° | [计算: 360°/24] | 等间隔 |

### ISL 物理参数
| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| λ | 1.55 μm | [来源: L01 §II-C Eq.(3)] | 典型激光通信波长 |
| P₀ | 20 W | [来源: L01 §II-C, L02 实验设置] | |
| B | 1 GHz | [来源: L01 §II-C] | |
| A (接收孔径) | 0.01 m² | [来源: L01 §II-C Eq.(5)] | |
| Ψ (响应度) | 0.5 A/W | [来源: L01 §II-C Eq.(5)] | |
| σ_N (噪声) | 3×10⁻⁷ A | [来源: L01 §II-C Eq.(5)] | |
| σ_J (指向抖动) | 10 μrad | [来源: L01 §II-B Eq.(2)] | Rayleigh 分布 |
| ε (中断概率) | 0.001 | [来源: L01 §III-D Eq.(20)] | |
| θ_FOR | 60° | [来源: L01 §III-A Eq.(8)] | |
| Z_MAX | 3000 km | [来源: L01 §III-A, L02 实验设置] | |

### 调度约束参数
| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| N_LCT | 3 | [设计选择: 鲁棒性扫描甜点, D012] | gap=11.1%, 9/9配置验证 |
| demand | 10 Gbps | [设计选择: 典型激光ISL负载, 鲁棒性扫描验证] | 5G→gap↑, 20G→gap↓ |
| N_GS | 100 | [来源: L01 实验设置] | |
| τ (决策间隔) | 10 s | [设计选择: D007] | 介于 setup delay 2~30s 之间 |
| episode_steps | 50 | [设计选择: D007] | 500s ≈ 1/12 轨道周期 |

### GNN/DL 参数
| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| GAT heads | 4 | [来源: L02 网络架构] | |
| hidden_dim | 64 | [来源: L02 网络架构] | |
| GAT layers | 3 | [设计选择: 平衡表达力与过平滑] | 2-3 层常见 |
| PPO clip | 0.2 | [来源: PPO 标准默认值] | |
| GAE λ | 0.95 | [来源: PPO 标准默认值] | |
| γ | 0.99 | [来源: PPO 标准默认值] | |
| Adam lr | 3e-4 | [来源: PPO 标准默认值] | |
| 训练 episodes | 500 | [设计选择: 基于 L09 的 50 ep 和 L10 的 75000 ep] | 中间值, 含 early stopping |

### 奖励参数
| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| w₁ (吞吐量) | 1.0 | [设计选择: D008] | 主目标 |
| w₂ (切换惩罚) | 0.3 | [设计选择: D008] | 稳定性约束 |
| w₃ (建链成本) | 0.2 | [设计选择: D008] | 稳定性约束 |
