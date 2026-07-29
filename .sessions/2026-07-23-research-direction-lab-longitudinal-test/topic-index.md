# Topic Index: Research Direction Lab 长程真实运行测试

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v2
  control_epoch: 59
  role: LIVE_TEST
  mission: 在真实研究反馈中验证轻量长程运行协议能否稳定推进并积累可用方法材料
  active_lane: NEXT_LIVE_TEST_SELECTION_READY
  authority_pointer: .sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D034
  decision_gate: D019/V013 v2.1 已终验并同步；当前无 active carrier，T027 前先选择能验证 signal→formal 转化的合法入口
  allowed_actions:
    - RECOVER
    - TASK_PREPARATION
    - PORTFOLIO_MAP
    - PROMOTION_PREFLIGHT
    - METHOD_FACTORY_TASK_PREPARATION
  forbidden_actions:
    - SCIENTIFIC_EXPERIMENT
    - CLOSED_AXIS_REOPEN
    - FORMALIZATION_ONLY_PACKAGE
    - GENERAL_INFRASTRUCTURE_BUILD
    - PRIVATE_FULLTEXT_ACQUISITION
    - ABSTRACT_AS_FULLTEXT
    - POST_STEP4A_ADVANCE
    - SCIENCE_SCOUT_REACTIVATION
    - PROTECTED_HISTORY_EDIT
  mission_log_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/mission-log.md
  mission_checkpoint: CP025
  next_legal_action: 重读 current portfolio 与完整 mission-log，按恢复三问比较现有可转化入口和新方法工厂 testbed，再准备 T027
```
<!-- RDL-CONTROL:END -->

> 状态: active（T026 已接收；epoch 59 / CP025，v2.1 已终验，下一 live-test 入口选择就绪）
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

## 未决项

- 下一 live test 的具体 scientific carrier/factory testbed 尚未选择；
- 下一真实压缩事件需量化 elapsed time、files read、lane/gate match；
- G1 只保留 bounded thesis asset，不重开科学修复。

## 当前位置

T026 已由 D034 接收为 `artifact_delta=WRITING_MATERIAL /
mission_method_delta=NONE`，CP025。当前无 active scientific carrier。system
D019/V013 v2.1 已终验并同步。下一步先按恢复三问比较现有可转化入口与新的方法
工厂 testbed，选择能验证 signal→formal 转化的下一 live-test 入口，再生成 T027。
