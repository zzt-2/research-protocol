# C1 reference-method extension — Step 4a A0/A′/A/B 预检

> 日期：2026-08-10  
> 专题：`.sessions/2026-08-09-coded-decoder-feedback-groundwork/`  
> 控制：CP012 / epoch 12 / D011 / V005  
> 状态：`VERIFIED_CONDITIONAL_PASS / D0_IMPLEMENTATION_PREFLIGHT`  
> 裁决：`D0_IMPLEMENTATION_UNIT_AND_NONSCIENTIFIC_BENCHMARK_ONLY`  
> 明确不授权：DEFECT_SMOKE/S1–S4、adapter、C1-ext、MVE、held-out experiment、Step 4a Go、贡献声称

## 1. Findings first

1. **Q1 是合法问题，不再是“动作原子是否全新”的空白题。** Q1 的 M-C-A、方法产出、近期顶刊 baseline 与量化对标四判据均已通过；Step 3.5 在三轮上限和全部 MUST/SHOULD debt 关闭后，未确认八字段完整链 exact collision。
2. **全局 reference M 存在严格的无编码结构残差。** 对 Gray square-16QAM、单个非零 `k*pi/2` 永久 jump、boundary 前占比 `alpha`，任何单一 global rotation 的理想下界为 `SER=min(alpha,1-alpha)`、均匀 expected pre-FEC hard-label bit-error fraction 为 `0.5min(alpha,1-alpha)`；noiseless truth boundary/correction 的 O1 为 0。该结果是 `[论证]`，不是 coded FER、goodput 或 dB 增益；有噪声时 O1 只移除 slip 分量，不保证总错误为 0。
3. **现有编码链允许精确映射候选 interval 到 touched codeword，但不天然提供 segment-local syndrome。** P08-R2 每 CW 为 `1024/1536`、384 个 16QAM symbols；单 CW output interleaver 将 symbol `j` 映到 rate-matched positions `{j,384+j,768+j,1152+j}`，不跨 CW。合法的最小 evidence 是在同一 full-frame 支持集上计算、按 evaluated bits 归一化的 re-encode likelihood；不同 suffix 的 raw touched-CW NLL sum 不能直接比较。“decoder 找到了真实 boundary”或“逐符号 syndrome”均未成立。
4. **方法必要性尚未成立。** 该候选是 deterministic finite search，不是 ML/MDP。PAPU-like、OFC2017-like、independently tuned global retry、小状态 scan/DP 或 differential/slip-tolerant FEC 可能已经以更低成本吸收问题；同 slice 的 90%/95% coverage 仍未知。
5. **自然 FSO occurrence 是最危险的未决项。** JLT 2020 可以锚定 turbulence/AO/CFO 场景，却不建立 discrete symmetry slip，且其 turbulent phase 在所用 DPLL 下影响可忽略；OFC/ICTON 的 slip 来自相邻 coherent-fiber/QPSK stress。两轴只能做 `[外推]` 的正交 factorization，不能声称 turbulence 导致 slip。
6. **工程预算只形成条件性点估计。** 两轮审查证明旧 6.50/7.00 日表都漏项；单一 owner 现把 source-explicit B2 adaptation 计为 2.00 日、D0=4.50 日、最小 C1+fresh held-out=2.00 日、contingency=0.50 日，总上限 7.00 日。任何必要工项超出 contingency 即是 hard blocker，不能靠删 identity/safety/baseline/held-out 挤回预算。

因此，本报告只支持把 D0 定义为对 A0 未决 fatal 的最小配对证伪。**D0 不是 MVE、不是 Step 4a Go，也不是贡献证据。step-091 接收 A0 科学合同；step-101→103 资产链随后证明 v3 可实现但仍需工程门。D011/V005/CP012 当前只授权实现、单测及独立代码审查后的非科学吞吐门，不授权执行 S1–S4。**

## 2. 冻结研究对象与 collision ceiling

### 2.1 Reference M、目标 C、待证伪 A

- **M / canonical B1**：冻结整帧只选择一个 constellation-symmetry phase hypothesis，再对整帧解调/译码；不输出 boundary，不执行 segment/suffix action。
- **C**：coherent-FSO coded receiver 中、合法 carrier dynamics 与 conventional CPR 后的 within-frame residual constellation-symmetry ambiguity / local cycle slip。
- **A**：若一帧前后属于不同 phase class，则一个 global phase candidate 不能同时对齐两段，且 whole-frame decoder evidence 可能被局部错误污染；是否留下 coded FER/goodput headroom、能否被 receiver-visible evidence 区分，均待 D0。

