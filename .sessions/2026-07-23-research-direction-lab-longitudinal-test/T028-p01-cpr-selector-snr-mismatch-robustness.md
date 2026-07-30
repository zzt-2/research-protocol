# Task Brief: P01 — CPR 选择器 SNR 失配鲁棒性

> 来源: S003 / D039（campaign 授权 + P01 端到端执行）| 产出位置: 回传 worker-log + artifact，主控接收
> 日期: 2026-07-30
> 唯一文档: 执行方只拿到这一个文档 + 指定源码路径（只读引用，不改 common/params/原 selector）

## 0. TL;DR（执行方先读）

你在 Windows + Git Bash 环境，worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，
Python = `/c/Users/zzt/.venvs/torch/Scripts/python.exe`（注意 win32 是 Scripts 不是 bin）。

**你的任务**：对已完成的 DA-NDA 两层 CPR 选择器，做 **SNR 失配鲁棒性** 的端到端诊断 package。先复现冻结 anchor（基线，不计创新），再注入 SNR 估计失配，判断失配是否实质损害原 0.8–1.5 dB 增益；若损害，跑传统 adapter，若 adapter 后仍残余再构造 robust 候选。

**产出**：一个 terminal verdict（五选一，见 §2.4）+ raw rows + paired CI + branch occupancy，回传到
`projects/thesis-fso/worker-logs/step-NNN-p01-cpr-snr-mismatch.md` 和 `projects/simulation/results/p01_cpr_snr_mismatch/`。

**最高纪律**：
1. **复现旧 selector 结果不是新方法**（FR-23）——必须注入**新的 SNR 失配**这一新失效条件。
2. **true SNR 绝不作部署输入**（TL-32/FR-25）——true SNR 只用于生成信号和离线评价；所有 receiver 用的是 nominal/估计 SNR。
3. **dev 前冻结"实质失效"判据**，看完 test 后不补门槛（见 §2.1 冻结判据）。
4. **不改 common/、params.py、原 selector** `_a4_switch_common768_30seed.py`——只新增 probe/adapter/candidate 文件。
5. 信道共享：必须用 `generate_shared_realization_apsk`，禁独立生成（TL-13）。
6. fresh held-out seeds，禁用 dev seeds；paired realization；raw rows 留全。

## 1. 背景（理解任务必需的，标"了解即可不对照评价"）

### 1.1 原 selector（已完成方法，method.tex 已成稿）

两层 DA/NDA 切换，定义在 `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.py:97-107`：

```python
def cv_awgn_theory(snr_db):           # :93-94
    return 0.74 + 0.12 * np.exp(-snr_db / 5.0)
GAMMA_EFF_TH = 13.0                    # :78
CV_MARGIN = 1.10                       # :79

def decide(rx_seg, gamma_db, gamma_lin):   # :97-107
    pwr = np.abs(rx_seg) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < cv_awgn_theory(gamma_db) * CV_MARGIN:      # stage-1 CV 边界，用 nominal gamma_db
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * gamma_lin)), 1e-6)   # stage-2 噪声扣除，用 nominal gamma_lin
    return 'da' if gamma_db + 10 * np.log10(h) < GAMMA_EFF_TH else 'nda'
```

**两处依赖运行时 nominal SNR**：①stage-1 CV 边界 `cv_awgn_theory(gamma_db)`；②stage-2 噪声扣除 `1/(2*gamma_lin)` + γ_eff vs 13 dB。

### 1.2 冻结 anchor（基线，复现它）

`projects/simulation/results/ccisp_family1_selector_a_30seed.json`：30 seed × scenes{weak,moderate,strong} ×
SNR{5,7,...,25} dB，每 seed 400 window × 256 symbol，common-768 口径（192 非 pilot symbol × 4 bit = 768 bit/window）。
生成器：`projects/simulation/simulator/run_ccisp_family1_selector_a_30seed.py`（`run_case` 用
`generate_shared_realization_apsk` + `A.decide(raw, snr, gl)` + `per_block` + branch routing）。
seed 公式：`ws = P.SEED_TURB0 + seed_index * N_WINDOWS + b`（N_WINDOWS=400）。

