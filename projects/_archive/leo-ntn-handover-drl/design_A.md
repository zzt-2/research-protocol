# 方案 A 设计文档：LA-DDQN（负载注意力 Dueling DDQN）

> 2026-05-08，基于 ARTHF 精读缓存 + 搜索脚本结果（20 条）完成。
> 本文件为独立设计文档，不修改其他文件。

---

## 1. ARTHF 竞争者关键发现

**ARTHF** (Fan et al., 2025, MDPI Electronics 14(15):3040) 是方案 A 的最强竞争者。

### 1.1 架构核心

- **Self-attention**（Eq.26-28）：Q/K/V 全部来自卫星特征 s_m ∈ R^7，经 W_Q/W_K/W_V 线性投影
- Attention softmax 仅在有效卫星间计算（M_k^t，非 M_max），positional bias 问题被论文夸大
- Self-attention 真正作用是**捕获卫星间关系**，而非"消除位置偏差"
- **Dueling Rainbow DQN**：Value 分支对有效卫星平均池化 → FC → v；Advantage 分支从 H（含 zero-pad）计算 → A ∈ R^{M_max×|atoms|}
- Advantage 中心化使用 M_k^max（含 zero-pad），引入数值偏差
- **Zero-padding** 到 M_max=8 候选，FC 处理含 ~40% 无效行

### 1.2 复现障碍

| 缺失项 | 影响 |
|--------|------|
| μ（切换惩罚常数） | 奖励函数无法完整复现 |
| β, γ（SNR/负载权重） | 奖励各分量相对权重未知 |
| w_p（预测权重） | 无法评估 LSTM 预测的实际贡献 |
| Rainbow 具体组件 | 不知哪些 rainbow 组件被启用 |
| LSTM 与 DQN 联合训练策略 | 端到端？分步？未知 |

**结论**：ARTHF A8 消融（完整复现）不可行，只能做近似对标（self-attention 风格对比）。

### 1.3 ARTHF 对比方法局限

仅对比 3 个 Rainbow DQN 变体（有/无 attention、有/无 LSTM），**无传统 baseline**。这削弱了论文的说服力——无法证明 DRL 方法整体优于传统启发式。

---

## 2. DLA（负载驱动注意力）模块设计

### 2.1 设计原则

ARTHF self-attention 的 Q/K/V 全部来自卫星特征，attention 权重**不受负载状态驱动**。DLA 的核心原则：**让负载分布主动决定"看什么"**。

这产生了结构层面的差异（cross-attention vs self-attention），而非超参调优层面。

### 2.2 架构

```
Input: Top-K 候选 (K, 5)
  [sinr_norm, load_norm, elev_norm, rem_t_norm, is_svc]
         │
    ┌────┴────┐
    │         │
┌───┴───┐ ┌───┴────┐
│Load   │ │Sat     │
│Stats  │ │Feats   │
│(1, 4) │ │(K, 5)  │
└───┬───┘ └───┬────┘
    │         │
 W_Q↓     W_K↓  W_V↓
 q(1,d)  K(K,d) V(K,d)
    │         │
    └────┬────┘
         │
  Cross-Attention
  α = softmax(q·Kᵀ / √d)  →  α ∈ R^{1×K}
  z = Σ_m α_m · V_m         →  z ∈ R^{1×d}
         │
  Per-satellite Fusion
  h_m = [sat_feat[m] ; z]   →  (K, 5+d)
         │
  FC(256)→FC(128)→FC(64)
  H ∈ R^{K×64}
         │
  ┌──────┴──────┐
  │ Dueling     │
  │ V: mean(H)→FC→v      │
  │ A: H→FC→A ∈ R^K      │
  │ Q(m)=v+A(m)-mean(A)  │
  └─────────────┘
```

### 2.3 负载统计 Query 构造

| 维度 | 名称 | 计算 | 范围 |
|------|------|------|------|
| 0 | l_avg | 候选卫星 load_norm 均值 | [0, 1] |
| 1 | l_max | 候选卫星 load_norm 最大值 | [0, 1+] |
| 2 | l_std | 候选卫星 load_norm 标准差 | [0, 0.5] |
| 3 | n_svc | 候选中当前服务卫星数（0 或 1） | {0, 1} |

