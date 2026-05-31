# 仿真器设计规格 — ris-phase-drl

## 1. 系统模型

**MU-MISO 下行 + RIS 辅助**：BS（M 天线）经 RIS（N 反射元素）服务 K 个单天线用户。

- 直连链路：**阻断**（Hd = 0），RIS 为唯一通信路径
- 级联信道：$\mathbf{h}_{\text{eff},k} = \mathbf{h}_{2,k}^H \operatorname{diag}(e^{j\boldsymbol{\theta}}) \mathbf{H}_1 \in \mathbb{C}^{1 \times M}$
- 波束赋形：ZF 预编码（基于当前级联信道），BS 侧不参与 DRL 优化
- 目标：最大化 sum rate $R = \sum_{k=1}^K \log_2(1 + \text{SINR}_k)$

**设计理由**：
- 仅优化相移（不联合波束赋形），与 MVE 一致，聚焦研究空白（大规模连续相移）
- ZF 消除用户间干扰，公平对比所有方法（beamforming 优势不混入 phase shift 贡献）
- 直连阻断：MVE v2 教训 + F3/领域共识（RIS 部署场景本就是直连受阻）

---

## 2. 信道模型

### 2.1 Rician 衰落

$$\mathbf{H} = \sqrt{\frac{\kappa}{\kappa+1}} \mathbf{H}_{\text{LoS}} + \sqrt{\frac{1}{\kappa+1}} \mathbf{H}_{\text{NLoS}}$$

- $\mathbf{H}_{\text{LoS}}$：确定性视距分量（ULA 阵列响应）
- $\mathbf{H}_{\text{NLoS}}$：$\mathcal{CN}(0,1)$ Rayleigh 分量
- $\kappa$：Rician 因子（dB）

| 链路 | 模型 | κ | 路径损耗 |
|------|------|---|---------|
| BS→RIS (H₁) | Rician | 10 dB | $PL_0 (d/d_0)^{-\alpha_1}$ |
| RIS→User (H₂) | Rician | 10 dB | $PL_0 (d/d_0)^{-\alpha_2}$ |
| BS→User (Hd) | 不建模（阻断）| — | — |

### 2.2 块衰落

- 每个 episode 开始时生成新的 H₁、H₂，episode 内固定
- episode 间独立生成（i.i.d.）
- **必须多步**：MVE v1 教训（单步导致 MDP 退化，TD3 = Random）

### 2.3 路径损耗

$$PL = PL_0 \left(\frac{d}{d_0}\right)^{-\alpha}$$

| 参数 | 值 | 来源 |
|------|-----|------|
| PL₀（参考路径损耗）| -30 dB | L02:Section IV |
| d₀（参考距离）| 1 m | L02:Section IV |
| α₁（BS-RIS 路径损耗指数）| 2.2 | L02:Section IV, L05 |
| α₂（RIS-User 路径损耗指数）| 2.8 | [ASSUMPTION] 室内外差异 |

---

## 3. Episode 结构

```
Episode 开始 → 生成 H₁, H₂（块衰落）
  Step 1:  obs = (H₁, H₂, θ₀) → agent 输出 θ₁ → 计算 R₁ → (obs₁, R₁)
  Step 2:  obs = (H₁, H₂, θ₁) → agent 输出 θ₂ → 计算 R₂ → (obs₂, R₂)
  ...
  Step T:  obs = (H₁, H₂, θ_{T-1}) → agent 输出 θ_T → 计算 R_T
Episode 结束 → 重新生成信道
```

- **T = 50 步/episode**（与 MVE 一致）
- 信道 episode 内固定，agent 可在固定信道上逐步改进相移
- 初始相移 θ₀：随机 ∈ [0, 2π)^N

---

## 4. 状态空间

| 组件 | 维度 | 说明 |
|------|------|------|
| H₁ 实部 | N×M | BS-RIS 信道 |
| H₁ 虚部 | N×M | |
| H₂ 实部 | N×K | RIS-User 信道 |
| H₂ 虚部 | N×K | |
| cos(θ_{t-1}) | N | 上一步相移（余弦分量）|
| sin(θ_{t-1}) | N | 上一步相移（正弦分量）|

**总维度**：$2NM + 2NK + 2N$

| 场景 | 维度 |
|------|------|
| N=64, M=4, K=4 | 640 + 512 + 128 = 1280 |
| N=100, M=8, K=4 | 1600 + 800 + 200 = 2600 |
| N=200, M=8, K=8 | 3200 + 3200 + 400 = 6800 |

