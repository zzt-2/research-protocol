# Task Brief: Coded decoder-feedback HEAD-authority 终态复验

> 来源: S001 / D003 / T007–T009 / CP003 | 产出位置: `projects/thesis-fso/worker-logs/step-056-coded-decoder-authority-terminal-verification.md`
> 日期: 2026-08-09

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 3
  action_class: VERIFY
  mission_checkpoint: CP003
```
<!-- RDL-TASK-CONTROL:END -->

## 目标与硬边界

Fresh-context 重跑 terminal package 四组验收，并纠正 T009 的错误保护哈希合同。只读检查仓库；唯一允许写入 step-056 worker log。不得修改 T009/step-055、证据、治理或受保护文件；不得联网、新检索、全文、Step 2、adapter、实现、实验、commit 或 push。

硬上限 **8 分钟**；日志必须记录 start/end/elapsed 与每组命令 exit。时间不足直接 `FAIL`。

## 先做的 authority check

禁止手抄 T009 中的完整 SHA。必须用以下方式取得真正基线：

1. `git rev-parse HEAD` 必须为 `1d76f917a89c719614aeefd7a165ab9819425978`；
2. `git show HEAD:projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-reopen-input-receipt.json`，解析 `protected_log_sha256`；
3. 交叉核对 `git show HEAD:.sessions/2026-08-08-rml-fsts-groundwork/T022-step4a-reopen-input-independent-verifier.md` 中的 bytes/SHA；
4. 比较当前四个 `projects/simulation/explore/cma-fade-divergence/p05_run*.log` 的 bytes/fresh SHA、mtime、untracked/unstaged 状态。

若 HEAD receipt、T022 与 fresh 文件一致，T009 D finding 的根因应标为 `INVALID_TASK_CONTRACT`，不是 file mutation；step-055 历史 FAIL 保留。

## 四组冻结检查

### A. JSON / coverage

- task-control validator PASS；原 mirror、reviewed mirror、integrated v2 可解析。
- reviewed=28/28，required fields/provenance 完整；disposition 8 duplicate / 10 irrelevant / 4 strong neighbor / 2 baseline / 4 unknown。
- 17 input paths；93 raw、66 records、93 unique provenance pairs 全覆盖；50 published、6 must-read、7 sources、R2 C1/C2=`2/2`。
- `Phase Estimation by Message Passing` 为独立 title key strong neighbor，仅 possible alias，不与 Springer DOI 合并。

### B. Collision / replacement

- C1/C2=`CORE_ACTION_EXACT`；TSP 2006=`STRONG_NEIGHBOR`。
- 四个 UNKNOWN 保留且没有可识别 action，不被冒充 irrelevant，也不提供 corpus-backed replacement。
- replacement=0；terminal/canonical/adapter=`STEP1_NO_METHOD_ACTION_SURVIVOR / NO_VALID_PROBLEM / false`；claim ceiling 只限本专题 Step-1 action survivor。

### C. Governance

registry/topic/S001/D003/mission/master 应一致记录 `T007 corpus FAIL → T008 repair → T009 invalid hash-contract FAIL → T010 pending`，权威数字 93→66、50/66、6、7、replacement=0；全部下游冻结。

### D. Git / protection

- HEAD 正确、staging 为空；fresh p05 bytes/SHA 必须与从 HEAD receipt/T022 动态读取的值一致，mtime 仍早于本专题且未暂存。
- 五个 tracked litsearch pyc 只是 unstaged noise，最终提交不得纳入；无 source/common/adapter/scientific-experiment artifact 变更。

## 输出

写 `projects/thesis-fso/worker-logs/step-056-coded-decoder-authority-terminal-verification.md`：P0/P1/P2、authority-source receipt、A/B/C/D 逐项 PASS/FAIL、命令/exit ledger、唯一 verdict=`PASS`/`FAIL`、FAIL 时的最小修复。聊天 ≤600 字，只回 verdict、P0/P1/P2、elapsed、authority result 与四组结果。
