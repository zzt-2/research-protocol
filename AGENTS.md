# 研究协议 — 项目指令

## 环境

- Python: `~/.venvs/torch/bin/python`（torch 2.11+cu126, CUDA RTX 4070, MinerU, pymupdf4llm）
- pip 镜像: `-i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`

## 目录结构

```
├── stages/              # 框架流程定义（groundwork.md 等）
├── domain-comms.md      # 通信领域定制（非通信项目忽略）
├── templates.md         # 文档模板
├── overview.md          # 框架总览
├── tools-guide.md       # 工具使用指南
├── papers/              # 共享论文库（所有项目共用）
│   ├── arxiv/{id}/      # arXiv 论文（id 如 2405.17150）
│   │   ├── source.html  #   原始文件（.html / .tar.gz / .pdf）
│   │   └── content.md   #   转换后 markdown
│   ├── doi/{doi_path}/  # DOI 论文（doi_path 如 10.1109_tmc.2025.3645456）
│   │   ├── source.pdf
│   │   └── content.md
│   ├── manual/{slug}/   # 无 arxiv/DOI 的论文（slug 如 cai-jsac-gdrl）
│   └── index.json       # 全局论文索引
├── search-archive/{date}/  # 检索缓存（date 如 2026-05-12）
├── .sessions/              # 会话管理（跨对话状态集中存放）
│   ├── {YYYY-MM-DD}-{project-slug}/  # 按项目/日期建文件夹
│   │   ├── H{NNN}-{slug}.md          # 跨对话交接记录
│   │   ├── PROMPT-{NNN}-{slug}.md    # 新对话提示词
│   │   └── LOG-{NNN}-{slug}.md       # 操作日志
│   ├── framework-evolution/           # 框架演进专题（跨项目，长期，不按日期另开）
│   │   └── LOG-{NNN}-{slug}.md       # 框架问题日志
│   ├── direction-scouting/            # 方向侦察/项目盘点（长期，不按日期另开）
│   └── thesis-structure-research/     # 论文结构研究（长期，不按日期另开）
├── reference/           # 参考实现代码
│   └── sim-template/    # 代码模板（config/env/model/train/reward/verify 最佳实践）
├── code-quality.md      # 代码质量经验积累（写代码前必读）
├── tools/               # 辅助脚本
├── templates/           # 模板文件
│   └── master-state-template.md  # Master prompt 模板
└── projects/{name}/     # 独立研究项目（全部项目级产物在此）
    ├── master-state.md  # Master 编排状态（每步后更新，恢复时首选读取）
    ├── decision_log.md
    ├── literature_notes.md
    ├── feasibility_report.md
    ├── competitor_notes/
    ├── baseline_report.md
    ├── worker-logs/      # Worker 执行日志（审计+框架反馈）
    ├── worker-tasks/     # Worker 任务文件（ephemeral，不提交）
    ├── search-archive/   # 项目专属检索记录（Contract 阶段等）
    ├── simulator/
    ├── baselines/
    ├── results/
    └── verify/
```

## 文件路径规则（禁止自作主张）

每类文件有且仅有一个存放位置，不允许在根目录随意创建目录或文件。

| 产物              | 生成方式                       | 存放路径                                                          |
| ----------------- | ------------------------------ | ----------------------------------------------------------------- |
| 检索结果 JSON     | `tools/search` 自动保存        | `search-archive/{YYYY-MM-DD}/{slug}.json`                         |
| 论文下载（arXiv） | `tools/download`               | `papers/arxiv/{arxiv_id}/source.{html,tar.gz,pdf}` + `content.md` |
| 论文下载（DOI）   | `tools/download`               | `papers/doi/{doi_path}/source.pdf` + `content.md`                 |
| 论文下载（无 ID） | `tools/download`               | `papers/manual/{slug}/source.pdf` + `content.md`                  |
| PDF 转 markdown   | `tools/convert`                | 输出到 PDF 同目录，文件名 `{pdf_stem}.md`                         |
| 手动下载的 PDF    | 用户操作                       | 放入 `papers/downloads/{date}/`，之后用 `tools/convert` 转换      |
| 参考实现代码      | 手动管理                       | `reference/{name}/`                                               |
| 代码质量经验      | 自动生成                       | `code-quality.md`                                                 |
| 代码模板          | 从最佳项目提取                 | `reference/sim-template/`                                         |
| Master 编排状态   | Master agent 每步后更新        | `projects/{name}/master-state.md`                                 |
| Worker 执行日志   | Worker 执行结束时写入          | `projects/{name}/worker-logs/step-{N}-{slug}.md`                  |
| Worker 任务文件   | Master 派遣前写入（ephemeral） | `projects/{name}/worker-tasks/`                                   |

**禁止事项：**

