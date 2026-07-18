# Direction Lab 运行流程

> 版本：DL-Process v0.2（2026-07-18）  
> 适用范围：双偏振星地 OSL 场景中的 ML 应用探索  
> 状态：项目级执行规范；尚未打包为 Codex skill

## 1. 目的与边界

Direction Lab 的研究单位是“机制族批次”，不是单个网络微变体。它复用已有地基中的 baseline、参数来源、论文库、失败记录和代码资产，在同一场景内批量寻找 ML 的可行应用。

它不替代正式 Groundwork，也不自动产出论文结论。所有 sandbox 数字只能在通过独立验证、重新冻结合同并进入正式阶段后使用。

固定不变量：

- 场景边界是双偏振星地 OSL 及其完整接收/处理链；地基不是 ML 候选封闭边界。
- canonical baseline、指标口径和已确认死路不可被候选运行静默改写。
- `standard-CMA` 与历史 `current-CMA/no-z` 必须是不同 component ID。
- 没有 manifest、receipt、execution result hash 和 source closure 的运行不得进入 evidence ledger。
- sandbox 结果不得自动进入正式 Groundwork、论文或 canonical baseline。

## 2. 三层工作模式

### 2.1 Scout（轻量）

目标是回答“下一批该比较哪些机制”，不跑正式仿真。

输入：anchor、已有代码/结果、论文索引、failure registry、Candidate Universe。  
输出：机制级 CandidateMap、BatchPlan、实现缺口表和排序理由。

Scout 必须先完成全景，再排序；不得因一个候选的正/负信号提前收敛。每个候选至少记录：

`mechanism | action time | information access | code interface | baseline | cost | diagnostic | dependency | collision risk | status`

### 2.2 Sandbox Batch（中量）

只有实现、输入/指标合同、fingerprint 和预算齐备的机制族才能进入。一个批次必须包含：

- 同一个 canonical baseline、realization、seed split 和 metric contract；
- 至少两个可区分机制，或明确声明这是一个有交互假设的组合批次；
- 最强简单对照、无变化 baseline 和必要 ablation；
- 预注册 primary metric、机制诊断、advance/retire/defer 条件；
- exact valid domain，禁止运行后扩大泛化声明。

运行链为：

`Queue PASS → manifest freeze → controller RUN → execution audit → artifact/hash → EvidenceGate → independent verifier → batch synthesis`

### 2.3 Promotion / Deep Evidence（重量）

只有批次级稳定 winner 才进入。Promotion 才调用完整 GW/Contract、增量文献补证、竞品闭合和论文材料门控。单个微变体不得直接跳入完整 GW。

## 3. 状态与门控

候选状态：

`SEED → MAPPED → QUEUED → PROBED → SYNTHESIZED → RETAINED / PROMOTED`

负向或阻断状态：

`STALE_BASELINE | INVALID_PROBLEM | COLLISION | RETIRED_SPECIFIC | DEFERRED | ARCHIVED`

状态转换必须由机器可读产物支持，不能只由自然语言日志推动。当前唯一状态源应是 `canonical-state.yaml`；`topic-index.md`、session note 和 README 只做摘要。

### 3.1 运行前硬门

脚本必须阻断以下情况：

- batch_id 未显式指定；
- Queue/Map/Registry 未 PASS 或 fingerprint 不一致；
- contract 使用隐式物理/运行默认值；
- baseline/component 状态与 manifest 不一致；
- source closure 缺失或只来自手写清单；
- 结果目录已有不同 manifest 的同名产物；
- `contract_override` 或外部注入函数绕过合同；
- sandbox manifest 请求 GO/KILL/PROMOTE；
- evidence receipt 缺失、result hash 不匹配、重复提交或 stale。

### 3.2 状态更新规则

运行前 manifest 记录 `pre_state_hash` 和输入快照。运行完成后只写 append-only completion event；独立验证通过后，由 state reducer 更新 `canonical-state.yaml`。

