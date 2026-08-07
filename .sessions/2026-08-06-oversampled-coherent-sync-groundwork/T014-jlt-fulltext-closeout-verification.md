# Task Brief: JLT 用户全文与 coverage terminal 独立验证

> 来源: S001 | 产出位置: `projects/thesis-fso/oversampled-sync-groundwork/jlt-fulltext-closeout-verifier-report.md`
> 日期: 2026-08-06
> 唯一文档: 本任务文件 + 指定 canonical artifacts

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 28
  action_class: FORMAL_COVERAGE_CLOSEOUT_VERIFICATION
  mission_checkpoint: CP015
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

独立验证用户提供 JLT 2025 IQ-skew 全文的 identity/action verdict，以及 D008/D032/current-state 的
coverage 处置是否证据一致。只读 canonical；只写 verifier report；不提交。

## 1. 必查事实

1. PDF/content/metadata/index 的 title、DOI、SHA、页数、行数一致；PDF可打开，content≥50行。
2. 全文是否确实显示 shared TS-A 上的顺序模块链；Eq. 16–23 是否仅输出 IQ-skew；是否存在单一
   `(frame,fractional τ,CFO)` objective/search。
3. T013 worker log/read note 的标准字段、七子表、实验数字、collision verdict 是否由正文支持。
4. formal D008、S001、topic-index、literature notes、Step 3/3.5 reports、H003、master-state 与 RDL
   D032/CP015/epoch28/registry 是否一致；历史 D007/H002/V005 必须保留历史血缘。
5. 用户原话只能支持 JOCN `USER_CONFIRMED_FULLTEXT_UNAVAILABLE`/停止重试，不得升级为 JOCN
   no-collision 或 exact novelty closure。
6. 未进入 Step 4a/实现/testbed/MVE/仿真，`common/`、`params.py`、Skill 与四个 protected logs 未变。

## 2. 确定性检查

- JSON/YAML parse；SHA256；`git diff --check`；staging/status；protected log hashes；stale-current grep。
- 明确列出初审 blocker；若 blocker>0，FAIL 且不得代修。主控修复后必须完整重跑。

## 3. 产出格式

报告必须含：identity、全文 action evidence、canonical/current-state、deterministic counts、blockers、
最终 `PASS/FAIL/PARTIAL`。不得修改任何 canonical 文件。

## 4. 验收

- [ ] task-control PASS；
- [ ] action verdict 由全文而非摘要支持；
- [ ] current-state 无 stale projection；
- [ ] claim ceiling 与用户原话边界正确；
- [ ] 独立 verifier report 已落盘。