潜在 C1-ext 仍只是设计假设：

`receiver samples/state + decoder evidence → defect trigger → bounded boundary/range candidates → local/suffix phase action → touched-CW full restart decode → receiver-visible selection/abstain → B1/B2 fallback → bounded output/cost ledger`

### 2.2 Step 3.5 能与不能证明的内容

完整 collision 签名固定为：

`receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output`

三轮定向查询、双向引用链和全文裁决的上限结论是：

`NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE`

它不等于“领域中没有”，也不证明 feasibility、自然 occurrence、B2 未吸收或 C1-ext 有贡献。Generic decoder feedback、phase hypotheses、Markov slip state、windowed FEC 和 local tolerance 原子均已拥挤；只有完整链和可验证 trade-off 可能承载增量。

## 3. A0 §0：合法问题门控

Canonical Q1 已写入 `literature_notes_coded_decoder_feedback.md`：

| 四判据 | 状态 | 承重证据 |
|---|---|---|
| 具体 M-C-A | PASS | arXiv 2511.21340 / TSP 2006 的 whole-frame global assumption；C/A 为可证伪结构假设 |
| 方法产出形态 | PASS | trigger→localize→bounded repair→fallback→cost 的 deployable chain |
| 近期顶刊 baseline | PASS | TVT 2025/2026 ICE-CEM global code-aided CFO/CPO baseline |
| 可量化对标 | PASS | FER/post-BER/goodput、paired CI、decode/CPR/latency、clean safety |

`A0 §0 = PASS / Q1 4/4`。后续 §1–§6 只围绕该 Q1，不把“没人组合过”当问题本身。

## 4. A0 §1：性能间隙与 oracle 上界

### 4.1 无编码结构上界

在 noiseless、均匀 Gray-16QAM、单个永久 symmetry jump 的限定模型下：

```text
SER_global(q)
  = alpha * 1[q != 0]
  + (1-alpha) * 1[q != -k mod 4]

SER_B1*(alpha)      = min(alpha, 1-alpha)
label_BER_B1*(alpha)= 0.5 min(alpha, 1-alpha)
SER_O1(alpha)       = 0
```

中央 boundary `alpha=0.5` 时，理想 single-global B1 仍有 `SER=0.5`、label-BER=`0.25`；靠近帧端点时趋于 0。三个非零 square-16QAM rotations 的均匀平均 bit-flip rate 均为 0.5。

### 4.2 来源标签与限制

| 声称 | 类型 | 结论上限 |
|---|---|---|
| P08-R2 mapping、CW 和 interleaver identity | `[实证：执行源码]` | 工程 identity，不是科学性能 |
| 上述 B1/O1 解析式 | `[论证]` | 只证明 pre-FEC structural residual |
| JLT turbulence/AO/CFO 数字 | `[实证：论文原场景]` | BPSK/ideal timing/no laser-PN；不可直接移植 |
| JLT FSO envelope + OFC/ICTON slip + P08 codec | `[外推]` | 只可作 factorized stress，不可作为 Go 核心论据 |
| OFC/ICTON/PAPU 的 gain/slip-rate | `[实证：各自 optical-fiber slice]` | 不给本项目 occurrence 或 coded gain |

LDPC 看到 soft LLR；interleaver/Tanner 位置会改变可纠正性，FER 不是 hard-label BER 的线性函数。因此：

`UNCODED_STRUCTURAL_HEADROOM = CONFIRMED`

`CODED_FER/POST_BER/GOODPUT_HEADROOM = UNKNOWN`

`FR21 = KILL_ONLY / NOT_GO`：O1 只用于判断是否还有实际 headroom；在没有 coded curve 前，不把 label-BER 换算为 dB，也不以 O1 优于 B1 作为 Go。

## 5. A0 §2–§6：非 ML 适配裁决

框架原问题针对 ML/MDP；C1 是 deterministic reference-method extension。这里保留门控实质，不伪造 ML 必要性或 S/A/R/P。

