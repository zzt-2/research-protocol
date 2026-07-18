# Investigation: VV Extreme Variance at Moderate Turbulence

> 2026-06-01 | Scientist Agent | 状态: 完成

## Objective

10-seed sweep results show VV at moderate turbulence (20 dB SNR) has BER mean 8.05% with 95% CI [3.04%, 13.06%]. This CI spans 4x, vastly wider than all other methods at the same conditions (e.g., DPLL 0.19% [0.17%, 0.22%]). Investigate whether this is a fundamental property of VV or an implementation artifact.

---

## 1. Per-Seed BER Data (20 dB, Moderate Turbulence, alpha=2.5, beta=1.8)

| Seed | BER (%) | Status | First failure symbol | h at failure | % symbols affected |
|------|---------|--------|---------------------|--------------|-------------------|
| 1000 | 0.162 | GOOD | — | — | — |
| 1001 | 3.885 | CATASTROPHIC | 1555 | 0.0142 | 98.4% |
| 1002 | 14.097 | CATASTROPHIC | 24538 | 0.0147 | 75.5% |
| 1003 | 19.548 | CATASTROPHIC | 13720 | 0.0187 | 86.3% |
| 1004 | 10.640 | CATASTROPHIC | 21027 | 0.0137 | 79.0% |
| 1005 | 19.438 | CATASTROPHIC | 3534 | 0.0168 | 96.5% |
| 1006 | 0.150 | GOOD | — | — | — |
| 1007 | 12.226 | CATASTROPHIC | 9532 | 0.0032 | 90.5% |
| 1008 | 0.194 | GOOD | — | — | — |
| 1009 | 0.196 | GOOD | — | — | — |

**Summary**: 4/10 seeds GOOD (BER < 1%), 6/10 seeds CATASTROPHIC (BER 3.9%–19.5%). Fail rate = 60%.

### Statistical Characterization

| Group | Count | Mean BER | Std BER | Log10(BER) mean | Log10(BER) std |
|-------|-------|----------|---------|-----------------|----------------|
| GOOD | 4 | 0.175% | 0.020% | -2.76 | 0.05 |
| BAD | 6 | 13.31% | 5.39% | -0.93 | 0.24 |

- Shapiro-Wilk normality test: W=0.838, p=0.042 → reject normality (bimodal)
- Log10(BER) group separation: 7.7 sigma
- Coefficient of variation: 0.95 (extreme overdispersion)
- Bootstrap 95% CI: [3.48%, 12.89%]

---

## 2. Root Cause Analysis

### 2.1 The Failure Mechanism

VV standalone in the sweep uses **FOE → VV(Nw=64)** — no DPLL pre-tracking, and a short window of 64 symbols. The failure mechanism has four stages:

**Stage 1: Deep fade block encounter**

At moderate turbulence (alpha=2.5, beta=1.8), 4.7% of blocks have h < 0.08. With 1000 blocks per seed, every seed encounters ~47 such blocks. The critical blocks are those with h < 0.02, where SNR₄ = gamma_bar * h / 8 drops below 0.25.

**Stage 2: Unwrap threshold crossing**

When the convolution window enters a deep fade block, the 4th-power signal becomes noise-dominated. The `np.unwrap(np.angle(avg))` function compares consecutive angle samples. In the noise-dominated region, the angle can jump by more than pi between adjacent samples, causing unwrap to add a spurious 2*pi correction.

With Nw=64 (vs the optimal 256), the averaging is 4x less effective:
- Nw=64 at h=0.01: SNR₄_avg = 100 * 0.01 / 8 * 64 = 8.0, sigma_angle = 1/sqrt(16) = 0.25 rad = 14.3 deg
- Nw=256 at h=0.01: SNR₄_avg = 100 * 0.01 / 8 * 256 = 32.0, sigma_angle = 1/sqrt(64) = 0.125 rad = 7.1 deg

The shorter window provides significantly less noise protection at the deep fade boundary.

**Stage 3: Irreversible wrong lock**

