# [S014] 最终一致性检查

> 2026-05-26 | Phase 6 | 完成

## 目标

三章论文最终一致性检查：参数、指标、符号、叙事、数据、隔离性六维度。

## 记录

### 维度1: 参数一致性

| 参数 | Ch1 | Ch2 | Ch3 | 一致性 |
|------|-----|-----|-----|--------|
| 轨道高度 | 550km | 550km | 550km | ✅ |
| 轨道倾角 | 53° | 53° | **86.4°** | ⚠️ 有意设计 |
| Walker-Delta F | 1 | 1 | 1 | ✅ |
| 星座规模 | 66-720 (训练66+100+200) | 396 (18×22) | 66 (6×11, 泛化48/288/720) | 各章不同（预期） |
| 信道模型 | Shannon B·log₂(1+SNR) | Shannon + FSPL + fading | **固定容量 10Gbps** | 根本不同 |
| ISL 类型 | 激光 1550nm, B=1GHz | N/A (GSL为主) | 面内固定+面间距离加权 | 各章不同 |
| ISL 断链阈值 | 5000km | N/A | 纬度>70°断链 | 不同机制 |
| 最小仰角 | 25° | 20° | N/A | 各章不同 |

**结论**：高度全部 550km ✅。倾角 86.4° 差异已有说明（S002 发现 53° 无法产生极地间隙，S003 改用 86.4° + 纬度阈值 70°）。信道模型 Ch1/Ch2 用 Shannon+FSPL，Ch3 用固定容量——S013 结论60已确认 Ch3 不使用 Shannon/FSPL。

**⚠️ S011 跨章参数对比表过时**：S011 §8c 的 Ch3 列（500km/53°/2×4=8）是旧 hgat 数据，不适用于 leo-congestion-routing。需基于实际 Ch3 参数重做。

### 维度2: 指标一致性

| 指标 | Ch1 | Ch2 | Ch3 | 矛盾？ |
|------|-----|-----|-----|--------|
| **主指标** | E2E delay (ms) | Composite reward | E2E delay (ms) | 否（Ch2 问题不同） |
| E2E delay 定义 | Σ(ISL传播时延) | N/A | Σ(传播时延 × 1/(1-util)) | ⚠️ 根本不同 |
| 辅助指标 | Stretch (delay/optimal) | Blocking rate, Throughput | MLU (max load/cap) | 否（各章互补） |
| Retention | delay_same/delay_cross, 值域(0,+∞), ~0.915 | reward_cross/reward_same, 值域100%-400% | N/A | ⚠️ 同名不同义 |
| 统计检验 | Welch's t-test (3 seed) | Welch's t-test + bootstrap CI | Bootstrap + Wilcoxon | 否（方法论一致） |

**关键发现**：

1. **E2E delay 模型差异**：Ch1 是纯传播延迟（无拥塞建模），Ch3 是传播延迟×拥塞惩罚权重 `1/(1-util)`。这是根本不同的延迟概念。Ch3 paper-materials 已明确标注 "congestion_factor 的定位" 段落说明这不是物理排队延迟而是拥塞惩罚权重。但绪论需显式说明三章延迟模型差异。

2. **Retention 同名冲突**：Ch1 定义为时延保留率（~0.915, 值域接近1.0），Ch2 定义为迁移奖励比（218%-340%）。Ch2 06_formulas_symbols.md §8 已有消歧："本章 retention 指迁移奖励比"。✅ 已处理。

3. **MLU 指标定位**：Ch3 的 GNN/ECMP MLU 改善不显著(p=0.26)，但 E2E delay -20% 显著。S013 结论59和 Ch3 paper-materials 均已标注应如实报告 MLU 局限、强调 delay。✅ 已处理。

### 维度3: 符号一致性

**已有消歧（Ch1/Ch2 的 06 文件中）**：

| 符号 | Ch1 统一 | Ch2 统一 | Ch3 状态 |
|------|---------|---------|---------|
| $N$ | $N_{\text{sat}}$ | $N_{\text{UE}}$ | **无 06 文件** |
| $B$ | $B_{\text{ISL}}$ | $N_{\text{blk}}$ | **无 06 文件** |
| $H$ | N/A | $N_{\text{ho}}$ | **无 06 文件** |
| GNN层数 | $L$=3 | $T$→$L$ | $L$=2 |
| 奖励权重 | N/A | $w_r, w_l$ | $\eta_t, \eta_e$ |
| 节点集 | $\mathcal{V}$ | $V$→$\mathcal{V}$ | **无 06 文件** |

**结论**：Ch1/Ch2 的 06 文件已包含跨章消歧标注。Ch3 缺 `06_formulas_symbols.md`（已知 P1-10，待写作前创建）。创建时需采用 S011 统一建议 + 实际 Ch3 参数。

### 维度4: 叙事一致性（"探索性分化"框架）

S012 确定的元分析框架："GNN 有效性取决于架构复杂度与任务需求的匹配"。

