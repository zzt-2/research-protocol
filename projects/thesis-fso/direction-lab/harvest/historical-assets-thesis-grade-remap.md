# 历史方法资产硕士级重裁

> 2026-08-12 | 任务 T012 | 只读历史证据重裁
> terminal: THESIS_GRADE_CANDIDATE_AVAILABLE
> 本报告不产生 METHOD_SIGNAL、不恢复 active carrier、不授权实验，也不修改论文正文。

## 1. 一页人话结论

过去的资产并非“什么都没有”，而是把两类问题混在了一起：一类是科学上确实无效，例如 truth leakage、scale/cost artifact、problem absent、明确 headroom gate FAIL；另一类只是没有击败所有近期强方法、没有证明 SOTA，或贡献粒度只够硕士级场景适配。前者不能复活，后者不应被永久淘汰。

按硕士级 reference-method extension 标准重裁后，26 个独立资产分为：

- READY_FOR_THESIS_PACKAGING：2 项；
- NEEDS_ONE_BOUNDED_CONFIRMATION：2 项；
- SUPPORTING_ONLY：11 项；
- PERMANENTLY_INVALID：11 项。

因此，现有资产可以形成一条诚实的 Ch3–Ch5 技术链：

1. Ch3：CCISP 自适应载波恢复，已经是可写的主方法；
2. Ch4：优先补 P01 的接收侧 SNR 配置失配校准适配器。它不是新 selector 理论，而是对 CCISP 在配置失配下的鲁棒扩展；历史上已复现损害并恢复 4/5 个 harm cells，只差一次冻结 cross-grid 的 bounded confirmation；
3. Ch5：select-before-execute 单分支执行已经具备完整工程方法链，可写成低复杂度执行架构；定点、prefix-LS、coded-chain 等作为实现与正确性支撑。

P11 的 complex-LS Butterfly FIR 是第二顺位候选：它具有“参考训练方法→低导频闭式校准”的完整迁移动作，但历史 9/11/13/15 dB 标签实际都落在默认 20 dB，且 blind CMA 可能吸收优势，因此只能在修正 SNR 注入后做一次 bounded confirmation。

本轮唯一推荐下一包是 P01，不是重新找新方向，也不是把 P02 的全局 9→11 dB 调参包装成方法。P01 若被全局标量 retune 完全吸收，就诚实降为 SUPPORTING_ONLY；若保留跨条件恢复与 nominal safety 的不可吸收增量，则可作为 Ch4 的“面向 SNR 配置失配的接收侧校准鲁棒 CPR 扩展”。

## 2. 全量资产表

### 2.1 独立资产