状态包含当前相移的理由：多步 episode 中 agent 可基于当前相移做增量改进（MVE 验证有效）。

---

## 5. 动作空间

| 属性 | 值 |
|------|-----|
| 类型 | 连续 |
| 维度 | N |
| 范围 | $\mathbf{a} \in [-1, 1]^N$（tanh 输出）|
| 映射 | $\theta_n = (a_n + 1)\pi \in [0, 2\pi)$ |
| 约束 | 单位模 $|e^{j\theta_n}| = 1$（自动满足）|

绝对动作（非增量），每步直接输出完整相移向量。

---

## 6. 奖励函数

### 6.1 结构

$$r_t = \sum_{k=1}^{K} \log_2\left(1 + \frac{|\mathbf{h}_{\text{eff},k}^H \mathbf{w}_k|^2}{\sum_{j \neq k} |\mathbf{h}_{\text{eff},k}^H \mathbf{w}_j|^2 + \sigma^2}\right)$$

> **单位**：bps/Hz（频谱效率），未乘带宽 B。跨方法对比时 B 被约去，不影响相对排序。

其中 ZF 波束赋形：
$$\mathbf{W} = \mathbf{H}_{\text{eff}}^H (\mathbf{H}_{\text{eff}} \mathbf{H}_{\text{eff}}^H)^{-1} \text{diag}(\sqrt{P_1, \ldots, P_K})$$

等功率分配 $P_k = P_t / K$。

> **实现注意**：H_eff H_eff^H 接近奇异时直接求逆不稳定。必须用 `torch.linalg.solve(HH, H.T)` 替代显式求逆，或加正则化 `HH + λI`（λ=1e-6）。

### 6.2 量级分析（domain-comms.md §1.5 审查）

**单组件奖励，无量级失衡风险**：仅 sum rate 一项，无惩罚/多目标加权。

| 场景 | 预期 sum rate |
|------|--------------|
| Random phase (N=64) | ~0.004 bps/Hz [MVE 实测] |
| TD3 optimized (N=64) | ~0.17 bps/Hz [MVE 实测] |
| Random phase (N=100) | ~0.01-0.1 bps/Hz [估算] |
| TD3 optimized (N=100) | ~1-10 bps/Hz [估算] |

**归一化策略**：无需显式归一化。
- 理由：单组件，TD3/SAC 内部 reward scaling 机制足够处理
- F3、L02、L06 均未做归一化（literature_notes 已确认）
- 训练时若 reward scale 异常，通过 SAC 的自动温度调节 / TD3 的 reward scaling 参数处理

---

## 7. 波束赋形策略

**ZF 预编码**（Zero-Forcing），每个 step 基于当前级联信道重新计算：

$$\mathbf{W}_{\text{ZF}} = \hat{\mathbf{H}}_{\text{eff}}^H (\hat{\mathbf{H}}_{\text{eff}} \hat{\mathbf{H}}_{\text{eff}}^H)^{-1}$$

功率归一化：$\mathbf{W} \leftarrow \sqrt{P_t} \cdot \mathbf{W} / \|\mathbf{W}\|_F$

**设计理由**：
- ZF 消除用户间干扰 → sum rate 仅取决于有效信道增益和噪声
- 所有方法（TD3/SAC/DDPG/PSO/Random/Fixed）使用相同 ZF → 对比公平
- M ≥ K 条件满足（M=4,K=4 或 M=8,K=8）

---

## 8. 参数溯源表

