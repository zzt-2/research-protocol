# Task Brief: T031 — P03 Fixed-Point / Resource-Performance Co-Design (Family B_FIXED_POINT)

> 来源: S003 / D040 campaign; A 族已关闭，P03 换族 = B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN
> 产出位置: 回传到 `projects/simulation/results/p03_fixed_point_codesign/` + worker-log
> 日期: 2026-07-30
> 唯一文档: 执行方只拿到这一个文档 + 冻结源码（不可改）
> Python（anchor-provenance 3.11.9）: `/c/Users/zzt/scoop/apps/python311/current/python`
>   **不要**用 torch venv（无 pydantic, Python 3.14，anchor 复现失败）

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，手上有已冻结的
DA/NDA CPR 选择器 anchor（`_a4_switch_common768_30seed.py::decide`）和 P01/P02 已验证的
per-window DA/NDA common-768 错误计数探针（`_p01_cpr_snr_mismatch_probe.py::run_case_multidelta`，
`_eval_selector(decide_fn, ...)` 接口）。

**你的任务**：判断已完成的 DA/NDA CPR 选择器在**定点部署**时，是否存在"统一位宽浪费资源或损害分支
选择"的**真实工程问题**；若存在，构造并验证 sensitivity-aware mixed-precision 方法。这是一个工程
诊断 + 条件式方法工厂包（PREFORMAL_METHOD_FACTORY），不是重开 NDA-ML。

**产出**：一个 terminal verdict + uniform/mixed Pareto 数字 + 是否 METHOD_SIGNAL，写入
worker-log `step-030-p03-fixed-point-codesign.md` + artifact JSON。

**最高纪律**：
1. **只动 selector 控制路径**（功率统计→噪声扣除→stage-1 CV 边界→stage-2 γ_eff 边界→分支选择）。
   分支输出（DA/NDA common-768 错误）**完全复用冻结的 per-window 错误**，不得重算 BER。
2. **bit-true 必须真实**：明确 Q-format（signed/unsigned、W/F、rounding、saturation、accumulator、
   coefficient quantization、float-bypass identity）。**禁止用 decimal rounding 冒充定点**。
   无法建立可信 bit-true 模型 → 终态 `BLOCKED_NO_BITTRUE_MODEL`。
3. **信息边界**：定点 `decide` 只能消费 `rx_seg`（raw 接收样本）、`gamma_db`（nominal SNR）、
   `gamma_lin`。**绝不**用 TX truth、true SNR、true h/phi 或离线标签作运行时输入。
4. **不修改冻结文件**：common/、params.py、`_a4_switch_common768_30seed.py`、`_p01_*.py`、
   `_a4_branchrouted_30seed.py`、`sc_nda_ml_sim.py`、anchor JSON 全部只读。新文件只放
   `projects/simulation/explore/nda-awgn-tracking-sandbox/_p03_*.py`。
5. **seed 隔离**：dev = 0–9（anchor 子集，range-finding + bitwidth freeze）；fresh held-out test
   = 30–49（P01 已用，但 P03 用**不同的判据**，可复用同一组 held-out seed，因为 P03 的估计量是
   位宽配置不是对 gain 的拟合——见 §3.4）。pollution seeds 71–80 禁用。
6. terminal verdict 必须是下列之一（method-production 终态集）：
   `ENGINEERING_DIAGNOTIC_METHOD_SIGNAL` / `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION` /
   `NO_DIAGNOSTIC_SIGNAL` / `BLOCKED_NO_BITTRUE_MODEL` / `BLOCKED_NO_DEFENSIBLE_RESOURCE_METRIC` /
   `EXECUTION_INVALID`。

## 1. 背景（理解任务必需的，标"了解即可不对照评价"）

### 1.1 冻结的 selector 控制路径（`_a4_switch_common768_30seed.py:93-107`）

