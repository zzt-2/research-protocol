# Handoff: 从真实地基进入 Direction Lab

> 来源: S003 / V006 | 交接目标: 将双偏振星地 OSL Groundwork 的既有资产导入 Direction Lab，开始第一轮真实候选族批量推进
> 文件名: H004-live-foundation-run.md

## 已完成边界

- H003 真实 shadow 观察完成 5 个主循环：controller 路由率 100%，P0 进入 trusted evidence 为 0；整体仍因恢复样本不足 3 次而为 PARTIAL。
- 当前 pilot v1 固定在 `44adff7`，不在真实使用期修改 controller、schema 或提示词护栏。
- 双偏振星地 OSL Groundwork 是真实地基：它冻结场景、baseline、指标、有效域和已知死路，但不封闭 ML 候选空间。既有候选族地图只是种子视图，不是“所有可用 ML 方法”的全集。

## 不要做什么

- 不把双偏振 OSL 项目当作从零 GW；优先复用已有候选地图、baseline 审计、失败结论和文献证据。
- 不把既有 CMA-fade/SOP/pilot 候选地图误当成完整研究空间；必须重新做一次全处理链 ML Candidate Universe 盘点。
- 不把旧的 pilot-Jones 或 Q-DP4 等已 Kill/DEFER 路线当作新贡献重新包装。
- 不绕过候选族地图直接挑一个方法深挖；不得单点正信号劫持主线。
- 不把 current-CMA/no-z 当 standard baseline；standard-CMA（含 z）与 ML 的固定标签指标口径必须分开。
- 不在候选地图和 batch queue 未重建前启动正式性能批次；不跳过必要的文献/证据门控。
- 不把真实运行中的性能数字自动写入论文材料；promotion 仍需独立 verifier 和人工决策。

## 必读

1. `.sessions/2026-07-17-direction-lab-governance-pilot/topic-index.md`
2. `.sessions/2026-07-17-direction-lab-governance-pilot/H004-live-foundation-run.md`
3. `.sessions/2026-07-17-direction-lab-governance-pilot/S003-live-shadow-observation.md`
4. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`
5. `projects/thesis-fso/master-state.md`
6. `.sessions/framework-evolution/R002-direction-lab-design.md`
7. `projects/simulation/verify/direction_lab_pilot/controller.py`

## 接口变更（如有代码改动）

无。真实运行固定复用 pilot v1 的 controller/receipt/evidence gate；新建的 Direction Lab 状态和 manifest 只能写入隔离目录。

## 失败数据附录（如涉及路线失败）

双偏振 OSL 地基已有多条明确负面结论，必须作为先验导入而不是重复运行：Batch 1 fade/clip 低信息；Batch 2 fG 无事件；基础盲 detector FAIL；Stokes-like pilot PARTIAL/stopped；pilot-Jones generic 机制撞车且 Step4a 仍封锁；Q-DP4 约束和回滚形态 Kill。具体以地基 topic-index/master-state 为准。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 地基 master-state 与新 Direction Lab state 尚未统一 | 唯一机器状态源 | 导入阶段 | 首轮建立 anchor snapshot 后复核 |
| manifest/receipt 无签名或不可变 registry | 正式证据需可信来源 | pilot 已知债务 | 不阻塞隔离批量探索，进入正式 promotion 前解决 |
| Round 4 恢复样本不足 | 长期可靠性未证 | PARTIAL | 真实运行中至少再做 2 次恢复 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 地基导入 | anchor 覆盖 baseline、候选族、有效域、dead ends、pending | R002 / 地基 topic-index | 未测 |
| 批次门 | CandidateMap + BatchQueue 完成后才允许 RUN | R002 | 未测 |
| 基线一致性 | standard-CMA/ML/fixed-label/PI 四者身份与指标口径可追溯 | 地基 D040/D045 | 未测 |
| 真实运行路由 | 运行循环中 controller 路由率 ≥90% | H003 | 100% shadow |
| 晋级 | 独立 verifier PASS，且未违反地基明确不含/DEFER/KILL | R002 + 地基不变量 | 未测 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

一个主对话连续完成：读取地基 → 生成 anchor snapshot → 枚举全处理链 ML Candidate Universe → 合并既有候选/失败/待测项 → 中性分类和全景排序 → 生成 BatchQueue → 只运行第一批小型 paired batch → 独立 verifier → 分析主对话历史。第一轮不做论文输出，不扩展出双偏振星地 OSL 场景。

## 可直接粘贴的新对话提示词

你现在把 Direction Lab pilot v1 用到真实研究地基上。主线地基是 `.sessions/2026-07-10-dual-pol-osl-groundwork/` 的双偏振星地 OSL Groundwork。

核心研究目标是：系统寻找 **ML 在这个场景下的任何合理应用、方法或改进**。地基只冻结场景、baseline、指标、已有证据和已知死路，不限制候选只能来自 CMA-fade、SOP、pilot-Jones 或已有 CandidateMap。既有候选地图是种子，不是封闭全集。

先读取并核验：

1. `.sessions/2026-07-17-direction-lab-governance-pilot/topic-index.md`
2. `.sessions/2026-07-17-direction-lab-governance-pilot/H004-live-foundation-run.md`
3. `.sessions/2026-07-17-direction-lab-governance-pilot/S003-live-shadow-observation.md`
4. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`
5. `projects/thesis-fso/master-state.md`
6. `.sessions/framework-evolution/R002-direction-lab-design.md`
7. `projects/simulation/verify/direction_lab_pilot/controller.py`

