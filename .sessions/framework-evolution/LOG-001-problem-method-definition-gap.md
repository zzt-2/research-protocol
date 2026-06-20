# LOG-001 框架根本缺陷：未定义"问题/方法/空白"，导致"按框架跑出垃圾"

> 2026-06-20 | 来源：thesis-fso 5 次殊途同归 + S005 agent 连犯 3 错 | 严重度：**P0（框架级，影响所有项目）**

## 问题陈述

当前研究协议框架**没有把"问题 / 方法 / 空白"这些核心概念定义准、放对位置**。后果是：agent 即使"按框架跑"，也会跑出垃圾——thesis-fso 5 次殊途同归（N1/③/A3/4b#1/(c) 全 Kill）就是证据，而这次 agent 连犯 3 错（空白当问题→定义太宽→章节标题当问题）是同一缺陷的二次发作。

这不是执行偏差，是**框架的制度性缺陷**。

## 证据链（三条，钉死）

### 证据 1：框架自己把"空白"当 Contract 假设的合法来源

`stages/contract.md` 第 86-88 行：

```
假设来源应该是 Groundwork 中发现的研究空白或改进空间，而不是凭空提出。具体来说：
- 从 literature_notes 的"已知局限"中识别研究空白
- 从 baseline 复现中确认改进空间确实存在
```

**这是制度性缺陷**：框架明确指导 agent "从 literature_notes 的研究空白识别假设"。我们 5 次失败"拿 literature_notes 空白当问题"——**是照框架执行的结果，不是偏离框架**。

框架把"空白"和"问题"混用了。literature_notes 第 184-189 行的"研究空白汇总"（相干信道估计空白 / 星地后均衡空白 / GG+相干+均衡联合空白）被框架指引成假设来源，但这些是"没人做过 X"（新颖性事实），不是"现有 M 在 C 下失效"（问题）。两者粒度差两个数量级：空白是领域级，问题是章节级。

### 证据 2：框架全文没有"问题"的正式定义

grep `stages/` 目录，"问题"出现 40+ 次（多是"研究问题""问题结构""问题本身"等用法），但**没有任何一处给出"什么算一个研究问题"的定义**。没有判据、没有示例、没有反例。

对比：框架对"baseline"有详细处理（contract.md Step 1 瓶颈诊断、Step 2 动作空间表达力审计 FR-13、反模式审查第 4 问"Baseline 共识性"），对"novelty/新颖性"有处理（contract.md Step 0 方案新颖性检索），对"假设"有处理（contract.md Step 1 形成假设 + success_signal/failure_signal）。**唯独"问题"——整个研究的起点概念——没有任何正式定义。**

### 证据 3：master-state.md 缺失，无跨 Step 硬门控

- `projects/_archive/` 下 5 个归档项目都有 `master-state.md`
- **`projects/thesis-fso/` 没有**（只有 literature_notes 里的 markdown 进度表，不是框架定义的状态文件）
- AGENTS.md 状态恢复章节把 master-state.md 列为优先级 2，说明框架**预期**每项目有此文件，但没强制建立，也没定义它必须含"GW Step 完成状态"作为门控载体
- `stages/groundwork.md` 各 Step 内部有子门控（gw-feasibility.md A0/B/D 维度门控），但**Step 之间没有"前序 Step 未 ✅ 禁止进下一步"的跨 Step 门控**

后果：agent 可以在 literature_notes 进度表 Step 2/3/3.5/4a 全 ⬜ 的情况下，直接跳去跑 MVE——没有任何框架级机制阻止。5 次失败全部发生在 Step 1 之后、Step 3-4a 之前的真空地带。

## 根因诊断

三个缺陷互为因果：

```
缺陷 A（概念层）：框架未定义"问题"，且把"空白"当问题来源
   ↓ 导致
缺陷 B（流程层）：GW 没有产出"问题清单"，只产出"文献清单/空白清单"
   ↓ 导致
缺陷 C（状态层）：没有可查的 Step 进度文件，跨 Step 无硬门控
   ↓ 导致
agent 在 Step 1 后真空里，拿"空白"当"问题"，凭标题联想自创"方法"，跳过 Step 3-4a 直接 MVE → 撞物理天花板 → Kill
```

A 是最根本的。即使补了 C（master-state.md + 门控），只要 A 不解决，agent 走完 Step 3 精读后产出的还是"空白清单"不是"问题清单"——只是把撞墙时间推迟。

## 改造方案（具体到文件和位置）

### 改造 1（对应缺陷 A）：在框架里正式定义"问题"，并与"空白"严格区分

**位置**：新建 `stages/glossary.md`（术语表）或在 `overview.md` 加"核心术语"段。**问题定义的唯一拥有者**，其他文件只引用。

**定义内容**（基于 S005 定稿的问题四判据 + 老师反馈）：

```
## 研究问题（Problem）的定义

研究问题 = "现有方法 M 在条件 C 下，因假设 A 而失效/不足"。

一个问题必须同时满足四条判据：
1. 具体技术矛盾：M / C / A 三要素都明确（不是章节标题、不是领域空白）
2. 有方法产出形态：解决它会长出可用方法（设计公式/准则/算法/框架），不是只给曲线/边界
3. 有近期 baseline 可对标：问题里天然嵌着具体 SOTA 方法 M（老师要求：对标 2019+ 顶刊）
4. 能做对比：自己的方法 vs baseline M 有可量化对比（老师要求：每章 1-2 个对比算法）

## 问题 vs 空白 vs 研究主题（必须区分）

| 概念 | 定义 | 粒度 | 能否当研究起点 |
|---|---|---|---|
| 空白（Gap）| "没人做过 X" | 领域级 | ❌ 只是新颖性证据 |
| 研究主题（Topic）| "X 的性能分析" | 章节级范围 | ❌ 是范围不是起点 |
| 问题（Problem）| "M 在 C 下因 A 失效" | 章节级、可解 | ✅ 唯一合法起点 |

空白 → 必须转译成"现有 X 的失效"才升级为问题。
研究主题 → 必须细化为带 baseline 和方法形态的具体矛盾才是问题。
```