- 不在根目录创建新的论文目录（如 `my-download-paper/`）
- 不在根目录创建 `literature_notes.md`（属于项目目录）
- 不在 `search-archive/` 根级放文件（必须按日期入子目录）
- 不手动创建 `papers/` 下的任意命名目录（走 `tools/download` 自动建路径）

## 框架文件是执行规范

以下文件不是"参考文档"，是必须读并遵守的执行规范：

- `stages/groundwork.md` — Groundwork 阶段每一步的操作、检查点、通过条件
- `templates.md` — 文档模板中的 `[MUST]` 和 `{占位符}` 规则
- `domain-comms.md` — 通信领域定制（非通信项目跳过）

**[MUST] 转阶段/转步骤必须先读对应框架文件。**

不允许凭记忆、凭上下文中的摘要、或凭"之前读过"跳过阅读。判断标准：本轮上下文中没有该文件的明确阅读证据（如本轮通过 Read 工具读过），视为未读。

**[MUST] 禁止跳过框架自创流程（FR-22）。**

`stages/groundwork.md` 等 stage 文件定义的是**唯一合法的研究推进路径**，不是"参考流程"或"可选项"。不允许脱离 stage 文件定义的步骤序列，凭"标题联想+物理直觉"自创"找方法→试 MVE→Kill"的循环。

具体强制：

- 任何"试新方法 / 开新方向 / 跑 MVE"的动作，**必须先回答"当前在 GW（或 Contract/Execute）的哪一步"**。指不到具体 Step（如"GW Step 4a 维度 D"）= 跳框架，**禁止开跑**。
- **GW Step 3（精读）和 Step 4a（可行性 Go/No-Go）是硬门控，不可跳过**。`literature_notes.md` 进度表任何一项为 ⬜ 时，禁止进入 MVE 或 Contract。
- **跳步的识别信号**：候选的论证起点是"标题联想"（如"PCS 能不能提升""交织能不能省东西"）而非 GW Step 4a 维度 A0 的产物（"现有 M 在 C 下失效/不足"）→ 一定跳了 Step 3-4a。
- **教训依据**：thesis-fso 项目在 GW Step 1 完成后跳过 Step 2/3/3.5/4a 直接试 5 个方向（N1/③/A3/4b#1/(c)），5 个全部 Kill，浪费 ~9 个对话。详见 `thesis-lessons.md` TL-30。用户原话："我 tm 以为之前按照框架来的"——连用户都以为在按框架走，实际全程跳步。

具体要求：

- 进入新阶段（如 GW → Contract）→ 必须读 `stages/{stage}.md`
- 进入新步骤（如 GW Step 3 → Step 3.5）→ 必须读该步骤的职责文件（如 `gw-supplement.md`）
- 跨对话续接、上下文压缩后恢复 → 同样必须重读
- 对话中如果涉及运行时机制（仿真器、processor 等），还要额外读对应 spec

### 文档职责边界

每条约束只有一个拥有者（完整定义所在文件），其他文件只引用。文档层级：

| 层级     | 文件                      | 职责                                               |
| -------- | ------------------------- | -------------------------------------------------- |
| 通用原则 | `overview.md`             | 核心原则、文档系统概览                             |
| 阶段流程 | `stages/*.md`             | 该阶段的完整操作流程                               |
| 领域定制 | `domain-comms.md`         | 领域特定技术栈、指标、反模式                       |
| 模板定义 | `templates.md`            | 文档模板和字段规则                                 |
| 代码质量 | `code-quality.md`         | 代码经验积累、必做清单、常见缺陷、各维度最佳来源   |
| 代码模板 | `reference/sim-template/` | config/env/model/train/reward/verify 骨架代码      |
| 本文件   | `AGENTS.md`               | 环境配置、目录结构、规则索引（不重复框架文件内容） |

### 文档更新流程

每条内容有且仅有一个拥有者文件。新增内容时：

1. **先写拥有者文件**（完整定义），再更新索引文件（一行引用）
2. **AGENTS.md 只加索引行**：规则名 + 文件路径，不解释内容
3. **code-quality.md 是教训唯一来源**：其他文件不重复教训内容

| 新增场景       | 拥有者（写这里）       | 需同步更新                             |
| -------------- | ---------------------- | -------------------------------------- |
| 失败模式/教训  | `code-quality.md`      | 无（projects-overview.md 已引用）      |
| 执行规则       | `stages/execute.md`    | AGENTS.md 护栏表加索引行               |
| 跨阶段规则     | 对应阶段文件           | AGENTS.md 护栏表加索引行               |
| 项目状态变更   | `projects-overview.md` | `directions-registry.md`（如涉及方向） |
| 代码质量检查项 | `code-quality.md`      | 无                                     |

## 跨阶段护栏