**语义**：l_avg 反映整体负载水平，l_max 捕捉最拥堵卫星，l_std 反映负载离散度（高 → 有轻载可选），n_svc 标记是否有当前连接。

### 2.4 与 ARTHF Self-Attention 的结构对比

```
ARTHF Self-Attention:
  Query 来源: 卫星 m 的特征 s_m        ← 每颗卫星独立 query
  Key 来源:   卫星 n 的特征 s_n        ← 卫星间互查
  Value 来源: 卫星 n 的特征 s_n
  输出:       Z ∈ R^{M_max × d}       ← 每颗卫星独立输出
  语义:       "卫星 m 应该关注哪些其他卫星"

DLA Cross-Attention:
  Query 来源: 负载统计 [l_avg,l_max,l_std,n_svc]  ← 全局负载上下文
  Key 来源:   卫星 m 的特征                        ← 卫星被查询
  Value 来源: 卫星 m 的特征
  输出:       z ∈ R^{1 × d}                        ← 单一负载感知上下文向量
  语义:       "给定当前负载分布，哪些卫星特征最重要"
```

**本质区别**：
- ARTHF: Q/K/V 同源 = **self-attention**，建模卫星间关系
- DLA: Q 来自负载、K/V 来自卫星 = **cross-attention**，建模"负载状态→卫星特征重要性"映射
- 输出形态不同：ARTHF 每颗卫星独立输出，DLA 产生单一上下文向量广播到所有卫星

### 2.5 参数规格

| 参数 | 值 | 理由 |
|------|------|------|
| K（候选数） | 8 | ≥ max 可见卫星数（avg 4.4, max ≈ 6-7） |
| d（注意力维度） | 64 | 与 FC 最后一层一致 |
| W_Q 输入维度 | 4 | 负载统计 |
| W_K/W_V 输入维度 | 5 | 完整卫星特征 |
| FC 层 | 256→128→64 | 与 B2 DDQN 骨干一致 |
| DLA 额外参数 | W_Q(4×64)+W_K(5×64)+W_V(5×64) = 896 | 极轻量 |

### 2.6 DLA 预期行为

| 负载场景 | DLA 行为 | 退化为 |
|----------|---------|--------|
| 低负载（l_avg < 0.3） | 权重趋均匀 | SINR 主导选择 |
| 高负载（l_avg > 0.7） | 权重偏向低负载卫星 | 负载均衡优先 |
| 单星高负载（l_max 高, l_avg 低） | 权重回避高负载卫星 | 选择性避让 |
| 高离散（l_std 高） | 权重集中到轻载卫星 | 梯度化选择 |

**核心特性**：DLA 自动在"信号优先"和"负载优先"之间切换，无需显式阈值规则。这是 ARTHF self-attention 无法实现的行为——因为 self-attention 的 Q 不包含负载上下文信息。

---

## 3. Top-K 候选压缩

### 3.1 问题

当前观测空间：396×4 + 1 = 1585 维。平均可见 4.4 颗卫星，有效数据仅 ~18 维，利用率 1.1%。

### 3.2 压缩方案

```
Top-K obs = K×5 + 1 = 41 维（K=8）
压缩率: (1585-41)/1585 = 97.4%
```

每颗候选卫星 5 维特征：[sinr_norm, load_norm, elev_norm, rem_t_norm, is_svc]。

**排序准则**：score_m = sinr_norm(m) + rem_t_norm(m)，取 top-K。
- 负载**不参与排序**——留给 DLA 学习
- 仰角不参与排序——与 rem_t 高度相关（仰角高→剩余时间长）
- is_svc 保证当前服务卫星**始终在候选集中**（排序前强制包含）

### 3.3 信息损失分析