读取后先核验至少 5 条地基事实：候选族地图状态、Batch 0.5/1/2 状态、已 Kill/DEFER 路线、standard-CMA 与 current-CMA 的区别、fixed-label 与 PI-BER 双口径。若地基文件互相冲突，先登记冲突并阻断下游，不自行猜测。

本轮目标是“复用地基，建立完整 ML 候选宇宙，并启动第一批真实候选族探索”。按顺序做：

1. 在隔离的 Direction Lab 目录生成 anchor snapshot，引用而不复制地基事实；
2. 沿完整处理链枚举 ML 应用点，包括但不限于：信道/状态估计、偏振解复用与均衡、定时/载波恢复、检测与软解调、译码辅助、链路监测、异常/失锁检测、在线自适应、复杂度控制、pilot/数据效率、跨参数泛化、联合模块优化；方法可包括监督/自监督/无监督、physics-informed、deep unfolding、equivariant、meta/online learning、生成式方法、混合 model-based/ML 等；
3. 对每个应用点继续枚举可改进维度：性能、鲁棒性、泛化、收敛、样本效率、pilot 开销、复杂度、时延、可解释性、校准和失效检测；纯硬件/纯协议旧排除不阻止其中可落到软件侧的 ML-assisted 变体进入地图；
4. 将新枚举结果与已有候选、失败路线、observation-only、DEFER 和待测项合并。旧 Kill 只否决原来的具体 M-C-A 和有效域，不能自动 Kill 整个 ML 方法族；
5. 完成中性扫描和全景分类后再统一排序，生成 BatchQueue，明确第一批并行候选、共享 baseline、seed、主指标、诊断指标、Go/Kill 条件；
6. 在 CandidateMap 和 BatchQueue 通过门控前，不运行正式批次；
7. 门控通过后只跑第一批小型 paired batch，所有动作走 controller/receipt/evidence gate，结果留在隔离目录；
8. 由独立 verifier 审查，不把任何数字直接写入论文材料；
9. 在同一主对话分析整个过程：AI 是否真正展开了 ML 全空间、是否仍被 CMA/pilot 旧路径锚定、哪些字段负担过重、是否出现新绕过。

硬约束：不把 current-CMA/no-z 当 standard；不复活已被否决的具体 M-C-A，但也不把局部 Kill 扩大成整个 ML 方法族禁令；不把已有候选地图当封闭全集；不跳 Candidate Universe/CandidateMap/BatchQueue；不修改 canonical baseline；不把真实性能结果自动晋级论文；不创建 skill；普通失败记录后换同族其他机制或下一候选，只有 P0 数据完整性或范围冲突才暂停。
