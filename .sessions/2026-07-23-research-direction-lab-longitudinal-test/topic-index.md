# Topic Index: Research Direction Lab 长程真实运行测试

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v2
  control_epoch: 17
  role: LIVE_TEST
  mission: 在真实研究反馈中验证轻量长程运行协议能否稳定推进并积累可用方法材料
  active_lane: B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR
  authority_pointer: .sessions/2026-07-06-step4a-mve-execution/decisions.md#D017
  decision_gate: B10 仅在 128 contiguous pilot 到 DD 的 source-native identity 成立后，才可接受 innovation-gated/adaptive-forgetting 方法比较
  allowed_actions:
    - RECOVER
    - TASK_PREPARATION
    - METHOD_CONSTRUCT
  forbidden_actions:
    - UNRELATED_SCIENTIFIC_EXPERIMENT
    - PRIVATE_FULLTEXT_ACQUISITION
    - ABSTRACT_AS_FULLTEXT
    - POST_STEP4A_ADVANCE
    - SCIENCE_SCOUT_REACTIVATION
    - PROTECTED_HISTORY_EDIT
    - SKILL_EDIT
    - GENERAL_INFRASTRUCTURE_BUILD
    - PILOT_JONES_REPAIR_OR_NEW_AXIS
    - HIGH_ORDER_CPR_COMBINATION_REPAIR
    - B1_OR_T008_REPAIR
    - UNAUTHORIZED_SCIENTIFIC_EXPERIMENT
  mission_log_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/mission-log.md
  mission_checkpoint: CP009
  next_legal_action: 独立审查 T010；通过后由线程内 executor 执行 source-native B10 identity 与同包 P1-P3 fair comparison
