# Task Brief: B12 source-structured fade-reliability MAP standalone

> 来源: S001（live D018 / R005 / formal D029）
> 产出位置: `projects/thesis-fso/worker-logs/step-015-b12-map-fade-aopn-standalone.md`
> 日期: 2026-07-27
> 唯一文档: executor 只需本 T、其中列出的本地论文与仓库源码
> 状态: **WITHDRAWN_BEFORE_DISPATCH — DO NOT EXECUTE**
> 撤回依据: live D019 / formal D030 / V038 / V039 / V040

> [!CAUTION]
> 本任务从未通过独立 dispatch review，任何 section 均不得执行。原合同混淆
> iid channel block 与物理湍流生命周期，且把 Huber IRLS precision 错写为
> `w²/sigma_eps`；随后又发现 DOI `10.1109/JLT.2025.3600402` 对
> Huber robust Bayesian CPR 的 direct method-family collision。B12 已返回池，
> 不得把本文件改成第二个 repair package。

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 36
  action_class: B12_STANDALONE_METHOD_PACKAGE
  mission_checkpoint: CP014
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，formal 阶段是
**Groundwork Step 4a 维度 D**。

**任务**：在全新隔离目录中，按 B12 OECC 2025 Eq.4–7 与 Wang 等 TSP 2022
协方差定义实现 source-structured PA / PA-ML / MAP；先过结构身份与信息访问门，
再同包实现一个 receiver-visible 的 one-pass robust MAP，用 standardized phase
innovation clipping 抑制深衰落相位 outlier，并在共同 realization 上与 MAP、
cheap rule 和 generic 256-QAM BPS 做 validation-frozen paired comparison。

**产出**：

- 隔离实现与 tests：
  `projects/simulation/explore/b12-map-fade-aopn-standalone/`
- raw/aggregate/receipt：
  `projects/simulation/results/b12-map-fade-aopn-standalone/`
- worker log：
  `projects/thesis-fso/worker-logs/step-015-b12-map-fade-aopn-standalone.md`
- 一个只包含上述实现、contract 和 worker log 的 commit。

### 最高纪律（违反一条即停止）

1. 起飞先运行 task-control validator；FAIL 不修改、不运行 seed。
2. 这是 B12 standalone，禁止 import/复制
   `high-order-cpr-combination/components.py`，禁止接回 B10、coarse→MAP、
   CW pilot、联合 CFO ML 或 T006 的任何科学实现。
3. OECC 未给 PA-ML 的 `W`、pilot sequence、sample count/seed 和 penalty
   精确定义。必须标 `PROJECT_VALIDATION_ASSUMPTION`，只能主张
   `SOURCE_STRUCTURAL_IDENTITY`，禁止写 bit-exact/full-numeric reproduction。
4. pilot 和 data 必须在同一 TX 序列中、经过同一 GG/Wiener/noise realization；
   所有方法消费同一个不可变 realization 对象。禁止按方法重生信道。
5. deployable 方法只能读 `rx`、known pilot/pilot mask、冻结参数和过去/当前
   receiver-visible 状态；不得读 tx bits/symbols、true phase、true h、seed 标签。
   truth 只在 evaluator 中计算 BER/phase diagnostics。
6. 先完成所有实现与测试，再运行 source-like structural smoke。smoke FAIL 立即
   停止，不能改公式、W grid、pilot、seed 或 gate；不得进入 primary validation/test。
7. primary 必须先完整跑 validation、按冻结规则选设置，再一次性跑 test。
   看到 test 后不得改算法、参数、SNR 网格、方法集合、指标或 gate。
8. 测试 PASS、source identity、metadata closure、negative result 和 worker-log
   完成都不是方法产出。executor 只给 evidence，不拥有科学 verdict。
9. 不修改 `projects/simulation/common/`、`projects/simulation/params.py`、
   `毕设/`、任何 current/formal owner、mission-log、RDL Skill 或旧实验目录。
10. 任一结果比理论预期好或坏超过 3×，在 receipt 标 `EXPECTATION_BREACH` 并
    停在 evidence，不写方法结论。

