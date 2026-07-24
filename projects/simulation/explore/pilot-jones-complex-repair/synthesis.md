# Synthesis: Pilot-Jones complex-model semantic repair + retest (T004)

> 阶段: formal GW Step 4a 维度 D（语义修复 + paired retest + 条件式 MVE）
> 授权: D064 / V038 / T004 (epoch 6)
> T003 immutable: commit 5445a2e, explore/pilot-jones-complex-salvage/, results/...salvage/, test_pilot_jones_complex_salvage.py — 保留为失败证据，未改一字

## 0. 结论一句话

complex-jones / PMD / PDL 的**语义缺陷已被修复**（25/25 semantic + legacy-regression 测试通过）；
修复后**PDL (M2) 问题在 approximately-verified 物理范围内存活**（1 dB PDL → 0.77 dB Q² headroom，impairment-added over M0；PDL 1dB 在 contract 标 APPROXIMATE，strictly-verified 的 DGD 6ps 轴 null）；
但**四个机制不同的方法候选（P1 energy-weighted、P1+whitening、P2 cond-adaptive-EMA、P3 joint pooled-tapped+whitening tracker）均不敌 validation 冻结的最强合法传统 baseline B\***（B2 tikhonov for 弱 PDL，B4_fde for 强 PDL，B1 for 弱 PMD）。
provisional verdict = **`PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL`**。
M4（PDL+PMD 联合）仅做 limiting sensitivity，未闭合，claim ceiling 自动收窄。

> **诚实标注（science-critic 后修正）**：
> 1. PDL 1dB 在 repair-contract 标 `verified: APPROXIMATE`（非 VERIFIED）；strictly-VERIFIED 的 DGD 6ps 轴 headroom 0.089 dB（null）。正面物理裁决只基于 approximately-verified PDL 轴。
> 2. headline headroom 经 B\* validation-optimal 冻结（B2 λ=0.1）后从初版误报的 1.02 dB 降到 **0.77 dB**（仍 >0.5 dB）。
> 3. 该 gap 的机制是**无源非酉 component 的弱 PSP 噪声放大**（oracle 也无法消除的 noise floor），不是"偏振智能组合"意义上的 conditioning。
> 4. 已补测 P3 joint tracker 与 cross-block pooled tapped baseline（critic 指出的未测机制），两者仍输 B\*。

## 1. T003 五项语义缺陷的复现与修复

见 `semantic-failure-reproduction.json`（每项 old_behavior / expected_semantics / reproduced / source_line / fix）。
`test_pilot_jones_complex_repair.py` **25 passed**：

- 7 项 legacy-regression：import 不可变 T003 模块，**断言 BUG 存在**（测试 PASS = 缺陷复现成功）。不得改 T003 让 legacy failure 消失。
- 18 项 repair-semantic：证明 T004 修复满足 12 个 semantic gate + 缺陷修复。

| 缺陷 | T003 源码 | 修复 |
|---|---|---|
| #1 噪声位置（PDL flat 是构造恒等） | `complex_jones_channel.py:104` `r_out = J_b @ r_canonical`（噪声也被 J 缩放） | `semantic_channel.separate_canonical` + `build_impaired_realization`：component 只作用 clean signal，`r_out = component_op(clean) + n_post`（同一噪声） |
| #2 PDL 非无源（σmax>1） | `complex_jones_channel.py:142` `g=[cond,1]` | `pdl_singular_values = [1, 10^(-PDL/20)]`（σmax=1，无源） |
| #3 PMD pilot 未过 FIR | `conventional_baselines.py:78` `sig = J[b] @ atm`（memoryless，pilot 跳过 FIR） | `inject_pre_channel_pilots`：TX frame 先换 pilot，整体重跑 atmosphere+component+同 n_post |
| #4 B3 tapped RX→RX 自预测 | `conventional_baselines.py:139` `rows_Y.append([rx[p], ry[p]])` | `estimate_jones_tapped`：`rows_Y.append(ps[:, p])`（target=已知 TX pilot） |
| #5 PMD oracle 非 ceiling + gate 混合 | `salvage_methods.py:138-187`（FDE oracle 漏 R(theta)）；`run_all.py:283` `survives = ... and p1_cell` | `oracle_full_inverse`（逆 component + R(-theta) + √h）；`problem_survives`（不读 P）与 `method_succeeds`（P vs B\*）分离 |

