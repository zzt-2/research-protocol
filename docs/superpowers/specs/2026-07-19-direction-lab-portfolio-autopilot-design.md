# Direction Lab Portfolio Autopilot 设计

> 日期：2026-07-19
> 状态：设计待实现；不授予新实验、B004、ML 训练或正式研究晋级权限
> 适用：Direction Lab 的跨批次持续探索控制面

## 1. 背景与问题

Direction Lab 已经具备 Candidate Universe/Map、BatchPlan、Scout/Sandbox/Promotion 分层、执行 receipt、source closure、EvidenceGate、claim-scope 五级结论门和 Sandbox canonical reducer。它能较可靠地证明“某一批运行是否真实、某一局部结论能否入账”。

但现有控制面仍以单候选闭环为中心。候选出现 `LOCAL_NEGATIVE`、`INFRASTRUCTURE_BLOCKED`、critic FAIL 或局部正信号后，流程经常把“下一方向选什么”交回用户；于是局部事件被误当成整轮终点。频繁停顿导致三个后果：

1. 一次只推进一个窄点，无法检验候选池的相对价值；
2. 用户必须在很久后发现覆盖不足、错误外推或钻牛角尖；
3. 大量时间花在补单候选治理接口，而不是获得跨机制的新信息。

根因不是门不够多，而是缺少一个组合级调度器：现有门保护证据和历史，却没有机器负责“失败后自动换谁、组合是否覆盖够、什么时候才真的可以停”。

## 2. 目标与非目标

### 2.1 目标

- 从冻结 anchor 和完整 CandidateMap 出发，连续推进一个候选组合，而不是单候选。
- 首轮 shadow campaign 至少完成 6 个有效批次，并覆盖至少 3 个不同机制族。
- 启动前证明冻结的候选组合不是偏窄子集，且预算足以支持 6 个科学批次和 3 个机制族。
- 达到上述下限前，单批失败、局部阻断、critic 退回或局部正信号不得触发用户方向拍板。
- 将 provenance 审查与科学推理审查分开，避免“复算正确”被误当成“结论合理”。
- 让 AI 自主完成候选归并、代表点设计、排序、诊断和换族；脚本只约束不可逆错误、预算失衡和错误外推。
- 用有界状态和少量权威入口支持上下文恢复，避免文档随批次失控膨胀。

### 2.2 非目标

- 不替代 Groundwork、Contract、Execute 或正式论文证据链。
- 不接管具体 runner、EvidenceGate、claim-scope validator 或 Sandbox canonical reducer。
- 不把 Communications 的 BER、MDE、调制、CSI 等语义写入通用 campaign schema。
- 不建设通用 DAG、插件系统、签名 registry、统一 runner 基类或自动文献全流程。
- 不在本设计阶段启动 B004、训练 ML、扩展仿真域或修改历史批次。

## 3. 设计原则

1. **组合级而非候选级终止**：候选结论是 campaign 事件，不是默认停机点。
2. **工作守恒**：只要存在合法 runnable 候选，调度器必须给出下一动作。
3. **科学自由、边界硬门**：AI 决定怎么研究；脚本决定哪些状态迁移和结论升级不允许。
4. **已有 owner 优先**：CandidateMap、BatchPlan、EvidenceGate、claim-scope 和 canonical 各自保持唯一职责。
5. **原始证据不因 critic 失败而消失**：退回的是解释或晋级，不是运行事实。
6. **状态可重建、摘要有界**：append-only event 是事实源，state 是 reducer 投影，raw artifact 留在原批次目录。
7. **先 shadow 后 skill**：先证明长跑行为稳定，再把导航和检查抽成 skill；强门始终留在脚本。

## 4. 分层架构

```text
Candidate Universe / CandidateMap / BatchPlan
                     │
                     ▼
           Portfolio Autopilot
      campaign contract + scheduler
                     │
          选择下一批及预算，而非运行算法
                     ▼
       Existing batch-specific runner/gate
     Scout gate / Atlas gate / Sandbox controller
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
 Evidence verifier        Science critic
 provenance/hash          inference/units/scope
          └──────────┬──────────┘
                     ▼
      campaign event + automatic rotation
                     │
       existing Sandbox completion reducer
       （仅在原流程允许时独立更新 canonical）
```