---

## 1. 背景与科学身份

### 1.1 为什么这是新 carrier

T006 的 B10+B12 combination 因 B10 source identity、B12 公式自行重构、
pilot/data 异通道、oracle/evaluator 和 statistics 同时失效，被 formal D013
标为 `UNRESOLVED_IMPLEMENTATION_INVALID`；没有 Kill B12 family。本任务不得
修 T006，只能从下列原文与独立代码重新开始。

### 1.2 权威本地全文

1. OECC 2025：
   `D:\code\study\research-protocol\papers\doi\10.23919_oecc-psc62146.2025.11109607\source.pdf`
   - Eq.4–7：PDF 第 2 页；
   - 数值/排序：PDF 第 3 页；
   - SHA256 必须在 source closure 中重算并记录，已知前缀/后缀
     `A8340228…19F8255` 只作核对，不可硬编码代替重算。
2. Wang et al., IEEE TSP 70:337–350 (2022)，DOI
   `10.1109/TSP.2021.3137966`：
   `D:\code\study\research-protocol\papers\doi\10.1109_tsp.2021.3137966\source.pdf`
   与同目录 `content.md`。
3. 现有 B12 结构化笔记：
   `D:\code\study\research-protocol\papers\_read_notes\_B12-freq-domain-pilot-increment.md`
   只能帮助定位，公式仍以 PDF 为准。

### 1.3 可闭合与不可闭合

必须在 `source-closure.yaml` 逐项记录：

- OECC Eq.4：
  \(\varphi_{PA}=\angle(S_{PA}^{*}R_{PA})\)，每 block 首符号为已知 pilot，
  用粗相位旋转全 block；
- Eq.5：对 \(2W+1\) 窗的
  \(\angle(\hat S^{*}(k)R_{PA}(k))\) 平均；`W` 未给；
- Eq.6：
  \[
  \hat\theta_0=
  \frac{\mathbf1^T\Sigma_\varphi^{-1}\varphi}
       {\mathbf1^T\Sigma_\varphi^{-1}\mathbf1},\quad
  \hat{\boldsymbol\theta}=
  \Sigma_\theta(\Sigma_\theta+\Sigma_\epsilon)^{-1}
  (\varphi-\hat\theta_0\mathbf1);
  \]
- Eq.7：
  \(\varphi_{sub}=\varphi_{PA}+C\Delta\varphi\)，相邻符号相位差由下三角
  \(C\) 累积，`a=conj(S_hat) ⊙ R_sub` 用于 subblock 重构；
- TSP [5]：
  \(\theta(0)=0\)，
  \([\Sigma_\theta]_{ij}=\min(i,j)\sigma_p^2\)，
  \(\Sigma_\epsilon\) 为 AOPN 对角阵，单正弦元素
  \(N_0/[2A|r(k)|]\)。

QAM 适配必须显式声明：

- 对 `a=conj(S_hat)*R_sub`，本项目用平均 `Es=1` 的判决辅助等效映射
  `sigma_eps = N0 / (2*max(abs(a), numerical_epsilon))`；
- 这是 `PROJECT_QAM_AOPN_MAPPING_ASSUMPTION`，不是 OECC 明写的完整归一化；
- `W`、pilot 值、random sample/seed、penalty reference 均是
  `PROJECT_VALIDATION_ASSUMPTION`；
- 这些债务限制 claim ceiling，但不允许 executor另找参数让结果变好。

### 1.4 正向方法

`ROBUST_MAP_HUBER1`：

1. 先用 source-structured MAP 得到一次相位估计；
2. 计算 wrapped receiver-visible observation residual；
3. 用
   `u_k=abs(residual_k)/sqrt(max(sigma_eps_k, eps))`，
   `w_k=min(1, c/max(u_k, eps))`；
4. 将 `sigma_eps_k` 一次性膨胀为 `sigma_eps_k / w_k**2`，只重算一次 MAP；
5. `c` 只在 validation grid 冻结；不得读取 truth 或 test。

