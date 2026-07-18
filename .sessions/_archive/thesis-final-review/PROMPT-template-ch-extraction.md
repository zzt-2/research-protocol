# Paper-Materials 重新提取 PROMPT 模板

> 本模板用于三章论文素材重新提取。每章一个对话，由本模板 + 章节参数组成。
> 设计于 S015（thesis-final-review），基于 thesis-platform 新工作流的 A-G 格式。

---

## 使用方法

新对话启动时，复制本模板，将 `{章参数}` 替换为实际值，作为第一条消息发送。

---

## 对话任务

将终审 14 轮对话的全部结论整合进 A-G 格式的 materials.md。产出是给论文写作管线消费的标准化输入。

**核心原则**：终审结论 > 旧 paper-materials > 原始项目文件。三者矛盾时以终审结论为准。

---

## 产出格式：A-G 单文件

产出文件：`projects/{project}/paper_materials/materials.md`

### 板块 A: 研究问题与论证逻辑

```
## A. 研究问题与论证逻辑

### A.1 问题定义
- 一句话定义 + 展开说明（附关键数据）
- 研究挑战的量化锚点

### A.2 现状局限
- 每条附 cite key，纯定性叙述（禁止嵌入具体数值）
- 局限来源标注（哪篇论文的什么结论）

### A.3 研究空白
- 空白陈述 + 证据（检索覆盖范围 + 未命中确认）
- 空白的结构性原因

### A.4 论证主线
- 2-4 句纯定性叙述
- 论证模式：{论证模式}

### A.5 Gap-Contribution 闭环映射表
| 空白(Gap) | 方法组件 | 结论回应 | 数据证据(板块E编号) |
|-----------|---------|---------|-------------------|
```

### 板块 B: 文献格局

```
## B. 文献格局

### B.1 文献角色速览
| cite key | 一句话贡献 | 与本研究关系 | 引用角色 |
|----------|-----------|------------|---------|

引用角色：竞品/替代方案、前驱/基础、理论/方法支撑、背景/综述
文献缺口标注 ⚠

### B.2 竞品精确区分
| 论文 | 覆盖要素 | 缺失要素 | 威胁等级 | 我们的优势 |
|------|---------|---------|---------|-----------|
```

### 板块 C: 贡献与核心论据

```
## C. 贡献与核心论据

### C.1 贡献声明
（每条附支撑证据计数 + 摘要级关键指标，不含完整实验设置和统计检验细节）

### C.2 贡献间关系
（递进/互补/独立的逻辑关系）

### C.3 证据蓝图
| 贡献 | 核心证据(板块E编号) | 补充证据(板块E编号) |
|------|-------------------|-------------------|
```

### 板块 D: 方法描述

```
## D. 方法描述

### D.1 架构总览
（流程描述，不含图）

### D.2 核心组件
（每个组件：动机 + 公式 + 设计理由）

### D.3 设计决策表
| 选择 | 理由 | 排除的替代方案 | 支撑 cite key |
|------|------|--------------|--------------|
```

### 板块 E: 证据目录

```
## E. 证据目录

### E.core 核心证据（支撑主要贡献的 10-15 条，完整展开）
### E.supplement 补充证据（其余，可折叠）

每条证据格式：
### [纯定性标题]
- 证据类型：定量数据 | 质性发现 | 统计结果 | 设计产物
- 内容：[按类型适配]
- 完整上下文：[前提条件、对比基线、适用范围]
- 来源：[本论文实验 cite key / 引用文献]
- 支撑论点：[哪个贡献声明]
- 统计显著性：[p值/CI]（如适用）
```

### 板块 F: 术语与符号

```
## F. 术语与符号

### F.1 术语表
| 术语 | 英文 | 缩写 | 定义 |
|------|------|------|------|

### F.2 符号表（采用跨章统一方案）
| 符号 | 含义 | 单位 | 值/范围 | 首现章节 |
|------|------|------|---------|---------|
```

### 板块 G: 实验设计

```
## G. 实验设计

### G.1 仿真环境参数表
（每个参数标注来源：contract/计算/文献）

### G.2 对比对象/Baseline
（含公平性声明）

### G.3 评估标准
（主指标 + 辅助指标 + 统计方法）

### G.4 控制变量
```

### 缺失处理
- 缺失板块写 `⚠ 缺失：[一句话描述]`，不展开空模板
- 缺失证据写 `⚠ 缺失`，不推断具体内容

