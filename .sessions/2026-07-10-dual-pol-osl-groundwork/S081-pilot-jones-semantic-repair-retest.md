# [S081] Pilot-Jones complex-Jones/PMD/PDL 语义修复、重测与条件式方法 MVE（T004）

> 2026-07-24 | 阶段: formal GW Step 4a 维度 D（semantic repair + retest）| 状态: provisional verdict 待主控验收
> 来源: S001 / formal D064 / V038 / T004

## 目标

修复 V038/D064 定位的 T003 五项语义缺陷（噪声位置、PDL 非无源、PMD pilot 未过 FIR、B3 tapped RX→RX 自预测、PMD oracle 非 ceiling + gate 混合），在隔离闭包重建正确 signal/noise/pilot/channel，合法 conventional baseline + oracle，M0–M4 paired headroom 重测，problem 存活则同包完成多机制方法 MVE 与双审查。止于 Step 4a provisional verdict。

## 记录

**Phase 0/2 复现与语义门**：`tests/test_pilot_jones_complex_repair.py` **25 passed**（7 legacy-regression 证缺陷存在 + 18 repair-semantic gate）。`semantic-failure-reproduction.json` 记录五项 old_behavior/expected/reproduced/source_line/fix。T003 全部 immutable（零改动）。

**Phase 1 contract**：`repair-contract.yaml` 冻结 primary signal chain（TX frame 先换 pilot → √h R(theta) clean → passive component → post-component 同 n_post → RX）。PDL 无源 σmax=1。PMD FFT-circular（前向与 oracle 同约定 + PMD_GUARD=8 排除块边界 transient）。关键工程发现（TL-22）：初版前向 edge-padded 时域卷积与 oracle FFT-circular 不一致致 M3/M4 oracle 恢复误差 0.49/3.9（完全错）；统一用 `pmd_circular_freq` + guard 排除后 M0–M4 noiseless 恢复 <1e-9。

**Phase 3/4 headroom**：B\* 每 family validation 冻结（B2 λ validation-optimal=0.1 for 弱 PDL；B4_fde for 强 PDL；B1 for 弱 PMD；不按名字指认 B3）。**problem_survives=True**：M2 PDL 1dB（APPROX-verified）headroom **0.77 dB**（impairment-added 0.69 dB，非 floor）；strictly-VERIFIED DGD 6ps null（0.089 dB）。无 oracle anomaly。fresh-test stress trend 全正。

**Phase 4.2 adaptation-scan + 方法候选**：A1–A6 全扫无 method signal。P1/P1_whiten/P2/P3(joint)+B3_pmd_pool 全测，fresh test 无任何 8/10 胜（P2 M3 160ps stress 7/8 最高，未达门）。method_succeeds=False。

**Phase 5 双审查**：独立 science-critic subagent 攻击 11 项 + 1 bug。verdict SURVIVES but weakened/scoped，全部响应：(1) B\* λ 重冻结 0.1（headroom 1.02→0.77）；(2) 框架改为"弱 PSP 噪声放大"；(3) 补测 P3 joint + pooled tapped（仍输）；(4) PDL 重标 APPROXIMATE-verified；(5) 修 test-headroom lookup bug。Integrity verifier（自验）：T003/protected/shared 全零改动，seeds disjoint，paired fingerprint 共享，`git diff --check` 干净。

**provisional verdict = `PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL`**。

## 决策引用

- D064：授权 T004 语义修复重测（**继承，未新建 D065**——provisional verdict 待主控验收）
- V038：T003 科学语义否决（五项缺陷定位）
- 无新建 D###（执行方不进 Step 5，provisional verdict 由主控接收后再定）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（D064 授权的 semantic repair + retest + 条件式 MVE，止于 provisional verdict；未进 Step 5/Contract/Execute，未改 protected/Skill/controller/shared canonical generator/params/common，未复活 Scout/P03，未 push）

## 后续

- **Provisional verdict = `PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL`**（允许枚举）：complex-Jones/PMD/PDL 语义修复后，**PDL (M2) 问题在 approximately-verified 物理范围存活**（1 dB PDL → 0.77 dB Q² headroom，impairment-added，非 floor；strictly-VERIFIED DGD 6ps null）；但 P1/P1_whiten/P2/P3 四个机制不同候选（含 joint tracker）均不敌 validation 冻结的最强合法传统 baseline B\*。
- **与 T003 的科学关系**：T003 的 `PIVOT_MODEL_NOT_JUSTIFIED`（"PDL 无问题"）是噪声位置错误的**构造恒等假象**；修复后 PDL 问题确实存活——这是更准确、更保守的科学状态。T002 的 `UNITARY_REAL_ROTATION_MCA_KILLED` 仍有效（扩展为：即便 passive PDL，问题存活但无方法关闭）。
- Pilot-Jones family **不在本轴关闭**，仍 `PILOT_JONES_FAMILY_UNRESOLVED`。complex-Jones/PMD/PDL axis 继续 UNRESOLVED。
- M4（PDL+PMD 联合）仅 limiting sensitivity 未闭合，claim 收窄到 APPROX-verified 单轴（M2 PDL）。
- 待主控验收 provisional verdict；4 篇 D056 全文债继续 BLOCKED；OE2021 一阶 PMD provenance 标 unverified 债务。
- 主控可能授权下一轮更强方法候选（pilot-covariance-aware / cross-block / 条件切换），或接受 negative。
- 不复活 Scout/P03，不改 protected history。

> 2026-07-24 主控接收 amendment（V039/D065）

T004 的工程语义修复部分可复用，但 provisional
`PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL` **不予接收**。M2/M4 的 PDL
component Jones 每 64 symbols 独立重抽 U/V，相当于每 25.6 ns 无来源跳变；固定
同一 1 dB component Jones 后，impairment-added headroom 在 validation/test 仅
0.0146/0.00445 dB，原正面 signal 消失。另有 Python `hash(model_id)` 跨进程
不确定、contract N=50000/runner N=20000、10-seed contract/8-seed run 和伪
`contract_sha256` 闭包缺陷。B3 过拟合只适用于 6 equations/6 coefficients 的
arbitrary per-block tapped LS，不得外推为真实系统普遍 pilot-budget limit。

当前状态改为 `T004_POSITIVE_GATE_INVALIDATED / T005_TEMPORAL_ADJUDICATION_READY`；
complex component rescue axis 仍 UNRESOLVED，不进 Step 5。
