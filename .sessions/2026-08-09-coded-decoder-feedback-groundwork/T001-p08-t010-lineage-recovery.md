# Task Brief: P08/R/R2 与 T010 decoder-feedback 证据血缘恢复

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-047-coded-decoder-lineage-recovery.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本任务书与其中列出的仓库文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 1
  action_class: RECOVER
  mission_checkpoint: CP001
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。任务是恢复旧 T010 C1/C2/C3 与 P08/P08-R/P08-R2 的有效/无效证据血缘，明确哪些只能作工程资产、哪些是本轮可重用事实、哪些绝对不能恢复。

**产出**：结构化事实报告写入上述 worker-log；聊天只回传 terminal、文件路径、最关键 5 条事实和异常。

**最高纪律**：

1. 只恢复事实，不提出新方法、不实现、不运行科学实验。
2. 以 `amends/supersedes/invalidates` 血缘判断 authority；mtime、文件更新日期或漂亮结论不是 authority。
3. 旧 P08/P08-R 科学数字默认无效；只有 P08-R2 corrected asset 中未被后续 D/V 推翻的 caller/source/测试事实可复用。
4. 每条承重事实必须给 `file:line`；数字须能指向 raw/artifact 或明确标 `PARTIAL/INVALID`。
5. 不修改 dormant 专题、源码、artifact 或四个 `p05_run*.log`。

## 1. 背景

旧预检 `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md` 在 ≤1 天 adapter 合同下把 C1/C2/C3 全部判 `REJECT/CODED_CHAIN_ASSET_BLOCKED`。本轮用户把预算扩到 3–7 天，但没有恢复任何旧科学结论。你的工作只回答“我们实际继承了什么”。

## 2. 任务详情

### 2.1 必读

- `.sessions/2026-07-20-research-direction-lab-system/T010-decoder-feedback-ccisp-method-construction-preflight.md`
- 同专题 `S019*`、`decisions.md` 中 D039-D040、`verifications.md` 中 V023、`mission-log.md` 对应 CP022-CP023
- `projects/thesis-fso/worker-logs/step-046-ch4-decoder-feedback-method-preflight.md`
- `.sessions/2026-07-23-research-direction-lab-longitudinal-test/` 中 P08/P08-R/P08-R2 对应 S、D、V、H 与 R010
- `projects/thesis-fso/worker-logs/` 中 P08/R/R2 对应 step 日志
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08*_*.py` 与 `projects/simulation/results/p08*` artifacts

### 2.2 要回答的问题

1. P08→P08-R→P08-R2→chronology correction 的完整 supersession 链及每一步根因。
2. 当前仍 VALID/PARTIAL/INVALID 的：coded-chain identity、receiver-visible prefix、decoder API、FER/BER 数字、oracle/headroom、chronology、统计合同。
3. T010 C1/C2/C3 的旧 classification、旧 reopen condition、collision 与 readiness 缺口。
4. 哪些旧数字/措辞绝对禁止进入本轮 Q#/Go/论文，哪些 source/API/test 事实可当 adapter 起点。

### 2.3 产出格式

```markdown
# Step 047 — P08/T010 lineage recovery
## Authority chain
| lineage | disposition | superseded by | current ceiling | evidence |
## Reusable facts
| fact | VALID/PARTIAL/INVALID | exact pointer | allowed use |
## Forbidden revivals
| claim/number | why invalid | authority pointer |
## C1/C2/C3 inherited record
| card | old class | action | collision | reopen condition | readiness gap |
## Artifact/source map
## Facts the master must independently verify
## Terminal
RECOVERY_COMPLETE / RECOVERY_CONFLICT
```

## 3. 已知陷阱

- V075 的 19/19 不证明 immutable pre-test chronology；后续 D051/V077 纠正必须进入血缘。
- `hard_out=True`、configured iterations 与实际 iteration trajectory/callback 是不同事实。
- P08-R2 的 partial engineering asset 不等于 decoder-feedback method evidence。
- 不把 T010 资产阻断解释成科学 Kill，也不因新预算自动改成 READY。

## 4. 验收

- [ ] P08/R/R2 至少 4 段 authority 血缘完整。
- [ ] 每个保留/禁止事实都有 `file:line`。
- [ ] C1/C2/C3 三卡均覆盖 action/collision/reopen/readiness。
- [ ] worker-log 不包含新方法建议或未经验证数字。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-047-coded-decoder-lineage-recovery.md`