核心原则见 `overview.md`。以下规则定义见对应文件，此处仅索引：

| 规则                          | 定义所在                                                                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 奖励归一化审查                | `domain-comms.md` §1.5, `groundwork.md` S6                                                                                                 |
| Baseline 合法性               | `groundwork.md` S4-7                                                                                                                       |
| 方向可行性预判                | `gw-feasibility.md`                                                                                                                        |
| 文献检索验证                  | `contract.md` S0, `domain-comms.md` §1                                                                                                     |
| 参数溯源审计                  | `contract.md` S3                                                                                                                           |
| 子对话调度预算                | `contract.md` S0.2-0.4, `overview.md`                                                                                                      |
| 仿真器验证标准                | `groundwork.md` S7A                                                                                                                        |
| Contract 修正                 | `stages/contract.md`                                                                                                                       |
| 反模式审查位置                | `stages/contract.md` S5                                                                                                                    |
| 预印本验证                    | `gw-read.md`, `paper-materials-workflow.md` S5                                                                                             |
| 论文引用质量                  | `thesis-materials.md`                                                                                                                      |
| 可行性防坑规则 FR-01~08       | `stages/gw-feasibility.md` A0§1/§6, A', A, D; `tools-guide.md` §8; `stages/groundwork.md` 方法类型标注; `code-quality.md` 方法论适配性矩阵 |
| GNN 信息冗余检查 FR-09        | `code-quality.md` 方法论适配性矩阵                                                                                                         |
| 空间隔离约束决策模式 FR-10    | `code-quality.md` 方法论适配性矩阵                                                                                                         |
| MVE 架构溯源 FR-11            | `stages/gw-feasibility.md` §D — MVE 结果必须包含架构摘要（动作空间/决策粒度/对比范式/奖励语义）                                            |
| MVE→Formal 架构差异门控 FR-12 | `stages/gw-feasibility.md` §D — GW Step 6 必须与 MVE 架构比对，差异影响对比机制则重验证                                                    |
| 动作空间表达力下界审计 FR-13  | `stages/contract.md` Step 4 — data-flow.md 必须审计模型决策空间是否覆盖每个 baseline                                                       |
| MVE 先验对照要求 FR-14        | `stages/gw-feasibility.md` §D — MVE 必须包含最强简单先验 baseline，pass 标准为 DRL > 先验（非仅 > Random）                                 |
| MVE 贡献目标基线对照 FR-15    | `stages/gw-feasibility.md` §D — MVE 必须包含 Contract 假设中指定的 baseline（贡献声称要超越的对手），pass 标准含"提出方法 > 目标 baseline" |
| 架构信息增量审计 FR-16        | `stages/contract.md` Step 2 — 每个核心组件必须用两个不同输入验证产生不同输出；相同输出则无信息增量                                         |
| 空白零假设检查                | `stages/gw-feasibility.md` §B — 零交叉论文必须列出≥3个空白存在的结构性原因并逐一反驳                                                       |
| 瓶颈诊断                      | `stages/contract.md` Step 1 — 架构设计前必须诊断 baseline 性能瓶颈（表达力/学习效率/天花板）                                               |
| 信号方向熔断                  | `stages/execute.md` — 首次执行结果与 MVE/GW 预测方向相反时，必须做组件级信息流追踪                                                         |
| 实验完备性对标检查            | `stages/contract.md` S5, `templates.md` 自检清单, `domain-comms.md` §7                                                                     |
| 检索用项目工具                | `tools-guide.md`                                                                                                                           |
| 防死胡同                      | `stages/execute.md` S4.5                                                                                                                   |
| 先验基线测试                  | `stages/execute.md` S0.5                                                                                                                   |
| 领域指标约定审计 FR-17        | `stages/contract.md` S2 — 冻结指标前必须验证所选指标是该子领域的首选通行指标（抽查 ≥5 篇同子领域论文）                                    |
| 环境保真度竞争格局分析 FR-18  | `stages/gw-feasibility.md` §D FR-12后 + `stages/execute.md` S1 — 环境升级时分析对所有方法竞争格局的影响，不只看主方法                     |
| 指标模型假设敏感性 FR-19      | `stages/contract.md` S2 + `stages/execute.md` S4 — 指标依赖模型假设时记录假设+做替代假设对比                                             |
| MVE 关键参数溯源 FR-20        | `stages/gw-feasibility.md` §D 维度 D step 4 + `thesis-lessons.md` TL-26 — MVE 每个关键物理参数必须标文献来源，禁止"为了让方法有用"拍参数 |
| oracle 上界前置门控 FR-21     | `stages/gw-feasibility.md` §D 维度 D step 5 + `thesis-lessons.md` TL-27 — 可解析上界的增益先算上界，<0.5dB 直接 Kill 不跑 MVE            |
| GW 流程强制门控 FR-22         | `stages/groundwork.md` 全文 + `thesis-lessons.md` TL-30 — 任何"试新方法/新方向"动作必须先回答"当前在 GW 哪一步"，指不到具体 Step = 跳框架禁止开跑；Step 3（精读）+ Step 4a（可行性 Go/No-Go）是硬门控不可跳过，literature_notes 进度表任一项 ⬜ 时禁止进 MVE/Contract |
| 增量改进非填补空白 FR-23      | `.sessions/2026-06-17-thesis-method-redirection/decisions.md` D005 + `thesis-lessons.md` TL-04/TL-12/TL-31 — 研究起点 = 找 2019+ 顶刊/baseline 指出其具体不足（问题），不是找"没人做过 X"（空白）；空白只是新颖性证据，必须转译成"现有 M 在 C 下失效"才是问题 |
| 方法论/教训强制重读 FR-24     | `thesis-lessons.md` TL-31 — 涉及方法论、方向判断、创新定位、问题定义的输出，动笔前必须 Read 当前专题 decisions.md + thesis-lessons.md；发现自己要写"新方法论"时先 grep 是否已覆盖，已覆盖复用编号不新建；"我感觉/我记得"不是证据 |

