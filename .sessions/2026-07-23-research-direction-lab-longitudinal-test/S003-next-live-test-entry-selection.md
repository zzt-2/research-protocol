# [S003] 选择下一 live-test 入口（CP025 后恢复）

> 2026-07-29 | 长程恢复 / 入口选择 | 状态：ENTRY_SELECTED_T027_PREPARED
> 来源: fork at HEAD `266b6940`（epoch 59 / CP025 / NEXT_LIVE_TEST_SELECTION_READY）

## 目标

本轮只做一件事：在只选择（不运行）下一 live-test 入口的约束下，回答恢复三问、比较
现有可转化入口与新的 method-factory testbed，给出唯一推荐；若入口合法则生成 T027，
否则给出 blocker。本轮不运行科学实验、不重开任何关闭轴、不修改 Skill。

## 记录

### 1. 恢复三问 + recovery route check

按 `long-horizon-control.md` §Master loop step 4，三句作答：

**Q1：下一动作是否直接构造、比较、晋级或写作方法？**
否。本轮的下一动作是 *选择入口并准备 T027*（动作类 `METHOD_FACTORY_TASK_PREPARATION`
/ `PORTFOLIO_MAP`），本身不构造/比较/晋级/写作任何方法。真正的方法构造发生在 T027 被
用户中转、executor 在后续对话执行时。

**Q2：如果不是，为什么它是下一正向方法动作不可缺少的？**
因为当前 portfolio remap = `READY=0 / NEEDS_SMALL_ADAPTER=0` 且 active scientific
carrier = `NONE`。按 `method-production.md` 的硬路由，此状态下禁止串行 formalize
hypothesis-only candidate，必须走 pre-formal method factory 或战略 gate。没有这一步
入口选择，下一正向方法动作（一次合法的 factory sprint）就没有被授权的载体、共享 testbed
和已冻结的 comparator 约束。所以它是 factory 路由的必要前置，不是独立工作量。

**Q3：当前 streak 和 READY 状态是否要求方法工厂、轮换或战略 gate？**
是。CP025 后 `mission_method_delta` 历史：CP001–CP017 全 `NONE`（旧协议），T019 后
4/8 非 NONE 但 signal→formal 转化 0/2。当前无 active carrier、`READY=0 /
NEEDS_SMALL_ADAPTER=0`。`method-production.md` §"Pre-formal method factory" 的全部
四条前置同时为真 → **硬路由到 method factory 或战略升级**。无 serial formalization
的合法空间。

恢复事实（已逐文件核读）：
- foreground 块（topic-index L3–33）：epoch 59 / CP025 / lane
  `NEXT_LIVE_TEST_SELECTION_READY` / authority D034。
- mission-log 全表（44 行）：CP001–CP025 完整；RC001 为首次显式恢复收据；signal 两个
  （CP019 T020 M4、CP023 T024 G1 派生），formal 转化 0/2。
- portfolio/current.yaml：`formal_active_carrier.id=NONE`；G1 workline
  `FORMAL_LINE_CLOSED_PACKAGING_ACCEPTED`；post_equalizer_correction / cost_function /
  equalizer_paradigm 三轴 `REOPENED`；remaining_open 中 F1/F3/F4 均 blocked/unresolved，
  F2 merged to Pilot-Jones。
- state/current.yaml：`science_authorized=false`；G1 only `NONBINDING_LOCAL_DIAGNOSTIC`。
- R009：旧阶段 0/17、T019 后 4/8、formal yield 0/2；最小修订三项已完成并终验。
- profile：D005 务实路线、多挑候选、批量排跑、动笔前查历史；本轮严格在其内。

恢复模式：probing→preparing（已选定入口，T027 已就绪，等待用户中转）。
lane/gate match：PASS（恢复后仍按"选下一入口、准备 T027、不运行"）。

### 2. 现有信号能否做 promotion preflight（分支 1）

两个 diagnostic signal 的 promotion preflight 按 `method-production.md` 五项检查：