```python
def cv_awgn_theory(snr_db):              # :93-94
    return 0.74 + 0.12 * np.exp(-snr_db / 5.0)

def decide(rx_seg, gamma_db, gamma_lin): # :97-107  (raw 信号统计 CV + 盲 h)
    pwr = np.abs(rx_seg) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < cv_awgn_theory(gamma_db) * CV_MARGIN:   # CV_MARGIN=1.10, stage-1
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * gamma_lin)), 1e-6)   # 噪声扣除, stage-2 输入
    return 'da' if gamma_db + 10 * np.log10(h) < GAMMA_EFF_TH else 'nda'  # GAMMA_EFF_TH=13.0
```

- stage-1：`cv`（变异系数，**尺度不变**）vs `cv_awgn_theory(γ)*1.10`。`cv_thr` 随 γ 在
  [0.815(@25dB), 0.863(@5dB)]，窄。
- stage-2：`h = mean(pwr) − 1/(2γ_lin)`（噪声扣除，**尺度依赖**），`γ_eff = γ_db + 10log10(h)` vs 13。
  `1/(2γ_lin)` 在高 SNR 极小（25dB→0.00158），低 SNR 较大（5dB→0.158）。
- **关键张力**（已分析）：stage-1 只需 fraction bits（cv 在阈值附近敏感）；stage-2 高 SNR 时
  噪声扣除 `1/(2γ_lin)` 下溢 → h_hat 量化误差 → 错误 γ_eff → 错分支。统一位宽要么在 cv 处
  浪费 integer bits，要么在 stage-2 高 SNR 处 fraction bits 不足。

### 1.2 已验证的探针接口（`_p01_cpr_snr_mismatch_probe.py`）

```python
def run_case_multidelta(scene, gamma_true_db, seed_index, deltas=DELTAS,
                        n_windows=400, extra_selector=None):
    # 返回 base（per-window DA/NDA common-768 错误 + per-window raw rx + tx）
    # 和 per_delta[delta] = {n_select_da, n_select_nda, selected_errors, choices}
    # extra_selector = {name: {"fn": decide_fn, "needs_pilot": bool, "needs_reset": bool}}
    #   decide_fn(raw, gamma_db, gamma_lin, b) -> 'da'/'nda'
```

`_eval_selector(decide_fn, name, ...)`（:234-261）已经：对每个 window 调 `decide_fn(pw_raw[b],
g_hat_db, g_hat_lin, b)`，按选择累加 `pw_da_err[b]`/`pw_nda_err[b]`（**冻结的 common-768 错误**）。
你只需写一个**定点 `decide_fp`**，签名 `(raw, gamma_db, gamma_lin, b) -> 'da'/'nda'`，通过
`extra_selector` 注入即可——**不需要重算 BER，不需要碰信道生成**。

### 1.3 anchor 增益（common-768 口径，30 seed，`ccisp_family1_selector_a_30seed.json`）

weak@9 +1.50dB、moderate@9 +1.05dB、strong@9 +0.83dB（增益集中在中低 SNR 5–13 dB，DA 占用
30–95%）。wrong-branch regret = 当定点 decide 选错分支时，相对于 per-block oracle
`min(nda_err, da_err)` 多付的错误数（×768 bit → dB）。

## 2. 任务详情

### 2.1 要回答的问题

(a) **float-bypass identity**：在足够宽（W≥14）下，定点 `decide_fp` 是否与浮点 `A.decide`
在所有 dev seed/cell 上**逐 window 决策一致**？若否 → bit-true 模型不可信 →
`BLOCKED_NO_BITTRUE_MODEL`，停。

(b) **uniform precision 的 Pareto**：扫位宽阶梯（见 §3.3），记录每个位宽的
`decision agreement vs float`、`wrong-branch regret (dB)`、`overflow rate`、`operation × operand-bit / storage-bit proxy`。
uniform baseline 是否已给出足够好的 Pareto frontier？若是（regret 在所有合理位宽下都 ≤ MDE
且无资源-性能矛盾）→ `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`。

