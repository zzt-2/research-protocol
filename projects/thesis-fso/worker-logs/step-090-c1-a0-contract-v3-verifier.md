# Step 090 — C1 A0 / D0 contract v3 fresh verifier

> 2026-08-10 | T044 / CP010 / epoch 10 | fresh-context verifier  
> snapshot：`step4a-a0-preflight.md` SHA256=`57A8E5EF262E8C388C93C4E353E29F4EADF8801F8EA4F7592F34BBEF7A6C92FC`；`d0-defect-smoke-contract.yaml` SHA256=`BCDFAF809EE2748CE345269E8688ED3325082DECC06240F161CF39BD86DFDB3B`。  
> scope / no-experiment receipt：仅静态读取框架、治理 owner、中央 report/YAML、step-081/085–089、本地 OFC2017 正文与 P08-R2 源码；只写本日志。未运行 web/search/download、仿真、defect smoke、adapter、MVE、科学实验、代码实现、commit 或 push。

## 1. Verdict

**FAIL；P0/P1/P2=`0/2/1`。**

本版已经关闭 controlled/natural 职责、受控 exposure、四层合取、cluster/polarization ownership、unknown-data symmetry tie、source tuple/pilot placement、B2 source transfer、one-way decoder 与 7.00 日预算的大部分旧缺口。但两个可导致相反科学裁决的自由度仍存在：统计 CI/无效 bootstrap replicate 没有唯一算法；S3 fusion 的 dev 选择函数没有冻结。另有一处 report 把已移至 post-D0 的 clean safety 又写成 D0 同时关闭项。

## 2. Prior-finding closure

| step-089 finding | Verdict | Fresh closure result |
|---|---|---|
| P1-1：controlled exposure、合取、cluster/pol ownership、D0 action-policy | **OPEN** | exposure、四 strata 合取、seed cluster、X/Y separate、natural rows 禁作 counterfactual、D0 `applied_action_policy:none` 均已关闭；但 `d0-defect-smoke-contract.yaml:224-236` 未冻结 bootstrap 次数/随机种子/CI 类型及无效 denominator replicate 的保留/剔除规则，故同 raw rows 仍可跨 90/95、lower-CI 门得到不同裁决。 |
| P1-2：unknown-data symmetry tie / receiver-only comparator | **OPEN** | `unknown_data_maxlog_score.acceptance_role:none` 已正确退出；`S_PILOT` 是 receiver-visible、同十候选 support 的非退化替代。但 YAML `:286-302` 只给 lambda grid 和“dev only”，没有 dev objective 与 lambda tie-break，fusion 仍不能唯一冻结。 |
| P1-3：B2 source-faithful executable contract | **CLOSED** | common 16QAM BPS、`p_s/sigma_e2` dev grid、source exact tuples、pilot extension/no puncture、16QAM mixture LLR、one-way decode、test best-of prohibition及所有 QPSK→16QAM/FSO/dual-pol transfer均已明示；新增 `resolve_qam16` 禁用与合法 state `[0,1,2,3]` 也在快照内。 |

## 3. Requirement matrix

| Requirement | Verdict | Evidence / reason |
|---|---|---|
| A0 §0–§6 ceiling | PASS | report `:45-127` 保留 Q1 4/4、uncoded-only headroom、coded UNKNOWN、non-ML simple-method warning、negative evidence与 90/95 unknown；不把 A0 写成 PASS/Go。 |
| A′ / A / B | PASS | report `:129-186` 只冻结竞争维度；相对 B1 仅 uncoded structure confirmed，相对 B2 unknown；bounded-slice 非碰撞未升级 novelty。 |
| physical factorization | PASS | report `:188-195` 与 YAML `:62-75,197-223` 分离 natural occurrence 与 controlled suffix fixture，禁止 turbulence→slip 因果。 |
| truth boundary | PASS | YAML `:22-49` 与 report `:197-201` 将 TX/true phase/boundary/final correctness隔离到 TruthView/evaluator；deployable caller只收 ReceiverView。 |
| B2 source contract | PASS | YAML `:88-176` 冻结 common BPS、exact tuples、extended pilots、statistics/LLR transfer、one-way LDPC、独立 dev freeze与一次 frozen tuple。 |
| four strata / exposure | PASS（统计算法除外） | YAML `:238-331` 唯一分配 S1 occurrence、S2 causal damage/recoverability/coverage、S3 observability、S4 identity/cost，并显式合取、禁止 pooling。 |
| statistics / raw-row determinism | **FAIL** | estimand方向、ratio-of-sums、zero/negative denominator 与 unclipped CI 已写；但 bootstrap/CI 实现与 invalid replicate 处理未冻结，见 P1-1。 |
| S3 observability fusion | **FAIL** | pilot-only comparator、candidate support、absolute/incremental gates与 candidate tie-break已写；lambda dev objective/tie-break缺失，见 P1-2。 |
| 3–7 日 budget | PASS | YAML `:345-370` 为 D0 4.50d + post-D0 2.00d + contingency 0.50d = 7.00d；含 source adaptation、tests/statistics/raw receipts、post-D0 dev/fresh held-out，且 contingency 不得删 gate。 |
| authorization | PASS | YAML `:4-10`、report `:274-280` 与 topic CP010 均保持 execution/scientific experiment false；本 verifier不授权 D0。 |

