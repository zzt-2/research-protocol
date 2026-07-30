# Topic Index: Research Direction Lab 长程真实运行测试

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v2
  control_epoch: 61
  role: LIVE_TEST
  mission: 在真实研究反馈中验证轻量长程运行协议能否稳定推进并积累可用方法材料
  active_lane: SPRINT003_PREFORMAL_FACTORY_BOUND
  authority_pointer: .sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D036
  decision_gate: 最终纠偏完成（S003→D036/V062）：纠正门2 证据等级（sprint-001 块末更新=结构性吸引子归因已被 V052 拒收，降级为 source-backed 疑似作用点）；冻结传统 comparator = tuned per-symbol canonical Godard-with-z CMA（provenance cb1_cell_runner:124-129，禁 scalar-error _cma.py 冒充）；action_class 改为 PREFORMAL_METHOD_FACTORY（不再用 METHOD_FACTORY_TASK_PREPARATION 掩盖实验）；新增 PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR 终态；T027 validate_task_control.py PASS（epoch 61 / CP025）
  allowed_actions:
    - RECOVER
    - TASK_PREPARATION
    - PORTFOLIO_MAP
    - PROMOTION_PREFLIGHT
    - PREFORMAL_METHOD_FACTORY
  forbidden_actions:
    - SCIENTIFIC_EXPERIMENT
    - CLOSED_AXIS_REOPEN
    - FREQUENCY_DOMAIN_SUBBAND_FAMILY
    - FORMALIZATION_ONLY_PACKAGE
    - GENERAL_INFRASTRUCTURE_BUILD
    - PRIVATE_FULLTEXT_ACQUISITION
    - ABSTRACT_AS_FULLTEXT
    - POST_STEP4A_ADVANCE
    - SCIENCE_SCOUT_REACTIVATION
    - PROTECTED_HISTORY_EDIT
    - FORMAL_MVE
    - PAPER_CLAIM
    - PROTECTED_OWNER_MODIFY
  mission_log_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/mission-log.md
  mission_checkpoint: CP025
  next_legal_action: 本对话内端到端执行 T027 诊断 sprint-003（PREFORMAL_METHOD_FACTORY，bounded）：executor 跑 3-5 个更新粒度构造，独立 verifier 验收，主控接收；授权仅覆盖本次诊断 sprint
```
<!-- RDL-CONTROL:END -->

> 状态: active（CP027：sprint-003 端到端完成，verdict NO_DIAGNOSTIC_SIGNAL；epoch 61 / CP027，CB1 更新粒度均衡族轴关闭；频域/子带族因物理自由度不存在已撤回，作 rejected task brief 保留）
> 创建: 2026-07-23 | 最后更新: 2026-07-29

## 专题信息

- 上游设计专题：`2026-07-20-research-direction-lab-system`
- 长程权威链：`mission-log.md`
- 详细过程：T###、`projects/thesis-fso/worker-logs/step-###-*`、artifacts、D/V
- 本文件职责：只保存原始目标、当前范围、不变量、当前 gate 和下一合法动作

## 范围边界

### 原始目标（冻结）

在用户只中转 T 路径和四项完成索引的协作方式下，让 fork 主控跨多个真实工作包稳定保持目标、在局部失败后合法换路、控制治理成本，并提高形成可用论文方法与材料的概率；运行一段时间后由原 system design 对话根据磁盘证据审计。

### 当前范围

- T001–T026 的完整 disposition、method delta、轮换和重量见 `mission-log.md` CP001–CP025。
- T019 后产生两个局部 `METHOD_SIGNAL`；T025/T026 形成
  `PACKAGING_BOUNDARY` 与 `WRITING_MATERIAL`，但 active scientific carrier、
  formal method 和当前论文主方法仍均为 0。
- G1 科学线关闭，claim ceiling 保持
  `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`；现有方法卡、小节和图只作次级/扩展资产。