(c) **mixed-precision 是否稳定超越 uniform**（仅在 uniform 存在明显矛盾时）：3–5 个机制不同的
mixed-precision 候选，每个有**不同的 deployable bit-allocation/scaling action**（不是统一位宽换数字）。

### 2.2 bit-true 定点合同（必须实现，逐项冻结）

实现一个独立的 `_p03_fixed_point.py`，含：

- **quantize(value, W, F, signed, mode='half_up')**：饱和二补码定点。round-half-up（ties→+inf，
  `raw = floor(value*2^F + 0.5)`），饱和到 `[−2^(W-1), 2^(W-1)−1]`（signed）或 `[0, 2^W−1]`（unsigned）。
- **float-bypass identity**：W=64, F=40 时 `quantize` 与输入的误差 ≤ 2^(−40)。
- **block-floating-point 归一化**（per-window，决策等价，标准 DSP）：
  - `pmax = max(|rx_k|^2)` over window；`exponent e = floor(log2(pmax))`（共享）；
  - 归一化 mantissa `pwr_k' = pwr_k / 2^e ∈ [0.5, 1]`（近似）；
  - `cv` 从归一化 mantissa 算（尺度不变，float-bypass 下精确）；
  - `mean_pwr`（绝对，stage-2 需要）= `mean(pwr_k') * 2^e`，再量化到 (W,F)。
- **非线性算子**（sqrt for std、log10 for γ_eff、div for cv）：在浮点精度计算，但**输入和输出**
  都量化到声明的 (W,F)（模拟 LUT 实现，输入/输出位宽与数据通路匹配）。
- **accumulator 位宽**：`W + ceil(log2(N=256)) + 2 guard = W + 10`（标准，不是额外资源）。
- **LUT 系数**：`cv_thr = cv_awgn_theory(γ)*1.10`、`noise_sub = 1/(2γ_lin)`、`log10` 表，预计算并量化到 (W,F)。
- **decide_fp(raw, gamma_db, gamma_lin, W, F)**：镜像 `A.decide` 的两阶段逻辑，但每个数据依赖算子量化。
  返回 `'da'`/`'nda'`。

**必须测试**（写 `_p03_smoke_check.py`）：
- float-bypass（W=64,F=40）与原 selector 在 dev 0–9 全 cell 逐 window 决策一致；
- 极值/零值/饱和/舍入边界（构造 pwr=[0, max, 临界阈值±1LSB] 的合成 window）；
- 确定性/seed 可复现（同输入两次调用字节级一致）；
- 不使用 TX truth / true SNR / 离线标签（AST/grep 审计 `decide_fp` 可执行代码无 true/tx 引用）。

### 2.3 Phase A：uniform-precision baseline（`_p03_phaseA.py`）

- 位宽阶梯（dev 前 freeze）：`(W, F) = {(6,4),(8,6),(10,8),(12,10),(14,12),(16,14)}`，即
  `F = W − 2`（2 integer bits 覆盖归一化后 [0,4) mantissa）。浮点只作 reference，**不作 Go comparator**。
- 每个 (scene, γ, seed, bitwidth) cell：调 `run_case_multidelta(..., extra_selector={"fp_Wf":
  {"fn": lambda r,g,gl,b: decide_fp(r,g,gl,W,F)}})`，δ=0（定点不依赖 SNR 失配；P03 是位宽问题不是 SNR 问题）。
