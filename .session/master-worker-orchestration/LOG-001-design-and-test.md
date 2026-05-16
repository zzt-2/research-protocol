# Master-Worker 编排系统 — 设计与演进日志

> 专题目录：`.session/master-worker-orchestration/`
> 用途：主对话编排系统的设计决策、测试记录、问题追踪、迭代改进
> 维护方式：所有 Master-Worker 相关的讨论、决策、测试结果都追加到此目录下的 LOG 文件

---

## LOG-001: 初始设计与端到端测试

> 日期：2026-05-16
> 状态：初版完成，测试通过

### 1. 背景

当前用户手动开多个 Claude Code 对话推进研究项目，每步手动喂 prompt、读输出、做决策。框架规则（FR-01~08）靠用户记住并提醒 agent，经常漏执行。

验证 `claude -p` 不限流且支持子 agent 后，决定构建 Master-Worker 编排层。

### 2. 架构

```
用户（交互式）
  └── 只做 Go/No-Go、方向调整、手动操作

Master 对话（交互式 Claude Code）
  ├── 持有 master-state.md（项目状态 + FR 检查清单 + 调度表）
  ├── 读框架文件，翻译成 Task 文件给 Worker
  ├── 派遣: claude -p --append-system-prompt ... --max-budget-usd ...
  ├── 判断 Worker 输出，记录 decision_log
  └── 关键节点提交 git commit

Worker（claude -p，无状态）
  ├── 读 Task 文件 + 指定框架文件
  ├── 执行具体步骤（搜索/精读/MVE/仿真）
  ├── 可内开子 agent（精读论文、跑实验）
  ├── 写 worker-log（审计 + 框架反馈）
  └── 返回 structured summary（≤50 行）
```

### 3. 核心设计决策

| 决策 | 选择 | 原因 |
|------|------|------|
| Worker 是否读框架文件 | **读** | 框架文件经过大量打磨，Master 翻译会丢失信息 |
| Worker log 位置 | `projects/{name}/worker-logs/` | 随项目走，git 追踪，方便回看 |
| Worker 权限模式 | `bypassPermissions` | 研究任务已信任，自动执行不经确认 |
| Worker task 文件 | `projects/{name}/worker-tasks/`（ephemeral） | .gitignore 不提交，每次派遣前 Master 写入 |
| decision_log 由谁写 | **Master** | 风格一致，Worker 只返回事实和发现 |
| Worker 是否写 handoff | **不写** | Master 自己维护所有状态 |
| 同时开几个 Worker | **1 个** | 串行控制，避免并发冲突 |
| Master 状态持久化 | 三层：master-state.md / handoff / memory | master-state.md 始终最新，新对话读此文件恢复 |

### 4. 产出物清单

| 文件 | 说明 |
|------|------|
| `templates/master-state-template.md` | Master prompt 模板（~250 行，9 章节） |
| `projects/{name}/master-state.md` | 项目实例（Master 每步后更新） |
| `projects/{name}/worker-logs/step-{N}-{slug}.md` | Worker 执行日志 |
| `projects/{name}/worker-tasks/step-{N}-task.md` | Worker 任务文件（ephemeral） |

### 5. 端到端测试结果

**测试项目**: leo-resilient-routing
**测试步骤**: 定向检索 MARL 抗毁路由竞品
**Worker 命令**:
```bash
claude -p \
  --append-system-prompt "..." \
  --allowed-tools "Bash Read Glob Grep Write Edit Agent" \
  --max-budget-usd 1.5 \
  --effort high \
  --permission-mode bypassPermissions \
  "执行定向检索测试..."
```

**结果**: 通过
- Worker 执行了 3 组搜索（90+ 条结果）
- Worker log 完整写入 75 行（结构化）
- Worker 返回明确结论（MARL 路由已有竞品，MARL+课程学习+抗毁 仍为空白）
- 质量门 3/3 通过
- Worker 未直接修改 decision_log.md 或 master-state.md

### 6. 发现的问题与待改进

#### P1: Worker log "框架反馈"和"自评遗漏"章节未填写
- **现象**: Worker 写了执行过程和结论，但跳过了"框架反馈"和"自评遗漏"
- **原因**: Task 文件中没有显式要求这两个章节
- **修复**: Task 文件模板中增加提醒："Worker log 必须包含'框架反馈'和'自评遗漏'章节，即使写'无'"

#### P2: Worker log "Master 摘要"与全文有重复
- **现象**: 75 行 log 中，总结部分和全文分析有信息重复
- **影响**: 不大，Master 主要读 summary，全文只在审计时看
- **暂不修复**: 等更多 Worker log 积累后再优化格式

#### P3: Worker stdout 和 worker-log 的关系不明确
- **现象**: Worker 的 stdout（claude -p 返回给 Master 的文本）和 worker-log 文件内容有重叠
- **当前行为**: stdout 是简短结论，worker-log 是完整记录
- **这是正确的行为**: Master 读 stdout 做快速判断，需要细节时读 worker-log

### 7. 未测试的场景

| 场景 | 风险 | 计划 |
|------|------|------|
| Worker 超时/崩溃 | 中 | 下次测试时故意给短超时 |
| Worker 质量门失败 | 中 | 等实际跑 4a 步骤时观察 |
| Master 上下文溢出恢复 | 高 | 需要跑 3+ 步骤后测试 |
| Worker 内开子 agent 精读论文 | 中 | Step 3 时测试 |
| 长步骤（Step 7 implement）| 高 | 预算 5 USD，可能不够 |
| 完整 GW 流程串行跑通 | 高 | 用 beam-hopping 项目从头测试 |

### 8. 使用的 CLI flags 确认可用

| Flag | 用途 | 状态 |
|------|------|------|
| `--append-system-prompt` | 注入 Worker 身份和规则 | ✅ 可用 |
| `--allowed-tools` | 限制 Worker 可用工具 | ✅ 可用 |
| `--max-budget-usd` | 控制单次 Worker 成本 | ✅ 可用 |
| `--effort high` | 提高执行质量 | ✅ 可用 |
| `--permission-mode bypassPermissions` | Worker 自动执行 | ✅ 可用 |
| `claude -p` 基础非交互模式 | Worker 运行方式 | ✅ 不限流 |
| `claude -p` 内开子 agent | Worker 精读论文 | ✅ 可用 |

### 9. 下一步

1. **实战测试**: 用 beam-hopping 项目从 Step 1 开始跑完整 GW 流程
2. **模板调优**: 根据实战积累的 worker-log 优化 Task 文件和 Log 格式
3. **Master 指令优化**: 如果发现 Master 经常遗漏某些检查，强化 master-state.md 中的检查清单
4. **考虑 Contract/Execute 阶段**: 当前模板只覆盖 GW，后续需要扩展
