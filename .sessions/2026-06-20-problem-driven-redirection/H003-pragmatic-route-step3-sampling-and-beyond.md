# Handoff: 务实路线启动——Step 3 选样 + 精读 + 后续全链路工作拆解

> 来源: S014 + D004 + D005 | 交接目标: 按务实标准启动 Step 3，并理解从选样到毕业的完整工作链路
> 文件名: H003-pragmatic-route-step3-sampling-and-beyond.md

## 已完成边界

**本轮（2026-06-26）定了三件改变地基的事**：

1. **S013 作废 + S014 纠正**：导师真 3 篇在 `papers/teacher/`（全北理工学位论文：王培森 NOMA / 李兀祺 扩频干扰抑制 / 弱信号同步），S013 误把 `papers/downloads/2026-06-23/`（S011 Q#-A 核查残留的 JAXA/ESA/TNO 论文）当导师论文，纯日期目录联想（TL-33 第 1 次复现）。4 篇同门方向骨架（+夏兆宇）已提取，实验室套路 = 场景三约束→现有方法单一环节失效→多维协同 DSP+硬件落地。

2. **D004 立（框架待验证）**：三条打磨点——对手显式化（传统未优化 baseline 作对手）/ motivation 结构字段（精读模板加场景约束+失效点+切入点）/ 证据链强制（宣称在 Step X 必附证据指针）。AGENTS.md 加了 FR-25/FR-26 索引行。

3. **D005 立（INVARIANT 级，最高优先级）**：学位定位翻转为**务实路线**——先能写出东西毕业，接受赢传统 baseline 几 dB 作贡献，oracle 上界 FR-21 降级为参考。**导师已确认接受增量**。底线仍守（不接受孤证凑数/标题联想/伪命题，要导师同意，方法必须指标提升）。

**当前 GW 进度**（查 master-state.md GW Progress 表）：Step 1 search ✅ / Step 2-7 全 ⬜。**Step 3（精读）整个从没做过**——6 次 Kill 全是跳过 Step 3 直接试 MVE。所以从"选样"到"毕业"是一条完整未走的长链路。

## 不要做什么

**1. 不要用严苛标准砍自己（D005 核心纠正）**
- ❌ 不要用 oracle 上界 <0.5dB 当 Go/Kill 门（FR-21 已降级为参考）
- ❌ 不要找"baseline 致命失效/真缝"才肯 Go（务实标准 = baseline 在具体条件下不够好+改进空间就 Go）
- ❌ 不要被"物理上窄"的悲观假设吓退（R001 已证：只有 ③ MCS 排程规范走到 FR-21 被砍，其余子地带"窄"是未验证假设）
- ✅ 要跟传统未优化 baseline 比，能赢几 dB 就 Go（参考同门 2-4dB 量级）

**2. 不要跳 Step 3（TL-30 仍有效，D005 没废这条）**
- ❌ 不要标题联想试 MVE（"PCS 能不能提升""交织能不能省东西"这种起点 = 跳步）
- ❌ 不要单假设反向验证（Q#-A 模式，D003 已禁）
- ✅ 要按 gw-read.md 走完精读全流程（7 个子表 + 问题清单 Q#）

**3. 不要把务实 = 造假（底线）**
- ❌ 不接受孤证凑数（Q#-A 模式仍禁——孤证+被反驳的方向做了答辩会被问倒）
- ❌ 不接受伪命题/标题联想
- ✅ 务实是"做真问题但允许增量贡献"，不是"造垃圾"

**4. 不要凭印象/联想（TL-31/33 仍有效）**
- ❌ 不要像 S013 那样凭日期目录联想（用 papers/ 下文件做外部输入判断前必查 meta.json 来源）
- ❌ 宣称"在 Step X / 已读 Y"必附证据指针（FR-26）
- ✅ 任何方法论/方向判断动笔前必 Read decisions.md + thesis-lessons.md（FR-24）

**5. 不要回头救 6 次 Kill（诚实结论）**
- 6 次里大概率没几个能救（③0.09dB / 4b#1 BER堵 / (c)信息论硬约束 / N1 gain≈0 / A3场景不匹配 / Q#-A孤证）
- 优先往前选样，不回头救旧。除非选样卡死才回头逐个重评。

## 必读（按优先级）

**新对话开始时必须读**（按这个顺序）：