---

## 跨章统一约束（每章提取时必须遵守）

### 符号统一（来自 S011）

| 符号 | 统一方案 |
|------|---------|
| $N$ | Ch1: $N_{\text{sat}}$, Ch2: $N_{\text{UE}}$, Ch3: $N_{\text{node}}$ |
| $h$ | 轨道高度→$h_{\text{orb}}$，隐层维度→$d_h$ |
| $B$ | Ch1: $B_{\text{ISL}}$, Ch2: $N_{\text{blk}}$, Ch3: 带宽加链路下标 |
| $H$ | Ch2 切换数→$N_{\text{ho}}$, UAV高度→$h_{\text{UAV}}$ |
| GNN层数 | 统一用 $L$ |
| 奖励权重 | 统一 $\eta$ 加语义下标 |
| 节点集 | 统一花体 $\mathcal{V}, \mathcal{E}$ |
| $K$ | Ch2 top-K 候选, Ch3 Rician→$K_R$ |
| $f$ | Ch1 PE频率参数, Ch3 载波频率→$f_c$ |

### 元分析框架（来自 S012）

统一论点："GNN 有效性取决于架构复杂度与任务需求的匹配"

| 章 | 叙事定位 | GNN 优势条件 | 统一解释 |
|---|---------|------------|---------|
| Ch1 | 规模不变性 | 同构 GAT + 规则拓扑 + PE | 4-neighbor 结构完全不变→泛化成功 |
| Ch2 | 排列等变性/规模适应性 | 二部图 + N>30 | 卫星侧固定，UE 侧增加同类节点 |
| Ch3 | 故障弹性 | 故障打破拓扑规则性 | 结构漂移导致复杂模型退化 |

### 贡献定位（来自 S011-8f + S012）

| 章 | 定位 | 适合动词 | 禁用动词 |
|---|------|---------|---------|
| Ch1 | 系统性验证 | evaluate, demonstrate, apply | invent, pioneer, 首次 |
| Ch2 | 规模适应性实证 | investigate, design, evaluate | create, discover |
| Ch3 | 故障弹性实证 | evaluate, show, leverage | originate, devise |

### 两种规模泛化命名（来自 S011-8d）

- Ch1: 星座规模泛化 / Constellation-size generalization
- Ch2: 用户规模泛化 / User-density generalization

### 延迟模型差异（来自 S014）

- Ch1: E2E delay = Σ(ISL 传播时延)，无拥塞建模
- Ch2: 无 E2E delay 指标（主指标为 composite reward）
- Ch3: E2E delay = Σ(传播时延 × 1/(1-util))，拥塞惩罚权重（非物理排队延迟）

### 统计报告标准（来自 S007 + S008）

- 3 seeds + mean ± std + bootstrap 95% CI + Welch's t-test
- 统一以 stat_tests.json 为权威数据源（不使用旧 paper-materials 中的 std）

---

## 子 Agent 策略

### 原则
- 每个 agent 输入控制在 ~50K
- 按内容量分组，不按文件类型分组
- 每个 agent 返回结构化摘要，不返回原始内容
- 一批最多 3 个 agent 并行

### 执行顺序

**第一批（3 agents 并行）**：A0 + A1 + A2
**第二批（2-3 agents 并行）**：A3 + A4 + A5（如适用）
**主线程**：读跨章上下文 → 接收所有 agent 摘要 → 合成 materials.md

### Agent 分组

#### A0 写法规范（通用，每章都跑）
- 输入：S007(41K) + R003(5K) + thesis-structure-research/topic-index(3K) = **~49K**
- 输出：贡献声称模板 + 统计惯例 + 图表惯例 + 局限性写法范例 + 结构参考
- 产出供主线程合成时参照

#### A1 终审结论（章相关，见下方章节参数）
- 输入：thesis-final-review 中本章相关的 session 文件 + thesis-chapter-fixes 中本章相关内容
- 输出：按主题分类的结论清单（贡献定位 / 数据修正 / 竞品更新 / 已知问题）

#### A2 核心素材-上（章相关，见下方章节参数）
- 输入：旧 paper_materials 的 01+02+06 + contract
- 输出：研究问题 + 方法 + 公式 的结构化摘要

