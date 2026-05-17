# Contract（冻结）

> 冻结研究假设和实验方案。Contract 冻结后 Execute 阶段不允许修改假设/signal/fairness rules（事实性参数修正见 Amendment 机制）。
> 通信领域研究：额外阅读 `domain-comms.md` 中的指标体系和推荐技术栈。

---

## 目标

冻结经过验证的研究假设和实验方案，为 Execute 阶段提供不可变的执行基准。"经过验证"指参数已溯源、数据流已推演、反模式已排查。

## 输入

Groundwork 全部产出（literature_notes.md + baseline_report.md + feasibility_report.md + decision_log.md）

[MUST] `feasibility_report.md` 中 Go/No-Go 决策为 Go 方可进入 Contract 阶段。

## 输出

`contract.md`（核心工件）+ `data-flow.md`（端到端推演）+ `decision_log.md`（追加）

## 人介入点

[MUST] Contract 冻结前用户必须确认。这是最关键的人介入点。

---

## Step 0：方案新颖性检索

[MUST] 在形成假设前，必须确认候选方案的新颖性。流程：

### 复用条件

如果 Groundwork 阶段已完成（literature_notes 含 ≥8 篇精读 + Step 3.5 已完成）：
- **跳过 0.1 系统检索**，直接复用 GW 检索结果
- **简化 0.2 竞品精读**，仅补充 GW 未覆盖的 Contract 特有竞品（如相同方法在不同场景的应用）
- **保留 0.3 二轮定向检索**，但范围收窄到 Contract 特有的新颖性验证

[MUST NOT] 浅搜后直接派设计子对话。必须走完 0.1→0.2→0.3 三步后，再派设计子对话。

[通用] 所有写入文件的论文 URL 必须先验证标题匹配，错误的 URL 会浪费子对话上下文。

### 0.1 系统检索（使用项目脚本）

[MUST] 使用 `bash tools/search` 而非 WebSearch（检索流程参见 gw-search.md），因为脚本支持 5 源聚合（S2 + OpenAlex + arXiv + SerpAPI + Tavily）、去重、相关性评分、引用链展开。

```bash
bash tools/search "LEO satellite handover attention DQN" \
  --preset scenario-method --top 30 --year-from 2024 -o search-archive/{date}/contract-xxx.json
```

每个候选方案至少 3 组关键词。推荐预设：`scenario-method`（拆分场景+方法）。

[MUST] 新颖性检索结果中正式发表文献占比应 ≥50%。如预印本占主导，需针对核心方法补充正式发表的类似方法检索。
判断依据：DOI 非 arXiv（10.48550）+ venue 为正式期刊/会议名。

### 0.2 竞争者精读 + 摘要缓存（精读流程参见 gw-read.md）

[MUST] 对检索命中的直接竞争论文，在主对话中用 web reader 精读并**将架构摘要写入文件**（而非仅存在上下文中）。摘要文件供后续设计子对话直接读取，避免子对话重复消耗上下文。

摘要文件路径：`projects/{name}/competitor_notes/{作者姓氏}_{年份}.md`

摘要必须包含：网络架构图、attention/GNN 模块具体结构、观测/动作/奖励定义、与候选方案的重叠度评估。

### 0.3 二轮定向检索（检索流程参见 gw-search.md）

[MUST] 精读后如果发现特定技术细节需要进一步确认（如"cross-attention 在卫星选择中是否已有"），派子 agent 做定向补充检索。搜索关键词从精读发现中提炼，而非泛泛搜索。

二轮检索结果追加到 `competitor_notes/` 和 `decision_log.md`。

### 0.4 并行方案设计

[SHOULD] 多个候选方案需要并行深入设计时，遵循以下规则：

1. **独立输出文件**：每个方案写独立设计文件（`design_A.md` / `design_C.md`），**不共享同一文件**，避免并发写冲突
2. **上下文预算**：子对话 prompt 分两阶段——
   - Phase 1：读已缓存的 `competitor_notes/` 文件，**不重复 web reader 读论文全文**
   - Phase 2：基于缓存摘要做架构设计和差异化分析

---

## Step 1：形成假设

[MUST] 假设指向一个可量化的预测。不是"改进性能"而是"在 X 场景下 SNR 提升 ≥3dB"。

假设来源应该是 Groundwork 中发现的研究空白或改进空间，而不是凭空提出。具体来说：
- 从 literature_notes 的"已知局限"中识别研究空白
- 从 baseline 复现中确认改进空间确实存在
- 从仿真环境验证中确认实验条件能支撑假设

---

## Step 2：起草 Contract（draft 状态）

