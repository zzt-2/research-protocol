# 候选方向深度评估（第二轮）

> 日期: 2026-05-16
> 来源: 3 个深搜 agent（C/NFV, E/IoT, I/FL），各 6-8 组搜索 + WebSearch
> 总检索量: 一轮 ~500 条 + 二轮 ~540 条

## 候选方向 1: GNN + NFV/SFC 跨规模服务链嵌入（推荐 ★★★★★）

### 核心问题
在小规模底层网络上训练 GNN+DRL 做 SFC embedding，泛化到大规模网络，无需重训练。

### 文献空间
- GNN+VNF 放置/VNE: 20+ 篇（已充分研究，c=99 那篇 2020 为代表）
- GNN+SFC 编排: 有初步探索（GraphSSC 2026, GCN-Transformer SFC 2026）
- **GNN+NFV+size generalization: 几乎空白**（仅 GPG-VNFE 2025 接近，用预训练而非结构化泛化）
- 空白类型: **方法×场景交叉空白**（GNN+NFV 有论文，size gen 也有理论论文，但交叉点无人做）

### 与现有工作共享性
- **方法论**: 完全共享 GNN+DRL+size gen 框架
- **系统模型**: 不同（NFV 是虚拟化网络，非卫星），但仿真框架（PyG+wandb）可复用
- **差异化**: 图结构更复杂（底层网络 + SFC 请求 双图编码）

### 组合叙事线
```
Ch1: GNN routing size gen (卫星拓扑图) → Ch2: GNN handover size gen (用户-卫星二部图) → Ch3: GNN SFC embedding size gen (底层+SFC双图)
```
统一主线: "GNN+DRL 的跨规模泛化——从卫星到地面虚拟化网络"
技术深度递进: 单图→二部图→异构双图

### 初步问题建模
- **优化目标**: 最大化 SFC 接受率 + 最小化资源消耗 + 负载均衡
- **约束**: 节点 CPU/内存容量、链路带宽、VNF 顺序依赖、延迟上限
- **MDP**:
  - 状态: 底层网络图（节点=服务器, 边=链路）+ 待嵌入 SFC 图（节点=VNF, 边=依赖）
  - 动作: 顺序为每个 VNF 选择放置节点
  - 奖励: 接受率 + 资源效率 - 违反约束惩罚
- **GNN**: 异构 GNN (HGT/RGCN) 编码双图，输出底层节点嵌入
- **Size gen 路径**: 20 节点/5 SFC 训练 → 200+ 节点/50+ SFC 部署

### 可行性评估: 高
- 纯 Python（NetworkX 拓扑 + PyG GNN + 自定义环境）
- VNF placement 是 NP-hard（可归约为 bin-packing），贪心离最优差距大
- 已有 c=99 论文证明 GNN > MLP 在此问题上有实质优势
- 无物理约束

### 风险
1. **先验近最优（中低）**: NP-hard 保证优化空间，但特定网络规模/负载下贪心可能够好——需 MVE 验证
2. **与 hgat-dag-offloading 方法重叠（中）**: 都是图+任务分配，需确保差异化（双图编码 vs 单图）
3. **竞品时间窗口（低）**: GPG-VNFE 2025 已接近此方向，需尽快推进

### 发表潜力
- 顶刊: JSAC, TMC, TNNLS
- 预期贡献: 首个 NFV 场景 size gen + 异构双图 GNN + 实用价值（运营商实验室训练→生产部署）

---

## 候选方向 2: GNN + IoT mMTC 免授权上行调度（推荐 ★★★★☆）

### 核心问题
GNN+DRL 做 mMTC grant-free 上行调度，从小规模设备拓扑训练泛化到大规模（100→1000+ 设备）。

### 文献空间
- GNN+功率控制: 已充分研究（Eisen 2019 c=110 起，20+ 篇）
- GNN+D2D 链路调度: 已充分研究（FPLinQ 系列）
- GNN+mMTC grant-free: **几乎空白**（仅 2025-2026 两三篇初步探索）
- **IoT 场景 size gen: 几乎空白**（仅 RobustGANTT 2024，背散射场景非标准 mMTC）
- 空白类型: **场景空白**（mMTC grant-free 几乎没有 GNN 方案）

