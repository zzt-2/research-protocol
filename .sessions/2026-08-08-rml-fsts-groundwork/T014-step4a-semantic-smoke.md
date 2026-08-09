# Task Brief: RML-FSTS Step 4a semantic-smoke implementation and execution

> 来源: S004 / D010 | 日期: 2026-08-09
> 执行产出: isolated source/tests/artifacts + `projects/thesis-fso/worker-logs/step-4a-rml-fsts-semantic-smoke.md`

## 0. 任务

在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2` 按 `projects/simulation/explore/rml-fsts-step4a/contract.json` test-first 实现并运行一次 semantic smoke。不得改合同、`common/`、`params.py`、旧 B3、治理 owner、论文或四个 `p05_run*.log`；不得 commit/push。最多 15 分钟运行时间。

## 1. 必读

- `contract.json`（唯一参数/metric/terminal truth source）
- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-formula-identity.md`
- `projects/thesis-fso/worker-logs/step-4a-rml-fsts-testbed-readiness.md`
- `projects/thesis-fso/rml-fsts-groundwork/step4a-a0-preflight.md`
- Wang shared canonical `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:103-215`
- engineering pattern only: `projects/simulation/explore/oversampled-coherent-sync-q1/` and its focused tests

## 2. 最小文件

- `projects/simulation/explore/rml-fsts-step4a/rml_fsts_core.py`
- `projects/simulation/explore/rml-fsts-step4a/run_semantic_smoke.py`
- `projects/simulation/tests/test_rml_fsts_step4a.py`
- generated `projects/simulation/explore/rml-fsts-step4a/artifacts/*`
- worker-log path above

## 3. 强制实现

1. 精确 Wang FSTS identity builder：paper `B_N/B_L_tx`、X/Y within-symbol swap、adjacent-block swap、front/back conjugate symmetry；输出每极化恰 320。
2. Eq. (7) coarse；coarse compensation；cross-pol receiver lag `L_rx` fine；default lag 去旋恒 1并与 Eq. (8)–(11) exact path 数值等价。
3. 同一 immutable rx samples 扫 `{10,20,40,80}`；off-default 仅用 known FSTS phase de-rotation，不读 payload/truth。
4. 显式注入 CFO、100 kHz combined Wiener phase noise、weak/strong quasi-static Gamma-Gamma、10/20 dB AWGN；component seeds独立派生。
5. frozen visible/truth dataclasses；B0/B1/B2 method API 不接 truth。power proxy 从 rx samples 算；dev median bin/lookup与 B1写 freeze receipt，test 前 seal/hash。
6. raw observations/truth/action/method/scores → deterministic summary；cardinality/referential integrity/hashes/provenance。
7. B0/B1/B2/O1/O1_hindsight；C1在门前只写 `NOT_CONSTRUCTED_BY_GATE`。
8. ranking crossover、NMSE/onset+severe outage、fine-range false lock、B2 residual、paired delta/95% CI、唯一 smoke reducer。
9. runtime hidden-truth metamorphic test 从 real runner method entry 到 estimator；另测 visible power变化可改变 B2 bin/action（若 lookup actions不同，否则明确 skip原因）。

## 4. TDD/validity gates

先写聚焦测试并记录真实 RED 输出，再实现。必须覆盖：length/structure、Eq.7-11 noiseless identity、wrap边界、default equivalence、action非 no-op、paired identical rx hash、truth mutation invariance、dev/test/receipt seal、raw重算、terminal reducer boundaries。执行 fresh focused pytest；任何 validity gate失败都返回 execution invalid，不下科学 terminal。

## 5. 科学边界

- 这是 post-MRC/pol-demux source-domain diagnostic，不是完整 Wang system或星地部署。
- Enhanced 公式不实现；非默认 lag不冒充 paper point。
- O1 headroom不能触发 Go；若 reducer推荐 MVE，只回报 gate evidence，不自行构造 C1/MVE。
- 不因结果“不好看”改 SNR、lag、seeds、bin、阈值或物理模型。

## 6. 回传

返回：pytest命令/结果、run命令/耗时、artifact paths/hashes、B0/B1/B2/O1数字与 paired CI、crossover/B2吸收/机制、smoke reducer、是否合法进入 bounded MVE。完整数据写 worker-log，聊天只给精简摘要。
