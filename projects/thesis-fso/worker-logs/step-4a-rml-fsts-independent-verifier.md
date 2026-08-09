# RML-FSTS Step 4a independent terminal verification

> 2026-08-09 | fresh-context read-only scientific terminal verification | authority request: T019

## Verdict

**PASS。P0/P1/P2 = 0/0/0。**

独立重放支持唯一 terminal：`STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`。本 PASS 只确认 Step 4a 在 validity/calibration 起飞门前被硬阻断，以及相应 owner/artifact 边界一致；它不构成 performance grid、MVE、Q1 Kill/Resolved/Go、`METHOD_SIGNAL` 或贡献成立。D011 在终验前明确只具有 `PENDING_INDEPENDENT_VERIFICATION` 权限（`.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:355-366`）。

## Evidence replay

1. **恢复事实**
   - fresh command `git rev-parse HEAD` 返回 `80a9dc1e5ed9c1a22a0edd7d1172c19372a1ac2b`；`git diff --cached --name-status` 为空。Step 4a 起点的 contemporaneous session evidence 记录同一 HEAD、原 tracked/staged diff 为空、仅四个既有未跟踪 `p05_run*.log`（`.sessions/2026-08-08-rml-fsts-groundwork/S004-step4a-feasibility.md:12`）。本终验没有把当前已形成的 Step 4a dirty delta 倒推成起点状态。
   - shared 130981 canonical 位于 `D:/code/study/research-protocol/papers/doi/10.1016_j.optcom.2024.130981/`；fresh SHA-256 为 PDF `2a5728193de8fac0ffbd1c55f60847fe44b9d462c70e13c8325c798c84feefc2`、content `67fa0ea9f1c8b8c37b48bc87474c4a7d7b565b2ebe3f0c12b44cca9d8aa66ecb`。原文是固定分块 FFT、跨块均谱、正负谱功率比 coarse FOE，且 FFT/power 点是被评参数，不是 condition→lag/window selector（`D:/code/study/research-protocol/papers/doi/10.1016_j.optcom.2024.130981/content.md:47,71-87,127-141`）。
   - Q1 在 Step 4a 前仅为 `PROVISIONAL_SURVIVOR_WITH_FULLTEXT_LIMITATIONS`，Step 4a 尚未启动；B2 conditioned single-lag lookup 是不可删的 strongest cheap comparator（`.sessions/2026-08-08-rml-fsts-groundwork/H005-step3-5-provisional-survivor.md:8,29,68-69`；`projects/thesis-fso/literature_notes_rml_fsts.md:38,89`）。

2. **A0 完整性**
   - owner 逐项包含 §0–§6、A′/A/B 与 testbed readiness（`projects/thesis-fso/rml-fsts-groundwork/step4a-a0-preflight.md:5-45`）。B2 是 Go 对手、O1 只作 headroom/Kill、C1 在 residual 门前不存在（同文件 `:9-15,23-25,35-45`）。
   - deployable/oracle 边界明确：true CFO、true `h`/SNR/turbulence、seed 与 per-action outcome 只能进 scorer/O1；runtime 需过 hidden-truth metamorphic test（同文件 `:19-25`）。独立 A0 进一步冻结同预算 action search、dev/test 隔离、Go/Kill 对手分离，未把 consistency check 当科学结果（`projects/thesis-fso/worker-logs/step-4a-rml-fsts-a0-independent.md:44-62,95-111`）。

3. **D010 失败语义**
   - V006 在任何 RED/grid 前判定两项 P0：off-default receiver-lag adapter 改变原联合 `(B_N,B_L)` 方法对象；未验证 SNR + Gu scalar-GG 缺 source calibration/B0 anchor（`.sessions/2026-08-08-rml-fsts-groundwork/verifications.md:130-152`；`.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:312-353`）。D010 合同自身为 `REJECTED_PRE_RUN` 且 `terminal_authority=NONE`（`projects/simulation/explore/rml-fsts-step4a/contract.json:3-4`）。
   - fresh recursive listing 显示 `projects/simulation/explore/rml-fsts-step4a/` 只有 rejected `contract.json` 与 terminal receipt；按 `rml_fsts_core|run_semantic_smoke|test_rml_fsts|raw|result|mve|grid` 搜索为 0 项。因此不存在 scientific raw row、paired delta/CI 或 result-driven repair；receipt 也冻结 raw rows=`0`、grid/MVE=`NOT_RUN`（`projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-terminal-receipt.json:17-29`）。

## Scientific semantics

