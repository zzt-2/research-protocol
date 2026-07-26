# Worker Log — T008 B1 identity-repaired adaptive phase-window method package (v2)

> 阶段: GW Step 4a (维度 D MVE) | 日期: 2026-07-26 | 状态: PARTIAL
> Authorization: live D001 (epoch 12, B1_IDENTITY_REPAIRED_METHOD_PACKAGE) / formal D013 / system D018 / mission CP007
> Source: live-test `T008-b1-identity-repaired-method-production.md`
> Verdict: **`KILL_NO_ADAPTIVE_WINDOW_SPACE`** (§5 corrected oracle space collapsed; Phase C/D NOT executed, per T008 §5 first stop condition)

## 1. 任务与授权边界

执行 T008 任务包：在 GW Step 4a 内修正 T007 的五个 identity 缺口
(baseline / required-SNR / oracle candidate / observability / feature premature
kill)；corrected oracle 空间存活则同包完成 P1–P3 + fresh-seed paired
comparison，否则按 §5 first stop condition 作 `KILL_NO_ADAPTIVE_WINDOW_SPACE`。
**不进 Step 5/Contract/Execute；不修 T006/T007；不复活 Scout/P03；不改 shared
generator / params.py / common/_modulation / Direction Lab Skill。** 聊天只返回四行。

## 2. 实际完成

### Phase A — frozen contract (DONE)

`explore/b1-adaptive-phase-window-v2/`:
- `seed-census.yaml` — 全历史 seed 普查（T002–T007 / Direction Lab / b-series /
  cma-fade-divergence / 大 MVE 常量），冻结 fresh 8xxx 池（val 8000-8009，
  test 8100-8119，与全历史观察池不相交）。
- `source-closure.yaml` — 继承 T007 源 identity（未受争议），逐项重述。
- `MVE-SPEC.md` — 含 0.why v2（五项缺口）、5 smokes、§5 corrected gate、§10 三方法。
- `contract.yaml` — frozen literals + 五项 gap closure（每项标注 T007 defect 行号）。

### Phase B — identity smokes (DONE, 7/7 PASS)

`explore/b1-adaptive-phase-window-v2/identity_smoke.py`。7 个 smoke 全过：
1. source/algorithm identity（noiseless BER ~0；VV 相位跟踪真实 per-block 平均
   <0.05 rad；pi/4 bias 精确；legal pi/2 不变；linewidth 方差比 8.0）
2. signal/information identity（pilot/data 同物理通道 rel RMSE ~0；deployable
   签名无 truth）
3. baseline identity（B*/B-cond 是 validation 冻结整数；合成测试恢复期望值）
4. oracle/metric identity（required_snr 匹配真实曲线；无 crossing→NaN；oracle
   candidate set ⊇ B* → oracle BER ≤ B* BER）
5. observability identity（|rho|<0.5 但 exact-window acc > majority-fixed →
   rho 单独不能 Kill）
6. direction + window tradeoff（16-QAM E1 通过；BER(8)≠BER(256)）
7. input/output non-degenerate（P1 对两物理条件选不同 N multiset；P3 fallback）

源 identity + 五项 gap 闭合，未触发 `BLOCKED_IDENTITY`。

### Phase B — §5 corrected space gate (DONE, FAILED → KILL)

`explore/b1-adaptive-phase-window-v2/corrected_gate.py`。在 canonical GG
block-fading（BLOCK=100，uplink_strong α/β=1.0/0.7，linewidths 10/20/80 kHz，
SNR 工作区 12/16/20 dB，10 val seeds 8000-8009）上：

- **FREEZE B\***（validation 全局最低 mean BER）：QPSK=256，16-QAM=256。
- **FREEZE B-cond**（validation per-condition）：QPSK {clean:128, operational:128,
  adversarial:256}；16-QAM {all:256}。