物理假设：深衰落时 phase observation 由近高斯变成重尾/outlier；one-pass
standardized clipping 防止异常 observation 对 MAP 造成过度影响。它是有界
robust adaptation，不是反复迭代调参。

---

## 2. 实现边界

### 2.1 新目录与文件

只允许新建：

```text
projects/simulation/explore/b12-map-fade-aopn-standalone/
  __init__.py
  config.py
  qam256.py
  shared_realization.py
  source_map.py
  methods.py
  baselines.py
  evaluator.py
  run_all.py
  source-closure.yaml
  contract.yaml
  seed-census.yaml
  MVE-SPEC.md
  tests/
    test_b12_map_fade_aopn.py
```

以及结果目录与 worker log。若确需额外隔离 helper，先在 worker log 说明理由；
不得修改 shared/old code。

### 2.2 参数真相源

- primary `R_SYM`、`LASER_LW`、GG weak/moderate/strong 参数、`BLOCK`
  均从 `projects/simulation/params.py:SimulationConfig` 读取；
- source-like transfer 固定 `R_SYM=100e9`、`linewidth=150e3`、256-QAM、
  AWGN+Wiener、`L_block=128`、`L_sub=1`，并标
  `SOURCE_REPORTED_STRUCTURE / PROJECT_NOISE_NORMALIZATION`；
- primary 固定 CFO=0（pre-compensated），不得新增 Doppler/CFO estimator；
- EsN0 定义以未衰落、Gray square-256QAM、平均 `Es=1` 为参照：
  `n=sqrt(1/(2*gamma))*(N_r+jN_i)`，`E|n|²=1/gamma`；
- GG field amplitude 只乘 `sqrt(h)`，不按 realized mean(h) 或 waveform power
  renormalize，不做 AGC。

新 `config.py` 用 frozen dataclass + derived fields；不得硬编码散落常量。

### 2.3 256-QAM 与 pilot

- 实现一般 square-256QAM Gray mod/demod，平均 Es=1；
- roundtrip、Gray adjacent mapping、mean-power 和 hard-decision tests 必须过；
- 每 128-symbol block 的 index 0 是 known pilot；pilot 固定为单位功率
  `(1+1j)/sqrt(2)`，标 `PROJECT_VALIDATION_ASSUMPTION`；
- data bits 只对应非 pilot positions；BER 分母只含 data bits；
- pilot/data 在写入同一 TX array 后一次通过 channel。

### 2.4 方法与 evaluator 的信息边界

所有 deployable API 接收一个只含以下字段的 frozen view：

```text
rx, pilot_mask, known_pilots, noise_variance, block_length,
subblock_length, symbol_rate, linewidth
```

禁止 tx bits/symbols、true phase/h、seed、GG label。evaluator 单独持有 truth，
只在方法返回后计算：

- data-only BER；
- per-128-block BER 与 outage；
- wrapped phase RMSE（diagnostic only）；
- nonfinite/solve failure/condition number。

BPS 用同一 RX、同一 block 和 pilot 做 π/2 ambiguity alignment；禁止 TX-truth
resolve。BPS 只实现通用 256-QAM、CFO-precompensated feed-forward 版本。

---

## 3. 前置测试与理论预期

### 3.1 未运行 seed 前必须通过的 tests

至少覆盖：

1. qam256 roundtrip、Es=1、Gray adjacency；
2. sigma2 phase innovation `2π linewidth / R_SYM`；
3. Sigma-theta exact `min(i,j)*sigma_p²`；
4. constant/noiseless phase：PA/PA-ML/MAP 误差接近 0；
5. Eq.6 使用 solve，不显式 matrix inverse；finite/PSD/symmetry；
6. pilot 和 data 的 channel/noise object identity 一致；
7. 相同 realization 被所有方法复用，方法调用不改变对象；
8. deployable signature 不含 truth，运行时 truth-access trap 必须触发失败；
9. 两个仅 receiver-visible residual 不同的输入产生不同 Huber weight/output；
10. residual 全为 0 时 robust MAP 与 MAP 数值退化一致；
11. fixed-variance、hard-skip 与 Huber robust 是三个不同输出动作；
12. BPS noiseless 256-QAM BER=0 且只用 pilot 解全局 π/2 ambiguity；
13. BER denominator/data mask 精确一致；
14. result writer 使用 `common._experiment.save_results` 并含 git/hash/contract
    metadata；