### 与现有工作共享性
- **方法论**: 完全共享 GNN+DRL+size gen 框架
- **图结构**: 干扰图（设备=节点, 干扰=边）——与 Ch1 拓扑图、Ch2 二部图都不同
- **仿真框架**: 可复用训练管线，但仿真器需重新开发

### 组合叙事线
```
Ch1: GNN routing size gen (几十颗卫星) → Ch2: GNN handover size gen (数百用户) → Ch3: GNN mMTC size gen (数千设备)
```
规模递进: 卫星(10²) → 用户(10²-10³) → IoT设备(10³-10⁴)
叙事: "GNN 跨规模泛化能力随问题规模增长的挑战与解决方案"

### 初步问题建模
- **优化目标**: 系统吞吐量 + QoS 满足率 + 公平性
- **约束**: 可用 RB 数、每设备功率上限、干扰 SINR 门限
- **MDP**:
  - 状态: 干扰图（设备=节点, 干扰=边）+ 缓冲队列 + QoS 等级
  - 动作: 每设备 {传输/等待} + RB 分配 + 功率选择
  - 奖励: 吞吐量 + QoS 满足率 - 功率消耗
- **GNN**: GraphSAGE/GAT 编码稀疏干扰图
- **Size gen 路径**: K=50 设备/M=20 RB 训练 → K=500-1000/M=50-100 部署

### 可行性评估: 中-高
- 纯 Python 仿真可行（O(K²) 干扰矩阵计算）
- **必须高负载场景**（设备数 >> RB 数）才有优化空间
- 3GPP 典型场景: 1000 设备竞争 50 RB → 竞争比 20:1

### 风险
1. **GNN ≈ MLP（中）**: 如果干扰图太密集（近似全连接），GNN 退化为 MLP——需稀疏图结构
2. **先验近最优（中）**: 低负载时 gap 小，必须聚焦高负载——需 MVE 验证 gap
3. **动作空间设计（中）**: 每设备 {传输/等待} + RB 分配，组合爆炸风险——需简化

### 发表潜力
- 顶刊: JSAC, TWC, TCOM
- 预期贡献: 首个 mMTC grant-free GNN 方案 + IoT 场景 size gen + 10x→100x 规模泛化

---

## 候选方向 3: GNN + 无线联邦学习资源调度（推荐 ★★★☆☆）

### 核心问题
GNN 编码设备干扰拓扑，DRL 联合优化 FL 的 client selection + 功率/带宽分配，跨设备规模泛化。

### 文献空间
- GNN+FL 无线资源调度: ~10 篇（2024-2026 刚起步，引用量 <25）
- **FL 场景 size gen: 完全空白**
- 子问题空白: Client selection(GNN 1篇 c=4), 功率分配(1篇 c=23), 联合优化(几乎空白), 聚合调度(空白)
- 空白类型: **交叉领域空白**（GNN、FL、无线 各自有大量论文，但三者交叉极少）

### 与现有工作共享性
- **方法论**: 共享 GNN+DRL 框架
- **图结构**: 客户端拓扑图（设备=节点, 信道关系=边）
- **额外复杂度**: 需仿真 FL 训练过程（非纯资源分配）

### 组合叙事线
```
Ch1: GNN routing size gen (纯网络优化) → Ch2: GNN handover size gen (网络+移动性) → Ch3: GNN FL scheduling size gen (网络+AI训练)
```
复杂度递进: 纯网络 → 网络+移动性 → 网络+AI训练动态

### 初步问题建模
- **优化目标**: FL 收敛速度（达到目标精度的轮数）+ 能耗 + 延迟
- **约束**: 总功率/带宽预算、设备能量、数据异构性
- **MDP**:
  - 状态: 设备图（节点=设备, 边=信道关系）+ FL 训练状态（round, 精度, 梯度范数）
  - 动作: Client selection (top-K) + 功率分配 + 带宽分配
  - 奖励: 收敛速度 - 能耗 - 延迟
- **GNN**: GraphSAGE/GAT 编码设备图
- **Size gen 路径**: K=20 设备训练 → K=200-500 部署

