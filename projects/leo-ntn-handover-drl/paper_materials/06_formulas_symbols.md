# 公式汇总与符号约定

> 跨章节共享的公式和符号定义。供大纲阶段确定术语约定和公式呈现决策。

---

## 1. 奖励函数

每个决策步 $t$ 的即时奖励：

$$r_t = w_r \cdot R_{norm} + w_l \cdot L_{norm} - w_b \cdot B - w_h \cdot H$$

| 项 | 符号 | 含义 | 范围 |
|----|------|------|------|
| 归一化速率 | $R_{norm}$ | $\log_2(1 + \text{SINR}) / \log_2(1 + \text{SINR}_{max})$ | [0, 1] |
| 归一化剩余容量 | $L_{norm}$ | 卫星剩余可用信道 / 总信道数 | [0, 1] |
| 阻塞惩罚 | $B$ | 被 capacity 拒绝的 UE 数量 | $\geq 0$ |
| 切换惩罚 | $H$ | 发生切换的 UE 数量 | $\geq 0$ |
| 权重 | $w_r, w_l, w_b, w_h$ | 各项权重系数 | — |

来源：contract.md §Simulation Config。

MDP Checkpoint 验证：无单一项占 >95%（最大项 60.9%），策略区分度 120%。来源：baseline_report §1.2。

---

## 2. MPNN-E 消息传递公式

二部图双向传递，每层分两步。

### Step 1: UE → Sat

消息函数（边条件化）：

$$m_{ue_i \to sat_j} = \text{MLP}_{msg}^{ue}([h_{ue_i} \ \| \ h_{sat_j} \ \| \ e_{ij}])$$

更新函数（聚合 + 残差 + LayerNorm）：

$$\tilde{h}_{sat_j} = \text{MLP}_{upd}^{sat}\left([h_{sat_j} \ \| \ \text{mean}\{m_{ue \to sat_j}\}]\right)$$

$$h_{sat_j}' = \text{LayerNorm}(h_{sat_j} + \tilde{h}_{sat_j})$$

### Step 2: Sat → UE

消息函数：