| K 值 | 损失 | 依据 |
|------|------|------|
| K≥7 | **零** | 仿真器统计 max 可见卫星 ≈ 6-7 |
| K=6 | ≈0% | 极少数时刻可见 7 颗 |
| K=5 | 低 | 丢弃 0-1 颗最弱候选（低 SINR + 短剩余时间） |
| K=4 | 中低 | 可见 5+ 颗时丢弃排序末尾 1-2 颗 |
| K=3 | 中 | 可见 5+ 颗时丢弃 2+ 颗 |
| K=2 | 高 | 过激进，可能丢失优质候选 |

### 3.4 vs Zero-padding（ARTHF 方案）

| 维度 | Zero-padding (ARTHF) | Top-K (LA-DDQN) |
|------|---------------------|------------------|
| 固定维度 | M_max=8 | K=8 |
| 有效信息密度 | ~55%（avg 4.4/8 行有效） | 100%（所有行有效） |
| FC 计算浪费 | ~45% 在 zero-pad 行上 | 0% |
| Advantage 中心化偏差 | 含 zero-pad 行的零值 | 无偏差 |
| Attention softmax | 需手动 mask 无效行 | 无需 mask（全有效） |
| 排序信息 | 丢失（原始顺序） | 保留（按质量排序） |
| 与星座规模耦合 | 否（M_max 固定） | 否（K 固定） |

**推荐 K=8**：零信息损失 + 与 ARTHF M_max=8 对齐便于公平对比。

---

## 4. 完整网络架构

### 4.1 从观测到动作的完整流程

```
[Environment State]
  396 卫星 × (sinr, elev, load) + 15 UE × is_current + t_conn
        │
  [Top-K Preprocessor]
  按 score=sinr+rem_t 排序 → 取 K=8 候选
  提取负载统计 [l_avg, l_max, l_std, n_svc]
  输出: candidates (K, 5), load_stats (1, 4)
        │
  [DLA Module]（§2）
  Cross-attention: load_stats → Q, candidates → K/V
  Per-sat fusion → FC(256→128→64) → H (K, 64)
        │
  [Dueling Q-Network]
  V = FC(mean(H)) → scalar
  A = FC(H) → R^K
  Q(m) = V + A(m) - mean(A)
        │
  [Action Selection]
  ε-greedy: argmax Q(m) with prob (1-ε)
  Action ∈ {0, ..., K-1}
        │
  [Environment.step(action)]
```

### 4.2 参数量

| 模块 | 参数量 | 说明 |
|------|--------|------|
| Top-K 预处理 | 0 | 纯排序+切片 |
| W_Q | 4×64 = 256 | 负载→query 投影 |
| W_K | 5×64 = 320 | 卫星→key 投影 |
| W_V | 5×64 = 320 | 卫星→value 投影 |
| Fusion + FC | (5+64)×256 + 256×128 + 128×64 ≈ 52K | 标准 FC 层 |
| Value 分支 | 64×64 + 64×1 ≈ 4K | |
| Advantage 分支 | 64×64 + 64×1 ≈ 4K | |
| **总计** | **~61K** | vs B2 DDQN ~712K（减少 12×） |

参数效率来源：Top-K 将输入维度从 1585 压缩到 41，消除了巨大的第一层 FC。

### 4.3 训练配置

| 参数 | 值 | 理由 |
|------|------|------|
| Learning rate | 1e-3 | 与 B2 一致 |
| Discount factor γ | 0.99 | 与 B2 一致 |
| Buffer size | 100K | 与 B2 一致 |
| Batch size | 256 | 与 B2 一致 |
| Target update | 每 1000 步 | 与 B2 一致 |
| ε-greedy | 1.0 → 0.01，指数衰减 | 与 B2 一致 |
| Episodes | 300 | 与 B2 一致 |
| Optimizer | Adam | 标准选择 |
| 奖励函数 | v2: r=0.6·R_norm+0.4·L_norm-0.5·B-0.1·H | 与 baseline 统一 |

---

## 5. 消融实验设计

### 5.1 实验组（8 组 + 2 对照）

