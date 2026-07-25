# Worker Log — T007 B1 adaptive phase-estimation window method package

> 阶段: GW Step 4a (维度 D MVE) | 日期: 2026-07-25 | 状态: PARTIAL
> Authorization: D013 (epoch 9, ADAPTIVE_PHASE_WINDOW_METHOD_PACKAGE)
> Source: live-test `T007-b1-adaptive-phase-window-method.md`
> Verdict: **`KILL_NO_ADAPTIVE_WINDOW_SPACE`** (structural gate failed; Phase C/D not executed)

## 1. 任务与授权边界

执行 T007 任务包：在 GW Step 4a 内完成 B1 自适应相位估计窗的结构性问题门，
门通过则同包实现三种 receiver-visible 自适应窗方法（P1/P2/P3）与 paired test。
**不进 Step 5/Contract/Execute；不修 T006；不复活 Scout/P03；不改 shared
generator / params.py / Direction Lab Skill。** 聊天只返回四行。

## 2. 实际完成

### Phase A — frozen contract (DONE)

- `explore/adaptive-phase-window/source-closure.yaml`：sat.1553 L440 open problem
  与 [60] Leven 理论锚的逐字引用；参数 provenance（paper-sourced /
  canonical-project / validation-tuned）；3 条可证伪理论预期（E1/E2/E3）；
  identity separations；forbidden 项。
- `explore/adaptive-phase-window/MVE-SPEC.md`：M-C-A 问题定义、条件表（clean/
  operational/adversarial sourced + stress secondary）、frozen window grid
  {8,16,32,64,128,256}、metrics、Phase B 结构门、Phase C 三方法、Phase D
  pre-registered verdict。
- `explore/adaptive-phase-window/contract.yaml`：frozen literals、seed plan
  （78xx val / 79xx test，与 T005 74xx/75xx、T006 76xx/77xx 不相交）、
  determinism/identity guards。

### Phase B1 — semantic gates (DONE, 8/8 PASS)

`explore/adaptive-phase-window/semantic_gates.py` + `channel.py` + `cpe.py` +
`evaluator.py`。8 个 gate 全过：noiseless、known-constant-phase（legal pi/2
resolve）、Wiener window tradeoff、phase-sign + linewidth→variance（8× ratio）、
**pi/4 fourth-power bias + legal pi/2 ambiguity**（QPSK 与 square 16-QAM 均为
pi/4 bias，T006 "doc 4 / code 8 pi/4" mismatch 已禁）、pilot/data equal energy
+ mask、no-future/no-truth in deployable signatures、window path varies with
conditions。

源 identity 闭合，未触发 `BLOCKED_SOURCE_IDENTITY`。

### Phase B2 — structural KILL gate (DONE, FAILED → KILL)

`explore/adaptive-phase-window/b2_structural_gate.py`。在 AWGN+Wiener 静态
slice 上扫 window grid × SNR{10,14,18,22} × linewidth{10k,20k,80k} × 5 val
seeds，再在 GG block-fading 上做 per-block oracle headroom。

**结果（QPSK + 16-QAM 双调制，均判 KILL）：**

| 项 | QPSK | 16-QAM |
|---|---|---|
| E1 (SNR↓→N↑) majority | 2/3 PASS | 3/3 PASS |
| E2 (linewidth↑→N↓) majority | **0/4 FAIL** | 4/4 PASS |
| kill1 (E1/E2 方向) | **TRIGGERED** | not |
| kill2 (universal fixed) | not testable (FEC unreachable on AWGN slice) | not testable |
| kill3 (oracle headroom <0.5dB) | NOT (median +1.026 dB) | NOT (median +0.413 dB) |
| kill4 (features \|rho\|<0.5) | **TRIGGERED** (ρ_SNR=-0.074, ρ_innov=+0.24) | **TRIGGERED** (ρ_SNR=-0.387, ρ_innov=+0.353) |
| **verdict** | KILL | KILL |

**核心发现**：oracle 空间存在（truth-assisted per-block oracle 能拿 0.4-1.0 dB
median gain over best fixed N），但**没有任何 receiver-visible feature 能以
deployable accuracy 预测 best N**。两条物理原因：
1. linewidth 轴在 satellite-FSO ECL 区间（10-80kHz）几乎退化：σ²_p=2π·Δν·T_S
   在 2.5GBaud 下仅 2.5e-5（10kHz）到 2e-4（80kHz），window ≤256 内相位跟踪
   滞后可忽略，AWGN 噪声平均主导（与 D-011/A1 一致的物理）。
