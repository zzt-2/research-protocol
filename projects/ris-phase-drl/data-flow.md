# 端到端数据流推演 — ris-phase-drl (CCAN+TD3)

> 产出阶段：Contract Step 4
> 用途：Execute 阶段对着此文件写代码

## 1. 配置 → 信道生成

- 输入：SimConfig(N=100, M=8, K=4, κ=10dB, P_t=30dBm, σ²=-94dBm, ...)
- 处理：ChannelGenerator.generate()
  - 生成 H1 (N×M) Rician: sqrt(κ/(κ+1)) × H_LoS(ULA) + sqrt(1/(κ+1)) × CN(0,1)
  - 生成 H2 (N×K) Rician: 同上
  - 应用路径损耗：H1 *= sqrt(PL_BS_RIS), H2 *= sqrt(PL_RIS_UE)
- 输出：H1 (N×M) complex, H2 (N×K) complex

## 2. 观测构造

- 输入：H1, H2, 当前 θ (N,)
- 处理：_get_obs() — 拼接 6 段
  - Re(H1).ravel(): N×M = 800
  - Im(H1).ravel(): 800
  - Re(H2).ravel(): N×K = 400
  - Im(H2).ravel(): 400
  - cos(θ): N = 100
  - sin(θ): N = 100
- 输出：obs = (2600,) float32

## 3. CCAN Actor 前向传播

### 3.1 输入预处理

- 输入：obs (2600,)
- 处理：拆分为 6 段，重组为 per-element 特征
  - element_i 输入 = [Re(H1[i,:]), Im(H1[i,:]), Re(H2[i,:]), Im(H2[i,:]), cos(θ_i), sin(θ_i)]
  - shape: (N, 2M+2K+2) = (N, 26)
- 输出：per_element_feat (N, 26)

### 3.2 Channel Encoder (Attention)

- 输入：per_element_feat (N, 26)
- 处理：
  1. Linear(26, d_model=64) → (N, 64)
  2. Multi-Head Self-Attention(n_heads=4, d_model=64) → (N, 64)
     - Q,K,V: Linear(64, 64) × 3 heads
     - 每个 RIS 元素 attend 所有其他元素，捕获信道空间关联
  3. LayerNorm + Residual → (N, 64)
  4. FFN(64, 128, 64) + LayerNorm → (N, 64)
- 输出：channel_embed (N, 64)

### 3.3 Phase Decoder (Shared MLP)

- 输入：channel_embed (N, 64) + [cos(θ_i), sin(θ_i)] per element
- 处理：per-element shared MLP
  - concat: (N, 64+2) = (N, 66)
  - Linear(66, 128) → ReLU
  - Linear(128, 1) → tanh
  - 权重在 N 个元素间共享
- 输出：action (N,) ∈ [-1, 1]

## 4. 环境执行

- 输入：action (N,) ∈ [-1, 1]
- 处理：env.step(action)
  1. θ = (action + 1) × π → θ ∈ [0, 2π)
  2. phase_shift = exp(jθ) → (N,)
  3. H_eff = H2^H @ diag(phase_shift) @ H1 → (K, M)
  4. W = ZF_beamforming(H_eff, P_t, K) → (M, K)
  5. link_gain = H_eff @ W → (K, K)
  6. SINR_k = |diag_k|² / (Σ_{j≠k} |gain_{k,j}|² + σ²)
  7. sum_rate = Σ log₂(1 + SINR_k) → scalar
- 输出：next_obs (2600,), reward=sum_rate (float), terminated=bool, info={sum_rate, sinrs}

## 5. Critic 前向传播（Amendment 1: CCAN-aware Critic）

- 输入：obs (2600,), action (N,)
- 处理：
  1. 共享 Actor 的 CCAN Channel Encoder 提取信道特征（与 Actor 共享梯度）
     - obs → reshape (N, 26) → input_proj → attention → FFN → channel_embed (N, 64)
     - mean-pool over N → (64,)
  2. concat(channel_embed_pooled, action) → (64+N,) = (164,)
  3. Q1: MLP(164, 400, 300, 1)
  4. Q2: MLP(164, 400, 300, 1)
