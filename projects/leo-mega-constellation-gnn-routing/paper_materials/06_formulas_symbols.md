# 公式汇总与符号约定

> 跨章节共享的公式和符号定义。供大纲阶段确定术语约定和公式呈现决策。

---

## 1. Walker-Delta 星座轨道力学

卫星索引与 ECI 坐标：

$$\text{idx} = p \cdot S + k, \quad p \in [0, P),\ k \in [0, S)$$

$$\mathbf{r}(t) = r \begin{pmatrix} \cos\Omega_p \cos u - \sin\Omega_p \sin u \cos i \\ \sin\Omega_p \cos u + \cos\Omega_p \sin u \cos i \\ \sin u \sin i \end{pmatrix}$$

其中 $r = R_\oplus + h$，$\Omega_p = 2\pi p / P$，$u_{p,k}(t) = u_0^{p,k} + nt$，$n = 2\pi/T_{\text{orb}}$，$T_{\text{orb}} = 2\pi\sqrt{r^3/\mu}$。

来源：contract.md §Simulation Config。

---

## 2. ISL 信道模型

ISL 距离（实时计算）：

$$d_{u,v}(t) = \|\mathbf{r}_u(t) - \mathbf{r}_v(t)\|_2$$

Shannon 容量（简化近似）：

$$C = B \cdot \log_2(1 + \text{SNR}(d))$$

$$\text{SNR}(d) = \text{SNR}_{\text{ref}} \cdot \left(\frac{d_{\text{ref}}}{d}\right)^2$$

断链条件：$d_{u,v}(t) > d_{\max} = 5000\ \text{km}$ 时 ISL 断开。

来源：D015 (B=1GHz), D016 (实时距离+断链), D017 (激光链路)。

---

## 3. Orbital Positional Encoding

$$\text{PE}(p, k; P, S) = \big[\ \sin(f_i \cdot p/P),\ \cos(f_i \cdot p/P),\ \sin(f_i \cdot k/S),\ \cos(f_i \cdot k/S)\ \big]_{i=0}^{n_{\text{freq}}-1}$$

频率 $f_i = 2^i \cdot 2\pi$，$n_{\text{freq}} = d_{\text{PE}}/4$，输出维度 $d_{\text{PE}} = 16$。

节点 $u$ 的输入特征：

$$\mathbf{x}_u = [\ \mathbb{1}[\text{is\_dest}_u]\ \|\ \text{PE}_{\text{own}}(p_u, k_u)\ \|\ \text{PE}_{\text{dest}}(p_d, k_d)\ ] \in \mathbb{R}^{33}$$

边 $(u,v)$ 的特征：

$$\mathbf{e}_{uv} = [\ \delta_{\text{delay}}(u,v),\ d(u,v)\ ] \in \mathbb{R}^{2}$$

来源：contract.md §GNN+RL 配置; D012。

---

## 4. GAT 消息传递

第 $l$ 层更新（4 头注意力，含边特征）：

$$\mathbf{h}_u^{(l+1)} = \text{ELU}\left( \bigg\|_{m=1}^{M} \sum_{v \in \mathcal{N}(u)} \alpha_{uv}^{(m)} \mathbf{W}^{(m)} \mathbf{h}_v^{(l)} \right)$$

注意力系数（边条件化）：

$$\alpha_{uv} = \frac{\exp(\text{LeakyReLU}(\mathbf{a}^\top [\mathbf{W}\mathbf{h}_u \| \mathbf{W}\mathbf{h}_v \| \mathbf{W}_e \mathbf{e}_{uv}]))}{\sum_{w \in \mathcal{N}(u)} \exp(\text{LeakyReLU}(\mathbf{a}^\top [\mathbf{W}\mathbf{h}_w \| \mathbf{W}\mathbf{h}_v \| \mathbf{W}_e \mathbf{e}_{uw}]))}$$

方向预测头（两层 MLP）：

$$\mathbf{o}_u = \mathbf{W}_2 \cdot \text{ReLU}(\mathbf{W}_1 \cdot \mathbf{h}_u^{(L)}) \in \mathbb{R}^4$$

方向掩码（ISL 断链时）：

$$\hat{o}_{u,d} = \begin{cases} o_{u,d} & \text{if direction } d \text{ has active ISL} \\ -\infty & \text{otherwise} \end{cases}$$

来源：models.py (RoutingActorCritic); D022 (neighbor_map)。

---

## 5. 监督预训练损失

$$\mathcal{L} = \frac{1}{|\mathcal{V}_{\text{valid}}|} \sum_{u \in \mathcal{V}_{\text{valid}}} \text{CE}(\hat{\mathbf{o}}_u, y_u)$$

其中 $y_u$ 为 Dijkstra 最短路的第一跳方向标签（4 类），$\mathcal{V}_{\text{valid}}$ 排除源=目的和无有效标签的节点。

来源：D018 (监督预训练); pretrain.py。

---

## 6. 加权 Dijkstra 推理