15. test/validation seed census exact-token 与 task-control validator。

### 3.2 跑前理论预期（TL-20/TL-22/TL-26）

写入 `MVE-SPEC.md`，不得事后改：

- source-like AWGN+Wiener：aggregate 定性排序应为
  `MAP <= PA-ML <= PA`（BER 越低越好）；OECC 的约 4/5/7.5 dB 只能作趋势锚，
  因 W/pilot/penalty 口径缺失，不能作数值 gate；
- robust MAP 在 flat/source-like 条件不应比 MAP 好很多；BER 改善超过 3× 或
  SNR gain >3 dB 首先视为 bug；
- robust 增量若存在，应集中在 moderate/strong GG、near-working-region 和
  phase outlier/outage，而非所有 SNR/GG 一致大胜；
- noiseless/高 SNR 无衰落应 BER≈0，robust 与 MAP 退化接近；
- BPS 是强传统 comparator；若 robust 在所有条件远胜 BPS，先检查 BPS identity、
  π/2 resolve、pilot/data denominator 和 noise normalization；
- 若所有方法 BER≥0.2 或没有共同工作区，不得用 Q²/proxy dB 制造 crossing。

---

## 4. 冻结执行协议

### 4.1 起飞检查

在任何 seed 前：

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T015-b12-map-fade-aopn-standalone.md
git status --short
```

必须：

- validator PASS；
- tracked worktree clean；
- HEAD 等于 dispatch receipt 冻结的 commit；
- source PDF/hash、task、owner pointer、params/common dependency hashes 写入
  `contract.yaml`；
- exact-token census 证明执行前 seeds `72727001–72727020` 在仓库中均为 0；
  本 T 自身出现不计，census 必须记录排除本 T 后的结果。

### 4.2 Phase A — structural identity smoke

固定：

- AWGN+Wiener、256-QAM、100 GBaud、150 kHz；
- `L_block=128`、`L_sub=1`；
- EsN0 `[32,35,40] dB`；
- seeds `72727001–72727005`；
- PA-ML `W` project grid `[2,4,8,16]`。

运行顺序固定为 SNR → seed → W → method。每个 `(SNR,seed)` 只生成一个
realization。

全量完成后，用下列预注册规则冻结一个 W：

```text
score(W) = (
  nonfinite_or_solve_fail_rows,
  rows_where_MAP_BER > PA_ML_BER,
  rows_where_PA_ML_BER > PA_BER,
  total_MAP_bit_errors,
  W_grid_index
)
```

全部从小到大。structural identity PASS 还必须满足：

- formula/tests 15/15 PASS；
- frozen W 的 aggregate mean BER 在至少 2/3 SNR 上满足
  `MAP <= PA-ML <= PA`；
- 所有方法 finite，无 truth access；
- pilot/data/data-mask identity 全过。

否则 receipt =
`BLOCKED_SOURCE_STRUCTURAL_IDENTITY`，禁止 Phase B/C，直接写 worker log 和
commit。此时 `mission_method_delta` 建议只能是 `NONE`。

### 4.3 Phase B — primary validation freeze

仅在 Phase A PASS 后运行。

固定 primary：

- `R_SYM=cfg.system.R_SYM`、`LASER_LW=cfg.system.LASER_LW`；
- GG `[weak,moderate,strong]`，参数只从 `SimulationConfig`；
- EsN0 `[24,28,32,36,40,44] dB`；
- `n_symbols=32768`（256 blocks × 128）；
- validation seeds `72727006–72727010`；
- frozen W from Phase A。

方法/setting：

- PA；
- PA-ML(frozen W)；
- MAP；
- FIXED_VAR_MAP（block 内用 receiver-visible median `sigma_eps`）；
- HARD_SKIP_MAP，threshold
  `abs(a)/sqrt(N0) < [1.0,2.0,3.0]` 时 observation precision=0；
- ROBUST_MAP_HUBER1，`c=[1.5,2.0,3.0]`；
- BPS256，window `[31,63,127]`、64 test phases。

每个 `(GG,SNR,seed)` 只生成一个 realization；先跑全部 setting，全部完成前不得
查看局部排名或冻结。每 family 全局 setting score：

```text
(
  nonfinite_or_solve_fail_rows,
  BER_ge_0p2_rows,
  data_bit_errors_total,
  block_outage_count_at_3p8e_3,
  preregistered_setting_index
)
```

全部从小到大。冻结 HARD_SKIP、ROBUST 和 BPS 各一个全局 setting；不得按 GG/SNR
分条件选参。

### 4.4 Phase C — fresh test

validation freeze 原子写入且 hash 固定后，使用：

- 同一 primary grid；
- test seeds `72727011–72727020`；
- 只运行 PA、PA-ML、MAP、FIXED_VAR_MAP、frozen HARD_SKIP、
  frozen ROBUST、frozen BPS；
- 不再运行/选择其他 setting。

不得 resume 到非前缀 key。raw canonical key 固定：

```text
[phase_index, gg_index, snr_index, seed_index, method_index, setting_index]
```

Phase A/B/C 分开 raw；每次保存必须原子写、前缀 deep-equal、source/contract/code
hash 完整。任何 stale/hash/prefix/duplicate/gap 返回
`BLOCKED_STALE_OR_CORRUPT_CHECKPOINT`，不得修补或覆盖。

---

## 5. 预注册判读

executor 必须计算证据，不得自行最终裁决。

### 5.1 common working region

一个 `(GG,SNR)` 只有在 test 10 seeds 上 MAP、cheap HARD_SKIP 和 BPS 的 aggregate
BER 都 `<0.2` 且 finite，才可用于方法性能比较。无共同区时只能报 boundary。

### 5.2 HD-FEC required EsN0

- target BER=`3.8e-3`；
- 只在同一方法随 SNR aggregate BER 单调且两相邻点 bracket target 时，对
  `log10(BER)` 做线性插值；
- 无 bracket 返回 NaN，不得用 Q²、BER slope extrapolation 或 dB-equiv proxy。

### 5.3 METHOD_SIGNAL 的两个预注册入口

满足 clean/source-like 退化门后，以下任一入口可成为 verifier 考虑的
`METHOD_SIGNAL`，但仍需独立科学验收：

**A. crossing gain**

- 至少一个 GG 档中，ROBUST 的 required EsN0 相对
  `max-strength comparator = min(required MAP, HARD_SKIP, BPS)` 改善
  `>=0.5 dB`；
- paired seed bootstrap 95% CI 的 BER-difference 方向支持 ROBUST；
- 其他有共同 crossing 的 GG 档退化不超过 `0.2 dB`。

**B. outage gain**

- 在 moderate 或 strong GG 的至少两个相邻 SNR 点，ROBUST 相对 MAP、
  HARD_SKIP、BPS 三者都同时减少 block outage；
- 每个点相对改善 `>=20%` 且绝对改善 `>=0.01`；
- paired bootstrap 95% CI 对三项比较均不跨 0；
- 同点 aggregate BER 不恶化。

两入口都不满足：

- 已创建方法并完成公平 test → executor 建议
  `FAIR_COMPARISON_RUN`；
- 只胜 MAP 但不胜 cheap/BPS → 建议 `PACKAGING_BOUNDARY`；
- source/identity/working-region 失败 → method delta 建议 `NONE`。

禁止把 test PASS、negative、identity、代码资产或 boundary 单独写成
`METHOD_SIGNAL`。

### 5.4 统计与归因

- 所有比较 paired by exact realization；
- 报 per-seed、aggregate、median/IQR、paired bootstrap 95% CI；
- 独立列出 outlier contribution，任何单 seed 贡献总 gain >50% 标红；
- 报 clean/source-like、weak/moderate/strong 分层，不混成一个总体数；
- 从 raw 重算 aggregate，aggregate 不得只有 summary；
- executor 的因果解释标 `HYPOTHESIS`，主控/verifier 会独立重算。

---

## 6. 产出格式

### 6.1 receipt

`receipt.json` 至少包含：

```json
{
  "task_control": "PASS",
  "head_at_start": "...",
  "source_pdf_sha256": {},
  "phase_a_status": "...",
  "phase_b_status": "...",
  "phase_c_status": "...",
  "source_identity_ceiling": "SOURCE_STRUCTURAL_IDENTITY_ONLY",
  "project_assumptions": [],
  "frozen_settings": {},
  "raw_paths": [],
  "raw_sha256": {},
  "tests": {"passed": 0, "failed": 0},
  "simulation_or_seed_run": true,
  "expectation_breach": false,
  "suggested_formal_science_disposition": "...",
  "suggested_mission_method_delta": "...",
  "method_signal_entry_a": false,
  "method_signal_entry_b": false,
  "stop_reason": "...",
  "commit": null
}
```

### 6.2 worker log

必须按以下标题：

```markdown
# Step 015 — B12 MAP fade-AOPN standalone