$$m_{sat_j \to ue_i} = \text{MLP}_{msg}^{sat}([h_{sat_j}' \ \| \ h_{ue_i} \ \| \ e_{ij}])$$

更新函数：

$$\tilde{h}_{ue_i} = \text{MLP}_{upd}^{ue}\left([h_{ue_i} \ \| \ \text{mean}\{m_{sat \to ue_i}\}]\right)$$

$$h_{ue_i}' = \text{LayerNorm}(h_{ue_i} + \tilde{h}_{ue_i})$$

T=2 层：重复 Step 1 + Step 2 共 2 次。

来源：design_C.md §3.3；来源：D010（选择 MPNN-E）、D013（T=2）。

---

## 3. 分解式 Dueling Q 函数

标准 Dueling DDQN 输出 $|A|$ 个 Q 值（$|A|=396$），输出层巨大。方案 C 采用分解式：

$$Q(UE_i, sat_j) = V(h_{ue_i}) + A(h_{ue_i}, h_{sat_j}, h_{edge_{ij}}) - \frac{1}{|J_i|}\sum_{j \in J_i} A(h_{ue_i}, h_{sat_j}, h_{edge_{ij}})$$

其中：
- $V(h_{ue_i}) = \text{MLP}_v(h_{ue_i}) \to \mathbb{R}$：状态价值，仅依赖 UE 嵌入
- $A(h_{ue_i}, h_{sat_j}, h_{edge_{ij}}) = \text{MLP}_a([h_{ue_i} \| h_{sat_j} \| h_{edge_{ij}}]) \to \mathbb{R}$：卫星选择优势
- $J_i$：UE $i$ 的可见候选卫星集合

来源：design_C.md §4.1；来源：D011（选定分解式 Q）。

---

## 4. top-K 候选压缩

对每个 UE，按综合评分选择前 K=6 颗候选卫星：

$$\text{score}_m = \text{elev\_norm}(m)$$

按 $\text{score}_m$ 降序排列，取前 $K=6$ 个。不足 $K$ 个时用 dummy 边填充（特征全零）。

效果：
- 候选集从 396 降至 $\leq 6$，动作空间从 396 维降至 $\leq 7$ 维
- 仿真器统计：平均 4.4 颗可见卫星，K=6 零信息损失

来源：design_C.md §2.2；来源：D012（K=6 选择）。

---

## 5. 预训练辅助损失

GNN 预训练使用两个辅助任务的加权和：

$$\mathcal{L}_{aux} = \text{BCE}(\hat{b}_i, b_i) + \text{MSE}(\hat{\Delta l}_j, \Delta l_j)$$

其中：
- $\hat{b}_i$：GNN 预测的 UE $i$ 下一步阻塞状态（二分类）
- $b_i$：实际阻塞状态
- $\hat{\Delta l}_j$：GNN 预测的卫星 $j$ 下一步负载变化（回归）
- $\Delta l_j$：实际负载变化

来源：design_C.md §5.1；来源：D013（两阶段训练策略）。

---

## 6. 维度设计表

### GNN 消息传递 MLP

| MLP | 输入维度 | 隐层维度 | 输出维度 | 参数量 |
|-----|---------|---------|---------|--------|
| $\text{MLP}_{msg}^{ue}$ | 4+2+3=9 | 32 | 32 | ~320 |
| $\text{MLP}_{upd}^{sat}$ | 2+32=34 | 32 | 2 | ~1,152 |
| $\text{MLP}_{msg}^{sat}$ | 2+4+3=9 | 32 | 32 | ~320 |
| $\text{MLP}_{upd}^{ue}$ | 4+32=36 | 32 | 4 | ~1,188 |

残差投影到 d=64（可选增强）：$h' = \text{LayerNorm}(\text{MLP}_{proj}(h) + \text{MLP}_{upd}(\text{AGG}(\text{messages})))$

来源：design_C.md §3.4。

### Dueling Q 网络

| 网络 | 输入维度 | 隐层维度 | 输出维度 | 参数量 |
|------|---------|---------|---------|--------|
| $\text{MLP}_v$ | 64 | 64 | 1 | ~4K |
| $\text{MLP}_a$ | 64+64+32=160 | 64 | 1 | ~10K |

来源：design_C.md §4.3。

### 总参数量对比

| 网络 | 参数量 | 说明 |
|------|--------|------|
| B2 DDQN (flat 396-action) | ~490K | 1585×256 + 256×128 + 128×396（含偏置 = 490,125） |
| C GNN Encoder | 13,120 | 4 个小 MLP + LayerNorm（源码实测） |
| C Dueling Q | 12,738 | MLP_v + MLP_a（源码实测） |
| **C 总计** | **25,858** | **比 B2 少 19×** |

来源：design_C.md §4.3。

---

## 7. 符号约定表

| 符号 | 含义 | 范围/单位 | 首现章节 | 备注 |
|------|------|----------|---------|------|
| $N$ | UE 数量 | — | 系统模型 | 跨章统一为 $N_{\text{UE}}$ |
| $K$ | top-K 候选数 | K=6 | 方法-topK | |
| $T$ | GNN 消息传递层数 | T=2 | 方法-GNN | 跨章统一为 $L$ |
| $G_t$ | 时刻 $t$ 的动态二部图 | — | 方法-图定义 | |
| $V_{ue}$ | UE 节点集合 | — | 方法-图定义 | 跨章统一为 $\mathcal{V}_{\text{UE}}$ |
| $V_{sat}$ | 候选卫星节点集合 | — | 方法-图定义 | 跨章统一为 $\mathcal{V}_{\text{sat}}$ |
| $E$ | UE-卫星可见边集合 | — | 方法-图定义 | 跨章统一为 $\mathcal{E}$ |
| $h_{ue_i}$ | UE $i$ 的节点嵌入 | $\mathbb{R}^{64}$ | 方法-GNN | |
| $h_{sat_j}$ | 卫星 $j$ 的节点嵌入 | $\mathbb{R}^{64}$ | 方法-GNN | |
| $e_{ij}$ | UE $i$ 与卫星 $j$ 的边特征 | $\mathbb{R}^3$ | 方法-图定义 | |
| $h_{edge_{ij}}$ | 边嵌入 | $\mathbb{R}^{32}$ | 方法-GNN | |
| $Q(i,j)$ | UE $i$ 选择卫星 $j$ 的 Q 值 | $\mathbb{R}$ | 方法-Dueling Q | |
| $V(h_{ue})$ | 状态价值函数 | $\mathbb{R}$ | 方法-Dueling Q | |
| $A(i,j)$ | 卫星选择优势函数 | $\mathbb{R}$ | 方法-Dueling Q | |
| $\gamma$ | 折扣因子 | 0.99 | 方法-训练 | |
| $\varepsilon$ | 探索率 | 0.5→0.05 | 方法-训练 | |
| $R_{norm}$ | 归一化速率 | [0, 1] | 系统模型 | |
| $L_{norm}$ | 归一化剩余容量 | [0, 1] | 系统模型 | |
| $B$ | 阻塞 UE 数 | $\geq 0$ | 系统模型 | 跨章统一为 $N_{\text{blk}}$ 以避免与带宽混淆 |
| $H$ | 切换 UE 数 | $\geq 0$ | 系统模型 | 跨章统一为 $N_{\text{ho}}$ 以避免与高度混淆 |
| $\text{SINR}$ | 信干噪比 | dB | 系统模型 | |
| $\text{SINR}_{max}$ | 最大 SINR（归一化基准） | dB | 系统模型 | |

来源：contract.md, design_C.md。

---

## 8. 跨章术语消歧

| 术语 | 本章含义 | Ch1 含义 | 备注 |
|------|---------|---------|------|
| retention | 迁移奖励比（跨规模部署 reward / 同规模 reward），值域约 100%~400% | 时延保留率（delay_same / delay_cross），值域接近 1.0 | 本章不使用"时延保留率"语义；为避免混淆，正文中首次出现时标注"本章 retention 指迁移奖励比" |
