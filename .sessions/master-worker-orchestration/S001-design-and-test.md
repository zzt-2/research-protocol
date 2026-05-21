# Master-Worker 编排系统 — 设计与演进日志

> 专题目录：`.sessions/master-worker-orchestration/`
> 用途：主对话编排系统的设计决策、测试记录、问题追踪、迭代改进
> 维护方式：所有 Master-Worker 相关的讨论、决策、测试结果都追加到此目录下的 LOG 文件

---

## LOG-001: 初始设计与端到端测试

> 日期：2026-05-16
> 状态：初版完成，测试通过

### 1. 核心问题与动机

#### 1.1 当前痛点

用户（PhD 学生）使用一套精心打磨的研究协议框架推进多个研究方向。框架包含 9 个 GW 步骤、8 条 FR 防坑规则、代码质量检查清单等。但实际执行中：

- **规则执行靠人记忆**：FR-01~08、代码质量必做清单等规则，需要用户在每次对话中主动提醒 agent。用户缺乏相关经验，全靠框架约束，但框架约束本身又依赖用户自觉执行。
- **手动开对话太碎**：每个步骤或每 2-3 个步骤就需要手动开新对话、喂 prompt、读输出、写 handoff。频繁的上下文切换消耗大量精力。
- **跨对话知识丢失**：每个新对话从零开始，不记得之前踩过的坑。框架文件记录了通用规则，但具体项目的上下文（比如"resilience 项目 4a 时 FR-01 触发了先验覆盖问题"）需要用户自己回忆。

用户的原话："我没什么相关经验，全靠框架约束。我的位置可以靠更好的约束解决。"

#### 1.2 根本洞察

问题的本质不是框架规则不够好，而是**规则的执行层缺失**。框架写了"Step 4a 必须检查 FR-01~08"，但没有机制保证每个 agent 真的去检查。

传统解法是"写更好的规则"，但用户提出了另一个方向：**能不能让 AI 自动执行这些规则？** 不依赖人记忆，不依赖 agent 自觉，而是由一个持久的"主控"agent 自动检查。

这就是 Master-Worker 的核心动机：**把规则执行从"人监督 agent"变成"agent（Master）监督 agent（Worker）"**。

#### 1.3 为什么不是子 agent？

Claude Code 已有子 agent（Agent tool）。为什么不用子 agent 直接编排？

| 对比维度     | 子 agent                          | Worker (claude -p)                    |
| ------------ | --------------------------------- | ------------------------------------- |
| 上下文       | 共享 Master 的上下文空间          | **独立上下文**，不占 Master 空间      |
| 上下文溢出   | 子 agent 大量输出会撑爆 Master    | Worker 输出只有 stdout 摘要（≤50 行） |
| 持久性       | 随 Master 对话消亡                | Worker log 文件永久保存               |
| 可审计性     | 子 agent 过程在对话历史里，难检索 | Worker log 是独立文件，随时可查       |
| 框架文件访问 | 需要重新读（或 Master 转述）      | Worker 自己读，完整访问               |
| 成本         | 共享 token 预算                   | 独立预算（--max-budget-usd）          |

关键差异是**上下文隔离**：论文全文、搜索结果 JSON 等重上下文操作，如果用子 agent 做，所有输出都留在 Master 上下文里，3 步就满了。Worker 模式下，这些重操作在独立上下文完成，Master 只接收结构化摘要。

#### 1.4 可行性验证

在正式设计前做了 3 轮验证测试：

1. **基础测试**：`claude -p "回复'测试成功'"` → 一次性返回，无限流
2. **子 agent 测试**：`claude -p` 内开 Agent tool 读文件 → 成功
3. **高强度测试**：5 组批量搜索 + 结果汇总 + 去重分析 → 耗时约 7 分钟，完整输出，无限流

这 3 轮测试排除了"claude -p 限流"和"子 agent 不可用"两个最大风险。

### 2. 架构设计

#### 2.1 三层分工

