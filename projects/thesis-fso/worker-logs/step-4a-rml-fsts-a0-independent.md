# RML-FSTS A0 independent audit

## Verdict

`ALLOW_SEMANTIC_SMOKE`

限定语：这只允许先完成一个以证伪为目的、无 C1 的 semantic smoke；不等于 A0 已对方法可行性判 PASS，更不允许进入 bounded MVE。当前 testbed readiness=`NEEDS_ADAPTER`：第一次运行前必须冻结合法 `B_L` 网格、论文数值功率点、CFO-MSE regret 的分母/数值地板，并证明同一 realization 可在所有 action 上配对重放。上述均是可修复的本地适配；若任一项无法闭合，应转 `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`，不能把无效 testbed 当成科学 Kill。

## §0 Legal problem

### 合法性结论

Q1 是合法但尚未证实的研究问题，可以进入 A0 的“最快证伪”切片：

| 判据 | 审计结论 | 证据语义 |
|---|---|---|
| 具体 M-C-A | PASS：M 是 Wang/Enhanced fixed-`B_L` FSTS；C 固定 PM-4/16QAM、320-symbol TS 与 receiver-power bin，再改变 receiver-visible condition；A 是固定 action 的最优值/排序可能改变并产生 regret | FACT：M 与固定参数存在；INFERENCE：condition 会改变 ranking |
| 可复用产出 | PASS：若假设成立，产出可以是受条件约束的 design rule/performance-curve family；当前不把它写成 controller | INFERENCE |
| 近期 baseline | PASS：Wang 2023 是 source M，Enhanced 2024 是 task-matched comparator；Morelli/Yu 只限制 generic multi-lag/stepwise prior-art ceiling | FACT |
| 可量化 | PASS：CFO MSE、outage/BER、range 与 complexity 均可量化；但本轮可立即执行的首要 gate 只能是校准后的 CFO MSE，outage 事件尚未定义 | FACT + UNKNOWN |

必须保持三层语义分离：

- **FACT**：Wang 的 fixed `B_L` 存在 precision/range trade-off；论文设置随 modulation/training length 采用不同 `B_L`，低功率下 FS/FOE 退化。
- **INFERENCE**：在同一 B2 key 内，turbulence/branch/phase reliability 可能改变 action ranking。
- **UNKNOWN**：target crossover 是否存在、B2 后是否仍有 `>=20%` CFO-MSE regret 或 `>=10 pp` outage regret、该残差是否可由 action 前的 receiver estimate 观测。

对 deterministic selector 的 A0 翻译是：性能空间由 `B2→O1` gap 实测，不套 ML/MDP；simple-prior coverage 由 B2 直接承担；Morelli/Yu 与 SSRN 债务限制 claim，不替代 target test。由于 gap 仍是 UNKNOWN，本结论只放行 smoke，不放行方法或 MVE。

## §1 Method identity/action space

所有对象必须共享同一 FSTS estimator、预处理、训练长度、action set 与输出 metric；差别只能是如何选择单个 `B_L`（及与其合法绑定的 `B_N`）。

| 对象 | 可用输入 | action | 输出 | 对手角色 |
|---|---|---|---|---|
| **B0 paper fixed** | modulation、TS config；论文固定参数 | 论文 preset：320-symbol PM-4QAM `(B_N,B_L)=(16,20)`，PM-16QAM `(8,40)` | 标准 FSTS frame/CFO estimate 与 metric | source baseline；必须先复现其趋势，但不是唯一 Go 对手 |
| **B1 dev-global fixed** | dev set 的 aggregate metric；test 时不读 condition | 在预冻结合法网格中选一个 dev-optimal fixed action（每个 waveform/TS family 冻结一次） | 同 B0 | 排除“论文参数没调好”解释 |
| **B2 conditioned single-lag lookup** | 仅 modulation、TS length、dev-frozen receiver-power bin；test 时只读同名已知/估计量 | 每个 key 选一个 single lag，表与 bin 在 dev 后冻结 | 同 B0 | **最强廉价、合法传统 Go comparator**；任何只跨这些 key 的 crossover 都算被 B2 吸收 |
| **O1 truth/oracle** | post-hoc ground truth 与所有 action 的 test outcome | 同一网格内选 cell-wise truth-best action；不得进入运行时 decide path | headroom/regret 上界 | 仅作 headroom/Kill；O1 gap 大不构成 Go |
| **C1 future receiver-visible selector** | 只允许 action 前、因果可得的 receiver estimate | 从与 B0–O1 完全相同的网格选一个 action | 同一 FSTS 输出，另记录选择开销 | 当前不存在、不得构造；只有 B2 后 residual 稳定、可观测、可行动时才可进入 bounded MVE |

