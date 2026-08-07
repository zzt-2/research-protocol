# Task Brief: Q1 deterministic semantic smoke 执行

> 来源: S003 / D010–D011 | 产出位置: `projects/simulation/explore/oversampled-coherent-sync-q1/`、`projects/thesis-fso/worker-logs/step-015-q1-semantic-smoke.md`、`projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-report.md`
> 日期: 2026-08-07
> 预算: 单个 ≤1 天 Groundwork Step 4a 维度 D Probe；不提交、不 push

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 30
  action_class: FORMAL_STEP4A_SEMANTIC_SMOKE_EXECUTION
  mission_checkpoint: CP017
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

严格按 `docs/superpowers/plans/2026-08-07-oversampled-sync-semantic-smoke.md` 测试先行地实现并运行 D010
冻结的 deterministic semantic smoke。比较 B0/B1/B2/C-grid；单一主维度为 wrong-basin false-lock rate。
不得把 Probe 扩成正式 MVE、testbed、production 方法或论文数字。

## 1. 必读与证据边界

1. 本任务文件与上述实施计划；
2. `projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-discussion.md` §4；
3. `projects/thesis-fso/oversampled-sync-groundwork/testbed-bom.md`；
4. `projects/thesis-fso/literature_notes_oversampled_sync.md:43-55,102-112`；
5. `code-quality.md` 及 `reference/sim-template/config.py`、`verify.py`、`experiment.py`。

本地有界负面证据结论冻结为：exact Q1 joint-vs-sequential headroom/失败/FIM 数字未找到，仍是
`EVIDENCE_GAP`；Du 2021 只提供异任务低 SNR error-propagation prior，Sun/Le Bidan/Zhou 只支持真实链已做
coarse CFO/clock preprocessing 或存在耦合污染，均不能预判 Q1 headroom。不得新增 Web 检索。

## 2. 冻结方法身份

- B0：strengthened staged common-score chain，依次 coarse CFO、timing、frame/fine CFO；中间硬判决不回看。
- B1：完整 timing bank；每个 tau 分支在完整共同 `(d,CFO)` 网格上运行同一 normalized GLRT，再按统一
  terminal score 全局选优。它与 C-grid 的 exact equivalence 是待验证的结构问题。
- B2：B0 初始化后，在同一 score 上先更新 tau、再联合更新 `(d,CFO)`；非降更新；固定点或 8 轮停止。
- C-grid：receiver-visible-only 的完整共同 3-D grid 全局 argmax，不读取 truth，不做 genie/continuous refinement。

共同 score、窗口、normalization、候选集与 lexicographic tie-break 必须唯一实现；四法不得各自复制一份略有
差异的公式。

## 3. 冻结参数与人口

- waveform：56 GBd QPSK、2 sps、RRC beta 0.1、TX/RX matched filtering、64 symbols；精确前导缺失，使用
  fixed seed `20260807` 的 diagnostic QPSK，RRC span 10 symbols 标为 implementation sentinel。
- residual truth：`d={-8,0,8}` samples，`tau={-0.4,-0.2,0,0.2,0.4}` samples，
  `CFO={-100,-50,0,50,100}` MHz；共 75 cells，是主指标人口。
- stress truth：相同 d/tau，`CFO={-5,+5}` GHz；单独报告，不并入主指标。
- hypothesis：d 为 `-10..10` samples step 1；tau 为上述五点；residual CFO 为 `-150..150` MHz step 50；
  stress CFO 为 `{-5,-2.5,0,2.5,5}` GHz。
- layers：noiseless；另跑一个 -6 dB deterministic AWGN diagnostic layer，master seed `20260808`，每 cell
  seed 用 SHA256 派生。-6 dB 只是 Le Bidan numerical-stress anchor，不是外场分布。
- 数值容差、group delay、参考平面、固定 observation window、score normalization 均须写入 manifest 与测试。

## 4. TDD 与 semantic gates

必须先见到针对缺失行为的预期 RED，再最小实现至 GREEN。至少覆盖：manifest/provenance 完整性、visible-only
API、hidden-truth metamorphic、one realization per cell、identity、timing/CFO/frame sign、common score/tie-break、
B1/C exact grid equivalence、B2 monotonic trace、false-lock/coverage 算术、stable 2x2、layer isolation、compute
ledger、terminal reducer、artifact referential integrity。禁止把“C 必须赢”写进测试。

若 identity、paired realization、truth isolation 或 score comparability 任一失败，立即返回
`SEMANTIC_INVALID` 修合同，不输出科学 terminal。

## 5. 输出与裁决

输出 manifest、observations/truth/method-results、完整 surface NPZ、ambiguity PNG、summary、terminal、provenance、
TDD evidence、worker log 和 scientific report。每个结果须能由 `cell_id/realization_id/rx_hash/grid_hash/score_hash`
闭合。真实计算量记录 complex MAC、FFT 次数/尺寸、插值次数、candidate score 次数，以及 warm-up 后同进程 5 次
wall-time median。

稳定错误区定义为：固定 frame/layer/SNR 下，存在轴相邻 2x2 tau/CFO truth cells，且四格映射到同一
wrong-basin label。primary `R_FL/G_C/coverage` 不混 stress；`miss=N/A`。

只允许下列科学终态：

1. `STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE`；
2. `STEP4A_PREFLIGHT_KILL_OR_PIVOT`；
3. `STEP4A_PREFLIGHT_EVIDENCE_GAP`。

B1/C grid-equivalent、B1/B2 任一覆盖 `>=95%`、B0 无 false lock、无稳定 2x2、或 `G_C<5%` 均 Kill/Pivot。
只有解析/数值非可分、稳定 2x2、`G_C>=5%` 且两覆盖均 `<95%` 才 Recommend。信息不足则 Evidence Gap。

## 6. 写入白名单与禁止项

允许新增/修改：

- `projects/simulation/explore/oversampled-coherent-sync-q1/**`；
- `projects/simulation/tests/test_oversampled_coherent_sync_q1.py`；
- `projects/thesis-fso/worker-logs/step-015-q1-semantic-smoke.md`；
- `projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-report.md`。

禁止修改 `projects/simulation/common/`、任何 `params.py`、旧实验、Skill、`.sessions/`、master-state、四个
`projects/simulation/explore/cma-fade-divergence/p05_run*.log`。禁止 Web、新论文下载、Q2、ML、testbed、正式
MVE、Step 5、Contract/Execute、commit、push。

## 7. 返回格式

返回 task-control 检查、RED/GREEN 命令与 exit、测试数、运行命令、artifact hashes、terminal、四法每层
false-lock counts/rates、`G_C`、coverage、stable-region、B1/C equivalence、compute ledger、warnings、实际
changed-file allowlist。任何异常先停止，不得擅改阈值或扩 grid。
