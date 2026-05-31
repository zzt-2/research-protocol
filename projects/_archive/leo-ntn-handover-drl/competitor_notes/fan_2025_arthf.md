# ARTHF (Fan et al., 2025, MDPI Electronics)

## 基本信息

- **标题**: Joint Traffic Prediction and Handover Design for LEO Satellite Networks with LSTM and Attention-Enhanced Rainbow DQN
- **作者**: Dinghe Fan, Shilei Zhou, Jihao Luo, Zijian Yang, Ming Zeng
- **年份**: 2025 (online 2025-07-30)
- **期刊**: Electronics, Vol. 14, Issue 15, Page 3040
- **DOI**: 10.3390/electronics14153040
- **URL**: https://www.mdpi.com/2079-9292/14/15/3040
- **许可**: CC BY 4.0 (开放获取)

---

## 网络架构

### 整体流程

ARTHF 分为两个串联模块：(1) LSTM 流量预测模块，输入历史流量输出未来需求；(2) Attention-Enhanced Rainbow DQN 切换决策模块，将预测流量嵌入状态空间后输出切换动作。

### LSTM 流量预测模块

- **输入**: 每个TTG的历史流量时序，维度 `[T_l, F_l]`，其中 `T_l=3`（3个历史时隙），`F_l=3`（3个特征通道）
- **结构**: 两层堆叠 LSTM
  - Layer 1: 3个 LSTM 单元，输入维度 `F_l=3`，输出隐藏状态 `h_t^(1)`
  - Layer 2: 3个 LSTM 单元，输入来自 Layer 1 的输出，输出隐藏状态 `h_t^(2)`
  - 每个 LSTM 层包含标准 forget gate / input gate / output gate
- **输出头**: 全连接层序列 `(128, 64, 32, 1)` + ReLU 激活，生成标量流量预测值 `d_k,pre_t`
- **每个 TTG 独立处理**：不共享参数或隐藏状态

### Attention-Enhanced Rainbow DQN 切换模块

完整网络结构（从输入到输出）：

```
输入: S_e ∈ R^{M_k^max × 7}  (zero-padded state matrix, M_k^max=8)
  │
  ▼
Self-Attention Layer
  │  Q_m = s_m · W_Q,  K_m = s_m · W_K,  V_m = s_m · W_V   (Eq.26)
  │  输出维度 D (论文未明确给出具体数值)
  │  α_{m,n} = softmax over n=1..M_k^t  (Eq.27, 仅在有效卫星上计算)
  │  z_m = Σ_n α_{m,n} · v_n                             (Eq.28)
  │  → 输出 Z ∈ R^{M_k^max × D}
  ▼
Fully Connected Layers (逐行处理，保持矩阵结构)
  │  FC(256) + ReLU → FC(128) + ReLU → FC(64) + ReLU
  │  → 输出 H ∈ R^{M_k^max × 64}
  ▼
Masking
  │  o_m = 1 if S_e(m,:) ≠ 0, else 0                     (Eq.29)
  │  H' = H ⊙ o  (逐元素乘mask)
  ▼
Dueling Architecture (两个并行分支)
  │
  ├─ Value Branch:
  │    h_avg = (1/M_k^t) Σ_m H'(m,:)                     (Eq.30, 仅对有效卫星平均)
  │    FC layer → 标量状态价值 v
  │
  └─ Advantage Branch:
       直接处理 H'，经 FC layer → 优势矩阵 A ∈ R^{M_k^max × |action_dist|}
       每行 A(m,:) 对应卫星 m 的优势分布
  │
  ▼
Q-value 组合
  │  Q(m,:) = v^T + A(m,:) - (1/M_k^max) Σ_{n=1}^{M_k^max} A(n,:)   (Eq.31)
  │  → Q ∈ R^{M_k^max × |action_dist|}
  ▼
Softmax (逐行)
  → 选择概率分布 P ∈ R^{M_k^max × N_atoms}
  → 每行 P(m,:) 表示选择卫星 m 的概率分布
```

### Attention 模块详细说明

- **Q/K/V 来源**: 对每个卫星 m 的特征向量 `s_m = S_e(m,:)`（7维），分别通过可学习矩阵 `W_Q, W_K, W_V` 线性投影得到 `q_m, k_m, v_m`，输出维度记为 D
- **注意力分数**: `α_{m,n} = exp(q_m · k_n / D) / Σ_n exp(q_m · k_n / D)`，分母的 softmax 范围仅覆盖**有效卫星** `n=1..M_k^t`（不含 padding）
- **缩放因子**: D 作为温度参数稳定梯度（即 scaled dot-product attention）
- **输出**: `z_m = Σ_n α_{m,n} · v_n`，每个卫星获得所有有效卫星的加权聚合表示

### Dueling 架构详细说明

