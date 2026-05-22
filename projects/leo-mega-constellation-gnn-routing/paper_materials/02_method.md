# 方法架构

## 1. 架构总览

本文提出一种基于轨道位置编码（Orbital Positional Encoding, Orbital PE）和多尺度混合训练的 GNN 路由框架，实现 LEO mega-constellation 跨规模零样本路由泛化。核心思路：在小规模星座（66-200星）上监督训练 GAT 编码器，推理时直接部署到 720 星目标星座，通过加权 Dijkstra 推理生成近最优路径。

**端到端流程**：

```
                    训练阶段（离线）
 ┌──────────────────────────────────────────────────┐
 │  Walker-Delta 星座 (66/100/200星)                │
 │         │                                         │
 │    build_snapshot() ──→ 动态 ISL 拓扑 + 时延      │
 │         │                                         │
 │    snapshot_to_pyg() ──→ PyG Data (节点/边特征)   │
 │         │         + Orbital PE (预计算)            │
 │         │                                         │
 │    Dijkstra labels ──→ 方向监督标签 (4 类)         │
 │         │                                         │
 │    RoutingActorCritic (3层 GAT, h=128)            │
 │         │  CrossEntropy Loss + 方向掩码            │
 │         │                                         │
 │    预训练权重 → pretrained.pt                      │
 └──────────────────────────────────────────────────┘

                    推理阶段（在线）
 ┌──────────────────────────────────────────────────┐
 │  目标星座 (720星)                                 │
 │         │                                         │
 │    build_snapshot() ──→ 实时拓扑                  │
 │         │                                         │
 │    snapshot_to_pyg() ──→ PyG Data + Orbital PE    │
 │         │                                         │
 │    GNN forward() ──→ 方向 logits (N, 4)           │
 │         │                                         │
 │    加权 Dijkstra:                                 │
 │      w(u,v) = delay(u,v) + relu(best_logit - logit)│
 │         │                                         │
 │    最短路径 → 路由表                               │
 └──────────────────────────────────────────────────┘
```

**关键设计选择**：不采用逐包贪心推理（D019 确认成功率极低），而用 GNN logits 构造边权重，通过 Dijkstra 全局优化（D020）。

---

## 2. 星座与图建模

### 2.1 Walker-Delta 星座定义

采用 Walker-Delta 构型，参数记法 $T/P/F$，其中 $T = P \times S$ 为卫星总数，$P$ 为轨道面数，$S$ 为每面卫星数，$F$ 为相位因子。

卫星索引：$\text{idx} = p \cdot S + k$，其中 $p \in [0, P)$ 为轨道面编号，$k \in [0, S)$ 为面内编号。

卫星在时刻 $t$ 的 ECI 坐标：

$$\mathbf{r}(t) = r \begin{pmatrix} \cos\Omega_p \cos u - \sin\Omega_p \sin u \cos i \\ \sin\Omega_p \cos u + \cos\Omega_p \sin u \cos i \\ \sin u \sin i \end{pmatrix}$$

其中：
- $r = R_\oplus + h$ 为轨道半径
- $\Omega_p = 2\pi p / P$ 为第 $p$ 面的升交点赤经（RAAN）
- $u_{p,k}(t) = u_0^{p,k} + n \cdot t$ 为辐角，初值 $u_0^{p,k} = 2\pi(k + Fp/P)/S$
- $n = 2\pi / T_{\text{orb}}$ 为平均角速度，$T_{\text{orb}} = 2\pi\sqrt{r^3/\mu}$

**星座配置**：

| 配置 | $P$ | $S$ | $N$ | 用途 |
|------|-----|-----|-----|------|
| train_66 | 6 | 11 | 66 | 训练（小规模） |
| train_100 | 10 | 10 | 100 | 训练（中规模） |
| train_200 | 10 | 20 | 200 | 训练（大规模） |
| target_720 | 18 | 40 | 720 | 目标（零样本推理） |
| extend_1584 | 72 | 22 | 1584 | 扩展测试 |

所有配置共享 $h = 550$ km, $i = 53°$, $F = 1$。

### 2.2 +Grid ISL 拓扑

每颗卫星维持 4 条星间链路（ISL），构成 +Grid 拓扑：