- R009 效果审计与 system D019/V013 最小协议修订均已完成并同步个人 Skill。
- 修订终验后，下一轮 live test 以
  `METHOD_SIGNAL → Step 1–3/3.5/4a → PROMOTION_READY/active carrier`
  的端到端转化作为毕业方法生产成功。

### 明确不含

- 不运行科学实验、重开已关闭轴、进入 Step 5/Contract/Execute 或恢复 science-scout；
- 不修改 session-governance、建设 controller/scheduler、通用基础设施或 per-fork manifest；
- 不获取私有全文，不把摘要冒充全文；
- 不修改 protected history、formal scientific owners 或 thesis framework；
- 不把流程 PASS、包装或写作材料冒充正式方法；
- 不要求用户读取技术日志或判断科学正确性。

### 范围变更记录

- 2026-07-23，system D017：建立只受 foreground control 授权的 live-test mission。
- 2026-07-23 至 2026-07-28，formal D062–D066、live D001–D025：Pilot-Jones、
  B10/B12、B1、A4、C15、B9、C16/Q14 等依次运行、拒收、局部 Kill 或返回池；
  逐次理由与边界保留在 `decisions.md`、`verifications.md` 和 CP001–CP017。
- 2026-07-26，system D018 / live D026：旧协议连续 17 包无方法增量，启用
  pre-formal method factory、formal/method 双账和三层记录。
- 2026-07-28 至 2026-07-29，live D027–D033：T019–T025 形成两个诊断 signal、
  一个 bounded package；逐次正式化与拒收理由见 CP018–CP024。
- **2026-07-29，live D034 / system D019**：接收 T026 写作材料并暂停 T027。
  - 原因：R009 确认旧阶段方法增量 0/17，后段 signal→formal 转化仍为 0/2，且真实协作基本每次交互都会压缩。
  - 新范围：只修改恢复三问、工厂硬路由、promotion preflight、事件式 recovery receipt，并压缩 current snapshot。
  - 影响：下一 live test 必须验证 signal→active carrier/`PROMOTION_READY`；包装和写作材料不计毕业方法成功。
- **2026-07-29，live D035 / V061**：T027 入口最小纠偏（用户中转指令）。
  - 原因：原 T027（频域/子带均衡族）未过 problem-bearing testbed preflight 门1——
    `_dual_pol_channel.py:127-132` 信道只有逐符号 GG 幅度、SOP 旋转、AWGN，**无色散/多径/FIR/频率选择性**，
    频域/子带无可作用的物理自由度；其 comparator 也非已确认的传统/任务适配/同信息对象；task-control
    `control_epoch=59` 与 topic epoch 60 不一致（validator `stale_control_epoch`）；`action_class` 写
    preparation 但正文要求运行实验，语义不一致。
  - 新范围：method-production.md 补入口四门（每门 file:line，禁"未测族/REOPENED/testbed 曾产 signal"放行）；
    T027 **原位重写**为唯一四门全过的替代入口（逐符号/更新粒度均衡族，comparator 首选逐符号
    stochastic-gradient CMA），不新建 T028；频域族作 rejected task brief 保留、不运行。
  - 影响：active_lane → `SPRINT003_DISPATCH_READY_ENTRY_REDIRECTED`，authority → D035；
    频域/子带族加入 `forbidden_actions`（`FREQUENCY_DOMAIN_SUBBAND_FAMILY`）；无科学 carrier 变更、
    无 protected history / formal owner 改动。