#### A3 核心素材-下+数据（章相关，见下方章节参数）
- 输入：旧 paper_materials 的 03+05 + feasibility + stat_tests
- 输出：实验结果 + 局限性 + 验证后数据表

#### A4 文献索引（章相关）
- 输入：旧 paper_materials/04
- 输出：文献角色分类 + 竞品区分表

#### A5 文献笔记+补充（Ch1/Ch2 有，Ch3 不同）
- 输入：literature_notes + (Ch2: novelty_search)
- 输出：补充文献格局 + 新颖性论证

### 主线程职责

读以下跨章上下文（~37K，直接读不委托 agent）：
- thesis-final-review/topic-index.md (12K) — 61 条结论 + 不变量
- S011 (6K) — 符号统一 + 元分析框架
- S014 (11K) — 一致性检查
- thesis-structure-research/topic-index.md (3K) — 结构研究
- 本模板 + handoff (~5K)

然后：接收所有 agent 摘要 → 合成 A-G materials.md → 质量自检

### 时间顺序提醒
- thesis-final-review 的结论**覆盖** thesis-chapter-fixes 的早期结论
- Ch3 特别注意：thesis-chapter-fixes 中的 Ch3 session 全部针对旧项目(hgat)，对新 Ch3(leo-congestion-routing)无用
- S005、S009 是基于错误理解的日志（S005=旧hgat技术审查，S009=训练数据误判），不要读
- 以 thesis-final-review 的 topic-index 为权威索引

---

## 质量门槛

- [ ] 总量 10-20K 字（含全部板块）
- [ ] 每条论据有 cite key 或 ⚠ 标注
- [ ] 关键数据与 stat_tests.json 完全一致（mean 值）
- [ ] 符号表采用跨章统一方案
- [ ] 贡献声称符合 R003 写法约束（无过度声称）
- [ ] 板块 A 纯定性（无具体数值）
- [ ] 板块 C 摘要级（无完整实验设置/统计检验细节）
- [ ] 完整证据条目只在板块 E 出现一次
- [ ] 跨板块事实陈述不矛盾
- [ ] 缺失板块标 ⚠ 缺失，不编造
- [ ] 文献只有 literature_notes 中的 cite key，不自造

---

## 输出位置

`projects/{project}/paper_materials/materials.md`

旧 01-06 文件保留不删除（供参考），但新产出是 materials.md。

---

## 章节参数

### Ch1: leo-mega-constellation-gnn-routing

**项目目录**: `projects/leo-mega-constellation-gnn-routing/`
**论证模式**: 空白填补型（实证）
**贡献定位**: GNN 跨规模路由的系统性验证

| Agent | 输入文件（完整路径省略 projects/leo-mega-constellation-gnn-routing/） | 大小 |
|-------|----------------------------------------------------------------|------|
| A1 终审+决策 | .sessions/thesis-final-review/{S002,S003,S004,S006,S008}.md + .sessions/thesis-chapter-fixes/topic-index.md + decision_log.md | ~48K |
| A2 问题+方法+公式 | paper_materials/{01,02,06}.md + contract.md | ~49K |
| A3 实验+局限+数据 | paper_materials/{03,05}.md + feasibility_report.md + simulator/results/stat_tests.json | ~52K |
| A4 文献索引 | paper_materials/04_literature.md | ~37K |
| A5 文献笔记 | literature_notes.md | ~49K |

**Ch1 特有注意事项**:
- 3-seed 数据替换旧单 seed（S004 已完成）
- size generalization 非 LEO 路由公认挑战，叙事定位为"跨领域迁移验证"
- 贡献从"首次创新"降级为"系统性验证+实证"
- Li 2026 已排除（非竞品），不要引用
- PE 是学习前提（非增强），消融故事调整
- Walker-Delta 理论声称降级为"有利条件"
- delay retention rate 为自造指标，需标注
- 不读 ch1_multi_seed_results.json（488K 太大），stat_tests.json 已有汇总

### Ch2: leo-ntn-handover-drl

**项目目录**: `projects/leo-ntn-handover-drl/`
**论证模式**: 空白填补型（实证）
**贡献定位**: 二部图 GNN 在多 UE 切换中的规模适应性

