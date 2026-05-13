---
name: research-init
description: 初始化新的研究方向项目。触发：用户说"开始新方向"、"新建项目"、"research init"，并给出研究方向描述。
---

# research-init

从零初始化一个研究项目，创建标准目录结构，加载框架文件，启动 Step 1。

## 前置条件

- 用户已给出研究方向描述
- 项目根目录是 `/mnt/d/code/study/research-protocol`

## 流程

### 1. 确定项目名

从用户的方向描述中提取一个简短英文 slug（如 `ris-phase-drl`、`leo-ntn-handover-drl`）。确认目录 `projects/{name}/` 不存在（已存在则问用户是否续接，如果是 → 走 `/research-resume`）。

### 2. 创建目录结构

```
projects/{name}/
├── sessions/
├── competitor_notes/
├── search-archive/
├── simulator/
├── baselines/
├── results/
└── verify/
```

### 3. 加载框架文件

按顺序读取（后续步骤需要引用）：

1. `CLAUDE.md` — 环境配置、目录规则、跨阶段护栏
2. `overview.md` — 核心原则、三阶段模型、上下文管理策略
3. `domain-comms.md` — 仅通信领域研究读（非通信跳过）
4. `stages/groundwork.md` — 7 步编排表
5. `stages/gw-search.md` — Step 1 检索流程

### 4. 写项目记忆

在 `~/.claude/projects/-mnt-d-code-study-research-protocol/memory/` 下创建 `project_{name}.md`，内容：

```markdown
---
name: {项目名}
description: {一句话方向描述}
type: project
---

## 当前状态
- 阶段：Groundwork Step 1
- 创建日期：{YYYY-MM-DD}

## 方向
{用户的方向描述}
```

### 5. 启动 Step 1

读完框架文件后，直接按 `stages/gw-search.md` 开始执行文献检索。构造搜索关键词（≥3 组不同角度），用 `bash tools/search` 检索。

### 6. 约束提醒（执行前向用户确认）

在开始检索前，向用户确认：

- 项目名是否正确
- 研究方向描述是否准确
- 是否为通信领域（决定是否读 `domain-comms.md`）

## 禁止

- 不跳过框架文件阅读直接开始
- 不自己编造搜索关键词，必须基于用户的方向描述
- 不在项目目录外创建任何文件