| # | 名称 | Attention | 候选 | 负载 Query | K | 目的 |
|---|------|-----------|------|-----------|---|------|
| **A1** | Flat FC | 无（FC 直连） | Top-K | — | 8 | 去除 attention，验证 DLA 价值 |
| **A2** | Self-Attn | Self-attention | Top-K | — | 8 | 对标 ARTHF 风格，与 DLA 对比 |
| **A3** | LA-DDQN pad | Cross-attention | Zero-pad | ✓ | 8 | Top-K vs Zero-padding |
| **A4a** | LA-DDQN K=4 | Cross-attention | Top-K | ✓ | 4 | K 值敏感度 |
| **A4b** | LA-DDQN K=6 | Cross-attention | Top-K | ✓ | 6 | K 值敏感度 |
| **A4c** | LA-DDQN K=8 | Cross-attention | Top-K | ✓ | 8 | **主方法** |
| **A4d** | LA-DDQN K=10 | Cross-attention | Top-K | ✓ | 10 | K 值敏感度 |
| **A5** | No-Load-Query | Cross-attention | Top-K | ✗（Q=卫星特征） | 8 | 去除负载驱动 query |
| **A6** | Fixed-Weight | 无学习 attention | Top-K | 固定 sinr+load | 8 | 学习权重 vs 固定权重 |
| — | B2 DDQN | 无 | 全量 396×4 | — | — | DRL baseline |
| — | B1 HHS | — | — | — | — | 传统 baseline |
| — | B4 Random | — | — | — | — | 下界 |

**注意**：A4a-d 合并为一个实验组（K 值敏感度），编号为用户指定的 A4。

### 5.2 各组设计细节

**A1: Flat FC（去除 attention）**
- 候选卫星 (K,5) 直接展平为 (K×5,) → FC(256→128→64) → Dueling Q
- 目的：隔离 DLA 的贡献。如果 A4c ≈ A1，说明 attention 无用。

**A2: Self-Attention（对标 ARTHF）**
- Q/K/V 全部来自卫星特征（每行 s_m ∈ R^5）
- attention 输出 Z ∈ R^{K×d}，逐行进入 FC
- 目的：cross-attention vs self-attention 的结构差异验证。如果 A4c > A2，证明负载驱动 query 比卫星自关联更有效。

**A3: Zero-padding（候选处理对比）**
- 不做 top-K 排序，改为 zero-padding 到 K=8
- 候选按**原始编号顺序**排列，不足 8 颗补零
- DLA 内部需额外 mask 机制（与 ARTHF Eq.27 一致）
- 目的：如果 A4c > A3，证明 top-K 排序优于 zero-padding。

**A4: K 值敏感度（4/6/8/10）**
- A4c (K=8) 是主方法，A4a/b/d 变化 K 值
- 预期：K=6≈K=8≈K=10 > K=4（4 太激进可能丢候选）
- 目的：证明 K=8 选择的合理性，并展示方法的鲁棒性

**A5: 去除负载特征**
- Cross-attention 仍存在，但 Q 不用负载统计
- 改为 Q = mean(sat_feats)（卫星特征均值作为 query）
- 目的：如果 A4c > A5，证明"负载驱动"是关键，而非 attention 结构本身

**A6: 固定权重 vs 学习权重**
- 用固定公式替代学习 attention：α_m = softmax(sinr_norm(m) × (1 - load_norm(m)))
- 手工设计：信号好 + 负载低 → 高权重
- 目的：如果 A4c > A6，证明学习到的 attention 模式优于人工启发式

**A7: 与 B2 DDQN 对比**
- B2 是无 attention、无 top-K 的全量 flat DDQN
- A4c vs B2：展示完整方法的整体提升

**A8: 与 ARTHF 近似复现对比**
- 完整复现不可行（μ/β/γ/w_p 未公开）
- 近似方案：A2（self-attention + top-K）+ 分布式 Q（51 atoms）模拟 Rainbow DQN
- 如果 A8 可行性不足，用 A2 替代 ARTHF 对标

### 5.3 评估指标

