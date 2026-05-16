# 方向可行性报告

## 研究方向
GNN encoder + QMIX/QPLEX 多 agent 强化学习，替代 MA-DRL 中的 FC encoder，实现可扩展、可泛化的 LEO 多波束卫星 BH 调度。

## Pivot 记录
- **v1 (已放弃)**: GNN 策略网络 + REINFORCE/PPO + top-K 动作空间 → MVE v1-v3 全败，前一轮项目 D011/D013 证伪
- **v2 (当前)**: MA-DRL + GNN encoder + QMIX mixing + per-cell binary action → 对齐成功论文范式（L05/L06）

---

## A0. 问题-方法适配性预检

### A0.1 性能间隙

| 场景 | 当前最优 | 理论/实际差距 | 来源 |
|------|---------|-------------|------|
| ≤37小区 | MA-DRL (QMIX/QPLEX) | 比贪心提升 16-73%，但 MCTS 仍优 20%+ | L05, L06, L07 |
| >40小区 | MA-DRL **不收敛** | 无法使用，MCTS 延迟 159s | L01 Tyche JSAC |
| 127小区 | MCTS (非实时) | 比 GA 提升 20.85%，比贪心提升 81.97%，但计算 159s | L01 |
| 功率分配(参考) | EPA/WMMSE | GNN 比传统方法高 20-30%，接近理论上界 | L03 Meta-GNN |

**结论**：在实时可用方法（MA-DRL/贪心）与最优方法（MCTS）之间存在 ≥30% 性能间隙。大场景下间隙更大（>80%）。**通过**。

### A0.2 问题结构适配

| ML 擅长特性 | BH 问题是否具备 | 证据 |
|-------------|----------------|------|
| 大状态空间，精确优化不可行 | ✓ C(N,K) 组合爆炸 | N=127, K=32 → 天文数字 |
| 环境动态复杂 | ✓ LEO 拓扑时变 + 流量随机 | L02 GRU 动态演化, L05 复合 Poisson |
| 跨场景泛化 | ✓ 不同流量分布、星座配置 | L03 meta-learning 验证 |
| 延迟奖励/长期依赖 | ✓ BH 决策影响未来队列状态 | L06 TTL=40, L07 多时隙缓冲 |

4/4 特性全部满足。**通过**。

### A0.3 跨域成功先例

| 先例论文 | 方法 | 领域 | 成果 |
|----------|------|------|------|
| L02 DynHGNN (TWC 2025) | HGNN + GRU | LEO 下行干扰管理 | 比 GCN/HGNN 最大提升 130Mbps |
| L03 Meta-GNN (TVT 2024) | MPNN + meta-learning | LEO 功率分配 | 比传统方法高 20-30%，接近上界 |
| REGNN (2020, 380cit) | 随机边 GNN | 无线资源分配 | 可扩展，参数不随网络规模增长 |
| GNN scalable RRM (2020, 461cit) | GNN 架构设计 | 无线电资源管理 | 理论可扩展性证明 |

≥4 篇强先例，方法-问题匹配有坚实经验支撑。**通过**。

### A0.4 MDP 非平凡性

- **S**: 队列状态 (N×T 维) + CSI + 干扰拓扑 + 流量需求 → N=37 时队列维 370, N=648 时数千维
- **A**: 离散组合 — 选 K 个小区照亮 (C(N,K) 或 N 维 per-cell binary)
- **R**: 吞吐量 - 延迟惩罚 - 负载不均衡 (每时隙稠密奖励)
- **P**: LEO 动态拓扑 + 随机流量

**最优策略非平凡**：不能简单取队列最大 K 个小区（贪心），因为相邻小区同时照亮会导致同频干扰。L06 专门设计了"空间隔离 BH pattern"，L07 用 per-cell Q-value + top-Nb 降维。这证明空间隔离约束使问题非平凡。**通过**。

### A0.5 负面证据搜索

| 搜索发现 | 分析 |
|----------|------|
| L01 Tyche: MA-DRL >40小区失败 | 根因是**独立 agent 假设**（无图结构），GNN 正是解决此问题 |
| M14 (AIAC 2024): 异构图+DRL 做 BH | 正面信号（有人尝试且可行），但仅会议论文、1cit |
| 未发现"GNN for BH 失败"报告 | 空白原因：MA-DRL 研究者聚焦算法变体（MAPPO/QPLEX），GNN 研究者聚焦连续问题（功率/信道） |

