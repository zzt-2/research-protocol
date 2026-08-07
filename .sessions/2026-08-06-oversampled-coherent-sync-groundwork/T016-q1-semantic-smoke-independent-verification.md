# Task Brief: Q1 semantic smoke 独立验证

> 来源: S003 / T015 | 唯一写入: `projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-independent-verifier-report.md`
> 日期: 2026-08-07
> 角色: fresh-context spec/code/science verifier；不得代修、不得提交

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 30
  action_class: FORMAL_STEP4A_SEMANTIC_SMOKE_VERIFICATION
  mission_checkpoint: CP017
```
<!-- RDL-TASK-CONTROL:END -->

## 0. 目标与裁决

独立验证 T015 是否严格实现 D010 合同，以及 `STEP4A_PREFLIGHT_KILL_OR_PIVOT` 是否可由 artifacts 重算。
报告须分别给出 `spec compliance: PASS/FAIL` 与 `code/science quality: PASS/FAIL`，列 Critical/Important/Minor
findings 和最终 `PASS/FAIL/PARTIAL`。任何 Critical/Important finding 都使最终 FAIL；不得自行修改文件。

## 1. 必读

1. T015、`docs/superpowers/plans/2026-08-07-oversampled-sync-semantic-smoke.md`；
2. `projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-discussion.md` §4；
3. Probe README、core、runner、focused tests；
4. artifacts 全套、T015 worker log 与 scientific report；
5. D010–D011、S003、H004、V007。

## 2. 必查 spec / science

- task-control PASS；仅 T015 白名单有 executor 写入，common/params/旧实验/Skill/四个 protected logs 未变；
- focused tests 重新 PASS；identity-only 重新 PASS；不得重新生成 grid 覆盖 canonical artifacts；
- estimator API/调用链不接收 truth；固定 visible、只换 truth metadata 时 B0/B1/B2/C output/trace/ledger 一致；
- 180 observations = 75 noiseless residual + 75 minus6db residual + 30 stress；每 cell 恰有四 method rows；
- observations/truth/results/surface index 的 cell/realization/rx/grid/score hashes 可闭合，无孤儿/重复；
- common score、固定 window、normalization、numeric tolerance 与 lexicographic tie-break 唯一；
- B1 和 C 不能只是共享同一 result object 或由 B1 直接调用 C；应从各自独立 traversal 得到同一完整 candidate set、
  score cube/argmax/tie-break。若实现只是别名，必须 FAIL；
- B0 符合 staged hard-decision 合同，B2 trace 非降并按 fixed-point/8轮停止；
- 从 method_results 独立重算每层 false-lock count/rate、G_C、coverage、stable 2x2 与 B1/C equivalence；
- stress 未混入 primary；minus6db/preamble/RRC span 均有 diagnostic claim ceiling；
- reducer 边界和 reason ordering 与 D010/T015 一致；科学终态只能为三者之一，semantic gate 优先；
- compute ledger 对 candidate visits 与 observation length 自洽；wall time 是 warm-up 后五次 median，不以大 O 伪装；
- full surfaces/plot/parameter provenance/script SHA/HEAD 和 artifact SHA 可重算；报告不把 deterministic grid rate
  外推为外场概率、论文数字或连续 estimator 等价。

## 3. 确定性命令

运行 task-control validator、focused pytest、identity-only（使用临时输出或不写 canonical artifacts）、JSON/JSONL/NPZ
parse、SHA256/reducer 独立脚本、`git diff --check`、`git status --short`、protected-path diff 与四 log hashes。
若需要临时脚本，只能放系统 temp 且最终删除，不得写 repo。

## 4. 报告格式

报告必须含：执行边界、spec verdict、quality verdict、test/identity 结果、artifact cardinality/hash closure、独立重算表、
B1/C independence 判定、compute/provenance/claim-ceiling 判定、protected boundary、findings、最终 PASS/FAIL/PARTIAL。
明确 verifier 名称与 blocker count。只写唯一 verifier report，不改任何 canonical/代码/artifact。