| ID | 名称 | 原 terminal / 当前事实 | 关键证据 | 旧关闭原因 | 新四档 | claim ceiling |
|---|---|---|---|---|---|---|
| ccisp | Received-Power-Aware Adaptive CPR | THESIS_METHOD_READY | internal-method-kernel-inventory.yaml；CCISP authority chain | 无；已完成 | READY_FOR_THESIS_PACKAGING | 仅 9 dB、fixed-NDA、common-payload BER-ratio 0.8–1.5 dB、三档 downlink GG；不恢复 26/29、uplink、1.2–1.9 dB、3.1 dB |
| branch_route_b | Select-Before-Execute Single-Branch CPR | THESIS_ENGINEERING_METHOD_READY | ccisp-select-before-execute-single-branch-method-package.md；recomputed-evidence.json | 曾与 fixed-point 复合记账 | READY_FOR_THESIS_PACKAGING | 不声称新 selector、新 CPR estimator、FPGA/PPA；只声称执行调度与软件/运算量降低 |
| p01_snr_adapter | Receiver-Visible Pilot-SNR Calibration Adapter | NO_DIAGNOSTIC_SIGNAL 中的局部有效 adapter | step-028-p01-cpr-snr-mismatch.md；2a_region_calibration_authority_reconciliation/authority-reconciliation.md | 后续候选未过 MDE，且曾与 P02/T004 混账 | NEEDS_ONE_BOUNDED_CONFIRMATION | 只声称配置失配鲁棒扩展，不声称全域鲁棒或新 selector 理论 |
| p11_complex_ls_butterfly | Pilot-Efficient Complex-LS Calibration for Linear Butterfly FIR | PARTIAL_LOCAL_20DB_BASELINE_ASSET | step-041-p11-pilot-efficient-butterfly-fir.md；D058 closeout | SNR 标签未真正注入；CMA 吸收风险 | NEEDS_ONE_BOUNDED_CONFIRMATION | 仅线性 Butterfly FIR 的低导频校准；不称 CNN 创新或 SOTA |
| p02_global_ref_retune | Global Stage-1 Reference Retuning | PROBLEM_RESOLVED_BY_REGION_RETUNING | step-029-p02-cand-rank-operating-regime.md；2a authority package | 单一 ref=11 作用全部 cells，truth-defined region 不可部署 | SUPPORTING_ONLY | 传统调参/廉价 comparator |
| p03_fixed_point | Q(8,6) Bit-True Selector Deployment | PROBLEM_RESOLVED_BY_UNIFORM_PRECISION | step-030-p03-fixed-point-codesign.md；kernel inventory | uniform precision 已足够；无混合精度方法增量 | SUPPORTING_ONLY | 定点可部署性与 Ch5 数值边界，不声称 FPGA 资源/PPA |
| p08r2_coded_chain_asset | Corrected Coded-Chain and Information-Boundary Asset | PARTIAL reusable asset | D049/V075；campaign thesis map | chronology/科学合同多轮修复，方法问题 absent | SUPPORTING_ONLY | coded baseline、递归 AST 与 metamorphic 门；不当主方法 |
| prefix_ls_coded_receiver | Prefix-LS Receiver Calibration | corrected receiver-side component | P08-R2 corrected chain；campaign synthesis | correctness/calibration component，无独立方法结果 | SUPPORTING_ONLY | 可并入 coded receiver 实现，不单独成算法章 |
| p10_single_expert_router_probe | Two-Cell Router Probe | EVIDENCE_INSUFFICIENT / LOCAL_TWO_CELL_PROBE | D055/V081；step-040-p10-single-expert-router.md | 2 cells×6 dev seeds，无 held-out，配置规则未运行 | SUPPORTING_ONLY | 局部 crossover 诊断，不称 router method |
| amc_q_a_contract_a | Prediction-Risk AMC Contract-A Audit | STOPPED_INCONCLUSIVE_TESTBED_ACTION_MISMATCH | AMC D008/D009；feasibility_report_v2.md | oracle/action contract 本身不可行，无法评估 | SUPPORTING_ONLY | 只保留 action-contract/testbed 边界，不写方法 |
| amc_q_b_split_timescale | Split-Timescale AMC Argument | STOPPED_BASELINE_AND_TESTBED_UNAVAILABLE | AMC D008/D009；q-b-gate audit | baseline 与 coherent sat-ground testbed 缺位 | SUPPORTING_ONLY | 论证/未来方向，不称已验证方法 |
| p1_shared_m0 | Shared M0-Power FOE–CPE Compute Graph | RECENT_BASELINE_UNAVAILABLE | shared-M0 D005/V005；R002 | generic action 已碰撞，窄 delta 无近期 task-matched baseline | SUPPORTING_ONLY | 计算图 refactor idea；不称独立方法/新颖 |
| rml_fsts_structural_lag | Conditioned Structural-Lag FSTS | STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED | RML D011/D013；A0 audit | action-before 与 phase-screen/SMF/noise config hard-blocked | SUPPORTING_ONLY | testbed/BOM 与动作时序边界，不称方法 |
| k2_multi_hypothesis_unwrap | Bounded Multi-Hypothesis Phase Unwrapping | EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION | multi-hypothesis R006/R007/V004 | ICASSP 2023 提供 Viterbi survivor cap；fixed-lag 是标准 traceback | SUPPORTING_ONLY | 竞争边界与实现邻居，不作为新方法 |
| strong_comparator_boundary_bundle | Strong-Comparator and Scientific-Integrity Boundary Bundle | campaign-level supporting bundle | campaign thesis map；R010；V084 | 不是单一 deployable action | SUPPORTING_ONLY | Ch4/Ch5 的 baseline、metric、oracle、lifecycle 与审计边界 |
| p04_continuous_gg_ood | Continuous-GG OOD Selector Robustness | PROBLEM_ABSENT_ON_CONTINUOUS_GG | step-031-p04-continuous-gg-ood.md；D042/V068 | pooled held-out regret 0.1459 dB < MDE 0.15，且非 OOD-specific | PERMANENTLY_INVALID | 只保留负面边界 |
| p05_ml_ood_online_adaptation | ML OOD Online Adaptation | PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER | step-032-p05-ml-ood-online-adaptation.md；D043/V069 | standard CMA 恢复，ML-specific action 无增量 | PERMANENTLY_INVALID | 只保留 swap-visible metric 与 conventional boundary |
| p06_causal_history | Cross-Frame Causal History Method | NO_CAUSAL_HISTORY_INCREMENT | step-033-p06-causal-cross-frame-history.md；D044/V070 | history 有信息，但 persistence 强基线显著更好 | PERMANENTLY_INVALID | 只保留因果评估教训 |
| p07_agc_adc | AGC/ADC Dynamic-Range Method | PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION | step-035-p07r-agc-adc-science-repair.md；D046/V072 | 旧 +0.91 dB 为 q 未除以 g 的 scale artifact；修正后静态低增益足够 | PERMANENTLY_INVALID | 仅保留 scale-correctness 教训 |
| g1_safe_gated_normalization | Safe-Gated Normalization | G1_SIGNAL_INVALID_SCALE_ARTIFACT | step-042-g1-promotion-groundwork-scale-artifact.md；D057/V083 | post-CMA rescale 修补固定 slicer 尺度，非 receiver action 增量 | PERMANENTLY_INVALID | 只作 artifact/threat-to-validity 反例 |
| p09_adaptive_bps | Adaptive/Early-Stop BPS | EXECUTION_INVALID / KILL_C3 | D053/V079；P09 invalidation marker | 实际全算64却记8、B_used 恒定、TX-truth BER、MDE 错12倍 | PERMANENTLY_INVALID | 仅作 cost/metric/truth-leakage 反例 |
| amc_q_a_prime_existing_claim | Q-A′ No-Transmit Risk-Aware AMC Existing Positive Claim | UNAUTHORIZED_DEV_ONLY_REFRAME_PROBE | AMC D008/D009；corrected_v2 | 未获用户授权改变动作合同，且 tune_C1 未按新合同调谐 | PERMANENTLY_INVALID | 现有正向 claim 永久无效；未来 family 需新 GW，不随本项被 Kill |
| c3_adaptive_segmented_cpe | Adaptive Intra-Window Segmented CPE | PHYSICAL_PREMISE_UNSUPPORTED | adaptive-segmented-CPE D002/V001；R001 | 0 dB、0/8 significant；tuned VV 在高 linewidth 更强 | PERMANENTLY_INVALID | 仅保留 fixed-window 物理边界 |
| oversampled_sync_q1 | Joint Frame–Timing–CFO Grid Search | STEP4A_PREFLIGHT_KILL_OR_PIVOT | oversampled-sync D012/V008；semantic-smoke-report.md | B1 与 C 180/180 exact-equivalent；-6 dB C 对 B0 为 -1.7241% | PERMANENTLY_INVALID | latency/complexity 若重开必须是新 M-C-A |
| coded_decoder_feedback_c1 | Decoder-Feedback Slip Recovery C1 | SCIENCE TERMINAL FAIL | step-205/206；commit 3aa3762 evidence | damage 0.06944<0.10；recoverability 0.04008，CI[-0.11235,0.19036] | PERMANENTLY_INVALID | 底座可复用，C1 方法线关闭 |
| dsp_outage_combining_q001 | DSP-Outage-Aware Multi-Aperture Combining Q001 | PROBLEM_ABSENT_OR_TOO_SMALL | combining D008/V005；R006 | occurrence 3.1111%<10%；BER regret 0.1114%，CI跨0 | PERMANENTLY_INVALID | sandbox/validity test 可复用，不保留 Ch4 方法 |