空白原因为 **"没人想到"** + **"技术壁垒刚解除"**（GNN+离散RL 组合近 2 年才成熟）。可解释且风险可控。**通过**。

### A0 结论：5/5 全部通过，无致命信号。继续维度 A/B。

---

## A. 结构优势论证

### GNN encoder vs FC encoder in QMIX framework

> [FR-08] 方法论对齐：top-3 成功 BH 论文（L05 QPLEX, L06 QMIX, L07 MAPPO）均用 Q-learning 系 + per-cell binary action。本方案跟随此范式，仅替换 encoder 从 FC → GNN。

**1. 空间干扰建模的信息损失**

BH 的核心约束是空间隔离：同时照亮的相邻小区产生同频干扰。在 QMIX 框架中：
- **FC encoder**：每个 agent 只看自己的 (queue, ttl, csi) → Q_i(a_i) 基于纯局部信息
- **GNN encoder**：通过 L 层消息传递聚合邻居状态 → Q_i(a_i) 包含 L-hop 干扰感知

关键区别：QMIX 的 mixing network 能做全局信用分配，但**不能弥补 agent 输入端的信息损失**。如果 agent 看不到邻居是否被照亮、邻居的队列积压，mixing network 也无法推断干扰拓扑。

**2. QMIX 保留的优势 + GNN 补充的能力**

| 能力 | FC+QMIX | GNN+QMIX |
|------|---------|----------|
| 全局信用分配 | ✅ mixing network | ✅ 同 |
| 局部决策 | 只看自己 | L-hop 邻居聚合 |
| 空间隔离感知 | ❌ 隐式（需 mixing 推断） | ✅ 显式（消息传递） |
| 可扩展性 | 需重训（agent 数=小区数） | 直接部署（参数共享） |
| 泛化到新规模 | 差（L01: >40 小区失败） | 强（L03: 19→61 zero-shot） |

**3. 实证证据**

- IA-Greedy >> Greedy 50%（MVE v3）：**干扰拓扑感知带来巨大增益**
- L02 DynHGNN：超图干扰建模比 GCN 提升 130Mbps（卫星干扰管理）
- L03 Meta-GNN：GNN 参数共享实现 19→61 小区 zero-shot 部署，FNN 崩溃
- QMIX-GNN (2025, 6cit)：GNN+QMIX 组合在通用 MARL 已验证可行
- TapFinger (2023, 58cit)：GNN+MARL 调度任务在通信领域已成熟

**4. 为什么这次不同于前一轮失败**

前一轮用 GNN 策略网络 + REINFORCE/PPO + top-K 动作空间，失败根因（D011/D013）：
- top-K 不可微 → 梯度稀疏 → 信用分配失败
- REINFORCE 高方差 → 训练不稳定
- 单 agent 标量奖励 → 无法区分各小区贡献

新方案逐项修复：
- Per-cell binary action + Q-value 排序 → 标准 QMIX-BH 动作空间（L06 验证）
- QMIX mixing network → 信用分配（值分解 + 单调性约束）
- DQN 训练（replay buffer + target network）→ 稳定训练

---

## B. 新颖性-可行性解耦

### 新颖性论据（事实判断）

经 Step 1-3 + Step 3.5 + pivot 补充检索共 14 轮检索确认：

| 组合 | 竞品数 | 代表论文 | 领域 |
|------|--------|----------|------|
| GNN + QMIX | 3 篇（低引） | QMIX-GNN(2025,6cit), Graph-QMIX(2022,0cit), SVMIX(2023,4cit) | 游戏/交通，非通信 |
| GNN + QPLEX | **0** | — | — |
| GNN + MARL + 卫星 BH | **0** | 7 篇 MARL-BH 全用 MLP，无一用 GNN | — |
| GNN + MARL + 通信调度 | 成熟范式 | TapFinger(58cit), 综述(48cit), 11+ 篇 | 通信领域验证 |