[MUST] 按 `templates.md` 中 contract 模板填写所有字段。

### 关键字段要求

- **hypothesis**：可量化的预测
- **success_signal**：定量阈值 + 评价指标 + 场景。例如"在 SNR 0-20dB 范围内，RMSE 降低 ≥15%"
- **failure_signal**：独立定义，不是 success 的反面。例如"核心方法 RMSE 与最简 baseline 差距 <5%"
- **baselines**：列出选定 baseline，包含交叉验证来源
  ```
  - B1: {名称} (来源: {论文/GitHub}) — 复现状态: {已复现/待复现} — 交叉验证: 被{N}篇论文使用
  ```
- **fairness_rules**：核心方法与 baseline 的公平对比规则（含信息泄露检查）
  - 相同数据划分、相同预处理、相同超参搜索预算
  - 处理组和对照组状态维度相同，差异仅在信息来源
  - 如存在不公平之处，显式声明
- **ablation_plan**：每个 ablation 消融什么、预期影响方向和大小
- **metrics**：评价指标列表（通信领域参考 `domain-comms.md` 中的指标体系）
- **simulation_config**：信道模型 + 参数 + 评估条件 + 数据集规模 + DL 配置
- **parameter_provenance**：每个仿真/DL 参数的出处（见 Step 3）

### Simulation Config 必填字段

所有通信研究必填：
- 信道模型及关键参数
- 评估条件（SNR 范围、场景列表）
- 数据集规模和划分方式
- DL 模型架构 + 训练配置（如适用）

按子领域扩展（参见 `domain-comms.md`）：
- 卫星通信：轨道参数（高度、倾角）、仰角范围、频段
- 随机接入：前导码数、RA 时隙长度、流量模型

粒度原则：足够让未参与研究的人复现实验，但不需要逐参数列举所有 ITU-R 输入。

### 数据集设计（自建数据集时必填）

如果研究需要自建数据集（非使用公开数据集），[MUST] 在 Contract 中包含"数据集设计"节（模板见 `templates.md` §contract），包含：
- 参数空间表：每个参数的取值范围和文献溯源
- 数据规模和划分方式
- 标注方案（如适用）

数据集设计直接支撑论文各章的实验设置节。参数溯源要求同 Simulation Config（每个参数需文献溯源/计算验证/设计选择三选一）。

> 注意：此步骤产出的 Contract 状态为 draft。Step 3-5 验证通过后才冻结。

---

## Step 3：实现性验算

> 起源：leo-mega-constellation-gnn-routing 项目中，Contract 冻结时 ISL 距离/模型/带宽三个参数错误，Execute 阶段才发现，导致仿真器重写。根源是 `[ASSUMPTION]` 标记的参数未经核实就冻进了 Contract。

**目的**：在冻结前，用最低成本（检索+计算）验证 Contract 中每个参数的真实性。

[MUST] 对 Simulation Config 中每一个涉及具体数值的参数，执行以下三选一：

| 验证方式 | 适用场景 | 输出 |
|---------|---------|------|
| **文献溯源** | 参数有论文出处 | `[来源: L{序号} §{章节}]` 或 `[来源: {论文} Table/Fig {N}]` |
| **计算验证** | 参数可从公式推导 | `[计算: {公式} 代入 {值}]` — 用子 agent 或 5 行 Python 验算 |
| **设计选择** | 无文献也无公式，属研究者的建模决策 | `[设计选择: {理由}]` — 必须附一段合理理由 |

**输出**：Contract 的 `parameter_provenance` 表更新，消除所有 `[ASSUMPTION]` 标记。模板见 `templates.md`。

### 执行方式

1. 列出 Simulation Config 中所有数值参数
2. 标注每个参数的当前状态（有来源 / `[ASSUMPTION]` / 未标注）
3. 对 `[ASSUMPTION]` 和未标注参数，派子 agent 并行核实（文献检索 + 计算）
4. 汇总核实结果，更新 parameter_provenance 表
5. 发现矛盾时（如文献值与 Contract 值不一致），标记为待决策项

### 门控条件

- [ ] 所有参数已消除 `[ASSUMPTION]`，每项有来源/计算/设计选择三选一
- [ ] 矛盾项已列出并经用户决策

> 为什么不直接冻假设再验参数：因为参数错误会导致假设本身不成立。ISL 距离算错 → 断链率算错 → 网络拓扑与假设不符 → 实验方案需要重来。先验参数再冻假设，成本更低。

---

## Step 4：端到端推演