| A0 项 | 适配后的问题 | 当前裁决 | fatal 条件 |
|---|---|---|---|
| §2 问题结构适配 | local evidence/action 是否相对简单 global/pilot/scan 有必要 | `WARNING_SIMPLE_METHOD_MAY_SUFFICE` | exact scan、pilot detector、global retry 或 primary B2 在各自资源入账后达到相同 output、safety、fallback |
| §3 相邻先例 | 相似 soft-state/decoder-assisted/local-tolerance 机制是否成功 | `PASS_PRIORS_EXIST / CROWDING_HIGH` | 先例不直接致命；完整链重名或无 trade-off 才致命 |
| §4 非平凡性 | finite boundary×rotation×fallback 是否退化为平凡 scan | `MDP=N/A_NON_RL / FINITE_SEARCH_WARNING` | 小状态 DP/固定阈值在 3–7 日 testbed 内等价，且无性能/成本第二维 |
| §5 负面证据 | feedback 失稳、rare defect、FEC/prior absorption | `NEGATIVE_EVIDENCE_MATERIAL` | feedback oscillation、defect absent、metric 无增量或 B2/FEC 清除 recoverable loss |
| §6 先验覆盖 | dev-frozen primary B2 对 O1 headroom 的比例，其他 families 约束 claim ceiling | `UNKNOWN_90_95_REQUIRES_PAIRED_SMOKE` | primary coverage `>=95%` 且无次维度；90%–95% 后又无预冻结 practical signal |

相邻成功先例已超过两篇：OFC 2014 whole-CW Markov turbo、Tikhonov mixture joint phase/LDPC、SC-LDPC slip-state window、PAPU、OFC 2017 soft-state LLR 与 burst-aware LDPC。它们证明 soft evidence/state interaction 可行，也把“decoder-aided”“windowed”“slip-aware”“soft-state”泛称占满。

主动负面证据包括：

- ICTON 2016 的 channel/decoder reliability contradiction、outer-loop oscillation、约 `1e-3` error floor 与错误帧 `>1000` bit；
- PAPU、OFC 2017、differential-FEC/HTDD 与 global retry 可能不用 decoder-local repair 就吸收损失；
- PAPU 高 OSNR cell 的 slip probability `<1e-7`，JLT FSO 全文不建立 discrete slip；
- Tikhonov limited-order 接近 DP、OFC 2017 fully parallel no-feedback、burst-aware LDPC 三轮饱和，均提示复杂链可能无剩余空间。

### 5.1 Primary B2 的 source-backed 选择

数值与实现唯一 owner 为 `d0-defect-smoke-contract.yaml`。冻结 primary identity 为 `OFC17_16QAM_EXTFRAME_V1`：periodic pilots → four-state Markov posterior → square-16QAM mixture LLR → one frozen LDPC decode；test-time best-of 禁止。原文只支持 QPSK、fourth-power CPE、`L=31`、`p_s/sigma_e^2` 与 tuple `(M,N)={(2,100),(3,10),(3,20),(3,100),(3,200)}`；common square-16QAM BPS front-end、FSO population、双偏振与 16QAM LLR 均逐项标为 `[外推]`，不移植原文 GMI/dB 数字。

为消除资源歧义，dev 选出唯一 tuple 后，B0/B1/B2/O1 及后续 C1 共享同一 extended pilot-bearing waveform、payload、phase/noise realization、pilot mask 与 symbol-time support；B0/B1 不消费 B2 state posterior。tuple、`p_s/sigma_e^2`、BPS 参数、score tie-break 均只在 disjoint dev 冻结。global retry 并入 B1；PAPU/differential/CSSC/CS-DC 只约束 claim ceiling，不进入 test-time envelope。升格任何 family 必须先 amendment、补预算并重新预检。

### 5.2 90%/95% coverage 合同

coverage 只用于 controlled primary reliability metric `L = affected-codeword error rate`：

`coverage_raw=(errors_B1-errors_B2)/(errors_B1-errors_O1)`。

每个 seed-cluster bootstrap replicate 内重算 counts、ratio 与 equal-cell macro aggregate；分母非正按 owner 的 fail-closed guard 处置，CI 使用未裁剪 ratio，`[0,1]` clipping 只用于展示。lower 95% CI `>=0.95` 为 absorption Kill，upper `<0.90` 为 non-absorption；中间区只能凭预冻结的 `>=5%` net-goodput 或 FER 非劣下 `>=25%` calls/latency 信号继续。coverage 不解释 latency、calls 或 goodput。

## 6. A′：竞争维度分解

当前没有一个维度被授权写成贡献。下表只冻结 D0/后续 MVE 必须量化的竞争面。

