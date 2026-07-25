# Worker Log: high-order CPR combination method (T006, B10/B12 Step 4a package)

> 阶段: formal GW Step 4a dimension D (combination method adjudication)
> 授权: D012 / T006 (epoch 8, HIGH_ORDER_CPR_COMBINATION_METHOD_PACKAGE)
> worktree: .worktrees/research-direction-lab-longitudinal-test
> branch: codex/research-direction-lab-longitudinal-test | start HEAD: bfc97d7e | T005 immutable: per worktree HEAD

## Input authority and immutable baseline

- branch `codex/research-direction-lab-longitudinal-test`, start HEAD
  `bfc97d7ea3122da6f9f8dbd6aee0e98e391a92ce`, worktree clean（初始）。
- T002/T003/T004/T005 immutable: `explore/results/tests/pilot-jones-*` — 全程零改动
  （`git diff --stat` 验证 protected 路径空 diff）。
- protected 未改: `projects/thesis-fso/direction-lab/`（canonical-state.yaml /
  completion-events.jsonl）、`.agents/skills/`（research-direction-lab /
  session-governance / sim-preflight）、shared canonical generator
  `common/_dual_pol_channel.py`、`common/_gg_time.py`、`common/_modulation.py`、
  `common/_recovery.py`、`params.py`。
- D012、topic-index RDL-CONTROL (epoch 8)、T006 任务书、master-state §2、
  literature_notes L20/L22、B10/B12 read-notes、stages/groundwork.md +
  gw-feasibility.md、thesis-lessons TL-20/22/23/26/27/30-33、code-quality.md、
  sim-preflight SKILL 全部完整读取并遵守。止于 Step 4a 维度 D，未进
  Step 5/Contract/Execute；不改 protected/shared/Skill/controller；不 push。

## Phase A — source closure + contract frozen (BEFORE any primary run)

- `source-closure.yaml`: B10 pilot-RLS（state/action/pilot→DD switch/complexity）
  + B12 MAP（anchor 频域 CW + MAP joint ML/MAP，含 AOPN model）。参数 provenance
  三分：来自论文（B10 28GBaud/CFO 1MHz-10GHz/lw 50kHz-1.45MHz；MAP L_block=128/
  L_sub=1/Wang [5]）/ 来自星地 simulator（2.5GBaud/10kHz ECL/16-QAM/canonical GG）/
  validation-tuned（lambda/L_block/ML window/pilot overhead/stress CFO+lw）。
  Image-only 公式（B10 L85-89 RLS recursion / L97 linear model / L107 DD output；
  B12 L71 PA-ML Eq 5 / L77 joint ML/MAP Eq 6 / L83 amplitude vector a）显式标
  closure caveat（FR-26/C6），数字 dB 仅作 context，不作 Go 论据。
- `contract.yaml`: primary modulation = uniform 16-QAM；canonical star-ground GG
  link（复用 `generate_shared_realization_dp(modulation='qam16')`，单极化 rX）；
  CFO/linewidth dimensional audit（nominal 100kHz CFO + 10kHz lw；stress 10MHz
  CFO + 100kHz lw，均在 B10 支持归一化范围内）；3 SNR 点 [14,17,20]dB 邻 HD-FEC
  waterfall；fairness（所有 arm 共享 pilot pattern/total TX energy/data mask/
  realization/BER denominator）；5 val + 10 test fresh disjoint seeds（7600-7604/
  7700-7709，与 T002-T005 excluded 不相交）；pre-registered verdict 4 态
  （KILL_NO_LEGAL_HEADROOM / GO_METHOD / COMPONENT_REPRO_ONLY /
  PROBLEM_SURVIVES_METHODS_FAIL）。

## Phase B — semantic gates (7/7 PASS)

1. **noiseless_recovery**: 高 SNR + 零 CFO + 近零 lw，O/B10/B12 BER ≈ 0 (< 1e-6)。PASS。
2. **cfo_phase_sign_and_units**: 已知 CFO=100kHz，B10 h1 sign 与预期一致，
   magnitude_ratio 在 [0.5, 2.0]。PASS。
