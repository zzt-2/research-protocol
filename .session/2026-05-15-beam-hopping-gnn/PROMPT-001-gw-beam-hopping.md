# 新对话提示词：方向 B — Beam Hopping + GNN

## 任务

为"多波束 LEO 卫星 Beam Hopping + GNN"方向执行 Groundwork Step 2-3（论文获取 + 精读）。创建项目目录 `projects/leo-beam-hopping-gnn/`。

## 方向定义

- **核心问题**：多波束 LEO 卫星的 beam hopping（波束跳变调度 + 功率/时隙分配）如何用 GNN 建模波束间空间干扰耦合，优于现有扁平 DRL 方法（PPO/D3QN/MAPPO）？
- **关键创新点**：GNN for beam hopping pattern design = **零篇论文**。GNN 天然适合图结构化干扰建模，但无人应用于 BH。
- **与已有项目关系**：与 leo-gnn-routing 互补（都用 GNN 但不同层：链路层资源分配 vs 网络层路由）。不与 ris-phase-drl 重叠（RIS 是地面辅助，BH 是卫星侧）。

## 检索资产（已完成，GW Step 1）

4 组检索已存档在 `search-archive/2026-05-15/`：

1. `leo-satellite-beam-hopping-gnn-graph-neural-network-resource.json`
2. `multi-beam-satellite-resource-allocation-deep-learning-power.json`
3. `beam-hopping-leo-satellite-scheduling-time-slot-allocation-d.json`
4. `satellite-beam-scheduling-graph-neural-network-spatial-inter.json`

去重后 74 篇相关。GNN for BH = 0 篇确认。BH+DRL 成熟（42 篇）。

最接近的 GNN 论文（不做 BH 但做相关任务）：
- Geng et al. TVT 2025（GNN + 元学习做波束间功率分配，+30% data rate）
- Zhang et al. TWC 2026（动态超图 NN 做信道+功率分配，LEO 下行）

关键 DRL baseline 论文（需复现或对比）：
- Zhao et al. TWC 2024（DT + A3C + MARL 做 BH pattern + 功率分配）
- Gong et al. TWC 2026（分层 MARL 做 BH 调度，5ms 实时）
- Xie et al. 2025 arXiv（PPO 混合离散-连续动作空间做多星 BH）
- Lin et al. TWC 2024（QMIX MADRL 多星 BH 调度）
- Zheng et al. ChinaComm 2023（势博弈 + 内点法联合 BH + 功率，+45% 吞吐量）

## 执行步骤

### Step 0：读框架文件（必须）

1. `stages/groundwork.md` — Step 2-3 部分
2. `stages/gw-search.md` — 检索复用规则
3. `stages/gw-acquire.md` — 论文获取流程
4. `stages/gw-read.md` — 精读模板
5. `domain-comms.md` — 通信领域定制（重点关注 §1.5 奖励函数设计）
6. `tools-guide.md` §1-3 — 工具使用

### Step 1：合并检索 + AI 候选审查

```bash
cd /mnt/d/code/study/research-protocol
# 合并 4 组检索结果
bash tools/search --merge search-archive/2026-05-15/leo-satellite-beam-hopping-gnn-graph-neural-network-resource.json,search-archive/2026-05-15/multi-beam-satellite-resource-allocation-deep-learning-power.json,search-archive/2026-05-15/beam-hopping-leo-satellite-scheduling-time-slot-allocation-d.json,search-archive/2026-05-15/satellite-beam-scheduling-graph-neural-network-spatial-inter.json --output search-archive/2026-05-15/beam-hopping-merged.json
```

然后按 gw-search.md 的 AI 候选审查流程做语义筛选。目标：15-25 篇高相关性候选。

**审查重点**：
- 区分"BH + DRL"（竞品/baseline）和"GNN + 多波束"（最接近但非 BH）
- 标记可复现的 baseline（有开源代码或详细算法描述）
- 识别 BH 仿真环境的标准设置（波束数、用户数、功率预算、时隙结构）

### Step 2：论文获取（gw-acquire）

优先获取：
- DRL baseline 论文（需要复现或对比）
- Geng 2025 和 Zhang 2026（最接近 GNN 工作，方法论可借鉴）
- 有 arXiv 版本的优先

用 `tools/download` 批量下载，IEEE 付费墙失败是预期行为。

### Step 3：精读（gw-read）

精读重点：
- **DRL baseline 方法的局限性**：为什么扁平 DRL 在大规模多波束场景表现差？空间干扰耦合如何影响性能？
- **GNN 方法论借鉴**：Geng 2025 和 Zhang 2026 如何建模波束间关系？能否迁移到 BH 问题？
- **BH 仿真建模**：多波束卫星模型（波束覆盖、干扰矩阵、功率约束）、业务需求模型（均匀/非均匀/时变）
- **创新切入点验证**：GNN 做 BH pattern 设计是否真的比 DRL 有优势？在什么条件下？

### Step 3.5：定向补充检索（必做）

精读完成后做定向检索，特别关注：
- GNN 在其他调度/分配问题中的应用（非卫星领域的方法迁移）
- BH 仿真环境参考实现

### 步骤间 handoff

每完成一步写 handoff 到 `projects/leo-beam-hopping-gnn/sessions/`。

## 约束

- 工具从项目根目录调用：`cd /mnt/d/code/study/research-protocol && ...`
- 路径合规：论文存 `papers/`，检索存 `search-archive/`
- 子 agent 最多 3 个并发
- 论文全文精读在子 agent 中执行
- 单对话不超过 3 步
- PDF 转换必须用 `tools/convert`
