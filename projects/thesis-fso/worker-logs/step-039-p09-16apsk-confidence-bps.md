# Worker Log step-039: P09 H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH

> 2026-08-01 | campaign P09 (重定向) | verdict: EVIDENCE_INSUFFICIENT | commit: Commit 1 (20d5825) + Commit 2 (pending)

## 任务

执行重定向 P09 = `H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH`（D051 计数纠正后进入）：
- M=16APSK full blind phase search (`bps_cpr` 真实 B×N exhaustive search)
- C=有限实时计算预算
- A=每 window 对全部相位候选计算星座距离，B×N 搜索开销
- 目标=相同 receiver-visible 信息/相同延迟/相同 BPS objective 下减 distance evals 保持 full BPS 性能

## 执行

### 入口门（4/4 PASS，file:line 见 p09_entry_gate.md）
- 门1：`common/_recovery.py:91-118` `bps_cpr` 真实 exhaustive search，B×N distance evals 可裁剪；16APSK adapter 复用 `run_bps_ablation.py:82-130`
- 门2：full BPS B=64 成本 16384 evals/block 主导，sanity 实测成本确实由 B 主导
- 门3：B0 full/B1 coarse/B2 two-stage 三个传统 comparator 有身份、同信息、同延迟、独立可调
- 门4：file:line 已举
- collision：grep confidence/coarse/two_stage/early_stop/curvature 零命中（代码库无既有变体）

### chronology 闭合（修复 P08-R2 缺陷）
- freeze receipt 独立 Commit 1 (`20d5825`) 在任何 held-out test 前，`test_started=false`
- test 模式校验 source hash + contract SHA256 + receipt 自身 hash 一致后才 `test_started=true`
- held-out seeds 12000-12039 fresh，disjoint from 全部 campaign history + dev 11000-11019

### Phase A/B/C dev（seeds 11000-11019, weak@{14,16,18,20,22}dB, lw=1e4）
- **Phase A full BPS BER 曲线**: 14dB→0.051, 16dB→0.036, 18dB→0.026, 20dB→0.020, 22dB→0.016（laser linewidth lw=1e4 导致 BER floor ~0.016，物理非 bug）
- **Phase B 传统 comparator @18dB**: B1 coarse B=32 BER=0.0264 evals/sym=32 (2× reduction, BER 近同 full)；B2 two-stage 32+8 BER=0.0260 evals/sym=40 (1.6×)；16+8 BER=0.0504 (16 相位太粗)
- **Phase C 候选 @18dB**: C1 conf-gated 全 thr BER=0.0480 evals/sym=24 (conf 指标无区分度，全 refine)；C2 curv thr=0.005 BER=0.0498 evals/sym=16.2；**C3 early-stop Bmin=8 BER=0.0255 evals/sym=8 (8× reduction, BER 近同 full)** 为最强候选

### Held-out test（frozen cell weak@18dB, n=40 fresh traj seeds 12000-12039, receipt hash 校验通过）
| method | BER_mean | CI [lo,hi] | ΔBER | ~ΔSNR(dB) | evals/sym | reduction | 双门 |
|---|---|---|---|---|---|---|---|
| B0_full (B=64) | 0.0314 | [0.0256,0.0374] | 0 | 0 | 64.0 | 1.0× | — |
| B1_coarse (B=32) | 0.0331 | [0.0271,0.0393] | +0.0017 | +0.36 | 32.0 | 2.0× | FAIL(<4×) |
| B2_two_stage (32+8) | 0.0333 | [0.0271,0.0398] | +0.0019 | +0.41 | 40.0 | 1.6× | FAIL |
| C1_conf_gated | 0.0509 | [0.0427,0.0591] | +0.0194 | +4.23 | 24.0 | 2.7× | FAIL(ber 差) |
| C2_curv | 0.0605 | [0.0530,0.0681] | +0.0291 | +6.32 | 16.3 | 3.9× | FAIL(ber 差) |
| **C3_early_stop (Bmin=8)** | **0.0312** | **[0.0255,0.0372]** | **-0.0002** | **-0.05** | **8.0** | **8.0×** | **complexity PASS, non-inf CI upper 0.03716 > thr 0.036427 FAIL** |

### Terminal verdict: EVIDENCE_INSUFFICIENT

- C3_early_stop 实测 8× complexity reduction + BER 点估计与 full BPS 持平 (0.0312 vs 0.0314)，**complexity 门 PASS**
- 但 BER CI upper (0.03716) 略超 non-inferiority 阈值 (b0_ber+mde_ber=0.0314+0.005=0.036427)，**non-inferiority 门 FAIL by 0.00073 BER (~0.16 dB)**
- CI half-width ~0.006 BER (~1.3 dB) 远大于 MDE/2 (~0.0025 BER / 0.05 dB)，n=40 traj 不足以 resolve 0.10 dB MDE（需 n~2000+ traj 按 1/√n 缩放）
- **诚实结论**：C3 early-stop 是有前景的 bounded pre-formal carrier（dev/test 一致的 8× reduction + BER 持平信号），但 n=40 统计功效不足以 confirm 0.10 dB MDE 非劣。EVIDENCE_INSUFFICIENT 是唯一合法诚实终态（非 METHOD_SIGNAL 因 CI 不过，非 NO_SIGNAL 因有点估计信号）。

## 复杂度计数审计（V078 check 6 PASS）

- B0_full: n_evals = B×N = 64×256 = 16384/block ✓
- B1_coarse(B=32): 32×256 = 8192 ✓
- B2_two_stage(16+8): (16+8)×256 = 6144（两 stage 全计）✓
- C1_conf_gated: 16×N + n_refined×8（refinement 全计）✓
- C2_curv: 16×N + n_refined×8 ✓
- C3_early_stop: B_used×N（adaptive width）✓

## 物理机制（为什么 C3 Bmin=8 在 16APSK 上有效）

(8,8)-16APSK 两环各 8 点 → 升幂 M0=8 → 相位模糊 2π/8 = π/4。BPS 测试相位 2π/B 均匀分布；B=8 时相位间距正好 = M0 模糊间距 π/4，**一个测试相位落在每个模糊分支内**，足够 resolve 相位。B=64 (full) 的更高密度在 lw=1e4 + weak 湍流 operating region 是冗余的——这是 C3 early-stop Bmin=8 有效且不丢性能的物理原因（非 bug，非 overfitting）。

## 产物

- sandbox: `projects/simulation/explore/p09-16apsk-confidence-bps/{p09_bps_methods.py, p09_run.py, p09_entry_gate.md}`
- artifacts: `projects/simulation/results/p09_16apsk_confidence_bps/{p09_freeze_receipt.json+sha256, p09_dev_phase{A,B,C}_raw.json, p09_test_raw_rows.json, p09_test_result.json}`
- worker-log: 本文件
- Commit 1 (20d5825): 计数纠正 + freeze receipt (pre held-out test)
- Commit 2: held-out test artifacts + 治理同步 (D052/V078/CP043)

## 不做

- 不建立 method card（verdict 非 METHOD_SIGNAL）
- 不宣称 C3 early-stop 为正式方法（claim ceiling 维持 LOCAL_SLICE / NONBINDING_DIAGNOSTIC；EVIDENCE_INSUFFICIENT 非 signal）
- 不 push
- 不重开已关闭族 / 不动 NDA-ML body / 不改 protected owner/formal/Skill/thesis framework