1. **structural action-before causality：确认。** Wang 的 `(B_N,B_L)` 定义并构造发端双偏振 FSTS，fine FOE 又以 `B_L` 为相关 lag（`D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md:107,185-205,231`）。因此改变原 Q1 structural action 必须重建发端 FSTS；从“当前 FSTS”接收样值形成的 power proxy 必然晚于该动作。Wang receiver chain 没有 probe/previous-frame feedback/state lifecycle（同原文 `:241-243`）。增加这些机制会改变 protocol/overhead，而不是补一个本地参数（`.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:372`）。
2. **source-channel non-equivalence：确认。** Wang 使用 Fourier phase screen、0.2 m aperture、SMF coupling、branch fading/phase 与 MRC（Wang canonical `content.md:241-243`）；项目 common 只生成 scalar irradiance `I=X*Y` 并以 dimensionless `gamma_bar` 注入 AWGN（`projects/simulation/common/_gg_time.py:1-97`；`projects/simulation/common/_dual_pol_channel.py:95-132`）。Gu 的 plane-wave scalar Gamma-Gamma 公式只给 irradiance marginal，不能恢复 phase screen、aperture/SMF 与 branch joint statistics（`papers/doi/10.3390_app12073331/content.md:84-117`；`projects/thesis-fso/worker-logs/step-4a-rml-fsts-source-calibration.md:173-188`）。
3. **dBm→离散噪声不可唯一：确认。** Wang 只给 LO power/responsivity，并笼统说明考虑 shot/thermal noise，未给 noise bandwidth、BPD/TIA/温度负载、dark/background、filter/ADC normalization（Wang canonical `content.md:243`）。项目 receiver-noise 公式显示这些量是把光功率闭合到电/离散噪声所必需的（`毕设/formulas-master.md:175-205`）；故不能从 Wang dBm 轴唯一导出 post-ADC `E[|w[k]|^2]`（`projects/thesis-fso/worker-logs/step-4a-rml-fsts-physical-transfer.md:11-17,60-84`）。
4. **B0 numeric gate：不可执行。** 当前没有同时闭合的 source point、source equation 与预冻结 numeric tolerance；无噪 identity 或 synthetic SNR 拟合不能替代（`projects/thesis-fso/worker-logs/step-4a-rml-fsts-source-calibration.md:233-245,261-269`）。
5. **缺图只是 recoverable gap。** fresh direct recheck 的 Fig. 8/10/11/12 四个 `large.gif` 均为 HTTP `403`、`text/html`、4141 bytes、同一响应体 SHA-256 `3d8b074f...d749dca41`；不是 GIF。它阻止读取 ticks/逐点曲线，但即使恢复原图也不会自动修复 causality、channel equivalence 或 noise-identifiability（`projects/thesis-fso/worker-logs/step-4a-rml-fsts-wang-figure-axis.md:9,19-24,34,74`；`.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:380`）。
6. **数字语义：确认未运行。** B0/B1/B2/O1/C1 performance 均为 `N/A (NOT_RUN)`；scientific raw rows=`0`，paired delta/CI=`N/A (NOT_RUN)`，C1 未构造，bounded MVE 未运行（receipt `:17-29`；`.sessions/2026-08-08-rml-fsts-groundwork/S004-step4a-feasibility.md:23-24,39-45`）。源论文数值、公式 sanity 数值和 Rytov transfer 数值均未被冒充为本轮 performance。

## Information boundary and fairness

- B0/B1/B2 的合法接口只可读 protocol-known 量与 action-before receiver estimate；true CFO/`h`/SNR/turbulence、payload/label、future sample、per-action outcome 只属于 generator/scorer/O1（`projects/thesis-fso/worker-logs/step-4a-rml-fsts-testbed-readiness.md:103-127,201-218`）。A0 对同 action grid、同 dev budget、dev/test freeze 与 same-rx pairing的公平性要求完整（`projects/thesis-fso/rml-fsts-groundwork/step4a-a0-preflight.md:21-25`）。
- 由于 performance runner、raw rows、lookup receipt 与 C1 均不存在，未发生 truth-driven deployable action、不公平 action search、同-rx 伪 pairing或 lookup 包装。D010 的潜在 identity/calibration 问题在 pre-run 即截断，不能当作“已公平运行”的证据，也没有污染科学 terminal（V006 `:130-152`；receipt `:17-29`）。
- B2 strongest cheap comparator 与 SSRN 6293357 全文债均被保留；terminal 5 没有把二者虚假关闭（`projects/thesis-fso/literature_notes_rml_fsts.md:157-170`；receipt `:89-93`）。

## Owner/artifact consistency

以下 owner 对 terminal、科学状态、数字与下一动作一致：

