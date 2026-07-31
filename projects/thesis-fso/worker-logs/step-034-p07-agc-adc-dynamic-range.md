# step-034 — P07 F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG（新机制族 F 首包）

> 2026-07-31 | campaign P07 | family F（首包）| executor: 主线程内独立实现
> 上游：D045（binding decision，撤回旧 P07-entry F/G/H 扫描）+ D039 campaign
> 验收：V071（独立 verifier）

## 任务

binding decision D045 撤回旧 P07-entry 的 F（timing offset）/G（场景扩展）/H（FEC/APSK）
三条未冻结扫描（rejected brief，不计有效 P07），指定新 P07 =
`F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG`（candidate-universe.yaml U07，ap=AP06）：冻结接收
模拟前端可变增益 + ADC 满量程/削顶/量化分辨率。**严格区别于 P03**：P03 = selector
内部控制路径定点 Q(W,F) 数字后处理；P07 = 模拟前端 AGC+ADC 作用于 `rx_raw` 在整个冻结
接收链**之前**。

## 冻结问题定义（M-C-A，读结果前冻结，见 FROZEN_CONTRACT.md）

- **M**：冻结接收链（`run_case_multidelta` per-window：blind/pilot MMSE + `A.per_block`
  + `A.decide` + `S.ber_oracle_turb`）。固定增益、固定满量程、有限位宽 I/Q ADC 接在模拟前端。
- **C**：源闭合 GG 动态幅度（`generate_shared_realization_apsk`，α,β∈{weak/moderate/strong}，
  SNR 5/9/13/17/21 dB，N_DFT=256/block，400 windows/cell，f_dot=150e6，mod='m16apsk'，
  SEED_TURB0=2000）。深衰落（低 h）与强峰值（高 h）时间交替。
- **A**：固定增益在两损害间折中——过高→峰值 clipping，过低→深衰落有效量化分辨率不足。
  问：该矛盾是否真实产生接收性能损失，能否被标准因果 AGC 解决，robust/clipping-aware
  AGC 是否还有可区分增量。

## Phase 0：可信因果 AGC/ADC adapter（ALL 5 BLOCKER gates PASS）

信号链：`channel float rx_raw → gain(由过去样本决定) → I/Q rail clip(±FS) → 有限位宽
uniform signed I/Q ADC → 量化 raw → 冻结接收链`。

signed I/Q quantizer：`code=clip(round_half_up(gain·value/step), ±(2^(W-1)-1))`，
`step=2·FS/2^W`，重建 `q=code·step`；饱和不 wrap。

五门全过（`p07_phase0_smoke.json`）：
- **G1 ADC math**：round-half-up（+0.5LSB→+1，-0.5LSB→0）、饱和不 wrap（W4 100·FS→7 非 -8）、
  signed 对称（±0.3 → ±38 @W8）。
- **G2 float-bypass 重构**：W=64 + FS=1e6 重构误差 ≤ 2^-40（实测通过）。
- **G3 float-bypass 接收链身份**：FixedGainAGC(g=1,W=64) 与原 `run_case_multidelta` 逐 cell
  byte-identical（0 mismatch，weak/mod/strong × {5,9,15,21} × seeds{0,1,2}）。
- **G4 因果性**：window-0 = nominal，gain 随过去 RMS 单调（小 RMS→大 gain），确定性重放。
- **G5 信息边界 AST**：`_p07_adapters.py` 所有 AGC class 体 + `quantize_iq` 体零 forbidden
  子串（h/alpha/beta/tx/phi/bits/oracle/future）。

## Phase A：问题成立 → fixed-gain 稳定跨位宽实质 regret

dev 前冻结（FROZEN_CONTRACT §4）：MDE=0.15 dB；≥3 cell 过门；跨 {6,8,10}bit 一致；
fixed-gain ladder {0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0}；dev grid = 3 scenes × 5 SNR
{5,9,13,17,21} × dev seeds {0..4} = 75 cells（代表性子集，5 SNR 跨低-中-高，非单点）。

结果（`p07_phaseA_dev.json`，dev-best gain 全选 0.75）：

| W | best gain | pooled regret (dB) | CI95 | cells ≥MDE |
|---|---|---|---|---|
| 6  | 0.75 | **+1.028** | [+0.886, +1.170] | 15/15 |
| 8  | 0.75 | **+0.924** | [+0.799, +1.049] | 14/15 |
| 10 | 0.75 | **+0.909** | [+0.788, +1.031] | 14/15 |

**问题成立**：dev-tuned 最佳固定增益在源闭合 GG 下有**稳定、跨位宽、远超 MDE 的实质
regret**（+0.91~+1.03 dB，6.5×~7×MDE；CI_low 全 >0；14-15/15 cell 过门）。clipping–resolution
折中是真实问题。→ 进入 Phase B。

## Phase B/C：传统 comparator + 候选工厂

