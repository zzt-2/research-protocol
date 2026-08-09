# Verifications — Coded decoder-feedback 方法主线 Groundwork

## V001: Step 1 terminal package 技术终验（语义映射待修）

> date: 2026-08-09
> 关联：S001 / D003–D004 / CP003–CP004 / T007–T010

### 验证项

- [x] 技术证据与 corpus：[由 fresh-context `/root/authority_terminal_verifier` 重跑 A/B] → mirror 28/28，93 raw→66 unique，50/66 published，must-read=6，sources=7，C1/C2 exact collision，replacement=0，P0/P1/P2=`0/0/0`
- [x] Git 与保护边界：[动态读取 HEAD receipt 和 HEAD T022，再与 fresh 文件比较] → `p05_run*.log` bytes/SHA 4/4 一致且一直 untracked/unstaged，无 forbidden scientific artifact 变更
- [ ] canonical problem 映射：[staged diff 独立审查对照 `stages/glossary.md` 与 `stages/gw-search.md`] → D003 的 `NO_VALID_PROBLEM` 未经 Step 3 M-C-A Q#，属于越级映射；已由 D004 修正，尚待 T011 fresh verification
- [ ] 治理收口：[检查 current owner、task snapshot、handoff checklist 与 V-template] → T009/H001/V001/report 已进入修复，尚待 T011 验证和 V002 接收

### 证据

`projects/thesis-fso/worker-logs/step-056-coded-decoder-authority-terminal-verification.md` 原始摘录：

```text
计数：P0=0 / P1=0 / P2=0。
四组 fresh-context 冻结检查均为 PASS。
integrated v2 输入为 8 个 C1 route、8 个 C2 route、1 个 reviewed mirror；raw=93、records=66
fresh 复算 published=50、must-read=6、sources=7、R2 C1/C2=2/2。
authority_result=HEAD_RECEIPT_T022_FRESH_MATCH_4_OF_4
```

同一日志暴露、后由 staged review 判为越级的原始接受行：

```text
terminal/canonical/adapter=STEP1_NO_METHOD_ACTION_SURVIVOR / NO_VALID_PROBLEM / false
```

D004 修正后的机器投影 fresh 读取：

```text
schema_version=coded-decoder-step1-integrated.v2.1
terminal=STEP1_NO_METHOD_ACTION_SURVIVOR
framework_disposition=STEP1_CANDIDATE_SET_EXHAUSTED
canonical_mapping=null
problem_disposition=NOT_EVALUATED_NO_Q_FORMED
```

验证链保留：T007/step-053=`FAIL 0/2/1` → T008/step-054 repair → T009/step-055=`FAIL 0/1/0`（`INVALID_TASK_CONTRACT`）→ T010/step-056 技术检查=`PASS 0/0/0`。T010 总耗时 `00:04:23.396`，小于 8 分钟。

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

已由 T011/V002 完成：D004 的语义层级、integrated v2.1、current owner 投影、T009 派发快照、H001 checklist、V001 模板以及保护边界均通过 fresh verification。V001 保持 PARTIAL 作为历史验证记录，不再单独支持终态关闭。

## V002: D004 语义/治理修正终验

> date: 2026-08-09
> 关联：S001 / D004 / CP004–CP005 / T011

### 验证项

- [x] Artifact 与定量收据：[fresh 解析 integrated v2.1 与 reviewed mirror，并独立复算] → 93 raw→66 unique、50 published、6 must-read、7 sources、93/93 provenance、R2 C1/C2=`2/2`、mirror 28/28 与 8/10/4/2/4 全一致
- [x] 语义层级：[fresh 对照 `stages/glossary.md` 和 `stages/gw-search.md`] → local=`STEP1_NO_METHOD_ACTION_SURVIVOR`、framework=`STEP1_CANDIDATE_SET_EXHAUSTED`、`canonical_mapping=null`、problem=`NOT_EVALUATED_NO_Q_FORMED` 合法；current owner 无越级 verdict
- [x] 治理与历史边界：[检查 registry/topic/master/S001/D004/mission/V001/H001/report/JSON、T009 EOF 与 V-template] → current 投影一致，旧 mapping 仅在显式 historical/superseded 位置保留，T009 快照、H checklist、V001 PARTIAL、v1 supersession 均合规
- [x] Git 与保护边界：[动态读取 HEAD receipt/T022、fresh 比较四个 p05 日志并审计 staging/status] → HEAD 正确，bytes/SHA 4/4 MATCH，四文件一直 untracked/unstaged，无 forbidden artifact 或 staging 漂移
- [x] 执行隔离与时限：[比较执行前后 cached/status 并记录计时] → verifier 唯一写入 step-057；最终复查 `00:04:08.356`，小于 8 分钟

### 证据

`projects/thesis-fso/worker-logs/step-057-coded-decoder-semantic-governance-verification.md` 原始输出：

```text
P0=0 / P1=0 / P2=0
A/B/C/D：全部通过
schema_version=coded-decoder-step1-integrated.v2.1
terminal=STEP1_NO_METHOD_ACTION_SURVIVOR
framework_disposition=STEP1_CANDIDATE_SET_EXHAUSTED
canonical_mapping=null
problem_disposition=NOT_EVALUATED_NO_Q_FORMED
raw_rows=93; records=66; published=50; must-read=6; source families=7
provenance=93/93; mirror=28/28; replacement.accepted=0
HEAD=1d76f917a89c719614aeefd7a165ab9819425978
p05 HEAD receipt/T022/fresh=4/4 MATCH
elapsed=00:03:34.523; final recheck total=00:04:08.356
verdict=PASS
```

Fresh verifier：`/root/t011_semantic_verifier`。本轮未联网、未实验、未进入任何下游科学步骤，唯一仓库写入为 step-057。

### 结论

PASS