- **Value 分支**: 先对所有有效卫星的特征行做平均池化 `h_avg`，再经 FC 层输出标量状态价值 `v`——与具体卫星无关的全局评估
- **Advantage 分支**: 直接对 `H'`（masked 后的特征矩阵）经 FC 层，输出矩阵 `A`，每行对应一颗卫星的相对优势
- **Q 值组合**: `Q(m,:) = v^T + A(m,:) - mean(A, axis=0)`，使用 M_k^max 上的均值做中心化（非仅有效卫星）
- **最终动作选择**: 对 Q 矩阵逐行 softmax 得到概率分布 P

---

## MDP 定义

### 观测空间（状态空间）

对每个 TTG k，状态为矩阵 `S ∈ R^{M_k^t × 7}`，每行对应一颗可见卫星，7列特征为：

| 列 | 特征 | 含义 |
|----|------|------|
| 1 | `s_{k,m}^t` | 服务状态（二值：当前是否由该卫星服务） |
| 2 | `θ_{k,m}^t` | 仰角（度） |
| 3 | `d_{k,m}^t` | 距离（km） |
| 4 | `T_{k,m}^t` | 剩余覆盖时间（s） |
| 5 | `SNR_{k,m}^t` | 信噪比（dB） |
| 6 | `l_m^t` | 该卫星的归一化负载（所有接入TTG的权重之和） |
| 7 | `Ψ_{k,m}^t` | 计算得到的负载代价（含预测流量，见Eq.18） |

**关键**: 第7列 `Ψ` 已经融合了 LSTM 预测的未来流量需求。

### 动作空间

- 离散动作：`a_t ∈ {1, 2, ..., M_k^t}`，选择哪颗可见卫星接入
- 动作空间大小随时间变化（可见卫星数量动态变化）

### 奖励函数

$$r_t = \sum_{k=1}^{K} \left[ \Lambda_k^t + \beta \cdot \text{SNR}_{k,m}^t + \gamma \cdot \Psi_{k,m}^t \right]$$

其中各项定义：

1. **切换代价** `Λ_k^t`（Eq.17）：
   - 若切换（`s_k^t ≠ s_k^{t-1}`）：`Λ = -μ`（μ 为正常数）
   - 若不切换：`Λ = 0`

2. **通信质量** `β · SNR_{k,m}^t`：直接使用所选卫星的信噪比，权重 β

3. **负载代价** `Ψ_{k,m}^t`（Eq.18）：
   ```
   Ψ_{k,m}^t = -( l_m^t + (1-w_p) · d_{k,cur}^t + w_p · d_{k,pre}^t )
   ```
   - `l_m^t`：卫星 m 当前的总归一化负载
   - `d_{k,cur}^t`：TTG k 的当前流量负载
   - `d_{k,pre}^t`：LSTM 预测的 TTG k 未来流量负载
   - `w_p ∈ [0,1]`：预测权重，平衡当前与预测负载
   - 负号：负载越高代价越大（惩罚）

4. **约束**：
   - C1: 每颗卫星的服务状态为二值变量
   - C2: 动作在可见卫星集合内
   - C3: 仰角 ≥ 最低仰角 θ_min

---

## 训练配置

### 超参数

| 参数 | 值 |
|------|-----|
| Learning rate | 0.001 |
| Discount factor γ | 0.95 |
| Training episodes | 1000 |
| Optimizer | 未明确指定 |
| Replay buffer size | 未明确给出 |
| Batch size | 未明确给出 |
| Rainbow DQN 其他组件 (Double DQN, Distributional RL, n-step, prioritized replay) | 论文仅提"rainbow DQN"但**未详述**具体启用了哪些 rainbow 组件 |
| μ (切换惩罚常数) | 未明确给出数值 |
| β, γ (奖励权重) | 未明确给出数值 |
| w_p (预测权重) | ∈ [0,1]，未明确给出数值 |
| M_k^max (最大可见卫星) | 8 |
| 时隙长度 | 5 s |
| 切换触发间隔 | 3 slots (15 s) |

### LSTM 训练配置

| 参数 | 值 |
|------|-----|
| 输入维度 [T_l, F_l] | [3, 3] |
| LSTM 层数 | 2 (stacked) |
| 每层单元数 | 3 |
| FC 输出头 | 128 → 64 → 32 → 1 (ReLU) |
| Learning rate | 0.001 |
| 训练 episodes | 1000 |

### 训练收敛表现

- 论文未给出收敛曲线或具体收敛轮数
- 仅展示稳态性能对比（Figure 5-8 的时序图）
- 4种对比方法：ARTHF / Attention Rainbow DQN（无预测）/ Rainbow DQN + 预测 / Rainbow DQN（无预测无attention）

### 星座仿真配置

基于 SpaceX Starlink 设计，5个子星座：

| 子星座 | 轨道高度 | 卫星数 | 倾角 | 轨道面数 |
|--------|----------|--------|------|----------|
| 1 | 540 km | 1584 | 53° | 72 |
| 2 | 550 km | 1584 | 53° | 72 |
| 3 | 560 km | 348 | 97.6° | 6 |
| 4 | 560 km | 172 | 97.6° | 4 |
| 5 | 570 km | 720 | 70° | 36 |

