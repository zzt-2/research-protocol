# RML-FSTS Q1 — Groundwork Step 4a A0 preflight

> 2026-08-09 | authority: D009-D010 | status: `ALLOW_SEMANTIC_SMOKE / NEEDS_BOUNDED_ADAPTER`

## §0 合法问题

Q1 四判据 4/4，M/C/A 与可量化对标均已在 `literature_notes_rml_fsts.md` 闭合；但只有 source fixed-`B_L` tradeoff 是 FACT。target ranking crossover、B2 后 residual、observability 和 actionability 全部仍是 UNKNOWN。Q1 是 provisional survivor，不是 Go、METHOD_SIGNAL 或 novelty closure。

## §1 方法身份与动作空间

- B0：PM-4QAM/16QAM 的论文 320-symbol FSTS，固定 lag 分别为 20/40。
- B1：同一 receiver-lag grid 上按 modulation 做 dev-global fixed-lag tuning。
- B2：dev-frozen `(modulation,TS length,receiver-measured power bin)` single-lag lookup；这是最强廉价 comparator。
- O1：hidden-cell expected-best lag，只作 headroom/Kill；per-realization hindsight 另列但不承重。
- C1：当前不存在。只有 B2 后稳定、可观测、可行动 residual 才允许构造。

Wang `B_L` 同时进入发端结构与接收 fine estimator。为保持同一 waveform/overhead/paired samples，D010 固定发端论文结构，只扫描 receiver lag `L_rx={10,20,40,80}`；off-default lag 用 receiver-known FSTS 做 phase de-rotation，default lag 必须精确退化为 Eq. (8)–(11)。这是 bounded adapter，不是 Enhanced 精确复现或新方法。

## §2 Deployable 信息边界

online known：modulation、TS length、symbol rate、known FSTS、action grid、frozen receipt。receiver-estimated：action 前从相同 FSTS 得到的 raw energy/power proxy 与无 truth 的相关质量。oracle/post-hoc：true CFO、true `h`/SNR/turbulence、component seeds、per-action error/best label，只能进入 scorer/O1。B0/B1/B2 的真实 caller→callee 必须通过 hidden-truth metamorphic test。

## §3 Baseline ladder 与公平性

所有 action 共享同一接收样值、coarse stage、320-symbol overhead、search grid、dev budget 和 metric。B1/B2 只读 dev，test 前 receipt 冻结；test 只评价。Go 对手是 B2，O1 只回答 headroom。raw population 不删失败样本；先落 per-realization rows，再确定性聚合和 paired CI。

## §4 物理条件与 provenance

10 GBaud、PM-4/16QAM、320 symbols、CFO `(-1.1,+1.1) GHz`、Tx/LO linewidth 50 kHz来自 Wang 2023。weak/strong Gamma-Gamma `(11.6,10.1)/(4.2,1.4)` 来自 Gu 2022/Al-Habash 2001 的项目真相源；它们是有溯源的 weak/strong baseband regimes，不等价声称 Wang `C_n^2` 映射。单 FSTS 仅 32 ns，而湍流相干时间为 ms 量级，因此帧内准静态是理论预期。SNR `10/20 dB` 明确标为未验证诊断范围；不冒充 dBm receiver power或星地系统数字。

## §5 Testbed readiness

仓库不存在 faithful Wang fine FOE；旧 B3 是 QPSK fourth-power FFT/伪 two-stage path，且 true `h` 泄漏。现有 PM symbol、GG/AWGN 和 artifact/metamorphic patterns 可支撑不改 `common/params.py` 的 4-file isolated adapter。因此状态是 `NEEDS_BOUNDED_ADAPTER`，不是 READY 或硬 BLOCKED。起飞门是：Eq. (7)–(11) identity、default-lag equivalence、noiseless/wrap calibration、same-rx pairing、visible/truth isolation、raw cardinality与 deterministic recompute 全过。

## §6 最快证伪与 terminal

最小 grid 为 `2 modulation x 2 SNR x 2 turbulence`，每 cell `8 dev +16 test` paired seeds。先查全条件 best-lag ranking；完全无稳定 crossover立即 `STEP4A_KILL_NO_RANKING_CROSSOVER`。若变化仅被 B2 power lookup 吸收，或 B2 后两项门限均未达，则 `STEP4A_RESOLVED_BY_CONDITIONED_LOOKUP`。只有 B2 后 residual 达 `20% NMSE` 或 `10 pp outage`、跨多条件/seeds稳定且 action 前可观测，才允许 fresh bounded MVE；否则 terminal 3。invalid identity/data contract 才用 terminal 5。

## A′ / A / B

当前结构优势为零：若最优 lag 只由 modulation/TS/power决定，产出就是 conventional lookup。空白可能源于廉价 lookup 已吸收、320-symbol 时间窗过短、condition action 前不可观测、generic multi-lag prior art/SSRN 全文债。semantic smoke 的职责是按该顺序证伪，不能从“没人确认做过”推出方法价值。

## Testbed readiness 结论

`ALLOW_SEMANTIC_SMOKE / NEEDS_BOUNDED_ADAPTER`。允许实现和运行一次冻结 smoke；不允许提前造 C1、扩物理范围、进入 Contract/Execute 或写 novelty。

## 证据

- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-a0-independent.md`
- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-formula-identity.md`
- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-testbed-readiness.md`
- Wang canonical HTML `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:103-215,231-319`
