# Direction Lab 运行流程

> 版本：DL-Process v0.3（2026-07-18）
> 适用范围：通用研究探索内核；当前提供 Communications profile，并由 OSL project adapter 实例化
> 状态：项目级执行规范；尚未打包为 Codex skill

## 1. 目的与边界

Direction Lab 的研究单位是“机制族批次”，不是单个网络微变体。它复用已有地基中的 baseline、参数来源、论文库、失败记录和代码资产，在一个明确领域内批量寻找 ML 的可行应用。

流程分为三层：

- **Universal Core**：状态、候选、能力类型、运行、证据、风险和生命周期；不包含 BER、SNR、pilot 或具体物理对象。
- **Domain Profile**：领域术语、合法指标、常见能力和反模式。当前的 `communications` profile 覆盖通信研究，但不绑定某一种链路。
- **Project Adapter**：项目的 simulator、baseline、代码组件、参数和 valid domain。当前双偏振 OSL 是一个 adapter，不是流程本身。

它不替代正式 Groundwork，也不自动产出论文结论。所有 sandbox 数字只能在通过独立验证、重新冻结合同并进入正式阶段后使用。

Universal Core 不变量：

- candidate 的输入、时间边界、输出/动作和 comparator 必须可描述；领域 profile 再补充具体字段。
- canonical baseline、指标口径和已确认死路不可被候选运行静默改写。
- 没有 manifest、receipt、execution result hash 和 source closure 的运行不得进入 evidence ledger。
- sandbox 结果不得自动进入正式 Groundwork、论文或 canonical baseline。

当前 Communications profile 的不变量：

- 必须区分 receiver-visible information、training/evaluation-only information 和 oracle/TX truth。
- BER/FER/LLR/GMI 等指标由 profile 声明，不得写进 Universal Core。
- baseline 合法性、同预算 comparator、因果 trace 和通信链路时序必须由 profile 或 Project Adapter 负责。

## 2. Capability Triage（进入 Scout 前的轻门）

先判候选的能力类型，再决定需要多重的合同和 runner：

| capability | 典型输出 | 额外前置能力 |
|---|---|---|
| `observational` | 监测、告警、质量估计 | receiver-visible trace adapter |
| `estimative` | 状态、信道、后验、置信度 | 标签/估计误差/因果边界 |
| `action` | pilot、reset、mode、resource action | action schema、comparator、决策时刻 |
| `closed_loop` | 在线控制、反馈、迭代接收机 | state snapshot、action hook、fork replay、post-action continuation |

Capability Triage 只做可行性检查，不建 Queue、不创建正式 fingerprint、不跑性能实验。至少回答：输入从哪里来、什么时候可见、是否改变状态、现有 runner 能否承载、缺口是小适配还是新仿真底座。

如果候选需要 `closed_loop` 能力而 Project Adapter 没有 state/action/replay 接口，直接标记 `DEFERRED_ARCHITECTURE`，不得先写一整套 Sandbox contract 再发现底座不支持。

## 3. 三层工作模式

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

## 4. 状态与门控

候选状态：

`SEED → MAPPED → QUEUED → PROBED → SYNTHESIZED → RETAINED / PROMOTED`

负向或阻断状态：

`STALE_BASELINE | INVALID_PROBLEM | COLLISION | RETIRED_SPECIFIC | DEFERRED | ARCHIVED`

状态转换必须由机器可读产物支持，不能只由自然语言日志推动。`state/completion-events.jsonl` 是 append-only 转换事实源，`canonical-state.yaml` 是由 reducer 物化的当前投影视图；`topic-index.md`、session note 和 README 只做摘要。

这里的 `canonical-state.yaml` 只对 Direction Lab Sandbox 投影负责；正式研究状态与授权只看 `projects/thesis-fso/master-state.md`。`sandbox_state: BOARD_READY` 表示全局 board/controller 基础设施能力，不等于当前 Scout 已进入 Sandbox，也不授予候选创建 Queue、Registry 或执行 batch。

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