1. **`topic-index.md`**（本专题）——读"不变量"段（D005 务实路线是第 1 条 INVARIANT）+ "当前位置" + "悬而未决" #23/#24
2. **`decisions.md` D005 + D004**——务实标准的具体执行规则 + D004 三条打磨点
3. **`thesis-lessons.md` TL-30/31/32/33**——跳步/凭记忆/标准不对称/自欺式跳步
4. **`projects/thesis-fso/master-state.md` §GW Progress 表**——确认当前在 Step 3（全 ⬜）
5. **`stages/gw-read.md`**——Step 3 精读的完整流程（7 个子表 + 问题清单 Q# + 综合分析）
6. **`S014-correct-S013-and-direction-skeleton-and-D004.md`**——4 篇同门方向骨架（motivation 结构正例库）
7. **`stages/glossary.md`**——四判据定义（注意 D005 把判据 A 从"真缝"降级为"baseline 不够好+改进空间"）

## 后续工作量拆解（核心——这不是一次对话能完成的）

**从"选样"到"毕业"是 GW Step 3 → Step 7 → Contract → Execute 的完整链路**，master-state 显示 Step 3-7 全 ⬜。诚实拆解如下（每个块 = 1 个对话工作量上限）：

### 块 A：选样（1 个对话）
- **输入**：683 条 landscape（`projects/thesis-fso/landscape.md`，509 主表+附录）+ 务实标准
- **动作**：按务实标准筛 ≥5 篇代表性论文——选样标准 = ①有传统 baseline 可比 ②方法能迁移到星地激光 ③工程可做 ④覆盖不同技术路线（D004-b motivation 结构）
- **产出**：选样清单给用户审（每篇一句话标"为什么选 + 传统 baseline 是谁 + 预期改进空间"）
- **不做什么**：不筛"真缝"，不卡 oracle 上界，不预设方向
- **完成标志**：用户审过选样清单

### 块 B：精读批次 1（1-2 个对话，每批 2-3 篇）
- **输入**：块 A 选样清单（已审）
- **动作**：派子 agent 按 gw-read.md 精读，每篇提取 7 个子表（**重点是第 7 项问题提取 M-C-A**），套用 D004-b motivation 结构字段
- **产出**：每篇 literature_notes 精读条目
- **注意**：按 AGENTS.md 论文精读必须委托子 agent，主对话只收结构化摘要；单子 agent ≤15 分钟；一次最多 3 个并行
- **完成标志**：≥5 篇精读条目落 literature_notes.md（groundwork.md:99 门槛）

### 块 C：综合分析 + 问题清单 Q#（1 个对话）
- **输入**：块 B 全部精读条目
- **动作**：撰写综合分析（方法分类/局限/趋势/背景）+ **研究问题清单 Q#**（把每篇 M-C-A 汇总，逐条过四判据，D005 修正判据 A）
- **产出**：literature_notes.md 综合分析节 + Q# 清单（每条标四判据 ✅/❌）
- **完成标志**：Q# 清单非空且至少 1 条四判据全过（GW Step 3 进 Step 4a 的硬门）

### 块 D：Step 3.5 定向补充检索（0.5-1 个对话）
- **输入**：块 C Q# 清单
- **动作**：用精读产生的新认知做一轮定向检索，弥补盲区（groundwork.md:33 必做）
- **产出**：更新 literature_notes.md
- **完成标志**：补充检索完成

### 块 E：Step 4a 可行性 Go/No-Go（1-2 个对话）
- **输入**：块 C/D 的 Q# 清单 + feasibility_report.md
- **动作**：每个 Q# 走 gw-feasibility 维度 A0（四判据门控）/ A'（竞争维度）/ A（结构优势）/ B（新颖性-可行性）/ D（MVE）
- **务实标准应用点**：维度 A 对手 = 传统 baseline；FR-21 oracle 上界只当参考不当 Kill 门；MVE 快速试错
- **产出**：feasibility_report.md + Go/No-Go 决策（用户确认）
- **完成标志**：至少 1 个 Q# Go（否则回 Step 3.5 补检索或换子地带）
- **风险点**：这是最容易卡住的环节，如果全 No-Go 要回选样（块 A 重来）

### 块 F：Step 5-7 Baseline 复现（2-4 个对话，最重工作量）
- **输入**：块 E Go 的 Q# + baseline 候选
- **动作**：Step 5 选 baseline → Step 6 设计仿真器 → Step 7 实现+复现
- **产出**：baseline_report.md（复现成功）
- **注意**：必须先读 `code-quality.md` + `reference/sim-template/`；GNN 模型继承 BaseActorCritic；训练循环集成 wandb+early stopping；save/load 含 optimizer+step_count
- **完成标志**：baseline 复现成功，指标对得上论文

### 块 G：Contract（1-2 个对话）
- **输入**：块 F baseline
- **动作**：data-flow.md / 假设设计 / 实验完备性对标（contract.md S1-S5）
- **产出**：Contract 文档
- **完成标志**：用户确认 Contract

