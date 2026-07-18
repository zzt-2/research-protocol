# [R002] Direction Lab：基于稳固地基的批量找方向工作流设计

> 2026-07-17 起草；2026-07-18 由项目流程规范落地
> 关联：framework-evolution / 用户确认采用 Direction Lab 方向
> 状态：设计依据；项目级执行规范见 `projects/thesis-fso/direction-lab/process.md`，尚未创建新 skill

## 调研问题

如何把已有论文库、仿真基点、候选族批量探索、失败机制和历史教训组织成一套方向发现系统，同时支持从零找方向、从地基展开方法族、批量横向比较、证据复用和执行侧强制止损。

## 现状发现

- `method-family-batch-exploration` 已有正确顺序：冻结基点 → CandidateMap → BatchPlan → 共享接口批跑 → winner 晋级。
- S040/S041 已经要求按候选族推进，而不是每个微变体机械重走完整 GW。
- 项目已有论文库、全局搜索索引、read notes、统一 batch runner、fixed/PI/swap/fade/recovery 指标和大量 D/V 失败数据。
- 但 skill 只是文字指导；`.sessions/` 同时承载讨论、运行状态、验证和检索过程；baseline、参数域、源码 SHA、指标口径没有统一 ledger；没有流程级止损。因此单点正信号仍会劫持主线。

## 设计结论

### 1. 两条轨道

**Direction Lab（默认轨道）**负责发现方向，工作单位是候选族/批次：

`Anchor Audit → Candidate Universe → Batch Queue → Paired Batch → Batch Synthesis → Promotion Board`

**Deep Evidence（按需轨道）**负责证明已经晋级的族级 winner。默认采用增量证明：复用已有论文、索引、read notes 和失败记录，只补当前候选的证据缺口。旧 GW Step 1–4a 降级为高成本深度尽调模块，仅在语料不足、跨入新领域或原创性声明需要时调用。

### 2. 问题真实性门

任何候选进入 batch 前，先检查：baseline 是否正确、failure 是否在正确 baseline 上重现、failure 属于 bug/参数域/指标口径/物理机制哪一类、strongest simple baseline 与 oracle 的位置、候选要改善的具体维度。未过此门的正信号不得进入 winner 排名。

### 3. 状态机

候选状态：`SEED → MAPPED → QUEUED → PROBED → EXPANDED → SYNTHESIZED → PROMOTED`。

负向状态：`STALE_BASELINE / INVALID_PROBLEM / COLLISION / KILLED / DEFERRED / ARCHIVED`。

状态转换必须由 batch manifest、evidence ledger 和 verifier 支持，不能由自然语言 session note 单独推动。

### 4. 批次级止损

- CandidateMap 未完成前，单个候选不得占用完整证明预算。
- 连续两轮改善 <10%，或机制诊断不朝假设方向变化：停止微变体。
- 只在单 seed/单参数域有效：不得晋级。
- 正确 baseline 已接近 oracle：转分析/边界或重定义问题，不继续堆方法。
- 连续两批没有新机制：回到 Candidate Universe，向外扩一层。
- provenance 返工超过一次：暂停运行，先修 evidence ledger。
- 贡献从“新算法”缩成“场景适配/参数调优”：重新评分，不能沿原主张继续。

## 目标目录结构

运行状态放在项目目录；`.sessions/`只保留讨论、决策、里程碑和跨对话交接。

```text
projects/{project}/direction-lab/
├── README.md                  # 入口、状态定义、恢复方式
├── anchor.yaml                # 基点、baseline、参数域、源码SHA、债务
├── candidate-map.yaml         # 候选族全景；只保留摘要与状态
├── batch-queue.yaml           # 批次顺序、预算、依赖、退出条件
├── promotion-board.md         # 横向排名和晋级理由
├── evidence-ledger.jsonl      # 事实、来源、有效域、SHA、状态
├── dead-ends.yaml             # 失败机制、数字、否决范围、可复用资产
├── batches/
│   └── B###-{slug}/
│       ├── manifest.yaml      # baseline/参数/seed/指标/阈值/代码SHA
│       ├── results.json       # 机器结果
│       ├── summary.md         # 该批次唯一人读摘要
│       └── verifier.md        # 独立审查和阻断理由
├── evidence-gaps/             # 全局论文库未覆盖的增量缺口
└── archive/                   # 已完成批次只读归档
```

