# 专题：GNN 波束跳跃（方向 B）

> 状态：**closed** | 创建：2026-05-15 | 最后更新：2026-05-15
> 项目目录：`projects/leo-beam-hopping-gnn/`

## 进展线索

### H010-gw-beam-hopping.md
方向 B（Beam Hopping + GNN）的启动提示词。定义核心问题（多波束 LEO 卫星 BH 用 GNN 建模波束间空间干扰耦合）、确认 GNN for BH pattern design = 零篇论文（蓝海）、列出已完成的 4 组检索资产（74 篇去重，GNN for BH = 0 篇确认）、规划 GW Step 2-3 执行步骤。

### H001-initial.md
GW Step 1-3 完成。4 组检索合并 105 篇，AI 审查 22 篇候选，精读 8 篇（L01-L08）。核心创新点再次验证：GNN for BH pattern design = 零篇论文。关键发现：所有 DRL 方法（QPLEX/PPO/MA3C）都不建模波束间空间干扰耦合，GNN 有明确优势切入点。最关键借鉴来源：L01（图构建+聚合函数）、L06（3D 超边图+开源代码）。待 Step 3.5 定向补充检索。

### H002-step35.md
GW Step 3.5 完成。4 组关键词定向检索 + 引用链分析，新增 53 条候选，筛选 12 篇精读 + 16 篇浅读候选。覆盖面缺口：Geng TVT 2025、Zhang TWC 2026 等 4 篇付费墙未获取全文。GNN 卫星 RA 正在起步但未触及 BH。待 Step 4a Go/No-Go 决策。

### H003-step4a.md
GW Step 4a 完成，Conditional Go。维度 A（结构优势）：GNN 保留干扰图拓扑，L01 实证 +30%。维度 B（新颖性-可行性）：零竞品确认，GNN 卫星 RA 已突破。维度 D（MVE）：GNN 收敛时 +16%~+48% over MLP，但 3/5 seeds REINFORCE 训练崩溃（非结构性问题）。GNN zero-shot 可扩展性确认（N=19 训练 -> N=37 部署）。条件：实现时必须用 PPO/SAC 替代 REINFORCE。

### H004-feasibility.md
GW Step 4b 完成，Go。Step 5 Baseline 选定：PPO+MLP（主选，核心消融）+ 图着色 L04（次选，非 ML 基线）+ Greedy/EPA（trivial 下界）。35 篇论文田野调查，Greedy 为绝对共识（8+ 篇）。全部 baseline 无开源代码，需自实现。4a Conditional Go + 4b Go = 整体 Go。仿真关键要求：必须包含真实天线方向图。

### H005-step4a-2.md
GW Step 5 完成。Baseline 交叉验证选定：PPO+MLP（核心消融）、图着色 L04（非 ML 基线）、Greedy/EPA（trivial）。QPLEX（L03）暂不选，实现成本极高。全部 baseline 优先级 3（无代码有描述），需自实现。待 Step 4b 仿真条件+资源风险验证。

### H006-step7-partA.md
GW Step 7 Part A 完成。仿真器 5 模块实现（config/antenna/channel/traffic/env）+ 3 项物理修正（噪声功率、路径损耗、干扰惩罚方向）+ 吞吐量归一化修正。MDP 试运行 16/16 验证通过 + 奖励合理性 3/3 通过。关键设计变更 D008/D009 记录。OptGreedy vs Random 差距 10.7% > 10% 阈值。

### H007-step7-partB.md
GW Step 7 Part B 完成。3 个 baseline 实现 + 统一评估。结果：OptGreedy +10.5%（干扰 intf=0.50，差距主因），GraphColoring +1.8%（干扰降 35.7%），PPO+MLP +0.2%（扁平 MLP 无法学习空间干扰结构，近乎 Random）。关键发现：干扰惩罚是核心区分因子，PPO+MLP < GC 支持 GNN 必要性论点。原计划进入 Contract 阶段，但实际先做了 PPO+GNN 初试。

### H008-ppo-gnn-trial.md
PPO+GNN 初试完成，方向待决。PPO+GNN 仅 +1.5% over Random，虽消融成立（GNN > MLP），但提升有限且未超传统 GraphColoring。根因分析：(1) 成功 GNN 论文全不用 RL（用无监督/监督学习）；(2) 奖励信号中 fairness 占 82% 几乎恒定不可学，可学信号 interference 仅 7%；(3) MVE 的 +16~48% 结论需要修正，问题不在算法稳定性而在动作空间+奖励结构。提出三条路径：A 调参（治标）、B 换无监督方法（需重写）、C 换方向。

### H009-archive.md
归档。6 种学习方法（PPO+GNN、DiffGNN v1/v2、REINFORCE+softmax、REINFORCE gamma=0.7）在 N=19 和 N=37 上全部失败，干扰指标均约等于 Random。根因：干扰是 beam pair 之间的物理关系，需要直接计算（如贪心逐波束 SINR 评估），无法从标量奖励通过梯度反向传播学到。不是方法问题、不是规模问题、不是奖励权重问题。BH+GNN 方向确认不成立，归档。

## 已确认结论

1. **GNN for Beam Hopping pattern design 是零竞品蓝海**：4 组检索 + 引用链分析 + 定向补充检索，全覆盖后仍为零篇。BH 方向 2025-2026 密集发文（42+ 篇），全部基于 DRL/传统优化。
2. **GNN+BH 方向不可行**：6 种学习方法（PPO+GNN、DiffGNN v1/v2、REINFORCE 变体）均失败。核心原因是干扰是波束对之间的物理关系，需要直接计算，无法通过标量奖励的梯度反向传播学到。
3. **MVE 的 Conditional Go 条件（PPO 替代 REINFORCE）被证伪**：问题不在训练稳定性（REINFORCE 崩溃），而在动作空间设计 + 奖励信号结构。MVE 的 +16~48% 不应作为后续预期。
4. **扁平 DRL（PPO+MLP）无法学习空间干扰结构**：+0.2% 近乎 Random，而传统图着色（+1.8%）和贪心（+10.5%）都能有效降低干扰。
5. **所有 baseline 均无开源代码**，需自实现。仿真器中天线方向图（Bessel/UPA）是关键要求。

## 未决项

无。专题已归档，方向确认不可行。

## 当前位置

专题已关闭。方向 B（BH+GNN）经完整 GW 流程（检索 -> 精读 -> 可行性 -> MVE -> 仿真器 -> baseline -> PPO+GNN -> DiffGNN -> REINFORCE 变体）充分验证后确认不可行，已于 2026-05-15 归档。