运行前 manifest 记录 `pre_state`（内容寻址 projection、event head 和 event count），并保存不可变 state snapshot。运行完成后只写 append-only completion event；独立验证通过后，由纯 reducer 从 immutable projection + event log 更新 `canonical-state.yaml`。可变的 top-level projection 不得进入 source import closure；历史 runner 若发现 expected canonical SHA 漂移，只能回退到内容寻址 projection，不能修改历史 batch。

因此，完成运行后更新状态不会反过来污染历史运行的 provenance。历史 batch 不得通过事后修改源快照来“修正”；B003 的旧 canonical bytes 已保存在 `state/projections/821415...yaml`，当前视图由 reducer 产生。

## 5. 代码与文件对齐

项目目录是运行态唯一拥有者：

```text
projects/thesis-fso/direction-lab/
├── process.md                 # 本规范，流程唯一拥有者
├── profiles/                  # 领域 profile；当前以 communications 为目标，不复制项目实现
│   └── communications.yaml
├── adapters/                  # 项目 adapter 的逻辑映射
│   └── dual-pol-osl.yaml
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

## 6. 止损与换族

- CandidateMap 未完成前，单候选不得占用完整证明预算。
- 连续两轮改善小于 10%，或机制诊断不朝假设方向变化，停止同一微变体扩展。
- 同一机制族连续两批没有新增信息，返回 Scout，换到另一应用点或方法族。
- 结果只在单 seed/单参数域有效时，只能 `RETAINED_SPECIFIC`，不得升为家族结论。
- baseline 接近 oracle 时，转为边界/分析问题，不继续堆模型。
- provenance 返工超过一次，暂停算力，先修 ledger/状态模型。
- 正信号若可能修的是代码 bug，先做 baseline/实现对照，不得直接写成研究发现。

## 7. 从零与从地基

从零入口：

`Project Intake → Prior Asset Scan → Broad Universe → Collision Precheck → BatchPlan`

从地基入口：

`Anchor Audit → Baseline Revalidation → Import Existing Evidence → Refresh Universe/Map → BatchPlan`

旧结果必须按 baseline SHA、参数域、指标口径和 source closure 标为 `VALID / STALE / UNKNOWN`。复用旧结果是证据复用，不等于复用旧结论。

## 8. 当前实例的正确解释

B001–B003 是 Communications profile 下的双偏振 OSL Project Adapter 实例。U24 属于 `observational`；U25 属于 `action/closed_loop`，因此不能复用 U24 的 observational runner。P01 的 contract/adapter PASS 但 fork-replay 和 action effect 不可观测时，应保持 `DEFERRED_ARCHITECTURE`，而不是进入 Sandbox。

B002 与 B003 的 U24 结果属于同一 exact contract；B003 的主要新增价值是治理链复核，而不是新的方法学证据。下一批不得继续重复 U24 微变体，也不得把 Logistic/MLP 的 exact-domain `ADVANCE_SPECIFIC` 扩展成方法族结论。

canonical state reconciliation 已完成，当前机器状态指向 B003。当前 Scout 是 P03/U19：CSI_NONE 接口合同已闭合，但尚未形成 residual headroom 研究证据或 Sandbox 资格。下一唯一合法动作是 P03 residual headroom probe；在其退出前暂停新增候选、B004、ML 训练和流程扩展。

## 9. 未来 skill 化要求

当前文件是项目级规范，不是 skill。稳定运行若满足以下条件，再抽取成 skill：

1. Universal Core、Communications profile 和 Project Adapter 的字段边界稳定；
2. 至少三个不同机制族批次通过同一套 Scout/Sandbox/Promotion 分层；
3. state reducer、manifest、receipt、artifact pointer 和 stale 传播接口稳定；
4. 失败候选和 salvage lineage 可查询；
5. 独立压力测试证明 agent 不能靠自然语言绕过硬门；
6. 项目专属字段与通用治理字段已解耦。

skill 只负责导航、检查和调用入口；真正的允许/阻断必须继续由脚本和状态机执行。