### 索引规则

- `README.md` 是入口索引，不复制结论。
- `candidate-map.yaml` 是候选索引，不放完整实验数字。
- `promotion-board.md` 是当前排名索引，不成为事实唯一来源。
- `evidence-ledger.jsonl` 保存事实、数字、SHA 和有效域。
- `dead-ends.yaml` 是失败机制唯一来源，其他文件只引用 ID。
- 每个 batch 只允许一个 `summary.md` 和一个 `verifier.md`，不按 seed 另建文档。
- `.sessions/` 每个实质批次最多一个 S###，不复制 runner 日志、raw JSON 和重复摘要。

### 双入口

从零：`Project Intake → Prior Asset Scan → Broad Candidate Universe → Collision Precheck → Batch Queue`。未知信息必须显式标为 UNKNOWN。

从地基：`Anchor Audit → Revalidate Baseline → Import Existing Evidence → Refresh Candidate Map → Batch Queue`。旧结果先按 baseline SHA、参数域和指标口径标为 `VALID / STALE / UNKNOWN`。

## 角色分工

- **Strategist**：生成候选族、提出机制假设、维护排序。
- **Executor**：只执行 manifest 中批准的 batch，不自行扩大范围。
- **Process Warden**：独立检查 baseline、ledger、停止条件和状态转换，可以阻断。
- **Integrator**：汇总 batch，更新 promotion board 和 dead ends。

主控不能绕过 Process Warden 的 BLOCK；若要绕过，必须形成显式 decision/scope 记录。

## 代码层对齐

Direction Lab 不只管理候选和文档；代码、配置、实验和结果必须与同一状态机绑定。当前 `projects/simulation/common` 同时存在正确 standard-CMA 与历史 current-CMA，`explore/` 又混有临时脚本、候选实现和 runner；这类结构会让 baseline 漂移和结果复用失真。因此新增以下代码契约。

### 代码职责分层

目标结构（不要求一次性搬迁旧代码，先建立映射）：

```text
projects/{project}/code/
├── simulator/                 # 信道/环境/数据生成；不含候选算法
├── baselines/                 # 正式 baseline；每个 baseline 有唯一 ID 和实现指纹
├── methods/                   # 候选族实现；按 family 分目录，不直接改 common
├── common/                    # 经过测试的无方向公共原语；禁止塞实验特例
├── experiments/               # 只负责读取 manifest、组装运行、写结果
├── verify/                    # 独立验证：等价性、退化、统计、有效域
├── results/                   # 机器结果；由 manifest 生成，不手写
└── sandbox/                   # 临时探索；必须有过期/归档状态，不能作为正式证据
```

与现有 `projects/simulation/{common,explore,simulator,tests,results,verify}` 的关系：

- 先用 registry 做逻辑映射，不立即大规模移动文件；
- `common/` 中的实现必须标注 `canonical / legacy / experimental`，legacy 不得被默认 import；
- `explore/` 只保留 sandbox 入口，晋级代码必须复制/提取到 `baselines/`、`methods/` 或 `experiments/`；
- 物理生成器、baseline、候选方法和评估器不能互相隐藏调用；
- 任何改动共享 `common/` 的实验必须先通过等价性和影响范围审查。

### 代码注册表

`anchor.yaml` 只引用 registry 中的组件 ID，不直接写模糊文件路径。每个组件至少记录：

```yaml
component_id: baseline.standard_cma.godard_z
kind: baseline                 # simulator / baseline / method / metric / runner
status: canonical              # sandbox / candidate / canonical / legacy / retired
entrypoint: projects/.../module.py:callable
source_sha256: ...
parameter_schema: ...
metric_contract: fixed_pi_swap_v1
valid_domains: [alpha4.2_beta1.4, ...]
supersedes: []
superseded_by: []
tests: [V-...]
```

baseline ID 必须区分 `standard_cma.godard_z` 与 `legacy_cma.no_z`，不能只写 `CMA`。

### 实验 manifest 是代码和方向的接口

每个 `B###/manifest.yaml` 必须同时声明：