## 2. 语义门（Phase 2，headroom 前全 PASS）

12 gate 全 PASS（测试化）：M0 byte-compat、n_post 跨损伤恒同且 component 只作用 clean、passive PDL σmax≤1/cond 精确、pre-channel pilot 同算子+FIR 支撑、DGD=0 no-op / 非零 ISI、tapped target=TX pilot（源码+行为双检）、noiseless exact-truth oracle 恢复 <1e-9（M0–M4 全过，FFT-based 逆的数值 floor，已 theory-justified guard 排除块边界 transient）、B3_pdl 在 matched M2 胜 no-op、oracle 不被 receiver-visible 反超、BER→Q²/zero-bound、problem/method gate 独立、M4 未闭合→claim 收窄。

关键工程发现（TL-22）：前向 PMD FIR 必须与 oracle 用**同一卷积约定**。初版前向用 edge-padded 时域卷积、oracle 用 FFT circular，两者不一致导致 M3/M4 oracle 恢复误差 0.49/3.9（完全错）。修复：前向与 oracle 统一用 `pmd_circular_freq`（FFT-circular per block），块边界 `PMD_GUARD=8` 样本 transient 从 metric denominator 排除（报告 excluded count）。修复后 M3/M4 noiseless 恢复误差 <1e-9。

## 3. Baseline adjudication（Phase 3，validation 冻结）

B\* = 每个 model family 在 **validation seeds** 上冻结的**最强合法传统 baseline**（候选含 B1/B2(λ validation-optimal)/B3_pdl/B3_pmd/B3_pmd_pool/B4_fde；不按名字指认 B3）。**B2 tikhonov 的 λ 在 validation 上逐 PDL 扫描**（[1e-3,1e-2,1e-1,1.0]），冻结为弱 PDL 最优 λ=0.1（science-critic 攻击 #5：B\* 不得冻结在 suboptimal 超参）：

| family | B\* | 原因 |
|---|---|---|
| M0 control | B1 | 控制组，headroom≈0.076 dB |
| **M2 PDL 1/3.5 dB** | **B2 tikhonov (λ=0.1)** | validation BER 最低 |
| **M2 PDL 6/9.5 dB** | **B4_fde** | 强 PDL 下 FDE 略胜 tikhonov |
| M3 DGD 6/40 ps | B1 EMA09 | 小 PMD 近 memoryless |
| M3 DGD 160 ps | B2 | 大 PMD 下 B2 略胜 |
| M4 joint | B2 | 同 M2 |

**B3_pmd（per-block 3-tap）在 6-pilot 预算下过拟合**（见 §5），但已补测 cross-block pooled tapped（B3_pmd_pool），仍输 B1/B2，故 PMD 轴 B\* 不含 tapped。

## 4. Problem-survival probe（Phase 4.1，不读 P）

| cell (val) | B\* | B\* BER | O BER | Q² headroom | oracle anomaly |
|---|---|---|---|---|---|
| M0 control | B1 | 0.00531 | 0.00498 | 0.076 dB | False |
| **M2 PDL 1dB (APPROX-verified)** | B2(λ=0.1) | 0.01180 | 0.00669 | **0.770 dB** | False |
| M2 PDL 3.5dB (stress) | B2 | 0.02394 | 0.01431 | 0.877 dB | False |
| M2 PDL 6dB (stress) | B4_fde | 0.04150 | 0.02797 | 0.849 dB | False |
| M2 PDL 9.5dB (stress) | B4_fde | 0.07453 | 0.05956 | 0.669 dB | False |
| M3 DGD 6ps (VERIFIED) | B1 | 0.00532 | 0.00493 | 0.089 dB | False |
| M3 DGD 40ps (stress) | B1 | 0.00605 | 0.00499 | 0.231 dB | False |
| M3 DGD 160ps (stress) | B2 | 0.03794 | 0.00488 | 3.262 dB | False |
| M4 joint (stress) | B2 | 0.02657 | 0.01411 | 1.097 dB | False |