```
用户（交互式）
  └── 职责：Go/No-Go 决策、方向调整、需要校园网等手动操作
  └── 不做：步骤执行、规则检查、文档编写、提交管理

Master 对话（交互式 Claude Code）
  └── 职责：
  │   - 持有项目全局状态（master-state.md）
  │   - 持有 FR-01~08 检查清单（内嵌在 master-state.md）
  │   - 读框架文件，为 Worker 编写 Task 文件（指定该读哪些框架文件）
  │   - 派遣 Worker（claude -p）执行具体步骤
  │   - 接收 Worker 结构化摘要，判断质量门
  │   - 写 decision_log.md
  │   - 关键节点提交 git commit
  └── 禁止：
      - 直接读论文 content.md
      - 直接跑 WebSearch / webReader
      - 直接跑长时脚本

Worker（claude -p，无状态）
  └── 职责：
  │   - 读 Task 文件 + 指定框架文件
  │   - 执行具体步骤（搜索/下载/精读/MVE/仿真实现）
  │   - 可内开子 agent（精读论文、跑实验）
  │   - 写 worker-log（审计 + 框架反馈）
  │   - 返回 structured summary（≤50 行）
  └── 不做：
      - 不写 decision_log（只返回发现，Master 记录决策）
      - 不写 handoff（Master 维护所有状态）
      - 不做 Go/No-Go 决策
```

**关键约束：同时只开一个 Worker。** 原因：

- 简化状态管理：Worker 产出是下一步 Worker 输入，串行保证依赖关系
- 文件无冲突：多个 Worker 写同一个文件会冲突
- Master 能从每个 Worker 输出学习，优化下一个 Worker 的 Task 文件

#### 2.2 Worker 读不读框架文件？

这是设计过程中讨论最久的一个决策。

**方案 A：Worker 不读框架文件，Master 翻译规则成具体指令**

- 优势：Worker 任务更聚焦，不会"漏读"框架文件
- 风险：框架文件经过 6 个项目的打磨，Master 翻译必然丢失细节。比如 gw-read.md 的精读模板有 ~20 个必填字段，Master 每次都要完整列举，一旦遗漏就是质量下降

**方案 B：Worker 读框架文件，Master 指定读哪些**

- 优势：框架文件的完整信息不丢失，Worker 能按原文执行
- 风险：Worker 可能"读了但没执行"，或者被框架文件中的不相关章节分散注意力
- 缓解：Master 在 Task 文件中指定读哪些文件、读哪些章节

**最终选择：方案 B。** 用户明确表示"框架文件是经过大量打磨的，不读会丢失很多信息"。这个判断基于实际经验——之前多次出现 agent "简化"框架要求导致产出质量下降的情况。

Master 的角色不是翻译框架，而是**精选**：根据当前步骤和方法类型，告诉 Worker 该读哪些文件。Worker 自己按框架要求执行。

#### 2.3 Master 的上下文管理

Master 的上下文是稀缺资源。核心原则：**重操作全部外包给 Worker，Master 只做轻量级判断。**

| 层级         | 内容                                                                     | 理由                                            |
| ------------ | ------------------------------------------------------------------------ | ----------------------------------------------- |
| **常驻**     | master-state.md（~250 行）、decision_log 最近 10 条、当前步骤 stage file | 这些是 Master 每次判断都需要的信息，~400 行总共 |
| **按需读**   | literature_notes.md 全文、feasibility_report.md、Worker log 全文         | 只在特定判断需要时读，不常驻                    |
| **永远不读** | 论文 content.md、搜索 JSON、训练日志、仿真器源码                         | 这些是 Worker 的领地，Master 碰了就是上下文浪费 |

关键约束：**Worker 的 stdout（返回给 Master 的文本）限制在 ≤50 行。** Worker log 可以写几百行完整记录，但 Master 只读 stdout 的结构化摘要。需要细节时，Master 再去读 worker-log 文件。

#### 2.4 Worker Log 的双重目的

Worker log 不只是执行记录，它是**框架改进的反馈通道**。

设计包含两个特殊章节：

- **框架反馈**：Worker 执行中发现的框架文件冲突、歧义、缺失指引
- **自评遗漏**：Worker 自己认为可能没做透的点

这两个章节的价值：

1. 多个项目的 Worker log 积累后，能发现框架文件之间哪些地方有歧义
2. Worker 的"自评遗漏"帮助 Master 判断是否需要补做
3. 长期来看，这些反馈是框架演进的素材

#### 2.5 Master 状态持久化（三层架构）

**问题**：Master 对话的上下文最终会满。满了之后怎么办？

**三层方案**：

```
Layer 1: master-state.md（始终最新）
  - 每步后更新：当前步骤、已完成步骤、最近决策
  - 新 Master 对话读此文件即可恢复
  - 这是最重要的文件——相当于 Master 的"大脑快照"

Layer 2: .sessions/ handoff（对话结束时写）
  - master-state.md 不包含的对话特有上下文：
    - 派遣历史（哪个 Worker 失败了、调了什么参数）
    - 用户偏好（观察到用户喜欢先看 X 再做 Y）
    - 失败分析（为什么 D015 的 Worker 重试了 2 次）
  - 辅助文件，帮新 Master 理解"上一个 Master 的思考过程"

Layer 3: 项目 memory 文件（~/.claude/.../memory/project_{name}.md）
  - 稳定的跨会话信息（如"用户是 PhD 学生"、"这个方向用 MARL"）
  - 低频更新，Claude 内建记忆系统
```

