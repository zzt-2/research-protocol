# Contract（冻结）

> 冻结研究假设和实验方案。Contract 写好后 Execute 阶段不允许修改。
> 通信领域研究：额外阅读 `domain-comms.md` 中的指标体系和推荐技术栈。

---

## 目标

冻结研究假设和实验方案，为 Execute 阶段提供不可变的执行基准。

## 输入

Groundwork 全部产出（literature_notes.md + baseline_report.md + feasibility_report.md + decision_log.md）

[MUST] `feasibility_report.md` 中 Go/No-Go 决策为 Go 方可进入 Contract 阶段。

## 输出

`contract.md`（核心工件）+ `decision_log.md`（追加）

## 人介入点

[MUST] Contract 冻结前用户必须确认。这是最关键的人介入点。

---

## Step 0：方案新颖性检索

[MUST] 在形成假设前，必须确认候选方案的新颖性。流程：

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

## Step 2：冻结 Research Contract

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

---

## Step 3：选题压力测试

[MUST] 回答以下 4 问，无致命风险信号才能通过：

1. **结构性优势**：核心方法 vs 最简 baseline 的结构性优势在哪？
   - 如果只是"用 DL 替代传统方法"而没有解释为什么 DL 适合这个问题 → 高风险

2. **边际结果**：结果仅边际优于 baseline（如 <5%）时，成果还能否成立？
   - 如果边际结果无法支撑任何有价值的结论 → 高风险

3. **信号独立性**：success/failure 信号是否独立且可操作？
   - failure_signal 不能只是 success_signal 的否定

4. **Baseline 共识性**：选定的 baseline 是否是领域共识？
   - 交叉验证数据：被几篇论文使用、是否有代码
   - 如果 baseline 是某篇论文自创的对比方法而非领域通用方法 → 需要额外论证

> 为什么加第 4 问：首次试跑中 baseline 选择完全缺乏交叉验证，选出的是单篇论文的特有对比方法而非领域共识。这个教训说明 baseline 的学术合法性也需要显式检查。

---

## Contract 的效力

- 实验开始后 Contract 不可修改
- 确需修正 → 创建 `contract_v2.md`，写清改了什么、为什么，旧版本保留
- [MUST NOT] 事后调整 success_signal 配合结果

**例外**：仿真环境缺陷导致结论不可靠 → 允许修复后重跑，但 [MUST] 记录变更提案并经用户确认

> 为什么这么严格：社区经验——"如果你不在实验之前把这些确定，模型一定会在结果出来以后帮你合理化。做科研最忌讳的就是先看到结果再编故事"。Contract 是防"事后编故事"的第一道防线。

### 变更提案格式

内嵌在 decision_log 中，不独立成文件：

```
[D{序号}][CHANGE-PROPOSAL] {变什么} | 理由: {为什么} | 影响: {哪些结果会作废} | 用户决定: {留空}
```

---

## 完成条件

- [ ] contract.md 已创建且所有字段已填写
- [ ] 压力测试 4 问已回答，无致命风险信号
- [ ] decision_log 包含假设形成的关键决策
- [ ] **用户已确认 Contract**
- [ ] **路径合规**：competitor_notes 在 `projects/{name}/competitor_notes/`，检索结果在 `search-archive/{date}/` 或 `projects/{name}/search-archive/`