因此，完成运行后更新状态不会反过来污染历史运行的 provenance。历史 batch 不得通过事后修改源快照来“修正”。

## 4. 代码与文件对齐

项目目录是运行态唯一拥有者：

```text
projects/thesis-fso/direction-lab/
├── process.md                 # 本规范，流程唯一拥有者
├── README.md                  # 入口和当前状态摘要
├── anchor.yaml                # baseline、参数域、已知债务
├── canonical-state.yaml       # 机器可读状态权威
├── candidate-universe*.yaml   # 候选全景及不可变 lineage
├── candidate-map*.yaml        # 机制级排序与覆盖状态
├── batch-queue*.yaml          # 已冻结批次合同
├── component-registry*.yaml   # 代码组件身份与 fingerprint
├── discovery-ledger.jsonl     # 搜索角度和收敛记录
├── failure-registry.yaml      # 失败机制、退出原因、salvage
├── batches/B###-slug/         # 每批 manifest、artifact、状态、复核、综合
├── tools/                     # 受门控的 runner/validator
└── tests/                     # runner、合同、指标和边界测试
```

代码状态与方向状态分离但必须互相绑定：

`SANDBOX → CANDIDATE → CANONICAL → ARCHIVED`

候选不得直接改写 canonical baseline；晋级必须产生新 component ID、测试、fingerprint 和 valid-domain 声明。

Evidence ledger 只保存 receipt、manifest/result hash 和 artifact pointer；完整结果只存在批次 artifact。每批只需要一个机器状态文件、一个 verifier report 和一个 synthesis，不复制 raw JSON 到 session 文档。

## 5. 止损与换族

- CandidateMap 未完成前，单候选不得占用完整证明预算。
- 连续两轮改善小于 10%，或机制诊断不朝假设方向变化，停止同一微变体扩展。
- 同一机制族连续两批没有新增信息，返回 Scout，换到另一应用点或方法族。
- 结果只在单 seed/单参数域有效时，只能 `RETAINED_SPECIFIC`，不得升为家族结论。
- baseline 接近 oracle 时，转为边界/分析问题，不继续堆模型。
- provenance 返工超过一次，暂停算力，先修 ledger/状态模型。
- 正信号若可能修的是代码 bug，先做 baseline/实现对照，不得直接写成研究发现。

## 6. 从零与从地基

从零入口：

`Project Intake → Prior Asset Scan → Broad Universe → Collision Precheck → BatchPlan`

从地基入口：

`Anchor Audit → Baseline Revalidation → Import Existing Evidence → Refresh Universe/Map → BatchPlan`

旧结果必须按 baseline SHA、参数域、指标口径和 source closure 标为 `VALID / STALE / UNKNOWN`。复用旧结果是证据复用，不等于复用旧结论。

## 7. 当前实例的正确解释

B002 与 B003 的 U24 结果属于同一 exact contract；B003 的主要新增价值是治理链复核，而不是新的方法学证据。下一批不得继续重复 U24 微变体，也不得把 Logistic/MLP 的 exact-domain `ADVANCE_SPECIFIC` 扩展成方法族结论。

候选 Universe 仍保持开放。下一轮先完成 canonical state reconciliation 和机制族 BatchPlan，再选择实现就绪且能产生新信息的批次。

## 8. 未来 skill 化要求

当前文件是项目级规范，不是 skill。稳定运行若满足以下条件，再抽取成 skill：

1. 至少三个不同机制族批次通过同一套 Scout/Sandbox/Promotion 分层；
2. state reducer、manifest、receipt、artifact pointer 和 stale 传播接口稳定；
3. 失败候选和 salvage lineage 可查询；
4. 独立压力测试证明 agent 不能靠自然语言绕过硬门；
5. 项目专属字段与通用治理字段已解耦。

skill 只负责导航、检查和调用入口；真正的允许/阻断必须继续由脚本和状态机执行。