**上下文溢出流程**：

1. 尽量完成当前步骤（中断点不好）
2. 更新 master-state.md
3. 写 handoff（记录派遣历史和思考过程）
4. 提交
5. 告知用户："请开新对话，说 resume project {name}"

**新对话恢复**：

1. 读 master-state.md → 获得完整项目状态
2. 读最新 handoff → 获得上一个 Master 的思考
3. 读当前步骤 stage file → 获得执行规范
4. 继续执行

#### 2.6 decision_log 为什么由 Master 写

当前的痛点是 decision_log 风格不统一——每个对话/agent 写的格式、详细程度、措辞都不同。

改为 Master 统一写：

- Worker 只返回**事实和发现**（"搜索到 10 篇竞品"、"MVE 失败，GNN 差 5.8%"）
- Master 根据 Worker 的发现做**判断和记录**（"D015: MARL 方向可行，基于 10 篇竞品分析"）
- 风格一致，跨步骤可追溯

#### 2.7 提交策略：从细碎到关键节点

当前的问题是 commit 太碎（几乎每个文件改动都 commit）或者太粗（攒一堆最后一起 commit）。

Master 的提交策略：

- **Worker 完成一个步骤** → commit（该步骤所有产出）
- **Go/No-Go 决策确认后** → commit（决策 + 相关文档）
- **用户手动操作后** → commit（标记人工介入点）
- **对话即将结束** → commit（保护未提交改动）

不再为每个 Worker 派遣单独 commit——Worker 只是中间过程，结果才有价值。

### 3. 核心设计决策汇总

| 决策                  | 选择                           | 替代方案        | 选择原因                           |
| --------------------- | ------------------------------ | --------------- | ---------------------------------- |
| Worker 是否读框架文件 | **读**                         | Master 翻译     | 框架文件打磨充分，翻译丢失信息     |
| Worker log 位置       | `projects/{name}/worker-logs/` | `.sessions/` 下 | 随项目走，git 追踪，方便回看       |
| Worker 权限模式       | `bypassPermissions`            | 默认/dontAsk    | 研究任务已信任，不需逐步确认       |
| Worker task 文件      | ephemeral（.gitignore）        | 持久化          | 每次派遣前重写，旧的没价值         |
| decision_log 由谁写   | **Master**                     | Worker 自己写   | 风格一致，Worker 只返回事实        |
| Worker 是否写 handoff | **不写**                       | 跟现在一样写    | Master 维护所有状态，Worker 无状态 |
| 同时开几个 Worker     | **1 个**                       | 并行多个        | 简化状态管理，避免文件冲突         |
| Master 状态持久化     | 三层                           | 单层 handoff    | 不同信息有不同更新频率和重要性     |
| commit 粒度           | 按步骤                         | 按文件/按对话   | 步骤是逻辑单位，不过碎不过粗       |

### 4. 产出物清单

| 文件                                             | 说明                                  | 位置                 |
| ------------------------------------------------ | ------------------------------------- | -------------------- |
| `templates/master-state-template.md`             | Master prompt 模板（~250 行，9 章节） | 框架级，所有项目共用 |
| `projects/{name}/master-state.md`                | 项目实例（Master 每步后更新）         | 项目级，每个项目一个 |
| `projects/{name}/worker-logs/step-{N}-{slug}.md` | Worker 执行日志                       | 项目级，每个步骤一个 |
| `projects/{name}/worker-tasks/step-{N}-task.md`  | Worker 任务文件（ephemeral）          | 项目级，不提交       |

模板 9 个章节：

1. 角色定义（Master 做什么/不做什么）
2. 项目状态（当前位置、已完成步骤、关键决策、活跃文件）
3. 步骤调度表（9 个 GW 子步骤 × 4 列）
4. FR 防坑检查清单（FR-01~08，每条：检查内容 + 触发步骤 + 失败动作）
5. 决策权限表（Master 自主 vs 用户确认）
6. 提交检查点
7. 上下文管理规则（常驻 vs 按需 vs 不加载）
8. Worker 派遣协议（命令模板 + Task 文件格式 + Worker Log 格式 + 每步预算）
9. 失败恢复（Worker 失败/超时/上下文溢出）