- `direction_id / family_id / candidate_id`；
- `simulator_id`、`baseline_id`、`method_id`、`metric_contract_id`；
- 参数域及参数来源；
- seed、N、窗口、pilot/监督信息和资源预算；
- 每个组件的源码 SHA、配置 SHA、环境指纹；
- 预注册假设、primary metric、机制诊断、pass/kill 条件；
- 输出结果的 `evidence_id` 和有效域。

没有完整 manifest 的运行只能标记 `sandbox_observation`，不能进入 promotion board 或论文证据。

### 代码晋级状态

代码也走独立状态机：

`SANDBOX → CANDIDATE → CANONICAL → ARCHIVED`

- **SANDBOX**：可以快速试错，结果不可作为正式结论；
- **CANDIDATE**：接口、共享 realization、指标契约和最小测试已通过；
- **CANONICAL**：经过独立验证、源码指纹冻结，并被某个 batch manifest 正式引用；
- **ARCHIVED**：保留复现资产，但不再默认 import。

方向晋级和代码晋级相互制约：方向不能用 SANDBOX 代码晋级；代码也不能脱离 CandidateMap 成为“默认方法”。

### 代码侧自动阻断

Process Warden/脚本在运行前必须拒绝：

- manifest 的 baseline ID 与实际 import 不一致；
- legacy/no-z CMA 被当作 standard baseline；
- 参数域与 anchor 不一致但未声明 override；
- source SHA 与结果记录不一致；
- 评估器没有 fixed/PI 双口径或缺少机制诊断；
- 结果目录已有同名但不同 manifest 的文件；
- 候选方法直接修改 canonical baseline 而没有新 component ID。

这样“方向状态—代码组件—实验 manifest—结果 ledger”四者才是闭环，而不是文档和代码各自演化。

## 旧日志回审：当前设计仍遗漏的闭环

子 agent 对既有专题日志和验证记录做了只读复盘，发现以下问题不能靠现有目录设计自动解决：

### P0：唯一状态源

旧项目出现 `master-state.md`、专题 `topic-index.md`、验证记录三套状态互相落后：主状态仍指向早期 GW Step，而专题已推进到更后阶段；同一候选同时出现进行中、封锁和 PARTIAL。新系统必须有一个机器可读的 canonical snapshot，至少包含候选 ID、当前阶段、证据等级、阻断项和下一合法动作。状态冲突时必须阻断下游，而不是由 agent 自行猜测。

### P0：证据等级门控

旧记录中存在 citation API 不可用却容易被误写成“无引用”的情况，也有 5 篇直接竞品中 4 篇只有摘要级证据。新系统必须把 `source_status`、`fulltext_status`、`citation_api_status` 和 `claim_scope` 分开；摘要级或 PARTIAL 证据不得进入 Step4a 或论文素材。

### P1：provenance 与复现债务

旧验证暴露过脚本 SHA 未记录、汇总计数/分母错误、旧网格无法精确重放等问题。代码 registry 和 batch manifest 还不够，必须增加 immutable run snapshot：实际入口、源码树 SHA、配置、环境、输入数据、随机种子和输出文件清单。汇总数字必须由机器产物重算，不能接受事后手写修正。

### P1：失败/退出注册表

失败数据虽保留，但没有统一记录候选的退出原因、最后可复现配置和 reopen 条件。应建立 `failure-registry`，将 `collision / threshold_fail / provenance_fail / unavailable / invalid_problem / deferred` 作为可查询状态，并把 generic 机制撞车、结构性增量未证实等终止条件注册为可执行 Kill/Defer。

### P1：索引膨胀与重复来源

旧专题已出现重复 S 编号、同一检索在不同日期产生重复副本、raw→unique 压缩口径不一致。新系统需要 canonical evidence registry（DOI/规范化标题优先、raw/duplicate/update 分型），而不是继续增加手工索引。

### P1：方向全景与代码契约仍需显式建模

复盘还指出四项尚未落到实体文件或机器检查：

- 代码目录设计提到了 component registry，但目录树尚未包含它；应新增独立的 `component-registry.yaml`，规定 schema 版本和唯一写入者。
- 候选地图需要记录已搜/未搜角度、查询、来源、raw/unique、新增量和收敛依据，否则仍可能边摸边 Kill；应新增 `discovery-ledger.jsonl`。
- 必须加入“扫描 → 中性判读 → 全景排序 → 批次执行”硬门；在 `BOARD_READY` 前禁止 Go/Kill 排名，避免局部结果提前收敛。
- 代码 registry 还需记录依赖闭包、输入输出 shape/dtype/unit、RNG/状态契约、环境锁、API 版本、兼容矩阵和反向影响测试。