| 检查项 | M4（T020） | G1（T024 派生） |
|---|---|---|
| thesis fit / 章节角色 | 可作小方法/安全组件 | 同左 |
| direct collision / 可达必读源 | ✗ 收据闭包未闭合（私域全文/文献未闭） | ✗ 同左 |
| **真实 task-matched comparator + 最强廉价替代** | **✗ blind_affine 0.318 反而劣于 baseline μ=0.03 CMA 0.314；无真实不同的合法 comparator** | **✗ D4 comparator 是 post-CMA 恒等映射（140/140 行与基线同分）** |
| frozen estimand / claim ceiling / closure budget | ✓ seed-cluster CI 已冻结 | ✓ 同左 |
| Step 1–3/3.5/4a 能否不靠 receipt-only 链闭合 | ✗ T021–T024 即 receipt 修复链 | ✗ Phase-A 未闭 |

**两个信号的 preflight 结果相同：`STRATEGIC_GATE`。** 不是 `PROMOTION_WORKLINE_READY`。
根本共同 blocker：**collapse-recovery 这类 post-CMA z-stream 后处理，在当前局部切片上
没有一个真正不同、任务适配、已充分调谐的 receiver-visible comparator**（blind_affine
欠拟合、D4 是恒等占位）。强包装所需的新颖性收据闭包也卡在私域全文/文献可达性上
（属用户层资源）。

`STRATEGIC_GATE` 按 skill 定义需要用户层裁决（更大访问/基础设施/论文范围决定），不是
可由主线直接 bind 的 T。因此分支 1 的结论是 blocker，不是合法的可晋级入口。

> 说明：preflight 不是"再跑一遍"——T021–T024 本身就是这层 preflight 的失败实例。
> D019 终验后规则是"信号→preflight→可闭合才进 bounded formal workline"；两个信号当前
> 都不满足"可闭合"。

### 3. 候选入口比较（分支 2：新 method-factory testbed）

既然 `STRATEGIC_GATE` 非可 bind 入口，比较"哪个新 factory testbed 最可能形成可正式转化的
候选"。判据来自转化失败的教训：**任何新候选必须自带真实、不同、调谐的 comparator，
否则再产 signal 也会在 preflight 重蹈 0/2 覆辙。**

| 入口候选 | testbed 可复用 | 机制与已拒/已测 distinct | 不撞 closed axis | 自带真实不同 comparator 可行 | 合法可 bind |
|---|---|---|---|---|---|
| **A. CB1 16QAM 上频域/子带均衡族** | ✓（sprint-002 corrected μ=0.03 testbed 已验证产 signal） | ✓（sprint-001 §8 明确"未测的第六族"；非 z-only post-proc，不同 receiver 步骤） | ✓（post_equalizer/equalizer_paradigm 均 REOPENED；频域从未测） | ✓（基线仍是 tuned CMA；族内可含真正不同的频域 expert） | **✓** |
| B. CB1 上 per-symbol/时变 μ 随机梯度族 | ✓ | ✓ | ✗（会破坏 CB1 block-end/固定 μ identity parity；sprint-001 §8 注明"需 master decision 放宽 identity"） | — | ✗（需先授权放宽 identity，非本轮可 bind） |
| C. 重建 F1 高 SOP-rate testbed 做 model-based tracker | ✗（state.yaml：`F1 testbed rebuild NOT authorized`） | — | ✗（protected） | — | ✗ |
| D. F4 coded-chain soft-feedback | ✗（INFRASTRUCTURE_BLOCKED，无 FEC 链） | — | ✗ | — | ✗ |
| E. 再做一次 z-only post-proc 批次（如 M4 续包） | ✓ | ✗（与已测 z-only 同族；CB1 z-only 线 T019/T020 已尽，M4 已登记 Q15 又于 T023 失败） | 边缘 | ✗（同 comparator 缺陷） | ✗ |