- 在独立 dev（seeds 0–9）建立表：`bitwidth | decision_agreement_vs_float | wrong_branch_regret_dB |
  gain/Q_penalty | overflow_rate | op×bit_proxy | storage_bit_proxy`。
  - `wrong_branch_regret` = 当 `decide_fp` 选的分支 ≠ float 选的分支时，多付的错误数（相对 per-block
    oracle），跨 window 聚合为 dB（`10log10(fp_selected_errors / float_selected_errors)`，paired-seed）。
  - `overflow_rate` = 量化饱和的 window 比例。
  - resource proxy（**必须明确标 proxy**，禁止声称真实 LUT/DSP/功耗）：
    `op_bit_proxy = Σ_per_op (operand_bitwidth)`（每个算子的操作数位宽之和，按 selector 每窗算一次）；
    `storage_proxy = Σ_register (bitwidth)`（pwr/sum/sum2/mean/var/std/cv/h/log10 等寄存器位宽之和）。

### 2.4 Phase B：3–5 个 mixed-precision 候选（仅当 uniform 存在明显矛盾）

候选机制（每个**不同 deployable action**）：
1. **statistic-sensitivity bit allocation**：cv 用窄位（尺度不变，少 fraction 即可），stage-2 mean/noise-sub 用宽位。
2. **range-aware per-stage scaling**：stage-1 和 stage-2 用不同 exponent 归一化。
3. **confidence-margin-preserving boundary quantization**：在阈值附近（|cv − cv_thr| < margin 或
   |γ_eff − 13| < margin）用更宽位，远离阈值用窄位。
4. **saturation-aware accumulator allocation**：accumulator 按实测动态范围收窄 guard bits。
5. **shared/coefficient-LUT mixed precision**：LUT 系数用固定宽位（与 γ 量化精度匹配），数据通路可异。

### 2.5 公平比较（`_p03_phaseBC.py`）

- uniform comparator 与各候选获得**相同 dev 调优机会**（uniform 的 (W,F) 也允许 dev 选最优阶梯点）。
- dev freeze 后跑 fresh held-out（seeds 30–49，复用 P01 held-out——因 P03 估计量是位宽配置不是
  gain 拟合，无泄漏；见 §3.4 论证）。
- paired cells/seeds；原始浮点 realization 与 branch outputs 跨方法共享（run_case_multidelta 已保证）。
- 报 decision agreement、wrong-branch regret、主性能损失、overflow、resource proxy。
- 画完整 Pareto frontier（resource proxy vs regret），不只挑单点。
- 消融：区分收益来自 mixed precision、scaling、还是更多总 bit budget（控制总 bit 相同时 mixed vs uniform）。

### 2.6 产出格式（强制，给模板）

worker-log `step-030-p03-fixed-point-codesign.md`：
```
# step-030 — P03 Fixed-Point/Resource Co-Design (Independent Executor)
> Task: T031 ... > Date ... > TERMINAL VERDICT: <六选一>
## 0. Mission recap
## 1. CRITERION FREEZE (写在跑任何 test 数据前)
  - float-bypass identity 通过判据
  - uniform 矛盾判据（什么算"明显资源-性能矛盾"）
  - mixed MDE（frozen，建议 0.15 dB 与 P01/P02 一致；或用 Pareto dominance）
  - seed 隔离（dev 0–9 / held-out 30–49 / pollution 71–80 禁）
## 2. bit-true 模型（Q-format 合同 + smoke 结果）
## 3. Phase A uniform baseline（Pareto 表）
## 4. Phase B mixed candidates（若运行）
## 5. 公平比较 + 消融
## 6. Terminal verdict + 理由
## 7. Key numbers（for controller relay）
## 8. Discipline items（信息边界 / seed 隔离 / 冻结文件 git diff 空 / 复现）
## Artifacts: results/p03_fixed_point_codesign/{...json}  Source: explore/.../_p03_*.py  Elapsed ...
```

artifact JSON 用 `save_results()`（CP-4 元数据），raw rows + aggregate 都存，verifier 要独立复算。

## 3. 已知陷阱（基于历史失败的具体案例）

1. **禁止用 decimal rounding 冒充定点**（brief 二）：`np.round(x, decimals=2)` 不是定点。
   必须是显式 Q(W,F) 饱和二补码。