dev 前冻结（FROZEN_CONTRACT §5,§6）：3 传统 AGC（causal-RMS/peak-hold/log-domain）+ 4 候选
（dual-tc/clipping-aware/robust-pct/hysteretic），每 family 公平 3-config dev 预注册集，
dev-tune on weak/strong × SNR{5,13,21} × dev seeds{0,1,2}=18 cells，fresh held-out on
3 scenes × SNR{5,9,13,17,21} × seeds{30..34}=75 cells，paired delta = strongest-conv − cand
（正=cand 更好）。

**Phase B：传统 AGC 部分缓解但未解决**（`conv_resolves=False`）。最强传统 AGC = causal-RMS：

| W | 最强传统 AGC | pooled regret (dB) | CI95 |
|---|---|---|---|
| 6  | causal_rms | **+0.896** | [+0.823, +0.969] |
| 8  | causal_rms | **+0.794** | [+0.714, +0.873] |
| 10 | causal_rms | **+0.767** | [+0.686, +0.847] |

causal-RMS 把 fixed-gain 的 +0.91~+1.03 dB 降到 +0.77~+0.90 dB（缓解约 0.12~0.20 dB），
但**仍远高于 MDE=0.15**（5×~6×MDE），问题未被常规 comparator 解决 → 进入 Phase C。

**Phase C：候选无一稳定超过最强传统 AGC**（`cross_consistent=False`）。最佳候选 = dual_tc，
paired delta（conv − cand）：

| W | 最佳候选 | Δ mean (dB) | CI95 | 过 MDE? |
|---|---|---|---|---|
| 6  | dual_tc | **−0.016** | [−0.047, +0.016] | 否（CI 跨 0，|Δ|≪MDE）|
| 8  | dual_tc | **−0.004** | [−0.039, +0.031] | 否（CI 跨 0，|Δ|≪MDE）|
| 10 | dual_tc | **−0.017** | [−0.039, +0.004] | 否（CI 跨 0，|Δ|≪MDE）|

W=8 全候选 delta：dual_tc −0.004、clipping_aware −0.209、robust_pct −0.115、hysteretic −0.467
（**全部 ≤0**——候选无一胜过 causal-RMS，多数反而更差）。无可区分 deployable action。

## 终态 verdict

**`NO_DIAGNOSTIC_METHOD_SIGNAL`**（method-production 终态集六选一）。有效 P07（计 7/10），
不产 METHOD_SIGNAL，仍 0 active carrier，不登记 pre-formal carrier。

**机制诚实**：clipping–resolution 折中**真实存在**（Phase A fixed-gain +0.91~+1.03 dB，
clipping rate 随 gain 单调：g0.5→2.5%、g1.0→30%、g4.0→91%；低 gain 侧分辨率损失、
高 gain 侧峰值 clipping，固定增益无法同时最优）；标准 causal AGC **部分缓解**（+0.77~+0.90 dB）
但**未解决**；4 个机制不同的 robust/clipping-aware AGC **无一稳定超过 dev-tuned causal-RMS**。
不是"问题不存在"也不是"常规已解决"，是"问题真实存在、常规部分缓解、无方法增量"。

**harvest（有界负面 + ADC 工程证据）**：
- (a) Ch5 接收机实现证据：8-10 bit uniform signed I/Q ADC + causal-RMS AGC 是该冻结接收链在源闭合
  GG 下的合理模拟前端配置（fixed-gain 与 causal-RMS 的量化/clipping 边界曲线）；
- (b) Ch3/Ch4 鲁棒性边界：该折中不是 ML/robust-AGC 可优于标准 causal-RMS 的 deployable 子问题
  （4 候选无一过 MDE，多数更差）—— 与 P06 一致的 "receiver-visible 信号被常规 baseline 吸收" 趋势。

## 包内确定性修复（1 次，已披露，V071 复核）

Phase-BC JSON 序列化 bug：numpy `bool_`（`ci["mean"] >= MDE`）不被 json.dump 识别，首次
`save_results` 崩溃（计算已完成 725s，仅序列化失败）。修复 = 加 `_to_jsonable` 递归转 native
Python 类型后重跑（计算结果不变，verifier V10 独立重算 raw→aggregate relErr ≤1e-9 + verdict
唯一）。**计算/数据/verdict 全不变，仅序列化类型修复 + 重跑保落盘**。判据/dev-ref/方法身份/
MDE/§5-6 顺序全不变。

## P06 措辞边界（不修改/不重跑）

P06 `NO_CAUSAL_HISTORY_INCREMENT` 准确表述：history-expanded > current-only、
persistence > history-expanded → "没有超过强传统 temporal baseline 的方法增量"，
**非"历史完全无信息"**。

## 产物

- 冻结合同：`projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/src/p07/FROZEN_CONTRACT.md`
- 实现：`_p07_adapters.py`（AGC/ADC）、`_p07_runner.py`（float-bypass runner）、
  `_p07_batch.py`（批量评估）、`_p07_smoke.py`（Phase 0）、`_p07_phaseA.py`、
  `_p07_phaseBC.py`、`_p07_verify.py`（独立 verifier）
- artifacts：`projects/simulation/results/p07_agc_adc_dynamic_range/`
  （p07_phase0_smoke.json、p07_phaseA_dev.json、p07_phaseBC.json、p07_verifier_result.json、
  p07_terminal_verdict.json）
