---
name: research-resume
description: 从 handoff 恢复研究项目。触发：用户说"继续 XX 项目"、"resume"、"接续上次"，或新对话需要恢复项目状态。
---

# research-resume

从 handoff 文件恢复项目状态，加载当前步骤所需的框架文件，输出状态摘要后继续执行。

## 前置条件

- 项目目录 `projects/{name}/` 已存在
- 用户给出了项目名，或从上下文可推断

## 流程

### 1. 读取状态（按优先级）

依次尝试读取，找到即停止：

1. `projects/{name}/sessions/` 下最新的 handoff 文件（按日期排序取最新）
2. `~/.claude/projects/-mnt-d-code-study-research-protocol/memory/project_{name}.md`
3. `projects/{name}/decision_log.md`（阶段摘要行）
4. `projects/{name}/feasibility_report.md`（如存在）
5. `projects/{name}/baseline_report.md`（如存在）

### 2. 读取当前阶段框架文件

根据恢复到的阶段，读取对应文件：

| 阶段 | 必读文件 |
|------|---------|
| Groundwork Step 1-2 | `stages/gw-search.md` + `stages/gw-acquire.md` |
| Groundwork Step 3 | `stages/gw-read.md` |
| Groundwork Step 4a | `stages/gw-feasibility.md` §4a 部分 |
| Groundwork Step 5 | `stages/gw-validate.md` |
| Groundwork Step 4b | `stages/gw-feasibility.md` §4b 部分 |
| Groundwork Step 6-7 | `stages/gw-experiment.md` |
| Contract | `stages/contract.md` |
| Execute | `stages/execute.md` |

**强制重读规则**：即使之前读过，本轮上下文没有新鲜阅读证据 → 视为未读，必须补读。

### 3. 输出状态摘要

```
## 项目状态：{name}

**当前阶段**：{GW/Contract/Execute} Step {N}
**上轮完成**：{handoff 中记录的内容}
**本轮目标**：{下一步做什么}
**注意事项**：{handoff 中的坑/未解决决策}

准备开始执行。
```

### 4. 开始执行

输出摘要后，按当前步骤的 stage 文件继续执行。

## 禁止

- 不用"之前读过"替代实际阅读——压缩后续接必须重读
- 不跳过 handoff 直接读 decision_log（handoff 有更完整的上下文）
- 不在未读完当前阶段框架文件前开始执行