| 维度 | 先验覆盖 | C1-ext 可能增量 | 当前结论/可声称条件 |
|---|---|---|---|
| defect-cell FER / post-BER | 高风险、同 slice 未知 | local action 可能回收 B1 残差 | 只有相对 frozen `B2_PRIMARY` 的 paired gain 且 CI 支持才可声称 |
| net goodput | 中/未知；pilot 与 coding overhead 可显著 | clean no-op、只处理 touched CW 可能减少常驻 overhead | 必须扣 pilot/coding/redecode/rollback；相对 B2 `>=5%` 才是候选 practical signal |
| decoder-equivalent calls / latency | global retry/window methods可能高；绝对值未知 | bounded candidates/touched-CW restart | FER 非劣时 calls 或 measured latency `>=25%` reduction 才可形成工程信号 |
| clean/no-slip safety | always-on priors 缺 abstain 数据 | explicit no-op + fallback | false action `<=1%`、net-goodput loss `<=1%`，否则 fatal/repair |
| localization/action validity | prior 多给 per-symbol state 或 whole-CW feedback，不给同链 boundary output | receiver evidence 排候选并驱动 bounded action | 只能声称 candidate ranking；必须由 localization/trigger/repair 消融证明 load-bearing |
| pilot/coding/buffer overhead | primary OFC2017-like tuple 决定共享 pilot-bearing waveform | C1 只可在同 waveform 上比较 decoder/local-action 增量 | pilot/symbol-time overhead 对所有 arms 相同；各方法额外 HMM/LLR/decode/buffer 成本分别入账；改成 no-pilot C1 属 scope amendment |

若 frozen `B2_PRIMARY` 在 primary metric 的 coverage lower 95% CI `>=95%` 且上述次维度无一达到预冻结 practical signal，C1 Kill；若所有维度均被高覆盖，也不得靠组合叙事继续。

## 7. A：结构优势论证

### 7.1 相对最简 B1 的已证结构优势

Piecewise phase class 下，任何 single-global rotation 必然牺牲前段或后段；该损失不能通过“选得更准的全局 candidate”消除。local truth action 可在限定模型中消除该 residual。因此 `boundary/range + local action` 相对 B1 具有一个明确的信息/动作增量。

### 7.2 相对增强 B2 的未证部分

真正的 primary 对手不是裸 B1，而是 dev-frozen `B2_PRIMARY`；global retry、PAPU-like 与 differential/slip-tolerant FEC 继续限制 claim ceiling，但不组成测试时 oracle envelope。现有全文没有给同一 coherent-FSO coded slice 的 O1 denominator，不能宣称 C1-ext 会赢增强 B2。

### 7.3 编码链能与不能支持的 localization

- 可精确做：on-air candidate interval → touched CW → RM positions → mother VN/touched checks；按候选重算受影响 LLR，对 touched CW 提供完整 1536 LLR 并完整 restart decode。候选评分必须落在相同 full-frame support：`score=(sum changed-CW NLL + cached unchanged-CW NLL)/total evaluated bits`；不同 suffix 的 raw touched-CW NLL sum 因长度偏置不得直接比较。
- 不可声称：decoder bit index 是时间 index、只译 suffix bits、沿用 changed-LLR 之前的 decoder state、per-CW failure 唯一确定 boundary、symbol-local syndrome 或 exact true-boundary recovery。
- 永久 suffix slip 会触及 boundary CW 及所有后续 CW；若候选集合为 `R` 个 rotation/boundary actions，最坏 decoder work 必须按 `R * sum(touched_CW(candidate))` 报告，并同时列 decode calls、BP iterations 与 wall-clock latency。若无法在预冻结上限内闭合，不能把“local”写成有界局部重算。

方法范式与已成功先例对齐为有限 hypothesis/state、soft receiver evidence 和 bounded/full-CW decoder interaction；没有理由引入 ML。若最终最优链退化为 simple scan/global bank，本方向按 `METHOD_DELTA=NONE` 终止或降为纯实现组件。

`A = STRUCTURAL_ADVANTAGE_VS_B1_CONFIRMED_UNCODED / ADVANTAGE_VS_ENHANCED_B2_UNKNOWN`。

## 8. B：新颖性与可行性解耦

### 8.1 新颖性事实的上限

当前只知道 bounded slice 未确认同八字段完整链。不能写“首个 decoder-aided slip recovery”“领域从未做过”或“新颖性已关闭”。Generic core 与多个相邻链已经碰撞。

### 8.2 可行性原料

- finite phase bank、decoder likelihood/soft state、pilot unwrap、slip-state LLR 与 rollback/fallback 均有成功先例；
- 当前源码可精确建立 CW/symbol/interleaver ownership，Sionna 2.0.1 可提供 soft output、per-call iterations、state/callback；
- 最小 legal route 不依赖 custom decoder：touched-CW full restart + re-encode NLL；
- 这些只证明组件可构建，不证明完整链有方法增益。

### 8.3 空白零假设