说明：P07 原始 artifact 与 P07-R 修复结论合并在 p07_agc_adc 一项中，既保留 invalidation 血缘，也不重复计数。

### 2.2 历史复合标签/别名，不重复计数

| 别名 | 归属 | 新档位 | 说明 |
|---|---|---|---|
| 2A calibration-aware CPR | p01_snr_adapter + p02_global_ref_retune + T004 | SUPPORTING_ONLY（复合标签） | D038 已拆账；只有 P01 可作为 B 候选，复合 2A 不再作为独立方法 |
| 2B branch-routed fixed-point CPR | branch_route_b + p03_fixed_point | SUPPORTING_ONLY（复合标签） | scheduling 已晋级 A；fixed-point 仍 C，不能互相连带 |
| 2C coded calibration | p08r2_coded_chain_asset + prefix_ls_coded_receiver | SUPPORTING_ONLY | correctness infrastructure，无独立 coded action |
| 2D risk/outage | amc_q_a_prime_existing_claim | PERMANENTLY_INVALID（现有 claim） | 只否定未授权 dev-only claim，不否定未来经新 GW 定义的新问题 |

## 3. A/B 档详细卡

### A1. CCISP 自适应载波恢复

- 方法名：Received-Power-Aware Adaptive CPR。
- reference：固定 DA 与固定 NDA CPR。
- 目标场景：三档 downlink Gamma–Gamma 湍流下的相干接收。
- adaptation delta：基于接收侧可见量的两阶段分支选择，固定 13 dB effective-SNR gate。
- baseline：固定 NDA 为 headline reference，固定 DA 作另一传统分支。
- 现有数字：合法 headline 为 9 dB、相对 fixed NDA、common-payload BER-ratio 0.8–1.5 dB、30 seeds。
- 主图：三档湍流下 selector/fixed-DA/fixed-NDA 的 BER-ratio 或所需 SNR。
- 消融：去除 CV gate、去除 13 dB gate、固定 DA/NDA。
- 最小缺口：无新科学实验；只需按权威口径进入论文整合。
- claim ceiling：局部 downlink GG 场景方法，不称全域最优或 SOTA。