## 上下文管理规则（跨步骤强制）

以下规则适用于所有阶段的所有步骤，不写在各步骤文档里以避免重复和漂移。

### 子 agent 强制委托

以下操作必须在子 agent 中执行，主对话只接收结构化摘要：

1. **论文全文精读**（gw-read）→ 子 agent 读 content.md，返回按模板提取的结构化数据
2. **web search / webReader 获取的信息**（gw-supplement 等）→ 子 agent 消化，返回 ≤500 词/篇的摘要
3. **引用链批量筛查**（≥10 篇的列表逐一查 abstract）→ 子 agent 执行，返回筛选后的候选列表
4. **MVE 实验执行**（gw-feasibility 维度 D）→ 子 agent 跑脚本，返回结果数字和分析
5. **子 agent 时间上限**：单次子 agent 执行不超过 15 分钟（约 900s）。任务拆分应确保单个子 agent 的工作量在此范围内。如果预计需要更长时间，必须拆分为多个子 agent 分批执行。

主对话负责：目标设定、边界框定、结果集成、最终判断。不负责大量文本的逐行消化。

### 主对话严禁 WebSearch / webReader

**[MUST]** 主对话（包括顶层和任何非子 agent 上下文）绝对不允许直接调用 WebSearch 或 `mcp__web_reader__webReader`。每次调用都会往上下文灌入大量 HTML，导致上下文爆炸。

- 文献检索 → 用 `tools/search`（脚本，结果结构化可控）
- 中文论文检索 → 用 `tools/search --source cnki` 或 `tools/blit --source cnki`（`--doc-type phd/master` 搜学位论文）
- 实在需要 web 查询 → **必须在子 agent 中执行**，子 agent 消化后返回 ≤500 词摘要
- 违反此规则的后果：上下文被撑满、有效信息被压缩丢失、对话提前终止

### web 事实性交叉验证

当 web search / webReader 对某论文做出功能/贡献断言时（如"论文 X 实现了 size generalization"）：

- **[MUST]** 用 Semantic Scholar API 或 DOI 直接查该论文 abstract 做交叉验证
- abstract 不支持该断言 → 标记为"AI 推断，未验证"，不作为 Go/No-Go 决策依据
- 记录到 `decision_log.md`
- **禁止**用 webReader 抓 ResearchGate / Google Scholar 页面替代 API 验证——会往上下文灌入大量无关 HTML

### 单对话步骤上限

单对话执行超过 **3 个步骤**时，主动建议分对话。写入 handoff 后由用户在新对话继续。

### 步骤间 handoff

每完成一个步骤更新 handoff（格式、写入时机、自包含要求见全局 AGENTS.md `.sessions/ 专题管理` 节）。路径：`.sessions/{date}-{project}/H{NNN}-{slug}.md`。

## 状态恢复

新对话恢复项目时，按以下优先级读取：

1. `projects-overview.md`（跨项目状态汇总，了解全局后再深入具体项目）
2. `projects/{name}/master-state.md`（Master 编排状态，当前步骤+已完成步骤+关键决策+FR 检查清单）
3. 项目记忆文件: `~/.Codex/projects/-mnt-d-code-study-research-protocol/memory/project_{name}.md`
4. `.sessions/*-{project}/` 下最新的 H{NNN} 文件（按编号排序取最大）
5. `decision_log.md`（阶段摘要行）
6. `feasibility_report.md`（如已到 Step 4）
7. `baseline_report.md`（如已到 Step 7）
8. `data-flow.md`（如已到 Contract Step 4）
9. 对应阶段框架文件