### 块 H：Execute 实验 + 论文写作（多个对话）
- **输入**：块 G Contract
- **动作**：跑实验 + 写论文（参照夏兆宇模板 S004 + 同门 4 篇 motivation 结构）
- **完成标志**：论文成稿

**总工作量估算**：块 A-H 约 **10-16 个对话**。这不是一次对话能完成的——务必分对话推进，每对话 ≤3 步骤（AGENTS.md 规则）。

## 接口变更（如有代码改动）

无代码改动（本轮全是方法论/决策/文档）。下个对话块 A 选样也不涉及代码。

## 失败数据附录（如涉及路线失败）

本轮无新路线失败。6 次 Kill 失败数据见 R001（`R001-six-kill-commonality-and-gw-step3-correction.md`）。

**对 6 次 Kill 在务实标准下的诚实重评**（D005 记录）：大概率没几个能救——
- ③ MCS 排程（oracle 0.09dB）：连传统 baseline 都赢不了多少，不救
- 4b#1 自适应交织（BER+时延双堵）：BER 维度真堵死，不救
- (c) GG-LLR 译码（-1.3~-1.8dB）：信息论硬约束，不救
- N1 概率整形（gain≈0）：MVE 实测没增量，不救
- A3 pilot CPE（AO 残余 1885×）：场景不匹配，不救
- Q#-A FEC（孤证+2反驳）：务实标准仍不接受孤证凑数，不救

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| FR-21 降级未改框架文件 | D005 已把 FR-21 降为参考 | 框架文件 gw-feasibility.md 仍写"硬 Kill 门" | Step 3 走一遍验证 D004/D005 有效后，改 gw-feasibility.md + groundwork.md |
| D004 三条打磨点未进框架 | D004 已立但"框架待验证" | gw-read.md/gw-feasibility.md 没加 motivation 字段/对手显式化/证据链 | 同上，Step 3 验证后进框架 |
| 务实"几 dB 算够"阈值未定 | D005 说"赢传统 baseline 几 dB" | 参考同门 2-4dB 但无统一阈值 | Step 3 精读后按子地带定（悬而未决 #23）|
| IEEE blit 检索债务 | S005 修了但高频限流 | landscape 已够用 | 需要补 IEEE 内容时再处理 |
| master-state §8 旧推断（Paillier） | S002 修过 | 已修 | — |

## 验证阈值（如涉及验证体系）

本轮不涉及验证体系。后续 MVE 的 pass 标准（务实路线下）：
- **Go**：方法 > 传统未优化 baseline（参考同门 2-4dB 量级，具体阈值块 E 定）
- **Kill**：连传统 baseline 都赢不了 / 方法增益 <0.5dB 且无次指标维度 / MVE FAIL
- **不放水**：不接受孤证/伪命题/标题联想（底线）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（D005 务实路线是第 1 条 INVARIANT）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 导师真 3 篇在 `papers/teacher/`（核查：`ls papers/teacher/` 看文件名）
  - [ ] GW Step 3 从没做过（核查：`master-state.md` GW Progress 表 Step 3 = ⬜）
  - [ ] D005 已确认导师接受增量（核查：`voice.md` 2026-06-26 "导师接受增量"）
- [ ] 已检查 _registry.yaml 中本专题 status = active（无 conflicts_with）
- [ ] 已确认当前范围未违反"明确不含"（仍要导师同意 S007 边界 / 仍不接受孤证凑数 / 方法必须指标提升）

## 下一轮

**块 A：选样（务实标准）**

具体可执行的下一步任务：

1. 读 `topic-index.md` 不变量段 + `decisions.md` D005/D004 + 本 handoff 的"工作量拆解"
2. 读 `projects/thesis-fso/landscape.md`（509 主表+附录）了解 landscape 全貌
3. 按务实标准（有传统 baseline 可比 + 方法能迁移 + 工程可做 + 覆盖不同技术路线）筛 ≥5 篇代表性论文
4. 每篇一句话标"为什么选 + 传统 baseline 是谁 + 预期改进空间 + motivation 结构类型"
5. 选样清单给用户审

**关键提醒**：选样时套用 D004-b motivation 结构字段——优先选 motivation 结构清晰（场景约束→失效点→切入点）的论文，避开"纯工程对比不批 baseline"的论文（像 JAXA 10294033 那种）。同门 4 篇（王培森/李兀祺/弱信号同步/夏兆宇）是 motivation 结构正例库。

**不要在块 A 做**：不精读（块 B 的事）/ 不过四判据（块 C 的事）/ 不判 Go（块 E 的事）。块 A 只负责"选出 ≥5 篇代表性论文给用户审"。