3. **pilot_data_mask_overhead**: pilot 与 data mask 不相交，overhead=1/64 精确。PASS。
4. **energy_fairness**: 所有 arm 共享 tx_with_pilots，TX energy 自动一致。PASS。
5. **no_future_leakage**: B10/B12 因果（前半帧 zeroing 后半不影响前半输出）；
   BPS/VV 用声明的 Nw 滑窗（允许）。PASS。
6. **no_tx_truth_in_deployable**: deployable arm 签名不含 oracle args
   （bits_data/phi_true/tx_data/h/theta_sop）。PASS。
7. **identity_non_degeneration**: B10/B12/P1/P2/P3 在 noisy 实现上输出 pairwise
   max-abs-diff > 1e-9，无 alias。PASS。

## Phase C — B* selection (validation only)

扫描 BPS(B,Nw) + VV Nw + DD-DPLL omega 在 3 cond × 3 SNR × 5 val seeds：
- winner = **VV Nw=128**（mean BER 1.1271e-2）。
- B* 冻结后 test seeds 仅复用，不再调参。

## Phase D — headroom gate (B\* → O)

3 cond × 3 SNR × 10 test seeds，per-cell paired bootstrap 95% CI（2000 resamples）：

- 最大 point estimate = **0.6059 dB**（adversarial_sourced|snr14，强湍流 + SNR 14dB
  近 HD-FEC waterfall）。
- 最大 CI upper = **1.7192 dB**。
- 唯一 survivor cell = `adversarial_sourced|snr14`（mean ≥ 0.5 AND ci_upper ≥ 0.5）。
- 独立 raw→aggregate 重算：survivor cell mean 重算 0.605863 = 存储 0.605863 bit-identical。

**verdict = HEADROOM_SURVIVES**（headroom 门过；进 Phase E 方法门）。

## Phase E — method gate (P1/P2/P3 vs B\* AND strongest standalone)

3 cond × 3 SNR × 10 test seeds × 7 arms（O/B\*/B10/B12/P1/P2/P3）：

- **无 go_candidates**：所有 P 在所有 cell 的 gain vs B\* 为 −9 ~ −20 dB，
  paired wins 0/10；gain vs strongest standalone 同样 −8 ~ −20 dB。
- clean_control 退化远超 0.1 dB tolerance（P3 在 clean_control 退化 −18 dB）。
- **verdict = `PROBLEM_SURVIVES_METHODS_FAIL`**。

机制诊断：在 canonical 10kHz 线宽（D-007 ECL 典型星地 FSO）下，
B10 的 DD 反馈环追踪 AWGN 致判决错误（TL-10 同源 positive-feedback 失败），
B12 MAP 的 Wiener covariance 趋零退化为 plain PA + over-smoothing。
P1/P2/P3 级联/门控两个失败估计器，放大失败。这与 D-009 对 NDA-ML 的结论
一致（10kHz 线宽下 NDA-ML ≡ VV，无机制增量），扩展到 B10/B12 组合族。

## Integrity (self-verification, same context — status PARTIAL)

> 独立 science critic / integrity verifier 子 agent 未使用（单 GLM 对话）。
> 按 T006 §6 规则，integrity/科学结论状态最高 PARTIAL；不得自称"双审查 PASS"。

- T002/T003/T004/T005/protected/shared 全零改动（`git diff --stat` 验证空）。
- fresh pytest T006：**32 tests PASS**（5.18s）。
- immutability regression：T003(13)+T004(25)+T005(17) = **55 tests PASS**（8.18s）。
- 跨进程 determinism：T006 bit-identical across PYTHONHASHSEED=0/99999
  （`test_crossprocess_fingerprint_subprocess`）。
- contract/result 闭包：`_assert_closure()` 跑前强制 contract N/seeds/cells = runner；
  `test_contract_sha_is_real_file_hash` 验证真 SHA256（非文件名字符串）。
