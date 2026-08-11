# Step 088 — C1 A0/A′/A/B fresh verifier

> 2026-08-10 | T042 / CP010 / epoch 10 | fresh-context verifier  
> control receipt：`validate_task_control.py T042...` fresh 返回 `PASS`；action=`FEASIBILITY_A0`。  
> scope：只读审查中央报告、step-085/086/087、framework、当前 owner、源码与本地全文；不替主线程修文件。  
> no-experiment receipt：未运行 web/search/download、adapter、defect smoke、MVE、科学实验、代码实现、commit 或 push。

## 1. Verdict

**FAIL；P0/P1/P2=`0/2/0`。**

中央报告对理论式、16QAM/interleaver mapping、coded/uncoded ceiling、physical transfer ceiling、truth boundary、A0/A′/A/B 结构和 B2 身份边界的合成基本忠实；但 D0 的定量验收函数尚未冻结，且 6.50 日 BOM 未覆盖报告自己要求的三路 independently-tuned `B2*` envelope。二者都会让后续 D0 无法确定性 fail-close，故不得据本报告另立控制决策开放 D0。

Disposition：**维持 CP010 等待修复**；`D0_EXECUTION_AUTHORIZED=NO`、`STEP4A_GO=NO`、`METHOD_SIGNAL=NONE`。

## 2. Requirement matrix

| Requirement | Verdict | Fresh evidence / reason |
|---|---|---|
| A0 §0 合法问题 | PASS | 中央报告 `:47-56` 逐项映射 Q1 4/4；canonical owner 在 `projects/thesis-fso/literature_notes_coded_decoder_feedback.md:80-91`。 |
| A0 §1 headroom / FR-21 | PASS | 报告 `:60-92` 保留 `[论证]/[实证]/[外推]`，只确认 uncoded structural residual，coded FER/post-BER/goodput 仍 UNKNOWN；FR-21 明确 Kill-only。 |
| A0 §2 non-ML 适配 | PASS | 报告 `:98-100` 改审 simple-method sufficiency，没有伪造 ML 必要性。 |
| A0 §3 相邻先例 | PASS | 报告 `:101,106-114` 同时保留成功先例与 crowding ceiling；本地全文支持。 |
| A0 §4 finite-search triviality | PASS | 报告 `:102` 明确 `MDP=N/A_NON_RL / FINITE_SEARCH_WARNING`，fatal 指向 small-state/scan 等价。 |
| A0 §5 负面证据 | PASS | 报告 `:103,108-114` 覆盖 feedback oscillation、rare/absent defect、FEC/B2 absorption。 |
| A0 §6 prior coverage 语义 | PASS | 报告 `:104,117-125` 正确保留 UNKNOWN、90/95 门、zero-denominator fail-closed；执行验收缺口另见 P1-1。 |
| A′ 竞争维度 | PASS | 报告 `:127-140` 覆盖 primary FER/post-BER、goodput、clean safety、decode/latency、pilot/coding/buffer overhead、localization，且均为条件性 claim。 |
| A：B1 与增强 B2 | PASS | 报告 `:142-160` 只确认相对 B1 的 uncoded 结构优势；相对 enhanced B2 仍 UNKNOWN。 |
| B：novelty / feasibility 分离 | PASS | 报告 `:162-184` 列 R1–R4 四项零假设，bounded-slice 非碰撞未被升级为 novelty closure。 |
| physical：natural / injected 两层 | PASS | 报告 `:186-193` 明确自然层不得注入、受控层不得回答 occurrence，也禁止 turbulence→slip 因果外推；D0.1 的可执行定量合同仍 FAIL，见 P1-1。 |
| truth / candidate ceiling | PASS | 报告 `:195-199,148-157,248-252` 把 TX/true state/final correctness 隔离到 evaluator，只允许 receiver-visible candidate ranking，不声称 true boundary。 |
| B2 ladder / 90–95 semantics | PASS | 报告 `:117-125,225-231` 正确冻结 `max(PAPU-like,OFC2017-like,global retry)`；differential/slip-tolerant FEC 单列结构吸收支路；CSSC/CS-DC 仅 identity ceiling；O1 只作 Kill/headroom。 |
| 6.50 日 BOM 完整性 | **FAIL** | 报告 `:205-213` 仅给 B1 + 单个 “frozen cheap B2” 共 0.50 日，却在 `:125,227,241` 要求三路 executable、independent-dev-tuned B2 envelope；缺实现/调谐/paired parity 的工期，见 P1-2。 |
| D0.0–D0.6 fail-closed | **FAIL** | `:237-243` 的 D0.1/2/3/5/6 仍使用“多个”“稳定”“显著”“优于”“安全”等未定义判据；`:254-264` 又把数字明确留为 D0 之后才冻结的“候选”，见 P1-1。 |
| 当前授权边界 | PASS | 报告 `:7-8,266-289` 明确 D0、adapter、MVE、Step 4a Go 与 claim 均未授权；与 CP010 一致。 |

### 三组强制边界 verdict