| owner | fresh replay |
|---|---|
| D011 | terminal 5 candidate；V007 前 pending；Q1 Inconclusive、METHOD_SIGNAL/贡献 None；三 blocker、B0 gate、全数 NOT_RUN；重开输入明确（`.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:355-395`） |
| S004 | validity-first stop、无 rows/CI/grid/MVE、只准 T019/V007（`.sessions/2026-08-08-rml-fsts-groundwork/S004-step4a-feasibility.md:19-24,52-60`） |
| topic-index | active/pending verification；failure count `0/0`；下游禁止（`.sessions/2026-08-08-rml-fsts-groundwork/topic-index.md:3,15,46-49,64-74`） |
| literature owner | candidate pending；三 blocker；B0–C1 N/A；Q1/信号/贡献 None；`0/0`（`projects/thesis-fso/literature_notes_rml_fsts.md:163-170`） |
| master-state | 相同 candidate、NOT_RUN 与重开输入（`projects/thesis-fso/master-state.md:8,38-56`） |
| H006 | pending handoff、无数据、三 blocker、next scope change（`.sessions/2026-08-08-rml-fsts-groundwork/H006-step4a-inconclusive-testbed.md:9,56-64,72-98`） |
| receipt | `terminal_authority=NONE_UNTIL_V007_PASS`；Q1 Inconclusive、failure `0/0`；三 blocker、B0 gate、reopen inputs（`projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-terminal-receipt.json:5-21,31-47,95-99`） |
| rejected contract | `REJECTED_PRE_RUN`、无 terminal authority（`projects/simulation/explore/rml-fsts-step4a/contract.json:3-4`） |

registry 仍保持专题 `active` 的 pre-V007 待验描述；这与 topic-index 的 `active/pending verification` 相符，不列为缺陷（`.sessions/2026-08-08-rml-fsts-groundwork/topic-index.md:3,15`）。

## Mechanical checks

- fresh `ConvertFrom-Json`：contract/receipt 均 PASS；`yaml.safe_load(.sessions/_registry.yaml)` 返回顶层 `dict`，PASS。10 个 T019 必需 Markdown/JSON 路径 `Test-Path` 全部存在。
- receipt 的六个 `source_logs` 逐一重算 SHA-256，`expected == actual` 为 **6/6**（receipt `:55-80`）。
- `git diff --check` exit `0`；staged diff 为空；protected science paths `common/`、`params.py`、旧 B3、paper、依赖专题 status 为空。branch=`codex/rdl-method-production-v2`，HEAD 仍为 `80a9dc1...a1ac2b`，`@{u}` 返回“no upstream configured”；本 verifier 未 commit/push。
- 四个 protected logs 仍为未跟踪、未暂存，fresh `(bytes, SHA-256)`：`p05_run.log=(641,7843b048...a4f11)`、`p05_run2.log=(2417,735e4650...c38b)`、`p05_run3.log=(929,c76887c6...344d)`、`p05_run4.log=(1430,95a1d184...621de)`；mtime 仍为 2026-07-30 21:53/22:08/22:21/22:39 +08:00。
- pre-write `git status --porcelain=v1` 的 tracked delta 仅 8 个 owner/governance 文件；untracked delta 为 T011–T019、S004/H006、Step 4a A0/contract/receipt/7 个 worker logs及四个 protected p05 logs。post-write 预期且复核只新增本指定 verifier log；没有修改 owner、contract、artifact、代码或保护日志。

## Findings (P0/P1/P2)

- **P0: 0。** 无 terminal 语义矛盾，无 blocker 伪造，无 performance 数字冒充。
- **P1: 0。** owner/artifact、信息边界、failure count 与 next action 一致。
- **P2: 0。** registry 的 active/pending 状态是 V007 接收前的显式保留，不是遗漏。

V006 的 `P0/P1/P2=2/5/2` 是对已 rejected D010 执行合同的历史 pre-run findings，不是本次 T019 owner-terminal verification 的当前 findings（`.sessions/2026-08-08-rml-fsts-groundwork/S004-step4a-feasibility.md:19`）。

## Unique terminal and next legal action

五个 D009 terminal 中只有 terminal 5 合法（terminal 定义见 `.sessions/2026-08-08-rml-fsts-groundwork/decisions.md:276-290`）：

1. 不能发 `KILL_NO_RANKING_CROSSOVER`：没有合法 scientific rows 或 crossover/paired-CI 评价。
2. 不能发 `RESOLVED_BY_CONDITIONED_LOOKUP`：B2 未实例化、冻结或评分。
3. 不能发 `KILL_NO_STABLE_OBSERVABLE_ACTIONABLE_RESIDUAL`：这要求在有效 testbed 上先得到并检验 residual/observability；当前 action-before protocol 和 source/noise calibration 在任何 scientific row 前即不成立，属于 testbed validity blocker，不是“已证明没有 residual”。
4. 不能发 `GO_BOUNDED_RECEIVER_VISIBLE_CONTROLLER_SIGNAL`：C1、fresh held-out MVE、paired CI/MDE 均不存在。
5. `INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED` 精确描述了三类独立 hard blocker 与 dependent B0 gate，且不虚构任何胜负结果。

**下一合法科学动作**：先取得 authors/source receiver+channel configuration，至少闭合 phase-screen/SMF 与 `P_rx[dBm] -> E[|w[k]|^2]`；再显式定义 action-before probe/previous-frame feedback、state lifecycle、overhead、fallback 与 stale-state semantics；之后必须先做 scope-change，才可重开 Step 4a（D011 `:395`；receipt `:95-99`）。在这些输入齐备前保持 Inconclusive 边界，禁止 performance grid、MVE、Contract、Execute 与论文写作。