| 零假设 | 当前反驳 | 状态与 falsifier |
|---|---|---|
| R1 pilot/differential/global turbo 已解决实用问题 | 它们付固定 pilot/coding/whole-frame cost，可能留下 goodput/latency 面 | `PARTIAL_REBUTTAL`；B2 coverage `>=95%` 且无次维度即成立 |
| R2 interleaver/decoder propagation 使 boundary 不可局部观测 | exact ownership 与 touched-CW NLL 可排候选，但不能证明 exact boundary | `UNRESOLVED`；receiver-visible metric 无增量即 fatal |
| R3 bounded change-point 只是平凡小状态 scan | explicit clean trigger、selective decode、fallback/cost 尚可能形成 trade-off | `WARNING`；simple scan 同 output/成本即 `METHOD_DELTA=NONE` |
| R4 合法 coherent-FSO 中 local discrete slip 极少或不存在 | 相邻 coherent-optical 有 slip stress；但 JLT FSO 不支持 turbulence→slip 因果 | `UNRESOLVED_OCCURRENCE`；自然 occurrence 门失败即 hard terminal/pivot |

`B = NOVELTY_NOT_CLOSED / FEASIBILITY_COMPONENTS_EXIST / COMPLETE_CHAIN_UNPROVEN`。

## 9. 物理与信息边界

### 9.1 两层 testbed 必须分开

1. **自然 occurrence 层**：来源支持的 coherent-FSO carrier dynamics、合法 physical parameters 与 corrected conventional CPR，在**不外部注入 discrete jump**时产生并由 evaluator 确认 within-frame symmetry slip。该层单独回答目标 defect 是否存在。
2. **受控 diagnosis 层**：在 frozen receiver output 后注入已知 `exp(jk*pi/2)` suffix step，正交扫描 boundary/jump，用于 identity、coded damage、O1 recoverability、B1/B2 coverage 与 receiver evidence stress。

受控注入层不能替代自然 occurrence 门。若没有可承重的 carrier receiver/parameter source，只能把结果称为 `residual-slip fixture`；它不能满足用户要求的“合法物理参数下确实出现”，也不能支持 coherent-FSO occurrence 或 turbulence-causality 声称。

### 9.2 Truth-free caller 边界

Deployable `ReceiverView` 只能含接收/均衡数据、known prefix、receiver-derived noise estimate 与 code layout。TX payload/info bits、coded bits、TX data symbols、true phase/CFO/channel/SNR、true slip boundary/correction 和 final correctness 只能进入隔离的 `TruthView/evaluator`，且在 method output 冻结之后评分。

当前 `CodedRealizationR2` 把 `sX/sY/h/theta/cw_info/cw_bits/gamma_bar` 与接收数据放在同一对象；deployable 方法不得继续接收该对象。Oracle 必须使用不同 caller/type，不能与 B0/B1/B2 共用字符串 dispatcher。

## 10. 工程可行性与 3–7 日边界

旧 6.50 日和 step-088 后的首版 7.00 日表均被撤回：前者没有 source-explicit B2/科学运行/contingency，后者把 OFC2017 adaptation 低估为 1.00 日且遗漏 disjoint C1 dev/held-out。machine-readable owner 重算为：

| 阶段 | 工项边界 | 日 |
|---|---|---:|
| D0 | contract/source 0.25 + Receiver/Truth/carrier 0.75 + B0/B1/O1/fixture 0.50 + source-explicit B2 2.00 + strata/tests/stats 0.50 + bounded runs/receipts 0.50 | **4.50** |
| post-D0 C1 | hard re-encode selector/trigger/local action/fallback 0.75 + identity/truth/clean/ablation/cost 0.50 + disjoint dev/fresh held-out/CI/report 0.75 | **2.00** |
| base + contingency | 6.50 + 0.50；contingency 可覆盖任何必要低估，但不得删除 identity/truth/safety/baseline/held-out | **7.00** |

资产静态预检已经 step-103 接收，但预算仍是 `BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK`，不是已证可行。若真实 common carrier/B2/decoder 路径使必要工作加 contingency `>7.00` 日，且允许的 vectorization/batch/cache/checkpoint 调整不能解除，或 shrink 会删除任一 gate/完整链 identity，即 `>7D_HARD_BLOCKER`。最小路线固定为三个 codeword-aligned boundaries、三种非零 rotations+no-op、hard re-encode NLL；不建设 soft callback/message-state，也不能称 exact syndrome localization。

## 11. D0 defect smoke 预冻结合同

