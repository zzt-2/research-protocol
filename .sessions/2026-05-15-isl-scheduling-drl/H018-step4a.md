# 新对话提示词：ISL Scheduling + DRL — Step 4a Go/No-Go

## 任务

为"LEO 星座 ISL 调度 + DRL"方向执行 GW Step 4a（方向可行性预判），写 feasibility_report.md。

## 状态恢复

按以下优先级读取：
1. 项目记忆：`~/.claude/projects/-mnt-d-code-study-research-protocol/memory/project_leo-isl-scheduling-drl.md`
2. 最新 handoff：`projects/leo-isl-scheduling-drl/sessions/2026-05-15-handoff-3.md`
3. 精读产出：`projects/leo-isl-scheduling-drl/literature_notes.md`（12 精读 + 3 浅读，综合分析 + Baseline 交叉验证已完整）
4. 框架文件：`stages/gw-feasibility.md`（Step 4a 完整流程）

## 待做事项

### 1. 读取框架文件

**[MUST]** 先读 `stages/gw-feasibility.md`，理解 4a 的完整流程、检查点和通过条件。

### 2. 撰写 feasibility_report.md

按 `templates.md` 的 feasibility_report 模板撰写，输出到 `projects/leo-isl-scheduling-drl/feasibility_report.md`。

核心内容：
- **A. 结构优势论证**：GNN 拓扑编码 + DRL 在线决策 vs 最简 FC-DQN（L09）。引用 L02 GNN 对偶变量学习 + L09/L10/L12 DRL ISL 调度的具体差距
- **B. 新颖性-可行性解耦**：
  - 新颖性：15 篇文献确认 GNN+DRL 细粒度 ISL 调度为空白（所有 DRL 论文为粗粒度+FC）
  - 可行性：L02 GNN 架构可复用，L09 奖励分解可借鉴，L04 setup delay 可嵌入
  - 空白原因：DRL ISL 调度方向本身刚起步（2022 首篇），GNN+DRL 范式尚未迁移
- **C. 仿真条件可行性**：已有 Starlink TLE + 轨道力学 + 激光信道模型参数（L01/L02/L04/L09）
- **D. MVE（最小可行实验）**：设计最小实例验证 GNN+DRL vs FC-DQN 的结构性优势
- **E. 资源/风险比例**：L09/L02 有详细结构化提取可指导复现

### 3. 更新 handoff

完成后写 handoff 到 `projects/leo-isl-scheduling-drl/sessions/2026-05-15-handoff-4.md`。

## 关键文献证据（预加载，不需要重读）

- L02 DeepLaDu：GATv2 4-head 64-dim，SGD lr=10⁻³，subgradient-based edge-level loss，性能≈LaDu-100但快10⁴倍
- L09 Wang TCOM：Double Dueling DQN 810→512→256→8，gamma=0.9，CS 压缩状态，720星收敛
- L10 Pi ICC：MADDPG + Gumbel-Softmax，lr=0.01，gamma=0.95，冲突惩罚{1.0,0.8,0.1}
- L12 Wang TWC：Double DQN 324→256→256→256→128→128→16，联邦FL异步聚合
- L04 ISASR：setup delay 2~30s，LISL range 1500km，Starlink 1584 星

## 约束

- 工具从项目根目录调用：`cd /mnt/d/code/study/research-protocol && ...`
- 子 agent 最多 3 个并发
- 单对话不超过 3 步
- feasibility_report 中的每个论断必须有 literature_notes 中的具体论文引用支撑