```
<!-- RDL-CONTROL:END -->

> 状态: active（B10 SOURCE-NATIVE METHOD PACKAGE READY FOR INDEPENDENT REVIEW）
> 创建: 2026-07-23 | 最后更新: 2026-07-26

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
- T006 工程资产保留，但科学 verdict 因 source identity/channel/statistics 多重缺口
  被拒收；B10/B12 family 为 UNRESOLVED，不继续当前修复。
- T008 的 17 项工程测试通过，但 Kill 因 required-SNR、oracle candidate 与
  evaluator working-region 身份失败被拒收；B1 只保留为未决 family。
- R001 已完成 campaign remap：比较 A4、B10/B12、B1 三条具有 formal 证据链的
  carrier，并逐项排除 B2/B3/B7/C15/B9/Pilot-Jones/P03/Scout 的 readiness。
- T009 已执行并经独立 verifier/主控接收为
  `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`；method delta 为 `NONE`。
- A4 已由 formal D016 返回候选池，不作 family Kill，也不开第二个 A4 repair 包。
- R002 已比较 B10、C15、B1、B9；只有 B10 具有现存 Step 1–3、可获取全文和
  不依赖第三 repair/新基础设施的直接激活路径。
- formal D017 已激活 `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`；epoch 17 只授权
  T010 的 source-native identity 与同包 P1–P3 method construct。独立 verifier
  通过前不执行。
- D004 已把运行方式改为本对话端到端推进；用户不再中转 GLM，项目强制的
  executor/verifier 分离改由本线程内部子 agent 完成。

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
- **[2026-07-25] [V001/D013]**：T006 科学 verdict 被主控拒收，carrier 转 B1。
  - 原因：B10 未实现 128-pilot training→DD，B12 关键公式自行重构，pilot/data
    channel 不同；唯一 headroom survivor 91.7% 来自单个 collapse seed。
  - 新范围：不修 T006，不 Kill B10/B12 family；只做 B1 adaptive phase-window
    Step 4a 大包，先结构门后方法。
  - 影响的未决项：从“B10/B12 组合是否失败”改为“固定相位窗是否存在可实现的
    condition-dependent 改进空间”。
- **[2026-07-26] [system D018]**：phase 1 冻结在 `aab425d`，停止派 T008，
  进入只读审计后的 v2 协议修订。
  - 原因：运行未严重跨 lane，但 mission 成功从“积累方法材料”漂移为问题存活、
    修复闭包和 scoped Kill；普通包治理过重，executor/owner 边界也未闭合。
  - 新范围：只修改 RDL Skill、最小 task guard、三层记录和当前控制面；不运行
    科学实验，不改变 phase-1 scientific disposition。
  - 影响的未决项：phase 2 从哪个 READY/NEEDS_SMALL_ADAPTER carrier 开始，
    必须等 v2 终验后按方法生产价值比较。
- **[2026-07-26] [D001]**：C15 推荐被 formal owner 核查推翻，首包续接 B1。
  - 原因：C15 未完成新候选 Step 1–3，直接运行违反 FR-22；B1 已有 formal
    Step 1–3，T007 Kill 又因 baseline/metric/oracle/observability 缺口未被接收。
  - 新范围：只授权 T008 在 GW Step 4a 做五项 identity 修复，并在合法空间仍在时
    同包完成三个方法；不再派纯 repair 包。
  - 影响的未决项：corrected headroom 是否存活，P1–P3 能否形成方法信号。
- **[2026-07-26] [D002/V002]**：T008 `KILL_NO_ADAPTIVE_WINDOW_SPACE`
  被拒收，B1 转 `BLOCKED_IDENTITY / RETURNED_TO_POOL`。
  - 原因：所有 primary cell 无 FEC crossing，却用 `dB-equiv` 触发 Kill；实际 gate
    不是 per-block oracle，且跳过包含真实 B*=256 的候选；BER population 与
    π/2 branch resolve 使基线不在可靠 working region。
  - 新范围：停止 B1 修复；只做 Goal handoff 和 campaign remap。
  - 影响的未决项：下一合法 carrier 必须由 remap 比较方法产出潜力、补债成本与
    formal readiness 后确定，不能从旧 portfolio 标签直接挑。
- **[2026-07-26] [D003/R001/formal D015]**：campaign remap 选择 A4 deployable
  adaptive CPR 作为首个 active carrier。
  - 原因：A4 已有方法动作、Step 1–3/Step 4a 证据、30-seed 数据和写作资产；
    相比 B10/B12 的 source-native 重建与 B1 的第三个 evaluator repair，更可能
    在一个包内直接产生可验收 method delta。
  - 新范围：只授权 T009 做一次有界 identity adjudication，并在同包完成 P1–P3
    fresh paired comparison；不改论文、common、params 或 owner。
  - 影响的未决项：A4 是否能在 strongest fixed comparator 下形成
    `METHOD_SIGNAL`；若不能，不开第二个 A4 repair 包，自动回到 carrier remap。
- **[2026-07-26] [D004]**：运行方式从“用户中转外部 GLM”改为“本对话主控
  端到端执行”。
  - 原因：用户明确不想拆分 GLM，希望本对话自行完成全部工作。
  - 新范围：主控直接管理线程内 executor/verifier，用户无需搬运 T 或技术回执；
    科学执行与审查仍保持不同 agent。
  - 影响的未决项：仅改变任务执行接口，不改变 A4、formal D015、CP008 或 T009
    科学门槛。
- **[2026-07-26] [D005]**：T009 身份阻断后撤销 A4 当前 carrier，重开
  post-T009 campaign remap。
  - 原因：独立 verifier 发现 pilot/TX-truth、DA/NDA frequency-stage、公认工作区
    与提交内 raw closure 四类 P0；P1–P3 未运行，method delta 为 `NONE`。
  - 新范围：A4 返回候选池且不再修当前 evaluator；formal 暂无 active carrier，
    只允许 Recover、Portfolio Map 和 Task Preparation，激活下一 carrier 前禁止实验。
  - 影响的未决项：下一动作改为比较 B10 source-native 最小重建与其他
    formal-ready candidates，并说明为何所选项比至少两个替代项更可能产生
    `METHOD_SIGNAL`。
- **[2026-07-26] [D006/R002/formal D017]**：post-T009 remap 激活 B10
  source-native adaptive pilot-RLS。
  - 原因：B10 已有 L20/Q1/Q2 Step 1–3、formal D012 与可获取全文；相对 C15
    少完整前置周期，相对 B1 避免第三 evaluator repair，相对 B9 不需新接收架构。
  - 新范围：只授权 T010 重建 128 contiguous pilot→DD 的 source-native fixed B10，
    identity 过门后同包比较 innovation freeze、adaptive forgetting、amplitude-only
    cheap rule 与 4OPM+BPS/DD-DPLL。
  - 影响的未决项：T010 是否产生 `METHOD_SIGNAL/PACKAGING_BOUNDARY`；失败后不开
    第二个 B10 repair，优先转 C15 Step 1–3 formalization。

## 已确认结论

### 不变量

- 顶部控制块只拥有前台动作绑定，不拥有科学事实。
- conversation summary 只能定位文件，不能改变 active lane。
- 每个执行包关闭一个科学决策不确定性，但可包含多个有界动作。
- candidate 轮换留在 exploration mission；formal 晋级才新建/恢复 formal topic。
- 普通包只使用 T、worker-log、可选 artifact 和 commit。
- master 与 executor 在同一 live-test worktree 串行操作，不同时写。
- 本对话是长期主控并端到端推进；用户无需中转 T 或判断技术正确性。
- MVE 执行与科学验收必须由不同的线程内 agent 完成，主控负责集成与拍板。

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
- **S001 续接 / T006验收/V001/D013/T007**：T006 32 tests 在 UTF-8 下通过，但
  source-native probe、pilot/data channel 审计与 robust headroom 统计共同推翻
  “机制失败”裁决；另发现 T006 缺 task-control marker。epoch 9 停止该修复并切到
  B1 自适应相位窗，授权一个结构门过即完成三方法的 T007 大包。
- **mission-log / phase-1 audit**：CP001–CP007 已回填。审计确认无严重跨 lane，
  但 formal success 多次没有 mission method delta；T007 暂不接收 family Kill，
  T008 停止。
- **D001 / phase-2 entry**：B1 作为唯一合法 formal carrier 续接；C15 保留候选，
  不以 portfolio readiness 冒充 formal authorization。
- **V001 / T008 dispatch review**：独立终验 PASS；formal/guard/identity/method
  continuation/statistical gate/≤1 天预算均闭合，无 P0/P1。
- **CP008 / D002 / V002**：T008 工程测试 17/17 PASS，但主控与独立 critic
  发现 metric、oracle、eval population 和 artifact closure P0/P1；正式 Kill 拒收。
  mission method delta 连续八包为 NONE，状态为 DRIFTED/STALLED，停止 T009。
- **H002**：新 GPT Goal 对话恢复入口；先验三条事实并做 campaign remap。
- **V003**：CP008 状态协调与 H002 独立终验 PASS，P0/P1/P2 均为 0。
- **R001 / D003 / formal D015 / T009**：三 carrier remap 选择 A4；control epoch
  14 只授权 deployable identity + P1–P3 方法生产大包。
- **D004**：取消外部 GLM 中转，control 升至 epoch 15；本对话主控使用线程内
  executor/verifier 端到端完成 T009。
- **V004**：campaign remap、formal 激活与 T009 独立终验 PASS；两轮审查缺口
  关闭后 P0/P1/P2 均为 0，允许中转 T009，不预判方法结果。
- **V005**：epoch 15 执行接口切换独立终验 PASS；P0/P1/P2 均为 0，确认
  T009 科学合同未变，允许线程内 executor/verifier 分离执行。
- **CP009 / V006 / D005 / formal D016**：T009 的 5 项工程测试与 DPLL smoke
  通过，但独立终审为 `FAIL, P0=4, P1=5, P2=1`。主控重算复现 540 行与 DA
  9/9 算术，同时确认 pilot/TX truth、1 MHz frequency-stage 不对称、无来源且
  无 crossing 的 working region、ignored raw/result 四项 P0；接受
  `BLOCKED_IDENTITY / NONE`，拒绝物理支配 claim。A4 回池，epoch 16 重开
  campaign remap。
- **R002 / D006 / formal D017 / T010**：比较 B10、C15、B1、B9 后激活 B10
  source-native adaptive pilot-RLS。T010 明确 128 contiguous pilot→DD、TX 侧
  同通道、source smoke、P1 fixed/P2 innovation freeze/P3 adaptive forgetting、
  amplitude-only cheap rule 与 conventional B*；等待独立起飞审查。

## 未决项

- B1 family 保持 `UNRESOLVED`；若未来复用必须重建 evaluator，而非继续修 T008；
- T010 的 source-native identity、合法 working region和方法信号尚待执行/验收；
- C15 保留为 T010 失败后的 Step 1–3 formalization 轮换点；
- live run 自然覆盖哪些恢复/轮换/晋级事件；
- 何时由原 design 对话进行阶段性审计。

## 当前位置

B10 SOURCE-NATIVE PACKAGE PREPARED。T009/CP009 的
`BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED / method delta NONE` 保持不变。
R002/D006/formal D017 已激活 B10 carrier，control 绑定 epoch 17 / CP009。
下一合法动作是独立审查 T010；通过后由线程内 executor 执行 source-native identity
与同包方法比较。不得修 T006/B12 组合、B1/T008、A4/T009，也不进入 Step 5。