| 指标 | 公式/定义 | 权重 |
|------|----------|------|
| 吞吐量 | Σ_UE Σ_t R_norm(t) | 主指标 |
| 阻塞率 | Σ(B=1) / 总步数 | 主指标 |
| 切换次数 | Σ(H=1) / 总步数 | 辅助 |
| Jain 公平指数 | (Σx_i)² / (n·Σx_i²)，x_i=各 UE 吞吐量 | 辅助 |
| 训练收敛速度 | 达到 95% 最终性能的 episode 数 | 效率 |
| 单步推理时间 | ms/step（含 attention 计算） | 部署 |

### 5.4 预期排序

```
阻塞率:  B4 < A4c < A2 ≈ A3 < A1 < A5 < A6 < B1
吞吐量:  A4c > A2 ≈ A4d > A3 > A4b > A1 ≈ A5 > A6 > B4 > B1
Jain's:  A4c > A2 > A3 > A4b > A1 > A5 > A6 > B1 >> B4
训练速度: A1 > A6 > A4a > A4b > A4c > A2 > A3 > A4d >> B2
```

**关键对比对**：
- A4c vs A2 → DLA(cross-attention) vs ARTHF(self-attention)，验证负载驱动 query 的价值
- A4c vs A1 → DLA 整体贡献
- A4c vs A3 → Top-K vs Zero-padding
- A4c vs A5 → 负载 query 的具体作用
- A4c vs A6 → 学习 vs 固定 attention
- A4a-d → K 值敏感度曲线
- A4c vs B2 → 完整方法 vs baseline

### 5.5 统计方法

- 5 个随机种子，报告均值 ± 标准差
- 配对 t 检验（α=0.05）判断显著性
- 训练曲线：滑动平均（window=10 episodes）

---

## 6. 贡献评估与目标期刊

### 6.1 贡献清单

| # | 贡献 | 类型 | 强度 | 说明 |
|---|------|------|------|------|
| C1 | DLA cross-attention 负载驱动 query | 方法论 | ★★★☆ | 结构性差异（非超参调优），但增量改进性质 |
| C2 | Top-K 候选压缩（97.4% 降维零损失） | 工程 | ★★☆☆ | 实用但非原创性贡献 |
| C3 | 8 组消融 + 传统 baseline 对照 | 实证 | ★★★☆ | 比 ARTHF（仅 Rainbow 变体对比）全面得多 |
| C4 | 轻量骨干（Dueling DDQN vs Rainbow DQN） | 工程 | ★★☆☆ | 简化而非创新 |

### 6.2 诚实评估

**方案 A 的核心叙事**：

> "ARTHF 用 self-attention 建模卫星间关系，但 attention 权重不受负载状态驱动。我们提出 DLA（负载驱动注意力），用负载统计作为 cross-attention query，让模型根据负载分布动态调整对卫星特征的关注。结合 Top-K 候选压缩消除零填充噪声，LA-DDQN 在负载均衡和阻塞率上显著优于 self-attention 方案。"

**优势**：
- 差异化清晰（cross vs self, top-K vs zero-pad）
- 消融设计严格，能证明每个组件的独立贡献
- 有传统 baseline（HHS）对标，补足 ARTHF 的缺失

**劣势**：
- 增量改进 ARTHF 而非范式创新
- ARTHF 发在 MDPI Electronics（IF~2.6），发更高级别期刊需更强的差异化
- Top-K 压缩作为独立贡献偏弱

### 6.3 目标期刊评估

| 期刊级别 | 可行性 | 理由 |
|----------|--------|------|
| MDPI（Electronics, Sensors, IEEE Access） | **高** | 差异化充分，消融全面，ARTHF 同级期刊 |
| IEEE CL / IEEE WCL | 中高 | 需要缩短为 letter 格式（6 页），突出核心发现 |
| IEEE TWC / TMC / JSAC | **低** | 增量改进性质，顶刊需更强创新 |
| Computer Networks / Physical Communication | 中 | 欧洲期刊，对方法论创新宽容度较高 |

**推荐目标**：MDPI Electronics/Sensors（保底）或 IEEE Access（冲刺），投稿周期 2-4 个月。

### 6.4 综合评分