| 章 | 叙事定位 | GNN 优势条件 | 数据支撑 | 适配状态 |
|---|---------|------------|---------|---------|
| Ch1 | 规模不变性 | 同构 GAT + 规则拓扑 + PE | retention 91.5%, 11x | ✅ |
| Ch2 | 排列等变性/规模适应性 | 二部图 + N>30 + inter-UE建模 | 50UE +21.2%(p=0.007) | ✅ |
| Ch3 | 故障弹性 | 故障打破拓扑规则性 → GNN自适应 | delay -20%, 11/12组赢 | ✅ |

**统一解释验证**（S011 结论41："规模扩展不改变局部结构的统计性质→泛化成功"）：

| 章 | 泛化结果 | 是否符合统一解释 |
|---|---------|---------------|
| Ch1 | 66→720, retention 91.5% | ✅ 4-neighbor 结构完全不变 |
| Ch2 | 20→50/100UE, 稳定性 2.8x | ✅ 卫星侧固定，UE 侧增加同类节点 |
| Ch3 | 48/288 有效, 720 退化 | ✅ 0.7x-4.4x 族内结构相似，10.9x 跨度过大 |

**⚠️ S011 §8b Ch3 叙事过时**：S011 的 Ch3 贡献描述（"HGAT 提供训练稳定性 mean 2.4x"、"零样本中简单聚合器优于复杂注意力"）针对旧 hgat。实际 Ch3(leo-congestion-routing) 叙事为"故障是 GNN 优势的激活条件"，贡献 80% 来自故障场景。元分析框架本身成立，但 Ch3 具体描述需更新。

### 维度5: 数据完整性（stat_tests.json vs paper-materials）

#### Ch1 核对

| 数据项 | paper-materials | stat_tests.json | 一致 |
|--------|----------------|-----------------|------|
| full stretch mean | 1.083 | 1.0826 | ✅ |
| full stretch std | **0.015** | **0.01879** (seed-level) | ⚠️ |
| full delay mean | 65.92 ms | 65.92 ms | ✅ |
| full delay std | **1.01** | **1.24** (seed-level) | ⚠️ |
| same stretch | 1.000 | 1.000 | ✅ |
| A1 stretch | 1.006 | 1.0063 | ✅ |
| A2 stretch | 1.106 | 1.1057 | ✅ |
| A3 stretch | 1.058 | 1.0583 | ✅ |

#### Ch2 核对

| 数据项 | paper-materials | stat_tests.json | 一致 |
|--------|----------------|-----------------|------|
| 20UE GNN reward mean | 12,847 | 12,846.6 | ✅ |
| 20UE GNN reward std | **126** | **46.2** (seed-level) | ⚠️ |
| 50UE GNN reward mean | 28,198 | 28,198.0 | ✅ |
| 50UE GNN reward std | **978** | **1,195.3** (seed-level) | ⚠️ |
| 50UE GNN blocking | 0.0101 | 0.0101 | ✅ |
| 50UE MLP reward mean | 23,273 | 23,272.6 | ✅ |
| 20UE p-value | 0.76 | 0.759 | ✅ |
| 50UE p-value | 0.007 | 0.0069 | ✅ |

#### Ch3 核对

| 数据项 | paper-materials | stat_tests.json | 一致 |
|--------|----------------|-----------------|------|
| GNN MLU mean | 1.378 | 1.3778 | ✅ |
| GNN MLU std | **0.047** | **0.049** (seed-level) | ⚠️ 微小 |
| ECMP MLU | 1.436 | 1.4355 | ✅ |
| MLP MLU | 1.637 | 1.6370 | ✅ |
| GNN/ECMP MLU | 0.96 | 0.9596 | ✅ |
| GNN vs ECMP p-value | 0.26 | 0.2618 | ✅ |
| GNN vs MLP p-value | <0.001 | 0.0 | ✅ |

**Std 差异根因分析**：所有 mean 完全一致。Std 差异来自计算层次不同——stat_tests.json 报告 seed-level std（3 个 seed mean 的标准差），paper-materials 的 std 可能来自 eval-episode-level 计算或 D031 早期计算。**建议**：写作阶段统一以 stat_tests.json 为权威数据源，paper-materials 中的 std 统一更新。

### 维度6: Ch1/Ch3 隔离验证

| 维度 | Ch1 | Ch3 | 重叠？ |
|------|-----|-----|--------|
| 问题 | 无故障 ISL 路由 + 规模泛化 | 故障弹性路由 + 在线决策 | **否** |
| 学习范式 | 监督学习（Dijkstra 标签） | PPO（DRL） | **否** |
| GNN 架构 | GAT 3层, h=128, 73K参数 | GAT 2层, d=64, 29K参数 | **否** |
| 规模泛化 | **主贡献**（11x, retention 91.5%） | **辅助贡献**（0.7x-4.4x 有效） | 部分重叠 |
| 故障 | 不测试 | 核心贡献（~80%来自故障） | **否** |
| 拓扑 | 53° 无极地间隙 | 86.4° 有极地间隙 | **否** |
| 延迟模型 | 纯传播延迟 | 传播×拥塞惩罚 | **否** |
| 决策粒度 | 逐跳方向（4方向） | 逐流 K-path（4候选路径） | **否** |
| Baseline | GRLR, Dijkstra | ECMP, MLP | **否** |

