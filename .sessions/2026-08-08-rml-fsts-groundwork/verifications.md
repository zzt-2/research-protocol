# Verifications — RML-FSTS Groundwork

## V001: T003 Step 1–2 独立终验

> status: PASS
> date: 2026-08-08
> 关联：S001 / D002 / R001 / R002
> verifier: fresh-context `/root/final_verifier`

### 验证范围

按 T003 §4.2 独立检查 12 项：专题结构与 registry、H003 三事实、Step 1 JSON/receipt、查询轮次与路线、Step 2 全文 identity/provenance/hash/bytes/lines、CORE 覆盖、terminal、literature owner/master-state、证据边界、Step 3+ 禁止项、上游历史保护、git/YAML/p05/no-push。

### 初审

`PARTIAL`，P0/P1/P2=`0/1/0`。唯一 P1 是 `121 unique / 71 published / 58.68%` 缺少可独立复算的 canonical identity ledger，且 Q1/Q2 的 raw/dedup 只有 receipt 记录、未明确说明 raw artifact 未持久化。其余 11 项 PASS。

### 唯一最小修复

未重跑检索、未增加 query、未改变 scientific terminal。新增正式 staged canonical ledger 与 Q1/Q2/Q3 retained 中间产物；receipt 明确 Q1/Q2 raw/dedup 是执行时同步记录的 stdout observation，不冒充不存在的 raw artifact。ledger 逐条记录 131 个合并输入、10 个重复移除、121 个唯一身份、71 个正式发表判定及本地索引指针。

### 复核结果

`PASS`，P0/P1/P2=`0/0/0`。独立复算 `123 + 8 = 131`、`131 - 10 = 121`、published=`71`、`71/121 = 0.586776… → 0.5868`；71 个正式发表 identity 的本地索引指针、123 个 query-origin ref、priority inputs 与三份 retained 中间产物 SHA256 均匹配。原 12 项全部回归 PASS。

### 结论

PASS。允许按 T003 一次性提交 Step 1–2 与治理同步；不授权 Step 3/3.5/4a、smoke、实现或仿真，不改变 object/package failure=`0/0`，不得 push。

## V002: T001 Groundwork Step 3 独立终验

> status: PASS
> date: 2026-08-09
> 关联：S002 / D004 / R003
> verifier: fresh-context `/root/step3_verifier`
> 证据报告：`projects/thesis-fso/worker-logs/step-3-rml-fsts-verifier.md`

### 验证范围

按 T001 §7.1 独立检查 12 项：仅 Step 3 边界；五篇 title/DOI/path/SHA/bytes 与 Yu adapter；5×标准字段、7 子表、通信参数与非 DRL N/A；五篇实验完备性与三篇写作架构；read-notes/read-log/literature owner 一致性；source/target 与 C3/C4 角色；缺失竞品承重边界；canonical Q# 四判据；Step 3 状态；literature/master/topic/registry/D004/H002 同步；failure=`0/0`；git/YAML/JSON/p05/禁区。

### 初审

`PARTIAL`，P0/P1/P2=`0/2/1`。两个 P1 分别为 L01/L02/L04 的 owner/read-log 相对 source path 无法无歧义解析到 receipt 冻结文件，以及 L02/L04 reader 将强制 Verification/Validation/Uncertainty 三轴误写成 Validity/Verifiability/Utility；一个 P2 是 Step 2 历史段仍以“当前状态”描述旧状态。其余 identity、字段、边界、Q1、机械门均通过。

### 唯一最小修复

未补文献、未改科学结论、未进入下游步骤。将 L01/L02/L04 owner/read-log 路径改为 receipt 的 shared absolute canonical，并在 L04 read-note 明确排除 worktree 内不同哈希副本；将 L02/L04 reader 统一为 Verification/Validation/Uncertainty=`2/2/2` 与 `2/2/1`；把旧状态句标明为“Step 2 结束时状态”。

### 复核结果

`PASS`，P0/P1/P2=`0/0/0`。三篇 shared canonical 3/3 存在且 hash/bytes 与 receipt 一致；五篇 reader 5/5 使用统一三轴并与 owner/read-note 汇总一致；literature/master/topic/registry/D004/H002 current view 一致；`git diff --check`、YAML/JSON parse、staged=0、四个 p05 日志 hash/no-stage、禁止路径 diff 全部通过。

### 结论

PASS。允许按 T001 一次性提交 Groundwork Step 3 产出与治理同步；Step 3.5 保持 NOT_STARTED，不授权 Step 3.5/4a、smoke、实现、仿真或 MVE，不改变 research-object/method-package failure=`0/0`，不得 push。

## V003: Step 3 主控接收语义纠偏复核

> date: 2026-08-09
> 关联：D005 / R003 / H003
> verifier: fresh-context `/root/q1_semantic_critic` + `/root/step3_integrity_audit`

### 验证项

- [x] 完整性：5/5 receipt/path/SHA/bytes、read-notes/read-log/owner 与 22 文件提交范围 → PASS。
- [x] Q1 A 方向：旧写法存在“稳定/足够=问题不存在”的 P1 歧义；改为 M 隐含依赖同一 lag 近似最优、该假设在 C 下被违反时 M 不足 → PASS。
- [x] 判据 3：Wang 2023 能承担 exact recent M；Enhanced 2024 是 2024 Optics Express task-matched comparator；项目既有 authority 明列 Optics Express 为光通信顶刊/允许保留的顶会顶刊，因此由 L02 闭合 2019+ 顶刊门，不依赖 Wang venue 等级 → PASS。
- [x] 阶段边界：A 仍 INFERENCE，crossover/failure/headroom 仍 UNKNOWN；Step 3.5/4a/实验均未启动 → PASS。

### 证据

`stages/glossary.md:18`；`projects/thesis-fso/master-state.md:190`；`.sessions/2026-06-20-problem-driven-redirection/decisions.md:983`；`.sessions/2026-06-04-advisor-review-revision/topic-index.md:94`；L01 `content.md:208,299`；L02 `content.md:404` 与 owner 的 L02 identity（Optics Express 32(15), 2024）；L04 `content.md:170`；critic 回执 `PARTIAL, P0/P1/P2=0/2/0`；integrity auditor 在 venue authority 闭合后的最终回执为 `PASS, P0/P1/P2=0/0/0`。修复后确定性 grep 显示 Q1 在 R003/owner/H003 同义，且未把 Wang venue 冒充顶刊。

### 结论

PASS。V002 的完整性/合同一致性结论保留；其 Q1 科学语义验收由 V003 修正。Step 3 completed 可维持，进入 Step 3.5 前置语义债已关闭。