- **corrected oracle headroom（B-cond vs B\*）**：
  - QPSK：median **0.000 dB-equiv**，20% trimmed **0.060 dB-equiv**
  - 16-QAM：median **0.000 dB-equiv**，20% trimmed **0.000 dB-equiv**
  - 两者 median + trimmed 均 8-15× 低于 0.5 dB KILL 阈值（FR-21 / TL-32 / FR-25）。
- **fresh test-seed 确认**（8100-8119，读 frozen 整数 only）：QPSK median
  0.0000，16-QAM 0.0000 —— 空间消失在 held-out test 上重现，非 validation artifact。
- **observability（reported, not a Kill）**：QPSK/16-QAM rho(SNR_hat,N)=0.000、
  rho(innov,N)=0.000、exact_acc=1.0、majority_acc=1.0。per-block oracle-best-N
  是常数 → rho=0 是空间消失的 *症状*，不是 Kill 原因。Kill 原因是 corrected
  headroom 字段（gap5 closure）。

### Phase C — 三方法 (SKIPPED, §5 gate failed)

T008 §5 first stop condition：corrected oracle 空间确实消失 → 允许 KILL 不实现
P1–P3。P1/P2/P3 的 receiver-visible controller 代码已写在 `cpe.py`（验证为
non-degenerate + fallback），但 **未跑 paired test、未生成 mechanism slice**
（`test_phase_c_not_executed` 强制断言无 Phase C 产物）。

### Phase D — paired test (SKIPPED, §5 gate failed)

未执行。

## 3. 五项 identity 缺口的闭合证据

| Gap | T007 defect | v2 closure | 证据 |
|---|---|---|---|
| 1 baseline | `b2_structural_gate.py:343` per-cell-per-seed 从 test truth 选 B* | B* = validation 全局冻结单一整数；test 读 frozen 整数 only | smoke3 + test_bstar_bcond_frozen_on_validation + fresh test-seed 确认 |
| 2 required-SNR | `b2_structural_gate.py:387` 硬编码 slope=0.15 造 dB | required_snr 真实曲线插值；无 crossing→NaN；verdict 用 log-BER + 真实测得 B* slope 的 dB-equiv | smoke4 + test_required_snr_real_curve_no_fabrication |
| 3 oracle candidate | oracle 候选集合/B* 包含未闭合 | oracle candidate set == WINDOW_GRID；B* 是成员（oracle BER ≤ B* BER per block） | smoke4 |
| 4 observability | 无 held-out exact-window / majority-fixed | validation + held-out test 同时报 rho/exact/top2/majority/regret | smoke5 + corrected_gate.observability 字段 |
| 5 feature premature Kill | 仅凭 `|rho|<0.5` Kill | rho 是 REPORTED 不是 KILL；§5 KILL 来自 corrected headroom | test_corrected_gate_verdict_is_kill 断言 KILL trigger 是 headroom 字段 |

## 4. 关键物理发现（TL-22 前置物理检查）

1. **HD-FEC 3.8e-3 在本评估框架下不可达**：block-buffered VV BER 在 ~7e-2 处有
   floor，来源是 (a) shared `common/_modulation` pilot-overlay 位映射 artifact
   （pilot 符号覆盖 pilot 位置但 `tx_bits` 仍持原始数据位，T008 禁止改 common）
   + (b) block=100 下 VV 相位估计噪声。所有 N / 所有方法共享该 floor，故不改变
   相对 headroom 结论；verdict 改用 paired log-BER + dB-equiv（真实测得 B* slope）。
2. **window 选择被 block size 主导**：canonical BLOCK=100 下，所有 N∈{8..256} 都
   作用于 100-symbol block（N≥100 整块平均；N<100 拆 mini-block，全读当前 block）。
   100-symbol block 内 Wiener 相位漂移可忽略（√(100·σ²_p)≤0.045 rad @ 80kHz），
   per-block 相位近似常数 → 所有 N 给出近似相同 VV 相位估计。window 选择被 block
   size 主导，不被 N 主导。
3. **linewidth 轴退化**：10-80 kHz / 2.5 GBaud 下 σ²_p 极小，linewidth-driven
   tracking-lag 项（高 linewidth 推 N↓）相对 AWGN-noise-averaging 项可忽略 → E2
   方向近退化。与 D-011/A1 (NDA-ML) 和 T007 B2 同物理。