2. **accumulator 溢出 ≠ "额外资源"**：accumulator 必须按 log2(N) 加宽，这是标准不是浪费。
   不要把 accumulator 位宽算进 "浪费"。
3. **block-float exponent 必须共享 per-window**：不能 per-sample exponent（那会破坏 cv 的尺度不变性）。
4. **非线性算子的量化层**：sqrt/log10/div 在浮点算但 I/O 量化——这是 LUT 模型，**不是**把整个
   算子当浮点（那样就没有位宽效应了）。verifier 会查。
5. **resource proxy 必须标 proxy**：禁止写 "LUT 减少 X%"、"DSP 节省"、"功耗降低"。只写
   `op×bit_proxy` 和 `storage_bit_proxy`，明确标注 "no real synthesis"。
6. **true γ 绝不进 decide_fp**：AST 审计 `decide_fp` 可执行代码无 true/tx/oracle/h/phi 引用。
   true γ 只在信道生成 + 离线 BER（已由冻结探针处理）。
7. **float-bypass 必须先过**：W=14/16 下逐 window 决策与 `A.decide` 不一致 → 模型错，停，不要硬跑 Phase A。
8. **复现 anchor**：先跑 `_p03_smoke_check.py` 确认 δ=0、W=64 时 `decide_fp` 与 `A.decide` 在 dev
   0–9 全 cell（weak/moderate/strong × 5–25 dB）逐 window 决策 100% 一致，再继续。
9. **判据冻结在先**：§1 的所有判据（float-bypass 通过 / uniform 矛盾定义 / mixed MDE / seed 隔离）
   必须写在跑任何 test 数据**之前**的 worker-log §1，trap #7（P01 教训）。

### 3.4 关于复用 P01 held-out seeds 30–49 的泄漏论证

P03 的"估计量"是**位宽配置 (W,F) / mixed-precision 分配**，不是对 gain 的拟合。dev（0–9）用于
range-finding（测 pwr 动态范围定 integer bits）和 uniform 最优阶梯点选择。位宽配置不拟合 per-cell
gain 数值，因此 held-out 30–49 的 gain 分布对位宽选择无信息泄漏。这与 P02 的"dev 调 ref 拟合
cand_rank"不同（P02 是参数拟合，P03 是配置选择）。**若你认为有泄漏风险，dev 只用 0–9 选 integer
bits（数据驱动范围），uniform 最优点和 mixed 分配的 dev-tuning 改用 seeds 10–19**（与 held-out
30–49 disjoint）。自行判断并在 §1 冻结说明。

## 4. 验收（主线拿到产出后怎么检查）

- [ ] float-bypass identity 在 W≥14 下逐 window 决策与 `A.decide` 100% 一致（dev 0–9 全 cell）
- [ ] Q-format 合同逐项实现（rounding/saturation/accumulator/LUT/block-float 全有）
- [ ] 冻结文件 `git diff --stat HEAD` 全空（common/、params.py、_a4_switch/_p01/_a4_branchrouted/
      sc_nda_ml_sim.py、anchor JSON）
- [ ] true γ 绝不进 decide_fp（AST 审计）
- [ ] terminal verdict 是六选一之一，且与数字一致
- [ ] raw rows + aggregate 都存，可独立复算
- [ ] resource proxy 明确标 proxy（无 LUT/DSP/功耗声称）
- [ ] worker-log §1 判据冻结在跑数据前
- [ ] seed 隔离（dev ≠ held-out，pollution 71–80 禁用）

## 附：产出回传位置

- worker-log: `projects/thesis-fso/worker-logs/step-030-p03-fixed-point-codesign.md`
- artifact: `projects/simulation/results/p03_fixed_point_codesign/*.json`
- source: `projects/simulation/explore/nda-awgn-tracking-sandbox/_p03_*.py`
- 完成后在 worker-log §7 给 controller relay 的关键数字 + verdict。
