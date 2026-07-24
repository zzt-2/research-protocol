# Synthesis — Pilot-Jones component TEMPORAL SEMANTICS adjudication (T005)

> 阶段: formal GW Step 4a 维度 D (temporal-semantics adjudication)
> 授权: D065 / V039 / T005 (epoch 7, PILOT_JONES_TEMPORAL_SEMANTICS_ADJUDICATION_PACKAGE)
> 范围: 只闭合 component temporal semantics、deterministic seed/SHA、contract/result 闭包，
>        并在 fixed/有来源慢变 component 下完成 M0/M2/M3 正式 headroom 裁决。
>        **不找新方法；不进 Step 5/Contract/Execute。**

## 1. 做了什么 (scope)

在一个 GLM 对话内，对 Pilot-Jones complex-component rescue axis 完成时间语义终审：

1. **Phase A — V039 四项失败复现**（不动 T003/T004 源码，只 import 不可变 T004 模块）：
   - T004 `build_jones_truth` 每 64 symbols (=25.6 ns) 独立重抽 U/V → 相邻 block 不同（reproduced）。
   - T004 `run_repair.make_realization_imp` 的 RNG seed 含 `hash(model_id)` → 两个独立 subprocess 同 seed/model/params fingerprint 不同（reproduced，实测 `0318bcd6…` vs `1faa60a4…`，hash 值 `8784…` vs `-4384…`）。
   - T004 contract N=50000 vs runner N=20000、10 vs 8 test seeds、`contract_sha256` 是文件名字符串不是 hash（reproduced）。
   - V039 固定器件反事实：5 seeds 平均 impairment-added headroom = **0.066 dB**（远低于 0.77 dB iid-block 伪影和 0.5 dB 门），方向与 V039 一致（reproduced）。
   - 输出 `results/pilot-jones-temporal-adjudication/t004-temporal-failure-reproduction.json`。

2. **Phase B — T005 fixed-component 语义门**（全部 PASS）：
   - passive PDL σmax=1 / σmin=10^(-PDL/20)；
   - component Jones 跨整个 frame 固定（单一 2×2 矩阵）；
   - deterministic hash-free seed（`1e6 + 31·seed + MODEL_ID_INT`），同 (seed,model) 同整数；
   - DGD=0 degeneracy（M3 DGD=0 → clean_component == clean_original，err=0）；
   - noise 未被 component 触碰（err=1.6e-16）；
   - **noiseless reference recovery**: M0 err=0, M2 err<1e-9, M3 err<1e-4 → reference 是合法 ceiling（关键：修正了 M2 forward ordering 为 rotation-then-component）。

3. **Phase C/D — 正式 headroom**（contract 先冻结后跑，grid = 2 条件 × 2 pilots × 3 cells × 10 seeds）：
   - B2 λ validation 扫 [1e-3,1e-2,1e-1,1.0] → 冻结 λ=0.1；B\* = B1 (EMA09) 在全部 12 cell 胜出（B2 Tikhonov 一致更差）。
   - 无 reference anomaly（O 在所有 cell 都 ≥ B\*，合法 ceiling）。
   - impairment-added over paired M0（test 10 seeds, per-seed paired, bootstrap 95% CI 2000 resamples）：

     | cell | mean (dB) | CI95 upper (dB) | dir+ frac |
     |---|---|---|---|
     | adversarial\|p4\|M2_pdl1dB | +0.070 | +0.191 | 0.30 |
     | adversarial\|p4\|M3_dgd6ps | +0.080 | +0.237 | 0.20 |
     | adversarial\|p6\|M2_pdl1dB | +0.032 | +0.097 | 0.20 |
     | adversarial\|p6\|M3_dgd6ps | +0.025 | +0.075 | 0.20 |
     | operational\|p4\|M2_pdl1dB | +0.003 | +0.011 | 0.10 |
     | operational\|p4\|M3_dgd6ps | +0.013 | +0.043 | 0.10 |
     | operational\|p6\|M2_pdl1dB | **-0.016** | 0.000 | 0.00 |
     | operational\|p6\|M3_dgd6ps | **-0.022** | 0.000 | 0.00 |

   - **最大点估计 0.080 dB，最大 CI 上界 0.237 dB，均 ≪ 0.5 dB**。两个 operational p6 cell 的 impairment-added 为负（fixed PDL/DGD 在该 SNR 下甚至不产生 headroom）。

4. **Phase E — 预注册裁决**（裁决规则在 contract 里先写死，跑前不移动门槛）：
   - 全部 8 个 primary 非-M0 cell 的点估计 AND CI 上界均 < 0.5 dB →
     **`KILL_COMPLEX_COMPONENT_RESCUE_AXIS_TEMPORAL_PRIMARY`**。
   - 该裁决 **不关闭整个 Pilot-Jones family**，4 篇全文债继续 BLOCKED，不进 Step 5/Contract/Execute。