Portfolio Autopilot 是独立的组合级调度层。它消费已有 map/plan 和两类审查 receipt，只记录“这一批对组合意味着什么、下一步是谁”，不调用 P03 内部 token、不解释 BER、不写 canonical 或 master-state。

## 5. 最小文件模型

每次长跑建立一个不可变 campaign 目录：

```text
projects/<project>/direction-lab/campaigns/C###-slug/
├── campaign.yaml       # 冻结合同
├── events.jsonl        # append-only 事实源
├── state.yaml          # reducer 可重建投影
└── batches/
    └── <batch-id>.yaml # 薄摘要：指针、receipt、组合级处置
```

代码第一版只新增：

```text
projects/<project>/direction-lab/tools/campaignctl.py
projects/<project>/direction-lab/tests/test_campaignctl.py
```

### 5.1 `campaign.yaml`

冻结以下内容：

- campaign ID、anchor/map/plan 的内容 hash；
- portfolio-scope preflight receipt：Universe/Map 覆盖、机制族 taxonomy、已知反例/被阻轴和 runnable 数；
- 候选与机制族初始组合；
- `min_valid_batches: 6`；
- `min_evidence_families: 3`；
- 时间/算力预算；
- 首轮单机制族预算份额 30% 软警戒，以及首次覆盖前同族最多 2 个有效批次的硬门；
- 每 2 个有效科学批次重排一次；
- capability 投资规则；
- 允许的全局停止原因；
- evidence verifier 与 science critic 的 receipt schema/version。

`preflight` 必须校验预注册时间/算力预算按各批上界足以完成至少 6 个科学批次和 3 个机制族；不足则 campaign 不能启动，不能把明知过小的预算用作日后早停理由。Portfolio-scope receipt 只消费 Candidate Universe/Map 及其现有 validator 的内容寻址结果，不在 campaign 内复制候选或领域 taxonomy。

合同不复制候选数据库、领域指标或五级 verdict，只保存其内容寻址引用。改变 anchor、指标含义、研究范围或全局预算，必须产生新的 campaign revision；不能静默改写原合同。

### 5.2 `events.jsonl`

每条事件至少含：

`event_id | campaign_id | expected_head | type | batch_id | candidate_id | family_id | scientific_question_id | artifact_hash | assessment_hash | disposition | information_code | pointers | timestamp`

admitted-batch event 必须内含 reducer 所需的上述规范化事实；pointer 只用于追溯详细 receipt，不得让 reducer 依赖可变外部摘要。事件使用 compare-and-append：`expected_head` 不匹配即拒绝，防止 replay、并发漂移和上下文恢复后重复入账。逐 cell 结果不写入这里。

### 5.3 `state.yaml`

只保存：

- 有效批次数、证据型机制族覆盖数；
- 各候选/机制族已用预算和连续占用；
- runnable/deferred/blocked/local-killed 队列；
- 最近两批获得的新机制信息；
- 待修复 synthesis；
- 当前 `next_action` 及其机器理由；
- 全局停止条件的逐项满足情况。

它不保存 raw result、BER 表、全文审查报告或 canonical 状态。删除后应能从 `campaign.yaml + events.jsonl` 字节级重建。

### 5.4 批次薄摘要

每个批次最多一个机器可读摘要，包含：

- 原 batch artifact/manifest/receipt 指针；
- evidence verifier receipt；
- science critic 的 PRE/POST 两份 receipt（或固定二元素数组）；
- `ADVANCE | KILL_LOCAL | BLOCKED | DEFER` 之一；
- 获得的新机制信息与对候选排序的影响；
- 不超过一项低成本修复建议。

完整结果、逐 cell 数据和复算证据仍留在原 runner 的 artifact 目录；session 只记里程碑，不复制数字。

## 6. 有效批次与覆盖计数

“跑了一个脚本”不自动算一个有效批次。计数必须同时满足：

1. 有独立且预注册的科学问题；
2. 消费合法 runner/gate 的真实 artifact；
3. evidence verifier 完成；
4. science critic 给出可机读处置；
5. 结果被 append 到 campaign events。

每个有效批次必须有不可变 `scientific_question_id`，由以下字段的规范化 hash 生成：

`hypothesis | mechanism_delta | data_scope | comparator_contract | estimand_contract`

`record` 必须同时对 `scientific_question_id`、artifact hash 和 assessment hash 去重；science critic 还要声明该问题与已计数批次 `distinct_from`。同一 artifact 换 batch ID、同一问题拆成多个参数文件、或只改无机制意义参数，均不得重复计数。