### 可行性评估: 中
- **仿真复杂度最高**: 需同时仿真 FL 训练循环 + 无线信道 + DRL 训练
- FL 训练仿真: 1000 episodes × 50 rounds × 50 devices = 中等计算量（2-8h/GPU）
- Baseline 充足: FedCS (c=442), DRL 方法, 优化方法

### 风险
1. **仿真复杂度（中-高）**: FL 训练 + 无线 + DRL 三层嵌套，调试困难
2. **GNN 必要性（中）**: 设备图是否有足够结构信息？如果边关系简单（仅信道质量），GNN 可能无优势
3. **问题空间偏窄（中）**: GNN+FL+无线 交叉点仅 ~10 篇，可能不够支撑完整研究方向
4. **竞品追赶（低）**: 2024-2026 刚起步，但 ACM 2024 (c=4) 已占位 client selection

### 发表潜力
- 顶刊: JSAC, TWC, TMC
- 预期贡献: 首个 FL 场景 size gen + 联合 client selection + 资源分配 GNN 方案
- 估计产出: 1-2 期刊 + 1-2 会议（偏窄）

---

## 最终推荐排序

| 排名 | 方向 | 推荐理由 | 主要顾虑 |
|------|------|---------|---------|
| **1** | **C: NFV/SFC 跨规模嵌入** | 文献空白确认（size gen×NFV=空白）；NP-hard 保证优化空间；GNN>MLP 已被验证；纯 Python 仿真简单；论文空间最丰富 | 与 hgat-dag-offloading 方法重叠 |
| **2** | **E: IoT mMTC 调度** | 场景空白最大（grant-free GNN≈0）；规模跨度最大（100→10000）；5G/6G 标准关联 | GNN>MLP 需稀疏图；高负载才有 gap；动作空间组合爆炸 |
| **3** | **I: FL 资源调度** | 交叉领域最空白（GNN×FL×无线≈10篇）；方法论统一 | 仿真最复杂三层嵌套；问题空间最窄 |

### 推荐理由详述

**首选 C 的核心理由**:
1. **风险最低**: GNN>MLP 已被验证（c=99 论文），NP-hard 保证优化空间，无物理约束
2. **内容最丰富**: NFV/SFC 文献充足，baseline 丰富，子问题多样，足以支撑深入分析
3. **空白最可论证**: GNN+NFV 有 20+ 篇，size gen 有理论论文，但交叉点 = 0——一个清晰的"方法×场景"交叉空白
4. **仿真最简单**: NetworkX 拓扑 + PyG GNN，无需物理层仿真
5. **MVE 最快验证**: 20 节点网络，贪心 vs GNN+DRL，1-2 天可出结果

**如选 E 的补充论据**:
- 规模跨度最大，与 Ch1/Ch2 形成自然递进（卫星→用户→IoT 设备）
- 5G NR mMTC 标准关联，实用价值明确
- 但 GNN>MLP 和 gap 存在性都需要 MVE 先验证

**I 不作为首选**:
- 仿真复杂度（FL 训练 + 无线 + DRL）是最大障碍
- 问题空间偏窄，论文产出可能不足
- 但如果前两个方向 MVE 失败，I 是保底选项

---

## 检索结果文件索引

本轮深搜新增检索文件（存于 search-archive/2026-05-16/）：

| 文件模式 | 方向 |
|----------|------|
| `gnn-vnf-sfc-*.json` | C: NFV/SFC |
| `gnn-network-slicing-*.json` | C: 网络切片 |
| `gnn-virtual-network-embedding-*.json` | C: VNE |
| `gnn-drl-nfv-*.json` | C: DRL+NFV |
| `size-generalization-gnn-resource-*.json` | C: Size gen |
| `gnn-combinatorial-optimization-*.json` | C: 组合优化 |
| `gnn-iot-device-scheduling-*.json` | E: IoT 调度 |
| `gnn-mmtc-resource-*.json` | E: mMTC |
| `gnn-d2d-scheduling-*.json` | E: D2D |
| `gnn-federated-learning-*.json` | I: FL 资源调度 |