## 0. 回执
## 1. 修改边界与 commit
## 2. Source closure 与 project assumptions
## 3. 公式/信息访问/共享 realization identity
## 4. Phase A structural identity
## 5. Phase B validation freeze
## 6. Phase C fresh test
## 7. Raw 重算与 statistics
## 8. METHOD_SIGNAL 两入口逐项证据
## 9. formal_science_disposition 建议
## 10. mission_method_delta 建议
## 11. 理论预期偏离与替代解释
## 12. 可复用资产、不可用结论与下一轮换点
```

明确写：

- executor 建议不是最终科学验收；
- test/governance/negative/boundary 不是方法；
- 是否触发第二包禁令：无论结果如何都写
  `NO_SECOND_B12_REPAIR_PACKAGE`。

### 6.3 commit

运行 `git diff --check`、定向 tests、raw deterministic re-aggregation、
forbidden-path diff 和 task-control validation 后，只提交：

- 新隔离目录；
- Step 015 worker log；
- 若 results 被 gitignore，receipt/raw 只留 hash 与路径，不强行提交。

不得提交 owner/control/mission-log 的改动。commit 后把完整 SHA 写回 receipt；
如 receipt ignored，只更新本地 receipt，不再为 receipt 单独建第二 commit。

---

## 7. 验收 checklist

- [ ] task-control/HEAD/binding clean；
- [ ] source PDF hash 与 Eq.4–7/TSP covariance 可复核；
- [ ] W/pilot/noise/penalty 明示为 project assumptions；
- [ ] T006/B10/CW/联合 CFO 路径完全未复用；
- [ ] qam256/公式/no-truth/shared-realization tests 全过；
- [ ] source-like 只作 structural identity，不冒充数值复现；
- [ ] Phase A FAIL 时未运行 primary；
- [ ] validation/test seed 与 settings 严格隔离；
- [ ] primary 所有方法共同 TX/pilot/data/noise/h/phase；
- [ ] aggregate 可从 raw 独立重算；
- [ ] FEC crossing 只用真实 bracket；
- [ ] robust 同时与 MAP、cheap、BPS 比较；
- [ ] 两个 METHOD_SIGNAL 入口逐项给 raw 证据；
- [ ] expectation breach、single-seed dominance、working region 明确；
- [ ] worker log 与 commit 边界闭合；
- [ ] executor 未改任何 owner/control/mission-log。

## 附：失败后的轮换

- Phase A structural identity FAIL：`BLOCKED_IDENTITY / delta NONE`，B12 回池；
- 无共同 working region：`PACKAGING_BOUNDARY` 或 `NONE`，B12 回池；
- 公平 test 无方法增量：`FAIR_COMPARISON_RUN`，不记 METHOD_SIGNAL，B12 回池；
- METHOD_SIGNAL 入口成立：仍须独立 verifier；executor 不得自行 promotion；
- 所有分支都禁止第二个 B12 repair 包，主控自动 remap 或进入 promotion review。