## 教训文档强制阅读

**[MUST]** 启动以下任务前，必须先读 `thesis-lessons.md`（至少读速查表和最近 3 条）：

- 仿真验证 / 仿真对比实验
- 文档批量同步 / 数字更新
- 宣布"重大发现"或"验证通过"
- 算法创新点提出或验证

核心教训摘要：
- TL-20: 跑仿真前先建理论预期，偏离即查
- TL-21: 文档数字审计用确定性 grep，不依赖 agent 链式标记
- TL-22: "震撼结果"先花 5 分钟查物理前提
- TL-23: 验证完毕再写文档，好结果触发冷静期

## 代码质量强制规范

**[MUST]** 准备 baseline、搭建仿真器、实现训练代码前，必须先读 `code-quality.md` 和 `reference/sim-template/` 中的对应模板。

具体要求：

- 新建 simulator 时，对照 `code-quality.md` 的必做清单逐项检查
- GNN 模型必须继承 `BaseActorCritic` 接口模式（`reference/sim-template/model_gnn.py`）
- 训练循环必须集成 wandb/tensorboard 和 early stopping（之前 6 个项目全部缺失，模板已补上）
- save/load 必须包含 optimizer + step_count，支持 resume
- 不重复已知缺陷（见 `code-quality.md` 常见缺陷表）

## 工具调用

`tools/` 下都是 **bash shell wrapper**，必须从项目根目录调用。派子 agent 时写完整命令：`cd /mnt/d/code/study/research-protocol && bash tools/search ...`。详见 `tools-guide.md` §1。

### PDF 转换（禁止自己搓）

遇到 PDF 转 markdown 需求时，**必须用 `tools/convert`**，不要自己写 pymupdf/pymupdf4llm 调用代码。

多篇并行转换默认输出 `{pdf_stem}.md`（按 PDF 文件名命名，互不覆盖）。批量转换用 `--batch`（自动按文件名建子目录）。

用法详见 `tools-guide.md` §3.5。

## 全局个人协作偏好

以下规则跨项目通用（来源：`~/.claude/CLAUDE.md` 个人偏好块），补充本项目的协作纪律。与上文"上下文管理规则"等已定义内容不重复，仅交叉引用。

### 协作风格

- 默认先讨论、先澄清、先锁边界，再进入执行
- facts-first / findings-first：先列事实和发现，再补总结
- 当前轮目标必须压窄，不顺手扩范围、补旧事项
- 没有新鲜验证证据，不宣称完成
- 规范书面中文

### 子 Agent 调度规则

> "哪些操作必须委托"见上文「上下文管理规则 / 子 agent 强制委托」。本节补充**任务分级**和**并发控制**。

按任务大小分级调度。主线程始终负责控场、汇总和拍板。

**并发控制**

- 一次最多同时开 3 个子 agent，不超发
- 需要开很多时，一批完成后再开下一批
- 后续批次可以利用前一批的产出来修正自己的 prompt 或范围

**小任务（1-2 个文件，无需验证链）**：主线程直接完成，不开子 agent。

**中任务（3+ 文件，需要测试验证）**

- **讨论阶段**：积极派 explore agent 并行检索相关代码和文档，不自己单线程查
- **执行阶段**：多独立任务时必须拆给 executor 子 agent 并行，不串行
- **验证阶段**：必须由独立 agent（code-reviewer / verifier）做，不自审自验

**大任务（跨对话、跨模块、跨前后端）**

- 比中任务更需要积极使用子 agent
- 每个对话内部按中任务规则执行
- 跨对话协作使用项目级的协作机制
- 典型拆分：讨论锁目标 → 规划拆任务 → 实施（1-3 个对话）→ 验证收尾

### 历史对话查阅

当用户提及之前对话的内容时，按关键词搜索历史记录。如需查看完整对话，将历史日志转为可读 markdown 再读。

### 压缩后上下文恢复

对话发生压缩（compact / away / continuation）后，若需要子 agent 恢复上下文，恢复 agent 必须按以下格式输出，总长度 ≤2000 字符。

**必填段（5 段）**

1. **Dead Ends / 被拒方案**（最高优先级）— 所有被讨论后否决的方向，附否决原因。这是压缩后最容易丢失且最致命的信息
2. **Progress Status / 进度状态** — DONE / IN PROGRESS / PENDING 三态标记，精确到子任务级别
3. **User Constraints & Intent / 用户约束与意图** — 用户明确表达的硬约束、偏好、期望
4. **Confirmed Decisions / 已确认决策** — 每条带强度标签：
   - `INVARIANT`：不可推翻的架构约束
   - `DECIDED`：已决定，可讨论但需显式推翻
   - `TENTATIVE`：暂定，后续可调整