> 起源：leo-mega-constellation-gnn-routing 项目中，Quick Test 暴露了三个设计遗漏：①模型缺少目的地 PE（不知道往哪走）②66 星配置 34.8% ISL 断链③混合 batch 不同配置导致 PE 维度不匹配。这些问题在纸笔推演中就能发现。

**目的**：不写代码，用纸笔走一遍"一个训练/推理样本从生成到评估的完整路径"，发现设计断层。

[MUST] 按以下顺序推演，每步检查"输入是否已在前面产出？维度/类型/范围是否匹配？"

```
1. 星座/网络配置 → 生成节点坐标/位置 → 计算连接关系 → 链路距离/容量
2. 流量/数据生成 → 选源/目的 → 构造需求
3. 状态构造：每个智能体/节点看到什么特征？→ 列出每个特征的维度和来源
4. 模型输入：网络收到什么？→ 画出 data flow（特征拼接/聚合/输出）
5. 模型输出：决策 → 如何映射到动作空间
6. 奖励/损失计算：用什么指标 → 如何从环境获取
7. 评估：M1-M5 怎么算 → 需要记录什么中间量
8. 跨规模泛化：训练配置 vs 推理配置，哪些维度变化（节点数/边数/特征维度）→ 模型如何处理
```

**输出**：`data-flow.md`（模板见 `templates.md`），记录每步的输入→处理→输出。

### 常见断层检查

| 断层类型 | 典型症状 | 本次起源 |
|---------|---------|---------|
| 特征缺失 | 模型缺少做决策所需的关键输入 | 缺少目的地 PE |
| 维度不匹配 | 消融实验移除某特征后维度坍缩 | E03/E05 消融维度问题 |
| 配置矛盾 | 某参数值在特定配置下产生矛盾 | 5000km 断链 vs 5500km 轨间距离 |
| 跨规模断裂 | 训练和推理的输入维度不一致 | 混合 batch PE 维度问题 |
| **表达力不足** | **模型动作空间严格弱于某个 baseline** | **单路径路由 vs ECMP 多路径分流** |

### [FR-13] 动作空间表达力下界审计

> 起源：leo-congestion-routing 项目中，Contract 假设"GNN ≥10% 优于 ECMP"，但 GNN 输出 per-edge 权重走单路径 Dijkstra，ECMP 走多路径分流。模型表达力严格低于 baseline，假设从结构上不可达。data-flow.md 检查了维度和特征完整性，但没检查行为语义。

[MUST] data-flow.md 必须包含"动作空间表达力审计"节，逐 baseline 检查模型的决策空间是否覆盖 baseline 的决策空间：

```markdown
### 动作空间表达力审计

| Baseline | Baseline 能做什么决策 | 模型能做什么决策 | 模型 ≥ Baseline？ |
|----------|---------------------|----------------|-----------------|
| B1: {名} | {baseline的决策能力描述} | {模型的决策能力描述} | {≥ / < } |
| B2: {名} | ... | ... | ... |
```

**判断标准**：
- 模型的决策空间**包含** baseline 的决策空间（模型能做 baseline 能做的一切，还能做更多）→ ≥
- 模型的决策空间与 baseline **不同但可比** → 需论证为什么在 success signal 的评估场景下模型仍能超越
- 模型的决策空间**严格弱于** baseline → <

**门控条件**：
- 全部 ≥ → 通过
- 任一 < → **必须**在 Contract 中标注为已知限制，并满足以下全部条件：
  1. 指出具体条件：在什么场景下模型仍能超越（如"当故障率 ≥5% 时等价路径不存在"）
  2. 该条件与 success signal 的评估场景一致
  3. 如果条件过于狭窄（如仅极端场景），考虑引入补偿机制（如 K-path splitting）或调整 success signal
- 无法满足上述条件 → 调整设计或调整假设

### 执行方式

1. 主对话在纸面推演，必要时派子 agent 验算特定步骤（如"66 星配置轨间距离均值是多少"）
2. 发现断层时，立即修正 Contract draft 对应字段
3. 推演完成后产出 `data-flow.md`

### 门控条件

- [ ] 8 步推演全部完成，每步有明确的输入→输出记录
- [ ] 所有断层已修正或标记为已知限制
- [ ] [FR-13] 动作空间表达力审计已完成，模型 < baseline 的项已标注为已知限制或已修正设计

---

## Step 5：压力测试 + 反模式审查

[MUST] 回答以下 5 问（前 4 问为选题压力测试，第 5 问为反模式审查），无致命风险信号才能通过：

1. **结构性优势**：核心方法 vs 最简 baseline 的结构性优势在哪？
   - 如果只是"用 DL 替代传统方法"而没有解释为什么 DL 适合这个问题 → 高风险