```
方案 A: ★★★☆☆ (3/5)
  创新性:   中（cross-attention 结构差异，但增量性质）
  实现风险: 低（B2 DDQN 直接扩展）
  工作量:   中（2-3 周实现 + 1-2 周实验 + 2-3 周写作）
  发表概率: 高（MDPI）/ 中（IEEE Access）
```

---

## 7. 方案 A vs C 对比与推荐

### 7.1 核心对比

| 维度 | A: LA-DDQN | C: GNN+DRL |
|------|-----------|-----------|
| **新颖性** | 中（ARTHF 覆盖 Dueling+Attention+Load 三要素） | **中高**（"二部图GNN+DRL+多UE负载均衡"无人占据） |
| 创新性质 | 增量改进（改 attention 类型 + 候选压缩） | **范式差异**（flat obs → 图结构化表示） |
| 实现复杂度 | 中（DLA 模块 + top-K 预处理） | 高（Graph Builder + GNN + 分解式 Q + 预训练） |
| 训练稳定性 | **低风险**（DDQN 扩展，成熟） | 中高风险（GNN 训练 + 拓扑非平稳） |
| 参数量 | ~61K（vs B2 712K） | **~29K（vs B2 712K，少 25×）** |
| 故事清晰度 | 中（需详细解释与 ARTHF 差异） | **高**（"结构化图编码→负载感知决策"） |
| 消融说服力 | 强（8 组 + 传统 baseline） | 中（6 组，GNN 层/预训练/图结构） |
| 可扩展性 | 低（K 固定） | **高**（图大小可变，GNN 参数共享） |
| 与文献差异 | 与 ARTHF 差异化需仔细论证 | 与 L15/Yu et al. 差异化清晰自然 |
| 目标期刊 | MDPI / IEEE Access | IEEE CL / IEEE TWC / Computer Networks |

### 7.2 风险-收益矩阵

```
         高收益 ←────────────────→ 低收益
           │                        │
  高风险   │    方案 C              │
           │  （如果 GNN 训练成功）  │  （不适用）
           │                        │
  ─────────┼────────────────────────┼──────
           │                        │
  低风险   │    方案 A              │
           │  （稳定发表）          │  （不适用）
           │                        │
```

### 7.3 推荐策略

**策略 1（保守）**：先做方案 A，确保发表
- 时间：4-6 周
- 风险：低
- 产出：1 篇 MDPI 级论文（保底）

**策略 2（进取）**：先做方案 C，A 作为退路
- 时间：6-8 周（C 可能需返工）
- 风险：中高
- 产出：如果 C 成功 → 1 篇更高级别论文；如果失败 → 退回 A

**策略 3（推荐）**：**C 主攻 + A 的 top-K 预处理直接复用**
- top-K 候选压缩不是方案 A 专属——方案 C 的 Graph Builder 同样受益（图规模从 396 降到 6-8）
- 先实现 top-K 预处理（通用组件），然后在 C 上构建 GNN
- 如果 C 训练不稳定，已有 top-K + DLA 可退回方案 A
- 时间：与策略 2 相同，但共享基础设施降低返工成本

### 7.4 最终建议

**方案 C 为主攻方向**，方案 A 保留为降级方案。理由：

1. **新颖性差距显著**：方案 C 的"三元组合无人占据"是硬事实，A 需要与 ARTHF 做细致差异化论证
2. **top-K 通用性**：A 的 top-K 压缩直接服务于 C（减少图节点），两个方案共享基础设施
3. **故事力**：C 的"flat → graph"叙事比 A 的"self-attention → cross-attention"更有说服力
4. **方案 A 的消融设计已就绪**：如果 C 失败，可直接启动 A 的 8 组消融实验

**执行顺序**：
1. 实现 top-K 预处理（方案 A/C 共享）
2. 实现 GNN + 分解式 Q（方案 C）
3. 预训练 + 联合训练
4. 如果 C 成功 → C 消融实验 → 撰写
5. 如果 C 训练不稳定 → 切换到 A（DLA + 已有 top-K）→ A 消融实验 → 撰写
