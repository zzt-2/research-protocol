# [R004] K2 candidate-source / research-object 入口和解

> 2026-08-12 | 关联：2026-08-08-ch4-reference-method-extension / D006–D007

## 调研问题

在 Q001 以 `PROBLEM_ABSENT_OR_TOO_SMALL` 关闭后，改变 candidate source 与 research object、接受单方向 5–9 天公平比较预算，是否足以解除旧 D006 对 K2 的入口拒绝；Shayovitz–Raphaeli TCOM 2016 是否已经给出与 K2 完全相同的 input→decision→action→output？

## 发现

### 1. 旧结论与本轮纠偏

R003/D006 的事实边界继续有效：Wang TSP 2022 明确发表了 phase-unwrapping suffix-pollution defect；TCOM 2016 是高风险强邻居；当时没有宣称 exact collision。旧拒绝同时依赖 E5/E7 在 Step 1 前要求动作细节和章节形态完全冻结，以及 5–9 天超过原 7 天预算。当前 scope change 改为只保留六个入口硬门：published defect、FSO transfer 可证伪、近期 baseline、可形成完整 action、强 comparator 存在、预算可接受。动作细节与章节图表留给 Groundwork Step 1–3 闭合。

### 2. Published defect

Wang 的 estimator 使用接收幅度和由 principal argument 生成的 unwrapped phase；一次 `j` 点解缠错误会污染所有后继累计点。论文明确指出较大 `ω0`、`N` 或 `σp²` 增大 failure，并在展示 estimator 本体性能时丢弃 failed runs，否则 MSE 会很大。证据：`papers/doi/10.1109_tsp.2021.3137966/content.md:61-75,335-357,431-449`。原 estimator 在线每样本 `O(1)`、总 `O(N)`，证据：同文件 `:207-213`。

### 3. TCOM 2016 动作签名

| 字段 | Shayovitz–Raphaeli TCOM 2016 | K2 当前只冻结的研究形态 |
|---|---|---|
| input | coded MPSK samples、pilots/preamble、LDPC soft symbols | single-tone principal phases/magnitudes；FSO residual CFO + laser Wiener PN |
| hypothesis state | 每个 phase mixture component 经星座符号扩展 | 有界相邻 winding hypotheses，状态上限与固定 lag 待 Step 1–3 闭合 |
| score | posterior mixture weights | receiver-only causal likelihood/reliability；具体式未冻结 |
| merge/prune | KL/CMVM clustering，maximum order `L=1/2/3` | 必须有 bounded merge/prune；不得冒充新动作原子 |
| lag/commit | 全序列 forward/backward + decoder iterations；未报告 fixed-lag commit | 固定 lag 后提交 unwrapped prefix/sequence |
| fallback | pilot + confidence-assisted reacquisition | pilot reset/单路径 fallback 必须进 comparator；细节未冻结 |
| output | phase posterior→symbol LLR→decoded bits | unwrapped phase sequence→原 Wang ML/MAP estimator |
| complexity | 每符号 `Mγ→γ` 降阶；limited 复杂度随 `M,γ` 二次项；8PSK order-3 约 312→238 MUL/iteration | 目标是 `H≤3`、固定内存与最坏时延；须在后续形成可审计合同 |

一手证据：`papers/arxiv/1306.3693/content.md:23-53,126-138,169-189,221-247,297-323,327-367,424-433`。

### 4. Exact-collision 裁决

`NOT_EXACT_AT_ENTRY / FULL_GENERAL_CAPABILITY_SUPERSET`。TCOM 2016 已占据“多轨迹、likelihood、merge/prune、bounded order、pilot recovery”的宽泛能力与动作原子，必须作为 mandatory comparator；但它不是同一任务、同一输入依赖、同一提交时序或同一输出接口。当前可区分 delta 仅限 decoder-free single-tone estimator、固定 `H≤3`、固定 lag/内存/最坏时延和保持 Wang estimator 输出身份。该裁决只排除入口 hard collision，不是新颖性或方法成立结论。

### 5. 六个入口硬门

| 门 | 结论 | 依据 |
|---|---|---|
| published defect | PASS | Wang 2022 suffix propagation 与 failed-run exclusion |
| FSO transfer 可证伪 | PASS_INFERENCE | coherent FSO 有 residual CFO、laser linewidth/Wiener PN 与接收 I/Q；后续须把 laser PN 与 atmospheric phase 分开 |
| 近期 task baseline | PASS_AT_ENTRY | Wang 2022；Step 1 必须补 2019+ coherent optical/FSO baseline |
| 可形成完整 action | PASS_TO_STEP1 | bounded hypotheses→score/merge/prune→fixed-lag commit→unwrapped output；细节未冻结 |
| 强 comparator | PASS | full Tikhonov mixture、fixed order 2/3、original/improved unwrap、LMMSE-WPA、pilot reset |
| 预算 | PASS_BY_SCOPE_CHANGE | 单方向 fair comparison 5–9 天获接受；Step 1 本身不授权该预算支出 |

## 结论

`A_PASS_NO_FATAL_ENTRY_BLOCKER`。K2 可作为唯一对象进入新的 Groundwork Step 1；K3 与其他候选不再比较。TCOM 2016 是 mandatory full-general comparator，不因强邻居身份预杀，也不允许将其已占的动作原子包装成新颖性。

## 对决策的影响

建立 D007，取代 D006 对“当前没有入口”的 operational terminal，但不改写 D006 的历史事实和当时门槛。若 registry 查重无冲突，则创建唯一 `2026-08-12-multi-hypothesis-phase-unwrapping` 专题并只执行 Step 1。