本节的 scientific population/gates 已由 step-091 接收，v3 实现接口又由 step-103 接收。D011/V005/CP012 当前仅允许实现、单测和后置非科学吞吐门；关闭 A0 未决 fatal 的 S1–S4 scientific execution 仍须新的 D/V/CP，不实例化 C1-ext。

### 11.1 Baseline ladder

- **B0_ANALYTIC**：§4.1 的 noiseless single-jump 解析曲线，只是 identity/headroom 锚，不参加实验 best-of。
- **B0_EXPERIMENTAL**：dev-frozen conventional square-16QAM BPS + one frozen LDPC decode；BPS 的 `(B,Nw)` 只在 seeds 8000–8009 冻结，无 decoder feedback、无 post-hoc phase retry。
- **B1_ENHANCED_GLOBAL**：同一 receiver-visible data 上枚举四个合法 whole-frame `k*pi/2` hypotheses，以 full-frame normalized re-encode NLL 一次选出一个 global action，再完整 frozen LDPC decode；它包含 conventional global retry，但不输出 boundary、不做 segment/suffix action。
- **B2_PRIMARY**：dev-frozen `OFC17_16QAM_EXTFRAME_V1`；精确 source tuples、pilot/HMM/16QAM LLR adaptation 与 one-way LDPC 见 YAML owner。所有 arms 共享冻结后的 pilot-bearing waveform，禁止 test-time best-of。
- **O1**：offline truth boundary/phase correction，仅作 recoverability/headroom/Kill；有噪声时只移除 slip component，不保证零错，不能驱动 deployable action或充当 best-of baseline。
- **C1-ext**：D0 全部门通过后，另立决策才允许实例化。

当前 P08-R2 的 LLR-temperature `method_B1` 与 LLR-clip/tuning `method_B2` 必须改用语义 ID，不能冒充上述 B1/B2。

### 11.2 单一数值 owner 与四 strata

全部 population、seeds、B2 tuples/统计、event 定义、exposure、estimand、CI、candidate work 与 budget 只由 `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml` 定义；本报告不复制第二套数字。owner 当前在 D011/V005/CP012 下 `implementation_authorized=true / unit_test_authorized=true / engineering_benchmark_authorized=true / execution_authorized=false / scientific_experiment_authorized=false`，且 `not_mve=true / not_c1_extension=true`。

| stratum | 唯一职责 | 冻结上限 | PASS / terminal 摘要 |
|---|---|---:|---|
| S1 natural occurrence | 无注入，只证明目标 defect 在合法 population 出现 | 20→50 seeds ×12 cells=`600` dual-pol frames / 1200 pol-trajectories | persistent events `>=12`、`>=4` seed clusters、`>=2` cells；否则 `NATURAL_DEFECT_NOT_ESTABLISHED` |
| S2 controlled damage/recoverability/B2 | common-random slip-on/off twins；自然事件不提供 counterfactual | 10 seeds ×3 cells ×2 target pol ×3 boundaries ×3 rotations=`540` on +60 off | B1 damage `>=0.10` 且 lower CI>0；O1 recovery `>=10%` 且 lower CI>0；再裁 B2 90/95 coverage |
| S3 controlled observability | 三个 CW onset×三 rotations+no-op；比较 pilot-only 与 pilot+decoder score | 独立 dev/test 各 540 cases；test `47,520` CW-decodes | combined top-1 `>=0.25` 且 lower CI>`0.10`；MRR increment `>=0.10` 且 lower CI>0；否则 decoder evidence 不 load-bearing |
| S4 clean diagnostic | 只做 identity、truth、candidate isolation、score determinism 与 cost；不应用 action | 10 seeds×3 cells×2 pol=`60` trajectories | 任一 identity/information/cost gate 不过即 blocker |

四层禁止 pooled。S1 与 S2/S3/S4 分别承重 occurrence、causal headroom、observability 与工程 identity，必须合取；uncertainty 统一按 seed-cluster bootstrap。natural multi-transition frames只计 occurrence，不进入唯一-boundary ranking。X/Y event 分开判定、按 seed 聚类。

### 11.3 observability、feedback 与 post-D0 边界

unknown-data max-log 16QAM Euclidean score 因 `pi/2` 群对称恒定 tie，只保留为 analytic null，**不承担 acceptance**。合法 receiver-only comparator 是同十候选 support 上的 known-pilot single-transition HMM likelihood `S_PILOT`；decoder score 是同 full-frame bit support 的 normalized re-encode NLL。fusion weight只在 seeds 8050–8059 冻结；test 比较 `S_PILOT+lambda*S_DEC` 对 `S_PILOT` 的 paired top-1/MRR 增量，ties 固定为 no-op→较早 boundary→较小 rotation。