**唯一合法且最可能形成可转化候选：入口 A**——在已验证的 CB1 16QAM testbed（corrected
μ=0.03 baseline、共享 realization/seed 集）上，对**频域/子带均衡这一机制不同族**做一次
bounded method-factory sprint，且**强制批次内含真实、任务适配、已调谐的 comparator**
（把"转化 blocker = 无真实不同 comparator"直接变成 factory 内的可闭合条件）。

为什么 A 优于其他：它复用一个**已被证明能产 signal** 的 testbed（M4 在此产过
`DIAGNOSTIC_METHOD_SIGNAL`），又落在 portfolio 明示 `REOPENED` 且**从未测过**的机制
轴（频域），还不破坏任何 identity parity，并把 preflight 的硬 blocker 直接内化为
factory 的 comparator 要求。即"signal 产得出"与"signal 带得走 comparator"在同一 sprint
里同时具备。

### 4. 唯一推荐

**推荐入口 A。生成 T027 = 一个 bounded pre-formal method-factory sprint 的任务简报**
（动作类 `METHOD_FACTORY_TASK_PREPARATION`，仅准备；executor 后续对话执行）。

T027 硬约束（详见 T027 文件）：
1. 复用 sprint-002 的 corrected μ=0.03 CB1 testbed、共享 realization 与 fresh disjoint
   seed 集，不新建基础设施、不改 common/params.py。
2. 目标族 = **频域/子带均衡**（sprint-001 §8 未测的第六族）；与已测 5 个 z-only post-proc
   构造及 M1–M4 逐条 dedup。
3. 批次内**必须**含至少一个真实、不同、已调谐的 receiver-visible comparator（非
   blind_affine、非恒等占位），使任何 signal 自带满足 preflight 的 comparator。
4. 严格 prefix-only 因果；identity smoke 与方法构造同包；claim ceiling =
   `DIAGNOSTIC_METHOD_SIGNAL`/`NO_DIAGNOSTIC_SIGNAL`，不得写论文/Go-Kill/自动晋级。
5. 无 signal 则记 `NO_DIAGNOSTIC_SIGNAL` 并 harvest/轮换；signal 则回 Step 1–3/3.5/4a，
   不在本轮晋级。

未达上述任一项（尤其 comparator 要点）→ executor 视为 `BLOCKED_SHARED_TESTBED` 或
退回，不强行收尾。

### 5. 范围与门控确认

- 本轮动作（选入口 + 写 T027 + 更新 topic-index/mission-log）全部在
  `allowed_actions`（RECOVER / TASK_PREPARATION / PORTFOLIO_MAP /
  METHOD_FACTORY_TASK_PREPARATION）内。
- 未触发任何 `forbidden_actions`：未运行科学实验、未重开 G1/Q15/B1/A4/B10/B9/B12/
  science-scout、未修改 Skill、未 protected-history edit。
- 未进 Step 5/Contract/Execute，未把诊断/包装冒充正式方法。
- 未开新专题（`_registry.yaml` 已查重：续 `2026-07-23-research-direction-lab-longitudinal-test`）。

## 决策引用

- D034：接收 T026、压缩 current snapshot、下一 live-test 以 signal→formal 转化为毕业判据（既有）
- 无新建 D###：本轮为入口选择，preflight 结论 `STRATEGIC_GATE` 是既有规则的直接应用，
  无新架构决策；factory 硬路由依据 `method-production.md` 既有规则。
- 触发原话：无（技术推导 + 既有恢复指令）

## 范围确认

- 本轮是否在 scope boundary 内：是。当前范围明确含"选择能验证 signal→formal 转化的
  下一 live-test 入口，再生成 T027"。

## 后续

- 用户中转 T027 → executor 在新对话执行 sprint-003（diagnostic only）。
- 收尾：本轮只提交 S003 + T027 + topic-index/mission-log 更新。
- 若 sprint-003 仍无 signal 或仍无真实不同 comparator → 触发战略 gate 升级（私域全文/
  论文范围决策），届时交用户，不在主线强行推。