Capability-only 批次可以记入基础设施预算，但不计入 `min_valid_batches` 或 `min_evidence_families`。一个机制族只有至少一个有效科学批次才算覆盖。

首轮 6 批约束按整数执行：在首次覆盖 3 个机制族前，同一机制族最多占 2 个有效批次。30% 是按预注册 compute/time cost 计算的 rebalancing 软警戒，因为 3 个机制族均分本身约为 33.3%；超过警戒必须解释和降权，但不制造数学上不可满足的硬门。

## 7. 调度状态机

### 7.1 批次处置

- `ADVANCE`：保留正信号和后续验证需求；若 campaign 下限未满足，轮换到另一机制族，不因正信号提前深挖。
- `KILL_LOCAL`：关闭具体 cell/slice/机制合同；保留 raw evidence，自动选择下一 runnable 候选。
- `BLOCKED`：记录缺失 capability 和影响范围；若存在其他 runnable 候选，立即轮换。
- `DEFER`：收益/成本不足或依赖未到位；回队列但不占当前执行位。

critic FAIL 不直接成为第五种科学结论：

- 可低成本修复且不改变结果含义：标 `NEEDS_REPAIR`，同一批最多修一次；
- 修复仍失败或需改研究合同：转 `DEFER` 或 `KILL_LOCAL`，调度器继续；
- provenance 失败但 raw artifact 可隔离：拒绝入账并轮换；
- 历史保护/P0 安全失败：进入全局停止审查。

### 7.2 `next_action`

调度器每次必须返回一个显式动作：

`RUN_BATCH | REPAIR_ONCE | BUILD_SHARED_CAPABILITY | REBALANCE | CLOSE_CAMPAIGN`

选择顺序：

1. 若到达两批边界，先 `REBALANCE`；
2. 从未达到最小族覆盖且预算可承受的 runnable 族中选择信息增益最高者；
3. 再按复用程度、机制可观测性、成本、失败也能获得的信息、撞车风险排序；
4. 无 runnable 候选时，评估共享 capability；
5. capability 不值得投资时，分类所有 blocker 并检查全局停止门；
6. 未满足停止门却无动作，视为控制器错误，不允许自然语言结束。

具体排序由 AI 给出并写入事件；脚本只校验预算、轮换、依赖和停止合法性。

## 8. 共享 Capability 投资

缺少 16QAM、coded output、state replay 等能力不应自动触发停机，也不应为一个候选无限建设基础设施。

只有同时满足以下条件，调度器才可选择 `BUILD_SHARED_CAPABILITY`：

- 明确服务至少 2 个候选，且最好跨 2 个机制族；
- 预计成本小于分别为这些候选独建两次的总成本；
- 不改 canonical baseline 的科学含义；
- 有非性能 smoke、接口退出条件和独立审查计划；
- 位于 campaign 的 capability 预算内。

否则该候选 `DEFER`，继续其他 runnable 方向。首轮 shadow 在完成 6 个有效科学批次之前，capability-only 工作最多插入 2 个执行单元；它们不占 6 个有效科学批次，也不满足机制族覆盖下限。

## 9. 双审查

### 9.1 Evidence verifier

复用现有执行与证据门，审查：

- manifest/source closure/result hash；
- baseline/component 身份；
- deterministic rerun 或规定的复现证据；
- receipt replay/stale/history protection；
- artifact pointer 是否真实存在。

### 9.2 Science critic

必须使用与实现者不同的 agent/context，分运行前和运行后两次审查。context ID 由调度运行时注入，不接受 reviewer 自填字符串；receipt 中的 implementer、evidence verifier 和 science reviewer context ID 必须满足设计声明的独立性约束，缺失、伪造或应分离的身份相等时不得 PASS，并必须有反例测试。

运行前检查：

- estimand、单位、分母、sample unit；
- 不确定性、MDE/power 或 zero-event 上界；
- comparator/oracle 的信息量与部署身份；
- 代表轴、已知反例和 scope certificate 计划；
- advance/kill 条件是否会把局部证据外推。

运行后检查：

- 结果与预注册统计量是否同量纲；
- 正/负信号是否可能来自 baseline bug、伪标签、选择偏差或灵敏度不足；
- 结论层级是否超过 artifact 支持范围；
- 历史反例是否被处理；
- 是否真的获得新的机制信息。

