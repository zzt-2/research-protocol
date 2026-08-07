# Step 046 — T010 Ch4 decoder-feedback 方法构造预检执行日志

> 日期：2026-08-07
> 任务：T010
> 范围：local-only / design-only

## 实际执行

- 完整读取 T010，并以 epoch 35 / CP022 / D039 运行 task-control validator：PASS。
- 只读核对 topic/mission、method-production、inventory、U38/U39/U47、F4-A/F4-C、P08-R2、P05、
  CCISP caller 与 Ch5 方法包；未调用 WebSearch、下载或新论文精读。
- 沿 P08-R2 与 CCISP caller→callee 完成四项 callback readiness：
  - per-symbol extrinsic：`NEW_INFRASTRUCTURE`；
  - syndrome/CRC/failure causal state：`NEW_INFRASTRUCTURE`；
  - decoder→CPR/recovery callback：`NEW_INFRASTRUCTURE`；
  - iteration/latency/net-rate accounting：`NEEDS_SMALL_ADAPTER`。
- 完整构造 C1/C2/C3 三张 concept card，并逐卡核对七个 survivor 门与五字段 collision receipt。
- 三卡均因依赖至少两项 `NEW_INFRASTRUCTURE` 被拒绝；survivor=0，terminal=
  `CODED_CHAIN_ASSET_BLOCKED`。
- fresh-context 初验为 BLOCK（P0/P1/P2=0/2/1）：补齐三卡预注册主表、D028/D047
  detection→rollback/relock action-signature collision，并把执行前控制收据绑定到 commit
  `8110fc4cc2a129c856eea9819e0cc0d1908a8b99`；未改变 survivor 或 terminal。

## 产出

- 科学/设计产出：`projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md`
- 治理同步：S019/D040/CP023/V023/topic/registry/voice。

## 范围核对

- 未进入 GW，未实现或修改 coded chain/CCISP/common/params，未运行仿真，未写论文正文。
- 未创建 active carrier、METHOD_SIGNAL、Go 或 promoted method card。
- 四个既有 `p05_run*.log` 未修改、未暂存。
- fresh-context 复验最终 PASS（P0/P1/P2=0/0/0），允许统一提交；不 push。
