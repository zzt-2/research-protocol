# Step 089 — C1 A0 revised preflight fresh re-verifier

> 2026-08-10 | T043 / CP010 / epoch 10 | fresh-context re-verifier  
> control receipt：`validate_task_control.py T043...` fresh 返回 `PASS`；action=`FEASIBILITY_A0`。  
> scope：只读科学/预算审查中央报告、framework、step-081/085–088、owner、执行源码与本地全文；不替主线程修中央报告、治理或代码。  
> no-experiment receipt：未运行 web/search/download、adapter、defect smoke、MVE、仿真、科学实验、代码实现、commit 或 push。

## 1. Verdict

**FAIL；P0/P1/P2=`0/3/0`。**

step-088 的旧 P1-2（三路 test-time `B2*` envelope 与单-B2 BOM 冲突）已按“唯一 dev-frozen primary + 其余只约束 claim ceiling”实质关闭；但旧 P1-1 仍未关闭：修订版虽补了数值阈值，却仍缺受控层 maximum exposure/分层合取规则，D0.6 也没有可执行的 selection/rejection function。另有两项独立 P1：`S_RX` 在 square-16QAM 下因旋转对称性恒定 tie，不能承担公平 receiver-only 增量对手；`B2_PRIMARY` 的 source-native 输入/front-end、pilot 插入、`sigma_e^2` 与 `(M,N)` grid 未闭合。

Disposition：**维持 CP010 等待修复**；`D0_EXECUTION_AUTHORIZED=NO`、`STEP4A_GO=NO`、`METHOD_SIGNAL=NONE`。

## 2. Step-088 closure

| step-088 finding | Verdict | 可复核证据 |
|---|---|---|
| P1-1：D0 acceptance functions 不定量、不 fail-closed | **OPEN** | 中央报告 `:252-278` 已补 event/metric/effect/CI/terminal，但 `:256,262,266` 未冻结 controlled twins/diagnostic 的 seed×cell×injection maximum exposure，也未规定 natural 与 controlled 是两层均须过、哪层承重或如何合取；`:276,278` 要求 false-action/rejection/fallback，却同时声明 D0 不授权 trigger/selection/fallback，未给 `score→accept/reject/no-op` 函数。另有 cluster unit 与 frame-binomial CI、双偏振 slip ownership 未闭合，详见 P1-1。 |
| P1-2：三路 B2 envelope 与 6.50 日单-B2 BOM 冲突 | **CLOSED（原问题）** | 中央报告 `:115-128` 冻结唯一 `B2_PRIMARY=OFC2017_LIKE_PILOT_4STATE_SOFT_LLR`，明确禁止 test-time best-of；`:212-233` 改为 D0 3.50d + post-D0 3.00d + contingency 0.50d = 7.00d point estimate，并保留 preflight blocker。该旧冲突不再存在；但 primary 自身尚未 source-faithful/executable，形成新的 P1-3。 |

## 3. Requirement matrix

