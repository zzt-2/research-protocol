# Q1 semantic smoke 独立复验报告

> verifier: `semantic_smoke_verifier`（fresh-context full re-verification）
> 日期: 2026-08-07
> 最终裁决: **PASS**
> blocker count: **0**（Critical 0 / Important 0 / Minor 0）

## 执行边界

- 唯一审查合同为 T016；重新对照 T015、实施计划、Step 4a §4、D010–D011、S003、H004、V007、Probe README/core/runner/tests、全套 artifacts、worker log 与 scientific report。
- 这是完整复验，不是只看修复补丁。仅重跑 task-control、focused pytest、identity-only 和只读独立重算；没有重跑 grid，没有修改 canonical/code/artifact/governance，没有 commit/push。
- 本报告为唯一写入，覆盖 verifier 自己的前版 FAIL 报告。

## Verdict

- **spec compliance: PASS**
- **code/science quality: PASS**
- **最终: PASS**

## Tests / identity

- T015 task-control：PASS；T016 task-control：PASS。
- fresh focused pytest：**28 passed in 2.89s**。
- fresh `--identity-only`：exit 0；四法均返回 `(0,0,0)`，identity/paired-realization/truth-isolation/score-comparability 全 True。
- estimator API 只接受 `ReceiverVisible/config/grid/method`，不接受 `TruthMetadata`。

## Artifact cardinality 与 hash closure

- 独立解析：180 observations、180 truth、720 method rows、180 NPZ surfaces、180 surface-index entries、5 条 TDD evidence。
- 人口严格为 residual noiseless 75 + residual minus6db 75 + stress noiseless 30；每 cell 恰有 B0/B1/B2/C 四行，无孤儿、重复或缺 method。
- cell/realization/rx/grid/score 引用链闭合；180 个 NPZ key 与 surface index 一一对应。
- manifest 自哈希、provenance 中全部 artifact SHA256、core/runner SHA256、HEAD 均独立重算一致。
- B1/C surface SHA256、完整候选 path、独立 lexicographic argmax、score 与 estimate 在 180/180 cells 一致。

## 独立重算

| Layer | B0 | B1 | B2 | C | G_C | coverage B1/B2 |
|---|---:|---:|---:|---:|---:|---:|
| noiseless | 0/75 | 0/75 | 0/75 | 0/75 | 0.0 | N/A / N/A |
| minus6db | 58/75 | 59/75 | 58/75 | 59/75 | -0.0172413793 | N/A / N/A |
| stress（隔离计数） | 0/30 | 0/30 | 0/30 | 0/30 | 不进入 primary reducer | 不适用 |

- B0 stable adjacent 2×2 wrong-basin：0 个；独立拓扑重算与 summary 一致。
- B2：180/180 traces 非降，`iterations<=8`，trace 长度符合 `1+2*iterations`。
- residual separability 独立分层：noiseless max AIR=`0.4155313607311553`，minus6db max AIR=`0.6357717679002818`，两层均非 exact-separable。
- stress AIR=`0.04797495564091718`，明确为 `diagnostic_only_excluded`；改变 stress diagnostic 不改变 residual reducer。
- 独立 reducer：两层均为 `STEP4A_PREFLIGHT_KILL_OR_PIVOT`；最终 terminal 与 reason ordering 完全一致：B1/C 等价 → 无稳定 2×2 → noiseless B0 零误锁 → 两层 `G_C<5%`。

## B1/C independence

**PASS。** 动态 spy 显示一次 `estimate_all` 创建 4 个不同 `_ScoreAccessor`；B1 与 C 各自独立访问完整 residual grid 的 735 candidates，result object 不同，不存在 B1→C 或 C→B1 直接调用。两者只复用共同 score/argmax helper，符合唯一 score/tie-break 合同，不是 result alias。

## Traversal / compute ledger

- ordered `visited_candidate_indices` 对 720/720 method rows 与独立重演完全一致，重复访问被保留。
- B0/B2 共 360 rows 均满足 `visited_candidate_count > unique candidate score calls`；residual B1/C 共 300 rows 均为完整 735-candidate path。
- `candidate_score_calls == unique_candidate_score_calls == unique(path)`；`complex_macs = unique score calls × 188`；FFT/插值计数自洽。
- timing ledger 每项均为 warm-up 1 次、同进程 5 次 raw timing，median 独立重算一致。

## Plot / provenance / claim ceiling

- 独立按“最大 B0 final-decision top1/top2 margin + cell-id tie-break”选中 `residual|minus6db|d=+8|tau=+0.0|cfo_hz=-100000000.0`，margin=`0.0051385603251201395`，与 summary 一致。
- PNG 目视确认 identity 与最可信 wrong-basin panel 均绘制 truth 圆圈、B0 top1 红叉和图例；wrong-basin truth/top1 分离清楚。
- fresh GREEN 输出保存在 `focused-pytest-green.txt`；其 SHA256 同时与 TDD row 和 provenance 匹配。历史 RED 均明确降级为 `executor_report_only`，未冒充独立证据。
- -6 dB、fixed-seed preamble、RRC span 10 均有 diagnostic sentinel ceiling；报告没有把 deterministic grid frequency 外推为外场概率、论文数字或 continuous-estimator equivalence。

## Protected boundary

- `git diff --check`：exit 0。
- `common/`、所有 `params.py`、Skill 与 protected log 路径 diff：空。
- 四个 protected logs 的 SHA256 与既有独立锚点一致：
  - `p05_run.log` `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
  - `p05_run2.log` `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
  - `p05_run3.log` `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
  - `p05_run4.log` `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`
- worktree 中主控 governance/control 准备文件仍在 executor allowlist 之外；受保护路径无改动，本 verifier 未改动这些文件。

## Findings

- Critical：无。
- Important：无。
- Minor：无。
- 前版 3 Important + 1 Minor 均已由当前代码、重生成 artifacts 与 fresh evidence 关闭：traversal/cache-miss 分账、plot selector/markers、stress/reducer 隔离、TDD evidence 标级/hash 均独立复验通过。

## 最终结论

PASS。当前 artifacts 足以独立重算 `STEP4A_PREFLIGHT_KILL_OR_PIVOT`；该 PASS 只覆盖 D010/T015 的 deterministic semantic smoke，不将结果升级为正式 MVE、Go/Conditional Go、testbed、论文数字或连续 estimator 等价。