2. **边际结果**：结果仅边际优于 baseline（如 <5%）时，成果还能否成立？
   - 如果边际结果无法支撑任何有价值的结论 → 高风险

3. **信号独立性**：success/failure 信号是否独立且可操作？
   - failure_signal 不能只是 success_signal 的否定

4. **Baseline 共识性**：选定的 baseline 是否是领域共识？
   - 交叉验证数据：被几篇论文使用、是否有代码
   - 如果 baseline 是某篇论文自创的对比方法而非领域通用方法 → 需要额外论证

5. **反模式排查**（详细案例见 `domain-comms.md` §5）：

   | # | 反模式 | 检查内容 | 状态 |
   |---|--------|---------|------|
   | 1 | 信息泄露 | 处理组和对照组状态维度相同？消融实验维度一致（用零向量而非删除）？ | ☐ |
   | 2 | 仿真过于简化 | 仿真器是否包含目标方法所擅长处理的信号特征？流量强度是否足以产生差异化？ | ☐ |
   | 3 | 确定性信道 + DL 强行优越 | GNN 优势来源是否明确（负载均衡/全局协调 vs 预测量）？低流量下是否有退化预案？ | ☐ |
   | 4 | 跨实验数据不一致 | 所有实验是否共用同一组拓扑快照和流量矩阵？ | ☐ |

   [MUST] 反模式排查应在 Step 4 端到端推演的 `data-flow.md` 基础上进行，而非凭空想象。

> 为什么反模式审查从 Execute 前移到 Contract：反模式本质是实验设计缺陷，应该在设计阶段（Contract）发现并修复，而非等代码写完再回头。Execute 阶段只需做实现级验证（代码是否忠实实现了设计）。

> 为什么加第 4 问：首次试跑中 baseline 选择完全缺乏交叉验证，选出的是单篇论文的特有对比方法而非领域共识。这个教训说明 baseline 的学术合法性也需要显式检查。

---

## Step 6：冻结

[MUST] 以上 Step 0-5 全部通过后，Contract 状态从 draft → frozen。

冻结操作：
1. 更新 contract.md 头部 `status: frozen`
2. 用户确认（最关键的人介入点）
3. 写 handoff 记录 Contract 冻结，列出 Execute 阶段入口

---

## Contract 的效力

### 冻结后的不可变与可变

**不可变**（修改需创建 `contract_v2.md` + 用户确认）：
- hypothesis、success_signal、failure_signal
- fairness_rules、ablation_plan
- experiment_list 的核心/对比/消融结构

**可修正**（通过 Contract Amendment 机制，无需新建版本）：
- Simulation Config 中的参数值（如发现物理参数计算错误）
- 修正流程：记录到 decision_log + contract.md 中加 amendment 注解 + 用户确认

[MUST NOT] 事后调整 success_signal 配合结果。

### Contract Amendment 格式

在 contract.md 对应字段旁加行内注解：

```
## Simulation Config
ISL bandwidth: B = 1 GHz  <!-- AMENDMENT: 原 500 MHz 无出处，修正为 L03 DuJo 值。D015 -->
```

同时在 decision_log 记录：

```
[D{序号}][AMENDMENT] {参数名}: {旧值} → {新值} | 理由: {核实发现} | 来源: {L{序号}/计算} | 用户确认: {留空}
```

### 变更提案格式（不可变字段的修改）

内嵌在 decision_log 中，不独立成文件：

```
[D{序号}][CHANGE-PROPOSAL] {变什么} | 理由: {为什么} | 影响: {哪些结果会作废} | 用户决定: {留空}
```

**例外**：仿真环境缺陷导致结论不可靠 → 允许修复后重跑，但 [MUST] 记录变更提案并经用户确认

> 为什么这么严格：社区经验——"如果你不在实验之前把这些确定，模型一定会在结果出来以后帮你合理化。做科研最忌讳的就是先看到结果再编故事"。Contract 是防"事后编故事"的第一道防线。

---

## 完成条件

- [ ] contract.md 已创建且所有字段已填写
- [ ] parameter_provenance 表已填写，所有 `[ASSUMPTION]` 已消除
- [ ] data-flow.md 端到端推演已完成，断层已修正
- [ ] 压力测试 5 问已回答（含反模式排查），无致命风险信号
- [ ] decision_log 包含假设形成的关键决策 + 参数核实记录
- [ ] **用户已确认 Contract 冻结**
- [ ] **路径合规**：competitor_notes 在 `projects/{name}/competitor_notes/`，检索结果在 `search-archive/{date}/` 或 `projects/{name}/search-archive/`