O1 首轮应采用 **cell-wise expected-metric oracle**，而非 per-realization hindsight winner；后者会把噪声择优也算作 headroom，容易虚高。若另报 per-realization oracle，只能列为更松的诊断上界，不能承载 20% gate。

## §2 Deployable information boundary

| 类别 | 可用项 | 禁止/注意 |
|---|---|---|
| online known | modulation、TS length、protocol/frame geometry、已配置 branch count、候选 action grid | 这些量若被用于 B2，必须在 dev/test 一致且 test 前冻结 |
| receiver-estimated | action 前从同一 TS 因果得到的 received-power/SNR proxy、branch energy/reliability、粗相关质量或粗 CFO proxy | 必须在 lag-dependent path 之前可算；不得使用执行某个 candidate 后才出现的 error/quality |
| oracle | true CFO、true `h`/phase trajectory、`C_n^2` 标签、真实 SNR（而非 receiver estimate）、每个 action 的 MSE/outage、oracle action label | 仅用于 O1 与离线审计，任何 runtime 读取都使 C1 无效 |
| post-hoc | aggregate、paired CI、regret、ranking、failure attribution | dev 可用来冻结 B1/B2；test post-hoc 只能评价，不能回写 bins、action set 或 policy |

必须做 hidden-truth metamorphic check：接收样值和所有 deployable metadata 不变，仅改 hidden truth/标签，运行时 action 必须不变。TX payload、目标标签、seed id、future sample 与 per-action outcome 均不得进入选择接口。

## §3 Baseline ladder and fairness

1. **一次冻结**：先冻结合法 action grid、FSTS estimator、metric、功率 bin 边界、dev/test seeds、搜索预算与 stop rules；看 test 后不得增删 action 或重分 bin。
2. **同预算搜索**：B1 与每个 B2 key 扫相同 action grid、相同数量 dev realizations；B2 的额外自由度只能是合同允许的 modulation/TS/power key。O1 也只能从相同 action grid 取最优。
3. **dev/test 隔离**：B1/B2 只在 dev 冻结；crossover、regret 与 gate 只在 disjoint test 上计算。若初筛扩 seed，只能按预先写定的一次扩容规则，不得同时调参数。
4. **paired realizations**：每个 cell/seed 的 symbols、`h`、phase、noise、CFO 与 receiver-power realization 在所有 actions 间完全相同；不得让 action 循环推进 RNG。报告 raw paired rows 后再 aggregate。
5. **等任务/等约束**：所有 action 保持 TS=320、同 overhead、同 coarse stage、同 CFO range validity；若较大 `B_L` 缩小 unambiguous range到无法覆盖冻结 CFO 条件，该 action 不合法，不能用低 MSE 换任务定义。
6. **Go/Kill 分离**：Go 对手是 B2；O1 只回答“最多还有多少 headroom”。`B2≈O1` 可 Resolved/Kill，`O1≫B2` 仍不能 Go，必须先有稳定 crossover、receiver-visible observability，并在之后的 fresh bounded MVE 中由 C1 实际胜过 B2。

建议把 normalized CFO-MSE regret 预冻结为
`R_mse=(MSE_B2-MSE_O1)/max(MSE_O1, epsilon_floor)`，同时报告绝对差与 ratio；`epsilon_floor` 必须来自 estimator calibration/数值精度，不能看结果后设置。若 O1 接近 floor 导致 ratio 失真，只能用已预定义的 outage branch，不能借巨大 ratio 宣称信号。Outage 需先给出一个与下游 capture/range 对齐的事件；当前 owners 未给事件定义，因此该 branch 暂不可承重。

## §4 Physical provenance

