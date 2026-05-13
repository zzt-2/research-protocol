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
├── reference/           # 参考实现代码
├── tools/               # 辅助脚本
└── projects/{name}/     # 独立研究项目（全部项目级产物在此）
    ├── decision_log.md
    ├── literature_notes.md
    ├── feasibility_report.md
    ├── competitor_notes/
    ├── baseline_report.md
    ├── search-archive/   # 项目专属检索记录（Contract 阶段等）
    ├── sessions/         # 跨对话交接记录（handoff）
    ├── simulator/
    ├── baselines/
    ├── results/
    └── verify/
```

## 文件路径规则（禁止自作主张）

每类文件有且仅有一个存放位置，不允许在根目录随意创建目录或文件。

| 产物 | 生成方式 | 存放路径 |
|------|----------|----------|
| 检索结果 JSON | `tools/search` 自动保存 | `search-archive/{YYYY-MM-DD}/{slug}.json` |
| 论文下载（arXiv） | `tools/download` | `papers/arxiv/{arxiv_id}/source.{html,tar.gz,pdf}` + `content.md` |
| 论文下载（DOI） | `tools/download` | `papers/doi/{doi_path}/source.pdf` + `content.md` |
| 论文下载（无 ID） | `tools/download` | `papers/manual/{slug}/source.pdf` + `content.md` |
| PDF 转 markdown | `tools/convert` | 输出到 PDF 同目录，文件名 `{pdf_stem}.md` |
| 手动下载的 PDF | 用户操作 | 放入 `papers/downloads/{date}/`，之后用 `tools/convert` 转换 |
| 参考实现代码 | 手动管理 | `reference/{name}/` |

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

具体要求：
- 进入新阶段（如 GW → Contract）→ 必须读 `stages/{stage}.md`
- 进入新步骤（如 GW Step 3 → Step 3.5）→ 必须读该步骤的职责文件（如 `gw-supplement.md`）
- 跨对话续接、上下文压缩后恢复 → 同样必须重读
- 对话中如果涉及运行时机制（仿真器、processor 等），还要额外读对应 spec

### 文档职责边界

每条约束只有一个拥有者（完整定义所在文件），其他文件只引用。文档层级：

| 层级 | 文件 | 职责 |
|------|------|------|
| 通用原则 | `overview.md` | 核心原则、文档系统概览 |
| 阶段流程 | `stages/*.md` | 该阶段的完整操作流程 |
| 领域定制 | `domain-comms.md` | 领域特定技术栈、指标、反模式 |
| 模板定义 | `templates.md` | 文档模板和字段规则 |
| 本文件 | `CLAUDE.md` | 环境配置、目录结构、规则索引（不重复框架文件内容） |

## 跨阶段护栏

核心原则在 `overview.md` 中有完整说明（Baseline-first / Human-in-the-loop / 单一事实源）。

以下高风险规则的完整定义见对应框架文件，此处仅作索引：

- **奖励函数归一化和用户审查**：`domain-comms.md` §1.5 + `groundwork.md` Step 6
- **Baseline 学术合法性和复现定义**：`groundwork.md` Step 4-7
- **方向可行性预判**：`gw-feasibility.md`（分两段：4a 方向根基+MVE 验证 + 4b 仿真条件+资源风险验证）
- **文献检索、验证和 URL 校验**：`contract.md` Step 0 + `domain-comms.md` §1
- **子对话调度和上下文预算**：`contract.md` Step 0.2-0.4 + `overview.md` "上下文管理策略"
- **仿真器验证标准**：`groundwork.md` Step 7 Part A
- **参数来源验证**：所有仿真参数、网络模型参数、信道模型参数必须有论文出处（标注论文 ID + 表格/公式编号）。无法溯源的标注 `[ASSUMPTION]` 并在 `feasibility_report.md` 中标记为待验证项。禁止编造数值。

## 上下文管理规则（跨步骤强制）

以下规则适用于所有阶段的所有步骤，不写在各步骤文档里以避免重复和漂移。

### 子 agent 强制委托

以下操作必须在子 agent 中执行，主对话只接收结构化摘要：

1. **论文全文精读**（gw-read）→ 子 agent 读 content.md，返回按模板提取的结构化数据
2. **web search / webReader 获取的信息**（gw-supplement 等）→ 子 agent 消化，返回 ≤500 词/篇的摘要
3. **引用链批量筛查**（≥10 篇的列表逐一查 abstract）→ 子 agent 执行，返回筛选后的候选列表
4. **MVE 实验执行**（gw-feasibility 维度 D）→ 子 agent 跑脚本，返回结果数字和分析

主对话负责：目标设定、边界框定、结果集成、最终判断。不负责大量文本的逐行消化。

### web 事实性交叉验证

当 web search / webReader 对某论文做出功能/贡献断言时（如"论文 X 实现了 size generalization"）：

- **[MUST]** 用 Semantic Scholar API 或 DOI 直接查该论文 abstract 做交叉验证
- abstract 不支持该断言 → 标记为"AI 推断，未验证"，不作为 Go/No-Go 决策依据
- 记录到 `decision_log.md`
- **禁止**用 webReader 抓 ResearchGate / Google Scholar 页面替代 API 验证——会往上下文灌入大量无关 HTML

### 单对话步骤上限

单对话执行超过 **3 个步骤**时，主动建议分对话。写入 handoff 后由用户在新对话继续。

### 步骤间 handoff 强制写入

每完成一个步骤，必须更新 handoff 文件（`projects/{name}/sessions/{date}-handoff.md`）：
- 当前步骤产出文件路径
- 关键结论（1-3 句）
- 未决问题（如有）
- 下一步操作（引用具体文件路径）

目的：context overflow 恢复后只需读 handoff，不需重跑已完成步骤。

## 跨对话协作

### 交接机制（handoff）

跨对话推进同一项目时，使用 `projects/{name}/sessions/` 管理交接：

- 每次对话结束前（包括上下文溢出导致压缩时），写 handoff 文件到 `projects/{name}/sessions/`
- handoff 文件名格式：`{YYYY-MM-DD}-handoff.md`（同一天多次用 `-handoff-2.md` 递增）
- 新对话恢复项目时，先读 handoff 再读其他文件
- handoff 不重复项目正式文档内容，只补充跨对话上下文和待办

### handoff 格式

```markdown
# Handoff {YYYY-MM-DD}

## 当前进度
- 阶段：{GW/Contract/Execute} Step {N}
- 状态：{进行中/阻塞/完成}
- 本轮完成：{具体做了什么，引用文件路径}

## 关键上下文
- 正在处理的问题：{如果有}
- 未解决决策：{如果有}
- 需要注意的坑：{如果有}

## 下一步
1. {具体操作，引用文件路径}
```

### 写入时机

- 用户说"新对话继续"或"给我提示词"时
- 上下文即将压缩时
- 切换子 agent 执行长任务前

## 状态恢复

新对话恢复项目时，按以下优先级读取：

1. 项目记忆文件: `~/.claude/projects/-mnt-d-code-study-research-protocol/memory/project_{name}.md`
2. `projects/{name}/sessions/` 下最新的 handoff 文件
3. `decision_log.md`（阶段摘要行）
4. `feasibility_report.md`（如已到 Step 4）
5. `baseline_report.md`（如已到 Step 7）
6. 对应阶段框架文件

## 工具调用

`tools/` 下都是 **bash shell wrapper**，必须从项目根目录调用。派子 agent 时写完整命令：`cd /mnt/d/code/study/research-protocol && bash tools/search ...`。详见 `tools-guide.md` §1。

### PDF 转换（禁止自己搓）

遇到 PDF 转 markdown 需求时，**必须用 `tools/convert`**，不要自己写 pymupdf/pymupdf4llm 调用代码。

多篇并行转换默认输出 `{pdf_stem}.md`（按 PDF 文件名命名，互不覆盖）。批量转换用 `--batch`（自动按文件名建子目录）。

用法详见 `tools-guide.md` §3.5。