- **2026-07-29，live D036 / V062**：T027 端到端完成（最终纠偏 → 科学执行 → 独立验证 → 主控接收，用户中转指令，一轮内无停顿）。
  - 最终纠偏（修 D035/T027/V061 证据等级与授权语义）：①门2 证据等级——sprint-001"块末更新几何
    =结构性吸引子原因"已被 V052 拒收，降级为 source-backed 疑似作用点；②comparator 冻结为
    canonical Godard-with-z（`cb1_cell_runner.py:124-129`，禁 `_cma.py` scalar-error 缺 z 冒充），
    μ dev 单独调谐；③action_class→`PREFORMAL_METHOD_FACTORY`（epoch 60→61，不再用 preparation 掩盖
    实验），授权仅本次 bounded sprint；④method-production.md 终态集 3→5（+ `PROBLEM_RESOLVED_BY_
    CONVENTIONAL_COMPARATOR` + `EXECUTION_INVALID`），补 Gate-2 evidence grade + comparator
    gradient identity 两段。
  - sprint-003 执行（commit `689151c`）：4 个更新粒度构造（block-64 anchor、tuned per-symbol
    Godard-with-z comparator、block-8/16、sliding-window recursive），dev 冻结后跑 fresh held-out
    （7 cells × 20 test seeds，禁 seeds 71–80）。独立 verifier V062 **PASS**（梯度身份逐方法核、
    raw→aggregate 独立复算吻合<1e-4、verdict 唯一正确）。verdict = **`NO_DIAGNOSTIC_SIGNAL`**
    （最佳 block8 vs comparator Δ=−0.00293、CI 跨 0、未过 MDE；comparator 只 1/7 cell 消除 collapse）。
  - 影响：CB1 更新粒度均衡族轴关闭（无 signal 即退出）；active_lane →
    `SPRINT003_PREFORMAL_FACTORY_BOUND`；authority → D036；仍 0 active carrier、无 protected owner
    / formal 改动；method-production.md 终态集与 Gate-2/comparator 段更新（同步 Skill）。

## 已确认结论

### 不变量

- 顶部 control 只绑定前台动作，不拥有科学事实。
- conversation summary 只定位文件，不能改变 active lane。
- `topic-index.md` 是当前快照；`mission-log.md` 是完整紧凑长链；T/worker/artifact 保存包细节。
- 每个执行包关闭一个科学决策不确定性，但可包含多个有界动作。
- formal science disposition 与 mission method delta 必须分账。
- candidate 轮换留在 exploration mission；formal 晋级才新建或恢复 formal topic。
- executor 不修改 formal/current/mission owners；master 接收后更新。
- MVE 执行与科学验收分离，用户不承担技术正确性判断。
- 包装、写作材料和可靠负面都可 harvest，但不自动成为主方法。

### 其他结论

- CP001–CP017 的状态保存基本成功，方法生产失败；问题主要是动作路由，不只是记忆丢失。
- T019 后工厂显著提高近端发现速度；当前端到端 formal-method yield 为 0/2。
- G1 的最佳位置是高阶调制扩展、discussion、附录或未来工作，不是当前主贡献。
- 恢复效果过去只有静态证据；RC001 首次显式记录，但耗时与读取数因规则生效前未测。

## 进展线索

| 阶段 | 结果 | 权威入口 |
|---|---|---|
| CP001–CP007 | phase 1：多次 semantic/identity 修复，0 方法增量 | mission-log |
| CP008–CP017 | Goal/形式化链：10 包连续 drift/stall，累计 17/17 `NONE` | mission-log |
| CP018–CP019 | T019/T020 方法工厂：第 2 包产生首个因果诊断 signal | mission-log |
| CP020–CP023 | Q15→G1 formalization：产生第二 signal，但 formal conversion 失败 | mission-log |
| CP024–CP025 | G1 bounded package→论文小节与两图；science ceiling 不变 | mission-log / T025–T026 |
| R009 / D034 | 纵向效果审计完成；进入 system D019 最小修订 | R009 / decisions.md |
| S003 | 下一入口选择：两 signal preflight=STRATEGIC_GATE，硬路由 method factory | S003 |
| S003→D035/V061 | T027 入口纠偏：频域/子带族 preflight 门1 失败（无物理自由度）撤回；原位重写为逐符号/更新粒度均衡族（四门全过），comparator=逐符号 SGD-CMA | S003 / T027 / V061 |
| S003→D036/V062 | T027 端到端完成（最终纠偏+执行+验收一轮内无停顿）：verdict `NO_DIAGNOSTIC_SIGNAL`；CB1 更新粒度族轴关闭；疑似作用点（块末更新）因果性未被确认（collapse 在所有更新粒度下持续） | T027 / sprint-003 `689151c` / V062 |

