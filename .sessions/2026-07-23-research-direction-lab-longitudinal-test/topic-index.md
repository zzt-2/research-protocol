# Topic Index: Research Direction Lab 长程真实运行测试

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v1
  control_epoch: 2
  role: LIVE_TEST
  mission: 在真实研究反馈中验证轻量长程运行协议能否稳定推进并积累可用方法材料
  active_lane: STATE_RECONCILIATION
  authority_pointer: .sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md#D061
  decision_gate: mutable current views 仍混有 D061 前 routing 与已纠正的 Step 3.5 事实，科学派工前必须先收敛
  allowed_actions:
    - STATE_RECONCILIATION
    - TASK_BRIEF_PREPARATION
  forbidden_actions:
    - SCIENTIFIC_EXPERIMENT
    - FORMAL_STAGE_CHANGE
    - SKILL_EDIT
    - INFRASTRUCTURE_BUILD
  next_legal_action: 执行 T001，只对齐 D061/H017 到可变 current views 并返回 worker-log，不运行科学工作
```
<!-- RDL-CONTROL:END -->

> 状态: active（T001_READY；仅授权 current-view reconciliation）
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

### 明确不含

- 当前不授权任何仿真、Probe、Scout、MVE、文献全文工作或基础设施建设；
- 不改变 Pilot-Jones、science-scout 或其他 formal/scientific 状态；
- 不修改 RDL Skill、session-governance 或 controller；
- 不创建 per-fork manifest、自动 scheduler 或每包一个 topic；
- 不把流程 PASS 当作方法或论文结果；
- 不让用户读取技术日志或判断科学正确性。

### 范围变更记录

- 2026-07-23，system D017：建立 live-test mission，初始只授权 Recover/Map/Reconcile/T 准备。任何科学 action class 必须由后续 control epoch 明确授权，并引用原 scientific/formal owner。

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

## 未决项

- T001 能否把可变 current views 收敛到 D061/H017，且不改科学结论与 protected history；
- current owner 收敛后，第二包应处理全文获取战略 gate，还是存在无需用户私有访问的更高信息量合法工作；
- live run 自然覆盖哪些恢复/轮换/晋级事件；
- 何时由原 design 对话进行阶段性审计。

## 当前位置

T001_READY。唯一合法下一步是执行 `T001-current-owner-reconciliation.md`，将 D061/H017 已确认事实同步到可变 current views。T001 完成并由主控验收前，不得运行科学实验、全文工作或改变 formal 状态。