## 2. claim ceiling（严格）

- complex-component PDL/PMD rescue axis 在 **fixed/verified temporal model** 下不重新引入值得研究的方法级 gap；T002 的 `UNITARY_REAL_ROTATION_MCA_KILLED` 扩展到当前 fixed complex model。
- **不声称** 关闭整个 Pilot-Jones family（仍有 4 篇全文未读、M4 联合轴未闭合、其他物理救活轴未排除）。
- iid-per-block（T004 伪影）reproduction 仅作 `UNVERIFIED_STRESS_ONLY`，**无论 magnitude 多大都不触发正面裁决**。

## 3. 复现闭包（V039 三项缺陷已修）

| V039 缺陷 | T005 修复 | 证据 |
|---|---|---|
| `hash(model_id)` 跨进程不确定 | 固定整数 `1e6+31·seed+MODEL_ID_INT[model]`，无 hash() | 跨进程 fingerprint bit-identical（`51977d12…` ×2 不同 PYTHONHASHSEED） |
| contract N=50000 vs runner N=20000 | contract/runner N 同为 20000，`_assert_closure()` 在跑前强制 | `test_contract_runner_closure` PASS |
| 10-seed contract vs 8-seed runner | val/test 各 10 seeds，contract 与 runner 一致 | 同上 |
| 伪 `contract_sha256`=文件名 | 真 SHA256 of contract.yaml，raw 记录 source SHA256 | `test_real_contract_sha` PASS；8 个源 SHA 全 match |

## 4. integrity (self-verification)

- T003/T004/protected/shared generator/common/params/Skill/controller **零改动**（`git status` 仅 2 个新 T005 路径）。
- fresh pytest：T005 17 tests PASS + legacy T003(13)+T004(25)=38 tests PASS（immutability）。
- 跨进程 determinism：T005 bit-identical / T004 disagree（regression 化）。
- raw→aggregate 独立重算：全 12 cell B\*/O headroom 重算与存储一致；独立 KILL 判定与存储 verdict 一致。
- actual SHA closure：8 个源 SHA + contract SHA 全部 match 实际文件。
- B\* 在 validation 冻结（λ=0.1, B1），test 不调参。

## 5. 独立审查状态

**未使用分离上下文的独立 science critic / integrity verifier 子 agent**（单 GLM 对话执行）。因此本包的 integrity/科学结论状态最高为 **PARTIAL**（按 T005 §6 规则：独立审查不可用时不得自称"双审查 PASS"）。所有 integrity 检查由执行方在同一上下文自验完成并记录于此 + worker-log + 测试文件，可由主控独立复核。

潜在 science-critic 攻击面（执行方预列，未由独立 critic 验证）：
- fixed component 是否过度保守（under-states 真实慢变漂移）→ contract 已声明此为"bias AGAINST positive signal"，对 Kill 是保守方向。
- M3 DGD=6 ps 是否过短 → verified 范围（Valjus sat.1553，1.5% T_S）；stress DGD 未进 primary。
- B\*=B1 一致胜 B2 是否合理 → B2 λ validation-optimal=0.1 已冻结；B1 在 fixed-component 下更稳是物理预期（PDL=1 dB cond=1.12 接近恒模，EMA 平滑占优）。
- bootstrap CI 仅 10 seeds → 已诚实报告；CI 上界 0.237 dB 即使翻倍仍 <0.5 dB，不改变裁决。

## 6. durable harvest / 复用

- **可复用**：fixed-component temporal model + deterministic seed + 真 SHA closure 是"component 损伤叠加 canonical 之上"的正确闭包模板；reference_m0_m2（rotation-then-component ML over 16 pairs）+ reference_m3（PSP-basis exact inverse）是合法 ceiling 实现。
- **负面/边界**：fixed 1 dB PDL / 6 ps DGD 在 operational(20 dB)/adversarial(17 dB) 两条件、4/6 pilots 下均不产生 ≥0.5 dB 的 impairment-added headroom → 该 rescue axis 在 verified 物理范围内不成立。
- **未决**：4 篇 D056 全文债 BLOCKED；M4 联合轴未闭合；整个 Pilot-Jones family 仍 UNRESOLVED（本包只 Kill complex-component rescue axis）。

## 7. 边界遵守

- 止于 Step 4a provisional verdict；**未进 Step 5/Contract/Execute**。
- 未运行 P1/P2/P3/P4 或任何 tracker/KF/RLS/FDE"方法"候选；只比较合法 conventional B\* 与 truth-assisted reference。
- 未改 protected/shared generator/common/params/Skill/controller；未复活 Scout/P03；未 push。
- T003/T004 source/raw/result/synthesis/worker-log 全部 immutable（`git status` 空 diff 验证）。