### 5. 端到端测试

#### 5.1 测试设计

**测试项目**: leo-resilient-routing（已到 Step 4a Pivot，需要重新评估方向）
**测试步骤**: 定向检索 MARL 抗毁路由竞品（不是完整 GW 步骤，而是验证编排链路）
**测试目的**: 验证 Master 写 Task 文件 → Worker 读取执行 → Worker log 写入 → Master 接收判断 的完整链路

#### 5.2 Worker 派遣命令

```bash
claude -p \
  --append-system-prompt "你是无状态研究 Worker。先读任务文件 projects/leo-resilient-routing/worker-tasks/step-4a-revisit-task.md，然后执行。Worker log 增量写入 projects/leo-resilient-routing/worker-logs/step-4a-revisit-search.md。不修改 decision_log.md 和 master-state.md。" \
  --allowed-tools "Bash Read Glob Grep Write Edit Agent" \
  --max-budget-usd 1.5 \
  --effort high \
  --permission-mode bypassPermissions \
  "执行定向检索测试，项目 leo-resilient-routing。先读 projects/leo-resilient-routing/worker-tasks/step-4a-revisit-task.md"
```

#### 5.3 测试结果

**链路验证**: 全部通过

- ✅ Worker 读到了 Task 文件
- ✅ Worker 读到了框架文件（gw-feasibility.md, code-quality.md）
- ✅ Worker 执行了 3 组搜索（90+ 条结果）
- ✅ Worker log 完整写入 75 行（结构化，含质量门自评）
- ✅ Worker stdout 返回简短结论（4 行）
- ✅ Worker 未修改 decision_log.md 或 master-state.md
- ✅ 质量门 3/3 通过

**Worker 实际产出**:

- MARL + LEO 路由：已有 10+ 篇竞品（2024-2026），不再新颖
- MARL + 课程学习 + 抗毁路由：空白，无直接竞品
- 差异化建议：聚焦"课程学习 + 抗毁"双差异化点

#### 5.4 发现的问题

##### P1: Worker log "框架反馈"和"自评遗漏"章节未填写

- **现象**: Worker 写了执行过程和结论，但跳过了"框架反馈"和"自评遗漏"两个章节
- **原因**: Task 文件中没有显式要求这两个章节，Worker 不知道要写
- **影响**: 框架改进反馈通道没有生效
- **修复方向**: Task 文件模板中增加提醒："Worker log 必须包含'框架反馈'和'自评遗漏'章节，即使写'无'"
- **优先级**: 中，下个 Worker 派遣时验证

##### P2: Worker log "Master 摘要"与全文有重复

- **现象**: 75 行 log 中，总结部分和全文分析有信息重复
- **影响**: 不大，Master 主要读 summary，全文只在审计时看
- **暂不修复**: 等更多 Worker log 积累后再优化格式
- **优先级**: 低

##### P3: Worker stdout 和 worker-log 的关系不明确

- **现象**: Worker 的 stdout（claude -p 返回给 Master 的文本）和 worker-log 文件内容有重叠
- **当前行为**: stdout 是简短结论（4 行），worker-log 是完整记录（75 行）
- **判断**: 这是正确的行为。Master 读 stdout 做快速判断，需要细节时读 worker-log
- **优先级**: 不需修复，但应在模板中明确说明两者关系

### 6. 未测试场景

| 场景                         | 风险 | 说明                                            | 计划                     |
| ---------------------------- | ---- | ----------------------------------------------- | ------------------------ |
| Worker 超时/崩溃             | 中   | Task 文件设计了增量写入，崩溃时部分 log 应存在  | 下次测试给短超时         |
| Worker 质量门失败            | 中   | Master 需要读 Worker log 的自评部分决定是否重试 | 等实际跑 4a 步骤时观察   |
| Master 上下文溢出恢复        | 高   | 核心流程：master-state.md + handoff + commit    | 需要跑 3+ 步骤后测试     |
| Worker 内开子 agent 精读论文 | 中   | `claude -p` 支持子 agent，但精读场景未测试      | Step 3 时测试            |
| 长步骤（Step 7 implement）   | 高   | 代码生成+验证，5 USD 预算可能不够               | 实际跑 Step 7 时验证     |
| 完整 GW 流程串行跑通         | 高   | 9 个步骤 × N 个 Worker 的完整链路               | 用 beam-hopping 从头测试 |
| Worker 多次重试              | 中   | 最多 2 次，然后报告用户                         | 等遇到失败时测试         |
| Worker 输出太大              | 中   | stdout ≤50 行约束是否真的生效                   | 观察                     |