Science critic 的 receipt 至少包含：

`review_id | phase(PRE/POST) | implementer_context_id | reviewer_context_id | subject_hash(contract/artifact) | assessment_hash | verdict | repairable | claim_ceiling | comparator_info_contract | deployability | historical_counterexample_disposition | objections(code/severity/evidence) | distinct_from`

它不能修改 raw result。缺少相应 Domain Profile/Project Adapter validator 或 validator receipt 时只能 `DEFER`，不得凭自由文本 PASS。`FAIL` 只阻止 synthesis/晋级；除全局 P0 外，不阻止调度器换到下一批。

## 10. 类型化科学证据

Campaign 不重定义通信指标。以下规则只是下游 receipt admission invariants；估计量、单位、zero-headroom、统计灵敏度与结论层级的具体语义仍由 `profiles/`、Project Adapter 和 `validate_claim_scope.py` 唯一定义。每个进入 science critic 的关键统计量必须声明：

`estimand | unit | numerator | denominator | sample_unit | uncertainty | tested_scope | claim_level`

强门拒绝：

- 比较双方 estimand 或单位不一致；
- cell 数、seed 数、symbol 数混作同一分母；
- zero event 被表述为“完美”而无置信上界；
- oracle/scoring-only 结果被当作 deployable 方法；
- CELL/SLICE 证据直接更新 DOMAIN/CANDIDATE/FAMILY；
- 未满足统计灵敏度却给出 terminal negative。

具体 BER/FER/GMI/MDE 解释仍由 `profiles/communications.yaml` 和 Project Adapter 拥有；campaign 只检查声明齐全和 receipt 是否来自现有 validator。

## 11. 全局停止权

### 11.1 允许停止

生产 campaign 的 `CLOSE_CAMPAIGN` 仅在以下任一情况成立：

1. 已达到最小批次/族覆盖，且同时满足预注册的组合饱和、候选穷尽或预算终点；
2. 全部 runnable 候选已局部处置，所有 blocker 已分类，且没有满足投资规则的共享 capability；
3. 已通过 preflight 证明足够的预注册时间或算力预算实际耗尽；
4. 发生无法安全绕开的历史保护/P0 证据完整性失败；
5. 下一步必须改变研究边界、canonical baseline 含义或进行超出 campaign 预算的大型基础设施投资。

第 2、3、5 项若在 6批/3族前触发，必须提供 `PORTFOLIO_EXHAUSTION_CERTIFICATE`。证书必须绑定 frozen map hash，由独立 science critic PASS，并让脚本逐个核对 map 中每个候选的 blocker receipt、替代路线、共享 capability 判定和覆盖状态；缺一项即不得早停。它不是让用户选下一个候选，而是证明当前冻结组合确已穷尽。

达到 6批/3族本身只是生产 campaign checkpoint，不自动关闭。首轮 shadow 是例外：它的唯一目标是验证治理行为，因此合同可把“6批/3族 + shadow 验收综合”定义为本次 pilot 的终点；该例外不得复制到生产 campaign。

### 11.2 不允许停止

以下均不是停机理由：

- 一个候选失败或一个 slice 没有 headroom；
- 某一轴 `INFRASTRUCTURE_BLOCKED`，但仍有其他 runnable 候选；
- Stage B 未触发；
- 一个候选出现正信号；
- science critic 拒绝某份 synthesis；
- 可安全修复的 provenance 小问题；
- 上下文将满、对话切换或定时进度汇报。

## 12. checkpoint、恢复与用户交互

- 每批完成：机器 checkpoint，更新 events/state，不询问方向。
- 每 2 个有效批次：portfolio rebalance，检查族覆盖、预算倾斜、连续无新机制信息和共享 capability 价值。
- 每 45–60 分钟：给用户一段简短进度，只报告已跑批次、当前组合健康度和下一自动动作，不请求方向拍板。
- 上下文切换：handoff 必须携带 `campaign_id + state hash + event head + next_action`。若 `next_action` 不是 `CLOSE_CAMPAIGN`，接收方应直接续跑。
- 达到 6 批/3族或合法全局停止：才给完整组合综合和需要用户决定的战略分叉。

状态恢复只需 campaign 三文件和它们引用的 receipts；不得要求新对话重读所有逐批日志才能知道下一步。

## 13. 错误处理与反循环