## 5. 证据与测试

落盘（`explore/b1-adaptive-phase-window-v2/`）：
- `seed-census.yaml`、`source-closure.yaml`、`MVE-SPEC.md`、`contract.yaml`、
  `channel.py`、`cpe.py`、`evaluator.py`、`identity_smoke.py`、`corrected_gate.py`、
  `method-card.md`、`synthesis.md`。

落盘（`results/b1-adaptive-phase-window-v2/`）：
- `corrected_gate_raw_{qpsk,qam16}.jsonl`、`corrected_gate_result_{qpsk,qam16}.json`、
  `corrected_gate_log_{qpsk,qam16}.txt`。
- source/contract/MVE-SPEC/seed-census SHA256 戳在 result JSON 的 `sha` 块。

测试 `tests/test_b1_adaptive_phase_window_v2.py`（**17 PASS / 0 FAIL**），覆盖：
- 5 identity smokes（subprocess exit 0）；
- determinism（AST 无 built-in hash() of objects；subprocess fingerprint bit-identical）；
- identity separations（pi/4 bias + legal pi/2；deployable 无 truth；B*/B-cond 冻结整数）；
- real-curve required-SNR（无造 dB；无 crossing→NaN）；
- corrected-gate verdict = KILL，且 KILL 来自 headroom 不是 rho（gap5 closure）；
- Phase C not executed（无 method_* 产物）；
- raw→aggregate BER recompute bit-identical；
- YAML/JSON parse；SHA stamps 匹配文件；
- forbidden-path diff（shared common / params.py / T002-T007 artifacts / T007 worker-log 全部 == HEAD）；
- explicit UTF-8 IO；`git diff --check` clean。

回归：T007 `test_adaptive_phase_window.py` 27 PASS / 1 FAIL。**该 FAIL
（`test_sha_stamps_match_actual_files`）是 T007 内部 pre-existing drift**
（T007 的 `b2_log` 记录的 SHA 与磁盘上 `source-closure.yaml` 当前 SHA 不符，
源文件在 T007 内 result 生成后被改但未重 stamp log），非 v2 引入——v2 完全
隔离在 `b1-adaptive-phase-window-v2/`，T007 文件与 HEAD byte-identical（v2 测试
`test_t002_t007_artifacts_unchanged_vs_head` 断言通过）。不在 v2 edit scope 修。

## 6. Determinism / 完整性自检

- PYTHONUTF8=1：所有 file IO 显式 `encoding='utf-8'`（AST 测试断言）。
- 子进程 fingerprint：两独立 Python subprocess 同 seed/params → bit-identical RX
  sha256（V039 T004 教训：AST 测试断言无 built-in hash() of objects）。
- source/contract/MVE-SPEC/seed-census SHA 戳与实际文件 hash 一致（测试断言）。
- raw → aggregate mean BER recomputation bit-identical，且 recomputed B* ==
  frozen B*（测试断言）。
- shared common / params.py 与 HEAD blob hash 一致（CRLF-safe via
  `git hash-object`，测试断言）；T002-T007 artifacts / T007 worker-log == HEAD。

## 7. 收尾状态

- **本对话不更新 formal owner / live control / master-state / mission-log**
  （由主控接收）。
- 未支持独立 critic/verifier 子上下文 → final status 上限 **PARTIAL**（诚实
  上限，但全部主包 + 17 项测试完成）。
- consolidated commit 待执行（本对话只一次 commit，不 push）。

## 8. 关键不变量遵守

- 只在 GW Step 4a 内工作；未进 Step 5/Contract/Execute。
- 未修 T006/T007、未复活 Scout/P03、未改 shared generator / params.py /
  common/_modulation / Skill。
- 未获取新私有全文；sat.1553 等用既有 papers/ 全文（主仓库共享库）。
- B10/B12 channel helper / 高阶 CPR 组合未复制、未导入、未作 baseline。
- 200 kHz-1 MHz 仅作 stress secondary（contract 标 role: secondary），未作
  sole/primary 正信号；本包 §5 gate 在 10-80 kHz 主区间即 KILL，未触 stress。