D0 不定义 trigger、threshold、accept/reject、fallback 或 applied local action，因此不再伪造 false-action/goodput gate。它只运行一次 frozen diagnostic evidence，所有 changed-CW candidates 从空 state 完整 restart；这排除 ICTON 型 recursive decoder-extrinsic oscillation。只有四 strata 全过并另立 D/V/CP 后，才允许在 disjoint seeds 8200–8219 冻结 C1 policy，并用 fresh 8300–8349 做 clean safety、fallback、组件消融与 fair comparison。

### 11.4 identity 锚与后续 practical signal

- no-slip/noiseless：B0/B1/O1 为 0；所有合法 boundary/rotation 的 noiseless O1 为 0；否则只能先修 rotation sign、prefix、CW split、interleaver。
- `alpha=0.5` noiseless single-global B1 不得优于 `SER=0.5, expected label-BER=0.25`；ideal curve 关于 0.5 对称。
- touched checks 只是 interval 的 Tanner one-hop support，不是 symbol-local syndrome；full restart 不复用旧 state。
- 后续 C1 至少达到：相对 frozen B2 的 FER/post-BER practical gain，或 `>=5%` net goodput，或 FER 非劣下 `>=25%` calls/latency reduction；clean false-action upper 95% bound与 net-goodput loss均 `<=1%`，且 decoder/local action 在消融中 load-bearing。未达即 `METHOD_DELTA=NONE`。

## 12. 当前裁决与下一控制动作

```text
Q1_4_OF_4                         = PASS
STEP3_5_COLLISION                 = NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE
A0_SECTION_1                     = UNCODED_HEADROOM_CONFIRMED / CODED_HEADROOM_UNKNOWN
A0_SECTION_2                     = WARNING_SIMPLE_METHOD_MAY_SUFFICE
A0_SECTION_3                     = PASS_PRIORS_EXIST / CROWDING_HIGH
A0_SECTION_4                     = MDP_NA_NON_RL / FINITE_SEARCH_WARNING
A0_SECTION_5                     = NEGATIVE_EVIDENCE_MATERIAL
A0_SECTION_6                     = UNKNOWN_90_95_REQUIRES_PAIRED_SMOKE
A_PRIME                          = COMPETITION_DIMENSIONS_FROZEN / CLAIMS_NOT_AUTHORIZED
A_STRUCTURAL                     = ADVANTAGE_VS_B1_UNCODED_ONLY / VS_B2_UNKNOWN
B_NOVELTY_FEASIBILITY            = NO_EXACT_COLLISION_BOUNDED / COMPLETE_CHAIN_UNPROVEN
FSO_OCCURRENCE                   = UNRESOLVED
ENGINEERING_BOM                  = 6.50D_BASE_PLUS_0.50D_CONTINGENCY / ASSET_PREFLIGHT_VERIFIED
BUDGET_FEASIBILITY               = BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK / HARD_CEILING_7.00D
FATAL_SIGNAL_CONFIRMED_NOW       = NONE
PRELIMINARY_DISPOSITION          = VERIFIED_CONDITIONAL_PASS / D0_SCIENTIFIC_EXECUTION_PENDING_ENGINEERING_GATES
STEP4A_GO                        = NO
METHOD_SIGNAL                    = NONE
D0_IMPLEMENTATION_AUTHORIZED     = YES / D011 + V005 + CP012 ONLY
D0_UNIT_TEST_AUTHORIZED          = YES / D011 + V005 + CP012 ONLY
ENGINEERING_BENCHMARK_AUTHORIZED = YES_AFTER_IMPLEMENTATION_UNIT_AND_INDEPENDENT_CODE_REVIEW
D0_S1_S4_EXECUTION_AUTHORIZED    = NO / NEW_D_V_CP_REQUIRED
```

step-091 已对 step-090 的全部残余项给出 `PASS / P0/P1/P2=0/0/0`。随后 step-101 保留 `FAIL 0/2/0`，step-102 additive repair，step-103 才以 `PASS 0/0/0` 接收 v3 实现前静态合同。D011/V005/CP012 当前只开放实现/单测/非科学吞吐门，不开放 S1–S4。未来 D0 只有同时关闭 occurrence、coded damage/headroom、recoverability、B2 absorption、decoder-information increment、diagnostic identity/information/cost，才允许另立决策实现 adapter/C1-ext；clean false-action、fallback 与 goodput safety仍属于 policy freeze 后的 post-D0 门控。最终 Step 4a Go 仍需维度 D/MVE 通过。