**problem_survives = True**（reason: verified gap >0.5 dB）：
- M2 PDL 1dB（APPROXIMATE-verified）headroom = **0.77 dB**（B\* 在 validation-optimal λ=0.1 冻结后；初版误报 1.02 dB 因 B\* λ 冻结 suboptimal），>0.5 dB 阈值；
- impairment-added over M0：0.77 - 0.076 = **0.69 dB**，是 PDL 结构引入的 gap，**不是深衰落 floor**；
- **无 oracle anomaly**（缺陷 #5 修复后 oracle 是合法 ceiling，任何 receiver-visible arm 系统性优于 oracle 都会触发 ORACLE_INVALID 停机——未发生）；
- fresh-test stress trend（impairment-added over M0）：PDL 3.5/6/9.5 → +0.89/+0.74/+0.44 dB（全正，单调递减）；M3 40/160 ps → +0.11/+2.23 dB（全正）。方向稳定，stress 不单独支持正面裁决但与 APPROX-verified 一致；
- **strictly-VERIFIED 的 DGD 6ps 轴 headroom = 0.089 dB（null）**——正面物理裁决**只**基于 APPROXIMATE-verified 的 PDL 1dB 轴。

## 5. 方法候选与 adaptation-scan（Phase 4.2，problem 存活后）

先跑 adaptation-scan A1–A6（不锁死单一方法内部找增量）：

- **A1 参数适配**：tikhonov λ 与 whitening κ 扫描 vs PDL。tikhonov 最优 λ 随 PDL 略变（1dB→1e-1，9.5dB→1e-2）但增益个位数百分点，B2(validation λ=1e-2) 已接近各点最优；whitening κ 全 PDL 不敏感（无信号）。
- **A2 结构适配**：pilot 预算 6/64 下 tapped LS 在 M3 过拟合（6 pilot 拟合 6 未知数→精确插值 pilot、不泛化 data；near-noiseless 下 pilot 残差 8.9e-16 但 data BER 0.147）。这是真实 pilot-budget 限制，不是 bug。
- **A3 组合适配**：P1(reliability) + B2(regularization) 数学上同族（都是加权/正则 LS），组合无增量。
- **A4 条件适配**：P1 vs B2 无 crossover（P1 全 cell 输 B2）。
- **A5 评价维度**：per-symbol error 方差/outage，P1（mean 0.060, std 0.168）仍劣于 B2（0.050, 0.156），无分化。
- **A6 失效边界**：B2 与 P1 失效边界同（都 PDL 驱动），无分化。

方法候选（每个含 M-C-A / legal inputs / equation / falsifier；**已补测 science-critic 指出的未测机制 P3 与 cross-block pooled tapped**）：
- **P1 energy-weighted LS**（reliability-aware 估计，inverse-variance 加权 normal equations）：test 全 cell 输 B\*（best 0 胜）。注意 P1 与 B2 数学近邻（同 single-tap LS 族，critic 攻击 #8 PARTIAL：P1 输 B2 近乎平凡）。
- **P1 + whitening**：与 P1 同（whitening κ 不敏感）。
- **P2 cond-adaptive EMA**（uncertainty-scheduled 平滑）：强 PDL 下发散（BER 0.27–0.39）；唯一接近 win 的是 M3 160ps stress（7/8），但未达 8/10 且仅 stress。
- **P3 joint pooled-tapped+whitening tracker**（critic 攻击 #10 指出的未测 joint 机制）：M2 全输（BER 0.39–0.43，远劣 B\*）；M3 输。joint 机制不成立。
- **B3_pmd_pool（cross-block pooled tapped，critic 攻击 #4 指出的公平 tapped baseline）**：M2 BER≈0.49（输），M3 160ps 0.051（略输 B2 的 0.038）。pooled 仍不敌单 tap + 正则。