| Boundary | Verdict | Evidence |
|---|---|---|
| natural occurrence vs injected diagnosis | 语义 PASS / D0 合同 FAIL | `step4a-a0-preflight.md:190-193` 正确分层；但自然事件定义、exposure 与 occurrence CI 未冻结，不能执行性 PASS/FAIL。 |
| coded vs uncoded headroom | PASS | `:13,60-92,271` 不把 `SER/label-BER` 解析式外推为 coded FER、goodput 或 dB。 |
| candidate ranking vs true boundary | 语义 PASS / D0 合同 FAIL | `:137,148-157,180,242,252` 只允许 candidate ranking；但 ranking metric/tolerance/CI 尚未冻结。 |

## 3. Fact spot-checks

以下 18 项均为 fresh 回源，不仅是中央文档互相对照。

| # | Claim checked | Verdict | Fresh source / derivation |
|---:|---|---|---|
| 1 | Q1 canonical 4/4，occurrence/observability/recoverability 留给 4a | PASS | `literature_notes_coded_decoder_feedback.md:80-91`。 |
| 2 | Step 3.5 为 bounded-slice ceiling，R3 仍有 0/1 新 SHOULD | PASS | `step3_5-supplement-report.md:20-28,61-78`：R3=`82/79,0/1`，不是 zero-new；唯一 OFC2017 debt 已闭。 |
| 3 | P08 mapper 是单位平均功率 Gray square-16QAM、bit order `[b0,b1,b2,b3]` | PASS | `p08_coded_chain.py:46-88`：axis `[-3,-1,+3,+1]`、`/sqrt(10)`、四 bit 顺序。 |
| 4 | `k/n=1024/1536`、Qm=4、20 iterations | PASS | `p08r_chain.py:89-105,128-145`。 |
| 5 | 每 CW 384 个连续 on-air symbols，flatten 不跨 CW 重排 | PASS | `p08r2_chain.py:204-215`；`1536/4=384`，row-major `cw_bits.reshape(-1)`。 |
| 6 | symbol `j` 对应 RM `{j,384+j,768+j,1152+j}` | PASS | installed Sionna `encoding.py:303-340,791-796`：`perm_seq[i+4j]=384i+j` 后以 `_out_int` 输出。 |
| 7 | 非零 16QAM symmetry rotation 平均翻 2/4 bits | PASS | 由上述 Gray 轴纸笔枚举：`π` 翻两 sign bits；`±π/2` 各有 8 个 1-bit 与 8 个 3-bit 变换，均值 2 bits。未运行 scientific rows。 |
| 8 | single-global B1 下界 `SER=min(alpha,1-alpha)`、label-BER 为其 1/2，O1=0 | PASS | 对 `q=0` 仅后段错、`q=-k` 仅前段错、其余 q 两段皆错，故取两段较小者；结合 #7 得 bit factor 1/2。 |
| 9 | 该解析式不能推出 coded FER/goodput/dB | PASS | interleaver 与 soft LDPC 事实见 `p08r_chain.py:128-164`、Sionna output interleaver；中央报告保持 UNKNOWN。 |
| 10 | 当前 decoder 只回 hard info；tuple state 不是 iteration count | PASS | `p08r_chain.py:158-175` 当前误名分支；Sionna `decoding.py:837-855,1670-1700` 明确返回 `msg_v2c` state。 |
| 11 | Sionna 2.0.1 支持 callbacks、soft output、per-call iteration/state | PASS | installed metadata=`sionna 2.0.1`；`decoding.py:188-200,837-855,1346-1394,1442-1469`。 |
| 12 | 当前 realization 把 RX 与 TX/truth 字段放在同一对象 | PASS | `p08r2_chain.py:153-186,207-233` 同时保存 `rX/rY`、`sX/sY`、`h/theta`、info/coded bits。 |
| 13 | P08-R2 名为 B1/B2 的方法不是 canonical B1/B2 | PASS | `p08r2_phaseA.py:164-194`：B1 仅 LLR temperature，B2 为 clipping + decoder alpha/offset。 |
| 14 | JLT 2020 不支持 turbulence→discrete slip | PASS | `10.1109_jlt.2020.3003561/content.md:31,96,194-206`：BPSK、未讨论 laser PN；在其 DPLL 下 turbulent phase difference negligible。 |
| 15 | ICTON 负面机制为 reliability contradiction / oscillation，error floor 约 `1e-3` 且错误帧 `>1000` bits | PASS | `10.1109_icton.2016.7550341/content.md:71,93-101`。 |
| 16 | PAPU 是 0.78% pilot/per-127 的 forward B2，高 OSNR slip probability `<1e-7` | PASS | `10.3390_app9132749/source.md:45,68,80-86`；post-FEC gains 3/1/0.5 dB 见 `:121-135`，仅限其 fiber/QPSK slice。 |
| 17 | OFC2017 fully parallel、无 decision feedback，GMI gain 0.5–0.8 dB | PASS | `10.1364_ofc.2017.w2a.56/7937400.md:39-53`。 |
| 18 | CSSC/CS-DC 仅 identity ceiling；关键 evidence pointers 存在 | PASS | `step-071-c1-cssc-universal-b2-fulltext.md:10-24,45-65` 两者 `UNRESOLVED_FULLTEXT`；中央报告列出的 framework/Q1/supplement/085–087/D/V/H 及八份直接全文路径 fresh `20/20` 存在。 |

