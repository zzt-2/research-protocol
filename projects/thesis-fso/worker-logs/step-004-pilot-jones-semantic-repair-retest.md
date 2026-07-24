# Worker Log: Pilot-Jones semantic repair + retest (T004)

> 阶段: formal GW Step 4a 维度 D（语义修复 + paired retest + 条件式 MVE）
> 授权: D064 / V038 / T004 (epoch 6, PILOT_JONES_SEMANTIC_REPAIR_RETEST_PACKAGE)
> worktree: .worktrees/research-direction-lab-longitudinal-test
> branch: codex/research-direction-lab-longitudinal-test | start HEAD: 9fd5e32 | T003 commit: 5445a2e

## Input authority and immutable baseline

- branch `codex/research-direction-lab-longitudinal-test`, start HEAD `9fd5e322`, worktree clean（初始）。
- T003 immutable: `explore/pilot-jones-complex-salvage/`、`results/pilot-jones-complex-salvage/`、`tests/test_pilot_jones_complex_salvage.py` — 全程零改动（`git status` 验证空 diff）。
- protected 未改: `projects/thesis-fso/direction-lab/`（STATUS.v1.md / project.v1.yaml / canonical-state.yaml / state/completion-events.jsonl）、`.agents/skills/`、T002 全部、shared canonical generator `common/_dual_pol_channel.py`、`common/_gg_time.py`、`params.py`。
- D062/D063/D064、V036/V037/V038、S079/S080（含主控 amendment）已完整读取并遵守。最高纪律 1–10 全部遵守：止于 Step 4a 维度 D，未进 Step 5/Contract/Execute。

## T003 failure reproduction

`tests/test_pilot_jones_complex_repair.py` **25 passed**：7 项 legacy-regression（import 不可变 T003 模块，**断言 BUG 存在**，PASS=缺陷复现成功；不得改 T003 让 failure 消失）+ 18 项 repair-semantic。详见 `semantic-failure-reproduction.json`（每项 old_behavior / expected_semantics / reproduced / source_line / fix）：

1. **噪声位置**（`complex_jones_channel.py:104` `r_out=J_b@r_canonical`）→ PDL 0→9.5 dB headroom bit-identical（构造恒等）。修复：component 只乘 clean，`r_out=component_op(clean)+n_post`。
2. **PDL 非无源**（`complex_jones_channel.py:142` `g=[cond,1]` σmax>1）→ 修复 `pdl_singular_values=[1,10^(-PDL/20)]`。
3. **PMD pilot 未过 FIR**（`conventional_baselines.py:78` memoryless J@atm）→ 修复 `inject_pre_channel_pilots`（TX frame 先换 pilot，整体重跑 atmosphere+component+同 n_post）。
4. **B3 tapped RX→RX 自预测**（`conventional_baselines.py:139` `rows_Y=[rx[p],ry[p]]`）→ 修复 `rows_Y=ps[:,p]`（已知 TX pilot）。
5. **PMD oracle 非 ceiling + gate 混合**（`salvage_methods.py:138-187` FDE 漏 R(theta)；`run_all.py:283` `survives=...and p1_cell`）→ 修复 `oracle_full_inverse`（逆 component+R(-theta)+√h）+ `problem_survives`/`method_succeeds` 分离。

## Signal/noise/pilot contract

见 `repair-contract.yaml` §primary_signal_chain：TX frame（先换 pilot）→ √h R(theta) clean → passive component Jones/PMD/PDL → post-component AWGN（canonical 同一 n_post draw）→ RX。component 只作用 clean signal，不碰 n_post。PDL 无源（σmax=1）。PMD FFT-circular（前向与 oracle 同约定 + PMD_GUARD=8 块边界 transient 从 metric denominator 排除，报告 excluded count）。

## Semantic gates

12 gate 全 PASS（测试化，`test_pilot_jones_complex_repair.py`）。关键工程发现（TL-22）：前向 PMD FIR 初版用 edge-padded 时域卷积、oracle 用 FFT circular，不一致致 M3/M4 oracle 恢复误差 0.49/3.9（完全错）。统一用 `pmd_circular_freq` + guard 排除后，M0–M4 noiseless 恢复误差 <1e-9（FFT-based 逆的数值 floor）。

## Baseline adjudication

B\* 每 family 在 validation 冻结，候选含 B1/B2(λ validation-optimal)/B3_pdl/B3_pmd/B3_pmd_pool/B4_fde。B2 λ validation 扫描 [1e-3,1e-2,1e-1,1.0]，冻结弱 PDL λ=0.1（critic 攻击 #5 修复）。B\*：弱 PDL=B2(λ=0.1)，强 PDL=B4_fde，弱 PMD=B1，大 PMD=B2，M4=B2。不按名字指认 B3。

## Oracle validation

`oracle_full_inverse` 逆全信道（component + R(-theta) + √h），noiseless M0–M4 恢复 <1e-9。**无 oracle anomaly**（任何 receiver-visible arm 系统性优于 oracle 都触发 ORACLE_INVALID 停机——缺陷 #5 修复后未发生）。oracle 是合法 ceiling/Kill，非 Go 对手（FR-25）。

## Problem-survival probe

problem_survives=True（verified gap >0.5 dB，**不读 P**）：
- M2 PDL 1dB（APPROX-verified）headroom=**0.77 dB**（B\* λ=0.1 冻结后；初版误报 1.02 dB），impairment-added 0.69 dB（非 floor）。
- strictly-VERIFIED DGD 6ps=0.089 dB（null）。正面裁决只基于 APPROXIMATE-verified PDL 轴。
- fresh-test stress trend 全正（PDL +0.89/+0.74/+0.44，M3 +0.11/+2.23 dB）。
- 无 oracle anomaly。