5. **Intermediate Conclusions / 中间结论** — 分析过程中的量化发现和因果结论，保留具体数字

**可选段（有则填，无则省略）**

6. **Direction Changes / 方向变化** — 讨论过程中方向如何演变
7. **User Attitude / 用户态度** — 仅在有明确证据时填写（用户原话或行为），无证据时标 `insufficient data`，不推断。用户原话的持久来源是专题的 `voice.md`，本段落是压缩恢复时的临时投影
8. **Operational Obstacles / 操作障碍** — 遇到的技术困难（限速、结构发现、工具限制等）

**填写规则**

- 恢复输出必须包含"为什么"和"为什么不那样做"，不能只返回"做了什么"
- 量化数据保留具体数字（如"75.5%"而非"大多数"），不丢弃精度
- 恢复后不要立即全面规划，先确认约束和进度再推进
- 信息来源优先级：file > session_note > away_summary > inferred，推断内容必须标注 `[inferred]`

**Why:** 基于 187 个对话的大规模分析，压缩后最大的问题是"信息降级"而非"信息消失"——概念保留但边界丢失。Dead Ends 段落可单独预防 ~30% 的恢复后纠正。完整规范和分类法见 `.sessions/2026-05-24-context-recovery-spec/`。

### 分层试错法速查

当任务涉及不确定性、需要试错迭代时，遵守以下纪律。完整方法论文档见 `.sessions/2026-05-25-methodology/methodology.md`。

**触发条件（满足任一即生效）**

- 无法一开始确定最佳实现方法
- 已尝试 1 种方法但效果不达标
- 方案涉及 LLM/ML 等非确定性组件
- 框架步骤 ≥3 且步骤间有复杂交互

**7 条原则（一句话版）**

- **P1 假设先行**：动手前写清假设和退出判据，判据包含量化锚点
- **P2 失败截断**：连续 2 轮 <10% 改善 / 同方向 3 次未达标 → 强制截断
- **P3 最小切片**：每次只验证一个假设的一个维度，端到端贯通
- **P4 架构冻结**：决策分 INVARIANT / DECIDED / TENTATIVE 三级，约束级不可轻推翻
- **P5 前置门控**：质量标准写在做之前，用户干预时回溯门控缺失
- **P6 分离审查**：实现和审查用不同上下文，区分信号和噪声
- **P7 过程优先**：纪律放在"怎么做事"上，不放在"做事会得到什么"上

**压缩防护（3 条强制规则）**

- **F1**：Spike FAIL 结论立即写入 decisions.md（`status: rejected`），不能只留在 session note
- **F2**：迭代计数器每轮写入 session note 固定段落，恢复时读此段落
- **F3**：假设声明必须包含"否决条件"字段（什么情况下必须放弃该假设）

**适用范围**

- Lane A：不需要
- Lane B：P1 + P3 + P6 + F1-F3
- Lane C：全部

### 失败模式诊断速查

遇到问题时先匹配下表，再按策略处理。

| # | 失败模式 | 口语化信号 | 该做什么 |
|---|---------|-----------|---------|
| M1 | 管道断裂 | "上游给了下游没收到""字段对不上""下游没用上" | Pipeline 信息契约审计——逐字段校验上下游接口（分层试错法 Stage 1） |
| M2 | LLM 行为偏差 | "打分都差不多""全在中间档""LLM 总回避极端" | prompt 显式分布要求 + 评分量化触发条件（Prompt 方法论 #16-18） |
| M3 | 评估维度盲区 | "都挺垃圾""在垃圾堆里排座次""指标好了但用户说不行" | 引入人类参照锚点做绝对差距评估，跨样本验证维度通用性（评估驱动法 Phase 1） |
| M4 | 约束过载反向降质 | "越改越差""来回打补丁""补不完""LLM 全选不改" | 减约束 > 加约束，检查负面/正面比是否超 2:1（分层试错法 Stage 4） |
| M5 | 自审自验失效 | "自己给自己打分""checklist 全过但实际不行""你说好但用户说不行" | 生成和审查必须分离——不同上下文、不同 agent（分层试错法 P6） |
| M6 | 范围偏离 | "跑偏了""这不是我要的""偏离了最初目标" | 目标回溯检查——当前产出形态是否匹配原始需求？范围变更必须显式声明 |

**触发时机**

不要求主动查阅。以下情况出现时**必须**在此表匹配：

- 连续 2 轮迭代改善 <10%
- 用户对输出表达不满（"不行""垃圾""怪""不对"）
- 自动评估与人类判断不一致
- 迭代超过 3 轮仍无收敛迹象

### 自动提交规则