| 参数 | 值 | 来源 | 验证状态 |
|------|-----|------|---------|
| N（RIS 元素数）| {64, 100, 200} | L06:100, F3:32-64, L02:80 | 已验证 |
| M（BS 天线数）| {4, 8} | L02:8, F3:8-12 | 已验证 |
| K（用户数）| {4, 8} | L02:4, F3:8-12 | 已验证 |
| κ₁（BS-RIS Rician）| 10 dB | MVE 设计 | 已验证(MVE) |
| κ₂（RIS-User Rician）| 10 dB | MVE 设计 | 已验证(MVE) |
| Hd（直连链路）| 阻断 | F3:§II-A, MVE v2 | 已验证 |
| T（episode 长度）| 50 步 | MVE 设计 | 已验证(MVE) |
| P_t（发射功率）| 30 dBm | [ASSUMPTION] 参考微基站 | 待验证 |
| σ²（噪声功率）| -94 dBm | L06:Section IV | 已验证 | <!-- VERIFY: 总噪声功率(dBm), = kT₀B + NF = -174+70+10 = -94 -->
| f_c（载频）| 2.4 GHz | L05:Section IV | 已验证 |
| B（带宽）| 10 MHz | L05:Section IV | 已验证 |
| PL₀（参考路径损耗）| -30 dB | L02:Section IV | 已验证 |
| d₀（参考距离）| 1 m | L02:Section IV | 已验证 |
| α₁（BS-RIS 路径损耗指数）| 2.2 | L02:Section IV | 已验证 |
| α₂（RIS-User 路径损耗指数）| 2.8 | [ASSUMPTION] | 待验证 |
| d_BS-RIS（BS-RIS 距离）| 50 m | [ASSUMPTION] | 待验证 |
| d_RIS-UE（RIS-用户距离）| 10 m | [ASSUMPTION] | 待验证 |
| 训练 episodes | 3000-5000 | F3:5000, L06:10000 参考 | 待验证 |
| Replay buffer | 1e5 | F3:1e5 | 已验证 |
| Batch size | 256 | [ASSUMPTION] 标准 DRL | 待验证 |
| lr（学习率）| 1e-3 | F3:1e-3 | 已验证 |
| γ（折扣因子）| 0.99 | F3:0.99, L01:0.99 | 已验证 |
| τ（软更新率）| 1e-3 | F3:1e-3 | 已验证 |
| Seeds | ≥3 | 竞品对标（0/8 声明 → 我们超越全部）| 设计决策 |

[ASSUMPTION] 参数：5/22 ≈ 23% < 30% 门槛。✅

---

## 9. 模块清单

| 模块 | 功能 | 引用 |
|------|------|------|
| `channel.py` | Rician 信道生成 + 块衰落 + 路径损耗 | L02:§II, F3:§II-A |
| `env.py` | Gym-style 环境：state→action→reward 循环 | — |
| `beamforming.py` | ZF 预编码计算 | L02:功率归一化 |
| `reward.py` | SINR + sum rate 计算 | F3:§III |
| `config.py` | 所有超参数集中管理 | — |
| `verify.py` | 解析/统计/退化验证 | §10 验证标准 |

---

## 10. 验证标准

### 10.1 解析验证

| 测试 | 方法 | 通过条件 |
|------|------|---------|
| θ=0 sum rate | 已知 H₁,H₂ → 解析计算 SINR → 与 env 输出对比 | 相对误差 < 1% |
| 全对齐相移 | 设 θ 使所有元素同相 → 验证 sum rate 为最大值 | 比随机相移高 >10× |
| ZF 零干扰 | 验证 W_ZF 下用户间干扰 = 0 | 残差 < 1e-10 |

### 10.2 统计验证

| 测试 | 方法 | 通过条件 |
|------|------|---------|
| Rician 分布 | 生成 H₁,H₂ → 检验幅度分布 | Rician κ=10dB 拟合误差 < 5% |
| 块衰落独立性 | Episode 间信道独立 | lag>T 的自相关 < 0.1 |
| 奖励分布 | Random policy → 统计 R 的均值/方差 | R > 0（有信号）|

### 10.3 退化测试

| 测试 | 方法 | 通过条件 |
|------|------|---------|
| κ→∞（纯 LoS）| 设 κ=1e6 → 信道确定性 | 100 episodes 输出方差 ≈ 0 |
| N→0（去 RIS）| 设 N=0 或 H₁=0 → 无 RIS 路径 | sum rate = 0（直连阻断）|
| 固定相移 | θ ≡ 0 → 连续 episodes | 输出完全确定 |

### 10.4 自相关预警

- Episode 内 reward 序列的 lag-1 自相关 > 0.95 → 警告"过于平滑"
- 预期：episode 内 reward 应逐步上升（agent 改进相移），lag-1 ≈ 0.5-0.9（正常）
- Episode 间独立，lag-T 自相关 < 0.1

---

## 11. MVE vs Formal 架构差异 [FR-12]