## 13. 审查历史

- `step-088-c1-a0-preflight-verifier.md`：`FAIL`，P0/P1/P2=`0/2/0`；D0 不定量，三路 test-time B2 envelope 与单-B2 BOM 冲突。
- `step-089-c1-a0-preflight-reverifier.md`：`FAIL`，P0/P1/P2=`0/3/0`；旧 envelope 数量冲突关闭，但 controlled exposure/合取/action policy 未闭、`S_RX` 为 symmetry tie、B2 front-end/统计/tuple/pilot placement 不可唯一执行。另一路 adversarial audit 独立指出 resource fairness、estimand/CI 与 held-out/BOM 漏项。
- `step-090-c1-a0-contract-v3-verifier.md`：`FAIL`，P0/P1/P2=`0/2/1`；此前 B2 source contract、strata/exposure/symmetry/budget 问题已关闭，残余问题仅为 bootstrap/无效分母复刻规则、S3 fusion 的 dev objective/tie-break，以及报告把 post-D0 safety 误列为 D0 闭环项。
- 本版修复：在唯一数值 owner 中冻结 10,000 次 seed-cluster percentile bootstrap、PCG64 seed、逐 cell 重算与 equal-cell macro、NA replicate 上限/最小有效 replicate/terminal；冻结 S3 pilot 与 decoder score 的支持集归一化、dev-only lexicographic fusion objective 与唯一 tie-break；把 clean false-action/fallback/goodput safety 明确移回 post-D0 policy gate。
- `step-091-c1-a0-step090-narrow-verifier.md`：`PASS`，P0/P1/P2=`0/0/0`；P1-1/P1-2/P2-1 全部 CLOSED，YAML parse、task-control、owner 初末 SHA、p05 4/4 与 staging 均 PASS。该时点由 D010/V004/CP011 开放冻结 D0；其当前 execution authority 后被 D011 限权取代，A0 scientific gates 与 adapter/C1-ext/MVE/held-out 禁令继续有效。
- `step-101-d0-asset-contract-verifier.md`：`FAIL`，P0/P1/P2=`0/2/0`；HMM clean/controlled statistic-fit 权重与 BPS/B2 typed dev-freeze artifacts 未闭。该失败不是 scientific terminal，保留为 v3 修复血缘。
- `step-102-d0-dev-freeze-artifact-audit.md`：给出不重开 scientific fields 的 additive repair，冻结七个具名 artifacts、exact aggregation 与 test chronology。
- `step-103-d0-dev-freeze-reverifier.md`：`PASS`，P0/P1/P2=`0/0/0`；step-101 两项 P1 CLOSED，`94/94` 静态断言 PASS，抽核范围内无 scientific-field drift。终态只允许治理转交，不自行授权任何实现或实验。

## 14. 证据指针

- 框架：`stages/gw-feasibility.md:19-137`；`stages/glossary.md` 问题四判据。
- Q1 owner：`projects/thesis-fso/literature_notes_coded_decoder_feedback.md:80-91`。
- collision：`projects/thesis-fso/coded-decoder-feedback-groundwork/step3_5-supplement-report.md`；step-067–083。
- 理论、physical factorization：`projects/thesis-fso/worker-logs/step-085-c1-a0-theory-headroom.md`。
- coded chain、mapping、truth boundary、BOM：`projects/thesis-fso/worker-logs/step-086-c1-a0-coded-chain-bom.md`。
- priors、negative evidence、90/95：`projects/thesis-fso/worker-logs/step-087-c1-a0-prior-negative-evidence.md`。
- 首轮 A0 独立审查：`projects/thesis-fso/worker-logs/step-088-c1-a0-preflight-verifier.md`。
- 修订版 A0 独立审查：`projects/thesis-fso/worker-logs/step-089-c1-a0-preflight-reverifier.md`。
- A0 contract v3 独立审查：`projects/thesis-fso/worker-logs/step-090-c1-a0-contract-v3-verifier.md`。
- step-090 残余项窄复核：`projects/thesis-fso/worker-logs/step-091-c1-a0-step090-narrow-verifier.md`。
- D0/B2/统计/预算唯一数值 owner：`projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`。
- 资产闭合：`projects/thesis-fso/coded-decoder-feedback-groundwork/d0-asset-preflight.md`；step-094–103。
- 控制 owner：`.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md`、`decisions.md` D011、`verifications.md` V005、`H004-d0-implementation-entry.md`。