- **轨内链路**（intra-orbit）：同一轨道面内相邻卫星，$k \pm 1 \pmod{S}$
- **轨间链路**（inter-orbit）：相邻轨道面同编号卫星，$(p \pm 1 \pmod{P})$ 面 $k$ 号卫星

共 $E = 2 \cdot N$ 条无向边（理想情况，未断链时）。

**动态断链**：ISL 距离超过 $d_{\max} = 5000$ km 时断开（L02 Starfield §2.2）。距离基于实时轨道力学 ECI 坐标计算，而非固定值（D016 修正）：

$$d_{u,v}(t) = \|\mathbf{r}_u(t) - \mathbf{r}_v(t)\|_2$$

断链在 66 星配置中显著（轨间距离可达 5694 km，超过阈值），训练数据天然包含不完整拓扑。

### 2.3 节点特征

| 特征 | 维度 | 说明 |
|------|------|------|
| $\mathbb{1}[\text{is\_dest}]$ | 1 | 目的节点标记（one-hot） |
| $\text{PE}_{\text{own}}$ | 16 | 自身 Orbital PE |
| $\text{PE}_{\text{dest}}$ | 16 | 目的节点 Orbital PE（广播到所有节点） |
| **合计** | **33** | |

目的节点 PE 广播到全图使每颗卫星获得目的地方向信息，与自身位置编码的差值隐式编码了"我在哪里、要去哪里"的关系。

### 2.4 边特征

| 特征 | 维度 | 说明 |
|------|------|------|
| $\delta_{\text{delay}}$ | 1 | ISL 传播时延（ms），$\delta = d / c \times 1000$ |
| $d$ | 1 | ISL 几何距离（km） |
| **合计** | **2** | |

### 2.5 ISL 信道模型

ISL 类型为光学激光链路（1550 nm，D017）。采用 Shannon 容量的简化近似：

$$C = B \cdot \log_2(1 + \text{SNR}(d))$$

$$\text{SNR}(d) = \text{SNR}_{\text{ref}} \cdot \left(\frac{d_{\text{ref}}}{d}\right)^2$$

参数：$B = 1$ GHz（L03 DuJo §V-A1），$d_{\text{ref}} = 2000$ km，$\text{SNR}_{\text{ref}} = 10^{15}$（光学链路高信噪比近似）。

> **论文标注**：此 Shannon 模型为简化近似，实际激光 ISL 容量远高于此（Starlink 约 100 Gbps/链路），但路由决策主要依赖相对时延排序，容量绝对值对路由结果影响有限。

---

## 3. Orbital Positional Encoding

### 3.1 编码公式

Walker-Delta 星座中，每颗卫星由 $(p, k)$ 唯一确定轨道位置。Orbital PE 将 $(p, k)$ 归一化后用多频率 sin/cos 编码：

$$\text{PE}(p, k; P, S) = \big[ \sin(f_i \cdot p/P),\ \cos(f_i \cdot p/P),\ \sin(f_i \cdot k/S),\ \cos(f_i \cdot k/S) \big]_{i=0}^{n_{\text{freq}}-1}$$

其中频率 $f_i = 2^i \cdot 2\pi$，$n_{\text{freq}} = d_{\text{PE}} / 4$，输出维度 $d_{\text{PE}} = 16$（4 个频率）。

### 3.2 规模无关性

关键性质：PE 输入为归一化坐标 $p/P \in [0, 1)$ 和 $k/S \in [0, 1)$，而非绝对编号。这使得：
- 训练时 66 星（$P=6, S=11$）的 PE 值域与推理时 720 星（$P=18, S=40$）相同
- GNN 学到的是"归一化轨道位置 → 方向偏好"的映射，而非记忆特定卫星编号
- 多尺度训练让模型见过不同 $(P, S)$ 组合下的归一化位置分布，增强泛化

### 3.3 为什么 sin/cos

类比 Transformer 位置编码，多频率 sin/cos 提供：
- **低频分量**：编码轨道面的粗略方位（第几面）
- **高频分量**：编码面内精细位置
- **连续性**：相邻卫星的 PE 相似，远距离卫星的 PE 差异大

替代方案对比：