| Requirement | Verdict | Fresh evidence / reason |
|---|---|---|
| A0 §0 合法问题 | PASS | `literature_notes_coded_decoder_feedback.md:80-91` 固定 Q1 与四判据 4/4；中央报告 `:45-56` 未把空白当问题。 |
| A0 §1 headroom / FR-21 | PASS | `:58-92` 只确认 noiseless uncoded structural residual；coded FER/post-BER/goodput 保持 UNKNOWN，O1 明确 Kill-only。 |
| A0 §2 simple-method sufficiency | PASS（分析层） | `:98-104` 保留 `WARNING_SIMPLE_METHOD_MAY_SUFFICE`；没有伪造 ML 必要性。可执行 B2/receiver-only 对手缺口另见 P1-2/P1-3。 |
| A0 §3 相邻先例 | PASS | `:101,106-113` 同时保留成功先例与 crowding/negative ceiling。 |
| A0 §4 finite-search triviality | PASS | `:102,169` 明确 MDP=N/A、simple scan/DP 等价即 `METHOD_DELTA=NONE`。 |
| A0 §5 负面证据 | PASS | `:103,108-113` 保留 ICTON oscillation、rare/absent defect、FEC/B2 absorption。 |
| A0 §6 prior coverage | **FAIL（执行合同）** | 90/95 语义和 affected-CW FER 公式正确，但 `B2_PRIMARY` 未形成 source-faithful runnable contract，且 D0.5 的 receiver-only comparator 为退化 tie，无法证明 decoder evidence 相对合法简单先验的信息增量。 |
| A′ 竞争维度 | PASS（claim ceiling） | `:138-151` 分离 FER、goodput、calls/latency、clean safety、localization 与 overhead；没有把任一维度写成贡献。 |
| A：结构优势 | PASS（限定） | `:153-171` 只确认相对 single-global B1 的 uncoded action增量；相对 enhanced B2 仍 UNKNOWN。 |
| B：novelty / feasibility | PASS | `:173-195` 保留 bounded-slice ceiling与 R1–R4 falsifier，不升级 novelty closure。 |
| physical：natural / controlled | 语义 PASS / 合同 FAIL | `:199-204` 正确分离自然 occurrence 与 controlled injection，禁止 turbulence→slip；但 D0.1 的双偏振 event ownership、cluster CI 与两层合取规则未闭合。 |
| truth / restart / ICTON | PASS | `:206-210,270,275-278` 隔离 TruthView，changed CW full restart，一次 frozen evidence、每候选独立重启；未复用旧 state 或 recursive feedback。 |
| B2 primary identity | **FAIL** | `:119-128,246` 抓住 pilot→4-state→LLR→one-way LDPC 和 no-best-of，但遗漏 source-required `sigma_e^2`、source-native fourth-power CPE caller；`(M,N)` grid 与全文不符，pilot 如何进入固定 6144 coded-data frame 也未冻结。 |
| D0.0–D0.6 fail-closed | **FAIL** | 数值门显著改善，但 controlled maximum exposure/stratum aggregation、D0.6 selection/rejection function、cluster-valid occurrence CI 未闭合。 |
| coverage / comparator fairness | **FAIL** | coverage 只用于 affected-CW FER且资源指标分离是 PASS；`S_RX` rotationally invariant tie 使 observability baseline 不公平，故 coverage/observability package仍 FAIL。 |
| 7.00 日 BOM | 算术 PASS / 内容 FAIL | `3.50+3.00+0.50=7.00`，point-estimate/preflight-pending 标签诚实；但 B2 source adaptation、pilot insertion/statistic estimation 和 controlled exposure 未能映射到可验收工项，不能裁 `POINT_ESTIMATE_COHERENT`。 |
| 审查历史 / 当前授权 | PASS | `:327-331` 如实保留 step-088 `FAIL 0/2/0`；`:320-325` 仍为 `D0_EXECUTION_AUTHORIZED=NO`，须新 D/V/CP。 |

## 4. Fact spot-checks

以下 24 项均 fresh 回源；不只检查中央报告自洽性。

