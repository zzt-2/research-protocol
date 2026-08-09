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