**anchor 头部增益（主控预核，G_C = 10·log10(BER_NDA / BER_selected)，common-768 口径）**：
- weak@9dB +1.50 / weak@7dB +1.35 / weak@11dB +1.22 / weak@5dB +0.89 / weak@13dB +0.47
- moderate@9dB +1.05 / moderate@7dB +0.87 / moderate@11dB +0.97 / moderate@5dB +0.58
- strong@9dB +0.83 / strong@7dB +0.70 / strong@11dB +0.79 / strong@5dB +0.48
- 高 SNR（≥17dB）增益≈0（分支占用锁死 NDA）

**增益集中在 weak/moderate/strong 中低 SNR（5–13 dB），此处 DA 占用 30–95%**——失配若有害，最可能在这些 cell。
tuple/list 形式头部增益供 dev 判据锚点用（不是 test 后补的）。

## 2. 任务详情

### 2.1 Phase A：problem-bearing probe（先证明问题存在）

**先复现 anchor 的一个 dev 子集**（不全跑 990 cell）：用 dev seeds = seed_index 0–9（10 seed）×
**全部 11 SNR × 3 scene = 330 dev cell**，复现 `decide(raw, snr, gl)` 的 selected_errors / branch occupancy，
核对与 anchor 同 cell 同 seed 的 `selected_errors`、`n_select_da/nda` **逐 seed 完全一致**（anchor raw 已存，
可直接比对；不一致 = 复现失败，排查后才能继续）。这步证明你正确复现了原 selector。

**dev 前冻结"实质失效"判据**（写在 worker-log §判据冻结，test 前定稿）：

原方法声称规模是 0.8–1.5 dB 增益（9 dB 峰值）。定义**实质损害**：在某失配 δ 下，原 anchor 中增益 ≥0.5 dB
的 cell（weak/moderate/strong @ 5–13 dB）的 **mean paired-seed gain 被削掉 ≥0.3 dB**（相对 δ=0 基线），
且 CI 不跨 0。即：增益从 ~1 dB 掉到 <0.7 dB 且统计显著 = 实质损害。
- 选 0.3 dB 阈值理由：约为原增益规模（0.8–1.5 dB）的 ~25–37%，是"明显但非噪声级"的损害。
- 若你判断该阈值不合理，**在 dev 前书面说明并改**，但一旦 dev 跑完不得再改。
- **只看 δ=0..±3 dB 范围**（见下），超出范围的极端失配不在本 package 判据内。

**注入 SNR 失配**：receiver 持有一个**有偏的 nominal SNR** `γ̂_dB = γ_true_dB + δ`，δ ∈ {−3,−2,−1,0,+1,+2,+3} dB。
- 信号用 **true γ** 生成（`generate_shared_realization_apsk(N_DFT, gl=10**(γ_true/10), scene, ...)`）。
- selector 的 `decide(raw, γ̂_dB, 10**(γ̂_dB/10))` 用**有偏 γ̂**。
- 评价用 true γ 的 branch 输出（DA/NDA 各自在 true γ 下的 BER）；分支选择由有偏 γ̂ 决定。
- **true γ 绝不进 decide**（TL-32/FR-25）——它只生成信号 + 离线算 BER。
- 覆盖 anchor 的主要 cell：dev 上先看 weak/moderate/strong @ {5,7,9,11,13} dB（15 cell，失配最可能显现处）。

**Phase A 产出**：对每个 (scene, γ_true, δ)，记录：选择错误率（与 δ=0 选不同分支的 window 比例）、
branch occupancy（DA%/NDA%）、common-768 BER_selected、相对 δ=0 的 gain retention = gain(δ) − gain(δ=0)，
paired CI（per seed gain_db 的 Student-t 95%）。