### 7. CLI Flags 可用性确认

测试过程中确认 `claude -p` 以下 flags 全部可用：

| Flag                                  | 用途                                                    | 状态      |
| ------------------------------------- | ------------------------------------------------------- | --------- |
| `--append-system-prompt`              | 注入 Worker 身份和规则（不覆盖默认 system prompt）      | ✅        |
| `--allowed-tools`                     | 限制 Worker 可用工具（如 "Bash Read Write Edit Agent"） | ✅        |
| `--max-budget-usd`                    | 控制单次 Worker 成本上限                                | ✅        |
| `--effort high`                       | 提高执行质量                                            | ✅        |
| `--permission-mode bypassPermissions` | Worker 自动执行不需确认                                 | ✅        |
| `claude -p` 基础非交互模式            | Worker 运行方式                                         | ✅ 不限流 |
| `claude -p` 内开子 agent              | Worker 精读论文、跑实验                                 | ✅        |

其他可用但未测试的 flags：

- `--output-format json` — 可能让 Master 更容易解析 Worker 输出
- `--max-turns` — 限制 Worker 对话轮数，防止跑飞

### 8. 与现有框架的关系

Master-Worker 不是替代现有框架，而是在框架之上加一层执行自动化：

| 现有机制                 | Master-Worker 中的角色        | 变化                                                       |
| ------------------------ | ----------------------------- | ---------------------------------------------------------- |
| 框架文件（stages/\*.md） | Worker 读的执行规范           | 不变，只是执行者从"用户开的对话"变成"Master 派遣的 Worker" |
| FR-01~08 检查清单        | 嵌入 master-state.md §4       | 从"用户记住并提醒"变成"Master 自动检查"                    |
| handoff 机制             | Master 上下文溢出时的恢复手段 | 从主要状态传递手段降级为辅助                               |
| decision_log.md          | Master 统一写入               | 从"谁都可以写"变成"只有 Master 写"                         |
| 文件路径规则             | Worker 遵守（框架层面不变）   | 不变                                                       |
| 子 agent 强制委托        | Worker 内部使用               | 从"主对话派子 agent"变成"Worker 派子 agent"                |

**未覆盖的部分**：

- 当前模板只覆盖 GW 阶段。Contract 和 Execute 阶段的步骤调度表需要后续补充。
- `--allowed-tools` 中列了 `Agent`（允许 Worker 开子 agent），但未测试 Worker→子 agent→子 agent 的三层嵌套。

### 9. 成本估算

基于测试数据的粗估：

| 步骤               | 预算    | 预估实际消耗 | 估算依据                      |
| ------------------ | ------- | ------------ | ----------------------------- |
| 1 search           | 1.0 USD | ~0.3-0.5     | 测试中 3 组搜索 + 汇总约 0.3  |
| 2 acquire          | 1.5 USD | ~0.5-1.0     | 下载+转换，主要看论文数量     |
| 3 read             | 3.0 USD | ~1.5-2.5     | 精读 5-8 篇，每篇需要子 agent |
| 3.5 supplement     | 2.0 USD | ~0.5-1.0     | 定向检索+更新                 |
| 4a feasibility     | 3.0 USD | ~1.0-2.5     | 分析为主，可能含 MVE          |
| 5 validate         | 1.5 USD | ~0.5-1.0     | 交叉验证                      |
| 4b sim-feasibility | 2.0 USD | ~0.5-1.0     | 评估为主                      |
| 6 sim-design       | 2.0 USD | ~0.5-1.5     | 设计+参数溯源                 |
| 7 implement        | 5.0 USD | ~2.0-4.0     | 代码生成+验证，最重           |

**GW 全流程估算**: ~8-15 USD（~60-120 RMB）。对比手动操作节省的时间，性价比高。

### 10. 下一步

1. **实战测试**: 用 beam-hopping 项目从 Step 1 开始跑完整 GW 流程，验证 9 个步骤的完整链路
2. **修复 P1**: Task 文件模板增加"框架反馈"和"自评遗漏"的显式要求
3. **模板调优**: 根据实战积累的 worker-log 优化 Task 文件和 Log 格式
4. **Master 指令优化**: 如果发现 Master 经常遗漏某些检查，强化 master-state.md 中的检查清单
5. **Contract/Execute 扩展**: 当前模板只覆盖 GW，后续补充 Contract 和 Execute 的步骤调度表