TTG: 20×20 网格，25 km 格距，流量来自 Milan 数据集。
频段: Ka-band (20 GHz)，带宽 400 MHz，最低仰角 40°。

---

## 候选卫星处理

### 可变数量候选卫星的方案

**采用 zero-padding + masking 策略**：

1. **Padding**: 将实际状态矩阵 `S ∈ R^{M_k^t × 7}` 零填充到固定大小 `S_e ∈ R^{M_k^max × 7}`（M_k^max = 8）
2. **Attention 阶段**: softmax 分母仅在有效卫星 `n=1..M_k^t` 上计算（Eq.27），padding 卫星不参与注意力计算
3. **FC 后 Masking**: 通过 `o_m = 1{S_e(m,:) ≠ 0}`（Eq.29）识别有效卫星，对 H 逐元素乘 mask 得 H'
4. **Value 分支**: 仅对有效卫星特征做平均（Eq.30 使用 M_k^t 而非 M_k^max）
5. **Advantage 中心化**: 使用 M_k^max 做均值（Eq.31），包含 padding 行的零值

### 输入组织

- 每行 = 一颗可见卫星的特征向量（7维）
- 行数固定为 M_k^max=8，不足补零
- 每个 TTG 独立决策（per-TTG agent）

---

## 负载感知机制

### 状态中的负载信息

状态矩阵的第6列 `l_m^t` 为卫星 m 的归一化负载（所有接入该卫星的 TTG 的权重之和），来自 SIB 广播。

### 状态中的预测负载信息

第7列 `Ψ_{k,m}^t` 通过 Eq.18 将当前负载与 LSTM 预测的流量需求融合：
```
Ψ_{k,m}^t = -( l_m^t + (1-w_p)·d_{k,cur}^t + w_p·d_{k,pre}^t )
```
预测流量 d_{k,pre}^t 来自 LSTM 模块。

### 奖励函数中的负载编码

奖励第三项 `γ · Ψ_{k,m}^t` 直接使用上述负载代价，同时考虑：
- 卫星已有负载 `l_m^t`
- TTG 自身当前负载 `d_{k,cur}^t`
- TTG 预测的未来负载 `d_{k,pre}^t`

无预测的 baseline 使用贪心策略（鼓励所有 TTG 选当前最低负载卫星，不考虑实际流量需求差异）。

### 是否有显式负载均衡机制

**无显式约束**。负载均衡完全通过奖励函数中的惩罚项隐式实现，没有硬约束（如卫星负载上限）。评估指标使用 Jain's Fairness Index 衡量负载均衡效果。

---

## 与 LA-DDQN 方案的重叠度评估

> 注：此处的 LA-DDQN 指 He et al. (GLOBECOM 2020) 的 Load-Aware DDQN 方案（参考文献 [8]）。

### 重叠组件

| 组件 | ARTHF | LA-DDQN |
|------|-------|---------|
| DRL 基础框架 | Rainbow DQN (含 dueling) | Q-learning / DQN |
| 切换决策建模 | MDP | MDP |
| 负载感知 | 奖励中编码负载 | 奖励/约束中编码负载 |
| 多 TTG 场景 | 有 | 有（multi-agent） |
| 卫星可见性处理 | 可变候选集 | 类似 |

### 不重叠 / 差异化空间

| 差异点 | ARTHF | LA-DDQN |
|--------|-------|---------|
| **流量预测** | LSTM 预测模块，预测嵌入状态 | 无预测模块 |
| **Attention 机制** | Self-attention 消除位置偏差 | 无 attention |
| **DQN 变体** | Rainbow DQN（分布式、dueling 等） | 基础 Q-learning / DQN |
| **候选集处理** | Zero-padding + masking | 固定结构 |
| **负载建模深度** | 区分当前负载与预测负载，加权融合 | 仅当前负载 |
| **训练架构** | 集中式（单 agent） | 分布式（multi-agent） |
| **通信质量建模** | 详细的大尺度衰落模型 (ITU-R) | 简化模型 |

### 对我们方案的启示

1. **LSTM 预测是可借鉴的核心思路**：将预测流量嵌入状态/奖励，实现主动式负载均衡
2. **Self-attention 处理变长候选集**：比 zero-padding + 固定 FC 更优雅，消除位置偏差
3. **Dueling + Rainbow 的稳定性**：Value/Advantage 分离提升了训练稳定性
4. **不足之处**：
   - 论文未公布关键超参数（μ, β, γ, w_p），复现困难
   - Rainbow DQN 具体启用了哪些组件（n-step? prioritized? distributional?）未说明
   - LSTM 与 DQN 联合训练策略未详述（端到端？分步？）
   - 每个 TTG 独立处理 LSTM，不考虑 TTG 间的空间相关性
   - 仿真规模虽大但未给出计算开销分析