**Phase A 判据（dev 前冻结）**：
- 若**所有 δ∈{±1,±2,±3} 在所有主 cell 的 |gain retention| 都 <0.3 dB 或 CI 跨 0** →
  **terminal verdict = `PROBLEM_ABSENT_UNDER_TESTED_MISMATCH`**，结束 P01。**这本身是一个有效科学负面结果（计 1/10）**，不制造 robust 方法。
- 若**存在至少一个 (scene, γ_true, δ) 的 gain retention ≤ −0.3 dB 且 CI 上界 <0**（实质损害）→ 问题成立，进 Phase B。

### 2.2 Phase B：传统 adapter（仅当 Phase A 问题成立）

实现一个 **receiver-visible 的常规 SNR/噪声估计 plug-in**，替换 selector 的 nominal γ̂：
- 候选估计器（选一个最常规的，DA pilot 已知可作 calibration prefix）：基于 pilot 符号的噪声方差估计
  `σ̂² = mean(|r_pilot − p·ĥ_pilot|²)`，`γ̂_est = signal_power / σ̂²`；或基于 decision-directed 残差。
  **只用 receiver-visible 量**（pilot、raw 功率），不用 true γ。
- comparator = (γ̂_est plug-in) + 原选择规则（`decide` 用 γ̂_est 而非有偏 nominal）。
- 独立 dev 调谐估计器（如窗长、pilot 子集），不能用 true γ。
- 在 Phase A 证明损害的同 cell + fresh held-out seeds 跑：gain(adapter) vs gain(nominal-有偏) vs gain(true-SNR oracle bound)。

**Phase B 判据**：
- 若 adapter 在所有损害 cell 恢复到 **gain retention ≥ −0.3 dB vs δ=0（即损害被消除）** →
  **terminal verdict = `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`**（adapter 已解决），不产生 METHOD_SIGNAL，结束 P01。
- 若 adapter 后仍有 cell 的 gain retention ≤ −0.3 dB 且 CI 上界 <0（残余损害）→ 进 Phase C。

### 2.3 Phase C：条件式 robust 候选（仅当 Phase B 后仍残余）

构造 **3–5 个机制不同的最小 robust 候选**（逐项 dedup，不能只调旧门限），每个只用 receiver-visible 输入：
1. **uncertainty-band robust threshold**：CV 边界用 γ̂ 的置信带上下界做最坏情况，而非点估。
2. **worst-case/minimax branch rule**：在 γ̂ 不确定区间内选最坏分支仍安全的那个。
3. **confidence-gated fallback**：γ_eff 接近 13 dB 阈值 ±margin 时回退到更稳的分支。
4. **hysteretic selector**：加迟滞，避免 γ̂ 抖动导致分支翻转。
5. **calibration-free rank/statistic selector**：完全不依赖 γ 绝对值，用 rank 或归一化统计量选分支。

每个候选单独 dev 调谐（自己的超参，公平预算），fresh held-out 评价。

**比较四方**：①原 selector（nominal 有偏 γ̂）；②conventional adapter（γ̂_est plug-in）；③最佳 robust 候选；
④true-SNR oracle（仅作 bound，不当 Go）。raw rows、paired CI、help/hurt/tie、语义 smoke、消融、复杂度齐全。

**Phase C 判据（method-production）**：只有最佳 robust 候选在 fresh held-out 上**稳定超过 conventional adapter**
（CI 不跨 0 且超 MDE），且排除额外信息/调参预算/实现伪影，才判 **terminal verdict = `DIAGNOSTIC_METHOD_SIGNAL`**。
否则 **`NO_DIAGNOSTIC_SIGNAL`**。

### 2.4 terminal verdict 五选一（主控最终接收，你给建议+证据）

