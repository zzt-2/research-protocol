# Topic Index: Research Direction Lab 长程真实运行测试

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v1
  control_epoch: 4
  role: LIVE_TEST
  mission: 在真实研究反馈中验证轻量长程运行协议能否稳定推进并积累可用方法材料
  active_lane: PILOT_JONES_STEP4A_BIG_PACKAGE
  authority_pointer: .sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md#D062
  decision_gate: 关闭 Pilot-Jones 是否存在结构性方法增量并值得继续这一科学不确定性
  allowed_actions:
    - PILOT_JONES_STEP4A_PACKAGE
    - TASK_BRIEF_PREPARATION
  forbidden_actions:
    - PRIVATE_FULLTEXT_ACQUISITION
    - ABSTRACT_AS_FULLTEXT
    - POST_STEP4A_ADVANCE
    - SCIENCE_SCOUT_REACTIVATION
    - PROTECTED_HISTORY_EDIT
    - SKILL_EDIT
    - GENERAL_INFRASTRUCTURE_BUILD
  next_legal_action: 执行 T002，在一个 GLM 对话内完成 Pilot-Jones Step 4a A0/A-prime/A/B/D、bounded source recovery、条件式 MVE 和 provisional verdict
```
<!-- RDL-CONTROL:END -->

> 状态: active（T002_READY；D062 已授权）
> 创建: 2026-07-23 | 最后更新: 2026-07-23

## 专题信息

- **slug**: `2026-07-23-research-direction-lab-longitudinal-test`
- **title**: Research Direction Lab 长程真实运行测试
- **性质**: 用真实研究反馈验证 D017 轻量协议；不是新的科学方向专题

## 范围边界

### 原始目标（冻结）

在用户只中转 T 路径和四项完成索引的协作方式下，让 fork 主控跨多个真实工作包稳定保持目标、在局部失败后合法换路、控制治理成本，并提高形成可用论文方法与材料的概率；运行一段时间后由原 system design 对话根据磁盘证据审计。

### 当前范围

- 从权威 current/formal owner 恢复现状，不从压缩摘要选择方向；
- 比较合法 carrier 和第一个会改变科学判断的 decision package；
- 使用顶部控制块、受 guard 约束的 T、worker-log、raw artifacts 和 commit；
- 在 control block 允许范围内串行推进，遇到 gate 更新控制块或交用户战略裁决；
- 记录真实恢复、失败/阻断、轮换、晋级/不晋级和工作包重量。
- 当前仅授权 Pilot-Jones Step 4a 单对话大包：A0/A′/A/B/D、方法形成、bounded source recovery、前置上界、条件式 MVE、双审查和 provisional verdict。

### 明确不含

- 不获取私有全文，不把摘要冒充全文；4 篇债务继续保留；
- 不进入 Step 5、Contract 或 Execute，不恢复 P03/science-scout；
- 不修改 RDL Skill、session-governance 或 controller；
- 不建设通用基础设施、per-fork manifest、自动 scheduler 或每包一个 topic；
- 不把流程 PASS 当作方法或论文结果；
- 不让用户读取技术日志或判断科学正确性。

### 范围变更记录

- 2026-07-23，system D017：建立 live-test mission，初始只授权 Recover/Map/Reconcile/T 准备。任何科学 action class 必须由后续 control epoch 明确授权，并引用原 scientific/formal owner。
- 2026-07-23，formal D062：用户选择 D056 带债豁免，允许 Pilot-Jones Step 4a 大包；4 篇全文债务不消失，正面最高 Conditional Go，止于 provisional verdict。

## 已确认结论

### 不变量

- 顶部控制块只拥有前台动作绑定，不拥有科学事实。
- conversation summary 只能定位文件，不能改变 active lane。
- 每个执行包关闭一个科学决策不确定性，但可包含多个有界动作。
- candidate 轮换留在 exploration mission；formal 晋级才新建/恢复 formal topic。
- 普通包只使用 T、worker-log、可选 artifact 和 commit。
- master 与 executor 在同一 live-test worktree 串行操作，不同时写。
- 用户只中转 T 路径和四项完成索引。

### 其他结论

- 本 live test 只验证真实发生的事件；未自然出现的事件标 `UNVERIFIED`，不伪造。
- 设计基线保留在 system topic 和 design worktree，供后续只读审计。

## 进展线索

- **S001**：live-test mission 激活边界、运行角色和初始 gate。
- **H001**：fork 主控启动入口；先恢复和比较 carrier，不运行科学工作。
- **S001 续接 / T001**：H001 接收 3/3 PASS；确认 formal owner=D061、Scout dormant，并发现 5 个可变 current views 残留 D061 前 routing。首包选择状态协调，不授权科学工作。
- **S001 续接 / T001 验收**：提交 `4a0d4a4` 的路径边界、protected diff、YAML 和字段级语义均 PASS；current owner 已收敛。下一门是需要用户权限/豁免的 4 篇全文获取战略 gate，当前不存在非重复且合法的 T002。
- **S001 续接 / D062/T002**：用户纠正 T001 只做状态协调、科学吞吐过低；T001 降为 bootstrap overhead。用户授权带债进入 Step 4a，下一包必须一次关闭科学决策，前置门通过时同包直接做 MVE。

## 未决项

- T002 对 Pilot-Jones 给出的 provisional verdict 及其完整证据；
- live run 自然覆盖哪些恢复/轮换/晋级事件；
- 何时由原 design 对话进行阶段性审计。

## 当前位置

T002_READY。D062 已记录带债豁免，formal/current owners 已更新为 Step 4a AUTHORIZED_IN_PROGRESS；T002 control guard 已 PASS。下一合法动作是执行一个 `PILOT_JONES_STEP4A_PACKAGE`；不得拆回纯文档小包，也不得越过 Step 4a。