## 4. Fact spot-checks

以下 28 项为 fresh 回源/复算，不仅是中央文档互相对照。

| # | Claim checked | Verdict | Fresh source / derivation |
|---:|---|---|---|
| 1 | T044 绑定 epoch10/CP010/`FEASIBILITY_A0` | PASS | fresh `validate_task_control.py` 返回 `PASS`。 |
| 2 | 当前 lane 只允许 A0/source/bound/test-contract | PASS | topic-index control block；`master-state.md:38-47`。 |
| 3 | Q1 4/4 但 occurrence/observability/recoverability UNKNOWN | PASS | D009 `decisions.md:360-398`、H002 `:7-18`。 |
| 4 | YAML 可 parse | PASS | fresh `yaml.safe_load` 得 `dict / coded_decoder_feedback.d0.v1`。 |
| 5 | report/YAML 快照稳定且数值 owner 单一 | PASS at audit snapshot | SHA 见页首；report `:230-232` 指向 YAML，复制摘要与 YAML 一致。 |
| 6 | YAML 的 source/code 路径存在 | PASS | OFC2017、`adaptive-phase-window/source-closure.yaml`、`p08r2_chain.py`、`common/_recovery.py` fresh exists。 |
| 7 | OFC2017 exact tuples | PASS | YAML=`(2,100),(3,10),(3,20),(3,100),(3,200)`；正文 `7937400.md:47,127,131`。 |
| 8 | pilot count N=10 | PASS | `1+ceil(6144/9)=684`。 |
| 9 | pilot count N=20 | PASS | `1+ceil(6144/19)=325`。 |
| 10 | pilot count N=100/200 | PASS | `1+ceil(6144/99)=64`；`1+ceil(6144/199)=32`。 |
| 11 | pilots extend frame, do not replace/puncture 6144 coded data symbols | PASS | YAML `:130-141`；正文原 schedule为 1 pilot + N-1 data（`:119-123`）。 |
| 12 | source front-end facts are QPSK fourth-power, L=31, `p_s/sigma_e2` | PASS | `7937400.md:27-31,41-47`；YAML `:111-123` 明示 transfer。 |
| 13 | common BPS code exposes B/Nw and no hidden source fourth-power caller | PASS | `projects/simulation/common/_recovery.py:91-118`；YAML把该变化标为 transfer。 |
| 14 | existing 8×pi/4 resolver prohibited; legal states are 0–3 | PASS | YAML `:104-105`；当前 `bps_cpr` 自身不调用该 helper。 |
| 15 | B2 one-way decoder / no feedback | PASS | YAML `:158-176`；OFC2017 `7937400.md:43`；step-081 `:16-25`。 |
| 16 | B1 and B2 dev choices are test-frozen and test best-of forbidden | PASS | YAML `:92-106,164-176`；B1 parameters use B1-only objective per tuple，B2 selects exactly one tuple/stat pair。 |
| 17 | B0/B1/B2/O1 share waveform/payload/time support | PASS | YAML `:130-141,178-195`；额外 pilots不再只给 B2 买 FER。 |
| 18 | P08-R2 codec identity | PASS | `p08r_chain.py:89-178`：1024/1536、Qm=4 interleaver、20 iterations；`p08r2_chain.py:195-215`：16 CW/pol、6144 symbols。 |
| 19 | on-air symbol j maps to four RM stripes and no cross-CW interleaver | PASS | step-085 `:26-43`、step-086 `:87-131`；report `:154-158`。 |
| 20 | S1 exposure | PASS | `20*12=240` frames；`50*12=600` dual-pol frames=`1200` pol trajectories。 |
| 21 | S1 gate/CI semantics | PASS | YAML `:239-250`：12 events、4 seed clusters、2 cells；cluster CI descriptive only，不误用 pooled exact-binomial。 |
| 22 | S2 exposure | PASS | `10 seeds*3 cells*2 target pol=60 clusters`；`60*3 boundaries*3 rotations=540 on` + `60 off`。 |
| 23 | S3 candidate/decode arithmetic | PASS | `3*3+noop=10`；`16+3*(12+8+4)=88` CW-decodes/case；`540*88=47,520`。 |
| 24 | S4 exposure | PASS | `10*3*2=60` trajectories。 |
| 25 | natural rows never supply damage counterfactual | PASS | YAML `:23-24,252-270`；S2 `natural_rows_used:false`。 |
| 26 | dual-pol ownership and multi-transition rule | PASS | YAML `:197-209`：X/Y separate、seed cluster、multi-transition natural frames occurrence-only。 |
| 27 | coverage algebra and clipping ceiling | PASS（CI implementation FAIL） | YAML `:224-236`：ratio-of-sums formula、nonpositive headroom guard、unclipped CI、display-only clipping。 |
| 28 | budget arithmetic and completeness | PASS | fresh sum=`4.50 + 2.00 + 0.50 = 7.00`；fresh held-out/tests/receipt/source adaptation均有 line item。 |