2. raised-power phase-innovation estimator 被 AWGN 噪声主导，对 linewidth 几乎
   无响应（80kHz/10kHz innov_hat 比 ≈1.0），无法作 E2 deployable feature。

### Phase C — 三方法 (SKIPPED, gate failed)

任务包规定：B2 结构门失败 → 立即 Kill，不实现 P1/P2/P3。已遵守。
P1/P2/P3 的 receiver-visible controller 代码已写（`cpe.py`），但**未跑 paired
test、未生成 mechanism slice**（测试 `test_phase_c_not_executed` 强制断言无
Phase C 产物）。

### Phase D — paired test (SKIPPED, gate failed)

未执行。

## 3. 证据与测试

落盘：
- `explore/adaptive-phase-window/`：source-closure.yaml、MVE-SPEC.md、
  contract.yaml、channel.py、cpe.py、evaluator.py、semantic_gates.py、
  b2_structural_gate.py、synthesis.md。
- `results/adaptive-phase-window/`：b2_raw_{qpsk,qam16}.jsonl、
  b2_result_{qpsk,qam16}.json、b2_log_{qpsk,qam16}.txt。
- source/contract/MVE-SPEC SHA256 戳在 result JSON 与 log 里。

测试 `tests/test_adaptive_phase_window.py`（28 PASS / 0 FAIL / 0 SKIP-after-fix），
覆盖：semantic gates、theoretical direction（E1 + innov 弱响应）、identity
separations（pi/4 bias、legal pi/2 resolve、no truth/future、fixed/condition/
oracle 区分）、raw→aggregate bit-identical、verdict boundaries（6 synthetic
cases + collapse check）、determinism（subprocess fingerprint、no built-in
hash、SHA stamps match files、explicit UTF-8 IO）、protected immutability
（shared generator + params.py unchanged via git blob hash、T002-T006 artifacts
not modified）、B2 verdict is KILL + Phase C not executed。

回归：T006 (32 PASS)、T005 pilot-jones (17 PASS) 全过，无回归。

## 4. Determinism / 完整性自检

- PYTHONUTF8=1：所有 file IO 显式 `encoding='utf-8'`（测试断言）。
- 子进程 fingerprint：两独立 Python subprocess 同 seed/params → bit-identical
  RX sha256（V039 T004 教训：禁 built-in hash()，AST 测试断言）。
- source/contract/MVE-SPEC SHA 戳与实际文件 hash 一致（测试断言）。
- raw → aggregate BER recomputation bit-identical（测试断言）。
- shared generator / params.py 与 HEAD blob hash 一致（CRLF-safe via
  `git hash-object`，测试断言）。

## 5. 收尾状态

- **本对话不更新 formal owner / live control / master-state**（由主控接收）。
- 未支持独立 critic/verifier 子上下文 → final status 上限 **PARTIAL**（诚实
  上限，但全部主包完成）。
- consolidated commit 待执行（本对话只一次 commit，不 push）。

## 6. 关键不变量遵守

- 只在 GW Step 4a 内工作；未进 Step 5/Contract/Execute。
- 未修 T006、未复活 Scout/P03、未改 shared generator / params.py / Skill。
- 未获取新私有全文；sat.1553 等用既有 papers/ 全文（主仓库共享库）。
- B10/B12 channel helper / 高阶 CPR 组合未复制、未导入、未作 baseline。
- 200kHz-1MHz 仅作 stress secondary（contract 标 role: secondary），未作
  sole/primary 正信号。
- oracle per-block N 仅作 Kill/headroom bound，从未当 deployable Go 对手。
- BER 接近 0.5 的 seed 未通过 Q² 非线性变换主导 verdict（collapse_check 已实现）。

## 7. 给主控的接收要点

1. **科学结论**：B1 自适应相位估计窗在 satellite-FSO ECL 主区间（10-80kHz /
   2.5GBaud / QPSK+16-QAM / GG uplink-strong）无可部署 adaptive 空间。理论
   oracle headroom 0.4-1.0 dB 存在但无 receiver-visible feature 可捕获（最佳
   |rho|=0.387 < 0.5）。
2. **候选处置建议**：B1 作为 deployable method 在主区间 Kill；保留作 defensive
   negative-result 材料（量化回答 sat.1553 L440 open problem）。
3. **未闭合项**：kill2（universal fixed regret）在 AWGN slice 上 FEC 不可达，
   未测试；若主控认为需要在更靠近 FEC waterfall 的 SNR grid 上补测，可在
   Step 4a 内开一个 bounded 补测包（不重建方法）。
4. **status 上限 PARTIAL**：无独立 critic/verifier 上下文；全部主包已完成。
