# [S002] Ch1 路由 Size Generalization 质量审计报告

> 2026-05-22 | 审计 | 完成

## 目标

对 Ch1（LEO mega-constellation GNN routing size generalization）做系统性质量审计，覆盖新颖性、实验完备性、指标完整性、数据自洽性四个维度。

## 审计结论

| 维度 | 判定 | 通过率/状态 |
|------|------|------------|
| A. 新颖性 | **SAFE** | 4/4 核心声称无实质性重叠 |
| B. 实验完备性 | **BELOW THRESHOLD** | 14/26 (54%)，低于 80% 阈值 |
| C. 指标完整性 | **PARTIAL** | 核心指标覆盖，统计严谨性缺失 |
| D. 数据自洽性 | **WARN** | 核心数字自洽，3 处次要矛盾 |

## A. 新颖性判定

### 核心声称新颖性

| 核心声称 | 判定 | 证据 |
|---------|------|------|
| 11x 零样本跨规模泛化 (66→720星) | **SAFE** | 5 组检索 + 120 篇论文无直接竞争者。GPN 做 1.7x，Scaling Swarm 做 3x |
| 加权 Dijkstra 推理 (GNN logits→边权重→最短路径) | **SAFE** | 未见任何论文使用此方案，主流为端到端 DRL 或贪心逐跳 |
| Orbital PE 是可学习性前提条件 | **SAFE** | 未见论文提出或验证 orbital PE。A1 消融证明无 PE 训练精度 39.66%≈随机 |
| 多尺度混合训练 2-4pp 改善 | **SAFE** | 未见论文研究多尺度混合训练对卫星路由 GNN 的贡献 |

### 竞品差异化矩阵

