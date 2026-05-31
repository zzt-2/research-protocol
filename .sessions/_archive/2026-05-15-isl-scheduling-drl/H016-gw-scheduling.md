# 新对话提示词：方向 A — ISL Scheduling + DRL

## 任务

为"LEO 星座 ISL 调度 + DRL"方向执行 Groundwork Step 2-3（论文获取 + 精读）。创建项目目录 `projects/leo-isl-scheduling-drl/`。

## 方向定义

- **核心问题**：巨型 LEO 星座中 ISL（星间链路）的建立、维护和切换如何用 DRL 在线优化？区别于路由（给定拓扑找路径），ISL 调度是决定哪些链路存在。
- **与已有项目关系**：与 leo-gnn-routing 互补（链路层 vs 网络层，DRL vs GNN）。不与 ris-phase-drl、leo-ntn-handover 重叠。

## 检索资产（已完成，GW Step 1）

4 组检索已存档在 `search-archive/2026-05-15/`：

1. `leo-satellite-inter-satellite-link-scheduling-topology-manag.json`
2. `leo-satellite-laser-optical-inter-satellite-link-isl-establi.json`
3. `satellite-constellation-topology-reconfiguration-dynamic-lin.json`
4. `mega-constellation-satellite-isl-handover-switching-distribu.json`

去重后 101 篇相关，ISL 调度子方向 10 篇（5 篇用 DRL）。关键竞品：
- Wang et al. TCOM 2024（MADRL 激光 ISL 调度，27 cites）
- Pi et al. ICC 2022（MADDPG ISL 规划，27 cites）
- Wang et al. TWC 2024（联邦 RL 激光 ISL 调度）
- Guo et al. TWC 2024（分布式拓扑优化，33 cites）
- Gu et al. 2026 arXiv（GNN+拉格朗日对偶联合连接+路由）

## 执行步骤

### Step 0：读框架文件（必须）

1. `stages/groundwork.md` — Step 2-3 部分
2. `stages/gw-search.md` — 检索复用规则
3. `stages/gw-acquire.md` — 论文获取流程
4. `stages/gw-read.md` — 精读模板
5. `domain-comms.md` — 通信领域定制
6. `tools-guide.md` §1-3 — 工具使用

### Step 1：合并检索 + AI 候选审查

```bash
cd /mnt/d/code/study/research-protocol
# 合并 4 组检索结果
bash tools/search --merge search-archive/2026-05-15/leo-satellite-inter-satellite-link-scheduling-topology-manag.json,search-archive/2026-05-15/leo-satellite-laser-optical-inter-satellite-link-isl-establi.json,search-archive/2026-05-15/satellite-constellation-topology-reconfiguration-dynamic-lin.json,search-archive/2026-05-15/mega-constellation-satellite-isl-handover-switching-distribu.json --output search-archive/2026-05-15/isl-scheduling-merged.json
```

然后按 gw-search.md 的 AI 候选审查流程，对合并结果做语义筛选和优先级标注。目标：筛选出 15-25 篇高相关性候选。

### Step 2：论文获取（gw-acquire）

从筛选后的候选中，按优先级下载论文。优先获取：
- 5 篇直接竞品（Wang TCOM 2024, Pi ICC 2022 等）
- 有 arXiv 版本的优先（自动下载成功率高）
- IEEE 付费墙论文列出手动获取清单，不强求

用 `tools/download` 批量下载，失败清单交给用户。

### Step 3：精读（gw-read）

按精读模板提取每篇论文的结构化数据。通信领域额外提取信道模型参数表。

精读重点：
- 现有 ISL 调度方法（启发式/优化/DRL）的优劣势
- 仿真环境设置（星座规模、轨道参数、ISL 模型）
- 关键指标（时延、链路利用率、切换开销、吞吐量）
- 可借鉴的 baseline 和可改进的方向

### Step 3.5：定向补充检索（必做）

精读完成后，基于新认知做一轮定向检索，弥补盲区。

### 步骤间 handoff

每完成一步写 handoff 到 `projects/leo-isl-scheduling-drl/sessions/`。

## 约束

- 工具从项目根目录调用：`cd /mnt/d/code/study/research-protocol && ...`
- 路径合规：论文存 `papers/`，检索存 `search-archive/`
- 子 agent 最多 3 个并发
- 论文全文精读在子 agent 中执行
- 单对话不超过 3 步
- PDF 转换必须用 `tools/convert`
