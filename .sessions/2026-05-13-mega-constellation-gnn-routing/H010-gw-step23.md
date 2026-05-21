# 新对话提示词：GNN-based LEO Mega-Constellation Routing — GW Step 2-3

## 任务

对选定方向"**GNN-based routing optimization for LEO mega-constellation networks**"执行 Groundwork Step 2（论文获取）和 Step 3（精读），产出 `literature_notes.md`。

## 背景

在卫星通信大类下完成了大规模文献检索（2026-05-13），识别出 3 个候选方向。经用户确认，选定**方向 1：GNN-based routing for LEO mega-constellation**。

核心判断依据：

- **蓝海**：5 年仅 ~38 篇相关论文，2025-2026 增速显著
- **与导师方向高度吻合**：ISL + LEO 链路层，从 ISL ACM 延伸到 ISL 网络层 routing
- **仿真负担轻**：网络层问题，不需要复杂信道模型，NumPy + PyTorch Geometric 即可
- **GNN 是天然工具**：星座网络=图结构，size generalization 是核心挑战

## 方向详情

读 `.sessions/DIRECTION-CANDIDATES.md` 中"方向 1"的完整分析，包含代表文献列表和趋势数据。

## 项目设置

1. 在 `projects/` 下创建项目目录：`projects/leo-mega-constellation-gnn-routing/`
2. 初始化项目文件（`decision_log.md`、`literature_notes.md` 等）

## 执行步骤

### Step 0：读框架文件（必须）

1. `stages/groundwork.md` — 整体流程（Step 2-3 部分）
2. `stages/gw-acquire.md` — 论文获取操作规范
3. `stages/gw-read.md` — 精读模板和提取要求
4. `domain-comms.md` — 通信领域定制
5. `tools-guide.md` §1-3 — 工具使用

### Step 1：获取必读论文

从 `.sessions/DIRECTION-CANDIDATES.md` 方向 1 的代表文献开始：

**最高优先级（必读）**：

- (2024) GNN-Based Routing for Link Reliability Optimization in SD-LEO Satellite Networks, doi:10.1109/NFV-SDN61811.2024.10807492
- (2026) Geographic-Based Auxiliary Routing Scheme in SDN-Based Mega Constellation Networks, IEEE IoTJ, doi:10.1109/JIOT.2025.3638842
- (2025) Multi-Attribute Consistency Segment Resilient Routing, IEEE TMC, doi:10.1109/TMC.2025.3570670
- (2024) Clustered Multi-Criteria Routing Algorithm for Mega LEO, IEEE TVT, doi:10.1109/tvt.2024.3396350
- (2025) A Scalable Multicontroller SDN Framework, IEEE IoTJ, doi:10.1109/JIOT.2025.3576912

**补充检索**：用 `--find-similar` 和 `--citations` 从上述论文扩展引用链，确保覆盖：

- GNN 在无线网络中的 size generalization 工作（历史检索中已有相关结果）
- 传统 LEO 路由方法（OSPF-based、snapshot-based、DTN-based）
- GNN for wireless 系列经典工作（Shen et al., Kim et al.）

用 `tools/download` 获取论文全文（优先 arXiv 开源版本），用 `tools/convert` 转 markdown。

### Step 2：精读

按 `gw-read.md` 模板对每篇论文提取：

- 研究问题和方法
- 星座模型参数（卫星数、轨道面数、ISL 类型、轨道高度）
- 路由算法详情（目标函数、约束、求解方法）
- 性能指标（时延、吞吐、负载均衡系数、收敛速度）
- 仿真环境和 baseline（用什么工具、对比哪些方法）
- 通信领域额外字段（`domain-comms.md` §1.1）

### Step 3：综合分析

在 `literature_notes.md` 中写综合分析，重点关注：

1. **GNN 架构选择**：现有工作用 GCN/GAT/GraphSAGE 哪种？各自优劣？
2. **Size generalization 现状**：是否有人做过星座规模泛化？效果如何？
3. **仿真工具链**：大家用什么做路由仿真？自建？NS-3？SNS3？
4. **Baseline 惯例**：对比哪些传统方法？用什么指标？
5. **创新空间确认**：综合精读后，创新点是否仍然成立？

## 约束

- 论文获取遵循 `gw-acquire.md` 止损规则（IEEE 付费墙是常态，下载失败不重试 >2 次）
- 精读目标 ≥8 篇核心文献（通信细分领域标准）
- 工具调用从项目根目录：`cd /mnt/d/code/study/research-protocol && ...`
- 路径合规：论文存 `papers/`，检索存 `search-archive/`，项目产物存 `projects/`
- 子 agent 最多 3 个并发
