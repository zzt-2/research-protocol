# Session Log 2026-05-15

## 任务
为第二研究方向执行 Groundwork Step 1（文献检索 + 方向初筛）。

## 完成内容

### Step 0：框架文件已读
- gw-search.md, groundwork.md, domain-comms.md, tools-guide.md

### Step 1：评估现有搜索资产
- 读取 `.session/DIRECTION-CANDIDATES.md`（2026-05-13 的 180+ 条检索）
- 方向 2（beam hopping）：12 篇核心论文，GNN 方向零覆盖 → 空白确认
- 方向 3（NTN 整合）：25 篇，大方向过度拥挤（200+/年），不再推荐

### Step 2：补充检索（2026-05-15，共 12 组）

**方向 A — ISL Scheduling（4 组）：**
1. `leo-satellite-inter-satellite-link-scheduling-topology-manag.json` — ISL 调度/拓扑管理
2. `leo-satellite-laser-optical-inter-satellite-link-isl-establi.json` — 激光 ISL 建立
3. `satellite-constellation-topology-reconfiguration-dynamic-lin.json` — 拓扑重构
4. `mega-constellation-satellite-isl-handover-switching-distribu.json` — ISL 切换 + MARL

**方向 B — Beam Hopping（4 组）：**
5. `leo-satellite-beam-hopping-gnn-graph-neural-network-resource.json` — BH + GNN
6. `multi-beam-satellite-resource-allocation-deep-learning-power.json` — 多波束资源分配
7. `beam-hopping-leo-satellite-scheduling-time-slot-allocation-d.json` — BH 时隙调度
8. `satellite-beam-scheduling-graph-neural-network-spatial-inter.json` — GNN + 波束调度干扰

**其他探索（4 组）：**
9. `leo-satellite-spectrum-sharing-interference-management-deep-.json` — 频谱共享/干扰管理
10. `leo-satellite-inter-satellite-link-wavelength-frequency-assi.json` — ISL 波长/频率规划（3 篇相关，太冷）
11. `leo-satellite-user-link-service-link-optimization-resource-mana.json`（待确认文件名）— 用户链路（红海，与 handover 重叠）
12. `leo-satellite-cross-layer-optimization-joint-link-scheduling.json` — 跨层联合（与 routing 项目重叠）

### Step 3：方向分析

#### 方向 A：ISL Scheduling + DRL
- 4 组检索 → 120 条原始 → 101 篇去重后相关
- ISL 调度子方向：10 篇，其中 5 篇用 DRL → **窄蓝海**
- 更广的 ISL+ML 领域活跃（47 篇 DRL，39 篇在 2025）
- 关键对手：
  - Wang et al. TCOM 2024（MADRL 激光 ISL 调度，27 cites）
  - Pi et al. ICC 2022（MADDPG ISL 规划，27 cites）
  - Wang et al. TWC 2024（联邦 RL 激光 ISL 调度）
  - Guo et al. TWC 2024（分布式拓扑优化，33 cites）
  - Gu et al. 2026 arXiv（GNN+拉格朗日对偶联合连接+路由）

#### 方向 B：Beam Hopping + GNN
- 4 组检索 → 116 条原始 → 74 篇去重后相关
- GNN for beam hopping：**确认零篇**
- BH + DRL 成熟：42 篇 DRL（22 篇 MARL）
- 最接近 GNN 论文：
  - Geng et al. TVT 2025（GNN + 元学习做波束间功率分配，+30% data rate）
  - Zhang et al. TWC 2026（动态超图 NN 做信道+功率分配）

#### 排除的新角度
- **ISL 波长/频率规划**：仅 3 篇，0 ML，太冷门 → 框架不友好（撑不起 8 篇精读 + baseline）
- **用户链路优化**：18 篇 DRL 穿透率 83%，红海 + 与 handover/beam hopping 重叠
- **跨层联合优化**：真正跨层仅 4-5 篇，但与 GNN routing 项目撞车（L006/L027 同方法空间）

### 用户决策
A 和 B 两个方向并行推进，各自独立进入 GW Step 2-3。

## 检索存档清单（2026-05-15）

方向 A 用的 4 个文件：
- `search-archive/2026-05-15/leo-satellite-inter-satellite-link-scheduling-topology-manag.json`
- `search-archive/2026-05-15/leo-satellite-laser-optical-inter-satellite-link-isl-establi.json`
- `search-archive/2026-05-15/satellite-constellation-topology-reconfiguration-dynamic-lin.json`
- `search-archive/2026-05-15/mega-constellation-satellite-isl-handover-switching-distribu.json`

方向 B 用的 4 个文件：
- `search-archive/2026-05-15/leo-satellite-beam-hopping-gnn-graph-neural-network-resource.json`
- `search-archive/2026-05-15/multi-beam-satellite-resource-allocation-deep-learning-power.json`
- `search-archive/2026-05-15/beam-hopping-leo-satellite-scheduling-time-slot-allocation-d.json`
- `search-archive/2026-05-15/satellite-beam-scheduling-graph-neural-network-spatial-inter.json`

## 下一步
- 方向 A、B 各开一个新对话，并行执行 GW Step 2（论文获取）+ Step 3（精读）
- 各自需先合并检索 JSON、做 AI 候选审查