**规模泛化重叠分析**：两章都做跨规模部署，但：
- Ch1 监督学习 + 无故障 + 拓扑规模变化（节点数变化）
- Ch3 DRL + 故障驱动 + Walker-Delta 族内（P×S 变化）
- Ch1 主贡献 = 规模泛化，Ch3 主贡献 = 故障弹性
- Ch3 的规模泛化是辅助，且 10.9x 退化（与 Ch1 的 11x 成功形成对比）
- 叙事可利用此对比："Ch1 监督学习范式下 11x 成功 vs Ch3 DRL 范式下 10.9x 退化——训练范式和故障场景是泛化难度的关键因素"

**结论**：Ch1/Ch3 贡献机制零重叠，隔离性 STRONG。规模泛化的部分重叠反而可转化为元分析的对比论据。

## 检查总结

### 通过项（无问题）

1. ✅ 三章轨道高度一致（550km）
2. ✅ Ch1/Ch2 倾角一致（53°），Ch3 差异有说明
3. ✅ Ch2 retention 消歧已标注
4. ✅ Ch3 MLU 不显著如实报告
5. ✅ Ch1/Ch2 符号文件有跨章消歧标注
6. ✅ "探索性分化"框架三章适配成立
7. ✅ 统一解释（局部结构统计性质）验证通过
8. ✅ 三章 stat_tests.json 均存在
9. ✅ 所有 mean 值完全一致
10. ✅ 统计结论（显著/不显著）完全一致
11. ✅ Ch1/Ch3 贡献机制零重叠

### 待处理项

| 级别 | 问题 | 位置 | 处理建议 |
|------|------|------|---------|
| **CRITICAL** | **三章 paper-materials 全部过时** | Ch1/Ch2/Ch3 | 两周前提取，未反映终审14轮对话的大量更新；需讨论提取工作流后全部重做 |
| HIGH | Ch3 未按 01-06 格式拆分 | Ch3 | 仅单文件 paper-materials.md，无 paper_materials/ 目录 |
| HIGH | Ch3 缺 06_formulas_symbols.md | Ch3 | 无符号文件 |
| HIGH | S011 符号/参数表 Ch3 列是旧 hgat 数据 | S011 | 重做时以 S013 为 Ch3 权威来源 |
| MEDIUM | Ch1/Ch3 延迟模型根本不同 | 绪论/各章引言 | 需显式说明延迟模型差异 |
| MEDIUM | Ch1 std 不一致（stretch 0.015 vs 0.019） | Ch1 paper-materials | 重做时统一用 stat_tests 数据 |
| MEDIUM | Ch2 std 不一致（reward 978 vs 1195） | Ch2 paper-materials | 同上 |
| LOW | Ch3 MLU std 微小差异（0.047 vs 0.049） | Ch3 paper-materials | 重做时统一 |
| LOW | S011 两种规模泛化命名需更新 Ch3 部分 | S011 §8d | 绪论中参考 |

### Paper-materials 过时详情

三章 paper-materials 约 2 周前提取，此后经历了以下未反映的更新：

| 更新来源 | 影响内容 | 未反映的章节 |
|---------|---------|------------|
| S001-S002 竞品检索 | 新竞品 5+6+4 篇，空白验证 | Ch1/Ch2/Ch3 |
| S003 GNN 理论文献 | size gen 理论支撑、统计标准 | Ch1/Ch2/Ch3 |
| S004 Ch1 修复 | 3-seed 数据、贡献降级 | Ch1 |
| S005 Ch3 技术审查 | M/M/1→拥塞惩罚、天线增益、noise | Ch3 |
| S006 Ch1+Ch2 审查 | retention 公式统一、eps-greedy 修正 | Ch1/Ch2 |
| S007 18篇精读 | 写法规范、统计惯例、结构参考 | 跨章 |
| S008 数据确认+统计 | stat_tests.json、图生成 | Ch1/Ch2/Ch3 |
| S011 符号统一 | 7类冲突+18项公式修正 | Ch1/Ch2/Ch3 |
| S012 元分析+Ch3确认 | "探索性分化"框架、Ch3=leo-congestion-routing | 跨章 |
| S013 Ch3终审 | 节点特征修正、E02/E08矛盾说明、合规6/8 | Ch3 |

**结论**：paper-materials 不能直接用于写作，需在讨论提取工作流后全部重新提取。

## 决策引用

- 无新决策

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

1. **新对话**：讨论 paper-materials 提取工作流（格式/范围/输入源）
2. **重提取**：基于终审全部结论，三章统一重新提取 paper-materials
3. **开题报告**：重提取完成后准备