| 维度 | MVE (§D 架构摘要) | Formal (本设计) | 影响对比？ |
|------|-------------------|-----------------|-----------|
| 动作空间 | 连续 per-element, N=64, ∈ [0, 2π) | 连续 per-element, N={64,100,200}, ∈ [0, 2π) | **否**。结构相同，仅规模扩展。所有 baseline 同等扩展 |
| 决策粒度 | 全局（一次输出所有元素相移）| 全局（一次输出所有元素相移）| **否**。完全一致 |
| 对比范式 | 模型输出完整相移向量 vs baseline | 模型输出完整相移向量 vs baseline | **否**。完全一致 |
| 奖励语义 | 绝对值（即时 sum rate）| 绝对值（即时 sum rate）| **否**。完全一致 |
| 波束赋形 | 未明确（MVE 中隐含）| ZF 预编码（显式）| **否**。ZF 为所有方法共享，不改变相对排序 |

**FR-12 门控结论**：全部"否" → **通过**，进入 Step 7。

---

## 12. Baseline 实现要点

| Baseline | 动作空间 | 特殊实现需求 |
|----------|---------|-------------|
| B1: DDPG | 同 TD3（N 维连续）| 单 Q 网络 + target smoothing 无 |
| B2: SAC | 同 TD3（N 维连续）| 自动温度调节 + 双 Q |
| B3: Random | 每步随机 θ ∈ [0,2π)^N | 无网络 |
| B4: Fixed (θ=0) | θ ≡ 0 | 无网络 |
| B5: PSO | N 维连续搜索 | 种群 20-50 粒子，每步更新一次 |

PSO 在 episode 内运行：step 0 初始化种群，每 step 更新粒子位置+评估 fitness，T=50 步内收敛。所有 baseline 共享相同的 env、channel、beamforming 模块。

---

## 13. 训练配置

| 参数 | 值 | 来源 |
|------|-----|------|
| 算法 | TD3（主）/ SAC（辅）| feasibility_report §4a |
| Episodes | 3000-5000 | F3 参考 |
| Steps/episode | 50 | MVE |
| Replay buffer | 100,000 | F3 |
| Batch size | 256 | [ASSUMPTION] |
| Actor lr | 1e-3 | F3 |
| Critic lr | 1e-3 | F3 |
| γ | 0.99 | F3 |
| τ | 1e-3 | F3 |
| Hidden dims | [400, 300] | F3:400, 调整 |
| Seeds | ≥3 | 实验完备性对标决策 |
| Early stopping | 连续 100 episodes reward 变化 <1% | [ASSUMPTION] |

---

## 14. 实验场景矩阵

| 场景 | N | M | K | 目的 |
|------|---|---|---|------|
| S1（基准）| 100 | 8 | 4 | 主实验，对标竞品 |
| S2（MVE 对照）| 64 | 4 | 4 | 与 MVE 结果一致性验证 |
| S3（用户扩展）| 100 | 8 | 8 | 多用户场景泛化 |
| S4（规模扩展）| 200 | 8 | 8 | 大规模可扩展性验证 |
| S5（天线对比）| 100 | 4 | 4 | 少天线场景 |

每个场景 × 6 方法（TD3/SAC/DDPG/PSO/Random/Fixed）× ≥3 seeds。

---

## 15. 实现必做清单（code-quality.md 对照）

以下为跨 6 项目系统性踩坑归纳，Step 7 实现前逐项勾选：

### Simulator 层
- [ ] Config 用 dataclass + `__post_init__` 计算派生量，不用裸模块常量
- [ ] Env 继承 `gymnasium.Env`，返回标准 5-tuple，info dict 包含 reward 分解
- [ ] Channel 模型独立于 env，通过构造函数注入
- [ ] σ² 注释标明 `# VERIFY: 总噪声功率(dBm), = kT₀B + NF = -174+70+10 = -94`
- [ ] 奖励注释标明 `# 单位: bps/Hz（频谱效率），未乘带宽 B`
- [ ] ZF beamforming 用 `torch.linalg.solve` + 正则化（λ=1e-6），不直接求逆
- [ ] 验证套件覆盖 6 类：解析 / 统计 / 退化 / 自相关 / MDP trial / baseline

### 训练层
- [ ] **必须集成 wandb/tensorboard**（之前 6/6 项目全部缺失）
- [ ] **必须有 early stopping**（reward plateau：连续 100 episodes 变化 <1%）
- [ ] save/load 包含 optimizer + step_count + normalizer，支持 resume
- [ ] 训练中保存 best model（不只是最终 model）
- [ ] grad clip = 1.0（不过大，ntn-handover 踩过 10.0 = 无 clip 的坑）
- [ ] Replay buffer 容量验证：N=200 时 state dim=6800，buffer=1e5 → ~2.2GB CPU RAM，可接受