$$w(u, v) = \delta_{\text{delay}}(u, v) + \text{relu}\big(\max_d\ o_{u,d} - o_{u, \text{dir}(u,v)}\big)$$

- $\delta_{\text{delay}}(u,v)$：ISL 传播时延（ms）
- $\max_d\ o_{u,d}$：GNN 推荐方向的 logit（最大值）
- $o_{u,\text{dir}(u,v)}$：边 $(u,v)$ 对应方向的 logit
- 惩罚项 = 推荐方向与实际方向的 logit 差

来源：D020 (加权Dijkstra); D023 (评估结果)。

---

## 7. 评估指标

### Stretch（路径最优性比）

$$\text{stretch}_p = \frac{\text{delay}_p}{\text{delay}_p^*}$$

其中 $\text{delay}_p^*$ 为 Dijkstra 最短路径时延。

### 时延保留率

$$\text{retention} = \frac{\text{delay}_{\text{GRLR, same-scale}}}{\text{delay}_{\text{ours, cross-scale}}}$$

来源：contract.md §Metrics (M4)。

---

## 8. 维度设计表

### GNN 编码器

| 层/模块 | 输入维度 | 隐层维度 | 输出维度 | 参数量 |
|---------|---------|---------|---------|--------|
| GAT Layer 1 | node=33, edge=2 | 32×4 heads | 128 | ~4.4K |
| GAT Layer 2 | 128 | 32×4 | 128 | ~16.5K |
| GAT Layer 3 | 128 | 32×4 | 128 | ~16.5K |
| Edge transform | 2 | 32×4 | — | ~0.8K/layer |
| Actor head (方向预测) | 128 | 128 | 4 | ~16.5K |
| Critic head | 128 | 128 | 1 | ~16.5K |
| **总计** | | | | **~71K** |

### vs GRLR Baseline

| 模块 | GRLR | Ours |
|------|------|------|
| 输入维度 | node=3, edge=2 | node=33, edge=2 |
| GAT 层数 | 1+1 (独立) | 3 (共享) |
| 隐层维度 | 64/32 | 128 |
| 注意力头 | 1 | 4 |
| 感受野 | 6 节点局部图 | 全局图 |
| 位置编码 | 无 | Orbital PE (16 dim) |
| **参数量** | **~5K** | **~71K** |

来源：models.py; grlr_model.py; D024 (GRLR复现)。

---

## 9. 符号约定表

| 符号 | 含义 | 范围/单位 | 首现章节 |
|------|------|----------|---------|
| $N$ | 卫星总数 | — | 系统模型 |
| $P$ | 轨道面数 | — | 系统模型 |
| $S$ | 每面卫星数 | — | 系统模型 |
| $h$ | 轨道高度 | 550 km | 系统模型 |
| $i$ | 轨道倾角 | 53° | 系统模型 |
| $F$ | Walker 相位因子 | 1 | 系统模型 |
| $(p, k)$ | 卫星轨道位置 | $p \in [0,P),\ k \in [0,S)$ | 系统模型 |
| $d_{\max}$ | ISL 断链阈值 | 5000 km | 系统模型 |
| $B$ | ISL 带宽 | 1 GHz | 系统模型 |
| $\delta_{\text{delay}}$ | ISL 传播时延 | ms | 系统模型 |
| $d_{u,v}$ | ISL 几何距离 | km | 系统模型 |
| $\text{PE}(p,k)$ | Orbital 位置编码 | $\mathbb{R}^{16}$ | 方法-PE |
| $d_{\text{PE}}$ | PE 输出维度 | 16 | 方法-PE |
| $n_{\text{freq}}$ | PE 频率数 | 4 | 方法-PE |
| $\mathbf{x}_u$ | 节点 $u$ 输入特征 | $\mathbb{R}^{33}$ | 方法-特征 |
| $\mathbf{e}_{uv}$ | 边 $(u,v)$ 特征 | $\mathbb{R}^{2}$ | 方法-特征 |
| $\mathbf{h}_u^{(l)}$ | 节点 $u$ 第 $l$ 层嵌入 | $\mathbb{R}^{128}$ | 方法-GAT |
| $M$ | 注意力头数 | 4 | 方法-GAT |
| $L$ | GAT 层数 | 3 | 方法-GAT |
| $\alpha_{uv}$ | 注意力系数 | $[0,1]$ | 方法-GAT |
| $\mathbf{o}_u$ | 方向 logits | $\mathbb{R}^4$ | 方法-预测头 |
| $y_u$ | 方向标签 | $\{0,1,2,3\}$ | 方法-训练 |
| $\mathcal{V}_{\text{valid}}$ | 有效标签节点集 | — | 方法-训练 |
| $w(u,v)$ | 加权 Dijkstra 边权 | ms | 方法-推理 |
| $\text{stretch}_p$ | 路径最优性比 | $\geq 1.0$ | 实验评估 |
| $\text{delay}_p^*$ | Dijkstra 最优路径时延 | ms | 实验评估 |
| retention | 时延保留率 | $[0,1]$ | 实验评估 |

来源：contract.md; models.py; config.py。