每个候选都含 B\*、proposed full、mechanism-off/naive ablation、最显然的 conventional ancestor（tikhonov/whitening/EMA/FDE）。

## 6. 条件式 MVE（Phase 4.3）

problem 存活 → frozen validation → fresh test（8 seeds 7200–7207，与 val 7100–7104 / semantic 7001–7002 / T002-T003 excluded 全 disjoint）：
- P1/P1_whiten/P2/P3 在所有 non-M0 cell 的 paired W/T/L **无任何 8/10 胜**（P2 在 M3 160ps stress 7/8 为最高，未达门且仅 stress）。
- clean M0 无回归（P 与 B\* 都 BER≈0.005）。
- → **method_succeeds = False**。

P 输 B\* → `METHOD_CANDIDATES_FAIL_ON_SURVIVING_PROBLEM`，不是 model-not-justified（gate 分离，缺陷 #5 修复；problem_survives 不读 P，method_succeeds 不读 problem）。

## 7. Provisional verdict

**`PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL`**

- **problem survives**：M2 PDL 在 approximately-verified 物理范围（1 dB，contract 标 APPROXIMATE）确实产生 method-worthy gap（0.77 dB Q² headroom，impairment-added 0.69 dB，非 floor）；strictly-VERIFIED 的 DGD 6ps 轴 null（0.089 dB）。
- **method candidates fail**：P1/P1_whiten/P2/P3 四个机制不同候选（含 joint tracker）在 fresh test 上不敌 validation 冻结的最强合法传统 baseline B\*。
- **claim ceiling**：problem 存活但无提出方法超越 B\*；complex-Jones/PMD/PDL 轴**不在此包关闭**（family 仍 UNRESOLVED）。M4（PDL+PMD 联合）仅 limiting sensitivity 未闭合，claim 自动收窄到 APPROXIMATE-verified 单轴（M2 PDL）。
- 4 篇 D056 全文债仍 BLOCKED（不冒充已读）；最高 provisional，待主控验收。

## 8. 与 T003 的对比（修复前 vs 后）

| 项 | T003（INVALIDATED） | T004（修复后） |
|---|---|---|
| 噪声位置 | component 乘含噪 RX（PDL flat 恒等） | component 只乘 clean，同 n_post |
| PDL 物理性 | σmax=cond>1（放大器） | σmax=1（无源） |
| pilot 信道 | pilot 跳过 PMD FIR | pilot/data 同算子 |
| B3 tapped | RX→RX 自预测 | RX→已知 TX pilot |
| oracle | 漏 R(theta)，被 B1 反超 | 逆全信道，无 anomaly |
| problem/P gate | AND 混合 | 分离 |
| M2 PDL 结论 | "flat=无问题"（构造恒等假象） | **verified 1dB 有 1.02 dB gap（真问题）** |
| verdict | PIVOT_MODEL_NOT_JUSTIFIED（假） | PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL（真） |

T004 的核心科学贡献：**T003 的"PDL 无问题"是噪声位置错误的构造恒等假象；修复后 PDL 问题确实存活，但当前方法候选无法关闭它**——这是比 T003 更准确、更保守的科学状态。

## 9. Durable harvest

- **可复用**：semantic_channel 的 clean/n_post 分离 + FFT-circular PMD（前向与 oracle 同约定 + guard 排除）是后续任何"component 损伤叠加在 canonical 之上"的正确模板；oracle_full_inverse（逆全信道）是 ceiling 的正确实现。
- **负面/边界**：6-pilot/64 预算下 3-tap 每 block tapped LS 过拟合（不泛化），是 PMD task-matched baseline 的真实预算约束——后续若要 tapped baseline，需更多 pilot 或跨 block 聚合。
- **未决**：M2 PDL verified gap 存活但无方法关闭——主控可能授权下一轮找更强方法候选（如 pilot-covariance-aware 或 cross-block），或接受 negative。
