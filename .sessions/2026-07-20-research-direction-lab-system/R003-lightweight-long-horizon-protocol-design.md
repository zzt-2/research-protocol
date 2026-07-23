# [R003] 轻量长程运行协议候选设计与场景演练

> 2026-07-23 | 关联：2026-07-20-research-direction-lab-system / S014 / D016

## 调研问题

在不重写现有 Research Direction Lab、不建立强 controller、也不依赖对话记忆的前提下，怎样让长期主控在压缩、换对话、候选失败、方向轮换和正式晋级过程中稳定保持当前 mission，并让用户只承担极短中转？

## 发现

### 1. 根因不是恢复说明不足，而是跨 owner 缺少前台绑定

现有 owner 大多已经各自写对：

- `research-direction-lab` 已定义上下文丢失后 Recover、Probe/Scout/Deep Evidence、information gain、candidate rotation、blocked ≠ failed 和战略升级；
- `session-governance` 已定义 topic-index、H/T、voice/profile 和 handoff 验证；
- Direction Lab `state/current.yaml` 正确记录 science-scout dormant；
- formal `master-state.md` 正确记录 Pilot-Jones 状态；
- system 专题 `topic-index.md` 正确记录当前应先设计运行协议。

本次 S014 故障发生在“多个真实状态之间”：压缩摘要突出 Pilot-Jones，主控便把 formal candidate 误推成当前 next action，越过 system-design gate。

因此真正缺口是：

1. 当前主控/fork 的 role、mission 和 active lane 由谁绑定；
2. 未完成 decision gate 怎样约束下一任务；
3. 摘要推断怎样不得改变 lane；
4. 怎样保持 AI 科学判断，而不把方向选择写成状态机。

### 2. 必要能力

| 能力 | 必须回答的问题 |
|---|---|
| 前台 lane | 当前是设计、探索、formal、执行还是审计；谁拥有下一动作？ |
| 权威分层 | 哪些是磁盘事实，哪些只是摘要或主控推断？ |
| 决策门 | 当前尚未拍板什么；因此禁止哪些动作类型？ |
| 科学信息验收 | 本包会改变哪个候选排序、机制、baseline 或论文 disposition？ |
| disposition | FAIL/BLOCKED/SATURATED/DIAGNOSTIC/晋级分别怎样处理？ |
| topic 生命周期 | 候选轮换、mission 结束和 formal 晋级何时需要新 topic？ |
| 单包闭环 | 一个 GLM 对话能连续做什么，在哪个门停止？ |
| 恢复交接 | 压缩、换主控和 fork 后最少读取什么？ |
| 纵向验收 | 怎样证明稳、快、产出可用，而不是单轮合规？ |

### 3. 非目标

- 不建立自动选研究方向的 controller；
- 不用固定候选数、固定批次数或 work conservation 证明有效；
- 不为每个异常新增一条规则；
- 不为每个候选或 Probe 新建 topic；
- 不要求恢复时重读全部历史；
- 不把文件齐全、receipt/verifier PASS 当科学信息；
- 不在设计阶段预选真实科学方向；
- 不复制既有 Skill/current/master-state 已拥有的事实和规则。

### 4. owner 边界

- 候选 Map、比较、disposition、rotate/deepen：`research-direction-lab`；
- topic 生命周期、主控换对话、H/T/voice：`session-governance`；
- 探索证据和 candidate current：项目 Direction Lab projections；
- formal 阶段授权：项目 `master-state.md`；
- 执行合同与细节：T + worker-log + artifact + commit；
- 尚缺的接口：当前主控/fork 的“前台 lane + 未决 gate + 允许动作类型”怎样绑定这些 owner。

### 5. 四种候选架构

| 候选 | 做法 | 优点 | 风险 | 判断 |
|---|---|---|---|---|
| A. Skill/checklist-only | 再强调 Recover、读日志、不得跳 gate | 无新文件 | 本次已证明可被忽略 | 不足 |
| B. topic 前台控制块 | topic-index 顶部维护很小的 role/lane/gate/allowed/forbidden/next-action | 复用 current snapshot；热路径短；不复制科学事实 | 同 topic 同时做设计和 live fork 会冲突 | 当前首选；live test 独立 mission topic |
| C. per-fork manifest | 每个长期 fork 一张 run card | 并行角色最清晰 | 新状态源和同步成本 | v1 单 fork 不需要 |
| D. 强 controller | 代码控制转移和下一动作 | 约束最强 | 固化科学判断，最重 | 排除 |

