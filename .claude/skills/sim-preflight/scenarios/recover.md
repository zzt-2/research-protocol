# 场景 D：新对话恢复前置（最高风险场景）

**这是最高风险场景**——新 agent 没有历史上下文，最容易跳过规则。任何"继续昨天的仿真工作"类对话，必须按本流程开始。

## Step 0：指令反问（如用户指令模糊）

用户说"继续昨天仿真/工作"且**无具体目标** → 反问 3 个问题：

1. **哪个专题？**（列 `_registry.yaml` 中 `status=active` 的专题，按 `last_updated` 降序）
2. **哪个未决项？**（列所选专题 `topic-index.md` 的"未决项"段）
3. **本轮输出形态？**（跑实验/写论文章节/加算法/分析）

用户明确后才进 Step 1。

## 恢复步骤（按顺序，不可跳）

### Step 1：读项目全局状态

1. **`projects-overview.md`** — 跨项目状态汇总
2. **`毕设/master-state.md`**（如有）— 当前章节+已完成+关键决策

### Step 2：读专题上下文

3. **`.sessions/_registry.yaml`** — 找到当前 active 专题
   - 多个 active 时：按 `last_updated` 降序，最近修改的是默认
   - 用户未明确时反问（见 Step 0）
4. **`.sessions/{专题}/topic-index.md`** — 专题进展、不变量、范围边界
5. **`.sessions/{专题}/H###` 最新 handoff**（按编号取最大）— 上轮做了什么、不要做什么、必读

### Step 3：读中断历史（强制，F1/F2 压缩防护）

```bash
# grep 多种写法（兼容历史未统一标签）
grep -rE "\[中断\]|INTERRUPT" .sessions/{专题}/ 2>/dev/null | tail -10

# 也查使用日志（中断必写日志）
LOG=.sessions/sim-preflight-log/usage-$(date +%Y-%m).md
test -f "$LOG" && grep "interrupts=\[" "$LOG" | tail -10
```

**grep 空时 fallback**：
- 0 命中 → 工作笔记写"无历史中断（首次执行或历史未启用中断标签）"
- **不中断**，继续 Step 4
- 但需提醒用户："本专题无中断历史，若上轮对话实际跑过仿真但被中断，请补充"

### Step 4：读关键决策 + 启动治理机制

7. **`.sessions/{专题}/decisions.md`**（如有）— D### 决策记录
8. **`.sessions/{专题}/verifications.md`**（如有）— V### 验证记录

**如 decisions.md 不存在 → 主动创建**（治理机制启动）：

```markdown
# Decisions — {专题}

> D### 决策记录：架构决策、方向选择、路线失败记录
> 每条有取代/被取代字段形成血缘链。旧决策标 superseded 不删。

## D001: [决策标题]
- **status**: active | superseded
- **supersedes**: 无 / D0XX
- **superseded_by**: 无
- **date**: YYYY-MM-DD
- **背景**: ...
- **决策**: ...
- **影响范围**: ...
```

在最新 handoff"约定变更"段记录："新建 decisions.md（治理机制启动）"。

### Step 5：调用本 skill 主文件

9. 回到 `SKILL.md`，按场景路由选具体场景文件执行

## topic-index 状态机处理

| topic-index 状态 | 用户意图 | 行动 |
|-----------------|---------|------|
| `active` 推进中 | 继续推进 | 续接，按 Step 1-5 |
| `active` 主体完成 + 有未决项 | 推进未决项 | 续接，**必须读"未决项"段** + 反问"本轮推进哪个未决项" |
| `active` 主体完成 + 无未决项 | 不确定 | 反问："主体已完成，是续接还是关闭？关闭后是否开新专题？" |
| `closed` 但用户要继续 | 续接 | 反问："专题已 closed，是续接（改回 active）还是开新专题？" |
| `dormant` | 唤醒 | 改回 active，续接 |

## 不变量

- **跳过 Step 1-4 直接跑代码 = 立即中断**（见 `rules/interrupt.md`）
- **Step 3 中断历史必读**——这是 F1/F2 压缩防护的核心机制
- **Step 4 decisions.md 不存在必须主动创建**，不能永远跳过

## 恢复后第一动作

恢复上下文后，**第一动作**必须显式声明：

```
我已读完：[列出文件]
当前状态：[用户上轮做到哪，topic-index 状态]
本轮计划：[按场景 X 文件执行]
```

等用户确认后再进入具体场景流程。

## 写使用日志

恢复完成后写日志（见 `rules/usage-log.md`）：

```
[YYYY-MM-DD HH:MM] 场景=D | 任务="恢复仿真工作" | routing=correct | interrupts=[] | changes=[] | issues="..." | duration=5min
```