| # | Claim checked | Verdict | Fresh source / derivation |
|---:|---|---|---|
| 1 | T043 绑定 epoch10/CP010/FEASIBILITY_A0 | PASS | fresh `validate_task_control.py` 返回 `PASS`；T043 control block 与 topic-index 一致。 |
| 2 | authority owner 当前是 GW Step4a A0，实验禁止 | PASS | `projects/thesis-fso/master-state.md:38-47`；topic-index foreground block。 |
| 3 | Q1 canonical 四判据 4/4 | PASS | `literature_notes_coded_decoder_feedback.md:80-91`。 |
| 4 | Step3.5 R3 为 `82/79,0/1`，非 zero-new | PASS | `step3_5-supplement-report.md:23-28,75-82`。 |
| 5 | R3 唯一 OFC2017 debt 已全文裁 `STRONG_NEIGHBOR` | PASS | `step-081:40-53`。 |
| 6 | P08 mapper 是单位平均功率 Gray square-16QAM、bit order `[b0,b1,b2,b3]` | PASS | `p08_coded_chain.py:43-61`：axis `[-3,-1,+3,+1]`、`/sqrt(10)`。 |
| 7 | `k/n=1024/1536`、Qm=4、20 iterations | PASS | `p08r_chain.py:89-105,128-145`。 |
| 8 | 每 polarization 16 CW、384 symbols/CW、6144 data symbols | PASS | `p08r2_phaseA.py:58-63`；`p08r2_chain.py:195-215`；`1536/4=384`。 |
| 9 | on-air symbol `j` 对应 RM `{j,384+j,768+j,1152+j}`，不跨 CW | PASS | installed Sionna output-interleaver derivation见 step-085 `:26-43`，源码 owner见 `encoding.py:303-344,791-796`。 |
| 10 | 非零 square-16QAM symmetry rotation 平均翻 2/4 bits | PASS | Gray 轴有限枚举，step-085 `:52-69`；三个非零 rotation 均无 fixed point、mean flips=2。 |
| 11 | ideal single-global residual `SER=min(alpha,1-alpha)` | PASS | 对 q=0、q=-k、其余两类逐项最小化；step-085 `:71-98`。 |
| 12 | label-BER 是上述 SER 的 1/2；O1=0 只在 noiseless | PASS | #10 + step-085 `:85-98,119-126`；中央报告没有外推 coded FER/dB。 |
| 13 | 当前 decoder只回 hard info；tuple state不是 iteration count | PASS | `p08r_chain.py:158-178` 与 step-086 `:83-85`；Sionna 2.0.1 state=`msg_v2c`。 |
| 14 | 当前 realization把 RX 与 TX/truth放在同一对象 | PASS | `p08r2_chain.py:199-233` 同存 `rX/rY,sX/sY,h,theta,cw_info,cw_bits`。 |
| 15 | P08-R2 旧 method_B1/B2 不等于中央语义 B1/B2 | PASS | `p08r2_phaseA.py:164-194`：temperature 与 clip/decoder tuning。 |
| 16 | JLT2020不能支持 turbulence→discrete slip | PASS | step-085 `:163-181`：BPSK、无 laser-PN、turbulent phase在其 DPLL 下近可忽略；中央报告保持 factorized ceiling。 |
| 17 | OFC2017 input 包含 `p_s` 与 `sigma_e^2`，front-end为 QPSK fourth-power CPE、L=31 | PASS | `7937400.md:27-31,39-47`。中央报告只冻结了 `p_s`估计，没有冻结 `sigma_e^2` 或 source-native caller。 |
| 18 | OFC2017 one-way decoder interaction / no feedback | PASS | `7937400.md:41-49` 与 step-081 `:16-25`：pilot state probability并行改 LLR，FEC只下游消费一次。 |
| 19 | source-native `(M,N)` 不是中央报告的 Cartesian grid | **FAIL in report** | 全文 `:47,127` 为 `(M=2,N=100)`；`:131` 为 `M=3,N={10,20,100,200}`。报告 `:125` 写 `M∈{2,3},N∈{20,100,200}`，既制造未源证组合又漏 `(3,10)`。 |
| 20 | OFC2017 pilot interval 是 1 pilot + `N-1` data | PASS | `7937400.md:119-123`。报告未说明在固定 6144 coded-data symbols 中是替换、puncture/erasure 还是延长 frame。 |
| 21 | `S_RX` 对 square-QAM合法 rotation恒定 tie | **FAIL in report** | 对 constellation `C=e^{jkπ/2}C`，`min_{x∈C}|ye^{-jkπ/2}-x|²=min_{x∈C}|y-x|²`；按任意 boundary求和仍相同。报告 `:275` 已承认 ties 固定 no-op，却仍用其 MRR 作为 decoder增量对手。 |
| 22 | dual-pol slip shared/independent 必须冻结 | **FAIL in report** | step-085 `:143-151` 明确“按 polarization 独立构造需另行冻结 slip 是否共享”；报告 D0.1 state/event无 polarization index或 shared/independent rule。 |
| 23 | 7.00 日算术 | PASS | D0 `0.25+0.50+0.75+1.00+0.75+0.25=3.50`；post `0.50+1.25+0.75+0.50=3.00`；+0.50=`7.00`。 |
| 24 | framework/Q1/supplement/085–088/D/V/H owner 文件 | PASS | T043列出的 12 个 owner/pointer fresh `12/12` 存在。 |

## 5. Findings

### P0

0。

### P1-1 — step-088 的 D0 fail-closed 缺口仍未实质关闭

- **位置**：`projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md:252-278`。
- **事实**：自然层给了 `20→50 seeds × 12 cells` 上限，但受控 twins/diagnostic 只列 3 boundaries×3 rotations，没有冻结使用哪些 seeds/cells、最大 trajectories/frames；D0.2/3/5 也未规定 natural 与 controlled 是“均须过”、仅 controlled 承重还是怎样合取。`:266` 声称 uncertainty unit 是 seed/trajectory cluster，`:271` 却对 12 cells/seed 的 event frames使用普通 exact-binomial Clopper-Pearson；若同 seed跨 cells 共享 trajectory，该 CI 不处理 cluster dependence。step-085 `:149` 要求双偏振 slip shared/independent 必须另冻，报告 event state却无 polarization语义。最后，D0.6 要求 false-action/rejection/fallback，但 `:278` 又明确 D0不授权 trigger/selection/fallback，未冻结哪个 score/margin产生 action、何时 no-op/reject。
- **为什么是 P1**：同一 raw rows 可因 stratum 合取、cluster unit、pol ownership或 clean action定义不同而得到相反 PASS/FAIL；这正是 step-088 P1-1 要消除的解释自由度。
- **所需修正**：冻结 controlled 的完整 maximum exposure；逐门写明 natural/controlled 的 acceptance aggregation；按预注册独立单位选择 cluster-valid CI（或证明每 frame独立后再用 CP）；冻结 per-pol/shared event与candidate action；为 D0 diagnostic 明确 `score→accept/reject/no-op`，否则 D0.6 标 N/A 并移到正式 C1 合同，不能两边同时承担 gate。