- 输出：Q1, Q2 各一个标量
- **变更理由**：原 MLP Critic 输入 2700→400 压缩比 6.75:1，丢失信道特征，无法准确评估不同信道下的动作质量（D018, D019）。新 Critic 输入仅 164 维，压缩比 2.4:1，信息保留充分。

## 6. 训练更新 (TD3)

- 输入：ReplayBuffer batch (256 transitions)
- 处理：
  1. Target smoothing: actor_target(s') + clip(Noise, -0.5, 0.5) → smoothed_action
  2. Q_target = r + γ(1-d) × min(Q1_target, Q2_target)
  3. Critic loss: MSE(Q1, Q_target) + MSE(Q2, Q_target)
  4. Delayed actor update (every 2 steps): actor_loss = -Q1(obs, actor(obs))
  5. Soft update targets: τ=1e-3
  6. Grad clip: max_norm=1.0
- 输出：updated networks

## 7. 评估指标

- 输入：每个 episode 的 reward 序列
- 处理：
  - M1: avg(sum_rates) across 50 eval episodes
  - M2: max(sum_rates) across 50 eval episodes
  - M3: first episode where rolling_avg ≥ 0.95 × final_avg
  - M4: 单步 wall-clock time (ms)
- 输出：avg±std, best, convergence_ep, latency_ms

## 跨规模泛化

- 训练配置：N=100, M=8, K=4
- 推理配置：N∈{64,100,200}, M=8, K∈{2,4,8}
- 变化维度：
  - N 变化：obs_dim 从 2600 变化（2NM+2NK+2N）
  - attention 维度不变（N 个 token，d_model=64）
  - Phase Decoder 因参数共享，N 变化不需改架构
- 处理方式：CCAN 的 per-element + shared-weight 设计天然支持 N 变化。只需调整输入 reshape 的 N 参数

## 断层检查

| 检查项 | 结果 |
|--------|------|
| obs 拆分为 per-element 特征 | ✅ (N, 26) 维度明确，每元素 2M+2K+2 |
| attention 输出维度 | ✅ (N, 64) → Phase Decoder 输入 (N, 66) |
| action 范围匹配 env | ✅ tanh ∈ [-1,1] = env.action_space |
| reward 标量 | ✅ sum_rate 单分量 |
| N 变化时维度一致性 | ✅ per-element reshape 自适应 |
| Critic 输入维度 | ✅ channel_embed(64) + act_dim(N) = 164 (原 2700→400 已修正) |

## 动作空间表达力审计 [FR-13]

| Baseline | Baseline 决策能力 | CCAN 决策能力 | CCAN ≥ Baseline？ |
|----------|------------------|--------------|------------------|
| B1: TD3+MLP | 输出 θ∈[-1,1]^N（连续 N 维），逐维独立 | 输出 θ∈[-1,1]^N，通过 attention 捕获元素间关联 | ≥（MLP 是 CCAN 无注意力时的特例） |
| B2: SAC+MLP | 同 B1 | 同上 | ≥ |
| B3: DDPG+MLP | 同 B1 | 同上 | ≥ |
| B4: PSO | 30 粒子 × 50 步迭代优化，全局搜索 | 单次前向传播 | ≠（CCAN 快但非迭代；公平性：PSO 无训练开销，CCAN 有训练成本。对比维度不同：训练后推理 vs 迭代优化） |
| B5: Random | 均匀随机 θ | — | ≥（trivially） |
| B6: Fixed | 恒定 θ=0→π | 可学到此固定值 | ≥（CCAN 可表达 Fixed 策略） |

**结论**：全部 ≥（B4 为不同范式对比，已在 fairness_rules 中声明）。CCAN 的动作空间是 MLP baseline 的超集（有注意力 → 无注意力是特例退化），表达力门控通过。