| 条件/参数 | owner 已证 | 本轮允许 | 未证与外推限制 |
|---|---|---|---|
| modulation/rate | Wang：10 GBaud PM-4/16QAM；Enhanced：10 Gbaud QPSK/16QAM | 首烟仅 PM-4/16QAM，分别评估 | 不外推到 BPSK/其他调制 |
| TS/action anchor | Wang：320/960 symbols；320-symbol 下 PM-4QAM `(16,20)`、PM-16QAM `(8,40)` | TS 固定 320；paper action 作为 B0 | 除 paper point 外的合法 `B_L` 网格尚未在 owner 冻结；必须验证整除、fine-range 与 estimator contract |
| receiver power/SNR | Wang/Enhanced 均有 power sweep 与 low-power degradation/threshold 事实 | 只用从论文恢复的确切数值点；至少一个非 floor 点与一个 low-power 但仍可评价点 | owner 摘要没有数值范围；禁止拍 SNR、禁止只取让 crossover 出现的一端 |
| turbulence/diversity | Wang：`C_n^2=1e-16/1e-14`、1/2/4/6 branches、10 km phase-screen FSO | 可用两点作 source-backed weak/strong paired cells；首烟固定 branch count | 两点不证明连续星地分布；AO 未报告；不能把 branch count 本身伪装成不可知 condition |
| CFO | Wang：`±1.1 GHz` | 冻结同一 source-backed CFO distribution/points并对 actions 配对 | true CFO 不能进入 selector；须先确认每个 action 的合法 fine range |
| linewidth/phase | Wang Tx/LO linewidth 50 kHz；Enhanced 摘要记 80 kHz但单位文本有限 | 主 smoke 只用 50 kHz；80 kHz最多作后续敏感性 | 不能自造 AO residual/linewidth；320-symbol μs 级窗内的慢变机制必须先做时间尺度核算 |
| target transfer | Paillier 提供 20° LEO、AO+DPLL 与 fading/phase transfer physics | 只作外推约束 | 它是 BPSK/DPLL、单场景，不证明 FSTS target crossover |

物理结论：已有 provenance 足够搭一个 **source-domain falsifier**，不足以把结果称为星地 deployment 证明。若 shared testbed 不能同时承载“固定 320-symbol FSTS action 自由度”和“source-backed turbulence/power realizations”，结果只能是 testbed blocked/inconclusive，而不是 Q1 的 no-crossover Kill。

## §5 Testbed readiness

`NEEDS_ADAPTER`，不是 `READY`，也尚非硬 `BLOCKED`。

| readiness 项 | 结论 | 起飞前闭合条件 |
|---|---|---|
| 问题承载自由度 | 概念上存在：`B_L` 是 precision/range trade-off 的真实 action | 证明实现可在 TS=320 下替换至少 3 个合法 action，而非只改标签或同时改变 overhead |
| baseline failure/action alignment | 对齐：假设与 action 都是 fixed `B_L` ranking；不需要 ML/MDP | B0 必须先复现 source qualitative anchor；否则后续 crossover 无解释力 |
| named comparator | 已具备 B0/B1/B2/O1；B2 是最强廉价 comparator | 把 B2 bins、grid、dev budget 写死；不得只跑 B0/B1 |
| executable metric | CFO error/MSE 可执行；outage branch尚不可执行 | 校准 known-CFO case，冻结 MSE normalization/floor；若使用 outage，先冻结 capture/range 事件与单位 |
| paired replay | owner 尚无证据 | 同一 realization 可按 action 重放且不推进 RNG；做 hash/identity 断言 |

这四个 adapter（action validity、paper anchor、metric calibration、paired replay）全过即可运行 smoke。任何一个失败，进入 terminal 5；不能临时改物理参数“让方法有用”。

## §6 Fastest falsifier and terminal map

### 最小 smoke 切片