| 方案 | 问题 |
|------|------|
| 可学习嵌入表 | 需要固定词表大小，无法泛化到未见过的 $N$ |
| one-hot $(p, k)$ | 维度随 $P, S$ 变化，不可泛化 |
| 纯 $(p/P, k/S)$ | 无多尺度频率表达能力 |
| **sin/cos（采用）** | **固定维度、连续、多频率、规模无关** |

---

## 4. GAT 消息传递

### 4.1 模型架构

采用 Graph Attention Network（GAT）作为骨干编码器，3 层，隐层维度 $h = 128$，4 头注意力。

**第 $l$ 层更新**：

$$\mathbf{h}_u^{(l+1)} = \text{ELU}\left( \bigg\|_{m=1}^{M} \sum_{v \in \mathcal{N}(u)} \alpha_{uv}^{(m)} \mathbf{W}^{(m)} \mathbf{h}_v^{(l)} \right)$$

其中 $\|$ 表示多头拼接，$M = 4$ 为头数，每头输出维度 $h/M = 32$。

**注意力系数**（含边特征）：

$$\alpha_{uv} = \frac{\exp(\text{LeakyReLU}(\mathbf{a}^\top [\mathbf{W}\mathbf{h}_u \| \mathbf{W}\mathbf{h}_v \| \mathbf{W}_e \mathbf{e}_{uv}]))}{\sum_{w \in \mathcal{N}(u)} \exp(\text{LeakyReLU}(\mathbf{a}^\top [\mathbf{W}\mathbf{h}_w \| \mathbf{W}\mathbf{h}_v \| \mathbf{W}_e \mathbf{e}_{uw}]))}$$

边特征 $\mathbf{e}_{uv} = [\delta_{\text{delay}}, d]$ 通过独立的边变换矩阵 $\mathbf{W}_e$ 参与注意力计算（PyG `GATConv` 的 `edge_dim` 参数）。

### 4.2 方向预测头

GAT 编码后，通过两层 MLP 将节点表示映射到 4 个 ISL 方向的 logits：

$$\mathbf{o}_u = \mathbf{W}_2 \cdot \text{ReLU}(\mathbf{W}_1 \cdot \mathbf{h}_u^{(L)})$$

其中 $\mathbf{o}_u \in \mathbb{R}^4$，对应 4 个方向：{轨内前向, 轨内后向, 轨间右, 轨间左}。

### 4.3 方向掩码

每个节点不一定有全部 4 个方向的邻居（ISL 断链时）。推理和训练时对不可用方向的 logit 置 $-\infty$：

$$\hat{o}_{u,d} = \begin{cases} o_{u,d} & \text{if direction } d \text{ has active ISL} \\ -\infty & \text{otherwise} \end{cases}$$

---

## 5. 训练策略

### 5.1 Phase 1: 监督预训练（Dijkstra labels）

**数据生成**：对每个 $(snapshot, destination)$ 对：
1. 构建 ISL 拓扑快照
2. 运行全对 Dijkstra，获得 $next\_hop$ 矩阵
3. 将 $next\_hop$ 映射为 4 方向标签（$0=$ 轨内前, $1=$ 轨内后, $2=$ 轨间右, $3=$ 轨间左）
4. 节点 $u$ 到目的 $d$ 的标签 = Dijkstra 最短路的第一跳所在方向

**训练细节**：
- 损失函数：交叉熵（仅计算有有效标签且至少有一个可用方向的节点）
- 优化器：Adam, $\text{lr} = 10^{-3}$
- 训练轮次：150 epochs
- 批大小：64
- 每个训练配置 20 个快照 $\times$ $N$ 个目的地 = 每配置 $20N$ 个样本
- 三配置混合：总计 $20 \times 66 + 20 \times 100 + 20 \times 200 = 7320$ 个样本

**训练结果**（D018）：
- 训练集平均方向精度：97.6%
- 目标 720 星方向精度：66.8%
- Retention（目标 / 训练）：71%

### 5.2 PPO 微调的失败分析（D021）

实验验证了 PPO 微调在两个 reward 方案下均无效：

**方案 1：贪心 reward**（逐跳方向 → 路径 stretch）
- 失败原因：reward 太稀疏——99% 路径失败（贪心成功率仅 1.7%-30%），几乎无正梯度信号