Once unwrap locks into the wrong branch, the phase estimate acquires a permanent offset. The phase error shifts from the stable ~-45 deg (pi/4 offset) to an arbitrary value (observed: +133 deg, +116 deg, -112 deg, etc.). The standard deviation of the error in BAD seeds is 23–51 deg, vs 1.3–1.7 deg in GOOD seeds.

**Stage 4: Global rotation cannot fix it**

`resolve_qpsk` applies a single global rotation from {0, pi/4, pi/2, ..., 7*pi/4}. When the phase error changes mid-sequence (one value before the slip, another after), no single rotation can fix both segments. The unfixed segment contributes high BER proportional to its length.

### 2.2 Why Same h Values Give Different Outcomes

A critical observation: seeds 1000 and 1008 (GOOD) have min_h values of 0.0062 and 0.0022 respectively — *lower* than several BAD seeds. Yet they survive. This proves the failure is **stochastic, not deterministic**:

1. **Phase value at entry matters**: The residual phase (after FOE compensation) at the exact moment of the deep fade determines whether the 4th-power angle crosses the wrap boundary. This is random across seeds.

2. **Convolution context matters**: The surrounding blocks' h values determine how much "rescue signal" the convolution window receives. But even with strong neighbors, failure can occur if the noise realization at the boundary is unfavorable.

3. **FOE error matters**: Different seeds produce different FOE estimation errors (observed: -149 kHz to +105 kHz). Larger FOE errors create more phase drift within the VV window, reducing the margin before the wrap boundary.

### 2.3 Why Fixed Baseline Does Not Fail

The Fixed baseline (FOE → DPLL → VV with M_vv=256) has 0% failure at moderate turbulence because:

1. **DPLL pre-tracking**: DPLL removes the residual frequency offset and tracks the Doppler phase change. The signal entering VV has near-zero phase drift, so the 4th-power phase is nearly constant within the window.

2. **Larger window (M_vv=256)**: 4x more averaging dramatically reduces noise at deep fade boundaries. At h=0.01, sigma_angle drops from 14.3 deg (Nw=64) to 7.1 deg (Nw=256).

3. **Combined effect**: DPLL provides the phase stability, and the larger window provides the noise robustness. Together they eliminate the stochastic failure mode.

### 2.4 Fail Rate vs SNR (Transition Zone)

| SNR (dB) | BER Mean (%) | Fail Rate (%) |
|-----------|-------------|---------------|
| 0–14 | 26–49 | 100% |
| 16 | 16.1 | 90% |
| 18 | 10.3 | 70% |
| 20 | 8.1 | 60% |
| 22 | 6.0 | 40% |
| 24 | 3.7 | 10% |
| 26+ | <0.02 | 0% |

20 dB is squarely in the transition zone where the system is at the edge of the stochastic threshold. Below 16 dB, all seeds fail; above 26 dB, none fail.

---

## 3. Is This an Implementation Artifact?

**Partially yes, partially no.**

### Artifact component

The sweep's `method_vv()` uses suboptimal parameters (Nw=64, no DPLL). With the Fixed baseline's optimal parameters (DPLL + Nw=256), VV works perfectly at moderate turbulence (0% failure). The 60% fail rate is inflated by the suboptimal standalone configuration.

### Fundamental component

Even with optimal parameters, VV's **open-loop unwrap is fundamentally fragile** at strong turbulence (100% fail rate at alpha=1.5, beta=0.8). The mechanism is the same — stochastic threshold crossing at deep fades — but at strong turbulence the fades are so deep and frequent that no window size can provide enough margin.

The **bimodal distribution** (seeds either work perfectly or fail catastrophically) is a fundamental property of open-loop phase unwrapping in fading channels. It cannot be eliminated by parameter tuning; it can only be shifted to higher turbulence levels by using DPLL pre-tracking and larger windows.

---

## 4. Comparison: All Methods at 20 dB, Moderate Turbulence