- raw→aggregate 独立重算：survivor cell mean headroom bit-identical（0.605863）。
- actual SHA closure：contract + 11 source SHA 全 match 实际文件。
- B\* validation 冻结（VV Nw=128），test 不调参。
- seeds disjoint：val{7600-7604} ∩ test{7700-7709} ∩ T002-T005 excluded = empty。
- Windows locale：32 tests 在默认 locale 与 PYTHONUTF8=1 下均 PASS。

## Commands and exact results

- `python explore/high-order-cpr-combination/run_all.py`（~336s）→
  phaseB gates 7/7 PASS / phaseC B\*=VV Nw=128 / phaseD HEADROOM_SURVIVES
  （max point 0.6059 dB, max CI upper 1.7192 dB, survivor=adversarial_sourced|snr14）
  / phaseE `PROBLEM_SURVIVES_METHODS_FAIL`（all P gain vs B\* −9~-20 dB, 0/10 wins）。
- `python -m pytest tests/test_high_order_cpr_combination.py -q` →
  **32 passed in 5.18s**。
- `python -m pytest tests/test_pilot_jones_temporal_adjudication.py
  tests/test_pilot_jones_complex_repair.py tests/test_pilot_jones_complex_salvage.py -q`
  → **55 passed in 8.18s**（immutability regression）。
- `git diff --check` → 无 whitespace error。
- `git diff --stat HEAD -- projects/simulation/common/ projects/simulation/params.py
  projects/thesis-fso/direction-lab/ .agents/skills/ projects/simulation/explore/pilot-jones-*/`
  → 空（protected/shared 全零改动）。
- YAML parse（contract + source-closure）+ JSON parse（5 result files）→ OK。
- raw recompute（survivor cell mean）→ bit-identical。

## Changed files

新增（explore/high-order-cpr-combination/）：
- `source-closure.yaml`（B10/B12 source closure + 参数 provenance + image caveat）
- `contract.yaml`（frozen grid + pre-registered verdict）
- `components.py`（B10 pilot-RLS + B12 MAP standalone + truth-assisted O）
- `baselines.py`（B\* ladder BPS/VV/DD-DPLL + P1/P2/P3 + eval_resolve）
- `channel_helpers.py`（canonical single-pol 16-QAM + pilot injection + BER）
- `semantic_gates.py`（7 gates）
- `run_all.py`（Phase B-E orchestrator + SHA closure）
- `synthesis.md`（本文件综合报告）
- `__init__.py`（package marker）

新增 `results/high-order-cpr-combination/`：
- `phase_b_gates.json`、`phase_c_bstar.json`、`phase_d_headroom.json`、
  `phase_e_methods.json`、`result.json`。

新增 `tests/test_high_order_cpr_combination.py`（32 tests）。

新增 `worker-logs/step-006-high-order-cpr-combination-method.md`（本文件）。

## Protected/immutable verification

T002（pilot-jones-step4a）、T003（salvage）、T004（repair）、T005（temporal-adjudication）、
protected（direction-lab/、.agents/skills/）、shared canonical generator
（common/_dual_pol_channel.py、common/_gg_time.py、common/_modulation.py、
common/_recovery.py）、params.py — `git diff --stat` 验证空 diff。

## Anomaly

- B10/B12 image-only 公式（RLS recursion / PA-ML Eq 5 / joint ML/MAP Eq 6）按
  FR-26/C6 closure caveat 重建（从 surviving prose + canonical RLS/ML/MAP form），
  非数据异常。
- RLS 在 long DD run（N=8192, lam=0.99）出现 (1/lam)^N 数值溢出；加 P-norm cap
  （`P_NORM_CAP = 1e6 * ||P_init||`，超限时 reset 到 P_init）防护。这是数值
  safeguard，不限制 genuine tracking（real tracking keeps P bounded by input covariance）。
  非数据异常，是实现 safeguard。
- 独立审查不可用 → status PARTIAL（非数据异常，是 T006 §6 规则限制）。
- 组合方法在 canonical 10kHz 线宽下 9-20 dB 输给 B\* —— 这是真机制失败
  （D-009 NDA-ML 结论的扩展），非 bug；semantic gates 全过 + CFO sign/units
  正向验证排除实现错误。