- **lag set**：每个 modulation 至少 3 个合法 action：paper `B_L` + 一个更小 + 一个更大、均保持 `B_N B_L=320` 并通过 fine-range 检查。两个 action 虽可观察 sign flip，却不能排除最优点在网格边界，因此不得用于 no-crossover Kill。具体相邻数值需由 action-validity adapter 冻结，当前不得臆造。
- **cells**：最小 8 cells=`2 modulation × 2 receiver-power bins × 2 source-backed turbulence levels`；TS=320、branch count、linewidth 与 CFO distribution 固定。每个 `(modulation,TS,power-bin)` 是一个 B2 key，weak/strong turbulence 构成 key 内 crossover 检验。
- **seeds**：首轮每 cell `8 dev + 16 disjoint paired test`。只有 sign flip 或 CI 触零时，按预注册规则一次扩为 `16 dev + 32 test`，不改变 grid/bins/physics；扩后仍不确定则 terminal 5，不宣 Go/Kill。
- **统计对象**：对每个 cell/action 保存 raw squared CFO error 与 outage flag；用 paired bootstrap/CI 比较 action difference。稳定 crossover 要求同一 B2 key 的两个 condition 中 pairwise difference 符号相反，且扩容后两侧 CI 均排除 0；单个 seed 的 argmin 变化不算 crossover。

### 次序与立即停止点

1. **validity/calibration**：B0 qualitative anchor、known-CFO metric、paired replay、range/overhead contract任一失败 → `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`，立即停。
2. **ranking crossover**：在每个 B2 key 内查 condition-dependent ranking。所有 key 均无稳定 reversal，且 paired CI 支持同一排序 → `STEP4A_KILL_NO_RANKING_CROSSOVER`，立即停，不构造 C1。
3. **B2 residual**：仅有 key 间（modulation/power）变化，或 B2 后 `R_mse<20%` 且 outage regret `<10 pp` → `STEP4A_RESOLVED_BY_CONDITIONED_LOOKUP`，立即停。
4. **stability**：残差只来自一个 cell/seed、metric floor、range violation 或未公平调谐 → 先按预注册扩容/修复一次；仍不能闭合 → `STEP4A_KILL_NO_STABLE_OBSERVABLE_ACTIONABLE_RESIDUAL` 或 terminal 5（取决于科学无信号还是 testbed 无效）。
5. **observability/actionability**：只有 hidden `C_n^2`/true `h`/true CFO/outcome 才能区分 oracle action，或 receiver proxy 在 action 后才可得 → `STEP4A_KILL_NO_STABLE_OBSERVABLE_ACTIONABLE_RESIDUAL`。
6. **仅当 2–5 全过**：semantic smoke 只授权 fresh-disjoint-seed bounded MVE。之后 C1 必须在相同 action set 上实际胜 B2并经独立 verifier，方可裁决 `STEP4A_GO_BOUNDED_RECEIVER_VISIBLE_CONTROLLER_SIGNAL`；smoke 本身不能给该 terminal。

## A-prime / A / B

| 维度 | 当前独立结论 | smoke 判据 |
|---|---|---|
| A′: CFO-MSE/outage | 可能存在空间，但 B2/O1 gap 仍 UNKNOWN | B2 后达到冻结门限且跨 key 内多条件/seeds 稳定 |
| A′: range/overhead/complexity | B0/B1/B2 天生廉价；任何 C1 都有额外选择成本，当前无结构优势 | 不得以牺牲 unambiguous range/overhead 换 MSE；收益必须覆盖选择成本 |
| A′: deployability | B2 只读粗粒度已知量，先验覆盖高 | residual 必须由 action 前 receiver estimate 观测，不得靠 truth |
| A: 结构优势 | **目前没有**。若差异仅由 modulation/TS/power 决定，所谓“自适应”就是查表 | 只有同一 B2 key 内的稳定、可观测 ranking reversal 才产生非查表增量的讨论资格 |

空白零假设至少有以下四个结构性原因：

1. **已被 cheap lookup 吸收**：文献中 `B_L` 差异可能只来自 modulation/TS/power。反驳方式仅是 key 内 crossover + B2 residual；否则 Resolved。
2. **320-symbol 时间窗太短**：星地/AO/轨道慢动态在 μs 级 TS 内近似常量，无法改变 lag ranking。必须用 source-backed coherence/linewidth做时间尺度核算；差多个数量级则 Kill，不调 linewidth。
3. **condition 不可在 action 前观测**：true turbulence/phase quality 只在 post-hoc 可知。只允许 causal receiver estimate；无法保留 oracle ranking 的可分性则 Kill。
4. **动作形态已有 generic prior art / 高风险全文债**：Morelli/Yu 已覆盖 multi-lag/stepwise 基本形态，SSRN 6293357 仍可能碰撞 action-level。对此没有 novelty 反驳；只把 smoke 限定为可行性证伪，保持全文债与 claim ceiling。

