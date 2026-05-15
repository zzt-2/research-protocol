# 提示词：P0-1 步骤完成标记机制

## 任务

为 Groundwork 阶段增加步骤完成标记机制，解决跨对话恢复时 agent 重复执行已完成步骤的问题。

## 背景

审查发现：agent 跨对话恢复时无法快速判断哪些步骤已完成，导致浪费 20-40% token 重跑。当前步骤完成状态只存在于 git commit 消息中，无结构化标记。

详见 `.session/framework-evolution/LOG-001-framework-issues-2026-05-15.md` 的 P0-1。

## 要读的文件

1. `stages/groundwork.md` — 步骤编排表，理解 Step 1-7 的结构
2. `templates.md` — literature_notes 模板，找到头部插入进度表的位置
3. 任意一个已有项目的 `literature_notes.md`（如 `projects/leo-isl-scheduling-drl/literature_notes.md`）看当前头部结构

## 具体改动

### 1. `templates.md` — literature_notes 模板增加进度表

在 `literature_notes` 模板头部（标题行之后、核心论文精读之前）增加：

```markdown
## 步骤进度

| Step | 状态 | 完成日期 | Commit | 备注 |
|------|------|----------|--------|------|
| 1 检索 | ⬜ | | | |
| 2 获取 | ⬜ | | | |
| 3 精读 | ⬜ | | | ≥5 篇为单步门槛 |
| 3.5 补充 | ⬜ | | | |
| 4a 可行性 | ⬜ | | | |
| 5 Baseline | ⬜ | | | |
| 4b 仿真可行性 | ⬜ | | | 依赖 Step 5 产出 |
| 6 仿真器 | ⬜ | | | |
| 7 验证 | ⬜ | | | |

> 步骤完成时将 ⬜ 改为 ✅ 并填写日期和 commit hash。
```

### 2. `stages/groundwork.md` — 编排查表增加标记要求

在每个步骤的描述中增加一条：**完成时必须更新 `literature_notes.md` 步骤进度表**。

## 约束

- 进度表放在 `literature_notes.md` 头部（不是 `decision_log.md`），因为它是精读产物的附属
- 只改模板和流程定义，不改已有项目的 literature_notes
- 保持改动最小化，不引入新文件
