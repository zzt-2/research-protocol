# [S019] Ch4 方法槽位纠偏与 decoder-feedback 预检

> 2026-08-07 | 流程纠偏 / 方法构造准备 | 已完成
> 2026-08-07 | T010 本地方法构造预检 | 已完成，coded-chain asset blocked

## 目标

纠正 `SUPPORTING_ONLY` 被误算作长程方法进展的问题，并准备一个不跑实验、只判断方法形是否成立的
decoder-feedback CCISP 构造预检。

## 记录

- CP021 同时记录 `mission_method_delta=NONE`、`thesis_method_disposition=SUPPORTING_ONLY` 与
  `weight=ADEQUATE / drift=ALIGNED`。后两项对审计质量可以成立，对“填补 Ch4 方法槽位”的 mission
  却不成立。
- 对应失败模式为 M6 范围偏离，而不是 2A 科学裁决错误：P01/P02/T004 的 `SUPPORTING_ONLY`
  保持有效，但不能关闭方法槽位，也不应再获得下一轮包装机会。
- 对 `method-production.md` 只增加一个窄规则：开放方法槽位仅由 `THESIS_METHOD_READY` 或 authority
  显式映射的 task-local equivalent（如 `THESIS_ENGINEERING_METHOD_READY`）关闭；
  supporting/reject 进入 harvest 后必须轮换到 method-shaped construct。
- 当前 Ch3 CCISP 主方法和 Ch5 select-before-execute 工程方法已有 authority，Ch4 仍缺方法。
- T010 只读本地 coded/decoder/CPR 资产，构造并碰撞最多三条 decoder-feedback 动作链；不检索、
  不进入 GW、不实现、不仿真。最多保留一个 survivor，且 survivor 只能回 GW Step 1。
- T010 控制绑定 validator PASS。沿实际 caller→callee 审计后，逐符号 extrinsic、syndrome/CRC
  因果状态、decoder→CPR/recovery callback 均为 `NEW_INFRASTRUCTURE`；iteration/net-rate 的基础字段
  已有，但外层 latency 账本仅为 `NEEDS_SMALL_ADAPTER`。
- 已完整构造 C1 phase-hypothesis feedback、C2 extrinsic soft-symbol iterative CPR、C3
  syndrome-triggered recovery 三张卡，并逐卡完成算法、比较器、主图、消融、工期、claim ceiling 与
  collision receipt。三者都因至少两项 `NEW_INFRASTRUCTURE` 未过 survivor gate 5，survivor=0。
- 唯一终态为 `CODED_CHAIN_ASSET_BLOCKED`：这是本地资产 readiness 裁决，不是 decoder-feedback
  科学假设的 Kill，也不授权补接口、进入 GW、实现或仿真。
- fresh-context verifier 初验 BLOCK（0/2/1）后，只补三卡主表、D028/D047 action-signature collision
  与 pre-execution commit 收据；复验 PASS（P0/P1/P2=0/0/0），未改变 survivor 或 terminal。
- 专题膨胀审计为 19 个 S 文件；D039/T010 已显式给出本轮 scope change，故按默认规则追加 S019，
  不新建 S020。

## 决策引用

- D039：方法章节槽位只由方法终态关闭，并转入 decoder-feedback 正向构造预检（新建）
- D040：三条 decoder-feedback 方法形均受 coded-chain 新基础设施阻断（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（D039/T010 只授权本地 design/collision preflight）

## 后续

等待用户战略决定。不得自动建设 coded callback、进入 GW、实现、仿真或继续围绕该资产做包装闭环；
如需继续，必须显式选择扩大基础设施范围或更换 candidate source/research object。
