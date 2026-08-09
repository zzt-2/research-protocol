# Task Brief: C1/C2/C3 动作碰撞、竞品与 Ch4 适配复核

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-048-decoder-feedback-candidate-recheck.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本任务书与其中列出的仓库文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 1
  action_class: PORTFOLIO_MAP
  mission_checkpoint: CP001
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你在指定证据 worktree。任务是用当前 contribution inventory、thesis spine 和 historical dead ends 重新审查 T010 C1/C2/C3，并在不做外部检索、不声称 Groundwork Go 的前提下，给主控一个最多两个候选的证据化收敛建议。

**产出**：写 `step-048` worker-log；聊天只回 terminal、建议 survivor 上限、文件路径、5 条关键理由。

**最高纪律**：

1. 本任务是 design/current-evidence recheck，不是 Step 1 search，不得把未检索竞品写成已确认。
2. 从 action signature 检索历史，不按候选名字；命中后必须回读原始 D/V/worker-log。
3. adapter、correctness、monitoring、LLR scalar calibration 都不算方法动作。
4. 候选最多两个，必须机制不同；没有合格项可报 0，不得为凑数保留。
5. 不修改任何 owner、源码或 artifact。

## 1. 必读

- `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md`
- `.sessions/2026-07-20-research-direction-lab-system/T010-decoder-feedback-ccisp-method-construction-preflight.md`
- `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`
- `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`
- `projects/thesis-fso/direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`
- `projects/thesis-fso/direction-lab/harvest/ch4-concept-method-batch-001.md`
- P05、F4-A/F4-C、D047 detection→recovery、D028 stale-state 相关原始 D/V/worker-log
- `thesis-lessons.md` TL-30–TL-33 与分类速查

## 2. 要回答的问题

逐卡核对：具体 M-C-A、deployable input→action→output、decoder runtime 时点、实际改变的 CPR/recovery 决策、P08/F4/P05/CCISP/传统 turbo/CRC repair 碰撞、strongest conventional comparator、strongest cheap alternative、最小 adapter、主图/消融/fallback、当前 READY/NEEDS_ADAPTER/HYPOTHESIS_ONLY/REJECT。

如果三卡均不合格，只允许从同一 corrected coded-chain 与直接动作缺口派生至多两张 replacement sketch；不得制造新 research object。

## 3. 产出格式

```markdown
# Step 048 — Candidate recheck
## Current contribution/dead-end map
## Card-by-card matrix
| field | C1 | C2 | C3 |
## Action-signature collision receipts
## Direct-competitor unknowns for Groundwork Step 1
## Provisional convergence
| rank | card | class | keep/reject | why | Step-1 falsifier |
## Thesis chapter capability checkpoint
## Master verification list
## Terminal
CANDIDATES_CONVERGED / NO_PROVISIONAL_CANDIDATE / EVIDENCE_CONFLICT
```

## 4. 验收

- [ ] 三卡的 9 个指定字段齐全。
- [ ] 每个历史碰撞有原始 `file:line`，不是 inventory 二手转述。
- [ ] provisional survivor ≤2，且明确“仅允许进入 Step 1，不是 Go”。
- [ ] strongest comparator/cheap alternative 未确认处明确标 unknown。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-048-decoder-feedback-candidate-recheck.md`