- **每个对话只提交一次**，在对话即将结束时（所有任务完成、准备收尾时）统一 commit
- **中途不提交**，不管完成了多少步骤、改了多少文件
- **commit 消息**：简明概括本对话完成的所有工作
- **例外**：用户明确要求提交时立即执行；对话涉及长时间运行的实验/训练时，可在实验启动前提交一次防丢失

**Why:** 碎 commit（每步一提）让 git log 噪音极大，30 次提交/3 天反而降低可读性。之前因"整块"定义模糊，实际执行成了每步一提。

### .sessions/ 专题管理

使用 `.sessions/` 目录管理跨对话的讨论、决策和交接过程。任何项目只要存在 `.sessions/` 目录就适用以下规则。

#### 专题注册表

`.sessions/_registry.yaml` 是全局专题注册表。每条记录含：slug、title、status（active / dormant / closed）、created、last_updated、description。

- **开新专题前必须查注册表**：若已有同方向专题且未 closed，应续旧专题而非另起炉灶。除非用户明确要求开新专题。
- **开新专题时必须登记**：在 `_registry.yaml` 中新增条目。slug 格式为 `YYYY-MM-DD[-HHMM]-主题简名`。

#### 编号体系（强制）

每个专题内的文件必须使用统一编号：

- `S` 前缀 = session note（讨论、决策、实施记录）
- `R` 前缀 = research note（调研、分析）
- `H` 前缀 = handoff（跨对话交接）
- `D` 前缀 = decision（决策记录，写在专题的 `decisions.md` 中，不单独建文件）
- `V` 前缀 = verification（验证记录，写在专题的 `verifications.md` 中，不单独建文件）
- 3 位递增编号：`S001`、`D003`、`V002`...，各前缀独立递增
- 文件名格式：`{前缀}{编号}-{简短描述}.md`（D/V 条目在单文件内用 `## D###:` 标题区分）

**禁止**使用 `NOTE-001`、`HANDOFF-001`、`handoff-v3.md`、`session-note.md`、`postmortem.md` 等无前缀或随机命名。

**无编号辅助文件**（每个专题最多各一个，与 `topic-index.md` 同构，不进 S/R/H/D/V 编号体系）：`topic-index.md`（必须）、`decisions.md`、`verifications.md`、`voice.md`（用户原话映射，见下节）。这些是索引/聚合文件，不是 session/research/handoff 记录。

#### decisions.md 和 verifications.md（每个专题可选）

每个专题可创建 `decisions.md`（决策记录）和 `verifications.md`（验证记录）。D### 和 V### 条目按编号排列在对应文件中，不单独建文件。

- `decisions.md`：架构决策、方向选择、路线失败记录。每条有取代/被取代字段形成血缘链。旧决策标 `superseded` 不删。
- `verifications.md`：实施验证、路线验证。每条关联 S### 或 D###，结论必须是 PASS/FAIL/PARTIAL 三选一。

创建时机：当专题首次产生符合 D### 或 V### 标准的内容时创建文件。不需要预先创建空文件。

#### voice.md（每个专题可选）

`voice.md` 是用户/导师原话的忠实档案——对抗转述失真、给决策溯源。和 `topic-index.md` 同构（无编号辅助文件，不进 S/R/H/D/V 编号体系）。

**极简原则：原话占主体，元数据压到最小。不为一条原话加数倍的说明（态度标签/归纳/语境注释都算说明）。**

- **收录**：除零信息推进/应答（"继续""嗯""好"）外都收，**不去重**（同一诉求多次说各自保留独立行）。纯操作指令（"跑测试""读文件"）不收。
- **格式**：每条原话一行，按日期归组。仅 `→产出`（可选，就 `→ D001` 不解释）、`[转述]`、`⟶冲突`（仅对立时）三种元数据；用户说的不标来源，仅导师/批注标。
- **创建时机**：专题首次产生符合收录边界的原话时创建，不预建空文件。
- **与 User Attitude 段落关系**：全局恢复规范的 `User Attitude / 用户态度` 段落从 `voice.md` 取原话（voice.md 持久源，User Attitude 临时投影）。

完整规范（收录边界/长原话/归档后手）见 session-governance skill 的 `references/voice-quote.md`。

#### 新建 vs 追加规则

- 专题起步时建 `S001-主题简述.md`
- 后续对话续接同一专题时，**默认追加到当前最后一个 S###**，不新建
- 只有以下情况才开新 S###：
  - 有大量新内容需要记录，且与当前 S### 的主题有明显区别
  - 追加会导致新旧内容冲突或理解困难（比如旧文件只需改几十行，但新内容要写上百行才能说明白）
  - 内容性质变了（S 切到 R，或反过来）
- 新开 S### 时编号 = 当前最大号 +1

#### topic-index.md（每个专题必须）

