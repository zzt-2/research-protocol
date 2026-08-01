# step-037 — P08-R G_CODED_LLR_CALIBRATION_UNDER_GG_RESIDUAL 科学完整性修复（G 族，修正重判）

> 2026-08-01 | campaign P08-R | family G（修复后关闭）| executor: 主线程协调 + 子 agent
> 上游：D048（binding decision，冻结旧 P08 科学结论）+ 用户 P08-R 执行指令
> 验收：V074（16/16 ACCEPT，脚本 + 独立 sub-agent 双重核验）

## 任务

用户 P08-R 执行指令：旧 P08 科学结论（`PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE` + Phase A 数字 +
"coded loss 主导是不可恢复突发深衰落"归因 + worker-log triangle interleaver 声称 + harvest）不得继续使用。
systematic-debugging 流程：根因复现（保存修复前证据）→ 治理回退 → coded-chain 身份澄清 →
GG/信息/oracle/metric 修复 → fresh powered experiment → 条件式方法构造 → 独立 verifier → 单次 commit。
不修改旧 p08_* 文件隐藏错误，新建 `p08r_*` 版本化路径。不 push。

## 六根因复现（修复前，证据 `projects/simulation/results/p08r_coded_chain_repair/p08r_prefail_evidence.md`）

- **H1 GG provenance**：`p08_phaseA_gate.py:86` 硬编码 scenes={weak:(1.2,1.2),moderate:(4.2,1.4),strong:(8.0,4.0)}，与 params.py:100-228 真相源（weak=11.6,10.1/moderate=4.0,1.9/strong=4.2,1.4）三档全不一致且档位错位（moderate 的 (4.2,1.4) 实为 strong 值）。docstring 自称 "matching params.py" 谎报。
- **H2 runtime information**：6 处 σ²=1/(2γ_bar)（p08_coded_chain.py:314,348,381；p08_phaseA_gate.py:135,300），γ_bar 是 SNR 循环变量非 receiver-visible。B0/B1/B2 全用同一全局标量；均衡器逐 block 估 h 但未传到 LLR σ²。
- **H3 oracle action space**：`_oracle_sigma2`（p08_phaseA_gate.py:185-190）docstring 说 per-symbol 但实现返回单一 global scalar=mean(|eq-s_true|²)，每 polarization-realization 一标量，不覆盖候选 local/blockwise action space。
- **H4 metric contract**：Primary A（req-SNR@FER=0.1）对 B0/B1/B2 全 inf；代码（p08_phaseA_gate.py:397-407）静默退到未冻结 raw FER-delta，MDE=0.15dB 的 SNR-domain 交叉检查 NaN 从未生效。
- **H5 coded identity**：`p08_coded_chain.py:159` 调 `LDPC5GEncoder(k,n)` **未传 num_bits_per_symbol=4**（sionna encoding.py:792-793 交织被跳过）；correctness gate #10（p08_correctness_gate.py:236-238）自承未启用 3GPP interleaver；worker-log step-036:34 却谎称 "3GPP §5.4.2.2 sub-block + triangle bit-interleaver"。
- **H6 state lifecycle**：n_symbols=6144=384 sym/cw×16 cw/polarization，把 16 cw 当独立样本算 FER（应 trajectory/seed cluster）；raw schema 缺逐 cw h/fade 字段；fer=1.0 双峰 15% 行 16/16 全失败。

V073 15/15 ACCEPT 漏审：只查 consistency + provenance receipt（source hash、H·c=0、noiseless roundtrip、raw→aggregate relErr=0、seed 隔离），未查科学合同六项（H1-H6）。命中 sim-preflight rules/mve-validation.md "consistency≠correctness"（P07-R/D046 同病在 coded 层重演）。

## 治理回退（D048）

- accepted_valid_packages 8→**7**；current=P08-R；P09 暂停；G family 暂不关闭。
- V073 保留不删，标"合同一致性通过但科学合同六项漏审"。
- 旧 artifacts `projects/results/p08_coded_chain/*` 加 INVALIDATED_BY_P08R.md（不删不改）。
- P08 codec/AWGN 基础设施保留为 PARTIAL reusable asset。

## coded-chain 身份澄清（修复前冻结，option A）

`p08r_identity_freeze.md`：选项 A（启用 `num_bits_per_symbol=4`）验证并冻结。out_int 是真 3GPP §5.4.2.2
sub-block+triangle 置换（1536 unique，1534/1536 moved，前 12=[0,384,768,1152,1,385,...]，Q=384）；
noiseless roundtrip A BER=0（encoder↔decoder 配对正确，de-interleave 由 decoder 内部 out_int_inv 自动）。
身份诚实称 "5G NR BG2 rate-matched LDPC component + Gray-16QAM BICM，含 3GPP §5.4.2.2 bit interleaver"。

## 最小修复脚本（新建 `p08r_*`，旧 p08_* 不动标 INVALIDATED）