### P1-2 — D0.5 的 `S_RX` 是由 constellation symmetry 强制造成的弱对手

- **位置**：`step4a-a0-preflight.md:163-169,264-278`，尤其 `:275`。
- **事实**：square-16QAM constellation 对四个 `k*pi/2` rotation闭合。若 `S_RX` 只是 unknown-data max-log Euclidean score，则每个合法 rotation、每个 suffix boundary的 per-symbol最小距离完全不变，所有候选 deterministic tie；固定 no-op只是在 tie-break中指定一个常数输出。
- **为什么是 P1**：`S_DEC` 相对这个退化 baseline取得 MRR gain，只能证明 coded labels打破了一个人为丢掉 pilot/phase-state信息的对称性，不能证明 decoder evidence相对“receiver-only CPE/pilot metric”有增量，也不能排除 A0 §2 的 pilot/small-state简单方法。绝对 top-1 `>=0.25` 不修复 comparator-task mismatch。
- **所需修正**：把 `S_RX` 降为 identity/chance floor；另冻一个合法、非退化且同 candidate output的 receiver-only comparator（例如 known-pilot likelihood / OFC2017-like state posterior或 source-backed phase-continuity score），给予独立 dev tuning并在同 support/资源账本上比较。若没有这样的 score，D0.5只能回答“decoder score有绝对信息”，不能裁“decoder信息增量”。

### P1-3 — 单一 `B2_PRIMARY` 已解决 envelope 数量问题，但尚非 source-faithful executable comparator

- **位置**：`step4a-a0-preflight.md:115-128,212-233,241-262`；source=`papers/doi/10.1364_ofc.2017.w2a.56/7937400.md:27-49,119-131`；lineage=`step-081:14-25`。
- **事实**：原方法接收 blind fourth-power CPE 的 `p_s` 与 residual `sigma_e^2`，L=31；正文只执行 `(M=2,N=100)` 与 `(M=3,N={10,20,100,200})`。修订报告的 B0却是 16QAM DD-DPLL，未说明 L=31 front-end如何进入 B2，未冻结 `sigma_e^2` 的 receiver-visible估计；`:125` 写成错误 Cartesian grid并漏 N=10。更关键的是 source pilot schedule为每 N symbols一 pilot、N-1 data，而 P08链固定 6144 coded-data symbols：报告没有冻结 pilot是替换（需 puncture/erasure mapping）还是延长 frame（改变 trajectory length/latency），仅说 goodput扣 overhead。
- **为什么是 P1**：D0.4 coverage的唯一 primary comparator无法按当前合同唯一实现；不同 caller、statistic、grid和pilot insertion会改变信息量、FER、goodput、发生率 exposure与 1.00 日工期。旧 P1-2 的数量冲突虽关闭，新 comparator仍可能成为弱/错实现。
- **所需修正**：冻结 source-native或明确 adaptation contract：front-end、`p_s/sigma_e^2` estimator、exact candidate tuples、pilot placement/puncturing/frame extension、LLR marginalization与 one-way decoder caller；所有 QPSK→16QAM/4th-power→DD-DPLL transfer逐项标 `[外推]`。随后把这些具体工项映射到 1.00 日B2行并重裁 point estimate。

### P2

0。

## 6. Control disposition

**维持 CP010 等待修复。**

本 verifier 不授权 D0、adapter、C1-ext、MVE、科学实验、Step 4a Go、Contract/Execute 或 thesis claim。主控应先修 P1-1/P1-2/P1-3，再派新的 fresh verifier；只有 `P0/P1/P2=0/0/0` 后，主控才可另立 D/V/CP 考虑开放 D0。

## 7. Protection receipt

- task-control：fresh `PASS`。
- protected p05：final fresh `4/4 MATCH`：`p05_run.log=7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`；`p05_run2.log=735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`；`p05_run3.log=C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`；`p05_run4.log=95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`。与启动值及 step-088 receipt 一致。
- git staging：启动与 final fresh 均 `EMPTY`（`STAGED_COUNT=0`）；四个 p05 仍为既有 untracked，均未 staged。
- 唯一写入：本 verifier 只新增 `projects/thesis-fso/worker-logs/step-089-c1-a0-preflight-reverifier.md`；final fresh status=`??`。
- 禁止动作：未运行 web/search/download、代码实现、adapter、defect smoke、MVE、仿真、科学实验、commit 或 push。
