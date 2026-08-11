# Task Brief: C1 A0 step-090 residual findings narrow verifier

> 来源: S001 / D009 / step-090 FAIL | 产出位置: `projects/thesis-fso/worker-logs/step-091-c1-a0-step090-narrow-verifier.md`
> 日期: 2026-08-10
> 唯一任务文档: 执行方只按本 T045 做窄复核，并读取下列中央 owner/step-090 作为证据

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 10
  action_class: FEASIBILITY_A0
  mission_checkpoint: CP010
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR（执行方先读）

你在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。step-090 已完成全量审查，结论为 `FAIL / P0/P1/P2=0/2/1`；此前 B2 source contract、strata/exposure/symmetry/budget 等问题均已 **CLOSED**。

**你的任务**：只验证 step-090 的 P1-1、P1-2、P2-1 是否被当前中央 report/YAML 唯一、fail-closed 地修复，同时核验 owner 快照、YAML parse、task-control 和受保护日志。

**产出**：`projects/thesis-fso/worker-logs/step-091-c1-a0-step090-narrow-verifier.md`。

**时间纪律**：8–10 分钟目标，12 分钟硬上限；到上限立即用现有证据给出 PASS/FAIL，不扩大审查面。

**最高纪律（违反一条即无效）**：

1. 只复核三个 residual findings；不得重开 step-090 已 CLOSED 的问题，也不得做新的 22-fact 全量审查。
2. 当前仍 CP010/epoch10；禁止 D0、adapter、C1-ext、MVE、held-out、仿真、科学实验、代码实现、web/search/download、commit/push。
3. 只允许新写 step-091 日志；不得修改中央 report/YAML、治理文件、源码或四个 `p05_run*.log`。
4. PASS 必须 P0/P1/P2=`0/0/0`；若发现修订引入新的、足以导致相反科学裁决的直接矛盾，才可按行号登记，不得借机扩成全量设计审查。

## 1. 背景（了解即可，不要对照评价已关闭项）

中央 owner：

- `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md`
- `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`
- 上轮独立审查：`projects/thesis-fso/worker-logs/step-090-c1-a0-contract-v3-verifier.md`

本次待核快照 SHA256：

- report：`046bb45a95bde5672270a552828e2a5730987b48ac681c5fcad86f44b8755f27`
- YAML：`6c1e228f892ac1981fd22d7c7e89e0247df5c2cece9a69798e4387da2b003a4b`

step-090 的 residual findings：

- P1-1：bootstrap/CI、cluster resampling、invalid denominator replicate 处理没有唯一冻结。
- P1-2：S3 pilot/decoder score normalization、dev fusion objective 与 lambda tie-break 没有唯一冻结。
- P2-1：report 末端把 clean false-action/fallback/goodput safety 误写成 D0 闭环项。

## 2. 任务详情

### 2.1 必答问题

1. YAML 是否可由 `yaml.safe_load` 解析，且上述两个 owner 的开始/结束 SHA 都等于本 brief 快照？
2. P1-1 是否 **CLOSED**：
   - raw row 必需字段、cluster key、逐 cell estimand 与 equal-cell macro 顺序是否明确；
   - 恰为 10,000 replicates、NumPy PCG64 seed `2026081001`、two-sided 95% percentile `2.5/97.5`；
   - 每 replicate 是否以 10 个 seed blocks 有放回重采样，并在 replicate 内重算 cell counts/estimands/macro；
   - recoverability/coverage 的 invalid replicate 定义、保留 NA、禁止 impute、最大 invalid fraction `0.05`、最小 valid `9500`、两个 terminal 和“CI 只用 valid reps”是否唯一且 fail-closed；
   - coverage 是否先逐 cell pooled counts，再 equal-cell macro，不能换成 pooled-all-cells 或 mean-of-ratios。
3. P1-2 是否 **CLOSED**：
   - pilot score 是否按 pilot observations 归一化；decoder score 是否在每个 candidate 的相同 full-frame coded-bit support 上归一化；
   - fusion 是否只在 dev seeds `8050–8059` 上，按 cell 算 MRR/top1 后三 cell 等权；
   - lambda 是否用唯一 lexicographic objective：先最大 fused macro MRR，再最大 fused macro top1，再取较小 lambda；test 前恰好输出一个 lambda。
4. P2-1 是否 **CLOSED**：report 是否把 D0 gate 写为 occurrence、coded damage/headroom、recoverability、B2 absorption、decoder-information increment、diagnostic identity/information/cost，并明确 clean false-action/fallback/goodput safety 只属于 policy-freeze 后 post-D0。
5. report 审查历史是否诚实登记 step-090 `0/2/1`、本轮三类精确修复与“D0 仍禁止”。

### 2.2 执行方式

1. 先验证 T045 task-control。
2. 记录 owner 初始 SHA；解析 YAML。
3. 只读 step-090 Findings 与当前 owner 的对应字段/段落，按 2.1 逐项做 CLOSED/OPEN。
4. 检查 `git diff --cached --name-only` 为空、四个日志 SHA 匹配；写 step-091 后再次核验 owner/protected SHA。
5. 不修文件；若 OPEN，给最小必需修复，不提出新设计。

### 2.3 产出格式（强制）

```markdown
# Step 091 — C1 A0 step-090 residual findings narrow verifier

> control / scope / snapshot / no-experiment receipt

## 1. Verdict
PASS/FAIL；P0/P1/P2=x/y/z。

## 2. Residual-finding closure
P1-1 / P1-2 / P2-1 各 CLOSED/OPEN，逐字段给证据行。

## 3. Determinism checks
YAML parse、bootstrap、invalid replicate、S3 fusion、report post-D0 boundary。

## 4. Findings
只列仍 OPEN 或本轮直接引入的新矛盾；无则明确 P0/P1/P2 均 0。

## 5. Control disposition
维持 CP010 修复，或允许主控另立 D/V/CP 考虑开放 D0；本日志不得直接授权 D0。

## 6. Protection receipt
owner 开始/结束 SHA、p05 4 SHA、staging、唯一写入、禁止动作。
```

## 3. 已知陷阱

1. `step-090` 的 owner SHA 是旧快照，不是本轮期待值；必须使用本 T045 给出的新 SHA。
2. `candidate ranking tie-break` 不能替代 `lambda hyperparameter tie-break`；必须核对 lexicographic dev objective。
3. invalid replicates “不超过 5%”不等于算法已冻结；还必须有 NA 处理、有效 replicate 下限、terminal 与 CI denominator。
4. D0 的 S4 是 diagnostic identity/information/cost，不应用 policy；不得再次要求 D0 提供 false-action/fallback/goodput safety。
5. 四个受保护日志的正确 SHA256：
   - `p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
   - `p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
   - `p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
   - `p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`

## 4. 验收

- [ ] T045/CP010 task-control PASS。
- [ ] 只复核 P1-1/P1-2/P2-1，三项逐一 CLOSED/OPEN。
- [ ] YAML parse，owner 初末 SHA 4/4 匹配。
- [ ] PASS 时 P0/P1/P2=`0/0/0`，且没有把 PASS 当 D0 直接授权。
- [ ] p05 4/4 匹配、staging empty、唯一新写 step-091。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-091-c1-a0-step090-narrow-verifier.md`