## 5. Findings

### P0

0。

### P1-1 — bootstrap CI 与 invalid-denominator replicate 处理未冻结

- **位置**：`projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml:224-236,252-276,320-331`；report `:121-127,241`。
- **事实**：owner 只写 `seed_cluster_bootstrap_95_percent_ci` 和 “inside each replicate 重算 counts/ratio/macro”。未写 bootstrap replicate 数、确定性 RNG seed、percentile/basic/BCa CI、seed 如何跨三 cells 联动重采样；coverage replicate 分母非正比例 `>0.05` 会 terminal，但 `<=0.05` 的无效 replicate 是剔除、保留 NA 还是按 fail value 计入未定义。damage 的 cell 内聚合也未明确是 paired-case mean 还是 CW pooled rate。
- **影响**：相同 raw rows 可得到不同 lower/upper CI，直接改变 S2 damage/recovery、coverage 90/95 与 gate conjunction；属于可导致相反科学裁决的 P1。
- **所需修正**：冻结 raw-row必需字段与 cluster key、cell内计数/ratio→equal-cell macro 的唯一顺序、bootstrap `n/resample/RNG/CI`，并明确每类 zero/negative replicate 的 fail-closed处理及 CI denominator。

### P1-2 — S3 fusion 的 dev 选择函数不完整

- **位置**：`d0-defect-smoke-contract.yaml:278-303`；report `:243-247`。
- **事实**：`S_PILOT` 已替换退化的 unknown-data score，lambda grid=`[0.25,0.5,1,2,4]` 且 test不调参；但没有说明 dev 上以 top-1、MRR、incremental MRR还是合取 margin选 lambda，也没有 lambda 同分 tie-break。`normalized_single_transition_pilot_hmm_log_likelihood` 还未冻结具体 normalization。
- **影响**：同一 dev rows 可冻结不同 lambda，随后 S3 absolute/incremental test gate可能给相反 verdict；candidate ranking tie-break不能替代 hyperparameter tie-break。
- **所需修正**：冻结 `S_PILOT` 每候选公式/normalization、fusion dev objective、合取/排序规则和 lambda tie-break；test只消费唯一 frozen lambda。

### P2-1 — report 末端把 post-D0 clean safety 又写成 D0 同时关闭项

- **位置**：report `:247,280`；YAML `:305-318,333-343`。
- **事实**：`:247` 与 YAML 正确规定 D0 无 applied action/false-action/fallback，clean safety 在 policy freeze 后；`:280` 却写 D0 必须同时关闭“stability/safety/cost”才可 post-D0。
- **影响**：YAML owner 足以阻止误执行，故不升级 P1；但恢复者可能误以为 D0 仍有未定义 safety gate。
- **所需修正**：把 `:280` 改为 D0 关闭 diagnostic identity/information/cost；clean false-action/fallback/goodput safety由 post-D0 fresh held-out关闭。

## 6. Control disposition

**维持 CP010 修复。**

本 verifier 不授权 D0、adapter、C1-ext、MVE、科学实验、Step 4a Go、Contract/Execute 或 thesis claim。修复上述 P1/P2 后须另派 fresh verifier；只有 `P0/P1/P2=0/0/0`，主控才可另立 D/V/CP 考虑开放 D0，不能由本日志直接授权。

## 7. Protection receipt

- task-control：fresh `PASS`。
- protected p05 启动 SHA：`p05_run.log=7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`；`p05_run2.log=735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`；`p05_run3.log=C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`；`p05_run4.log=95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`。
- final fresh receipt：p05 `4/4 MATCH`；report/YAML SHA 分别仍为 `57A8...92FC` / `BCDFA...DFDB3B`，快照未漂移；staging `EMPTY`（count=0）；本日志状态=`??`，相对启动状态唯一新增 `projects/thesis-fso/worker-logs/step-090-c1-a0-contract-v3-verifier.md`；禁止动作均未执行。