## Adaptation scan and method candidates

A1–A6 全扫（不锁死单一方法）：A1 tikhonov λ 最优随 PDL 略变但 B\*(λ=0.1) 已接近各点最优，whitening κ 全 PDL 不敏感；A2 6-pilot 下 per-block tapped 过拟合（已补 cross-block pooled 仍输）；A3 P1+B2 数学同族无增量；A4 P1 vs B2 无 crossover；A5 per-symbol error 方差 P1 仍劣 B2；A6 失效边界同。候选 P1/P1_whiten/P2/P3(joint) + B3_pmd_pool，全测。

## Conditional MVE

fresh test（8 seeds 7200–7207，全 disjoint）：P1/P1_whiten/P2/P3 无任何 8/10 胜（P2 M3 160ps stress 7/8 最高，未达门且仅 stress）。clean M0 无回归。method_succeeds=False。

## Integrity verifier

- T003 artifacts byte-unchanged（`git status` 空 diff 验证）。
- protected/shared generator/common/params 未改（`git status` 空 diff）。
- seeds disjoint：val{7100-7104} ∩ test{7200-7207} ∩ T002/T003 excluded = empty（代码验证）。
- paired：同 (cell,seed) 全 arm 共享 realization fingerprint（代码验证）。
- `git diff --check`：无 whitespace 错误。
- 25/25 测试 PASS；source SHA 链记录在 result.json。
- **bug 修复记录**：初版 test-headroom B\* lookup 用 val 名查 test summary 致空（critic 发现）；已修（`reaggregate.py` + `run_all_repair.py` val→test 映射）。

## Science critic

独立 subagent 攻击 11 项 + 1 bug。结果：verdict **SURVIVES but weakened/scoped**。已全部响应：
- #1 噪声位置（REFUTED，post-placement 合法）。
- #2 PDL 机制（PARTIAL，已改框架为"弱 PSP 噪声放大"非 conditioning）。
- #3 FFT-circular+guard（REFUTED，不抹除 ISI，under-states ISI 反而保守）。
- #4 6-pilot tapped（SUSTAINED 真过拟合；已补 pooled 仍输）。
- #5 B\* suboptimal λ（SUSTAINED；已重冻结 λ=0.1，headroom 1.02→0.77 dB）。
- #6 oracle 泄漏（REFUTED，代数+恢复误差验证）。
- #7 metric artifact（REFUTED）。
- #8 P1 是 B2 近邻（PARTIAL，已注明）。
- #9 APPROX-verified 非 VERIFIED（SUSTAINED，已重标）。
- #10 P3 未测（PARTIAL，已测 P3+B3_pmd_pool 仍输）。
- #11 D056 债（SUSTAINED，已标 blocking）。
- bug（test-headroom lookup，已修）。

## Provisional verdict and claim ceiling

**`PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL`**。claim ceiling：problem 存活（APPROX-verified PDL 轴）但无方法超越 B\*；complex axis/family 不在此包关闭（UNRESOLVED）；M4 未闭合，claim 收窄到 APPROX-verified 单轴。4 篇 D056 全文债 BLOCKED。

## Durable harvest

- **可复用**：semantic_channel 的 clean/n_post 分离 + FFT-circular PMD（前向与 oracle 同约定 + guard 排除）是"component 损伤叠加 canonical 之上"的正确模板；oracle_full_inverse（逆全信道）是 ceiling 正确实现。
- **负面/边界**：6-pilot/64 下 per-block 3-tap tapped LS 过拟合（不泛化），pooled 仍输——PMD task-matched baseline 的真实预算约束。
- **未决**：M2 PDL APPROX-verified gap 存活但无方法关闭；主控可授权下一轮更强方法候选或接受 negative。

## Changed files

新增（pilot-jones-complex-repair/）：repair-contract.yaml、semantic_channel.py、pilot_and_baselines.py、repair_methods.py、run_repair.py、run_all_repair.py、reaggregate.py、synthesis.md、semantic-failure-reproduction.json。
新增 results/pilot-jones-complex-repair/：probe_val.json、probe_test.json、result.json。
新增 tests/test_pilot_jones_complex_repair.py。
新增 worker-logs/step-004-pilot-jones-semantic-repair-retest.md（本文件）。
新增 .sessions/2026-07-10-dual-pol-osl-groundwork/S081-...。

## Protected/immutable verification

T003（explore/results/tests/salvage）零改动；protected（direction-lab/、.agents/skills/）、shared canonical generator（common/_dual_pol_channel.py、common/_gg_time.py）、params.py 零改动——`git status` 验证空 diff。

## Commands and exact results

- `python -m pytest projects/simulation/tests/test_pilot_jones_complex_repair.py -q` → **25 passed in ~2s**。
- `python run_all_repair.py`（3m，含 B2 λ-scan + 9 cell × (5 val + 8 test) seed × 12 arm）→ verdict `PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL`。
- `python reaggregate.py`（修 test-lookup bug 后从 raw 重算）→ 同 verdict，stress_added 正确填充。

## Anomaly

- B3_pmd（per-block 3-tap, 6-pilot）系统性 ~0.23–0.35 BER（过拟合，不泛化）——真实 pilot-budget 限制，已补 cross-block pooled 验证仍输；非 bug。
- P2 cond-adaptive-EMA 在 M3 160ps stress 接近 win（7/8）但仅 stress、未达门——记录，不纳入正面裁决。
- 初版误报 PDL1dB headroom 1.02 dB（B\* λ 冻结 suboptimal），critic 发现后重冻结 λ=0.1 降至 0.77 dB——已修正，仍 >0.5 dB。