每个专题**必须**有 `topic-index.md`，内容含：专题标题和状态、进展线索（按编号列出每个文件摘要）、已确认结论、未决项、当前位置。

**已确认结论**必须分为两个子段落：

- **不变量**：架构约束级别的结论，动任何一条必须重新讨论
- **其他结论**：普通技术决策

**范围边界**必须包含：

- **原始目标**：不可修改，冻结记录
- **当前范围**：可随 scope-change 决策更新
- **明确不含**：显式排除项
- **范围变更记录**：每次范围变更必须记录（日期、决策D###、变更内容、原因）

新建专题时同步创建 `topic-index.md`。新增 session note / research note 后，若变更不大（补充细节、修措辞），直接更新上一条进展线索而非追加新条目；只有实质新阶段才新增条目。

#### 专题生命周期

- `active`：正在推进
- `dormant`：暂停，可能续接
- `closed`：已完成，不再更新

续接专题时先读 `topic-index.md`，再读最新 session note / handoff。续接后更新注册表 last_updated。

#### Session note 模板

每个 session note 必须包含以下锚点段落，段落内部允许自然展开。不需要的段落写"无"不要省略段落。

```markdown
# [S###] 标题

> YYYY-MM-DD | 阶段 | 状态
> （追加时新增一行日期，如 > 2026-05-18 续接）

## 目标

[本轮要完成什么]

## 记录

[正文。内容随阶段自然变：讨论进程、关键事件、决策表格、设计细节、实施日志等均可]

## 决策引用

- D###：[一句话摘要]（如果是本 session 做出的，标注"新建"）
- 无决策

## 范围确认

- 本轮是否在 scope boundary 内：是 / 否（如果否，见 scope change record）

## 后续

[未决项、下一轮需要知道的、待观察事项等。无则写"无"]
```

#### Research note 模板

```markdown
# [R###] 标题

> YYYY-MM-DD | 关联：专题 slug / D###

## 调研问题

[要回答什么问题]

## 发现

[调研结果]

## 结论

[回答调研问题]

## 对决策的影响

[这些发现是否影响现有决策？是否需要新建 D###？]
```

#### Handoff 模板

每个 handoff 必须包含以下锚点段落。不需要的段落写"无"不要省略段落。

```markdown
# Handoff: [交接主题]

> 来源: S### | 交接目标: [一句话]
> 文件名: H###-{简短描述}.md

## 已完成边界

[做了什么、当前做到哪一步]

## 不要做什么

[踩过的坑、已排除的方向、必须避免的做法]

## 必读

[下一轮对话开始时必须读的文件列表，按优先级排]

## 接口变更（如有代码改动）

[YAML 格式声明类型签名、prompt schema、跨模块依赖的变更。无代码改动写"无"]

## 失败数据附录（如涉及路线失败）

[具体失败数据，不能只写"失败了"。无则写"无"]

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

[具体可执行的下一步任务]
```

#### 治理 Skill 触发规则

在 `.sessions/` 项目中，以下 5 个时刻必须调用 session-governance skill：

1. **Session 启动**：续接或新开 session 时
2. **写决策**：提出新方向、推翻旧方案、路线验证失败时——**同步登记触发原话到 `voice.md`**（无锚点的态度原话也一并收；纯技术推导标"无"）
3. **扩大范围**：当前任务超出 session 目标时
4. **写 handoff**：创建 H### 文档时——**handoff 中用户关键指令/态度/约束必须 verbatim 引用并登记到 `voice.md`**
5. **收 handoff**：基于上一轮 handoff 开始工作时

Skill 包含详细检查逻辑和模板引用。范围越界/决策矛盾时**阻断要求显式确认**，不只是警告。

#### 专题注册表增强

`_registry.yaml` 每条记录应包含：

```yaml
- slug: topic-slug
  title: 专题标题
  status: active
  created: YYYY-MM-DD
  last_updated: YYYY-MM-DD
  description: 描述
  depends_on:                    # 可选
    - slug: other-topic-slug
      reason: 依赖原因
  conflicts_with: []             # 可选
  produces:                      # 可选
    - 产出物路径
```

开新专题时检查 `depends_on` 确保依赖专题已稳定，检查 `conflicts_with` 避免并行矛盾。

### 全局禁止事项

- 不把当前轮范围外的事项顺手塞进交付物
- 不先给结论再补事实
- 不跳过验证就宣称完成
- 不执行 `git reset --hard`、`git checkout -- .`、`git restore` 等会丢弃未提交改动的命令
- 不跳过 `.sessions/_registry.yaml` 查重就开新专题
- 不在 `.sessions/` 内使用无前缀或随机命名——必须用 `S`/`R` 编号
- 不创建没有 `topic-index.md` 的 `.sessions/` 专题
