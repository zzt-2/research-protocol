# Topic Index: Research Direction Lab 长程真实运行测试

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v1
  control_epoch: 8
  role: LIVE_TEST
  mission: 在真实研究反馈中验证轻量长程运行协议能否稳定推进并积累可用方法材料
  active_lane: HIGH_ORDER_CPR_COMBINATION_METHOD
  authority_pointer: .sessions/2026-07-06-step4a-mve-execution/decisions.md#D012
  decision_gate: 在 uniform 16-QAM 星地 GG+CFO/linewidth 条件下先判断 strongest-simple CPR 到 truth-assisted reference 是否有合法 headroom；若存活，同包判断 B10/B12 组合方法能否同时胜过传统 baseline 与两个 standalone component
  allowed_actions:
    - HIGH_ORDER_CPR_COMBINATION_METHOD_PACKAGE
    - TASK_BRIEF_PREPARATION
  forbidden_actions:
    - PRIVATE_FULLTEXT_ACQUISITION
    - ABSTRACT_AS_FULLTEXT
    - POST_STEP4A_ADVANCE
    - SCIENCE_SCOUT_REACTIVATION
    - PROTECTED_HISTORY_EDIT
    - SKILL_EDIT
    - GENERAL_INFRASTRUCTURE_BUILD
    - PILOT_JONES_REPAIR_OR_NEW_AXIS
  next_legal_action: 执行 T006；先做 B10/B12 source closure、合法 baseline 与 0.5 dB headroom gate，门通过则同一 GLM 对话完成 cascade/confidence-gate/adaptive-forgetting 三个方法与 paired test
```
<!-- RDL-CONTROL:END -->

> 状态: active（T006_READY；D012 已授权）
> 创建: 2026-07-23 | 最后更新: 2026-07-25

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
- T005 已完成并由 D066/V040 接收 scoped Kill；Pilot-Jones 退出当前 carrier。
- 当前仅授权 T006 高阶调制 CPR 组合方法包：恢复 B10/B12 既有 Step 1–3 证据，
  在 GW Step 4a 先验算合法 headroom，门过则同包实现并比较三个务实方法。

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
- **[2026-07-23] [D063]**：T002 只支持 unitary-real-rotation 局部 Kill；允许在 Step 4a 内检验 complex Jones/PMD/PDL 的唯一物理救活轴。
  - 原因：V036 critic 指出 canonical generator 未包含可能产生真实 conditioning/memory 的 PMD/PDL；V037 又发现原 FR-21 阈值映射无依据。
  - 新范围：物理模型充分性、隔离模型、传统任务适配 baseline、oracle/headroom 和条件式方法比较；不改 shared generator、不进 Step 5。
  - 影响的未决项：decision gate 从“当前 unitary 实例化是否有方法”转为“物理充分模型是否救活 family”。
- **[2026-07-23] [D064]**：T003 provisional verdict 被主控 V038 否决；授权同一 Step 4a 内的 semantic repair + retest。
  - 原因：PDL/PMD 作用于含噪 RX 导致可逆恒等、PMD pilot 未经过 FIR、B3 tapped 为 RX→RX 自预测、PMD oracle 被 B1 反超、problem gate 与 P1 success 混合。
  - 新范围：保留 T003 为失败证据，新建隔离 T004 修复闭包；只有可失败语义测试全过才运行 headroom/MVE。
  - 影响的未决项：complex-Jones/PMD/PDL 不再是 provisional Pivot，而是 `UNRESOLVED / SEMANTIC_REPAIR_AUTHORIZED`。
- **[2026-07-24] [D065]**：T004 正面 problem gate 被 V039 否决；授权同一
  Step 4a 内的 temporal-semantics + reproducibility 终审。
  - 原因：T004 每 64 symbols iid 重抽器件 PDL/PMD basis；固定器件反事实使
    impairment-added headroom 降至 0.0146/0.00445 dB。另有 Python hash、
    contract N/seed 数和假 SHA 闭包缺陷。
  - 新范围：只闭合 fixed/有来源慢变 component、deterministic closure 和正式
    headroom；不再搜索方法。
  - 影响的未决项：从“哪种方法关闭 0.77 dB”改为“该 0.77 dB 是否由错误时间模型
    制造”；若 fixed primary <0.5 dB，则关闭 complex component rescue axis。
- **[2026-07-25] [D066/D012]**：T005 关闭 verified fixed complex component rescue
  axis，前台 carrier 转到 B10/B12 高阶调制 CPR 组合方法。
  - 原因：8/8 primary cells 最大 point/CI upper 仅 0.0804/0.2372 dB；exact-inverse
    adjudication 证明该 Kill 不依赖原 MMSE regularization。
  - 新范围：在已有 B10/B12 Step 1–3 证据上执行 Step 4a headroom→method 大包；
    不继续修 Pilot-Jones，不恢复 Scout/P03。
  - 影响的未决项：从“Pilot-Jones 是否有余量”转为“高阶 CPR 是否有合法余量并能
    形成同时胜过 standalone components 的组合方法”。

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
- **S001 续接 / T002验收/D063/T003**：T002 工程与 raw 可信，但 V037 修正 contract stale count 和无依据的 BER-ratio→dB 门；只 Kill unitary-real-rotation M-C-A。用户要求“多做点”，授权同包检验 complex-Jones/PMD/PDL rescue。
- **S001 续接 / T003验收/D064/T004**：fresh 13 tests 通过但 V038 找到 5 项科学语义缺陷；T003 negative verdict 不接收。真实暴露“consistency/provenance PASS 被误作物理正确”的长程事件，epoch 6 授权语义修复重测大包。
- **S001 续接 / T004验收/D065/T005**：fresh 25 tests 通过，但 V039 发现
  component 每 25.6 ns iid redraw 的无来源时间语义；固定器件反事实把正面
  headroom 降到近零，同时暴露跨进程 hash 与契约闭包缺陷。T004 工程 PARTIAL
  可复用、科学 verdict FAIL；epoch 7 授权终局 temporal adjudication，不再堆方法。
- **S001 续接 / T005验收/D066/D012/T006**：raw 240 行与 8 cells 独立重算支持
  scoped axis Kill；主控另发现 M3 contract/implementation 与 Windows encoding 两项
  integrity 缺口，并用真 exact inverse 证明 verdict 不变。epoch 8 合法换到已有
  B10/B12 Step 1–3 证据，授权一个 headroom 过门即直接做三方法的 T006 大包。

## 未决项

- T006 能否在合法高阶 CPR 场景中先找到 `>=0.5 dB` headroom，再形成相对最强
  standalone component `>=0.3 dB` 的组合方法；
- live run 自然覆盖哪些恢复/轮换/晋级事件；
- 何时由原 design 对话进行阶段性审计。

## 当前位置

T006_READY。D066/V040 已接收 Pilot-Jones fixed complex component rescue axis 的
scoped Kill并停止继续投资；D012 激活 B10/B12 高阶调制 CPR 组合方法。下一包先做
source/baseline/headroom 闭包，门通过则在同一对话直接完成三个方法与 paired test；
仍不得越过 Step 4a。