补充数值抽查：IWCMC 的 candidate list `NQ=5` 与额外 5 decoder iterations=`17%` 见 `10.1109_iwcmc58020.2023.10182805/content.md:209-217,237,267`；OFC2014 的 3% pilot turbo gain 1.05 dB、距 ideal 0.3 dB 见 `10.1364_ofc.2014.m3a.3/content.md:307-311`。这些均未被中央报告跨场景改写成本项目性能。

## 4. Findings

### P0

0。

### P1-1 — D0 acceptance function 未冻结，不能确定性 fail-close

- **位置**：`projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md:237-243,254-264`。
- **事实**：D0.4 有 90/95 数字，BOM 有 `>7D` 数字；但 D0.1 没有 local symmetry-slip 的可执行 event definition、boundary tolerance、自然 exposure/seed×condition grid、最低有意义 occurrence rate 或零事件 upper-CI；D0.2 的“稳定损失”、D0.3 的“显著/实际 gap”、D0.5 的“优于 receiver-only score”、D0.6 的“安全”也没有冻结 metric、population、effect threshold、CI 与 stop rule。
- **为什么是 P1**：报告 `:254-264` 明确把 0.5 dB/10%/5%/25%/1% 等数字称为“D0 通过后”才冻结的候选，因此这些数不能反过来承担 D0 PASS。相同 raw rows 可被主观解释成 PASS 或 FAIL，违反 T042 对 D0.0–D0.6 fail-closed 的验收。
- **所需修正**：在开放 D0 前冻结每门的 `population → metric → estimator/CI → threshold → PASS/FAIL/ANOMALY → stop`；D0.1 另需 source-grounded natural event definition/exposure 与 controlled fixture 到 natural event class 的同一性检查；D0.5 冻结 candidate-ranking metric、grid/tolerance 和 decoder-evidence 相对 receiver-only 的最小增量。

### P1-2 — `B2*` 三路 envelope 与 6.50 日 BOM 不闭合

- **位置**：`step4a-a0-preflight.md:117-125,205-215,225-243`；来源差异见 `step-086-c1-a0-coded-chain-bom.md:218-229` 与 `step-087-c1-a0-prior-negative-evidence.md:35-41,110-133`。
- **事实**：中央合同要求 `B2*=max(PAPU-like,OFC2017-like,global retry)` 且三者独立 dev 调谐、same-info/cost parity；BOM 却只给“canonical B1 与 frozen cheap B2”合计 0.50 日，没有逐项纳入三路实现/适配、dev tuning、candidate-list/pilot overhead 与 paired cost 验证。step-086 的 6.50 日估计原本只承诺一个 cheap B2；step-087 后来才把三路 ladder 定为最低 envelope。
- **为什么是 P1**：D0.4 的吸收裁决依赖三路 max envelope；若 BOM 只实现一条，就会以弱 B2 错判“未吸收”，若全实现，6.50 日与 `>7D_BLOCKER=NOT_ESTABLISHED` 没有工期依据。
- **所需修正**：要么逐路重估并重算总 BOM/`>7D`，要么以 source-backed stop rule 先冻结一个能代表 strongest obvious alternative 的可执行 B2，并明确其余为何不进入 D0 absorption ceiling；不能保持三路 max 合同同时沿用单 B2 的 0.50 日。

### P2

0。

## 5. Control disposition

**维持 CP010 等待修复。**

当前只允许继续 `FEASIBILITY_A0 / SOURCE_AUDIT / THEORETICAL_BOUND / BASELINE_CONTRACT_DRAFT / FULLTEXT_READ`。修复 P1-1/P1-2、重算合同/BOM 并由新的 fresh verifier PASS 后，主控才可考虑另立 D/V/CP 开放 D0；本 verifier 不直接授权 D0、adapter、C1-ext、MVE、实验或 claim。

## 6. Protection receipt

- task-control：fresh `PASS`。
- protected p05：final fresh `4/4 MATCH`：`p05_run.log=7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`；`p05_run2.log=735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`；`p05_run3.log=C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`；`p05_run4.log=95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`。与 step-084/085 receipt 精确一致。
- git staging：final fresh `EMPTY`；四个 p05 均未 staged。
- 唯一写入：本 verifier 仅新增 `projects/thesis-fso/worker-logs/step-088-c1-a0-preflight-verifier.md`（fresh status=`??`）；启动时已有的其他 dirty/untracked 项未修改、清理或暂存。
- 禁止动作：未运行 web/search/download、代码实现、adapter、defect smoke、MVE、科学实验、commit 或 push。
