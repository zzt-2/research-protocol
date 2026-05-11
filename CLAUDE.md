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
├── papers/              # 论文归档（按日期+主题）
├── search-archive/      # 搜索结果缓存
├── tools/               # 辅助脚本（pdf_convert.py 等）
└── projects/{name}/     # 具体研究项目
    ├── config.py        # 仿真参数
    ├── decision_log.md  # 决策记录
    ├── literature_notes.md
    ├── simulator_design.md
    ├── baseline_report.md
    ├── simulator/       # 仿真器代码
    ├── baselines/       # baseline 实现
    ├── results/         # 实验结果
    └── verify/          # 验证脚本
```

## 框架文件是执行规范

以下文件不是"参考文档"，是必须读并遵守的执行规范：

- `stages/groundwork.md` — Groundwork 阶段每一步的操作、检查点、通过条件
- `templates.md` — 文档模板中的 `[MUST]` 和 `{占位符}` 规则
- `domain-comms.md` — 通信领域定制（非通信项目跳过）

开始任何阶段前，先读对应框架文件，按步骤执行。不要凭记忆或通用经验跳步。

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

- **奖励函数归一化和用户审查**：`domain-comms.md` §1.5 + `groundwork.md` Step 5
- **Baseline 学术合法性和复现定义**：`groundwork.md` Step 4-6
- **文献检索、验证和 URL 校验**：`contract.md` Step 0 + `domain-comms.md` §1
- **子对话调度和上下文预算**：`contract.md` Step 0.2-0.4 + `overview.md` "上下文管理策略"
- **仿真器验证标准**：`groundwork.md` Step 6 Part A

## 状态恢复

新对话恢复项目时，按以下优先级读取：

1. 项目记忆文件: `~/.claude/projects/-mnt-d-code-study-research-protocol/memory/project_{name}.md`
2. `decision_log.md`（阶段摘要行）
3. `baseline_report.md`（如已到 Step 6）
4. 对应阶段框架文件

## 工具调用

`tools/` 下都是 **bash shell wrapper**，必须从项目根目录调用。派子 agent 时写完整命令：`cd /mnt/d/code/study/research-protocol && bash tools/search ...`。详见 `tools-guide.md` §1。

### PDF 转换（禁止自己搓）

遇到 PDF 转 markdown 需求时，**必须用 `tools/convert`**，不要自己写 pymupdf/pymupdf4llm 调用代码。

**多篇并行转换必须各自用 `-o` 指定不同输出目录**，否则默认写同目录的 `content.md` 会互相覆盖。批量转换用 `--batch`（自动按文件名建子目录）。

用法详见 `tools-guide.md` §3.5。