**方案 2：加权 Dijkstra reward**（GNN 构造权重 → Dijkstra stretch）
- 失败原因：action-reward 解耦——改变单个节点的 logits 对整条 Dijkstra 路径的 stretch 影响极小，PPO 无法建立因果关联

**结论**：监督预训练后的 GNN logits 已足够好（加权 Dijkstra 成功率 100%），PPO 无法在监督基础上提供增量改善。最终方案不使用 PPO 微调。

### 5.3 多尺度混合训练策略

训练数据混合三种规模的星座快照（66/100/200 星），每个 batch 随机采样自不同配置。

**关键作用**：
- 让 GAT 学到规模无关的注意力模式——不同 $(P, S)$ 下同一归一化位置应有相似的方向偏好
- 消融实验（D027）表明多尺度训练贡献 stretch -2.3pp, $\leq 1.2\times$ 比例 +4pp，delay 开销 -2.4pp
- 贡献幅度（2-4pp）小于 Contract 预期（5-8pp），但方向符合预期

---

## 6. 加权 Dijkstra 推理

### 6.1 权重公式

GNN 输出每节点 4 个方向的 logits $\mathbf{o}_u \in \mathbb{R}^4$。推理时，将 logits 转化为边权重，运行 Dijkstra 最短路：

$$w(u, v) = \delta_{\text{delay}}(u, v) + \text{relu}\big(\max_d\ o_{u,d} - o_{u, \text{dir}(u,v)}\big)$$

其中 $\text{dir}(u,v)$ 为边 $(u,v)$ 对应的 ISL 方向索引。

**直觉**：
- 若边 $(u,v)$ 沿 GNN 推荐方向（$\text{logit} = \max$），惩罚项为 0，权重 = 纯时延
- 若边偏离推荐方向，惩罚项 = logit 差值，权重增大，Dijkstra 倾向避开
- relu 确保惩罚非负，不会出现负权重

### 6.2 与纯贪心对比

| 指标 | 纯贪心（逐 hop argmax） | 加权 Dijkstra |
|------|-------------------------|---------------|
| 路径成功率（train） | 22-30% | **100%** |
| 路径成功率（target 720） | 1.7% | **100%** |
| 根因 | 逐跳精度之积衰减（$0.976^{10} \approx 78\%$ 理论上限），低精度节点进一步拉低 | 全局优化，单跳错误可被后续路径修正 |
| mean stretch | N/A（大量失败） | 1.097 |
| $\leq 1.2\times$ optimal | N/A | 85.1% |
| $\leq 1.5\times$ optimal | N/A | 98.9% |

> 数据来源：720 星评估，10 snapshots $\times$ 5 TMs $\times$ 100 flows, seed=123（D023）

### 6.3 为什么选择此策略

加权 Dijkstra 在 GNN logits 质量足够好时（方向精度 >60%），将局部偏好全局化为最优路径。它不要求每跳都正确，而是通过惩罚不推荐方向来"软引导"Dijkstra。这比纯贪心鲁棒得多，且计算开销仅为一次 $O(E \log N)$ 的 Dijkstra。

---

## 7. 设计决策记录

| 决策 | 选择 | 理由 | 排除的替代方案 |
|------|------|------|----------------|
| D012 | Orbital PE + 多尺度训练 | 归一化坐标编码天然规模无关；多尺度增强泛化 | 可学习嵌入（不可跨规模）、one-hot（维度变化） |
| D015 | ISL 带宽 $B = 1$ GHz | L03 DuJo 基于 Starlink TLE 数据确认 | $B = 500$ MHz（无文献出处） |
| D016 | 实时轨道力学距离 + 5000 km 断链 | 四配置 ISL 距离差异巨大（1086-5694 km），固定值不适用 | 固定距离（错误，不适用任何配置） |
| D017 | ISL 类型为激光 | L02/L03 确认 optical laser link 1550 nm | RF ISL（与文献不符） |
| D019 | 不使用贪心推理 | 成功率极低（1.7%-30%），逐跳误差累积 | 逐跳 argmax（失败率过高） |
| D020 | 加权 Dijkstra | 成功率 100%，stretch 1.097，计算可行 | 纯贪心、beam search |
| D021 | 不使用 PPO 微调 | reward 太稀疏或 action-reward 解耦，80 轮无改善 | PPO fine-tuning（无效） |
| D022 | neighbor_map 双向注册 | 修复前只注册单方向，评估缺失 2/4 方向 | 单向映射（bug） |