## 未决项

- T027 sprint-003 已完成（`NO_DIAGNOSTIC_SIGNAL`，CB1 更新粒度族轴关闭）；
- 仍 0 active carrier；下一入口由 portfolio remap 选机制不同的合法 carrier，或战略 gate 升级
  （私域全文/论文范围决策），届时交用户；
- 下一真实压缩事件需量化 elapsed time、files read、lane/gate match；
- G1 只保留 bounded thesis asset，不重开科学修复；
- 频域/子带均衡族仅在信道源码被升级到含色散/多径/频率选择性后才可能重审，当前作 rejected task brief 保留。

## 当前位置

S003 入口选择后，经 2026-07-29 用户中转指令做**最小入口纠偏**（D035/V061）：原 T027 选的
**频域/子带均衡族**未过 problem-bearing testbed preflight 门1（`_dual_pol_channel.py:127-132`
信道只有逐符号 GG 幅度 + SOP 旋转 + AWGN，无色散/多径/FIR/频率选择性，频域/子带无可作用物理
自由度；其 comparator 也未冻结；task-control epoch 59≠60；action_class 与正文语义不一致），
故原 DISPATCH_READY 撤回，频域族作 rejected task brief 保留、不运行。

method-production.md 补了入口四门（物理自由度存在 / 基线失败与作用点一致 / 命名传统同信息
可独立调谐 comparator / 每门 file:line，禁"未测族/REOPENED/testbed 曾产 signal"放行；并厘清
shared anchor vs. identity parity——后者只保护继承基线比较连续性，不禁止跑不同传统算法）。

**2026-07-29 CP027（D036/V062）**：用户中转指令要求一轮内端到端完成"最终纠偏 → 科学执行 →
独立验证 → 主控接收"。最终纠偏（四项）：①门2 证据等级——sprint-001"块末更新几何=结构性吸引子
原因"已被 V052 拒收，降级为 source-backed 疑似作用点（不是已确认机制）；②comparator 冻结为
canonical Godard-with-z（`Δw ∝ (R²−|z|²)·z·r*`，provenance `cb1_cell_runner.py:124-129`，禁
`_cma.py` scalar-error 缺 z 冒充）；③action_class→`PREFORMAL_METHOD_FACTORY`（epoch 60→61）；
④终态集 3→5（+ `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR` + `EXECUTION_INVALID`）。

sprint-003 由独立 executor 跑（commit `689151c`）：block-64 μ=0.03 anchor（PI-SER 0.31431）、
tuned per-symbol Godard-with-z comparator μ=0.001（0.29685）、block-8/16、recursive CMA，4 构造
× 7 cells × 20 fresh test seeds。独立 verifier V062 **PASS**（梯度身份逐方法核、raw→aggregate
独立复算吻合<1e-4）。**verdict = `NO_DIAGNOSTIC_SIGNAL`**：最佳 block8 vs comparator
Δ=−0.00293、CI [−0.0112,+0.0056] 跨 0、未过 MDE=−0.005；comparator 只 1/7 cell 消除 collapse，
未达 PROBLEM_RESOLVED 判据；候选场在 64× 更新预算跨度上平坦，既非更多更新也非粒度产生可分离
优势。**疑似作用点（块末更新）的因果性未被本 sprint 确认**——collapse 在所有更新粒度下都持续。

CB1 更新粒度均衡族轴按 method-factory 纪律关闭（无 signal 即退出）。当前仍 0 active carrier；
无 protected owner / formal / thesis framework 改动；无 push。下一合法动作：portfolio remap 选
机制不同的合法 carrier，或战略 gate 升级（届时交用户）。
