# Decision Records — Direction Lab 可遵守性与控制器试运行

## D001: 采用审计账本背书的最小 decision receipt 与 evidence gate

> status: active
> date: 2026-07-17
> 取代：无
> 被取代：无
> 依据：调研: `.sessions/framework-evolution/R002-direction-lab-design.md` + 验证: V002/V003 + 用户原话: `voice.md` 2026-07-17

### 决策

每次 controller 决策生成绑定 `decision_id`、`run_id`、`action`、canonical manifest hash 与 allow/blocked 状态的 receipt；operation 仅通过 `execute()` 返回携带 receipt 的结果 envelope；evidence gate 只接收能与审计账本逐字段核对的 receipt，并按 evidence ledger、promotion board、formal materials 三类目标限制动作。

### 理由

纯内存 token 无法支持恢复测试；完整签名/可信 registry 超出本轮最小 pilot。审计账本背书可用确定性接口验证“走过 controller”，同时保留跨实例恢复能力。

### 排除的替代方案

- 不采用纯内存 opaque token：新上下文或新进程无法恢复。
- 不采用自声明 receipt：调用方可伪造，不能证明经过 controller。
- 本轮不采用签名、密钥管理或不可变数据库：范围和复杂度超过 pilot。

### 影响范围

仅影响 `projects/simulation/verify/direction_lab_pilot/`、对应测试与本专题记录；不修改 canonical baseline、正式实验入口或论文材料。

### 来源

S002 / 用户明确任务约束

## D002: execute 结果必须有审计 execution 记录并防止 replay

> status: active
> date: 2026-07-17
> 取代：无
> 被取代：无
> 依据：验证: V004/V005 + critic: 独立 verifier 复核

### 决策

在 D001 receipt 之外，`execute()` 必须为实际 operation 结果写入 execution audit event 与 `result_hash`；evidence gate 必须同时核对结果 hash、execution event 和 destination 幂等性，篡改结果标记 `UNTRUSTED`，同一 receipt 在同一目标重放标记 `REPLAY`。

### 理由

V004 黑盒复核证明仅凭合法 decision receipt 可以承载伪造 result，也可以重复写入 ledger；这直接违反“只有 controller.execute 产生的结果可验收”。execution event 是不引入签名系统的最小 provenance 绑定，replay 门避免账本污染。

### 排除的替代方案

- 不把“调用方保证不篡改 envelope”当作验收门：黑盒已证明不可靠。
- 不在本轮引入签名、密钥管理或不可变数据库：仍列为完整性债务。

### 影响范围

仅影响 pilot controller、evidence gate、定向测试和本专题运行产物；不改变 canonical baseline 或正式材料。

### 来源

S002 / V004 独立 verifier 发现 / V005 修复后复核

触发原话：无（技术推导）