因此 A/B 当前没有足够依据支持“方法成立”；但也没有出现必须在 smoke 前科学 Kill 的不可修复致命信号。最便宜的正确动作是先让 B2 尽可能吸收，而不是先造 C1。

## Fatal signals

- 只出现 source condition dependence，未出现同一 B2 key 内 target ranking crossover。
- B2 吸收全部 key 间变化，或 B2 后两项 regret 门均未达。
- “增益”依赖 true SNR/`h`/`C_n^2`/CFO、TX payload、future samples、post-hoc outcome 或 test labels。
- 候选 `B_L` 改变 TS overhead、coarse stage、合法 CFO range，导致对比任务不等价。
- B0 无法复现 source qualitative anchor，或 metric/paired replay 校准失败；此时是 invalid testbed，不是科学 Kill。
- 只在一个 seed、一个异常 cell、metric floor 或人为极端物理参数出现 signal。
- 用 O1 headroom 宣 Go，或在 B2 residual/observability 之前构造 C1。
- 把 SSRN 未取全文写成“首次/无竞品”，或反过来把它当 blanket blocker 阻止最小 falsifier。

## Claim ceiling

- 本审计只声称“允许执行受门控 semantic smoke”；不声称 target fixed-lag failure、算法正确、方法信号或章节贡献。
- consistency/test PASS 只证明接口/实现与冻结合同一致，不证明 scientific correctness。
- source-backed 10/20 km FSO 与 Paillier transfer physics 不能外推为星地 FSTS crossover 已证。
- 即使 smoke 出现 crossover/O1 headroom，也不得声称 `METHOD_SIGNAL`；必须先过 B2、observability、fresh bounded MVE 与独立验证。
- SSRN 6293357 保持高风险全文债；不得声称 first/exact novelty/novelty closure。

## Evidence pointers

- `.sessions/2026-08-08-rml-fsts-groundwork/topic-index.md:13-17,38-39,67-69`：原始目标、Step 4a scope、source/target 分离、B2 不变量与当前位置。
- `.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:226-254`：D008 provisional-survivor 与 SSRN/claim ceiling。
- `.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:256-299`：D009 Q1、B0/B1/B2/O1/C1、门限、hard exits、terminal 与 deployable 禁止项。
- `.sessions/2026-08-08-rml-fsts-groundwork/verifications.md:103-128`：V005 共享 canonical/action read、blocker 分层与 provisional claim boundary。
- `projects/thesis-fso/literature_notes_rml_fsts.md:34-39,80-90`：source fact、strongest cheap alternative 与 comparator 角色。
- `projects/thesis-fso/literature_notes_rml_fsts.md:127-133`：Q1 四判据、FACT/INFERENCE/UNKNOWN 与不得越权的语义。
- `projects/thesis-fso/literature_notes_rml_fsts.md:143-161`：qualified action boundary、SSRN 高风险 UNKNOWN 与 Step 3.5 claim ceiling。
- `projects/thesis-fso/literature_notes_rml_fsts.md:165-190,193-218`：Wang/Enhanced 的 modulation、TS、`B_L`、CFO、linewidth、power/turbulence/diversity provenance。
- `projects/thesis-fso/master-state.md:36-54`：当前唯一控制桥为 Step 4a A0/testbed readiness；semantic smoke 尚未运行。
- `stages/gw-feasibility.md:32-93,95-137`：合法 Q# 前置门、simple-prior coverage、A′/A/B 与空白零假设。
- `stages/gw-feasibility.md:147-182`：FR-20 provenance、FR-21 oracle Kill-only 与 4a 决策边界。
- `thesis-lessons.md:270-331,394-469,473-570`：理论预期、物理前提/参数、量级、metric 校准、层级门控、Go/Kill 对手分离与证据指针纪律。