### A2. Select-Before-Execute 单分支执行

- 方法名：Select-Before-Execute Single-Branch CPR。
- reference：先把 DA/NDA 两支都执行后再选择的直接双路径实现。
- 目标场景：已有 CCISP selector 的逐窗执行。
- adaptation delta：selector 先产生 branch command，只执行选中的 recovery branch，再接公共 detector。
- baseline：双分支完整执行；固定 DA/NDA 核作资源参照。
- 现有数字：396,000 windows command/output mismatch=0；A-F/B-F BER 均 0.1071559804；timing ratio=0.5424435602，单侧 95% 聚类上界=0.5472819332；branch calls -50%；复乘/复加/除法/FFT 分别 -39.45%/-46.87%/-51.28%/-36.44%。
- 主图：双路径执行与单路径执行的数据流/调用量/时延对比。
- 消融：仅去掉 lazy execution；保留 selector 与 estimator 不变。
- 最小缺口：无新科学实验；若未来声称 FPGA/PPA，另需 RTL/HLS 综合，不属于当前 A 档 claim。
- claim ceiling：软件执行合同和运算量工程方法，不声称新 selector/estimator 或硬件资源结论。

### B1. P01 接收侧 SNR 配置失配校准适配器（唯一优先）

- 方法名：Receiver-Visible Pilot-SNR Calibration for Robust CCISP。
- reference：原 CCISP selector。
- 目标场景：配置 SNR 与真实运行 SNR 存在 ±3 dB 偏差的 GG 条件。
- adaptation delta：用 receiver-visible 非相干 pilot SNR 估计修正 selector 的运行输入；true gamma 不进入 decide。
- baseline：原 CCISP；dev-frozen 全局标量 ref retune 是必须保留的最强廉价对手；oracle 只作 headroom。
- 现有数字：原 selector 在 5 个 harm cells 受损 0.324–0.704 dB；P01 恢复 4/5；nominal safety 退化 1/15；weak@9 残余 -0.32285 dB，CI[-0.35679,-0.28891]。
- 主图：SNR mismatch × GG/SNR cell 的 gain/regret heatmap，以及 nominal safety。
- 消融：无 adapter、pilot estimator 换真值仅作 oracle、全局标量 retune、仅校准不改 selector。
- 唯一补证问题：P01 的 receiver-visible adapter 在冻结 cross-grid 上，能否保留“恢复≥4/5 + nominal material harm≤1/15”，且不能被单一 dev-frozen 全局标量 retune 同时吸收恢复与 safety？
- PASS：上述两项成立，并以 paired cluster CI 支撑关键差值；晋级 Ch4 方法包装。
- FAIL：全局 retune 完全吸收，或恢复/安全性不稳定；降为 SUPPORTING_ONLY。
- 失败后用途：作为 CCISP 配置敏感性与校准边界表。
- claim ceiling：场景化校准鲁棒扩展，不称新 selector 理论或全域鲁棒。

### B2. P11 低导频 Complex-LS Butterfly FIR 校准

- 方法名：Pilot-Efficient Complex-LS Calibration for Linear Butterfly FIR。
- reference：full-label Adam 训练的线性 Butterfly FIR。
- 目标场景：接收侧有限 pilot 开销的线性 2×2 FIR 校准。
- adaptation delta：以 1% pilot 的 closed-form complex LS 替代 full-label iterative Adam。
- baseline：full-label Adam；blind CMA 是必须保留的强传统 comparator。
- 现有数字：历史 20 dB 局部切片中，B2 complex-LS BER约 3.10e-4，B0 Adam约 3.86e-4；1% pilot。原标记 9/11/13/15 dB 实际未注入，不能当跨 SNR 证据。
- 主图：true-SNR × turbulence 下 BER 与 pilot-overhead；CMA/Adam/LS 三者并列。
- 消融：pilot fraction、LS regularization、是否使用 full labels。
- 唯一补证问题：修正 gamma 注入后，1% complex-LS 是否在至少三个 true-SNR 的 paired held-out grid 上对 Adam 非劣，并在预注册目标切片不被 blind CMA 完全吸收？
- PASS：LS 对 Adam 非劣且至少一个预注册切片相对 CMA 保留有界优势；晋级工程/校准方法。
- FAIL：优势仅是默认 20 dB 或 CMA 完全吸收；降为 20 dB SUPPORTING_ONLY。
- 失败后用途：线性 Butterfly FIR 身份与 pilot-supervision 边界。
- claim ceiling：不称 CNN 创新、通用 ML equalizer 或 SOTA。