候选 B 的控制块只回答动作控制问题，不保存 candidate 数字、证据或 formal step 内容；这些继续通过 authority pointer 读取原 owner。

### 6. 第一轮历史场景演练

#### 压缩后误选 Pilot-Jones

若控制块为 `role=SYSTEM_DESIGN`、`gate=协议未定`、`allowed=分析/演练`、`forbidden=科学派工/Skill 修改`，Pilot-Jones 只能是只读 formal 事实，不能成为当前任务。

#### N1 的 MB 化身 FAIL，但 PCS 家族未关闭

candidate disposition 在 portfolio 标 `FAILED`；同一 exploration mission 内换机制，不新开 topic。固定状态机容易把 candidate FAIL 误升为 family FAIL。

#### F1/F4 blocked

blocked 不等于失败。有其他 READY 就轮换；只有剩余动作需要重大基础设施投资时才进入用户战略 gate，不为 blocker 单开 topic。

#### 4b#1 mission Kill 后原 topic 被用于广泛重定向

topic 应代表 mission/lifecycle，而不是候选杂物箱。formal mission Kill 后只收口、harvest、H 返回既有 exploration topic，不在原 topic 内扩成方向探索。

#### 秒级 Probe 膨胀

一个执行包围绕一个会改变决策的不确定性，允许同一 GLM 对话内完成必要 smoke、bounded repair 和最小验证；stop 条件满足即结束。普通包只产 T、worker-log、可选 artifact 和 commit。

#### 弱正信号失效

semantic/comparator gate 早于扩算力；integrity PASS 不能晋级。控制块只决定当前允许轮换还是 reconcile，不保存科学结论。

### 7. 第二轮组合场景演练

#### live fork 再次压缩

H 在 fork 启动时绑定唯一 live-test topic；压缩后只从顶部控制块恢复 lane。若控制块与 authority pointer 冲突，只允许 `RECONCILE`。

AI 完全不读控制块仍是剩余风险。因此未来 T 应携带 `control_ref + control_epoch + action_class`。v1 先不建 controller；若真实运行再次越门，再增加只验证这三项的确定性 guard。

#### 所有 READY 候选耗尽

先在原 exploration mission 内 Map/refresh。仍只剩高成本投资或 formal 目标变化时进入战略 gate。没有 ready work 不自动产生新 mission。

#### 弱正信号晋级

Probe PASS 只允许考虑 Scout；稳定 Scout 信号经 promotion review 后，才新建/恢复 formal topic。exploration topic 保留 lineage，不与 formal 验证混成一个 topic。

#### formal candidate 失败

formal topic 记录 FAIL、harvest 后 dormant/closed，并 H 返回既有 exploration mission；不得原地转成广泛重定向。

#### 用户不看中间技术结果

用户只转发 T 路径和四项完成索引。master 自行读取 worker-log/artifact/commit；只有目标、贡献线、重大投资或合法工作耗尽才请求用户。

#### 控制块变重或过期

控制块 replace-in-place，不追加历史；只存动作控制；只在 lane/gate/next-action 改变时更新；建议不超过约 12 行/9 字段。详细原因进 S，执行进 worker-log，科学事实进 project current。

组合演练未发现单 fork 场景必须采用 per-fork manifest 或强 controller。

## 结论

### 1. 轻量运行协议 v0.1

#### 顶部控制块

长期主控 mission 的 topic-index 顶部只维护：

`control_epoch | role | mission | active_lane | authority_pointer | decision_gate | allowed_actions | forbidden_actions | next_legal_action`

- `role`：design / live-test / exploration / formal / audit；
- `mission`：topic 冻结目标短句；
- `authority_pointer`：只指向科学/formal owner；
- allowed/forbidden：动作类型，不写算法名；
- `next_action`：唯一下一动作；
- epoch：仅当控制语义改变时递增。

#### 主控循环

1. Recover control；冲突只 reconcile。
2. 选择最能改变判断的科学不确定性，并解释为什么不是其他项。
3. T 引用 control epoch，冻结 question、decision delta、comparator、stop、预算和产出。
4. GLM 在一个对话内完成必要动作，直到关闭问题或触发 stop。
5. master 只接索引，主动审 worker-log/artifact/commit；分开判 integrity 与科学信息。
6. 先更新 scientific owner，再更新控制块。
7. 在 allowed actions 内继续/轮换/转阶段；mission 或重大投资变化才问用户。

### 2. disposition 语义