**创新空白坚实**：在卫星 BH 具体应用场景下，GNN encoder + QMIX/QPLEX 为零竞品。

### 可行性论据（预测判断）

| 论据类型 | 内容 | 置信度 |
|----------|------|--------|
| 直接类比 | GNN+QMIX 在通用 MARL 已验证（QMIX-GNN 2025）| 高 |
| 领域迁移 | GNN+MARL 调度在通信领域成熟（TapFinger 58cit）| 高 |
| 结构相似 | BH 与功率分配共享干扰图结构（L02/L03 已验证）| 高 |
| 范式对齐 | 跟随 top-3 BH 论文的 Q-learning + per-cell action 范式 | 高 |
| 可扩展性 | GNN 参数共享（L03: 19→61 zero-shot）| 高 |

### 空白原因分析

| 可能原因 | 判断 | 证据 |
|----------|------|------|
| 没人想到 | **主要原因** | MA-DRL BH 研究者聚焦算法变体（QMIX/QPLEX/MAPPO 堆叠），未见讨论 GNN 替代 FC encoder |
| 技术限制刚解除 | **次要原因** | GNN+MARL 在通信领域 2023-2024 年才成熟，尚未扩散到卫星 BH 子领域 |
| 试过效果不好 | 无证据 | 前一轮失败（D011/D013）是 action space/训练方法问题，非 GNN 架构问题 |

**结论**：空白因"没人想到" + "技术壁垒刚解除"，最有利的空白类型。

---

## D. 最小可行实验（MVE）

### v1 MVE（GNN+REINFORCE，已失败）

见前版 feasibility_report，三版均 FAIL。关键遗留价值：IA-Greedy >> Greedy 50%，证明干扰拓扑感知有效。

### v2 MVE（GNN+QMIX，进行中）

**假设**: GNN encoder + QMIX mixing network 能捕获小区间干扰拓扑，在相同 QMIX 框架下产生优于 FC encoder 的 BH 调度决策。

**最小实例**: 19 小区六边形网格, K=3 波束, 同一干扰模型

**架构**:
- GNN+QMIX: 共享 GCN encoder(2层, h=32) → per-agent Q-head → QMIX mixing network
- FC+QMIX: 共享 MLP encoder(2层, h=32) → per-agent Q-head → 同一 mixer
- 关键隔离：mixer 完全相同，仅 encoder 不同

**动作空间**: per-cell binary (每个小区独立 on/off)，执行时选 Q-value 最大的 K 个小区

**训练**: 1000 episodes × 50 steps, replay buffer 10000, target network, ε-greedy 1.0→0.05

**pass/fail 标准**:
- **Pass**: GNN+QMIX throughput > FC+QMIX ≥5%, 且 GNN+QMIX > Greedy ≥10%
- **Conditional**: GNN+QMIX > FC+QMIX 但 <5%
- **Fail**: GNN+QMIX ≤ FC+QMIX

**结果** (2026-05-16):

| 方法 | Throughput | vs FC |
|------|-----------|-------|
| GNN+QMIX | 6.58 ±0.15 | -11.4% |
| FC+QMIX | 7.42 ±0.55 | baseline |
| Random | 7.63 | — |
| IA-Greedy | **10.38** | — |

**MVE Verdict**: FAIL — GNN+QMIX < FC+QMIX，且两者均 < Random

**根因**: QMIX mixer 已有全局状态输入，GNN encoder 的邻居信息冗余；空间隔离约束需显式执行（IA-Greedy），不能通过 RL+GNN 隐式学习。

---

## Go/No-Go 决策

- 决策：**Kill**
- 理由：
  1. v1 MVE (GNN+REINFORCE): FAIL × 3 版
  2. v2 MVE (GNN+QMIX): FAIL — GNN < FC < Random
  3. 前一轮项目 6 种方法全部失败（D011/D013）
  4. 累计：2 项目 × 4 算法 × 2 规模 = 一致失败
  5. 根因确认：空间隔离约束需显式执行，RL+GNN 无法隐式学习
- 教训已写入 code-quality.md: A3(更新), A5(新增), B1(更新), FR-09, FR-10
- 用户确认：✅ (2026-05-16)