**配套修改**：
- `stages/contract.md` 第 86-88 行重写：假设来源是"GW 产出的**问题清单**（见 glossary.md 定义）"，**删除"从 literature_notes 的研究空白识别假设"这句**。空白只作新颖性证据，不作假设来源。
- `stages/gw-search.md` / `stages/gw-read.md`：精读产出模板加"问题提取"段——每篇精读必须回答"这论文解决了什么问题（M/C/A）？问题过四判据吗？"。
- `AGENTS.md` 护栏表：FR-23 增量改进规则，把"问题四判据"作为定义内容（当前 FR-23 只有一句话，需要展开指向 glossary.md）。

### 改造 2（对应缺陷 B）：GW 新增"问题清单"产出物

**位置**：`stages/gw-read.md`（精读规范）+ `templates.md`（模板）

GW Step 3 精读的产出，当前是"literature_notes.md 补充"。改造后产出必须包含一个**问题清单段**：

```
## 研究问题清单（GW Step 3 产出）

| # | 问题（M/C/A） | baseline M | 条件 C | 失效假设 A | 方法产出形态 | 过四判据 | 来源文献 |
|---|---|---|---|---|---|---|---|
| Q1 | ... | Petković 2020 | GG 湍流 | perfect CSI | 扩展 SEP 框架 | ✅ | content.md L## |
```

Contract Step 1 形成假设时，**必须引用这个清单里的 Q#**，不能凭空提假设。这样"空白→假设"的通道被堵死，"问题→假设"的通道被建立。

### 改造 3（对应缺陷 C）：master-state.md 强制化 + 跨 Step 硬门控

**位置**：`stages/groundwork.md`（开头加跨 Step 门控声明）+ `AGENTS.md`（master-state.md 定义强化）+ `templates/master-state-template.md`（模板，AGENTS.md 提到过这个文件）

- `templates/master-state-template.md` 加强制段 `## GW Progress`，格式 `Step N: ✅/⬜ [日期/验证记录]`
- `stages/groundwork.md` 开头加："Groundwork 各 Step 顺序执行。任何 Step 动作开始前，必须先读 projects/{name}/master-state.md 的 `## GW Progress`，确认前序 Step 均为 ✅。任一前序 Step 为 ⬜ → 禁止开始本 Step（FR-22）。"
- `AGENTS.md` master-state.md 描述加"**强制含 `## GW Progress` 段**，作为 FR-22 门控的唯一可查状态"
- 给 thesis-fso 补建 master-state.md（含 GW Progress，如实标 Step 2/3/3.5/4a 为 ⬜，Step 1 ✅）

## 改造的优先级和顺序

**必须按 A→B→C 顺序改**，因为 A 是根因：
1. 先改 A（glossary.md 定义问题 + contract.md 删空白来源 + FR-23 展开）——不解决 A，B/C 都没用
2. 再改 B（GW 问题清单产出 + Contract 引用机制）
3. 最后改 C（master-state.md + 跨 Step 门控）——这是执行保障，防止 A/B 改了但又被跳过

## 验证改造是否生效的标准

改造后，任何一个新项目跑 GW，必须满足：
1. GW Step 3 精读完，literature_notes 里有"问题清单"段，每条过四判据（改造 1+2 生效）
2. Contract Step 1 假设引用问题清单的 Q#，不出现"从空白识别假设"（改造 1 生效）
3. projects/{name}/master-state.md 存在且 GW Progress 段实时更新（改造 3 生效）
4. 任何跳 Step 的动作，在 master-state.md 上一眼能看出来（⬜ 状态 + 无对应 Step 声明）（改造 3 生效）

## 风险与注意

- **改造 1 改 contract.md 是动核心文件**，影响所有项目（包括 _archive 里 5 个已完成的）。改完需 grep 确认没有其他文件依赖"空白→假设"的旧逻辑。
- **glossary.md 是新文件**，要遵循 AGENTS.md 文档职责边界——"问题定义"的唯一拥有者，其他文件只引用一行。
- **改造 3 的 master-state.md 要给已有项目补建**，不只 thesis-fso。但 _archive 项目已 closed，不必补（只对 active 项目强制）。
- 这三个改造本身要按"分层试错法"做——先改 thesis-fso 跑一轮验证，再推广到所有项目。不要一次改完就当全局生效。

## 关联

- 本 LOG 来源：`.sessions/2026-06-19-4b1-adaptive-interleaving-groundwork/S004`（5 次殊途同归根因复盘）+ `S005`（agent 连犯 3 错）+ `H002`（重定方向 v2 handoff）
- 相关教训：`thesis-lessons.md` TL-04（空白≠机会）/ TL-30（框架强制规范）/ TL-31（教训复现）
- 相关护栏：`AGENTS.md` FR-22（GW 流程强制门控）/ FR-23（增量改进非填补空白）/ FR-24（方法论强制重读）
- 下一轮执行：见本专题待办"按 LOG-001 改 stages/ + AGENTS.md + thesis-fso master-state.md"