| 结果 | 含义 | 默认处理 |
|---|---|---|
| FAILED | 合法证据否决假设 | harvest 后换候选/机制 |
| BLOCKED | 缺接口、信息、评估器或材料 | 有 READY 就轮换；高杠杆基建再审 |
| SATURATED | 同合同不再改变判断 | 禁止 governance-only repeat，换机制或 Map |
| DIAGNOSTIC | comparator/语义/信息边界未闭合 | 做最便宜修复 Probe，不晋级 |
| SCOUT_READY | Probe 前置通过且比较有信息 | 进入小型 mechanism-distinct Scout |
| PROMOTION_CANDIDATE | 稳定信号有论文价值 | promotion review 后 formal topic |
| HARVESTED | 有耐久负面、边界、资产或方法论材料 | 记录去向，不等于主方向成功 |

这些是 AI 解释证据时使用的 disposition，不是自动状态机。

### 3. topic 生命周期

- topic 代表 mission，不代表临时候选；
- exploration 内候选失败、blocked、轮换、refresh：同一 topic；
- 候选正式晋级独立论文路线：新建/恢复 formal topic；
- formal mission 失败：收口并返回 existing exploration topic；
- 原始目标、owner 或产物生命周期实质变化：scope decision 后新 topic；
- 换主控/压缩：H；派执行：T；都不自动新建 topic；
- system design 与一次 longitudinal live test 是两个 mission，因此设计认可后只新建一个 test topic，不是每包一个。

### 4. v1 纵向验收

不以固定批次数单独判定，至少真实经历：

1. fork/新主控恢复；
2. 上下文压缩或等价恢复；
3. candidate FAIL/BLOCKED/SATURATED 后轮换；
4. 正信号晋级或明确不晋级；
5. 普通包未生成 S/D/V/H 全套；
6. 原 design 对话只凭文件还原目标、dead ends、gate 和下一步。

审计关注：

- lane/authorization 越界和用户纠偏次数；
- 每包是否改变科学判断或诚实记录 no-new-information；
- governance-only repeat；
- ordinary package 的治理/科学动作比例；
- 恢复时间和读取文件数；
- candidate ranking、mechanism、formal promotion 或 thesis disposition 是否改变；
- 是否产生可用方法候选；没有时是否能说明耗尽层级。

## 对决策的影响

v0.1 已通过两轮历史场景桌面演练，当前领先于 checklist-only、per-fork manifest 和强 controller，但仍是设计草案，不新建 D###、不修改 Skill、不创建 live-test topic。

实施前仍需确认：

1. 控制块只用于 RDL mission，还是进入通用 topic-index 模板；
2. control epoch v1 是否配极小 T guard；
3. live-test 和执行 GLM 的 worktree 串行/隔离方式；
4. promotion review 如何只复用现有 Probe/Scout/Groundwork；
5. 真实 event coverage 怎样形成，而不为测试流程伪造科学事件。

### 风险处置建议

1. **仅用于 RDL/长期自动研究 mission**：不修改所有 topic-index 的通用模板。普通短专题继续使用现有 session-governance；只有需要跨多个工作包自动轮换的 topic 才有顶部控制块。
2. **v1 即配极小 T guard**：S014 已提供一次真实越 gate 证据，满足“观察到具体失败后再加 guard”的条件。guard 只验证 `control_ref` 存在、`control_epoch` 一致、`action_class` 在 allowed 且不在 forbidden；不读算法语义、不选候选、不实现 scheduler。
3. **一个独立 live-test worktree**：设计 worktree 在提交后冻结为审查基线；live-test 从该提交建立一个分支/worktree。fork 主控与 GLM executor 在 live-test worktree 上串行操作，master 写 T 后停止写入，executor 完成并提交后 master 再审查；不为每包新建 worktree。
4. **不新增 promotion review 流程**：`PROMOTION_CANDIDATE` 只触发一次 promotion handoff，核对现有证据有效性、M-C-A 问题和 formal 入口；随后完全交给既有 Groundwork/Contract/Execute。Direction Lab 不复制 formal gate。
5. **event coverage 允许 PARTIAL**：不伪造失败或正信号来测流程。真实运行到用户认为“跑了一段时间”后回到 design 对话审计已覆盖事件；未自然发生的场景标未验证，结合 R003 历史演练，不用固定批次数制造形式 PASS。

据此，当前推荐形态为：

> **一个 RDL mission topic 的九字段顶部控制块 + 一个极小 T 授权 guard + 现有 H/T/worker-log/raw artifacts + 一个隔离 live-test worktree。**

它新增的是一个跨 owner 的动作绑定接口，不新增科学 current、不新增方向 scheduler、不改变 formal framework。