| Method | BER Mean (%) | 95% CI (%) | Fail Rate | Pipeline |
|--------|-------------|------------|-----------|----------|
| **VV** | **8.05** | **[3.04, 13.06]** | **60%** | FOE → VV(Nw=64) |
| DPLL | 0.19 | [0.17, 0.22] | 0% | FOE → DPLL(omega_n=8M) |
| KF_pilot | 0.21 | [0.19, 0.24] | 0% | FOE → KF(pilot-assisted) |
| Fixed | 0.18 | [0.16, 0.20] | 0% | FOE → DPLL → VV(M=256) |

The VV CI is 40x wider than DPLL's CI, driven entirely by the bimodal good/fail distribution.

---

## 5. Recommendation for Thesis

### 5.1 How to Describe the Phenomenon

> Viterbi-Viterbi (VV) 四次方鉴相器在中等湍流下呈现显著的种子间方差。10 种子实验中，60% 的种子遭遇灾难性相位解卷绕失败（BER > 3%），而其余种子表现良好（BER < 0.2%）。这种二态分布导致 VV 的 95% 置信区间 [3.0%, 13.1%] 比闭环 DPLL [0.17%, 0.22%] 宽约 40 倍。
>
> 失败机制是 VV 开环解卷绕在深衰落块（h < 0.02）处的随机阈值穿越：当滑动窗内的四次方信号信噪比降至 1 以下时，`np.unwrap` 产生不可逆的 2π 修正，永久锁定到错误的相位分支。该失败是否发生取决于衰落块处的精确相位值和噪声实现——具有相似信道统计特性的种子可能表现截然不同。
>
> 值得注意的是，VV 作为 Fixed 基线（FOE+DPLL+VV, M_vv=256）的一部分时，在中等湍流下零失败。DPLL 预跟踪消除了相位漂移，更大的窗口提供了更强的噪声鲁棒性。这说明 VV 本身不是有缺陷的，但当单独使用且窗口不足时，其开环结构在衰落信道下存在结构脆弱性。

### 5.2 What NOT to Claim

1. Do NOT claim "VV is unreliable at moderate turbulence" without qualifying that this is for standalone VV with Nw=64
2. Do NOT claim the variance is "unexpected" — it is the natural consequence of stochastic threshold behavior
3. Do NOT claim the sweep's VV configuration is representative of VV's best performance — the Fixed baseline shows VV with proper support works well

### 5.3 Suggested Figure

Use `investigation-vv-variance-figures.png` which contains:
- (A) Per-seed BER bar chart showing the bimodal distribution
- (B) Fail rate vs SNR showing the 16–24 dB transition zone
- (C) Log-scale BER comparison of all methods at 20 dB
- (D1–D4) Phase error trajectories for 2 GOOD and 2 BAD seeds
- (E) Moderate turbulence h distribution with failure thresholds marked
- (F) BER vs % affected symbols for BAD seeds

---

## 6. Key Evidence Files

| File | Content |
|------|---------|
| `investigation-vv-variance-figures.png` | 6-panel analysis figure |
| `results/sweep_20260601_181320.json` | Raw 10-seed sweep data |
| `common.py` L161-171 | VV implementation (`vv_cpr`) |
| `experiments/multi_seed_sweep.py` L64-72 | Sweep VV method (Nw=64, no DPLL) |
| `V-14-vv-performance-expectations.md` | Phase 1 VV theory (consistent with findings) |

---

## 7. Limitations

1. Only 10 seeds — the exact fail rate (60%) has wide uncertainty. With 100 seeds, expect the rate to converge to 40–70% at 20 dB.
2. Only analyzed VV standalone at Nw=64. The Nw=256 standalone case was not tested but is expected to have lower fail rate.
3. The stochastic threshold model is qualitative — we did not derive the analytical failure probability as a function of h, Nw, and phase angle.
4. Phase 1 research (V-14) predicted ~5% fail rate at moderate turbulence for the Fixed baseline configuration — consistent with this investigation showing 0% fail rate for Fixed and high fail rate only for the suboptimal standalone VV.