## 4. 永久无效清单及边界

永久无效只针对已经跑过且触发科学无效条件的现有方法 claim，不扩大为“整个研究 family 永久禁止”：

1. P04：目标 OOD 问题在冻结连续 GG 切片 pooled regret 低于 MDE，且不是 OOD-specific。
2. P05：standard online CMA 已解决主要问题，没有 ML-specific action 增量。
3. P06：history-expanded 虽优于 current-only，但 persistence 强基线显著更好。
4. P07：原 +0.91 dB 来自 q 未除以 gain 的 scale artifact；修正后静态低增益解决。
5. G1：post-CMA rescale 修补固定 slicer 尺度，非方法作用点。
6. P09：错误成本记账、恒定截断、truth-resolved BER 与错误 MDE 共同使 C3 无效。
7. AMC Q-A′：当前 positive claim 未获授权且调谐合同错误；只关闭该 claim，不 Kill 新 GW family。
8. C3 segmented CPE：历史增益 0 dB、0/8 significant，物理前提不足。
9. 过采样同步 Q1：联合 grid 与 timing bank 180/180 等价，且性能/复杂度无增量。
10. coded decoder-feedback C1：damage 与 oracle recoverability 两道科学门均 FAIL。
11. DSP-outage combining Q001：问题 occurrence 仅 3.11%，BER regret 约 0.11% 且 CI 跨0。

以下不能因“有更强方法”放入永久无效：P1、K2、RML-FSTS、AMC Q-A/Q-B。它们分别是 recent baseline/cheap absorption、testbed/action-contract blocker，故保留为 SUPPORTING_ONLY。

## 5. 优先候选排序

1. P01 receiver-visible SNR calibration adapter：唯一能自然承接 Ch3、作用点清楚、已有真实 harm/recovery 数字、testbed 已存在、只差一次 bounded cross-grid confirmation 的 Ch4 候选。
2. P11 complex-LS Butterfly FIR：方法链完整，但需先修正 SNR 注入并面对 blind CMA，风险高于 P01。
3. branch_route_b：已是 A 档 Ch5 工程方法，不需要新包；优先级仅指论文整合，不是实验执行。

## 6. 唯一推荐下一包

唯一推荐：P01 calibration-aware cross-grid bounded confirmation。

冻结范围：

- 对象：原 CCISP、P01 receiver-visible adapter、dev-frozen 全局 scalar retune、oracle headroom；
- 条件：历史 ±3 dB configuration mismatch × GG scene × SNR paired grid，并保留 nominal safety cells；
- primary：common-payload gain/regret 与 nominal harm；
- integrity：true gamma/h/turbulence label 不进入 deployable decide；dev/test seeds 隔离；paired raw rows；test 前冻结 PASS/FAIL；
- PASS：恢复≥4/5 harm cells，nominal material harm≤1/15，且单一全局 retune 不能同时吸收恢复与 safety；
- FAIL：P01 降为 SUPPORTING_ONLY，Ch4 不再沿该校准动作改名重开；
- 不在本任务执行；须另建任务书并先走 sim-preflight/当前 GW authority check。

## 7. 对 Skill 的最小修订建议（本轮不实施）

1. 永久无效理由白名单：只有 truth/privileged leakage、scale/metric/cost artifact、不可复现/chronology 无合法证据、物理自由度不存在、problem absent、明确 scientific/headroom gate FAIL 才能进 PERMANENTLY_INVALID；“更强邻居/SOTA 未证/机制不够原创”只能降 claim ceiling。
2. 在 candidate closure 前增加 thesis-grade salvage checkpoint：若 action chain 完整且已有局部有效增量，必须判断是 A、B 还是 C，并明确“唯一 bounded confirmation”，不得直接从期刊级竞争不足跳到 dead end。
3. comparator 分层：内部必须检查显而易见廉价替代是否完全吸收；论文主表只要求 reference/经典 baseline 与承重 comparator，不强制展示所有 full-general/SOTA 邻居。该规则只改变包装门，不放宽科学完整性门。