- `PROBLEM_ABSENT_UNDER_TESTED_MISMATCH`（Phase A 即终止，负面有效结果）
- `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`（Phase B adapter 解决，无 signal）
- `DIAGNOSTIC_METHOD_SIGNAL`（Phase C 候选稳定超 adapter）
- `NO_DIAGNOSTIC_SIGNAL`（Phase C 候选未稳定超 adapter）
- `EXECUTION_INVALID`（无法在包内确定性修复，附原因）

## 3. 已知陷阱（基于历史失败的具体案例）

1. **win32 Python 路径是 Scripts 不是 bin**（`/c/Users/zzt/.venvs/torch/Scripts/python.exe`，不是 `bin/python`）。
2. **信道共享**（TL-13）：必须 `generate_shared_realization_apsk`，禁独立生成；seed 公式与 anchor 一致才能逐 seed 比对。
3. **common-768 口径**（不是 mixed）：NDA 和 selector 都只在 192 非 pilot symbol = 768 bit 上算错误。pilot 位置 `np.arange(0,256,4)`=64 个。DA 只评 768 位（`ne_da`），NDA 也要算 `ne_nda_common768`。锚点 raw 字段 `fixed_nda_errors`=`ne_nda_common768`、`fixed_da_errors`=`ne_da`、`selected_errors`=按 choice 取。
4. **true SNR 不进 decide**（TL-32/FR-25）：decide 的两个入参 `gamma_db, gamma_lin` 都用 receiver 持有的（有偏 nominal 或估计），绝不用 true。true 只在 `generate_shared_realization_apsk(..., gl=true,...)` 和离线 BER 评价。
5. **dev/test seed 隔离**：dev 用 seed_index 0–9，held-out 用 **seed_index 30–49**（anchor 用 0–29，禁复用 0–29 作 test；dev 0–9 是 anchor 子集，复现用，不作最终 test 判据）。fresh held-out = seed_index 30–49。
6. **复现 anchor 先于一切**：Phase A 第一步是证明你能逐 seed 复现 anchor 的 selected_errors 和 occupancy，否则后续失配注入的结论不可信。
7. **dev 前冻结判据**：0.3 dB / CI 不跨 0 这些阈值必须在跑 test 前写进 worker-log，不得 test 后补。
8. **不改原文件**：新增 `explore/nda-awgn-tracking-sandbox/_p01_*.py` 和 `results/p01_cpr_snr_mismatch/`，不动 common/params/原 selector。
9. **语义 smoke**（evidence-and-claims）：probe 跑完先验证——δ=0 时选择错误率=0、gain retention=0（恒等恢复）；CV 边界在 δ→+∞ 时应单调推更多 window 进 NDA 分支。不满足先排查代码。
10. **CI 用 paired per-seed gain_db 的 Student-t**（与 anchor `ci_t` 一致），不是 cell 聚合后的单一 ratio。

## 4. 验收（主线拿到产出后怎么检查）

- [ ] worker-log 含：判据冻结段（test 前）、Phase A/B/C 各阶段记录、terminal verdict 建议 + 证据
- [ ] artifact `results/p01_cpr_snr_mismatch/*.json`：raw rows（每 (scene,γ_true,δ,seed) 一行）+ paired aggregate + CI
- [ ] 复现 anchor 逐 seed selected_errors 与 `ccisp_family1_selector_a_30seed.json` 完全一致（附比对证据）
- [ ] true SNR 未进任何 decide 调用（grep worker-log + 代码确认）
- [ ] fresh held-out seeds（30–49）独立于 dev（0–9），dev 判据不是最终 test 判据
- [ ] 语义 smoke（δ=0 恒等、δ→+∞ 单调）PASS
- [ ] terminal verdict 五选一明确，附 comparator/最佳候选/CI 数字

## 附：产出回传位置

- worker-log: `projects/thesis-fso/worker-logs/step-{NNN}-p01-cpr-snr-mismatch.md`（NNN 取当前最大+1）
- artifact: `projects/simulation/results/p01_cpr_snr_mismatch/`（raw + aggregate json）
- 不改 common/params/原 selector；不 push；commit 由主控统一做。