- 同一批最多一次低成本 repair；第二次仍失败必须轮换。
- 同一机制族连续两批没有新机制信息，强制降权并换族。
- 连续两批改善小于 10% 只能触发 rebalancing；达到 6批/3族前不能单独触发全局停止。
- 组件 fingerprint 或 anchor 漂移：现有结果标 stale，重新选择安全批次；只有无安全替代路径时才全局停。
- reducer 与 events 不一致：停止写入、重建 state；不修改旧 event 漂白历史。
- 用户中途给出范围变更：冻结当前 campaign，记录原因，以新 revision 继续；不在旧合同内偷换目标。

## 14. 首轮 Shadow Campaign

首轮只验证治理与长跑能力，不把结果自动作为论文证据。

硬约束：

- 至少 6 个有效批次；
- 至少 3 个机制族，每族至少 1 个有效科学批次；
- portfolio-scope receipt PASS，证明 Universe/Map 覆盖、族分类、历史反例和被阻轴均已纳入；
- preflight 证明预算足以覆盖 6 个科学批次和 3 族；
- 首次覆盖完成前每族最多 2 批；
- 每 2 批自动重排；
- `BLOCKED/KILL_LOCAL/critic FAIL` 后如有 runnable 候选，下一动作必须自动生成；
- 达到下限前不向用户请求方向拍板，除非命中第 11.1 节全局停止条件。
- 同一 `scientific_question_id`、artifact hash 或 assessment hash 不得重复计数。

验收指标：

| 指标 | 目标 |
|---|---|
| 用户事后纠偏次数 | 0 次 P0 范围/统计/基线纠偏 |
| 错误 terminal 次数 | 0 |
| blocked 后自动续跑率 | 100%（存在 runnable 候选时） |
| 有效批次/小时 | 记录基线，不以刷批次为目标 |
| 文档增长量/批 | 1 个薄摘要；无逐 cell Markdown |
| 新机制信息/批 | 每批必须给出至少 1 项可验证的新信息或明确局部否决 |
| 恢复一致性 | reducer 重建与 state 字节一致 |

治理结论只有 `PASS | PARTIAL | FAIL`。即使 6 批科学上全负，只要自动轮换、范围诚实、证据可复用，仍可能是治理 PASS；科学结果另行综合。

## 15. 接口与职责归属

- `direction-lab/process.md`：Portfolio Autopilot 正式生效后的流程 owner；本设计通过审查和实现 pilot 前不改写其当前规范。
- `Candidate Universe/Map`：候选事实与排序输入，不另建数据库。
- `BatchPlan/Queue/Registry`：批次计划与 Sandbox runnable 身份。
- `profiles/`：领域指标、统计解释和反模式。
- `adapters/`：项目轴、capability 和历史反例。
- `validate_claim_scope.py`：CELL→FAMILY 推理范围门。
- 现有 controller/EvidenceGate：运行真实性与可信入账。
- `state/completion-events.jsonl` + `reduce_state.py`：verified Sandbox canonical 投影。
- `campaignctl.py`：只拥有组合预算、轮换、全局停机和 campaign state。

P03 的 `atlas_gate.py` 继续是 P03 专用执行入口。Campaign 只消费其 artifact 和 receipt，不能复制、绕过或调用内部授权 token。

## 16. 最小 API 与后续实现顺序

第一版 API：

```text
validate_campaign(config, candidate_map, batch_plan)
reduce_campaign(config, events) -> state
next_action(state) -> action
append_event(event, expected_head)
admit_batch(summary_pointer, evidence_receipt, science_review)
may_stop(state) -> (allowed, reasons)
```

对外 CLI 只暴露四个动作：

```text
campaignctl preflight
campaignctl next
campaignctl record
campaignctl close
```

实现顺序应是：schema/transition 反例测试 → reducer → stop gate → receipt admission → CLI → fault injection → 6批/3族 shadow。实现计划必须另写；本设计本身不授权编码或实验。

## 17. 延后项

至少完成一次 6批/3族 shadow 并复盘后，才讨论：

- 打包为通用 skill；
- 多 campaign 并发；
- 加密签名或不可变外部 registry；
- 通用 DAG/资源调度；
- 自动文献工作流；
- 统一不同 runner 的插件接口。

这些能力在首轮没有直接缓解“局部结果导致停机”的核心问题，提前实现会再次把研究变成治理工程。
