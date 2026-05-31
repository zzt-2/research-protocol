# Handoff: 方向侦察 Batch 4 完成 → Top 1 候选深度验证

> 来源: Batch 1-4 搜索 | 交接目标: 对卫星 IoT NTN 接入 + GNN 做深度可行性验证
> 文件名: HANDOFF-008-batch4-validation.md

## 已完成边界

### 搜索阶段（全部完成）

4 个批次共搜索 **57+ 角度**，**13 个候选**，**44+ 排除**。

**批次 4（本轮）结果**：M 类（无线/卫星非热门子领域）7 角度 + N 类（传统通信）3 角度：
- 新候选 3 个：工业无线 TSCH(#11)、卫星 IoT NTN 接入(#12)、NTN-TN 双连接切换(#13)
- 排除 7 个：水下声学、AoI、无线链路调度、网络节能、端到端自编码、非理想信道补偿、调制识别

### 候选池现状

**严格符合"无线/卫星"约束的候选（8 个）**：

| # | 方向 | 置信度 | 核心空白 |
|---|------|--------|---------|
| **12** | **卫星 IoT NTN 接入 + GNN** | **高** | GNN×NTN IoT=0篇，3GPP标准驱动 |
| **11** | **工业无线 TSCH + GNN/Meta-RL** | **中高** | TSCH+先进ML≈5篇，工业需求真实 |
| **13** | **NTN-TN 双连接切换 + GNN** | **中高** | GNN×NTN-TN=0篇，图结构天然匹配 |
| 2 | GNN+IoT mMTC 免授权调度 | 中高 | grant-free GNN≈0，但地面grant-free红海 |
| 8 | Meta-RL+AMC | 中 | 地面Meta+AMC≈0，复杂度偏低 |
| 9 | 课程学习+卫星路由 | 中低 | 与Ch1/Ch3重叠 |
| 10 | 离线RL+边缘计算卸载 | 中高 | MEC偏CS边界 |
| 3 | GNN+FL 无线资源调度 | 低 | 三层嵌套仿真 |

**偏 CS/网络的候选（不符合"无线/卫星"约束，保留但不优先）**：#1 NFV/SFC, #4 组播路由, #5 CFN, #6/#7 离线RL+网络

### 关键结论

1. **传统通信物理层全线不可行**：调制识别、端到端自编码、硬件损伤补偿全部红海或方法不匹配，信息论锁死创新空间
2. **无线/卫星非热门子领域命中率最高（43%）**：场景驱动+窄领域比方法驱动+热门领域更有效
3. **Top 1 候选（#12 卫星 IoT NTN）**综合评分最高：空白确认、3GPP 标准驱动、与论文结构兼容

## 不要做什么

1. **不要再搜新角度**——57+ 角度已经够多，现在需要深度验证而非广度搜索
2. **不要跳过 GW 框架直接开 Contract**——必须走 GW Step 3-7 的完整流程
3. **不要忽略实验完备性对标**——框架刚更新，GW Step 3 精读必须包含实验完备性提取（3-5 篇核心竞品论文）
4. **不要忘记通信特有维度**——domain-comms.md §7 新增了信道模型分级、拓扑多样性、DRL 收敛性、复杂度四个维度，Step 4 可行性必须检查
5. **不要重蹈 Walker 网格覆辙**——卫星 IoT 的拓扑结构（卫星-用户二部图？动态变化？）需要仔细评估 GNN 是否真的有增量，还是又会退化为 MLP

## 必读

按优先级排序：

1. **`stages/groundwork.md`** — GW 阶段流程（Step 3-7）
2. **`stages/gw-read.md`** — 精读流程，含新增的实验完备性提取维度
3. **`stages/gw-feasibility.md`** — 可行性评估四维度
4. **`domain-comms.md` §7** — 新增的通信特有维度
5. **`.sessions/direction-scouting/scout-state.md`** — 完整搜索状态（候选池 + 已排除列表）
6. **`directions-registry.md`** — 根目录方向注册表（已同步至批次 4）
7. **`code-quality.md`** — 方法论适配性矩阵（FR-09 GNN信息冗余检查、FR-10 空间隔离约束）
8. **`templates.md`** — 含新增的实验完备性提取模板

## 下一轮

### 目标

对 Top 1 候选（#12 卫星 IoT NTN 接入 + GNN）执行 GW Step 3-4 深度验证。

### 具体步骤

#### Step 3：精读 + 实验完备性提取

用 `claude -p` 串行派 Worker 精读 3-5 篇核心论文：

1. **Liu et al. 2022** (c=42) "Deep Dyna-RL Based RA Control in LEO Satellite IoT" — DRL+NTN IoT 开创工作
2. **Cao et al. 2020** (c=139) "Deep RL for Multi-user Access Control in NTN" — DQN NTN 接入控制
3. **Feng et al. 2026** (c=0) "Joint Optimization of Access Control & Resource Allocation for LEO Satellite IoT Using DRL" — 最新 state-of-art
4. **Le et al. 2024** (c=84) "Survey on RA Protocols in Direct-Access LEO Satellite IoT" — 综述，了解问题全景

每篇 Worker 返回：
- 标准 gw-read 结构化数据（问题建模、方法、实验设置、结果）
- **实验完备性提取**：baseline 列表、评估指标、仿真规模、信道模型、对比范式
- 该论文的 GNN 适用性评估：问题有无图结构？拓扑是否异构？

精读完成后汇总**实验完备性对标表**。

#### Step 4：可行性评估

基于精读结果，按四维度评估：

- **A 新颖性**：GNN×NTN IoT 接入是 (a)没人想到 还是 (b)不需要？
- **B 方法适配**（关键判断！）：
  - 卫星-用户拓扑是否异构？（会不会像 Walker 星座一样规则？）
  - GNN 建模拓扑是否有增量？还是简单 DQN 就够了？
  - Size generalization 是否适用？（小场景训练→大场景部署）
- **C Baseline 可行性**：ACB、slotted ALOHA、DRL 方案能否纯 Python 实现？
- **D MVE 设计**：最小场景参数（1 LEO + N IoT + T 时隙），GNN vs DQN vs ACB

**加上 domain-comms.md §7 的通信特有维度**：
- 信道模型：3GPP TR 38.821 NTN 信道，纯仿真可行？
- 拓扑多样性：卫星-用户拓扑变化模式
- DRL 收敛：NTN 长传播延迟对 reward 的影响
- 复杂度：设备规模（mMTC 千级 vs 小规模百级）

#### 判定

- **Go** → 进入 GW Step 5-7（baseline 设计 → MVE → Contract）
- **No-Go** → 顺延 Top 2（#11 工业无线 TSCH），重复 Step 3-4

### Worker 派遣方式

与搜索阶段相同：`claude -p --append-system-prompt` 串行派遣，每个 Worker 做 1 篇论文精读或 1 个可行性维度检查。Worker 返回结构化摘要，主对话集成判断。

### 项目目录

如果 Go，新项目路径为 `projects/ntn-iot-gnn-access/`（或类似命名）。No-Go 则不创建。

### 预计工作量

- Step 3 精读：4 Worker × ~0.8 USD ≈ 3-4 USD
- Step 4 可行性：2-3 Worker ≈ 2-3 USD
- 总计约 5-7 USD，可在 1-2 个对话内完成
