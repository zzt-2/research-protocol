# Task Brief: Coded decoder-feedback Step 1 修复后终态独立复验

> 来源: S001 / D003 / T007–T008 / CP003 | 产出位置: `projects/thesis-fso/worker-logs/step-055-coded-decoder-post-repair-verification.md`
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

## 目标与边界

Fresh-context 验收 T008 是否完整修复 T007 的 P1/P2，并判断 `STEP1_NO_METHOD_ACTION_SURVIVOR / NO_VALID_PROBLEM` 能否正式接收。只读检查仓库，唯一允许写入的是 step-055 worker log；不得修文件、联网、新检索、全文、Step 2、adapter、实现或实验。

硬上限 **8 分钟**。日志必须写开始/结束时间、elapsed、每组命令和 exit code。若时间不足，立即输出 `FAIL`，不得超时补做。

## 必读

- 本专题 `topic-index.md`、`S001`、`decisions.md`、`mission-log.md`、T008
- `projects/thesis-fso/master-state.md` coded decoder-feedback 控制段
- step-053 与 step-054 worker logs
- repaired integrated report
- reviewed mirror JSON、integrated v2 JSON、原 28-result mirror

## 冻结的四组检查

### A. Task-control、JSON 与 coverage

1. T009 task-control validator=`PASS`；三份 JSON 均可解析。
2. reviewed mirror 28/28；每条都有 priority/reason、合法 disposition、relation、claim ceiling、原路径/1-based row provenance。
3. disposition=`duplicate 8 / irrelevant 10 / strong neighbor 4 / baseline 2 / unknown 4`；原镜像未被补写 review 字段。
4. integrated v2 输入恰为原 8 个 C1 route JSON、8 个 C2 route JSON、1 个 reviewed mirror；raw=93、records=66、provenance pair=93 且无缺失/重复；published=50、must-read=6、sources=7、R2 C1/C2=`2/2`。
5. `Phase Estimation by Message Passing` 必须是独立 title key strong neighbor，只记录 possible alias，未并入 DOI `10.1007/978-3-540-27824-5_22`。

### B. Collision、replacement 与 claim ceiling

1. C1/C2 仍各有 abstract-level `CORE_ACTION_EXACT` receipt；TSP 2006 仍只为 strong neighbor。
2. 四个 UNKNOWN 均忠实保留，且现有 metadata/abstract 不含可识别 carrier-recovery action；因此它们不提供 corpus-backed replacement，而不是被当作 irrelevant。
3. 镜像新增 actionable rows 只加强 iterative joint decoding/phase estimation、soft-decision PLL 或 conventional synchronization 邻域；没有不同 action。
4. replacement=0、terminal/canonical/adapter=`STEP1_NO_METHOD_ACTION_SURVIVOR / NO_VALID_PROBLEM / false`；scope 只限本专题 action-survivor，不扩大成领域无问题、B2 已解决或 testbed 不可建。

### C. Governance consistency

registry、topic、S001、D003、CP003 mission 与 master 均应反映 T007 FAIL→T008 repair→T009 pending；权威数字统一为 93→66、50/66、6、7、replacement=0；Step 2/adapter/MVE/Contract/Execute/论文方法声称冻结。

### D. Git 与 protected files

1. HEAD 仍为 `1d76f917a89c719614aeefd7a165ab9819425978`，staging 为空。
2. 四个既有 `p05_run*.log` 未修改/暂存，SHA256 分别保持：
   - `p05_run.log`: `7843F079267293E8C1DF0EA063B63C0925BC48122B3890F664B6F5B59C93CF11`
   - `p05_run2.log`: `735E67765338986AE89B356E6FD986E8B0CAFF1FD5D9F75AC3D35DB14153338B`
   - `p05_run3.log`: `C7681D64E7C44C58199A27B37E8F072941EC71C5DA22C021E57A96BB6505B34D`
   - `p05_run4.log`: `95A154CC631E9EBF27D21583562A75F7D82FF871A9DE5658BAEE0CEEC0C221DE`
3. 五个 tracked litsearch pyc 仍只是不暂存噪声；不得纳入最终提交。没有 source/common/adapter/scientific experiment artifact 改动。

## 输出

`projects/thesis-fso/worker-logs/step-055-coded-decoder-post-repair-verification.md`，包含：P0/P1/P2 数量、四组逐项 PASS/FAIL 与 evidence、命令/exit ledger、唯一 verdict=`PASS`/`FAIL`、若 FAIL 的最小修复。聊天 ≤600 字，只回 verdict、P0/P1/P2、elapsed 与四组结果。