---

## 8. 参数量分解

### 核心模型（RoutingActorCritic）

| 模块 | 参数量 | 计算 |
|------|--------|------|
| GAT Layer 1 | $33 \times 32 \times 4 + 32 \times 4 = 4,352$ | node_dim=33 → h/M=32, heads=4 |
| GAT Layer 2 | $128 \times 32 \times 4 + 32 \times 4 = 16,512$ | h=128 → h/M=32, heads=4 |
| GAT Layer 3 | $128 \times 32 \times 4 + 32 \times 4 = 16,512$ | h=128 → h/M=32, heads=4 |
| Edge transform (per layer) | $2 \times 32 \times 4 \times 3 = 768$ | edge_dim=2, shared per layer |
| Actor head | $128 \times 128 + 128 + 128 \times 4 + 4 = 16,516$ | FC(128→128→4) |
| Critic head | $128 \times 128 + 128 + 128 \times 1 + 1 = 16{,}513$ | FC(128→128→1) |
| **总计** | **72,965** | |

> 精确参数量由 `sum(p.numel() for p in model.parameters())` 给出，含 bias 项。

### GRLR Baseline 对比

| 模块 | GRLR | Ours |
|------|------|------|
| 输入维度 | node=3, edge=2 | node=33, edge=2 |
| GAT 层数 | 1 (Actor) + 1 (Critic), 独立 | 3 共享 |
| 隐层维度 | actor=64, critic=32 | 128 |
| 注意力头 | 1 | 4 |
| 感受野 | 6 节点局部图 | 全局图 |
| 位置编码 | 无 | Orbital PE (16 dim) |
| 参数量级 | ~5K | 72,965 |
| 训练方式 | PPO (RL) | 监督 (Dijkstra labels) |
| 推理方式 | 加权 Dijkstra | 加权 Dijkstra |

参数量差异的合理性：GRLR 每次决策只看 6 节点局部图，信息量低，无需大模型；我们的模型处理全图（66-200 节点），需要更大容量学习全局路由模式。

---

## 9. 训练不稳定风险缓解

### 9.1 方向掩码防止非法输出

训练和推理时，对不可用方向（ISL 断链）的 logit 置 $-\infty$，softmax 后概率为 0。这防止模型输出非法动作，也避免 cross entropy 对不存在的类别产生梯度。

### 9.2 标签过滤

Dijkstra 标签中，$u = d$（源 = 目的）或 next_hop 不存在的节点标签为 $-1$。训练时跳过这些节点，仅对有效标签计算 loss：

$$\mathcal{L} = \frac{1}{|\mathcal{V}_{\text{valid}}|} \sum_{u \in \mathcal{V}_{\text{valid}}} \text{CE}(\hat{\mathbf{o}}_u, y_u)$$

### 9.3 多尺度数据平衡

三配置混合后，大配置贡献更多样本（$20 \times 200 = 4000$ vs $20 \times 66 = 1320$），DataLoader 的 shuffle 保证每 batch 内配置分布相对均匀。

---

## 10. 与 Baseline 的代码复用关系

| 组件 | 共享代码 | 差异 |
|------|----------|------|
| Walker-Delta 星座 | `constellation.py` | 完全共享 |
| ISL 拓扑 | `topology.py` | 完全共享 |
| 信道模型 | `channel.py` | 完全共享 |
| 快照构建 | `snapshot.py` | 完全共享 |
| Dijkstra | `routing.py` | 完全共享 |
| 加权 Dijkstra 推理 | `env.py::evaluate_weighted()` | 完全共享 |
| GNN 模型 | 独立 | 我们: `RoutingActorCritic` (3层GAT, h=128); GRLR: `GRLRModel` (1层GAT, h=64) |
| 训练 | 独立 | 我们: `pretrain.py` (监督); GRLR: `grlr_train.py` (PPO) |
| 图构建 | 独立 | 我们: 全图 PyG Data; GRLR: 6 节点局部图 `build_local_graphs()` |

共享底层组件确保对比实验中星座、拓扑、信道、路由算法完全一致，差异仅来自 GNN 编码器和训练策略。