组件或证据变化后，还要沿依赖图传播 `STALE`。Kill 后不能简单丢弃资产，应保留“候选 → 组件 → 运行 → 结果”的 salvage lineage，区分可复用 baseline、方法模块、种子和纯方向结论。

这些缺口属于设计必补项，不应等到实现后再补丁式修复。

## 与旧 GW 的关系

旧 GW 不删除，也不改写成万能流程。它变成 Direction Lab 的 Deep Evidence 插件：winner 已有充分证据时走增量证明；winner 跨领域或证据稀疏时调用完整 GW；未经 batch 横向筛选的单点禁止调用完整 GW。

## 五个核心 schema（冻结草案）

### 1. `canonical-state.yaml`

唯一描述“现在在哪里、下一步允许做什么”：

```yaml
schema_version: 1
project_id:
active_candidate_ids: []
stage: ANCHOR_AUDIT | DISCOVERY | BATCHING | SYNTHESIS | PROMOTION | DEEP_EVIDENCE
evidence_level: NONE | ABSTRACT | FULLTEXT | VERIFIED_RUN | PAPER_READY
blocking_items: []
next_legal_action:
state_epoch:
updated_by:
```

它是状态权威源；`master-state.md`、`topic-index.md` 和 session note 只能由它生成摘要，不能反向覆盖它。

### 2. `component-registry.yaml`

每个 simulator、baseline、method、metric、evaluator 都必须有唯一身份：

```yaml
component_id:
kind: simulator | baseline | method | metric | evaluator
status: sandbox | candidate | canonical | legacy | archived
entrypoint:
source_sha256:
depends_on: []
io_contract: {input: [], output: []}
units: []
rng_state_contract:
environment_lock:
api_version:
tests: []
supersedes: []
superseded_by: []
```

### 3. `discovery-ledger.jsonl`

一行一个发现角度或查询：记录 `angle_id`、query、source、raw_count、unique_count、new_count、coverage_status、evidence_level 和收敛依据。只有所有角度达到 `NEUTRAL_READ`，候选板才能进入 `BOARD_READY`。

### 4. `failure-registry.yaml`

一条失败候选一条记录：

```yaml
candidate_id:
exit_code: collision | threshold_fail | provenance_fail | unavailable | invalid_problem | deferred
mechanism:
last_reproducible_run:
effective_domain:
reopen_condition:
salvaged_as: []
derived_from: []
```

### 5. `stale/salvage lineage`

结果、声明和资产都必须带 `depends_on` 与 `invalidated_by`。组件、参数、证据或环境变化时，沿依赖图传播 `STALE`；Kill 后沿 `salvaged_as` 保留可复用的 baseline、模块、seed 和分析结论。

五个 schema 的共同主键是 `project_id / candidate_id / component_id / run_id / evidence_id`，禁止用文件名或自然语言标题充当关联键。

## 实施顺序

1. 冻结本设计与术语；
2. 在一个现有项目建立最小 `direction-lab/` 目录和 schema；
3. 只读导入 CMA-fade/SOP 资产，验证 VALID/STALE 分类；
4. 将现有 batch skill 改为读取状态和 manifest；
5. 用一个小 batch 做前向压力测试；
6. 通过后推广到从零入口和其他项目；
7. 最后把稳定版打包成 skill。

## 验收标准

- CandidateMap 未完成时，任何 agent 都无法启动单点完整证明；
- baseline bug 或参数域变化会自动标 stale；
- batch 结果不读全部 session 也能恢复；
- 失败候选可按机制和有效域检索复用；
- 从零和从地基入口生成同一种状态结构；
- `.sessions/` 不再承载运行时逐步日志；
- Process Warden 能在真实压力测试中阻断一次“单点正信号劫持主线”。

## 未决问题

- schema 字段和校验脚本接口；
- 现有资产导入自动化程度；
- Process Warden 由独立 agent、脚本还是二者组合实现；
- promotion score 权重是否项目可配置。

## 对旧流程的影响

不是删除旧 GW，而是改变调用时机：先横向找 winner，再按证据缺口选择轻量证明或完整 GW。