- `p08r_chain.py`：H1 get_gg_scenes()（params.py 单一真相源）；H5 CodecAdapterR 传 num_bits_per_symbol=4；
  H2 CalibrationPrefix（32 已知符号）+ estimate_sigma2_from_prefix；H3 O0/O1/O2 oracle ladder；
  H6 CodedRealizationR（per-trajectory + per-cw evidence，shared physics）。
- `p08r_phaseA.py`：H4 MetricContractR（dev/test fresh seeds 6000-6019/7000-7039 disjoint history）；
  H6 trajectory-cluster bootstrap_ci；method_B0/B1/B2/oracle。
- `p08r_run.py`：orchestrator（dev workspace scan → freeze metric before test → tune B1/B2 → test →
  mechanism decomposition → verdict §9 A-D）。
- `p08r_verify.py`：V074 确定性 16 项核验。

## Phase A 结果（fresh seeds，240s）

**dev workspace**（weak/moderate/strong × fG{100,1000} × SNR{10..22}dB × 20 dev seeds × B0/O1/O2）：
B0 FER 清晰从 ~0.5-0.68（10dB）降到 0（22dB），跨所有 scene/fG。**与旧 P08 对比**：旧 P08 B0 在 13dB
FER=0.284、19dB 仍 0.121（卡住），corrected chain 下 B0 在 weak@12dB 已 FER=0.15、14dB=0——旧 P08 的
"卡在 0.2"完全是 H1 (α,β) 错 + H2 σ² 错的 artifact。

**frozen metric**（dev 选 operating region [0.1,0.3] 中 oracle headroom 最大的 cell）：
weak@1000Hz@12dB，dev B0 FER=0.169，MDE_fer=0.2347（power 0.8，n_test=40）。

**test**（40 fresh trajectories，paired B0/B1/B2/O0/O1/O2）：
| method | mean FER |
|---|---|
| B0 | 0.115 |
| B1 (T=0.5) | 0.115 |
| B2 (α=0.875,off=0.1,clip=20) | 0.113 |
| O0 | 0.115 |
| O1 | 0.115 |
| O2 | 0.109 |

- Δ(B0−strongest_conv)=+0.0016 CI=[+0.0000,+0.0039]
- Δ(strongest_conv−O1)=−0.0016 CI=[−0.0039,+0.0000]
- Δ(strongest_conv−O2)=+0.0039 CI=[+0.0000,+0.0117]
- Δ(B0−O2)=+0.0055 CI=[+0.0000,+0.0141]（统计显著但 **0.55% FER ≪ MDE_fer=0.2347**）

**mechanism decomposition**（关键）：
- 4/40 trajectory 是 B0 all-cw-fail（深衰落突发，h_truth_mean 0.29-0.41 vs 成功 ~0.9）；
- **相同 4/40 在 O2 也 all-cw-fail**（不可恢复——即便 finest-grained local-truth oracle 也译不出）；
- 32/40 B0 full success；O2 部分救回 3/40、全救回 1/40。

## Phase B / Phase C：不运行

gate 顺序：Phase A 判 PROBLEM_ABSENT → 不进 Phase B 方法工厂，不进 Phase C 公平比较。
O1/O2 coded headroom（0.55% FER）≪ MDE ⇒ 问题不存在，不构造方法（用户指令 §7：O1/O2 headroom<MDE 直接关闭）。

## verifier V074（16/16 ACCEPT）

脚本 `p08r_verify.py` 16 项确定性 PASS + 独立 sub-agent（fresh context，不信任 executor 自述）沿 caller→callee
检查科学信息边界，逐项核 H1-H6，最终 **ACCEPT**。sub-agent 独立重算 mechanism decomposition（B0 all-cw-fail
seeds={7009,7011,7016,7038} = O2 all-cw-fail seeds，完全一致）、raw→aggregate relErr<1e-12、MDE 重算精确一致。
唯一 future-work seed（非缺陷）：equalize() 盲 h 估计用 gamma_bar 作噪声底（receiver-side 模块非 decide 泄漏）。

## 治理结论（最终）

- P08-R counts_as_valid_package=True（有效科学修复，诚实负面回答 coded-LLR 问题为"否"，corrected chain 下建立）。
- campaign accepted_valid 7→**8**/10（恢复）。G 族（coded-LLR-calibration）**关闭**（PROBLEM_ABSENT：
  coded loss 主导是不可恢复突发深衰落 10% trajectory，非 LLR 失配；单一 receiver-visible σ²≈最强传统校准，
  oracle 仅 0.55% FER 局部 headroom≪MDE）。
- 不产方法卡/不晋升/不建 pre-formal carrier（verdict 非 METHOD_SIGNAL）。
- P09 只准备不运行：coded-LLR 问题被诚实判 absent → P09 须换不同机制族，重新过 problem gate。
- 旧 P08 数字不得进入论文或 harvest，除非被 P08-R 新结果重新支持（新结果支持同一物理归因但 corrected chain）。
