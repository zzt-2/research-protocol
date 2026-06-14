# 使用日志（强制写入，月度审计的基础）

## 文件位置

`.sessions/sim-preflight-log/usage-{YYYY-MM}.md`（按月切分）

如目录不存在，**首次写日志时由 agent 主动创建**：

```bash
mkdir -p .sessions/sim-preflight-log
```

## 日志条目格式（一行制，可 grep）

```
[YYYY-MM-DD HH:MM] 场景=X | 任务="<简述>" | routing=correct|wrong|ambiguous|interrupted | interrupts=[类型 N] | self-check=none|passed|failed | changes=[约定变更简述] | issues="<问题简述 或 none>" | duration=<耗时 或 stuck>
```

字段说明：

| 字段 | 取值 | 含义 |
|------|------|------|
| 场景 | A/B/C/D/multi/archive | SKILL.md 决策树路由结果 |
| 任务 | 字符串 | 用户原话简述（≤30 字） |
| routing | correct / wrong / ambiguous / interrupted | 路由判断是否准确 |
| interrupts | `[类型 N]` 或 `[]` | 触发的中断类型（见 interrupt.md 1-8） |
| self-check | none / passed / failed | 自检 agent 结果 |
| changes | `[参数 X→Y]` 或 `[]` | 约定变更简述 |
| issues | 字符串 或 `none` | 遇到的问题（skill 缺陷候选） |
| duration | `<N>min` 或 `stuck` | 耗时；卡死标 stuck |

## 真实示例（**这些数字已 grep 验证**）

```
[2026-06-15 14:23] 场景=A | 任务="改 sigma2_turb_weak 跑 BER" | routing=interrupted | interrupts=[2] | self-check=pending | changes=[] | issues="用户口述 0.05 与真值 1e-6 不符" | duration=stuck
[2026-06-15 14:45] 场景=B | 任务="加 BPS" | routing=ambiguous | interrupts=[] | self-check=none | changes=[] | issues="BPSParams 已存在但无 common/_bps.py" | duration=15min
[2026-06-15 15:00] 场景=D | 任务="恢复仿真工作" | routing=correct | interrupts=[] | self-check=none | changes=[] | issues="decisions.md 不存在，主动创建" | duration=5min
```

## 写入时机（强制）

| 时机 | 写入触发 |
|------|---------|
| 场景 A "改" 步骤结束 | 不论成功/失败 |
| 场景 B "改" 步骤结束 | 不论成功/失败 |
| 场景 C "改" 步骤结束 | 不论成功/失败 |
| 场景 D 恢复完成 | Step 0-5 全部完成后 |
| `interrupt.md` 中断触发 | 双写（session note + usage-log） |
| 自检 agent 返回结果 | pass/fail 都写 |
| `archive.md` 归档完成 | Step 6 |

## B 方案（事后审计，不强制事中）

**写入依赖 agent 自觉，可能漏写**。本 skill 采用 B 方案：

- **不**在事中强制中断（避免拖慢流程）
- 在 SKILL.md §5 加"使用日志验证"自检命令：每月至少 1 条日志，漏写在下次 audit 才暴露
- 月度审计（`rules/audit-skill.md`）必查"本月日志数 vs 本月 handoff 数"，比例异常 → 警告

## 不要写的内容

- **完整对话历史**——日志只记一行关键事实
- **完整代码 diff**——changes 字段只写"参数 X→Y"简述
- **主观感受**（"我觉得很顺"）——只记客观事实

## 日志归档

`usage-{YYYY-MM}.md` 文件本身不归档（每月一个文件，长期保留）。半年后 grep 全部月度文件做趋势分析。