| 竞品 | 年份 | 场景 | 最大泛化倍数 | 差异判定 | 我们的核心优势 |
|------|------|------|------------|---------|--------------|
| GRLR (TVT'25) | 2025 | LEO 路由 | 无（同规模） | SAFE | 11x 零样本泛化 + Orbital PE + 加权 Dijkstra |
| TELGEN (ToN'25) | 2025 | WAN TE | 20x | SAFE | 路由非 TE + LEO 非 WAN + 动态拓扑 + Orbital PE |
| GPN (TMC'25) | 2025 | 6G 组播 | 1.7x | SAFE | 11x vs 1.7x + mega 星座 + Orbital PE |
| Scaling Swarm (AI'25) | 2025 | 群智导航 | 3x | SAFE | 结构化拓扑 vs k-NN + 11x vs 3x + Orbital PE |
| GraphPR (TVT'25) | 2025 | LEO 路由 | 无 | SAFE | 跨规模泛化 + 多尺度训练 + Orbital PE |
| Size Transfer (arXiv'26) | 2026 | 图分类 | ~10x | SAFE | 路由非分类 + LEO 卫星 + 物理先验 PE |

**最需关注**：GRLR（44 引用，该方向标杆，后续工作可能加入 size gen）。

**建议加强的论证点**：
1. 训练成本量化：66-200 星 vs 720 星的计算资源差异
2. PE 不可替代性：A1 消融 39.66%≈随机 是核心证据
3. 规则拓扑优势：与 Scaling Swarm（非结构化 k-NN, 2x 退化）对比

## B. 实验完备性

### 领域标杆标准（从 GRLR/GPN/LARRI 提取）

| 维度 | 领域标准 | 最低要求 |
|------|---------|---------|
| Baselines | 4-7 个（启发式+学习+理论界） | 3 个：Dijkstra + 学习方法 + 理论界 |
| Ablations | 3+ 项，覆盖编码器/决策网络/关键机制 | 1-2 项 |
| Statistics | 5-100 随机实例，均值+方差 | 3-5 seeds + 均值 |
| Visualizations | 收敛曲线 + 分布图 + 路径可视化 | 收敛曲线 + 柱状图 |
| Metrics | 时延 + 收敛 + 计算开销 | 端到端时延 |
| Generalization | 跨规模 + 动态环境 + 跨流量 | 1 组动态适应性 |

### 覆盖度 Checklist

| 维度 | 子项 | 状态 | 影响 | 补救方案 |
|------|------|------|------|---------|
| Baselines | Dijkstra | ✅ COVERED | - | - |
| Baselines | GRLR | ✅ COVERED | - | - |
| Baselines | GraphPR | ❌ MISSING | CRITICAL | 复现或说明排除理由 |
| Baselines | 启发式 (ECMP/SPR) | ❌ MISSING | IMPORTANT | 加 1-2 个简单 baseline |
| Ablation | A1 无 PE | ✅ COVERED | - | - |
| Ablation | A2 无多尺度 | ✅ COVERED | - | - |
| Ablation | A3 无 PE+无多尺度 | ✅ COVERED | - | - |
| Ablation | A4 GNN 深度 | ❌ MISSING | IMPORTANT | E08, 2/3/4 层 GAT 对比 |
| Ablation | A5 PE 类型 | ❌ MISSING | IMPORTANT | E09, random PE 对照 |
| Ablation | Same-scale 对照 | ✅ COVERED | - | - |
| Statistics | 多 seed (≥3) | ❌ MISSING | CRITICAL | 5 seeds 重跑 E01+A1-A3+Same |
| Statistics | CI / std | ❌ MISSING | CRITICAL | 依赖多 seed |
| Statistics | p-value | ❌ MISSING | CRITICAL | 逐流数据已有，一行 scipy |
| Visualizations | 收敛曲线 | ❌ MISSING | IMPORTANT | 从训练日志提取 |
| Visualizations | CDF 图 | ❌ MISSING | IMPORTANT | stretch CDF |
| Visualizations | 路径可视化 | ❌ MISSING | NICE-TO-HAVE | 星座拓扑+路由路径 |
| Generalization | 11x 跨规模 | ✅ COVERED | - | - |
| Generalization | 24x (1584 星) | ❌ MISSING | IMPORTANT | E07, 配置已定义 |
| Generalization | 不同流量模式 | ❌ MISSING | IMPORTANT | E06, hotspot 场景 |

**覆盖率**：14/26 = **54%**（低于 80% 阈值）

**缓解因素**：LEO 路由领域标杆（GRLR/GraphPR）均为单规模测试、1 项消融、无 size gen 研究。我们的核心贡献（size gen）在领域内是独特的。

## C. 指标完整性

### 指标矩阵

| 指标 | 已报 | 可从现有数据补 | 需新实验 | 重要度 |
|------|------|-------------|---------|--------|
| 平均 E2E 时延 | ✅ 66.77ms | - | - | MUST |
| Mean/Median/P95 Stretch | ✅ 1.097/1.056/1.315 | - | - | MUST |
| 时延保留率 | ✅ 90.3% | - | - | MUST |
| 路径成功率 | ✅ 100% | - | - | MUST |
| 训练精度 | ✅ 97.6%/66.8% | - | - | MUST |
| 参数量 | ✅ 72,965 | - | - | MUST |
| ≤1.2x/≤1.5x 最优比例 | ✅ 85.1%/98.9% | - | - | MUST |
| **统计显著性 p 值** | ❌ | ✅ scipy t-test | - | MUST |
| **推理延迟** | ❌ | ✅ 加 time 计时 | - | MUST |
| 最大 E2E 时延 | ❌ | ✅ np.max(all_delays) | - | SHOULD |
| P99 时延 | ❌ | ✅ np.percentile(d,99) | - | SHOULD |
| 时延抖动 | ❌ | ✅ np.std(all_delays) | - | SHOULD |
| 路径跳数 | ❌ | ✅ len(path) 已有 | - | SHOULD |
| **M2 最大链路利用率** | ❌ | ❌ 需 ~15 行代码 | 部分 | SHOULD* |
| 多 seed 标准差 | ❌ | ❌ 需多轮运行 | 是 | MUST |
| 训练收敛曲线 | ❌ | 部分（需重跑存 loss） | 可能 | SHOULD |
| 1584 星泛化 | ❌ | ❌ | 是 | SHOULD |

*注：M2 在 Contract 中定义为核心指标（Agent 2B 判 CRITICAL），但从方法性质看 stretch 优化的路由天然负载不均（Agent 3A 判 SHOULD）。建议：补计算并如实报告，在论文中解释 stretch 优化未直接优化负载均衡。

## D. 数据自洽性

### 矛盾清单

| # | 位置 | 内容 | 严重度 |
|---|------|------|--------|
| 1 | `01_research_context.md` 附录速查表 | Dijkstra delay 标为 60.32ms（应为 60.77ms），来源引用 D024 实为 GRLR 结果 | LOW |
| 2 | `contract.md` vs 实际执行 | B=500MHz→1GHz(D015), hidden_dim=64→128(D018), PPO→监督(D018), 5seed→1seed | LOW（decision_log 已记录） |
| 3 | `02_method.md`/`06_formulas.md` | 参数量 ~71K vs 03_experiments 72,965 | LOW（四舍五入近似） |

### 核心数字验证

| 计算 | 公式 | 验证结果 |
|------|------|---------|
| 90.3% 保留率 | 60.32/66.77 = 0.9034 | ✅ 正确 |
| 9.9% vs Dijkstra | (66.77-60.77)/60.77 = 0.0987 | ✅ 正确 |
| 9.7pp stretch 差 | (1.097-1.000)*100 | ✅ 正确 |
| 2-4pp 多尺度贡献 | stretch: 2.3pp, ≤1.2x: 4.0pp | ✅ 在范围内 |

### 消融逻辑验证

- A1(无PE) stretch 1.002 ≈ Dijkstra：✅ 无 PE 退化为纯 Dijkstra，自洽
- A2(单尺度) stretch 1.120 > Full 1.097：✅ 多尺度改善 2.3pp，自洽
- A3(无PE+单尺度) stretch 1.049：✅ 介于 A1/A2 之间，自洽
- Same-scale stretch 1.000 vs Cross 1.097：✅ 9.7pp 差距完全来自跨规模迁移

**数据自洽性判定：WARN**（核心数字 PASS，3 处 LOW 级次要矛盾）

## 问题清单

### P0 CRITICAL — 必须修复才能投稿

| # | 问题 | 影响 | 补救方案 | 工作量 |
|---|------|------|---------|--------|
| P0-1 | **单 seed 评估** | 所有定量结论无统计显著性，审稿人必问 | 5 seeds 重跑 E01+A1-A3+Same，计算均值±std + Welch's t-test | 中（重跑，代码不改） |
| P0-2 | **p-value 缺失** | Contract 明确要求，逐流数据已有 | `scipy.stats.ttest_ind(gnn_delays, djk_delays)` 一行代码 | 低 |
| P0-3 | **M2 链路利用率** | Contract 定义核心指标，完全未报告 | ablation.py 路径追踪循环加 ~15 行：累加每边流量→计算利用率 | 低 |

### P1 IMPORTANT — 强烈建议修复

| # | 问题 | 影响 | 补救方案 | 工作量 |
|---|------|------|---------|--------|
| P1-1 | **E06 多流量模式** | 仅 uniform，hotspot 可能是 GNN 优势场景 | 实现 hotspot 流量生成器，重跑评估 | 中 |
| P1-2 | **E09 PE 类型对比** | 无法区分"轨道结构"vs"任意额外维度" | 替换为 random PE 重跑 A1 | 中 |
| P1-3 | **E07 24x 规模 (1584 星)** | 规模泛化上限未知 | 配置已定义，直接跑评估 | 低 |
| P1-4 | **E08 GNN 深度消融** | 感受野是否是跨规模瓶颈未回答 | 2/3/4 层 GAT 对比 | 中 |
| P1-5 | **推理延迟** | domain-comms.md §7 明确要求 | 加 time 计时，~5 行代码 | 低 |
| P1-6 | **CDF 图** | stretch 分布只有 3 个点值 | 从逐流 stretches 绘制 CDF | 低 |
| P1-7 | **收敛曲线** | 150 epoch 无 loss curve | 重跑时保存 loss history | 低 |

### P2 NICE-TO-HAVE — 锦上添花

| # | 问题 | 补救方案 |
|---|------|---------|
| P2-1 | 01_research_context.md Dijkstra delay 修正为 60.77ms | 改一处数字 |
| P2-2 | Contract 原文参数过时 | 加 amendment 备注 |
| P2-3 | 参数量统一为 72,965 | 统一 02/06 文件表述 |
| P2-4 | 拓扑可视化 | 可选 |
| P2-5 | ECMP/SPR baseline | 可选，Dijkstra 已是最强启发式 |

## 修复执行计划（全部补齐，按依赖排序）

用户决策：**全部修复，让论文无懈可击**。以下按执行依赖和投入产出排序，等待三章审计全部完成后统一规划执行。

### Phase A：代码改造（一次性，所有后续实验共用）

| 序号 | 改造项 | 对应问题 | 工作量 | 说明 |
|------|--------|---------|--------|------|
| A1 | 添加 M2 链路利用率追踪 | P0-3 | ~15 行 | ablation.py 路径追踪循环内累加每边流量→利用率 |
| A2 | 添加推理延迟计时 | P1-5 | ~5 行 | torch.cuda.synchronize() + time.perf_counter() |
| A3 | 添加逐流统计输出 | P0-2, P1-6 | ~10 行 | 输出 all_stretches/all_delays 到文件，供 CDF + t-test |
| A4 | 添加 loss history 保存 | P1-7 | ~5 行 | pretrain.py 训练循环中保存 epoch_loss 列表 |
| A5 | 添加多 seed 支持 | P0-1 | ~10 行 | 脚本参数化 seed，5 seeds: [123, 42, 0, 2024, 9999] |
| A6 | 添加 hotspot 流量生成器 | P1-1 (E06) | ~30 行 | 基于经纬度的非均匀流量分布 |
| A7 | 添加 random PE 对照 | P1-2 (E09) | ~15 行 | 与 Orbital PE 同维度但随机初始化 |

**预估总代码量**：~90 行，可在 1 个对话内完成并验证。

### Phase B：实验重跑（依赖 Phase A 完成后）

所有实验均使用 5 seeds，报告均值±标准差 + Welch's t-test。

| 序号 | 实验 | 对应问题 | 依赖 | GPU 时间估算 | 说明 |
|------|------|---------|------|------------|------|
| B1 | E01 核心跨规模泛化 × 5seeds | P0-1 | A1-A5 | ~2h/seed × 5 = 10h | 最关键，必须第一个跑 |
| B2 | A1 消融(无PE) × 5seeds | P0-1 | A1-A5 | ~1.5h/seed × 5 = 7.5h | PE 必要性论证 |
| B3 | A2 消融(无多尺度) × 5seeds | P0-1 | A1-A5 | ~1.5h/seed × 5 = 7.5h | |
| B4 | A3 消融(无PE+无多尺度) × 5seeds | P0-1 | A1-A5 | ~1.5h/seed × 5 = 7.5h | |
| B5 | Same-scale 对照 × 5seeds | P0-1 | A1-A5 | ~2h/seed × 5 = 10h | |
| B6 | E06 hotspot 流量 × 5seeds | P1-1 | A1-A6 | ~2h/seed × 5 = 10h | |
| B7 | E07 1584 星泛化 × 5seeds | P1-3 | A1-A5 | ~3h/seed × 5 = 15h | 更大星座，更慢 |
| B8 | E08 GNN 深度(2/3/4层) × 5seeds | P1-4 | A1-A5 | ~2h/seed×3×5 = 30h | 3 种深度各 5 seed |
| B9 | E09 random PE 对照 × 5seeds | P1-2 | A1-A5, A7 | ~1.5h/seed × 5 = 7.5h | |

**总 GPU 时间估算**：~105h（RTX 4070）。可分批串行或部分并行。

**执行顺序建议**：
1. B1 + B2 + B5（核心实验 + PE 消融 + 同规模对照）— 最关键的三项
2. B3 + B4 + B9（剩余消融 + random PE）— 补全消融矩阵
3. B6 + B7（流量模式 + 1584 星）— 扩展泛化范围
4. B8（GNN 深度）— 最耗时，可最后跑

### Phase C：可视化与分析（依赖 Phase B 数据）

| 序号 | 产出 | 对应问题 | 说明 |
|------|------|---------|------|
| C1 | stretch CDF 曲线 | P1-6 | Full/A1/A2/A3/Same 五条 CDF 叠加 |
| C2 | 收敛曲线 | P1-7 | 5 seeds 的 loss curve + 标准差带 |
| C3 | 消融对比柱状图 | 综合 | mean stretch ± std，5 组柱 |
| C4 | 规模泛化曲线 | 综合 | 66→100→200→720→1584（如有）stretch 趋势 |
| C5 | 统计检验汇总表 | P0-2 | 每对比较的 p-value + significance |
| C6 | 链路利用率分布 | P0-3 | M2 histogram 或 CDF |

### Phase D：文档修复（可与 Phase B/C 并行）

| 序号 | 修复项 | 对应问题 | 工作量 |
|------|--------|---------|--------|
| D1 | 01_research_context.md Dijkstra delay 60.32→60.77 | P2-1 | 改 1 处 |
| D2 | Contract 加 amendment 备注（参数变更） | P2-2 | 加 1 段 |
| D3 | 参数量统一为 72,965 | P2-3 | 统一 02/06 文件 |
| D4 | paper_materials 全部数字更新为 5-seed 均值±std | 综合 | Phase B 数据就绪后 |

### 工作量总估算

| 阶段 | 代码 | GPU 时间 | 人工时间 |
|------|------|---------|---------|
| Phase A 代码改造 | ~90 行 | - | 1 对话 |
| Phase B 实验重跑 | - | ~105h | 启动后自动运行 |
| Phase C 可视化 | ~100 行 | - | 1 对话 |
| Phase D 文档修复 | 改几处 | - | 0.5 对话 |

### 风险与注意事项

1. **M2 可能暴露弱点**：加权 Dijkstra 每次选同一路径，链路利用率可能不均。如 M2 差，论文需显式讨论"stretch 优化 vs 负载均衡"的 trade-off。
2. **B8 GNN 深度消融耗时最长**（30h），如果时间紧张可先跑 2 层 vs 3 层的 2 组对比。
3. **多 seed 方差**：如果 5 seeds 方差较大（std > 均值的 10%），需要增加到 10 seeds 或检查训练不稳定性。
4. **E07 1584 星可能 OOM**：720→1584 是 2.2x 节点数，GNN 显存需求约 5x。需先测试单 seed 是否能跑通。

## 决策引用

- 无新建决策

## 范围确认

- 本轮在 scope boundary 内：是（Ch1 质量审计，不涉及写作或其他章节）

## 后续

1. 等待 Ch2(S003)、Ch3(S004) 审计完成
2. 三章修复计划汇总后统一排期
3. 跨章一致性检查（H004）在三章修复完成后执行
4. Phase A 代码改造可在任意时机启动（不依赖其他章节审计）