| Agent | 输入文件（完整路径省略 projects/leo-ntn-handover-drl/） | 大小 |
|-------|----------------------------------------------------------|------|
| A1 终审+领域验证 | .sessions/thesis-final-review/{S001,S003,S006,S008}.md + .sessions/thesis-chapter-fixes/{S006,topic-index}.md | ~50K |
| A2 问题+方法+公式 | paper_materials/{01,02,06}.md + contract.md | ~40K |
| A3 实验+数据 | paper_materials/03_experiments.md + baseline_report.md + execute_progress.md + results/stat_tests.json | ~44K |
| A4 文献+局限 | paper_materials/{04,05}.md | ~41K |
| A5 新颖性+文献笔记 | novelty_search.md + literature_notes.md | ~49K |

**Ch2 特有注意事项**:
- eps_decay=5 旧数据不可靠（固定 episode seed），只用 eps_decay=20 数据
- 20UE GNN vs MLP 不显著(p=0.76)，叙事侧重 50UE + size gen 稳定性
- 50UE GNN +21.2% vs MLP (p=0.007)
- Retention 定义：per-UE 为 88%/71%（非总 reward 的 218%/340%）
- Lee & Lim 2025 为最直接竞争者（旧标记"非二部图"→实际用二部图，已修正）
- Xie 2023 + Yin 2022 为先例，新颖性需引用限定
- Jain's fairness 降级（通行率仅 17%），补 system throughput
- **size gen retention 数据来自单模型（seed=3），模型保存 bug 未修复**：在材料中标注"单模型结果，未经 3-seed 统计验证"
- 100UE 同规模训练失败可接受（文献无此先例）
- design_A.md 和 design_C.md 不读（设计决策已在 decision_log + contract 中覆盖）
- stat_tests.json 路径：`results/stat_tests.json`（非 simulator/results/）

### Ch3: leo-congestion-routing

**项目目录**: `projects/leo-congestion-routing/`
**论证模式**: 空白填补型（实证）
**贡献定位**: 故障弹性路由的实证分析

| Agent | 输入文件（完整路径省略 projects/leo-congestion-routing/） | 大小 |
|-------|----------------------------------------------------------|------|
| A1 终审结论 | .sessions/thesis-final-review/{S013}.md + {H002,H003}.md + topic-index.md(取 S012 结论段落) | ~30K |
| A2 旧素材+设计 | paper-materials.md + contract.md + data-flow.md | ~44K |
| A3 文献笔记 | literature_notes.md | ~58K |
| A4 决策+可行性+数据 | decision_log.md + feasibility_report.md + simulator-design.md + simulator/results/stat_tests.json + baseline_report.md | ~49K |

**Ch3 特有注意事项**:
- 项目从 hgat-satellite-dag-offloading 替换为 leo-congestion-routing（S012 决策）
- **不读 S005、S009**（旧 hgat 技术审查 + 训练数据误判，与当前 Ch3 无关）
- **不读 thesis-chapter-fixes 的 Ch3 session**（S002/S003 全部针对旧 hgat）
- S011 的 Ch3 部分针对旧 hgat，以 S013 为 Ch3 权威来源
- E2E delay = 传播延迟 × 拥塞惩罚权重 1/(1-util)（非 M/M/1 排队，S013-5b 修正）
- 贡献~80% 来自故障场景：无故障 GNN/ECMP≈1.0（ECMP 略优），8% 故障 delay -20%
- GNN vs ECMP MLU 不显著(p=0.26)，论文如实报告，强调 delay
- 跨规模：48/288 有效(delay 优势 17%-75%)，720 退化(10.9x 跨度过大)
- 节点特征文档 vs 代码不匹配已修（S013-P0-3，data-flow.md 已更新）
- E02 vs E08@0% 数据矛盾已说明（实验批次差异，S013-P0-2）
- 缺 06_formulas_symbols.md，需在板块 F 中创建（采用 S011 统一符号）
- 合规 6/8 PASS（baseline 数量和训练详情为 PARTIAL）
- Ch3 不使用 Shannon/FSPL（固定容量 10Gbps），物理层与 Ch1/Ch2 根本不同
- 轨道倾角 86.4°（vs Ch1/Ch2 的 53°），有意设计产生极地间隙
- stat_tests.json 路径：`simulator/results/stat_tests.json`
- 不读 analysis_f4_generalization.md（内容已被 S013 覆盖）
- 不读 master-state.md（编排状态，非素材）
- literature_notes.md 58K 超过 50K 目标，但为单文件无法拆分