- oracle per-block N 仅作 Kill/headroom bound，从未当 deployable Go 对手。
- BER 接近 0.5 的 seed 未通过 Q² 非线性变换主导 verdict（observability 字段
  标注 collapse；verdict 用 log-BER + regret）。
- §5 KILL 来自 corrected headroom（B-cond vs validation-frozen B*），**不**来自
  feature rho（gap5 closure 明确）。

## 9. formal_science_disposition（formal owner 接收用）

- **carrier**: B1 adaptive phase-estimation window（GW Step 4a）。
- **verdict**: `KILL_NO_ADAPTIVE_WINDOW_SPACE`（identity-repaired；§5 corrected
  oracle space 在 QPSK + 16-QAM 双调制、val + fresh test seed 全部消失）。
- **数字**: corrected B-cond-vs-B* headroom median 0.000 dB / trimmed
  0.000-0.060 dB（双调制），fresh test-seed（8100-8119）median 0.0000。
- **与 T007 关系**: T007 同 verdict 但未被接收（五项 identity 缺口）；v2 闭合
  全部五项缺口后达到同 verdict，且 KILL 现在 identity-correct——不可再以
  baseline/metric/oracle/observability 理由驳回。
- **不可推翻点**: §5 KILL 不是 feature-rho Kill（gap5 closure）；rho 是 reported
  不是 trigger。
- **不关闭**: 200 kHz-1 MHz stress 区间（σ²_p 大 5-50×，E2 可能可部署，但非
  primary regime，不可作 sole positive）；更大 block size 下的 adaptive window
  （out of scope，BLOCK=100 是 frozen canonical block）。

## 10. mission_method_delta（mission 接收用）

- **method delta**: NONE。无 P1/P2/P3 方法信号；无可包装方法产出；corrected
  oracle 空间消失，§5 first stop condition 允许 KILL 不实现方法。
- **harvest**: defensive negative result（identity-corrected，supersedes T007）+
  methodology template（identity-corrected structural gate）+ physics insight
  （block-size dominance + linewidth degeneracy）。详见 `synthesis.md` §9。
- **streaks**: no-method=8（CP007→CP008；T007 未接收不计入）。同轴=1（B1 首包）。
- **weight/drift**: ADEQUATE / ALIGNED。运行未跨 lane；identity 修复后 KILL 是
  诚实且 identity-correct 的；mission 从"积累方法材料"视角仍是 NONE delta，但
  消耗的治理成本（五项 gap 修复 + 同包裁决）是 v2 协议修订要消化的对象。

## 11. 给主控的接收要点

1. **科学结论**: B1 adaptive phase-estimation window 在 satellite-FSO ECL 主区间
   （10-80 kHz / 2.5 GBaud / QPSK+16-QAM / GG uplink-strong / block=100）无
   deployable adaptive 空间。corrected B-cond-vs-B* headroom median 0.000 dB /
   trimmed 0.000-0.060 dB，fresh test-seed 重现。
2. **与 T007 关系**: T007 同 Kill 未被接收（五项 identity 缺口）；v2 闭合五项
   缺口后达同 Kill，现 identity-correct。**建议 formal owner 接收此 Kill**。
3. **候选处置建议**: B1 作为 deployable method 在主区间 Kill（identity-corrected）；
   保留作 defensive negative-result 材料（量化回答 sat.1553 L440 open problem）。
4. **未闭合项**: 200 kHz-1 MHz stress / 更大 block size 下的 adaptive window 未测
   （out of scope）；若主控认为需要补测，可在 Step 4a 内开 bounded 补测包。
5. **status 上限 PARTIAL**: 无独立 critic/verifier 上下文；全部主包 + 17 项测试完成。
6. **mission delta**: NONE（无方法产出）；harvest 是 negative-result + methodology
   template。CP007 streak no-method=8。
