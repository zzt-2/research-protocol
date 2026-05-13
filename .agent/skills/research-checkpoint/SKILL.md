---
name: research-checkpoint
description: 完成当前步骤，检查质量门槛，写 handoff，转场到下一步。触发：当前步骤的实质工作完成，准备转场；或用户说"checkpoint"、"完成这步"。
---

# research-checkpoint

当前步骤完成后的标准化收尾：检查质量门槛 → 检查路径合规 → 写 handoff → 确定下一步。

## 前置条件

- 当前步骤的实质工作已完成
- 知道项目名和当前阶段/步骤

## 流程

### 1. 质量门槛检查

读取当前步骤的 stage 文件，找到"质量门槛"部分，逐条检查：

```
## 质量门槛检查：{Step名称}

- [ ] {门槛1}：{通过/未通过，附证据}
- [ ] {门槛2}：{通过/未通过，附证据}
- [ ] 路径合规：{通过/未通过，列出产出文件路径}
```

**任一门槛未通过 → 不转场，修复后重新检查。**

### 2. 人介入检查

查看当前步骤是否有人介入点（stage 文件中标记 `[MUST]` 的）：

- 需要人介入 → 停下来等用户确认，不自动继续
- 不需要 → 继续下一步

### 3. 写 handoff

写入 `projects/{name}/sessions/{YYYY-MM-DD}-handoff.md`（同一天多次用 `-handoff-2.md` 递增）：

```markdown
---
name: {项目名} handoff
description: {Step} 完成，转场到 {下一步}
type: handoff
---

# Handoff {YYYY-MM-DD}

## 当前进度
- 阶段：{GW/Contract/Execute} Step {N}
- 状态：{完成/阻塞}
- 本轮完成：{具体做了什么，引用产出文件路径}

## 关键上下文
- 正在处理的问题：{如果有}
- 未解决决策：{如果有}
- 需要注意的坑：{如果有}

## 下一步
1. {具体操作，引用文件路径}
```

### 4. 更新项目记忆

更新 `~/.claude/projects/-mnt-d-code-study-research-protocol/memory/project_{name}.md` 的"当前状态"部分。

### 5. 输出转场摘要

```
## Checkpoint 完成

**步骤**：{Step名称} ✅
**质量门槛**：全部通过
**人介入**：{需要/不需要}
**下一步**：{Step名称}（{一句话描述}）
**Handoff**：已写入 {路径}
```

## 禁止

- 质量门槛未通过时不转场——不带着已知问题进入下一步
- 不跳过 handoff 写入——即使上下文未溢出也要写
- 不替用户做需要人介入的决策
